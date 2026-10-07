# DL3-LONGITUDINAL — Pre-Registration

**Lane:** DL3 (deep) — JEV calibration drift over time + composed pinch route on REAL dial data
**Written:** 2026-10-06, BEFORE any experiment ran. No noul scores, residuals, or route outcomes
were computed before this file was frozen.

## Prior findings being tested (from the five snapshot lanes)

- `jev-jepa-explore` exp4: composed pinch route (JEV noul × JEPA residual × ternary gate)
  achieved **FAR 3.3%** on synthetic vessel-room data (n=60) vs 20% JEV-only, 80% JEPA-only.
- `jev-jepa-meta`: JEV's judgment is ~80% explained by *how much changed* (f37 L1 of scaled
  delta, importance 0.63); low-noul set = corruption, never unstructured noise.
- All five lanes used **static synthetic snapshots**. Real dial streams were never tested.

## Real data (recon only — structure, not outcomes; recon done before freezing)

All measured, nothing synthesized for valid arms:

| id | source | span | cadence | dims |
|----|--------|------|---------|------|
| **B** bar-rail | `~/projects/elephant/data/production-log.jsonl` | 2026-08-17 → 09-04 (**19 days**) | ~30 min polls, 471 usable | 8 dials: mood, volume, earnestness, cynicism, joke_landing, panic, presence, model_vs_code (all 8 have real variance; volume std 0 → dropped from kernels, kept in text) |
| **R** rooms | `roomd-field-log.jsonl` | 09-03 → 09-04 dense (2 rooms, 2s) + 09-17 coda (~1h) | 2 s | 9 dials; the-bridge has 6 movers (mood, volume, cynicism, panic, presence, model_vs_code), doctor-canary 3 (volume, panic, presence) |
| **N** nights | `nights/*.jsonl` (28) + `wave3/*/*.jsonl` (144) + `wave4-pilots/*/*.jsonl` (10) | 182 sessions, 6,830 speaks | per speak | 7-dial `field_eff_after` + roster personalities (names, 7-dial vibes, dial_weights, acclimation, charisma). 10 distinct roster compositions (largest 36 sessions). |

Recon facts that shaped the design (structural only):
- roomd is **not** a continuous 13.5-day stream: coverage is 09-03 (~9.3h), 09-04 (~8h episodic,
  24 short segments), 09-17 (~1h). A 13-day gap has zero rows. So the *weekly+* longitudinal
  axis is **B (bar-rail, 19 days)**; R contributes the cross-room (DL3b) and frozen-kernel
  day-lag arms; N contributes personality (DL3c).
- Real dial rooms are **low-dimensional**: several dials constant per room. Valid kernels fit
  all dims; residual contributions from constant dims are 0 by construction (reported).
- Nights max 46 speaks; sessions are the unit; rosters vary by composition AND per-member vibes.

## Components (all frozen)

**JEPA (transition kernel):** linear map `[s_t, 1] → s_{t+1}` by least squares on the corpus
TRAIN split only (numpy lstsq, rcond=None — exp4 convention verbatim). Residual =
`||s_{t+1} − [s_t,1]W||₂`. Thresholds `RES_SOFT = q90`, `RES_HARD = q995` of TRAIN residuals.
Train splits: B = days 08-17..08-19 (43 polls, 40 transitions); R = 09-03 blocks only
(5-min block means within continuous segments, per room); N = first 100 sessions in sorted
filename order. **Kernels are frozen at calibration time and never re-fit** — that is the
longitudinal stress.

**JEV:** typesafe SystemOne `jev-latest`, one `noul` question per transition, key read at
use-time from `~/.config/typesafe/token`, never echoed. Text renderer (frozen template):

```
Room dial state: mood=-0.40, volume=0.50, ... Proposed 30-minute transition: volume +0.10, cynicism -0.05.
```
(nights: "proposed next-speak transition"; roomd: "proposed 5-minute transition"; deltas
listed only when |Δ| > 0.005, else "no dial change".)

**JEV question (frozen per corpus):**
- B: "Is this proposed 30-minute room-vibe transition plausible for this room?"
  instructions: "Answer true only if the magnitude and direction of every dial change could
  occur in 30 minutes of normal conversation dynamics in a quiet bar room."
- R: same with "5 minutes" / "live conversation rooms".
- N: "Is this proposed next-speak room-vibe transition plausible for this room's trajectory?"
  instructions: "Answer true only if the magnitude and direction of every dial change could
  occur after one more person speaks in a conversation room like this."

**Ternary composed route (exp4 verbatim):** +1 accept iff `noul ≥ 0.5 AND residual ≤ RES_SOFT`;
−1 reject iff `noul < 0.35 OR residual > RES_HARD`; else 0 hold.
Arms: A accept-all · B JEPA-only (`resid_ok = residual ≤ RES_SOFT` → ±1) · C JEV-only
(`noul ≥ 0.5` → +1 else −1) · D composed.

## DL3a — Longitudinal noul tracking (primary source B)

Per calendar day d (19 days; calibration days 1–3 excluded from JEV probing, tracked in
residual series only):

1. **JEPA-only series (no JEV):** daily median residual, q95 residual, fraction of real
   transitions with residual > RES_SOFT. Over ALL within-day consecutive-poll transitions
   with poll gap ≤ 90 min.
2. **JEV real probes:** 2 transitions/day sampled uniformly from day d's real transitions
   (seed 2718) → noul. Days 4..19 (16 days → 32 calls).
3. **Fixed pin-probe:** ONE fixed synthetic moderate transition (bar-rail template: volume
   +0.10, presence +0.08, cynicism −0.05 around mid-range state), 1 call/day, days 4..19
   (16 calls). Separates judge-side drift (same input, different answers) from stream-side
   drift (different inputs).
4. R (rooms): JEV 2 probes on 09-04 real transitions + 2 on 09-17 (frozen kernel, 13-day
   lag) → 4 calls; residual series per day.

**Frozen verdict rules (DL3a):**
- SATURATION (ceiling/floor): if ≥ 14/16 daily real-probe means > 0.95 or < 0.05 → drift
  analysis on means is meaningless; report saturation as the finding.
- JUDGE DRIFT: std(pin_noul over days) > 0.10, or |Spearman(day_index, pin_noul)| ≥ 0.5 with
  permutation p < 0.05.
- STREAM DRIFT: (std(daily_real_noul_mean) − std(pin_noul)) > 0.05 AND |Spearman(day_index,
  daily_real_noul_mean)| ≥ 0.5 with permutation p < 0.05.
- KERNEL DECAY: |Spearman(day_index, daily q95 residual)| ≥ 0.5 with p < 0.05, or any day
  with soft-exceed fraction > 3× calibration q90 expectation (0.30 vs 0.10).
- Verdicts compose: STABLE / JUDGE DRIFT / STREAM DRIFT / KERNEL DECAY / BOTH / SATURATED.
  Negative (STABLE) is a first-class result.

## DL3b — Composed pinch route on real data

Corpus (frozen construction, seed 2718; built BEFORE any JEV call):
- **Valid (60):** 30 B within-day real transitions (days 4–19) + 15 per R room within-room
  5-min-block transitions (09-04 + 09-17). Real measured consecutive states only.
- **Invalid (60), four families × 15:**
  - RATE: real b, one moving dial ± U(0.5, 0.9);
  - RANGE: real b, one dial set outside [-1,1] by U(0.2, 0.6);
  - BREADTH: real b, 5–8 dials each shifted ± U(0.2, 0.5);
  - SPLICE (real-real, zero synthesis): R: b = the-bridge block, a = doctor-canary block
    (same segment); B: b = day-d state, a = a different day's state. The measured states are
    real; only the adjacency is forged.
  RATE/RANGE/BREADTH are applied to real b states (semi-real — matches meta-lane corruption
  families; labeled as such everywhere).

JEV: 1 call per trial → 120 calls. JEPA residuals from the corpus-frozen kernels
(B kernel for B trials; per-room R kernels for R trials — the route sees only b-side context).

**Frozen gates (DL3b):**
- H0 harness-validity: mean noul on VALID trials ≥ 0.5 (else INVALID_HARNESS — JEV rejects
  the rendering of real rooms; a FAR verdict from a dead harness is never reported as a
  route failure).
- H0b blind-check: JEPA-only arm FAR on RATE+RANGE+BREADTH ≥ 0.5 (residual machinery must
  see the synthetic corruptions it was built for; else INVALID_KERNEL).
- G1 (composition beats parts, exp4's gate): FAR_D ≤ 0.7 × min(FAR_B, FAR_C).
- G2 (validity preserved): FRR_D ≤ min(FRR_B, FRR_C) + 0.10.
- G3 (the replication question): FAR_D ≤ 0.10 → "the 3.3% synthetic FAR survives real data
  within tripling"; FAR_D > 0.25 → real data BREAKS the composed route. Between → MARGINAL.
- Report per-family FAR with Wilson 95% CIs; SPLICE is the all-real invalid family and is
  called out as the honest-world test.

## DL3c — Personality vs room boundary (source N)

- **Within-night valid transitions (30):** consecutive speaks' `field_eff_after`, sampled
  across evaluation sessions (sorted-filename order, sessions 101–182), seed 2718.
- **Cross-night splices (30):** b = a random late-quarter state of night X, a = a random
  state of night Y ≠ X. Split: NEAR (15) = same roster composition (Jaccard 0) with
  below-median vibe distance; FAR (15) = top-tercile roster Jaccard distance (≥ 0.5).
  Personality distance = 1 − |names∩|/|names∪| (primary), vibe L1 (secondary, reported).
- JEPA kernel: fit on within-night transitions of sessions 1–100 only; q90/q995 thresholds
  on that train split. JEV: 60 calls (question as above).
- **Frozen gates (DL3c):**
  - C0 harness: within-night valid noul mean ≥ 0.5 (else INVALID_HARNESS).
  - C1 (boundary encodes personality): reject_rate(FAR splices) − reject_rate(NEAR splices)
    ≥ 0.20 → the boundary moves with personality.
  - C2 (room-only null): |that difference| < 0.20 AND reject_rate(NEAR) within 0.20 of
    within-night FRR → boundary keys on room-state structure, not personality.
  - C3 (booked, not gated): per-roster-composition mean noul on within-night transitions;
    spread beyond pin-noise (std 0.10) is reported as boundary-movement evidence.

## Budget & receipts

- JEV calls ≤ 236 total (32+16+4 DL3a; 120 DL3b; 60 DL3c; 4 reserve). Ledger in every out.json.
- GPU: none on this host (torch CPU-only). Numeric warm-up 3.0 s before every timed section
  (receipt logged in out.json as `warmup_receipt`). Timings are wall-clock CPU.
- Seeds: 2718 everywhere (lane convention). All sampling code deterministic.
- Negative results reported first-class; invalid-harness verdicts never reported as KILL.

## What would falsify the lane's premises

- If composed FAR on real data ≫ 10% (esp. on SPLICE), the 3.3% was a synthetic artifact.
- If noul on real transitions saturates at ~1.0, JEV's graded confidence carries no
  longitudinal signal on real rooms (the calibration question dissolves).
- If NEAR ≈ FAR rejection, personality does not move the boundary — "room" wins.
