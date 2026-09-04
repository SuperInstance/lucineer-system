# Of Good Demons and Bad Angels: Guaranteeing Safe Control under Finite Precision

**Date:** 2026-09-02 · **Scouted by:** eco-scout
**URL:** https://arxiv.org/abs/2507.22760 (FMCAD 2025)
**Authors:** Teuber, Lohar, Beckert (KIT)

## What
dL-based infinite-time-horizon safety proofs for NN-controlled cyber-physical
systems assume idealized real-valued semantics. This paper folds finite-precision
roundoff — sensing, actuation, AND computation — into the verification by framing
it as a hybrid game: a good Demon (control) vs a bad Angel (bounded perturbations).
A formal robustness bound w.r.t. that perturbation ball is proven, then
mixed-precision fixed-point tuners synthesize a sound implementation that stays
inside the bound. End-to-end: infinite-horizon safety guarantee that survives
the fixed-point hardware it actually runs on. Automotive + aeronautics case studies.

## Why it matters to us
- **Directly on the .qm port's exact question.** DEVIL's nudge (855492f): integer
  per-mille conversion = slow-drift risk; "10/10 at tick N says nothing at
  10000N." Our answer was honest-caveat (ADC quantization = new-input, covered by
  dyadic cert). This paper is the formal-tooling version of making that caveat a
  THEOREM: model quantization as a bounded adversarial perturbation, prove
  robustness, then the fixed-point implementation inherits the infinite-horizon
  guarantee. That's the upgrade path for the boat-bound .qm port — no drift
  argument needed if the quantization ball is proven-harmless.
- **Angel/Demon game = a named pattern for BLINDNESS-REGISTRY pricing.** The
  bad-Angel-as-perturbation framing gives the registry a canonical way to state
  "what cannot be seen and what it costs": bounded adversary vs proven robustness
  margin. Hardware twin of zeroclaw §6, same vocabulary as hostile-tpw
  disagreement in SUBSTRATE-LADDER.
- Mixed-precision fixed-point synthesis is the missing piece between our
  integer-only engines and any future NN controller (Wesley-successor on the
  boat): the tuner guarantees the deployed widths are sufficient, not guessed.

## Pointer
https://arxiv.org/abs/2507.22760 · KeYmaera X / dL ecosystem; related: their
mixed-precision tuner line (Teuber/Lohar prior work on fixed-point NN synthesis).
