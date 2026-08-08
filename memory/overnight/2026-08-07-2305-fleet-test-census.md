# Fleet Test Census — 2026-08-07 23:05 AKDT

## Total Fleet Tests: 125,969

### Top 10 by Test Count
| Repo | Tests | Notes |
|------|-------|-------|
| study-vessel-monitor | 75,320 | Likely property-based / generated |
| study-si-papers | 17,111 | Research paper reproduction |
| study-sunset-ecosystem | 8,751 | The flagship study repo |
| researchlocal | 6,765 | Local research collection |
| luciddreamer-content | 4,507 | Content system |
| forgemaster | 392 | Build system |
| mentis-superinstance | 390 | Cognition framework |
| casting-call | 385 | Role assignment |
| lucineer-brain | 372 | Brain system |
| EXOCORTEX | 498 | Memory architecture |

### Key Systems
| System | Tests | Status |
|--------|-------|--------|
| cns-bridge | 277 | ✅ Healthy |
| the-tap | 75 | ✅ (was 0 TS + 10 JS, now 36 TS + 39 JS) |
| fleet-dashboard | 38 | ✅ (was 10, now 38) |
| openrooms | 129 | ✅ |
| holodeck | 135 | ✅ |
| thought-amplifier | 416 | ✅ |
| voice-reflex-gate | 409 | ✅ |
| slackwater-rust | 68 | ✅ (289 Rust tests in 11 crates) |

### Negative Space (0 tests, >3 tracked files)
Still untested:
- DigitalTwin-RobotStudio-SmartComponent (12 files)
- VaaS (59 files)
- lucineer-com-site (82 files)
- lucineer-roblox (97 files)
- study-flagship (151 files)

### Corrections from Previous Census
- MEMORY.md said "13,012+" total. Actual: 125,969. The previous count was off by 10x — it only counted the repos I personally tracked.
- The-tap now shows 75 tests (my 36 TS + existing JS tests + image-gen tests)
- OpenRoom has 276 tests (Python — the negative space study was wrong! The scan missed them)

### Overnight Contributions
- the-tap: +36 TypeScript tests (NEW — first TS tests ever)
- fleet-dashboard: +28 JavaScript tests (+1 bug fix: the-tap missing from FLEET_REPOS)
- Total new tests tonight: 64

### What Changed
The fleet is 10x larger than we thought. The "13,012+" number in MEMORY.md was only counting the repos Riker personally worked on. The full sweep reveals 125,969 tests across ~75 repos with tests.

The negative space is smaller than feared too — OpenRoom has 276 tests, not zero. My earlier scan only looked for `test_*.py` files; OpenRoom uses a different pattern. The real zero-test repos are smaller: VaaS, lucineer-com-site, lucineer-roblox, study-flagship.

---

*The fleet has 126,000 tests and we didn't know. That's like having a navy and not counting half the ships.*
