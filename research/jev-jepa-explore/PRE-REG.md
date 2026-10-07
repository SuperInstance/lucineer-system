# PRE-REG — JEV × JEPA × Ternary cross-pollination (Lane 5 creative explore)

Frozen 2026-10-06 ~13:35 AKDT, BEFORE any experiment fires.
Pattern source: ternary-synergy-miner journal (shared primitive → novel
composition → falsifiable claim → negative control → gates).

Components (treated as "repos" with shared primitives):
- **JEV** — typesafe judgment cell (`jev-latest`, /v1/systemone, graded noul
  confidence). Primitive: the calibrated true/false confidence scalar. Used in
  CM1 cell-mesh as pinch gate (PINCH=0.5 floor).
- **JEPA** — transitional JEPA (quilt-gpu-lab tools/transition_kernel.py) +
  elephant jepa_rag (9-dial reading vectors). Primitive: the field-EDGE
  (field_before → field_after), predicted by relational context.
- **Ternary** — SuperInstance 200-repo ecosystem. Primitive: {-1,0,+1} with
  0-as-structurally-special (abstain / deadband / carrier).

## Exp 1 — JEV as ternary router
60 vessel reports: 20 clear, 20 boundary (multi-domain overlap), 20 off-domain.
Arms: (K) keyword router [cm1_relay RULE, cannot abstain]; (J) JEV 3-noul
ternary router: route = argmax domain if max conf ≥ 0.5 else 0=escalate.
GATES (frozen):
- G1: JEV covered-trial accuracy > keyword overall accuracy.
- G2: JEV abstains (0) on ≥50% of boundary trials AND ≤20% of clear trials.
- G3: margin = top1−top2 JEV confidence separates clear vs boundary at AUC ≥ 0.75.
SYNERGY-PASS = G1 ∧ G2 ∧ G3.

## Exp 2 — JEPA as ternary encoder (ternary manifold learning)
100 runs = latent dims k ∈ {1,2,3,4,5} × 20 seeds. Torch GPU AE on
{-1,0,+1}^9 (9 = JEPA dial dim): train 2,000 sampled states, held-out 2,000.
Baselines: random-projection + per-dim decode; identity.
Metrics: per-trit decode error, Spearman(Hamming, latent Euclid).
GATES:
- G1: k=4 held-out trit error ≤ 0.02.
- G2: Hamming↔latent distance Spearman ρ ≥ 0.90 at k=4.
- G3: graceful degradation: error monotone-ish in k (k=5 ≤ k=3 error, no cliff).
SMOOTH-GEOMETRY-PASS = G1 ∧ G2 ∧ G3.
GPU law: ramp receipt at process start + sustained load (no idle gaps within
the sweep; sequential batches in one process).

## Exp 3 — Ternary-structured JEPA (ternary lattice transitions)
100 runs = noise σ ∈ {0.05,0.1,0.2,0.3,0.4,0.5,0.7,1.0,1.5,2.0} × 10 seeds.
Data: make_tripartite_transitions(field_dim=9), fields ternarized by
deadband=0 (median split: sign). Predictors of TERNARY field_after:
- flat: continuous TransitionPredictor(field_before, corr) → ternarize output;
- lattice: per-dim ternary table P(after|before,corr) 3×3×3 counts → argmax;
- markov1 floor (ternarized output).
Metrics: per-trit accuracy, exact-9-trit match, bit cost (log2 3^9 vs 288).
GATES:
- G1: lattice per-trit accuracy ≥ flat − 0.02.
- G2: lattice bits ≤ 5% of flat bits (14.3 vs 288 ⇒ trivially true by
  construction; the gate is that ACCURACY holds, G1 carries the weight).
- G3: lattice beats markov1 floor by ≥ +0.10 at σ=0.1.
LATTICE-PASS = G1 ∧ G3 (G2 is definitional, booked).

## Exp 4 — CM1 pinch mesh + JEV + JEPA composed
60 proposed room-state transitions: 30 valid (physics-consistent), 30 invalid
(graded: 10 mild, 10 medium, 10 egregious). Arms: A=accept-all; B=JEPA-only
(residual gate); C=JEV-only (noul pinch 0.5); D=composed ternary route:
  D = +1 accept if jev ≥ 0.5 AND resid_ok; −1 reject if jev < 0.35 OR resid
  hard-fail; 0 = hold (else).
GATES:
- G1: FAR(invalid accepted) arm-D ≤ 0.7 × min(FAR_B, FAR_C).
- G2: FRR(valid rejected/held-to-reject) arm-D ≤ min(FAR-adjusted baselines) + 0.10.
- G3: complementarity booked: count of trials where JEV and JEPA disagree.
COMPOSED-PASS = G1 ∧ G2.

## Exp 5 — Impossible-transition detector (+1/0/−1)
90 single events: 30 possible, 30 unlikely-but-valid (slow drift, rare-legal),
30 impossible (conservation/physics violations). Classifiers: JEV-only binary,
JEPA-residual-only binary, combined ternary 3-way (JEV conf × residual bands).
GATES:
- G1: combined 3-way accuracy ≥ 0.70.
- G2: unlikely-class recall ≥ 0.60 (the distinction binary detectors cannot make).
- G3: impossible-class precision ≥ 0.80.
TERNARY-DETECTOR-PASS = G1 ∧ G2 ∧ G3.

## Cost & honesty
- JEV calls: ~330 total (exp1 180, exp4 60, exp5 90). Token ledger booked.
- Seeds fixed (lab rule 2718 + derived). Negative controls where applicable
  (random-projection baseline exp2; markov1 floor exp3; accept-all exp4).
- Booking: results JSON + FINDINGS.md; negative results first-class.
