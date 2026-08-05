# Playtest Comparison Report — 2026-08-05

## Message Unwrapping Bug Fix: Before vs After

**Scenario:** `edge-cases` (all 3 personas)
**Bug fixed:** Processor wasn't reading the `message` field from job payloads, causing all deep-path (non-template) jobs to time out forever.

---

## Summary: The Fix Works

| Metric | Before (Aug 3) | After (Aug 5) | Delta |
|--------|---------------|---------------|-------|
| **Total interactions** | 13 | 18 | +5 |
| **Timeouts** | 13 (100%) | 0 (0%) | **FIXED** |
| **Jobs completed** | 0 (0%) | 16 (89%) | +16 |
| **Job creation failures** | 0 | 2 | +2 |
| **Avg quality score** | 1.0/10 | 6.9/10 | +5.9 |
| **Avg response time** | ~120s (all timed out) | 13.3s | — |
| **Build commands generated** | 0 | ~15 total | — |
| **Voice in character** | 0% (no replies) | 67-100% | — |

**Verdict: The message unwrapping fix completely resolved the timeout issue.** Every single deep-path job now completes instead of hanging indefinitely.

---

## Per-Persona Breakdown

### Explorer
| Metric | Before | After |
|--------|--------|-------|
| Errors/Timeouts | 4/4 (100%) | 0/6 (0%) |
| Avg round-trip | 84s (all timeouts) | 13.3s |
| Avg quality | 1/10 | 7.8/10 |
| Best quality | 1/10 | **10/10** (portal build) |
| Build commands | 0 | 5 (portal) + others |
| Voice in character | N/A | 67% |

**Notable:** The "build a portal to another dimension" message got a 10/10 — 5 build commands (4 parts + 1 light), in-character reply, 9.4s. Explorer's edge-case messages (`build nothing`, `what's your name?`, `can you fly?`, `tell me a story`) all completed with conversational responses.

### Builder
| Metric | Before | After |
|--------|--------|-------|
| Errors/Timeouts | 3/3 (100%) | 2/6 (33%) |
| Avg round-trip (non-error) | 121s (all timeouts) | 17.0s |
| Avg quality | 1/10 | 5.3/10 |
| Voice in character | N/A | 100% |

**Notable:** 2 job creation failures (not timeouts) on `build a house with negative dimensions` and `make the tower infinitely tall`. These failed at the worker relay level (no jobId returned), not at the processor — likely input validation issues. The 4 jobs that did create completed successfully with good in-character voice. The builder persona's responses stayed in a "foreman/scrap tower" theme nicely.

### Newcomer
| Metric | Before | After |
|--------|--------|-------|
| Errors/Timeouts | 6/6 (100%) | 0/6 (0%) |
| Avg round-trip | 122s (all timeouts) | 11.7s |
| Avg quality | 1/10 | 7.3/10 |
| Build commands | 0 | ~5 total |
| Voice in character | N/A | 67% |

**Notable:** Perfect completion rate. Even `h` (single character) and `...` (just dots) got meaningful responses with build commands. All 6 edge-case messages completed in under 15s each.

---

## Known Issues (Separate from the Bug Fix)

1. **Response repetition / context leakage:** Some responses seem to bleed between sessions. E.g., Explorer's "I don't want to build anything" got a reply about flying, and "tell me a story" also mentioned flying. The model may be caching or confusing context across jobs.

2. **JSON in replies:** Many responses include raw JSON in the reply text (the `reply` field contains `{"reply": "...", "commands": [...]}`). This is a response parsing issue in the processor — the model output isn't being properly unwrapped before being stored. **This is likely the same class of bug as the original message unwrapping issue, but on the output side.**

3. **Job creation failures:** Builder's `negative dimensions` and `infinitely tall` messages failed at the relay level (HTTP request returned no jobId). May be a payload validation issue or the worker rejecting certain message content.

4. **Low build command counts:** Most responses have 0-2 build commands. The "portal" build (5 commands) was the exception. Brain.py model fallback issues are known and being fixed separately.

5. **Voice inconsistency:** Lucineer sometimes introduces as "foreman of this workshop" and other times "foreman at this construction site" — personality coherence needs work.

---

## What Matters Most

> **Do jobs COMPLETE now instead of timing out?** ✅ YES — 16/18 completed (89%). The 2 failures are job *creation* errors (relay-side), NOT processor timeouts. Zero jobs stuck in pending.

The message unwrapping fix is confirmed effective. The deep path (non-template messages) now processes successfully.
