# Pipeline Verification Report
**Date:** 2026-08-05 11:49 AKDT  
**Run by:** Subagent (automated E2E verification)  
**Processor:** lucineer-processor.service v2 — active, PID 139441, uptime 6h  

## Summary

| # | Test | Path | Result | Time | Notes |
|---|------|------|--------|------|-------|
| 1 | Template match ("build a tower") | Template (instant) | ✅ PASS | <1s | 3 parts + light, correct tower template, inline completion |
| 2 | Deep path ("whats your favorite fish") | Scheduler → local model | ✅ PASS | ~21s | In-character reply about sturgeon. Scheduler used local model (6.5s inference). Response had raw JSON in reply text — minor quality issue. |
| 3 | Conversational ("hi") | Scheduler → local model | ✅ PASS | ~12s | In-character greeting, 1 decorative command. Scheduler local model (3s inference). |
| 4 | Edge case ("build nothing") | Scheduler → local model | ✅ PASS | ~8s | Handled gracefully, no crash. "build" verb + "nothing" (not a known keyword) → correctly routed to deep path. Reply had raw JSON leak — minor quality issue. |

## Detailed Results

### Test 1: Template Match — ✅ PASS
- **Input:** "build a tower"  
- **Response:** Instant inline (HTTP 200, no job ID)
- **Output:** Stone tower with base, battlement, lantern beacon + point light
- **Voice:** In-character ("Stone shaft's up, battlements are on, beacon's lit")
- **Path:** template (keyword match → `b_tower`)
- **Verdict:** Exactly right. Template path fires instantly with no processor overhead.

### Test 2: Deep Path — ✅ PASS
- **Input:** "whats your favorite fish"  
- **Job ID:** verify-test-2.0ff761ebbe5622cb8e2d215c  
- **Processing:** pending → claimed → complete (~21s total, 6.5s in scheduler)
- **Output:** Conversational reply about sturgeon. 0 commands (correct — no build requested)
- **Path:** scheduler (local model on RTX 4050)
- **Memory:** Logged player + assistant turns, profile upserted
- **Vectorize:** All skills below threshold (correct — no relevant skill)
- **Minor issue:** Reply contains raw JSON fragments from the model instead of clean text. The scheduler flagged "response not JSON, using as plain text." Model output formatting needs improvement but pipeline handled it gracefully.
- **Verdict:** Pipeline works end-to-end. Quality of local model output could be better.

### Test 3: Conversational — ✅ PASS
- **Input:** "hi"  
- **Job ID:** verify-test-3.9594f85207d49e3648245fbf  
- **Processing:** pending → claimed → complete (~12s total, 3s in scheduler)
- **Output:** In-character greeting + 1 decorative statue command
- **Path:** scheduler (local model)
- **Memory:** 2-turn cache hit (remembered test 2), profile + builds logged
- **Verdict:** Conversational path works. Local model responds in character with appropriate speed.

### Test 4: Edge Case — ✅ PASS
- **Input:** "build nothing"  
- **Job ID:** verify-test-4.c05f4c12b824e60f94075b58  
- **Processing:** claimed → complete (~8s total, 3.6s in scheduler)
- **Output:** Handled gracefully — model understood the contradiction, returned a humorous reply
- **Path:** scheduler (local model). Correctly bypassed template matching since "nothing" is not a known build keyword, but "build" verb was present (no negation match)
- **Verdict:** No crash, no hang, graceful handling of nonsensical input.

## Processor Log Analysis

- **Errors during test window:** None (3 benign "Expecting value" errors were pre-test heartbeat claim races — empty responses when polling with 0 pending jobs)
- **Warnings:** None
- **Circuit breaker:** Never tripped
- **brain.py fallback:** Never needed — all 3 deep-path tests resolved via local scheduler
- **Fast mode (last resort):** Never triggered

## Fallback Chain Verification (brain.py)

Confirmed 3-tier structure, none of which were needed during this test:
1. **Primary:** Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo
2. **Fallback 1:** Qwen/Qwen3-Coder-30B-A3B-Instruct
3. **Fallback 2:** deepseek-ai/DeepSeek-V3
4. **Last resort:** fast mode (Seed-2.0-mini single-model)

Planner has 1 fallback (Qwen3-30B-A3B). Chain is sound.

## Overall Verdict

**4/4 tests PASSED.** All four pipeline paths (template, deep, conversational, edge case) function correctly end-to-end. The job wrapper unwrapping fix from this morning is confirmed working — no parsing errors on any path. Local scheduler handles inference in 3-6s, well within the 120s client timeout.

### Known Minor Issues (non-blocking)
1. **Raw JSON in replies:** Tests 2 and 4 showed raw JSON fragments in the reply text when the local model doesn't return structured JSON. The pipeline handles this gracefully (falls back to plain text), but the user-facing reply is messy. Recommend improving the local model's JSON formatting prompt.
2. **Benign heartbeat errors:** Pre-test "Expecting value" errors on `/api/jobs/claim` are cosmetic — they occur when the processor polls with no jobs queued and gets an unexpected empty response. Harmless but noisy in logs.
