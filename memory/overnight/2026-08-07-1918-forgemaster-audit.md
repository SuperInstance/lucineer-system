# Forgemaster Overnight Audit — 2026-08-07 19:18 AKDT

## Repo Overview
- **Path:** `/home/eileen/projects/forgemaster/`
- **Purpose:** Build orchestration system — recipes, steps, artifacts, build queues, monitoring
- **Language:** Python 3.10+ 
- **Test suite (before):** 332 tests, all passing
- **Test suite (after):** 359 tests, all passing (+27 new, +9 skipped)

## Bugs Found & Fixed

### BUG-1: Stale error on retry success (MEDIUM)
When a step failed and was retried successfully, `step.error` still contained the old error message. The `_execute_step` method didn't clear the error field on success. This meant build reports could show errors for steps that ultimately succeeded.

### BUG-2: Uninformative error when action returns False (LOW)
When a step's action returned `False`, the error message was `None` — producing messages like `"Step 'X' failed: None"`. Now sets a meaningful default error.

### BUG-3: Transitive dependency skip propagation (MEDIUM)
The build system checked for FAILED upstream steps but not SKIPPED ones. A step whose dependency was SKIPPED (because *its* dependency FAILED) would still attempt to run. Now properly propagates SKIP status through the dependency chain.

### BUG-4: Silent recipe overwrite (LOW)
`Forge.submit()` silently overwrote recipes with the same name. Now emits a warning.

## Tests Added (27 new)
- Stale error cleared on retry success (3 tests)
- False-action sets meaningful error (3 tests)
- Transitive dependency skip chains (5 tests)
- Diamond dependency patterns (1 test)
- Deep chain all-skipped (1 test)
- Duplicate recipe names (2 tests)
- Step timeout field (3 tests)
- Error propagation: ValueError, TypeError, custom exceptions (4 tests)
- Empty recipe execution (3 tests)
- ForgeConfig propagation (3 tests)
- Mixed build batch reporting (1 test)

## Files Changed
- `forgemaster/forge.py` — bug fixes
- `forgemaster/queue.py` — bug fixes
- `tests/test_bugfixes.py` — new test file (452 lines)

## Commit
- `3e7b7a5` — pushed to main
