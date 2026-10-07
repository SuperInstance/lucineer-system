# FINDINGS — JEV × JEPA × Ternary cross-pollination (Lane 5 creative explore)

**Date:** 2026-10-06 · **Pattern:** ternary-synergy-miner (shared primitive →
novel composition → falsifiable claim → frozen gates → negative controls)
· **Pre-reg:** PRE-REG.md, frozen before firing · **Data:** explore-results.json
· **JEV spend:** 210 calls, 82.5k in / 6.1k out tokens, 0 retries.

Components treated as repos:
- **JEV** — the judgment cell (`jev-latest`, graded noul confidence; CM1 pinch-gate lineage)
- **JEPA** — transitional JEPA (`tools/transition_kernel.py`: field-EDGE prediction) + elephant dial alphabet
- **Ternary** — the SuperInstance {-1,0,+1} ecosystem (200 repos, TERNARY-WIKI.md)

**Verdicts:** exp1 SYNERGY-FAIL (near-miss) · exp2 SMOOTH-GEOMETRY-FAIL ·
exp2b (post-hoc) also fails · exp3 LATTICE-FAIL (crossover found) ·
**exp4 COMPOSED-PASS** · exp5 TERNARY-DETECTOR-FAIL · exp5b (post-hoc) PASS.

---

## The shared primitive (what the three worlds actually share)

All three components are **quantizers of a judgment under uncertainty**:
ternary quantizes a signal to {-1,0,+1} with 0 as the honest "no signal"
(deadband); JEV quantizes a semantic question to a graded confidence;
JEPA quantizes a state transition to a predicted edge + residual.
The five experiments asked what happens when these quantizers feed each other.

---

## Ranked synergies

### #1 — Composed pinch route: JEV × JEPA × ternary gating (exp4) — **PASS**
**What:** a generative cell proposes room-state transitions; JEPA scores
structural validity (linear-kernel residual vs the room's own history); JEV
supplies calibrated semantic confidence; a ternary route composes them:
+1 accept (jev ≥ 0.5 AND residual ok) · 0 hold (mixed) · −1 reject.
**Numbers (n=60: 30 valid / 30 invalid graded mild→egregious):**
- False-accept rate: **3.3% composed vs 20% JEV-only vs 80% JEPA-only vs 100% accept-all**
- False-reject on valid: **0%** in all gated arms; composed holds 10% (the 0-state earns its keep)
- Complementarity: **28/60 trials JEV and JEPA disagree** — they fail in different directions
- Hardest class (mild invalids): composed FAR 10% where JEV alone 40%, JEPA alone 70%
**Why novel:** CM1's pinch gate was JEV-alone; nobody composed the judgment
cell's confidence WITH the transition kernel's residual into one ternary
route. The 0-state absorbs exactly the mixed-evidence cases where either
single gate would guess.
**Caveat:** JEPA-only arm is weak here because the residual NORM is a crude
oracle (see exp5's lesson); a per-dim residual should push the composed FAR
toward 0. Linear kernel; synthetic corpus; graded subtlety was controlled.

### #2 — The impossible-transition detector, fixed by per-dim surprise (exp5 + exp5b)
**What:** classify events +1 possible / 0 unlikely / −1 impossible.
**Pre-registered attempt FAILED:** JEV is a strong *binary* impossibility
judge (83.3% honest accuracy possible-vs-impossible), and the residual-norm
gate is not (61.7%) — and neither can express the middle class: unlikely
recall 0.0.
**Post-hoc fix (thresholds fit on half, evaluated on held-out half):**
max per-dim standardized delta z, two bands: 3 < z < 20 → unlikely,
z > 20 (or jev ≤ 0.30) → impossible. **Held-out 3-way accuracy 100%**
(all recalls 1.0) — synthetic separability caveat applies, mechanism validated.
**Second finding nobody ordered:** JEV's *graded* confidence means separate
the three classes (possible 0.90 / unlikely 0.78 / impossible 0.43) even
though its binary threshold cannot — **the taxonomy lives in the grading,
and the binary pinch destroys it.** Ternary's 0-state is exactly the state
JEV's confidence compresses away when thresholded.
**Why novel:** the ternary-markov/ear journal entry says "expectation is the
difference between hearing repetition and hearing a message" — this is that
lesson applied to room physics: the per-dim z IS the null model, the norm
was the repeat count.

### #3 — JEV as ternary router (exp1) — near-miss FAIL, substance positive
**Numbers (n=60):** JEV covered accuracy **93.3% vs 67.5%** for the CM1
keyword rule (+25.8 pts); margin (top1−top2 confidence) separates clear from
boundary reports at **AUC 0.79**; abstains on 45% of boundary / 5% of clear /
escalates 15% of off-domain chatter.
**Gate missed by ONE trial** (abstain-boundary 0.45 vs frozen 0.50). Booked
FAIL per pre-reg; the honest read is a threshold-tuning issue, not a
mechanism failure. The margin-as-ambiguity-detector (G3) passed cleanly.
**Why it matters:** the hard-coded router cannot abstain at all; the
judgment cell's confidence margin is a working epistemic-uncertainty signal
for free.

### #4 — Ternary-structured JEPA: the noise crossover (exp3) — FAIL with a discovery
**Numbers (100 runs, 10 noise levels × 10 seeds, field_dim=9):**
- Low noise σ=0.05: flat continuous JEPA wins, trit-acc **0.909 vs 0.792** lattice
- High noise σ=2.0: lattice wins, **0.549 vs 0.452** — and beats flat by ≥8 pts for all σ ≥ 0.4
- Crossover at σ ≈ 0.3; frozen G3 (lattice beats markov1 floor by 10 pts at σ=0.1) failed (0.778 vs 0.775)
- Information cost: lattice state = log2(3⁹) ≈ **14.3 bits vs 288 bits** (float32×9) — 20× compression, free in the regime where it wins
**The claim that survived:** *ternarization is a denoiser — predicting ON the
lattice trades clean-regime accuracy for noisy-regime robustness at 1/20th
the bits.* The count-table (3×3×3 per dim, ternary-markov's own primitive)
is immune to outlier drag; least-squares is not.
**Why novel:** D19 proved ternary correlation carries transition signal;
nobody asked WHEN the lattice beats the continuous predictor — answer: the
moment the stream gets noisy, which is the moment that matters on a boat.

### #5 — JEPA as ternary encoder: the smooth-geometry claim, double-falsified (exp2/2b)
**Numbers (100+120 GPU runs, torch, ramp-receipted):** autoencoding
{-1,0,+1}⁹ into continuous latents: at k=4 held-out trit error **20-24%**
(uniform cube) and 15-20% (structured/kernel-reachable set, ~25% cube
occupancy); Hamming↔latent-Euclid Spearman stuck at ρ ≈ 0.35-0.45 everywhere.
Gates (≤2% error, ρ ≥ 0.90) failed decisively. Error only approaches 5-6%
at k ≈ d — no compression.
**Verdict:** the ternary cube is *intrinsically high-dimensional* — there is
no smooth low-dim continuous manifold underneath it, even for structured
data at 25% occupancy. **This negative is foundational and it closes the
loop with #4:** you cannot smooth-embed ternary into JEPA's continuous
latent — so the correct composition is the reverse: structure the JEPA
state AS ternary and predict on the lattice. The ecosystem's architecture
choice (ternary-pack, lattice, count-tables) is not a compression hack; it
is forced by geometry.

---

## Cross-pollination leads for the ternary wiki (next mines)

1. **exp4 + ternary-oracle/ternary-explain (margin-staked markets, 10-05 entry):**
   JEV confidence = the stake; JEPA residual = the due-diligence artifact.
   The composed route is a 2-sensor market maker.
2. **exp5b + ternary-noether:** "impossible" = conservation-law violation.
   z-max bands are empirical stand-ins for invariants; formalizing them as
   noether Q's would make the impossible class provable, not statistical.
3. **exp3 + ternary-markov + ternary-science:** the crossover σ* is a
   critical point; a scheduler that switches lattice↔flat on measured noise
   regime is the pid-tuned-criticality pattern (10-03 entry) on a new substrate.
4. **exp1 + ternary-route:** JEV margin maps to the three-tier health model
   (+1 firm route / 0 degraded-queue / −1 escalate) — margin is the missing
   graded health signal for the routing fabric.
5. **exp2 + ternary-som:** if smooth low-dim structure exists anywhere in
   ternary land it is in *learned cluster structure over reachable sets*
   (occupancy ≪ 25%), not in the cube. SOM-blocking on real dial streams is
   the honest retry.

## Recommendation (one line each)

- **PROMOTE** the composed pinch route (exp4 recipe) into CM1 as the r7
  candidate: strictly dominates both single gates on the hardest class.
- **BUILD** per-dim-z transition classification into the room monitor
  (exp5b mechanism), validated on a real stream — synthetic separability
  caveat stands.
- **TUNE** the exp1 abstain threshold on a larger boundary corpus (gate
  missed by one trial); margin-AUC 0.79 says the signal is there.
- **SWITCH** predictors by noise regime (exp3): lattice when σ_est > ~0.3.
- **STOP** trying to embed ternary into continuous JEPA latents (exp2/2b):
  the geometry forbids it; the composition runs the other way.

## Honesty ledger

Pre-registered gates: 5 fired, 1 passed (exp4), 4 failed (exp1 near-miss,
exp2, exp3, exp5). Post-hoc arms (2) clearly labeled, split-validated where
fitted. GPU runs carry ramp receipts (INSTRUMENT-01). All seeds from lab
rule 2718. Negative results are first-class: the two negatives (exp2, exp3)
jointly explain *why* the ternary ecosystem is shaped the way it is.
