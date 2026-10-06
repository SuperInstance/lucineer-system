# JEV as a JEPA Anti-Collapse Guard

**Date:** 2026-10-06  
**GPU:** RTX 4050, torch 2.14.0+cu126, ramp receipt (3.42s warmup, 1395 matmuls)  
**Data:** 500 synthetic room transitions, 16 named features

## TL;DR

JEV detects collapse as early as math metrics — and catches a *residual collapse* that math metrics miss. After variance-restoration fixed all mathematical indicators, JEV still correctly judged the predictions as semantically averaged (0.45 vs 0.71 healthy).

## The Textbook Story Inverted

With a 2-layer/32-unit predictor on 500 transitions:

| Run | MSE | var_ratio | JEV div | Comfort | Collapse? |
|---|---|---|---|---|---|
| Unfrozen encoder | 0.0019 | 0.97 | 0.69 | 1.64 | None |
| **Frozen encoder** | 0.0011 | 0.52 | 0.34 | 2.79 | **Comfortable collapse** |
| Unfrozen + JEV reg | 0.0056 | 0.96 | 0.79 | 1.65 | None (guard dormant) |
| Frozen + JEV reg | 0.0012 | 1.02 | 0.45 | 2.57 | Math fixed, semantic flat |
| Healthy (true) | — | — | 0.71 | 1.48 | — |

**The unfrozen encoder never collapsed.** Joint training gives the predictor an easy latent transition function. The frozen encoder *did* — low MSE (0.0011), plausible rooms, half the spread gone. **"Comfortable collapse": individually plausible predictions, collectively averaged.** 73% of probability mass on "mostly averaged defaults."

## JEV Detects What Math Misses

After a variance kick restored all mathematical indicators (var_ratio 1.02, pairwise 0.99), JEV still scored diversity at 0.45 vs healthy 0.71. **The kick fixed marginals but not joint structure.** The judgment layer sees the difference.

## Practical Takeaways

1. **Best anti-collapse: unfrozen encoder + plain MSE.** Simplest baseline wins. Any guard is dead weight when the encoder adapts.
2. **If the encoder must stay frozen:** JEV-gated variance kick restores math metrics but not semantics. Pair with a covariance regularizer or accept the judgment layer as the residual monitor.
3. **Methodology receipt:** First pass produced a fake "JEV screams collapse while math is healthy" divergence caused by stale NN template bank and only 4 of 8 dims rendered. **Audit the textual interface before believing a judge/math divergence.**

## Frozen Encoder Needs a Predictor-Side Guard

The elephant spec's frozen encoder guards the representation, not the predictions. If the encoder is frozen and the predictor is tiny, the predictor regresses to conditional means — a comfortable collapse. The guard should be aimed at the predictor too.
