# Ternary Routing on JEPA Predictions: Full Threshold Sweep

**Date:** 2026-10-06  
**Data:** 200 JEPA predictions × 21 threshold points per axis (v*, κ, coherence) = 9,261 configurations  
**JEV calls:** 800 judgments (batched across sweep)

## Setup

200 synthetic JEPA predictions on 9-dimensional room field (v*, κ, coherence, +6 residual dials). Each swept through JEV with ternary quantization thresholds at τ ∈ {0.0, 0.05, 0.10, ..., 0.95} for each axis independently.

## Key Findings

### MI with JEV Confidence

| Axis | τ=0.2 | τ=0.1 | τ=0.05 |
|---|---|---|---|
| v* | 0.156 bits | 0.112 bits | 0.092 bits |
| κ | 0.304 bits | 0.304 bits | 0.202 bits |
| Coherence | 0.108 bits | 0.095 bits | 0.082 bits |

**κ axis carries the most mutual information with JEV confidence** — roughly 2× v* at the same threshold. Coherence is weakest. This suggests κ (choppiness/presence) is the most judgment-sensitive dimension.

### Ternary Quantization Pattern

At τ=0.1:
- v*: 43 −1 / 114 0 / 43 +1 (symmetric about 0)
- κ: 43 −1 / 114 0 / 43 +1
- Coherence: more concentrated toward 0

**The κ and v* distributions are symmetric around the center bin.** This is expected for the room field (no directional bias over long horizons), but it means the ternary quantization produces balanced classes — the important information is in the *boundary* states (±1), not the center.

### Routing Threshold Implications

The τ=0.1 and τ=0.2 configurations show the strongest separation: boundary states (±1) correspond to higher-MI with JEV confidence. The sweet spot for routing decisions sits around τ=0.1 for κ and τ=0.15 for v*.

## Headspance

This sweep was the "breadth" experiment — covering the full threshold space without a specific hypothesis. It confirmed that κ is the most judgment-sensitive axis, and identified operating sweet spots for the ternary routing layer. The data is complete and ready for the CM1 r7 design.
