# Negative Space: vessel-agent-system — 13 Broken Test Modules

**Date:** 2026-08-07 23:42 AKDT

## The Finding

`vessel-agent-system` is a large repo (316 tracked files) with 201 collectible tests, but 13 test modules are broken due to missing dependencies. The test suite cannot fully run.

## What's Broken

13 modules fail to import during pytest collection:
- `aelma/bridge/tests/test_bridge.py` — `ModuleNotFoundError: No module named 'websockets'`
- `aelma/build_claude_bridge/tests/test_bridge.py` — same
- `aelma/build_kimi/tests/test_bridge.py` — same
- `aelma/build_kimi/tests/test_fishing_modes.py`
- `aelma/build_kimi/tests/test_telemetry_query.py`
- `aelma/build_kimi/tests/test_trip_summary.py`
- `aelma/build_kimi/tests/test_twin.py`
- `aelma/build_kimi/twin/environmental/tests/test_stewardship.py`
- `aelma/build_kimi/twin/safety/tests/test_crew_safety.py`
- `aelma/build_kimi/twin/sensors/tests/test_nmea_udp_capture.py`
- `aelma/build_kimi/twin/tests/test_crew_fatigue.py`
- `aelma/build_kimi/twin/tests/test_equipment_monitor.py`
- `aelma/test_twin_server.py`
- `aelma/tests/test_mob_detector.py`

## Root Cause

`websockets` Python package is not installed. Other missing dependencies likely exist. The repo's requirements/dependencies are not fully specified or not installed in the current environment.

## Impact

- Any test that CAN be collected (88 tests in build_claude) may pass or fail, but the broken modules are invisible to CI
- The `build_kimi` subsystem has the most broken tests (8 modules) — this is the Kimi-built vessel twin, possibly using different dependencies than the Claude-built version
- The `bridge` subsystem is completely untestable — this is the NMEA/signalk bridge that connects the vessel to the agent layer. Untestable bridge = uncertain vessel-agent communication.

## What To Do

1. `pip install websockets` and see what else breaks
2. Create a requirements.txt or pyproject.toml with all dependencies
3. Consider splitting the repo — it contains at least 3 distinct systems (bridge, build_claude, build_kimi) with different dependency graphs
4. The `--ignore` flags can make pytest skip broken modules, but that's hiding the problem

## The Pattern

The fleet has a dependency management pattern: repos that grow organically accumulate dependencies that aren't declared. The test suite becomes a minefield where some paths work and others don't. The first time you run `pytest` without `--ignore`, it crashes.

This is the same pattern as the hermit crab's shells — each system builds its own home with its own materials, and the homes aren't compatible. The Claude-built twin uses one set of packages. The Kimi-built twin uses another. They live in the same repo but they can't share a kitchen.

---

*316 files. 201 tests that can run. 13 modules that can't. The bridge between vessel and agent is untested. The crab has outgrown the shell.*
