# Branch Coverage Report — lucineer-brain

**Date:** 2026-08-06  
**Command:** `python3 -m pytest --cov --cov-branch --cov-report=term-missing -q`  
**Python:** 3.14.4  
**Tests:** 225 passed

---

## Summary

| File | Stmts | Miss | Branch | BrPart | Cover |
|------|-------|------|--------|--------|-------|
| brain.py | 425 | 14 | 150 | 15 | **95%** |
| tests/test_brain.py | 363 | 2 | 24 | 1 | 99% |
| tests/test_coverage_expansion.py | 265 | 2 | 10 | 4 | 98% |
| tests/test_health_cache.py | 98 | 0 | 0 | 0 | 100% |
| tests/test_pipeline_coverage.py | 522 | 0 | 4 | 1 | 99% |
| **TOTAL** | **1673** | **18** | **188** | **21** | **98%** |

---

## Missing Lines in brain.py (14 statements, 15 partial branches)

### Line 201→199 — `call_model` retry loop fallthrough
**Location:** `call_model()`, retry loop tail  
**Code:** `raise RuntimeError(f"Failed after {max_retries} retries: {last_error}")`  
**Why uncovered:** Every test either succeeds or raises on the first error. No test exhausts all retries with a non-429, non-timeout error that falls through the loop. The `for` loop's implicit `else` path (loop completes without `return` or `raise`) is never reached because the last retry always raises inline.

### Line 301 — `extract_json` depth-counting inner loop
**Location:** `extract_json()`, brace-matching fallback  
**Code:** The candidate extraction `json.loads` success path inside the depth counter  
**Why uncovered:** Most tests hit the direct `json.loads()` on the first try or the markdown-fence path. The embedded-in-prose path that finds a `{...}` block by counting depth is rarely the successful extraction route.

### Line 316→318 — `extract_json` array fallback after object fails
**Location:** `extract_json()`, `[...]` search after `{...}` fails  
**Why uncovered:** When JSON is embedded in prose, it's almost always an object `{...}`. Arrays embedded in prose that can't be parsed directly are uncommon in model output.

### Line 338→333 — `call_model` HTTPError non-retry branch
**Location:** `call_model()`, HTTPError handler  
**Why uncovered:** The branch where `e.code == 429` is false AND it's the last attempt. Most tests either test 429 (retry) or a 500 on first attempt (which raises immediately — but the branch counting for `attempt < max_retries - 1` vs the final attempt creates a partial branch).

### Line 670 — Deep mode planner fallback chain dedup
**Location:** `stage_plan()`, deep mode fallback chain construction  
**Code:** `if fb_model not in (MODELS["deep"], MODELS["planner"])` — the True branch  
**Why uncovered:** `PLANNER_FALLBACKS` contains `Qwen/Qwen3-30B-A3B`, which equals `MODELS["planner"]`. The dedup filter excludes it, so the True body (appending the fallback) is never entered in deep mode.

### Line 676 — Standard mode planner fallback dedup (True branch)
**Location:** `stage_plan()`, standard mode  
**Code:** `if fb_model != MODELS["planner"]` — True (append)  
**Why uncovered:** Same as above. `PLANNER_FALLBACKS[0]` IS `MODELS["planner"]`, so the dedup always filters it out. The branch that would append a different fallback model is never taken.

### Line 874 — `stage_hermes` verbose check on unparseable output
**Location:** `stage_hermes()`, `if verbose_check():`  
**Why uncovered:** Hermes unparseable output tests run without verbose mode. The verbose=True path through Hermes failure hasn't been tested.

### Line 940 — `stage_hermes` RuntimeError verbose print
**Location:** `stage_hermes()`, `print(f"⚠ Hermes unavailable...")`  
**Why uncovered:** The RuntimeError path in Hermes is tested but not with verbose mode enabled.

### Line 955 — `verbose_check` function body
**Location:** `verbose_check()`  
**Why uncovered:** The function itself — the `getattr` call line. This is likely a coverage artifact from the function being called via attribute assignment rather than direct invocation in some paths.

### Line 970 — `run_pipeline` verbose print for planner failure
**Location:** `run_pipeline()`, `if verbose: print("✕ Planner produced no steps...")`  
**Why uncovered:** Planner-no-steps fallback is tested in non-verbose mode only.

### Lines 975-978 — `run_pipeline` planner fallback result construction
**Location:** `run_pipeline()`, setting `result["_pipeline"]["planner_failed"]` and mode  
**Why uncovered:** The `run_fast` mock in the planner-failure test returns a dict with `_pipeline` already set. The real code path that constructs `_pipeline` from scratch is partially covered.

### Line 989 — `run_pipeline` verbose coder-fallback print
**Location:** `runpipeline()`, `if verbose: print("✕ All coder models exhausted...")`  
**Why uncovered:** Coder-exhaustion fallback is tested in non-verbose mode only.

### Line 1080 — `run_fast` verbose Hermes print
**Location:** `run_fast()`, `if verbose: print("→ Fast mode + Creative...")`  
**Why uncovered:** Fast+creative verbose mode not tested.

### Line 1103 — `run_fast` safety verbose print
**Location:** `run_fast()`, `if verbose: print("→ Fast mode + Safety check...")`  
**Why uncovered:** Fast mode safety check verbose path not tested.

### Line 1347 — `if __name__ == "__main__": main()`
**Why uncovered:** Module is imported, never run directly. Standard Python coverage artifact.

---

## Branch Analysis

### Critical Branches (well-covered)
- ✅ **429 retry logic** — fully covered (retry-then-succeed, retry-then-fail)
- ✅ **Timeout retry logic** — covered
- ✅ **Empty content → reasoning_content fallback** — covered
- ✅ **Safety fail-open** — covered
- ✅ **Safety block unsafe** — covered
- ✅ **Planner fallback chain** — covered for both standard and deep modes
- ✅ **Coder fallback chain** — primary success and fallback success covered
- ✅ **Hermes preserves commands** — covered
- ✅ **Intent parse fallback** — covered
- ✅ **Planner-no-steps → fast mode** — covered
- ✅ **Coder-all-failed → fast mode** — covered

### Gap Categories
1. **Verbose-mode paths (6 lines):** Every verbose print statement is a branch. Tests exercise the logic but not the verbose output. Low risk — verbose is diagnostic only.
2. **Dedup filter dead branches (2 lines):** The fallback chain dedup filters are structurally unreachable because the fallback list contains the primary model. The filters are defensive code.
3. **Loop fallthrough edge (1 line):** The `call_model` post-loop RuntimeError is unreachable in practice — the last retry always raises inline.
4. **JSON extraction edge (2 branches):** Depth-counted array extraction after object extraction fails. Rare in practice.
5. **Module entry point (1 line):** Standard Python artifact.

---

## Fault Injection Test Targets

The following fault scenarios are NOT covered by existing tests and should be added:

1. **TimeoutError at each pipeline stage** — currently only RuntimeError is tested. `call_model` can raise RuntimeError wrapping a timeout, but the pipeline stages should handle it gracefully at every stage boundary.
2. **Empty 200 OK responses** — model returns valid HTTP 200 with empty `content` string that bypasses the `call_model` empty check (e.g., content is whitespace-only).
3. **Malformed JSON from model** — model returns 200 OK but body is not valid JSON at all. Currently `extract_json` handles this, but no test chains through `stage_intent → extract_json returns None → fallback` with truly malformed (non-JSON, non-markdown) output at every stage.
4. **429 rate limit cascades** — verify the full fallback chain: primary coder → fallback 1 → fallback 2 → fast mode.
5. **Fallback chain activation when primary model fails** — need explicit tests that the `used_model` in `_meta` reflects the fallback, not the primary.
6. **Safety check always runs** — verify safety runs even when coder falls back to fast mode, even when creative mode wraps with Hermes, even when planner fails.

---

## Recommendation

Current coverage at **95% statement / 98% overall** is strong. The fault injection tests should target:
- The 6 verbose-mode branches (easy wins — just add `verbose=True` to existing test patterns)
- The fallback chain verification (assert which model was used)
- Cross-stage fault propagation (timeout at stage 1 vs stage 2 vs stage 3)
- Safety-check invariant (runs in every code path, including failure cascades)

These are quality-of-life improvements, not critical gaps. The core failure handling is well-tested.
