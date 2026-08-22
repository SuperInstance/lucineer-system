# Harness Verification Report — 2026-08-21

## 1. Test Suite
**281 tests passed, 0 failed** (34.75s). Includes 3 harness-specific tests in `test_harness.py`.

## 2. Calibration Harness (`scripts/calibration_harness.py --quick`)
Calibration converged: m0=1.2574, sigma_a=0.2851, fiber={phi=0.55, sigma_eta=0.02, nu=0.06, sigma_j=0.08}, delta_x0=0.14. Fresh-seed validation (seed 20261821): corpus_sd=0.2301, spread=0.541, ICC=0.777 (filed CI 0.637–0.840), q_trans=0.139, n_events=15, Sxx=0.1971 (exact). All target checks pass.

### Power Curves
| Axis | Effect | A power | D power | P power | S power | VOID eligible | Notes |
|------|--------|---------|---------|---------|---------|---------------|-------|
| flip (A/D) | 0.00 | 0.00 | 0.00 | — | — | no | 1.2 down-crossings |
| flip (A/D) | 1.00 | 0.50 | 0.00 | — | — | no | 13.8 crossings |
| flip (A/D) | 2.00 | 1.00 | 0.75 | — | — | **yes** | 38 crossings, VOID≥20 at dose 0.28 |
| diff (P/q) | 0.00 | — | — | naive_P=1.00 | q_power=0.00 | — | **Rigid common shift: q_rule correctly says UNINFORMATIVE, naive_P holds (no false persistence)** |
| diff (P/q) | 0.80 | — | — | naive_P=1.00 | q_power=1.00 | — | |
| slope (S) | 0.00 | — | — | — | 0.00 | — | |
| slope (S) | 0.50 | — | — | — | 1.00 (strict) | — | slope=−1.88 |
| slope (S) | 1.00 | — | — | — | 0.67 (strict) | — | slope=−1.81 |

**q-rule test verdict: PASS.** At zeta=0 (rigid common shift), q_trans=0.160 vs q_rest=0.156 → verdict=UNINFORMATIVE. Naive P holds at 1.00 but q-rule fires at 0.00. The rigid shift is correctly excluded as persistence evidence.

Coordinate firewall: data/nights SHA stable, K-names disjoint from T-names, writes confined to data/calibration/.

## 3. Riverbed Generator (`scripts/riverbed_generator.py`)
**Self-test: ALL 8 CHECKS PASSED.** Generated 9-night instrument corpus to /tmp/riverbed-verify/.

### Schema Compatibility (vs real night-T2.jsonl)
- **session_open**: key sets identical (gen ⊇ real − {staged_entries})
- **speak (v:2)**: key sets identical (all 20 keys match)
- **readers block**: 5 keys identical (charisma, field_eff_to_reader, lens_now, reader_fit, reader_known)
- **fit**: 8 keys identical (includes warmth_vmf)
- **session_close**: key sets identical
- **Manifest**: 9 nights, sha256 + stripped_md5 per file, deterministic_replay_identical=True for all
- **Pipeline compat**: `e2_instrument.logged_readings` + `premise_band_movers.night_windows` consumed generated data unchanged (174 finite rho reader-windows)
- **No `--verify` flag** on e2_nights.py; schema validated by structural key-set comparison against real T-night

## 4. Bugs Found
None. Both scripts and all 281 tests pass cleanly. The quick-mode calibration targets are met (corpus_sd within 0.007, ICC within filed CI, q in band, x-side stats exact by construction).
