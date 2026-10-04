# FLEET-HARDWARE RECEIPT — quilt-arcade local run #1

- **When:** 2026-09-28 11:10 AKDT
- **Host:** eileen (WSL2, Linux 6.18.33.2-microsoft-standard-WSL2, x64)
- **Runtime:** Node v22.23.2
- **Commit:** `66993df` (main — "README: zero-shot orientation… #4"), fresh clone from https://github.com/SuperInstance/quilt-arcade
- **Command:** `npm ci` (single dep: yaml ^2.9.1) → `node run_all.mjs`
- **Code changes made by runner:** NONE. Only repo mutations are harness-emitted artifacts (4 × `generated` timestamp lines in `experiments/*.json`) + untracked `node_modules/`. Nothing committed.

## Result: **ALL GREEN — 67/67 checks, exit 0**

### Wall time
- **Full gate: 37.15s** (scout estimated ~3 min; this box is faster — timings are machine-dependent per README)
- Peak RSS: ~149 MB
- npm ci: ~seconds, 0 vulnerabilities

### Phase A — plugin smoke (6/6 green)
All six manifests discovered, booted under stub DOM, ≥1 receipt emitted, **every declared fnv1a64 chain re-derived from GENESIS** (plugins.mjs asserts non-empty chained sources and re-derivation; a break throws):

| plugin | smoke |
|---|---|
| connect4 | ✓ (24ms) |
| gomoku | ✓ (57ms) |
| holdem | ✓ (25ms) |
| pong | ✓ (2ms) |
| reversi | ✓ (38ms) |
| tictactoe | ✓ (20ms) |

### Phase B — playtest harnesses (67/67 green)
| game | checks | time |
|---|---|---|
| tictactoe | 11/11 | 2117ms |
| reversi | 12/12 | 4686ms |
| connect4 | 11/11 | 7124ms |
| gomoku | 9/9 | 14241ms |
| holdem | 12/12 | 4070ms |
| pong | 12/12 | 3845ms |

### Null slots behavior
- No `QUILT_SLOT_*` env vars set on this box → all four slots (judge/JEV, jester, quantum/MOTH, predictor/JEPA) ran as **interface-only stubs, every hook returned `null`** ("no opinion / no surprise / no sample / no prediction").
- `assertSlotsValid()` passed in Phase A: each slot self-identifies, exposes async-callable hooks, declares credential state. Games fully playable and green with every slot dark — the constitution's null-slot requirement holds on real hardware.
- `learning_curves.md` regenerated **byte-identical** (deterministic aggregation — not in git diff).

### Surprises / notes
1. **It's green on the first fleet-hardware try.** No fixes needed — nothing to install beyond `npm ci`, no patches, no workarounds. The scout's suspicion ("ALL GREEN only ever earned in the z.ai lane") is now discharged: main @ `66993df` is genuinely green on WSL2/Node 22.
2. Run is **deterministic enough that learning_curves.md reproduced exactly**, though the 4 experiment JSONs got fresh `generated` timestamps (harness writes its own receipt of the run).
3. Pong is headless-only (no `index.html` yet, as README states) but full 12/12 green in Phase B.
4. Raw logs: `/tmp/quilt_receipt_raw.log` (run output) and `/tmp/quilt_receipt_time.log` (GNU time stats).
