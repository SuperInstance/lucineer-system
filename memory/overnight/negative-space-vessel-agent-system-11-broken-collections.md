# Negative Space: vessel-agent-system — 11 Broken Test Collections

**Date:** 2026-08-09 05:00 UTC
**Found during:** Overnight loop 3, technical pass

## The Finding

`vessel-agent-system` has 875 collected tests but 11 test files fail to import:

### Root Causes (3 layers deep)
1. **Missing pip dependencies:** `websockets`, `aiohttp`, `h3` — not listed anywhere (no requirements.txt, no setup.py, no pyproject.toml)
2. **Import path mismatch:** Tests in `aelma/tests/` import from `twin.*` but pytest from repo root can't resolve them
3. **API drift:** Tests reference `MOBInactiveError`, `PositionValidationError` — custom exception classes that were removed from the source. The module now raises plain `ValueError`/`RuntimeError`

### The Pattern
This is the flagship vessel repo. It's the most complex, most connected, and most broken test suite in the fleet. Three separate categories of failure:
- **Missing deps:** No requirements file at all
- **Import structure:** Tests designed to run from a subdirectory, collected from root
- **API drift:** Tests written against an earlier API that was simplified without updating tests

### What This Means
The vessel-agent-system is the ship's blueprint. If the blueprint's tests don't run, the ship's integrity is an article of faith. 875 tests collected but the 11 that fail are the ones testing the newest features (mob detector, quota manager, report generator, watchers).

### Recommended Fix
1. Add `requirements.txt` with: websockets, aiohttp, h3, and any other deps
2. Add repo-root `conftest.py` that adds `aelma/` to sys.path
3. Reconcile test expectations with actual API — either add the custom exceptions back or update the tests

## Status
**Partially fixed:** Installed missing deps (reduced from 25→11 collection errors). Full fix requires API reconciliation work that's beyond a single overnight loop.
