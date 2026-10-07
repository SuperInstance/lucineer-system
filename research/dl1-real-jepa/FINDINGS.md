# DL1-REAL-JEPA — FINDINGS

**Date:** 2026-10-06 · **Lane:** DL1 (deep water — real dial data, not synthetic room fields)
**Data:** 9 wave-1 night streams (`projects/elephant/data/nights/`, 258 logged latent points + 204 sliding-refit points) · **JEV:** 630 graded noul calls, 0 errors · **GPU:** RTX 4050, ramp receipt PASS (3.09 s, 2350 matmuls)

## TL;DR

The pre-registered JEPA falsification gate **PASSES on real data** — the predictor beats persistence by 61%/44% (v*/logκ, logged-fit channel) and 69%/32% (sliding channel), far above the 15% bar. But the judgment layer **splits the verdict by question**: JEV scores JEPA *more plausible* than persistence (valid +0.040, p≈2e-10) yet *less close* (−0.138) and *worse on coupling* (−0.094). And on real residuals, noul(valid) **correlates** with raw error (ρ=−0.53) — the orthogonality found on synthetic data (ρ≈0.01–0.03) **does not survive contact with real data**.

## 1. The gate: JEPA hypothesis NOT falsified on real data

Frozen gate G1 (PRE-REG §3): JEPA must beat persistence by >15% RMSE on BOTH v*ᵀμ̂ and log1p(κ), held-out nights {D-cold, S4b}, 10 seeds:

| channel | persistence (v* / logκ) | JEPA-10seed | improvement | G1 |
|---|---|---|---|---|
| A: logged cumulative fits | 0.0171 / 0.0467 | 0.0067 / 0.0259 | **+61.0% / +44.4%** | **PASS** |
| B: sliding-16 refits | 0.0189 / 0.3610 | 0.0058 / 0.2463 | **+69.2% / +31.8%** | **PASS** |

Encoder/basis verification: V1 PASS (258 logged fits internally consistent), V2 PASS (recomputed generalized basis cos=1.000000 vs filed REG-1 v* and v2 — bit-level reproduction of the registered axis). Mean-delta baseline also beaten (0.0140/0.0446 A).

## 2. JEV splits the verdict — the surprise of the lane

630 graded noul judgments on 90 stratified held-out transitions (45/channel, terciles of decoded residual, seed-0 JEPA + persistence arms + actual reference):

| question | JEPA | persistence | paired Δ (J−P) | Wilcoxon p | reading |
|---|---|---|---|---|---|
| **valid** (plausible evolution) | 0.914 / 0.895 | 0.869 / 0.850 | **+0.040** | 1.8e-10 | JEPA wins plausibility |
| **close** (matches actual) | 0.796 / 0.719 | 0.902 / 0.868 | **−0.138** | 3.4e-10 | persistence wins closeness |
| **coupling** (dial couplings hold) | 0.494 / 0.455 | 0.581 / 0.544 | **−0.094** | 1.2e-10 | persistence wins coupling |
| actual_valid (reference ceiling) | 0.942 / 0.931 | — | — | — | JEV's view of real dynamics |

**Why JEPA loses `close` while winning the latent gate:** the frozen loss weights v* and logκ at 1.0 but the residual projections (v2..v5, which carry most decoded-dial mass) at 0.25. Persistence trivially stays close in a slow regime by refusing to move. The latent objective and the judgment objective are **not the same objective** — the gate metric (v*, κ) and the consumer metric (decoded dial closeness) diverge, and the weighted L1 paid for v*/κ gains with decoded-closeness losses.

**Why persistence wins `coupling`:** zero movement trivially preserves every coupling. But coupling is NOT a pure movement penalty — within the JEPA arm, larger predicted movement correlates with *higher* coupling scores (ρ=+0.33). A coupling regression (RF, 5-fold CV R²=0.514) is dominated by **err_volume (importance 0.51)**: volume error is what actually breaks JEV's coupling judgment, and volume–presence contrast is precisely the REG-1 v* room axis. **JEV's "taste" on real data concentrates on the registered room axis** — independent convergence with the instrument's own eigenproblem.

## 3. The orthogonality finding does NOT survive real data

Spearman(raw decoded L1 residual, noul), pooled n=90/arm/question:

| | valid | coupling | close |
|---|---|---|---|
| JEPA | **−0.530** (p=8e-8) | −0.206 (p=0.05) | **−0.703** (p=1e-14) |
| persistence | −0.530 | −0.503 | −0.535 |

On synthetic transitions ρ(raw_err, noul) ≈ 0.01–0.03 (orthogonal). On real residuals it's −0.53. The synthetic orthogonality was an artifact of *corruption vs plausible-imprecision regimes*: real held-out residuals contain no corruption — everything is small plausible imprecision, so judgment tracks error monotonically. The two-regime separation JEV exploited on synthetic data has no counterpart here.

## 4. Zero catastrophes; the 20%-unexplained question inverts

- **A3: no low-noul (<0.5) valid rows — 0/90.** The corruption fingerprints (breadth vs focal) from the synthetic lanes never appear: nothing on real held-out data is broken.
- **A4: interpretable residual features explain only 34% (CV) of noul(valid)** — top drivers err_volume (0.21), κ_err (0.16), err_joke_landing (0.14), err_cynicism (0.13); coupling-gap features ≈ 0. Night-held-out R² 0.48–0.54. On synthetic the meta-predictor reached R²=0.81.
- **But** the unexplained *fraction* grows while the unexplained *mass* shrinks: noul(valid) sd is 0.009–0.020 (ceiling-compressed at ~0.9). The synthetic 20% lived across the full [0,1] range with real structure (coupling violations). The real residual ~50-66% is mostly noise on a flat ceiling.
- **κ error is a first-class driver:** ρ(|κ err|, noul(valid)) = −0.536 — as strong as raw dial L1. Choppiness error alone moves the judge. None of the synthetic-lane feature sets included a κ analogue.

## 5. Honest negatives & limits

1. **Wave-2 added zero data.** T-night raw fields are bit-identical to their S-family twins (verified max|Δ|=0.0, S1 vs T1). The "9 nights × 15 readers" framing is roster-side only; the room-field JEPA has 9 streams / 258 latent points. Small-corpus risk (flagged in the spec) is fully present.
2. **JEPA loses two of three JEV questions.** A gate built on `close` or `coupling` instead of latent RMSE would have *failed* JEPA. Which gate is "right" depends on the consumer — this is the concrete instance of the anti-collapse lane's "guard should be aimed at the predictor too."
3. **Channel B's κ is volatile** (persistence logκ RMSE 0.361 vs 0.047 cumulative) — sliding-16 refits make κ jump; the 31.8% improvement is real but the absolute regime is harsh. Cumulative fits are the calmer substrate.
4. **Decode is lossy** (5 of 7 basis dims rendered; v6/v7 carried from before-state; clip fraction 5/90 rows >0.001). Judged states are encoder-space renderings, not raw dials — deliberately homogeneous, but a rendering choice.
5. One night-family leakage axis: D (train) and D-cold (test) share the same script family with cold-entry variation; S4a/S4b likewise. Held-out nights are held-out *logs*, not held-out *conversations*.
6. 90 rows judged (budget cap), seed-0 predictions only; seed-to-seed judgment spread unmeasured.

## 6. What JEV catches that raw error misses (the actual answer)

On real residuals: **κ error** and **volume-axis error** — two physically-registered quantities (choppiness, the REG-1 room axis) that a plain L2/L1 on dials underweights. Raw error catches *how far*; JEV additionally reads *which direction the error points* — errors on the room axis (volume/presence contrast) and on concentration cost more plausibility than equal-magnitude errors on personality-side dials (mood/earnestness importances 0.09/0.06). That is the surviving kernel of "JEV's taste" on real data: **axis-selective, κ-aware error weighting** — not the coupling-violation detector the synthetic lanes suggested.

## Artifacts

`PRE-REG.md` (frozen before results, amended once pre-data with reason) · `build_data.py` + `real_latents.npz` + `extract-verify.json` (V1/V2) · `train_jepa.py` + `train-results.json` + `jepa_A.pt`/`jepa_B.pt` · `jev_battery.py` + `jev-rows.json` + `jev-real-judgments.jsonl` (630) · `analyze.py` + `analyze-summary.json`
