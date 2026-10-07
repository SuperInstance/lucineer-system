# FINDINGS — JEPA↔JEV Bilateral Dialogue (Lane 1)

**Run:** 2026-10-06, 72 JEV calls, jev-1.13.0 via `api.typesafe.ai/v1/systemone`, 55,247 input / 1,737 output tokens, 40.3s wall.
**Artifacts:** `dialogue-results.json` (all raw scores), `noul-analysis.png` (3 panels), `run_bilateral.py` (harness).

JEPA is **simulated** (numpy 7D room-state latent dynamics — smooth AR(1) correlated steps = "plausible"; decorrelated dimension-jumps = "implausible"). JEV judges each proposed transition with a single noul gate: *"Does this predicted state transition represent a valid room evolution?"* with the validity criteria stated in the instructions.

---

## 1. Predict → Judge (baseline, n=10)

| class | noul range | mean |
|---|---|---|
| plausible (λ 0.4–2.2) | 0.53 – 0.88 | **0.70** |
| implausible (mag 0.5–1.6) | 0.09 – 0.29 | **0.17** |

Separation 0.53, **zero overlap** at n=10. Noul is monotone in perturbation size within class (loud plausible λ=2.2 scored lowest of the plausible set; mild implausible mag=0.5 scored highest of the implausible set).

## 2. Judge → Predict (reversed — JEV states constraints first)

Asked JEV to bless next-state ranges as noul gates (v\* in 5 bins, κ in 4 bins; current state c=0.70, v\*=0.30, κ=3.0):

- **v\* gates: 0.46–0.50 — JEV hedges to a coin flip on every range.** It will not commit to a free-form interval; exactly as pre-registered ("JEV might not accept free-form ranges").
- **κ gates: 0.20–0.24 — uniformly rejected.** No 1–2-wide κ bin counts as "whole range valid in one step." This *is* usable signal: κ must move narrowly, not bin-jump.
- Prediction built from the surviving constraints (effectively: v\*≈[0.4,0.7] borderline-accepted; no κ bin accepted, so smooth κ dynamics kept) judged **0.67**; a prediction that ignored the gates judged **0.06**.

Honest caveat: because no κ range passed 0.5, the "constrained" arm degenerated to plain smooth dynamics (logged as such in the JSON — `accepted_k_ranges: []`). The 0.67-vs-0.06 contrast therefore replicates exp1's direction with constraint metadata in the state. **Takeaway: reversed direction yields weak *interval* constraints but a strong *rejection mask* — use noul gates as filters on candidate predictions, not as range oracles.**

## 3. Iterative calibration (3 rounds × 3 trajectories; JEPA absorbs via noise-scale λ and correlation-weight ρ)

| trajectory | start knobs | noul trajectory | behavior |
|---|---|---|---|
| A_wild | λ=2.6, ρ=0.2 | **0.27 → 0.45 → 0.59** | monotone recovery: each invalid judgment tames λ/boosts ρ |
| B_borderline | λ=1.4, ρ=0.6 | **0.81 → 0.43 → 0.44** | **degraded**: round-1 validity grew exploration (λ→1.57), overshot into invalid, taming didn't recover in 3 rounds |
| C_calm | λ=0.5, ρ=1.0 | 0.77 → 0.80 → 0.79 | stable |

**Iteration improves from invalid, is stable near-valid, but a naive "reward validity with exploration" rule oscillates** (B). Fix for next run: asymmetric absorption — shrink λ hard on invalid, grow it only a fraction of the shrink on valid, or gate exploration growth on noul margin above 0.5 (B's round-1 0.81 was a big margin → oversized exploration grant).

## 4. Calibration drift (50 trials, same initial state, ground truth known)

- **Plausible:** 0.714 ± 0.133, range [0.49, 0.90]
- **Implausible:** 0.215 ± 0.136, range [0.06, 0.51]
- **Bimodal with a near-empty valley at 0.4–0.5** (histogram counts: 5,9,5,3,2 | 7,6,4,7,2 — the dip sits exactly at the class boundary)
- **ROC AUC = 0.9952** (noul vs generative label). Youden threshold **0.455** (J = 0.92)
- Single overlap point: one implausible trial at 0.51 vs plausible min 0.49
- Within-class noul↔magnitude correlation: **−0.50** (plausible), **−0.70** (implausible) → noul is a *graded* score of transition violence, not a binary verdict wearing decimals

**Yes, there is a natural threshold — ≈0.45–0.50 — and it coincides with JEV's own semantic midpoint (0.5 = coin flip).** The empirical operating point and the model's built-in uncertainty semantics land on the same number, which is what you want from a calibrated pincher cell: `noul ≥ 0.5` as the default gate, 0.45 if recall matters more.

---

## Synthesis

1. **The conversation works in the forward direction.** JEV's noul cleanly rank-orders simulated JEPA predictions; 50-trial drift shows a stable bimodal distribution with a natural pinch point at ~0.46–0.5. This is the tunable gate the CM1 mesh wants, now verified on *state-transition* content rather than content triage.
2. **The reversed direction (judge-first) is a filter, not an oracle.** JEV hedges on interval acceptance (~0.5 everywhere for v\*) but issues crisp rejections (κ gates ≤0.24). Constraint elicitation should be phrased as *candidate rejection*, not range blessing.
3. **Feedback absorption converges from invalid but can destabilize the borderline band.** The failure is in the JEPA-side control rule (symmetric explore/exploit), not in JEV's judgments — B's round-2/3 predictions were genuinely wilder and were correctly scored down.
4. **Caveats, honestly booked:** (a) circularity — the validity criteria in JEV's instructions describe the same smooth/correlated dynamics the "plausible" generator implements, so AUC measures *JEV operationalizing stated criteria on numeric states*, not independent ground truth; (b) JEPA is simulated — no learned world model absorbed anything, only the knob policy did; (c) jev-1.13.0 returned bare noul (no confidence/probabilities fields) on these calls; (d) n=10/n=50 are small; the 0.51/0.49 overlap is one trial each side.

**Next:** asymmetric absorption rule + a 10-round run to test B-band recovery; re-run drift with criteria text that does NOT mirror the generator (breaks circularity); wire the 0.45/0.5 pinch into a routing cell.
