# JEPA on Real Dial Data: The Falsification Gate Survives, the Judgment Layer Splits

**DL1-REAL-JEPA · 2026-10-06 · quilt-gpu-lab deep lane**

*Authors: research subagent (DL1), on the elephant corpus and the typesafe SystemOne judgment cell (jev-1.13.0).*

## Abstract

Five prior experimental lanes (JEV×JEPA×Ternary) validated JEPA predictors and JEV judgment exclusively on synthetic room fields. We test both on **real dial streams**: nine logged night sessions of the elephant room-field instrument (frozen vMF encoder, REG-1 generalized-eigenbasis latent, 258 logged latent states). A 2-layer/64-unit MLP predictor, pre-registered before any result, beats the persistence baseline on held-out nights by **61% RMSE on the v* projection and 44% on log κ** (gate: >15% both; secondary sliding-window channel: 69%/32%) — the JEPA hypothesis is **not falsified on real data**. But 630 graded noul judgments of the real residuals split the verdict: JEV rates the JEPA predictions **more plausible** than persistence (+0.040, p≈2e-10) yet **less close to ground truth** (−0.138) and **worse on coupling** (−0.094). The synthetic-lane orthogonality between raw error and judgment (ρ≈0.01–0.03) **does not survive**: on real residuals ρ(raw L1, noul-valid) = −0.53. Zero catastrophic rows appear. Interpretable residual features explain only 34–54% of judgment variance, dominated by volume-axis error and concentration (κ) error — JEV's residual "taste" on real data is axis-selective and κ-aware, concentrated on exactly the instrument's registered room axis (volume–presence contrast), rather than the coupling-violation detector the synthetic lanes suggested.

## 1. Introduction

The elephant project's room-field thermometer reads seven conversational dials (mood, volume, earnestness, cynicism, joke_landing, panic, presence) through a frozen von Mises–Fisher encoder: trailing windows are standardized to z-space, and a closed-form Newton MLE yields the latent state (μ̂, κ, ρ) on S⁶. A registered generalized eigenproblem (REG-1) separates room-response from reader-personality variance and yields the data-derived room axis v* (a volume(+)–presence(−) contrast at 64–86° from the a-priori warmth direction W).

JEPA-v1 (pre-registered 2026-08-21) predicts the *latent* next state from the latent context — no reconstruction — with the encoder frozen by construction. Its falsification design is strict: beat the persistence baseline by >15% RMSE on both v*ᵀμ̂ and log(1+κ) on held-out nights, or the hypothesis dies. Prior lanes ran JEV (a calibrated judgment model, `noul` ∈ [0,1]) over *synthetic* room transitions and found (i) judgment is 81%-predictable from marginals, (ii) the residual 20% is "physical-coupling taste," (iii) judgment and raw error are orthogonal, and (iv) JEV detects semantic collapse math metrics miss. None of this was ever tested on real instrument output. This paper is that test.

## 2. Data and the meaning of "real"

Primary corpus: the nine wave-1 primary nights (A, D, D-cold, S1–S5 families), per-speak logged 7-dial room fields and the encoder's own logged fits (258 states). Two verification gates passed before any training: logged-fit internal consistency (V1), and bit-level reproduction of the filed REG-1 basis from the registered measurement machinery (V2, cos = 1.000000 on v* and v2).

Two honest data facts, verified before freeze: (a) wave-2 T-nights carry **bit-identical** raw fields to their wave-1 twins (the raw field is roster-invariant text content) — they add zero room-field data; (b) wave-3 is forward-model output — real instrument, synthetic dynamics — excluded here. The room-field JEPA therefore lives on 9 streams / 258 latent points: the small-corpus risk flagged in the JEPA-v1 spec is fully present, and the predictor is deliberately tiny (14→64→7).

Held-out nights (frozen): D-cold, S4b. Channels: (A) the instrument's logged cumulative fits; (B) sliding 16-speak refits through the same frozen solver (more local, more volatile κ). One leakage axis is acknowledged: test nights share script families with training nights (held-out logs, not held-out conversations).

## 3. Methods (frozen in PRE-REG before results)

Latent ℓ = [v*ᵀμ̂, log(1+κ), ρ, v₂ᵀμ̂, v₃ᵀμ̂, v₄ᵀμ̂, v₅ᵀμ̂]. Predictor input [ℓ_t, ℓ_t − ℓ_{t−1}] → 7. Weighted L1 (v*, logκ at 1.0; ρ 0.5; residual projections 0.25) with the registered q-rule mask (zero loss on edges whose motion is <20% room-subspace). Ten seeds; persistence and train-mean-delta baselines; GPU ramp receipt (3.09 s, 2350 matmuls, RTX 4050) before training.

JEV battery: 90 held-out transitions stratified by decoded residual terciles; three states per row (before / predicted / actual) rendered homogeneously in decoded μ̂-space (constrained least squares onto the five predicted basis projections, sphere-renormalized, destandardized, clipped — clip fraction reported); four graded noul questions (valid, coupling, close, actual_valid reference) across two arms (JEPA seed-0, persistence). 630 calls, zero failures. Key read at use-time, never echoed.

## 4. Results

### 4.1 The falsification gate passes (Table 1)

| channel | metric | persistence | mean-Δ | JEPA (10-seed) | vs persistence |
|---|---|---|---|---|---|
| A logged | RMSE v*ᵀμ̂ | 0.0171 | 0.0140 | **0.0067** | **−61.0%** |
| A logged | RMSE log(1+κ) | 0.0467 | 0.0446 | **0.0259** | **−44.4%** |
| B sliding-16 | RMSE v*ᵀμ̂ | 0.0189 | 0.0125 | **0.0058** | **−69.2%** |
| B sliding-16 | RMSE log(1+κ) | 0.3610 | 0.3477 | **0.2463** | **−31.8%** |

The room field's next latent state is substantially predictable from its recent latent history by a tiny network — the persistence null is rejected by a factor of 3–4 beyond the pre-registered bar.

### 4.2 The judgment layer splits (Table 2)

| noul question | JEPA | persistence | paired Δ | p (Wilcoxon) |
|---|---|---|---|---|
| valid | 0.914 / 0.895 | 0.869 / 0.850 | **+0.040** | 1.8e-10 |
| close | 0.796 / 0.719 | 0.902 / 0.868 | **−0.138** | 3.4e-10 |
| coupling | 0.494 / 0.455 | 0.581 / 0.544 | **−0.094** | 1.2e-10 |
| actual (reference) | 0.942 / 0.931 | — | — | — |

JEPA is judged the more *plausible* evolver and the less *accurate* one. The mechanism is visible in the loss: v*/κ weighted 4× over the residual projections that carry most decoded-dial mass; persistence refuses to move in a slow regime and is rewarded on closeness and (trivially) on coupling.

### 4.3 Orthogonality dies on real data (Table 3)

ρ(raw L1 residual, noul) on real residuals: valid −0.53, close −0.70 (JEPA arm); all p < 1e-7. The synthetic-lane orthogonality (ρ ≈ 0.01–0.03) was a property of mixed corruption/plausible regimes; real held-out residuals are uniformly small imprecision, and judgment tracks error monotonically.

### 4.4 What the unexplained variance is made of (Table 4)

RF regression of noul(valid) on interpretable residual features: 5-fold CV R² = 0.34 (night-held-out 0.48–0.54), vs 0.81 for the synthetic meta-predictor. Importances: err_volume 0.21, κ_err 0.16, err_joke_landing 0.14, err_cynicism 0.13, err_mood 0.09 — with ρ(|κ err|, noul valid) = −0.54 standalone, and coupling judgments dominated by volume error (importance 0.51). Personality-side dials (mood, earnestness) cost the least plausibility per unit error; the room axis and concentration cost the most. Zero transitions fall below noul 0.5 on validity — the corruption fingerprints of the synthetic lanes (breadth-vs-focal) never occur.

## 5. Discussion

**The gate and the judge disagree, informatively.** The pre-registered latent gate says JEPA wins; a gate built on decoded closeness or coupling would have said it loses. Both are correct: they measure different consumers' losses. This is the concrete real-data instance of the anti-collapse lane's conclusion that guards must target the *predictor's output space*, not the encoder. A follow-up loss weighting decoded-dial error (or judged closeness) is the obvious next experiment, now with a pre-registered three-way gate.

**JEV's surviving "taste" on real data is axis-selective, κ-aware error weighting.** The synthetic lanes' 20%-unexplained "coupling taste" does not transfer: real residuals contain no coupling violations for it to find. What remains robust is that equal-magnitude errors are *not* equal in judgment — errors along the registered room axis (volume–presence) and on concentration dominate, an independent convergence between the judgment cell and the instrument's own generalized eigenproblem. The judgment layer prices the quantities the instrument itself registered as room-response.

**Small-corpus honesty.** Nine streams is thin; test nights share script families with training nights; judgments cover seed-0 predictions on 90 rows. The 61–69% v* margins are wide enough to survive these caveats; the 0.04-scale noul deltas should be read as directional, not definitive.

**What would falsify the residual-monitor thesis next:** a predictor trained to optimize judged closeness that still loses noul(valid) — that would show the judgment layer carries information no dial-space loss reaches. Pre-registerable, cheap (the battery is resumable), and directly downstream of this lane.

## 6. Reproducibility

All scripts, frozen pre-reg, raw judgments (JSONL), latents, and model weights in `research/dl1-real-jepa/`. Deterministic: seeds fixed (torch/np/rf), the basis reproduces the filed REG-1 result exactly, and the battery is append-only resumable. GPU receipt logged in `train-results.json`. Read-only against `projects/elephant`.
