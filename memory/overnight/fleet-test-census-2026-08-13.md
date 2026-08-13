# Fleet Test Census — 2026-08-13 02:45 AKDT

**Total: 21,217 tests across 97 repos**

Run via: `bash fleet-inventory/fleet-tests.sh`

## Top 15 Repos by Test Count
| Repo | Tests |
|------|-------|
| study-sunset-ecosystem | 8,803 |
| ACE-Step-1.5 | 1,274 |
| slackwater-rust | 488 |
| EXOCORTEX | 498 |
| forgemaster | 399 |
| mentis-superinstance | 390 |
| study-pincher | 323 |
| study-spreader-tool | 310 |
| lucineer-worker | 308 |
| mud-arena | 344 |
| lingbot-map | 334 |
| casting-call | 409 |
| voice-reflex-gate | 409 |
| thought-amplifier | 444 |
| cns-bridge | 351 |

## Category Breakdown (approximate)
- **Rust crates:** ~3,500 tests (slackwater-rust, flux-genome-rs, eisenstein, gossip-ping, mud2scummvm, emergence-engine)
- **Python packages:** ~4,500 tests (slackwater stack, thought-amplifier, cns-bridge, etc.)
- **TypeScript/JavaScript:** ~13,000 tests (study-sunset-ecosystem dominates with 8,803)
- **Other:** ~200 tests

## Growth From Previous Census
- Previous (Aug 12): 4,774 tests counted (incomplete — many repos not scanned)
- Current: **21,217 tests** (comprehensive — 97 repos)
- The previous census was using a broken scanner. This new script works.

## Notes
- 97 repos with at least 1 test
- ~103 repos total in the fleet with .git directories
- The fleet test runner (`fleet-tests.sh`) is now the unified tool
- It handles Rust (cargo), Python (pytest), TypeScript (vitest), and Node.js (npm test)
- `--run` flag actually executes tests; default just collects counts
- `--json` flag for machine-readable output
