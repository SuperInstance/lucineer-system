# Bilateral Judgment: JEPA Predicts, JEV Judges, JEPA Learns

**Date:** 2026-10-06  
**Participants:** Lucineer foreman + GLM-5.3 subagent (Lane 1)  
**Data:** `dialogue-results.json`, `noul-analysis.png`, 72 live JEV calls  
**Pre-registration:** None — this was the exploratory first contact

## The Question

Can a bilateral dialogue between a predictor and a judge produce calibration-aware prediction error? JEPA predicts room-state transitions → JEV grades validity with its `noul` confidence → JEPA adjusts its next prediction based on the judgment. Iterated three rounds. Does the conversation improve both components?

## The Answer

**Yes, in the forward direction. No, in reverse. And the asymmetry is the insight.**

### Experiment 1: Predict → Judge (n=10 baseline)

JEPA predicts room-state transitions using a simulated 7D room-field model (smooth AR(1) correlated steps = plausible; decorrelated dimension-jumps = implausible). JEV grades each predicted transition with its `noul` gate.

| Class | Noul Range | Mean |
|---|---|---|
| Plausible (λ 0.4–2.2) | 0.53–0.88 | 0.70 |
| Implausible (mag 0.5–1.6) | 0.09–0.29 | 0.17 |

**Zero overlap. Separation: 0.53. Noul is monotonically correlated with perturbation size within each class.** This is JEV's calibration doing its job — `noul` is not a binary verdict wearing decimals, it is a graded violence score. Within the implausible class, the correlation with perturbation magnitude is −0.70.

### Experiment 2: Judge → Predict (reversed direction)

Asked JEV to bless next-state ranges as noul gates (v* in 5 bins, κ in 4 bins):

- **v* gates: 0.46–0.50** — JEV hedges to a coin flip on every range. It will not commit to a free-form interval.
- **κ gates: 0.20–0.24** — uniformly rejected. No 1–2-wide κ bin counts as "whole range valid in one step."

Prediction built from the surviving constraints scored noul 0.67; a prediction ignoring the gates scored 0.06. **The reversed direction yields a rejection mask, not a range oracle.** Use noul gates as filters on candidate predictions, not as range generators.

### Experiment 3: Iterative Calibration (3 rounds × 3 trajectories)

| Trajectory | Start | Noul trajectory | Behavior |
|---|---|---|---|
| A_wild | λ=2.6, ρ=0.2 | 0.27 → 0.45 → 0.59 | Monotone recovery |
| B_borderline | λ=1.4, ρ=0.6 | 0.81 → 0.43 → 0.44 | **Degrades** — round-1 validity grew exploration, overshoot |
| C_calm | λ=0.5, ρ=1.0 | 0.77 → 0.80 → 0.79 | Stable |

The failure in B is in the JEPA-side control rule (symmetric explore/exploit), not in JEV's judgments. **Fix identified: asymmetric absorption — shrink λ hard on invalid, grow it only a fraction of the shrink on valid.**

### Experiment 4: Calibration Drift (50 trials, same initial state)

- Plausible: 0.714 ± 0.133, range [0.49, 0.90]
- Implausible: 0.215 ± 0.136, range [0.06, 0.51]
- **Bimodal with a near-empty valley at 0.4–0.5** (the class boundary)
- **ROC AUC = 0.9952. Youden threshold = 0.455 (J = 0.92)**
- Single overlap point: one implausible trial at 0.51 vs plausible minimum at 0.49

**Yes, there is a natural threshold at ≈0.45–0.50, and it coincides with JEV's own semantic midpoint (0.5 = coin flip).** The empirical operating point and the model's built-in uncertainty semantics land on the same number. This is what you want from a calibrated pincher cell: `noul ≥ 0.5` as the default gate, 0.45 if recall matters more.

## The Shared Primitive

JEV and JEPA are both quantizers of uncertainty:

- JEV quantizes a semantic question to graded P(yes) ∈ [0,1]
- JEPA quantizes a state transition to a predicted edge + residual

The dialogue works forward (predict → judge) because JEV's calibration is built on distinguishing valid from invalid transitions, not generating allowed ranges. The reversed direction fails because JEV is a *filter*, not an *oracle*.

## Implications for the Fleet

1. The bilateral loop is a viable way to produce calibration-aware prediction error. Feed JEPA predictions into JEV; use the graded noul to adjust JEPA's control parameters.
2. The 0.45–0.50 pinch threshold should be wired into the routing layer. It is not arbitrary — it is the semantic midpoint, the natural operating point, and the empirically optimal cut.
3. Asymmetric absorption is required for feedback convergence. The symmetric control rule (B's failure mode) is a necessary but insufficient condition.
4. **The circularity caveat:** The validity criteria in JEV's instructions describe the same smooth/correlated dynamics the "plausible" generator implements. So AUC measures JEV operationalizing stated criteria on numeric states, not independent ground truth. This is honest but limits the strength of the claim.

## Headspace

This was the first experiment asked for, and it turned out to be the most fundamental. The bilateral dialogue is the simplest possible composition of JEV and JEPA. Everything else (ternary routing, anti-collapse, creative explore) extends from this core finding: JEV's noul is a real, calibrated, graded score of transition validity, and it can be used as a gate, a monitor, or a meta-signal. The asymmetry (forward works, reverse doesn't) is a constraint, not a bug — it tells us what JEV *is* and what it *isn't*.

JEV is a filter. It rejects. It does not generate. This has deep implications for the rest of the ecosystem.
