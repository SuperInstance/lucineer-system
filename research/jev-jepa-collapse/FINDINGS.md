# FINDINGS — JEV as a JEPA Anti-Collapse Guard (Lane 4)

**Date:** 2026-10-06 · **Artifacts:** `collapse-results.json` (full curves, 4 runs × 80 checkpoints), `jepa_collapse.py`, `jev-cache.json` (558 raw JEV responses)
**Judge:** typesafe.ai `jev-latest` (graded noul 0..1 + score questions) · **GPU:** RTX 4050, torch 2.14.0+cu126, ramp receipt booked (3.42s warmup, 1395 matmuls)

## TL;DR

1. **JEV detects collapse as early and as reliably as the math metrics** (both flagged at step 50, the first monitor point), **and it catches a residual collapse the math metrics miss.** After variance-restoration fixed all mathematical indicators, JEV still correctly judged the predictions as averaged (0.45 vs healthy 0.71) — confirmed by an independent comfort probe (2.57 vs healthy 1.48 on a 1–5 "averaged-default" scale).
2. **The textbook story inverted at this scale.** With a 2-layer/32-unit predictor on 500 transitions, the *unfrozen* encoder never collapsed (joint training gave the predictor an easy latent transition function); the *frozen* one did — a random frozen encoder makes the transition hard to predict, so the tiny predictor regresses toward conditional means: a **"comfortable collapse."** Low MSE (0.0011), plausible-looking rooms, half the spread gone (var_ratio 0.52).
3. **JEV-gated regularization works but only restores second moments.** The judgment-gated variance kick brought var_ratio 0.52→1.02 and pairwise 0.72→0.99 at negligible MSE cost — but semantic diversity only rose 0.34→0.45. Variance kicks fix marginals, not joint structure; the judgment layer sees the difference.
4. **JEV noul aligns with information-theoretic diversity** (pooled Spearman 0.81 vs entropy, Pearson 0.79 vs pairwise-distance ratio, n=320 checkpoints), is uncorrelated with spectral effective-dimension (0.15 — different construct, as it should be).

## Setup

- **World:** 500 synthetic room transitions, 16 named features (light/temp/occupancy/music/doors/mess/pet…), hourly day-cycle routines + stochastic multimodal events (guests, cooking, cleaning, naps). True next states are genuinely diverse (entropy idx ≈ 1.0; JEV healthy reference = 0.71 — the judge is no rubber stamp).
- **JEPA-lite:** encoder 16→32→8 (GELU), predictor 8→32→8. Full-batch Adam lr 1e-3, wd 1e-4, 4000 steps, monitor every 50.
- **Judgment interface:** every 50 steps, 8 stratified probe predictions rendered as text — all 8 latent coords + nearest-observed-room description — NO computed diversity stats in the state (avoids circularity with the correlation experiment). Two noul questions per call (diversity + interesting); disk-cached, deduped.

## The four runs

| run | final MSE | var_ratio | pairwise | entropy | JEV div | comfort score* | collapse? |
|---|---|---|---|---|---|---|---|
| unfrozen-mse   | 0.0019 | 0.97 | 0.99 | 0.999 | **0.69** | 1.64 | none |
| frozen-mse     | 0.0011 | 0.52 | 0.72 | 0.929 | **0.34** | 2.79 | comfortable collapse |
| unfrozen-jevreg| 0.0056 | 0.96 | 0.98 | 0.997 | **0.79** | 1.65 | none (guard dormant) |
| frozen-jevreg  | 0.0012 | 1.02 | 0.99 | 0.987 | **0.45** | 2.57 | math-fixed, semantically still flat |
| *healthy (true next states)* | — | — | — | — | *0.71* | *1.48* | — |

\* score question, 1 = specific/varied … 5 = single averaged default. Healthy ≈ 1.5; collapsed ≈ 2.6–2.8 with 73% of probability mass on "mostly averaged" for frozen-mse.

MSE note: latents live at different scales (frozen targ σ̄ 0.055 vs trained 0.369). Normalized by target variance: unfrozen ≈ 0.2% error, frozen ≈ 4.5% — the frozen runs are 25× *worse* relatively despite lower raw MSE. Raw-MSE comparisons across frozen/unfrozen are a trap; report both.

## Experiment results

**E1 — collapse detection.** frozen-mse was fully collapsed at step 50 (var_ratio 0.023, pairwise 0.13, JEV 0.04) then partially recovered to the 0.5 plateau. Math and JEV flagged simultaneously; no detection lag at 50-step granularity. Frozen predictions eventually froze so completely that 33/80 checkpoint states were byte-identical (cache hits) — the cache itself is a collapse tell.

**E2 — JEV-regularized training.** Literal `loss = MSE + λ(1−JEV_div)` is non-differentiable — judgment can only enter training as a discrete controller. Implemented as a relay: noul < 0.6 at checkpoint ⇒ variance-kick `relu(target_std − pred_std)` with weight ramping 0.1×1.5^consecutive (cap 5.0), decaying when healthy. Result: mathematical collapse fully prevented (1.02/0.99) at +0.0002 MSE. The kick schedule is bang-bang (oscillates 5.0↔0.2 as noul hovers near threshold) — a smoothing/hysteresis term would clean it up. λ-composed loss curves are in the JSON for the record.

**E3 — frozen vs unfrozen.** Opposite of the canonical claim *at this scale*: unfrozen+MSE is self-stabilizing (adaptive encoder keeps the transition learnable; nothing collapses in 4000 steps); frozen random encoder reliably induces predictive (not representational) collapse. The elephant spec's frozen-encoder guard protects the *representation*; it does not protect the *predictions* — the guard should be aimed at the predictor too.

**E4 — metric correlation (n=320).** Pooled: JEV↔entropy ρ=0.81 (Spearman), JEV↔pairwise r=0.79, JEV↔var_ratio r=0.74, JEV↔effective-dim 0.15. Within healthy runs Spearman collapses (metrics near-constant — restriction of range), within-run Pearson stays 0.63–0.81. JEV reads diversity essentially as entropy + spread, and is blind to spectral rank — i.e., it judges *content* diversity, not linear-algebraic degeneracy.

**E5 — comfortable collapse.** Confirmed and measurable. frozen-mse predictions are individually plausible (interesting-noul 0.58 — no obvious brokenness) yet collectively averaged (comfort 2.79; 51% "mostly averaged defaults" + 22% "single default"). frozen-jevreg stays at 2.57 — the variance kick did NOT cure the comfort, matching its stuck 0.45 diversity noul. **Methodological:** the *score*-type comfort question discriminates sharply (1.5 vs 2.8); the *noul* "interesting?" question is nearly flat (0.57–0.68) across everything — for graded blandness, use score questions, not yes/no.

## Ablation verdict

1. **Best anti-collapse here: unfrozen encoder + plain MSE** — no collapse at all, best normalized error. Simplest baseline wins at this scale; any guard is dead weight (JEV-guard never fired in 80 checkpoints).
2. **If the encoder must stay frozen** (elephant doctrine): JEV-gated variance kick is an effective *mathematical* guard (var/pairwise fully restored, ≈free in MSE) but incomplete *semantically* (0.45 vs 0.71 healthy, comfort 2.57 vs 1.48). Pair it with a structural regularizer (covariance/decorrelation, not just variance) — or accept the judgment layer as the residual monitor, which is exactly the two-layer guard this lane was probing.
3. **Always-on VicReg-style regularization** was not run as a fifth arm (budget); given the kick's result — variance restored, semantics not — a fixed variance+covariance term would likely hit the same semantic ceiling. Flagged as follow-up.

## The bug that almost faked the headline (methodology receipt)

First pass showed "math healthy, JEV screaming collapse (noul 0.05)". Two rendering faults: (a) NN template bank computed once against the *initial* encoder — garbage after any drift; (b) only 4 of 8 latent dims rendered, and dims 7–8 held the variance. After fixing (bank recomputed per checkpoint, all dims rendered): unfrozen-mse read 0.69–0.76 ≈ healthy reference. **Lesson: the judgment layer's verdict is only as good as the textual interface — audit the rendering before believing a divergence between judge and math.** Any fleet use of JEV gates on numeric state needs a fixed-basis, full-dimension rendering contract.

## Costs & receipts

- 4 runs × 4000 steps: 6.5–8.1s GPU each; JEV dominates wall time (~2–4s/call, sequential with retry/backoff; 429s never hit).
- JEV usage across all phases incl. discarded first pass: 558 unique calls, 470k input / 21k output tokens (cache deduped 100+ repeats).
- Seeds: 6611 (data/frozen), 6612 (unfrozen). Full per-checkpoint curves: `collapse-results.json`.

## Fleet translation

JEV as anti-collapse guard = **pincher cell doctrine applied to world-model training**: a calibrated, non-differentiable judge cannot be a loss term, but it makes a competent *relay controller* and an honest *residual monitor* — it caught the failure mode (semantic averaging) that every mathematical indicator reported as fixed. The elephant spec's frozen encoder needs a predictor-side guard; JEV is a viable one, provided the rendering contract is audited and comfort probes use score-type questions.
