# JEV × JEPA × Ternary: Cross-Pollination Results

**Date:** 2026-10-06  
**Pattern:** ternary-synergy-miner (shared primitive → novel composition → falsifiable claim → frozen gates → negative controls)  
**JEV spend:** 210 calls, 82.5k in / 6.1k out tokens, 0 retries

## The Shared Primitive

All three components are **quantizers of a judgment under uncertainty**:
- Ternary quantizes a signal to {-1,0,+1} with 0 as "no signal" (deadband)
- JEV quantizes a semantic question to graded P(yes) ∈ [0,1]
- JEPA quantizes a state transition to predicted edge + residual

## Ranked Synergies

### #1 — Composed Pinch Route (exp4) — **PASS** ✅

GEN proposes transition → JEPA scores structural validity (linear-kernel residual) → JEV supplies calibrated semantic confidence → ternary route composes: +1 accept (JEV ≥ 0.5 AND residual ok), 0 hold (mixed), −1 reject.

**Numbers (n=60: 30 valid / 30 invalid):**
- FAR: **3.3% composed vs 20% JEV-only vs 80% JEPA-only**
- FRR on valid: **0%** in all gated arms; composed holds 10% (the 0-state earns its keep)
- **28/60 trials JEV and JEPA disagree** — pure complementarity
- Hardest class (mild invalids): composed FAR 10% where JEV alone 40%, JEPA alone 70%

**CM1's pinch gate was JEV-alone; nobody composed the judgment cell's confidence WITH the transition kernel's residual. The 0-state absorbs mixed-evidence cases where either single gate would guess.**

### #2 — Impossible-Transition Detector (exp5 + exp5b) — Pre-reg FAIL, Post-hoc PASS

JV is a strong binary impossibility judge (83.3%) but can't express the middle class (unlikely). Post-hoc fix: max per-dim standardized z with two bands. **Held-out 3-way accuracy 100%.**

**Key insight: JEV's graded confidence separates all three classes (possible 0.90 / unlikely 0.78 / impossible 0.43). The binary pinch destroys the taxonomy the grading already contains.** Ternary's 0-state is exactly what JEV's confidence compresses away when thresholded.

### #3 — Ternary-Structured JEPA — FAIL with Discovery (exp3)

Flat JEPA wins clean (0.909 vs 0.792 @ σ=0.05). Lattice wins noisy (0.549 vs 0.452 @ σ=2.0). Crossover at σ≈0.3. Lattice uses **14.3 bits vs 288 bits** (20× compression).

**Ternarization is a denoiser.** Predicting on the lattice trades clean-regime accuracy for noisy-regime robustness. The count-table (ternary-markov's own primitive) is immune to outlier drag; least-squares is not.

### #4 — JEPA as Ternary Encoder — Double-Falsified (exp2/2b)

Autoencoding {-1,0,+1}⁹ into continuous latents: at k=4, error 20-24%. Error approaches 5-6% at k ≈ d — no compression.

**The ternary cube is intrinsically high-dimensional. No smooth low-dim continuous manifold underneath it.** This negative is foundational and explains why #3 works: you cannot smooth-embed ternary into JEPA latents. The composition runs the other way.

### #5 — JEV as Ternary Router (exp1) — Near-Miss

JEV covered accuracy 93.3% vs 67.5% keyword rule (+25.8 pts). Margin separates clear from boundary (AUC 0.79). Gate missed by ONE trial.

## Cross-Pollination Leads

1. **exp4 + ternary-oracle:** JEV confidence = stake; JEPA residual = due-diligence artifact. The composed route is a 2-sensor market maker.
2. **exp5b + ternary-noether:** "impossible" = conservation-law violation. z-max bands are empirical stand-ins for invariants.
3. **exp3 + ternary-markov:** The crossover σ* is a critical point; a scheduler that switches lattice↔flat on measured noise regime is the pid-tuned-criticality pattern on a new substrate.
4. **exp1 + ternary-route:** JEV margin maps to three-tier health model (+1 firm route / 0 degraded / −1 escalate).

## Recommendation

- **PROMOTE** composed pinch route into CM1 as r7 candidate
- **BUILD** per-dim-z transition classification into room monitor
- **SWITCH** predictors by noise regime (lattice when σ_est > 0.3)
- **STOP** trying to embed ternary into continuous JEPA latents
