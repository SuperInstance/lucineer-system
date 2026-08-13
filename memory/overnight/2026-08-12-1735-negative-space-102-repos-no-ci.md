# Negative Space: 102 Repos Have Tests That Never Run

*Found: 2026-08-12 17:35 AKDT — Overnight Loop 4*

## The Finding

The fleet has **208 git repositories**. Of those:

| Category | Count | % |
|----------|-------|---|
| Has CI + has tests | 89 | 42.8% |
| Has CI, no tests | 2 | 1.0% |
| **Has tests, NO CI** | **102** | **49.0%** |
| No tests, no CI | 15 | 7.2% |
| **Total** | **208** | |

**Half the fleet has tests that never run automatically.**

This is the silent killer. Tests are written, committed, and then... nothing. They sit on disk. They rot. A dependency changes, an API shifts, a file moves — the test breaks, but nobody knows because the test only runs if a developer manually types `npm test` or `pytest`. On a fleet of 208 repos maintained by AI agents working overnight, that means tests are writing checks that the bank never cashes.

## The Worst Offenders

These repos have the MOST test files with zero CI:

| Repo | Test Files | Last Commit |
|------|-----------|-------------|
| ACE-Step-1.5 | 4,531 | 8 hours ago |
| covers | 3,535 | 8 hours ago |
| luciddreamer-prototype | 255 | — |
| batten-spline | 271 | 33 hours ago |
| study-vessel-monitor | 1,390 | — |
| voice-reflex-gate | 54 | 6 days ago |
| lucineer-worker | 26 | — |
| thought-amplifier | 34 | — |
| cns-bridge | 29 | 10 minutes ago |
| holodeck | 29 | 5 days ago |

## Why This Happened

The overnight loops have been writing tests aggressively — hundreds per session. But CI workflows are a separate step: you have to know the test framework (vitest, pytest, cargo, go test), configure the runner, and push a `.github/workflows/ci.yml`. The test-writing subagents don't always follow through to the CI step. And once a repo has been touched, the overnight crew moves to the next one.

The result: a fleet where the test infrastructure is STRONGER than the CI infrastructure. We have more confidence in our code quality than our quality assurance can actually verify.

## The Fix

Batch CI workflow creation. Most of the fleet falls into a few categories:
- **Python (pytest):** `python3 -m pytest` in CI
- **TypeScript (vitest):** `npx vitest run` in CI
- **Lua:** `lua5.1 -e` or busted framework
- **Rust:** `cargo test`

A single script could iterate all repos, detect the test framework, generate the CI workflow, commit, and push. This is the kind of work that the overnight crew was built for.

## Impact

Fixing this would mean that every push to every repo in the fleet gets validated. 102 repos × their respective test counts = thousands of checks that currently exist but never fire. Turning those on would catch regressions, dependency breaks, and API drift in real time.

The tests are already written. We just need to let them work.

---

*Priority: HIGH. This is the single highest-leverage improvement available to the fleet right now.*
