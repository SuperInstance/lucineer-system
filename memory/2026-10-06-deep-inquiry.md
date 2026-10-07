# Deep Inquiry: What's Underwater in JEV×JEPA×Ternary

**Date:** 2026-10-06  
**Trigger:** Casey's audio — "you have just seen the iceberg. There's a huge part underwater. Time to suit up and go deep."

## The Iceberg

Five lanes completed. All papers pushed. Surface = synthetic room fields, simulated JEPA, synthetic corruptions.

## What's Underwater

### 1. JEPA on Real Dial Data (Not Synthetic)
Frozen vMF encoder is already built and registered. Real dial streams exist (wave-1, wave-2, wave-3 corpora). Train JEPA on actual dial data. The prediction error on real data IS the real signal — what the room actually does vs what JEPA predicts. Run JEV on real residuals. The 20% of JEV's variance unexplained by L1-norm IS the coupling-violation signal. What does it look like on real data?

### 2. JEV's Causal Decision Boundary (Not L1-Norm Dominance)
RF R²=0.81, L1-norm carries 63% importance. But the 20% is the interesting part — JEV's sense for physical couplings that don't show in marginals. Causal ablation: systematically remove physical couplings from state description, measure how JEV's noul changes. This is JEV's "physics" — what it thinks a room should do. Not what we think, but what JEV encodes.

### 3. The σ≈0.3 Crossover Point on Real Noise
Ternary lattice beats flat JEPA when noise σ > 0.3. What is real noise in the dial streams? Is the σ threshold meaningful? The crossover σ* might be the "signal-to-noise ratio" of the room itself.

### 4. Longitudinal JEV
All five lanes used static snapshots. What happens to JEV's calibration over time? Does the boundary move as personalities change? Run JEPA on a full week of dial data, JEV on daily slices. Track noul distributions over time.

### 5. The Composed Pinch Route on Real Data
Lane 5's exp4 PASS — FAR 3.3% on synthetic. What about real dial streams? The composed pinch route (JEV confidence × JEPA residual × ternary gate) is the strongest finding. It needs real-world validation.

## The Deep-Lane Protocol

Three deep-lane subagents:
- **dl1-real-jepa:** Train JEPA on real dial data, run JEV on residuals
- **dl2-causal-ablation:** Causal ablation study of JEV's decision boundary
- **dl3-longitudinal:** Longitudinal JEV calibration + composed pinch route on real data

Each lane gets its own research directory, pre-registration, frozen gates, and a FINDINGS.md.

## The Deep Water Starts Here

The 20% unexplained variance in Lane 2's meta-predictor IS the answer. That 20% is JEV's sense for physical couplings that don't show in marginals. If we can map what JEV catches that raw error misses, we have a model of the room's causal structure.

That's the deep water.
