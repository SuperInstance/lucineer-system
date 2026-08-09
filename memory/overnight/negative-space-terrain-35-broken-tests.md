# Negative Space: terrain — 35 Broken Tests, Zero CI Signal

**Date:** 2026-08-09 04:03 UTC
**Found during:** Overnight loop 1, technical pass

## The Finding

`terrain` has 74 tests. 35 of them were failing. Nobody noticed.

The tests expected files at `/tmp/terrain/rooms.mud` but nothing in the test suite or CI actually copied the repo files there. The tests were written assuming a manual setup step that was never documented or automated.

This means:
1. The CI workflow was passing despite 35 failing tests (or not running them)
2. Anyone cloning the repo and running `pytest` would see 35 red failures
3. Nobody flagged this because the repo is low-traffic

## The Fix

Added a session-scoped pytest fixture (`setup_terrain_files`) that copies `rooms.mud`, `scene.json`, and `terrain_core.py` from the repo root to `/tmp/terrain/` before any tests run. Simple, obvious, and should have been there from the start.

**Before:** 35 fail, 39 pass
**After:** 74 pass, 0 fail

## The Pattern

This is the same pattern seen across the fleet: tests written against absolute paths (`/tmp/terrain/`) instead of relative paths or fixtures. The test suite works on the original developer's machine but breaks for everyone else. The CI either doesn't run or doesn't report.

## The Meta-Finding

The fleet has **many repos with silently broken tests**. This is negative knowledge — things the system "knows" are broken but doesn't report. A fleet-wide test census would reveal dozens of these.

The ship's sensors can't see what they're not pointed at. The test runner is a sensor. If nobody reads its output, it's a sensor pointed at the floor.
