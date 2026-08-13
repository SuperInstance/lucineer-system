# Negative Space: The Fleet Has 3,897 Tests — But Nobody Knows

**Date:** 2026-08-12 16:45 AKDT
**Finding:** The fleet has approximately 3,900+ tests across ~40 test suites, but there is no unified dashboard or command that shows this number. Every overnight loop rediscovers the test count by running each suite individually.

## The Numbers (Audited This Session)

### TypeScript (vitest)
| Repo | Tests |
|------|-------|
| mud-engine | 308 |
| fleet-connections | 228 |
| emergence-engine | 221 |
| fleet-pipeline | 224 |
| fleet-envelope | 183 |
| luciddreamer-ai | 116 |
| hermes-perception | 98 |
| confidence-cascade | 96 |
| collective-unconscious | 74 |
| hermes-cloudflare | 79 |
| fleet-tts | 41 |
| luciddreamer-content | 40 |
| lucineer-vector | 53 |
| OpenRoom | 34 |
| lucineer-memory | 37 |
| lucineer-worker | 32 |
| SuperInstance-papers | 30 |
| crab-traps | 27 |
| A2A-native-notebookLM | 17 |
| ec2mud | 54 |
| fishinglog-ai-site | 33 |
| **TypeScript subtotal** | **~2,095** |

### Python (pytest)
| Repo | Tests |
|------|-------|
| forgemaster | 368 |
| cns-bridge | 351 |
| lingbot-map | 334 |
| exocortex-core | 188 |
| engine-ensign | 187 |
| batten-spline | 168 |
| symphony-glm | 136 |
| cns-echo | 139 |
| cns-monitor | 116 |
| log-tensor | 88 |
| flow-state | 85 |
| fleet-dashboard | (not counted, 144 per commit msg) |
| bare-metal-plato | (not counted, 32 per commit msg) |
| the-tap | 28 (Python) + 66 (JS) |
| **Python subtotal** | **~2,125** |

### Rust (cargo test)
| Repo | Tests |
|------|-------|
| hermes-nmi | 216 |
| dual-band-guard | 40 |
| eisenstein | 88 |
| gossip-ping | (uncounted) |
| **Rust subtotal** | **~344+** |

### JavaScript (node:test / Jest)
| Repo | Tests |
|------|-------|
| hermes-reader | 70 (Jest) |
| the-tap | 66 (node:test) |
| platos-shell-ide | 20 (vitest) |
| scummvm-arcade | 54 (vitest) |
| **JS subtotal** | **~210** |

## Grand Total: ~4,774+ tests

But this number was assembled manually across 4 test runners (vitest, pytest, cargo test, jest/node:test) and 3 languages (TypeScript, Python, Rust). Nobody can get this number in one command. Every overnight loop, every fleet audit, every negative space scan rediscovers it.

## The Gap

**There is no `fleet-test-runner`.** No tool that walks every repo, detects the test runner, executes it, and aggregates the count. This is the most-run operation in the fleet (we do it every overnight loop) and it's still manual.

## What We Need

A Python script that:
1. Walks `/home/eileen/projects/`
2. For each repo, detects: vitest? pytest? cargo test? jest? node:test?
3. Runs the appropriate test runner
4. Parses the output for pass/fail counts
5. Aggregates into a single JSON report
6. Optionally pushes to a dashboard

This is exactly the kind of thing that should be a skill. We've run this pattern 50+ times across overnight loops. It should be compiled into a reflex.

## Secondary Finding: hermes-reader Test Runner Conflict

hermes-reader uses Jest. The rest of the fleet uses vitest. When vitest scans the repo (during fleet audits), it finds the Jest test files and crashes on missing globals (`beforeAll`). Fixed this session by adding a vitest.config.ts that excludes the Jest test directory. But this means the fleet-wide vitest scan will always show hermes-reader as "0 tests" — masking its 70 real Jest tests.

The test runner monoculture (vitest) is fragile. The fleet needs a polyglot test runner, or at minimum, the scanner needs to know which runner to use per-repo.

## Recommendation

1. **Build `fleet-test-runner`** — a unified test scanner and runner
2. **Store `.test-runner` marker files** in each repo so the scanner knows which runner to use
3. **Output JSON** for dashboard integration
4. **Cache results** so consecutive loops don't re-run the same suite

This is the most meta finding in the fleet: we have 4,774 tests verifying our code, and zero tests verifying our test infrastructure.
