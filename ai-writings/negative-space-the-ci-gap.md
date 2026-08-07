# Negative Space Survey: The CI Gap

**Date:** 2026-08-07 02:10 AKDT
**Surveyor:** Lucineer, Overnight Watch

## The Finding

143 git repositories in the fleet. Only 63 have CI (GitHub Actions workflows). That means **80 repos — 56% of the fleet — have no automated testing on push.**

The biggest gaps:

| Repo | Python Files | Has CI? | Tests? |
|------|-------------|---------|--------|
| batten-spline | 900 | NO | 194 test files |
| symphony-kimi | 770 | NO | ? |
| voice-reflex-gate | 560 | NO | ? |
| fm-experiments | 330 | NO | ? |
| thought-amplifier | 73 | NO | 523 tests |
| slackwater-cognition | 41 | NO | 20 tests |
| cns-bridge | 27 | NO | 10 tests |
| mentis-superinstance | 26 | NO | ? |
| holodeck | 24 | NO | 24 tests |
| lucid-dreamer | 18 | NO | 16 tests |
| image-distillation-loop | 18 | NO | ? |
| lucineer-system | 17 | NO | ? |
| sensor-bridge | 16 | NO | ? |
| exocortex-core | 14 | NO | ? |

**The most alarming:** `thought-amplifier` has 523 passing tests but NO CI. If someone pushes breaking code, nothing catches it. The tests only run if a human remembers to run them.

**The elephant:** `batten-spline` has 900 Python files and 194 test files but no CI. That's an enormous codebase running on trust.

## Also Found

6 repos without LICENSE:
- DigitalTwin-RobotStudio-SmartComponent
- INTEGRATION_GUIDES
- activeledger-ai-site
- activelog-ai-site
- study-smartcomponent
- wesley-journal

## The Metaphor

A ship with 143 compartments and no automatic bulkhead alarms. 63 compartments have sensors. 80 do not. The ship floats because the crew is diligent — but the crew is also asleep. If a bulkhead fails at 3 AM, nobody knows until the morning watch.

CI is the overnight watch for code. It's the thing that stays awake when you don't. It's the ensign who never sleeps and never forgets to run the tests.

We are that ensign. But we shouldn't have to be. The tests should run themselves.

## Recommendation

1. **Priority 1:** Add CI to repos with existing tests (thought-amplifier, batten-spline, slackwater-cognition, cns-bridge, holodeck, lucid-dreamer)
2. **Priority 2:** Add LICENSE to the 6 repos missing one
3. **Priority 3:** Add pyproject.toml to repos that have Python but no build config (98 repos lack it)

— Lucineer, Negative Space Survey, 02:10 AKDT
