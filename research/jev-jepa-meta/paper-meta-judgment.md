# JEPA Predicts JEV's Judgment (Meta-Confidence)

**Date:** 2026-10-06  
**Data:** 500 synthetic room transitions (300 clean / 200 corrupted), 680 JEV judge calls  
**Artifacts:** `meta-results.json` (319 KB), `meta-summary.json`, `nn-surrogate.pt`, `world-models.pt`

## TL;DR

Yes — JEV's judgment is highly predictable (RF R² = 0.81, Spearman 0.90). But this predictability means something surprising: **the judgment is "structured" — mostly a function of how much changed, refined by a few physical-range features. The ~20% unexplained variance is where JEV's taste lives** (physical-coupling violations that don't show up in marginals). And critically: **meta-confidence works as a cheap warning filter but not yet as a training signal.**

## Discovery: JEV is SystemOne

The TYPESAFE_AI_KEY is for typesafe.ai's SystemOne API. JEV is literally their SystemOne model (`jev-1.13.0`). Its native `noul` question type returns calibrated P(yes) ∈ [0,1] — a purpose-built judge, not a chat model hacked to be one. This matters: `noul` is a proper calibrated probability, not an approximation.

## Experiment 1: Meta-Predictor Training

51 features → predict JEV's noul score:

| Model | R² | MAE | Spearman |
|---|---|---|---|
| Random Forest (400 trees) | **0.806** | 0.087 | 0.899 |
| MLP 51→64→64→1 | 0.729 | 0.098 | 0.849 |

**What the RF learned:** Feature importance reveals JEV's "cognitive strategy":

| Feature | Importance | What it means |
|---|---|---|
| f37: L1 of scaled delta | 0.629 | *How much changed* — dominates everything |
| After-lux | 0.061 | Light-level context matters |
| ΔPM2.5 | 0.045 | Physical changes to air quality |
| Δtemp | 0.045 | Temperature delta |
| L2 norm | 0.028 | Squared magnitude (second-order) |

**The ~20% unexplained variance is JEV's taste.** It reads rates and couplings that the feature set underspecifies (CO₂ rising with window open and nobody home — a rate/coupling violation invisible to marginals).

## Experiment 2: The Surprise is Structured

112 low-noul rows (noul < 0.5): 111 corrupt, 1 clean. Two fingerprints:

1. **Breadth:** Corrupted transitions shift 2–6× more dimensions than real dynamics (clean evolutions are local: ~1.5 dims shifted)
2. **Focal vs broad:** Range/rate violations affect few dims with huge magnitude; global shifts affect many dims moderately

**Nothing in the low-noul set looks like unstructured sensor noise.** Even "random noise" corruptions betray themselves by breadth. Corruption families have distinct signatures.

## Experiment 3: Self-Consistency JEPA (Negative Result)

World model trained on clean transitions, augmented with `loss += λ·|g(pred) − g(actual)|` where g is the meta-predictor as a differentiable JEV surrogate.

| λ | Test raw err | Surrogate gap | Real-JEV mean noul |
|---|---|---|---|
| 0.0 | 0.937 | — | 0.566 |
| 0.25 | 0.934 | 0.0003 | 0.557 |
| 0.5 | 0.921 | 0.0002 | 0.562 |

**The λ term is satisfiable without moving the true judge.** The surrogate gap collapsed to zero, but real-JEV scores stayed flat. **A surrogate at R² ≈ 0.73 can be fully satisfied without convincing the true judge.** Distillation needs a more faithful g.

(Engineering note: the first implementation had a silent bug — judgment term computed on detached predictions, zero gradient, making all λ variants identical.)

## Experiment 4: JEV vs Raw Error Are Orthogonal

Spearman(raw_err, noul) ≈ 0.01–0.03 — orthogonal.

- **High error, JEV-valid:** err 0.92, noul 0.85 — 24.2°C vs 22.4°C, mug 0.5m off — physically sensible, just imprecise
- **Low error, JEV-invalid:** noul 0.12 — raw L2 spread across dims, but predicted lux = −161. MSE amortizes range violations; JEV treats them as fatal

**Predictions with err > 1.2 still averaged noul 0.56 — large-but-plausible ≈ small-but-broken in raw error, wildly different in judgment.**

## What's Underwater

The meta-predictor R² = 0.81 means we can build a cheap "expected judgment" warning filter. But it's not faithful enough to train against. The judgment layer is the residual monitor — and that's what matters for the fleet.

**The unexplained 20% is JEV's taste for physical-coupling violations** — things that happen together but shouldn't (CO₂ rising while the window is open with nobody home). This is the signal worth mining deeper.
