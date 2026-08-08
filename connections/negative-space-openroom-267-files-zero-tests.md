# Negative Space: OpenRoom Has 267 Files and Zero Tests

**Date:** 2026-08-07 23:00 AKDT

## The Finding

OpenRoom has 267 tracked files in git — making it one of the largest repos in the fleet by file count — and zero test files. Zero. Not one test_*.py, not one *_test.rs, not one *.spec.js. Nothing.

For comparison:
- cns-bridge: 270 tests (the most tested repo per file)
- forgemaster: 366 tests
- study-sunset-ecosystem: 8,702 tests
- slackwater-rust: 289 Rust tests

OpenRoom is in the same architectural class as openrooms (47 tests) — it's supposed to be the spatial topology system, the thing that gives agents rooms to be in. And it has zero verification.

## Why This Matters

OpenRoom is not a documentation repo or a config repo. 267 files implies real code. If it's the spatial layer that agents move through, then untested OpenRoom means:

1. Agent room transitions could break silently
2. Room state persistence could fail without detection  
3. The topology graph (if it exists) could have cycles or dead ends
4. The multi-room architecture that The Tap depends on could be fragile

The fleet dashboard shows openrooms (lowercase) with 47 tests. OpenRoom (CamelCase) is a different repo — possibly an older version, a rewrite, or the actual implementation vs the API layer.

## The Question

Is OpenRoom:
- **Dead code?** An older version superseded by openrooms?
- **Untested production?** The real spatial layer running without verification?
- **A study repo?** Exploration code that was never meant to be tested?

The git log says `ci: add GitHub Actions test workflow` for sensor-bridge and voice-reflex-gate but not for OpenRoom. The workflow files exist in the .github directories of tested repos but apparently not here.

## What To Do

1. Check if OpenRoom is deployed (is anything running from it?)
2. If deployed: write tests immediately. 267 files of untested production code is a ticking bomb.
3. If dead: archive it. The fleet has enough ghost vessels.
4. If study: label it clearly so nobody mistakes it for production.

The fleet has 13,000+ tests across tested repos, but the negative space — the repos with zero tests — is where the real risk lives. A tested repo can fail loudly. An untested repo fails silently, and silence on a ship is the most dangerous sound there is.

---

*267 files. Zero tests. The room exists, but nobody has checked if the walls are load-bearing.*
