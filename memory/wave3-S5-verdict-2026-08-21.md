# WAVE-3 S5 — UNBLINDING + VERDICT (Arm 1 closed)

**Filed 2026-08-21 (S5). Executes the registered unblinding of the wave-3
generation-corpus plan. Blinded verdicts were filed first (S4,
`memory/wave3-S4-analysis-2026-08-21.md`); this step opened the seals and
adjudicated. Elephant run doc: `projects/elephant/docs/wave3-S5-verdict-2026-08-21.md`
(commit `6e7be88`); machine-readable:
`projects/elephant/data/wave3/s5-unblinded-summary.json` + `s5-icc.json`.**

## 1. Unsealing

Registered G3 procedure (S3 run doc §3): sidecar copy-back +
`riverbed_generator.py --unblind`. **Seal chain verified 16/16, zero tamper
failures** (manifest pins sidecar sha256; sidecar pins all 9 night sha256s).
Seals are one-time in effect — verdicts preceded opening; the study is now
permanently unblinded.

**α-truth:** w3k01=0 · w3k02=.25 · w3k03=.5 · w3k04=.75 · **w3k05=1
(collapse)** · w3k06=null-mode (flat/redraw) · pairs q1–q5 with m = the
lower-α member in every pair (q5 = endpoint 0/1), pair-seeds 2101–2105.

## 2. THE VERDICT (branch tables R5, adjudicated)

**H-GEN FALSIFIED → anti-hypothesis (ii), the honest negative, CONFIRMED.**
Signal-vs-noise recovered 16/16; instrument-vs-collapse 0/3 — every α=1
corpus read as instrument.

- **A**: instrument PASS (3/3 fire p≈0); intermediate PASS-fire/ordering-fail;
  **collapse KILL** (fires strongly — the pre-stated "misread as instrument"
  cell, 3/3); noise PASS (silent; lone start-ref p=.031 = 1/48 chance).
- **D**: instrument PASS; intermediate PASS/trend-fail; **collapse KILL 2/3**
  (1/3 uninformative — q5 D_null=1.0 on n=1); noise PASS.
- **P**: instrument PASS (0.99-class); intermediate PASS/trend-fail (pair
  gaps ≈2e-4); **collapse KILL** (holds 3/3 — the registered headline
  discriminator's KILL column); noise non-discriminator as pre-stated.
- **S**: instrument PASS (x-invariant); intermediate PASS/trend-fail;
  **collapse KILL** (signature absent 0/96 channels); noise PASS.
- **ICC** (computed at unblinding, registered adapter): instrument .729–.877
  PASS on the G6 re-band [0.60,0.80] (w3k01 .877 above top, inside the
  superseded original bracket — annotated); collapse .791–.805
  **non-discriminating** (G6-disclosed); **noise 0.260 — collapses, the
  prediction verified** (G6's 0.228 confirmed at 0.260).
- **2AFC**: FAIL — no pair separable at any channel; blinded majority calls
  3/5 vs truth (m was lower-α in all 5) = chance; P_trans ranking 0/5.
- **Gradient**: FAIL — α IS a total order, yet every signed direction
  violates it at ~chance (spread: 5/10 violations under the TRUE order).
- **Anti-hypothesis (i) not triggered**: no estimator recovered branches at
  all → structural channel invisibility, not estimator-specific
  contamination.

## 3. α-verification of the localization — VERIFIED (was inferred at S4)

Triple-verified: (1) generator source line 845 — α enters ONLY the anchor
(`vibe0 = pool + (1−α)·dev`); (2) the three α=1 corpora are indistinguishable
from α=0 on every leg; (3) α-only pairs separate 1–2 orders below room-draw
scatter on every statistic (A ~18×, P_trans ~16×, S ~10×, spread ~75×, ICC
~28× between/within). Every between-corpus trend (spread clusters 1.34×,
standalone ICC decline, S-slope scatter) **evaporates inside the pairs** —
room-draw-carried. P is pinned by the within-night-constant charisma-pull
fiber; S's power is below anchor-scale variation at this n; A/D read only
the α-invariant room path. The localization finding stands as filed, now
against true labels.

## 4. Deferred items adjudicated

- **ICC**: computed (above). PASS instrument-vs-noise; non-discriminating
  instrument-vs-collapse.
- **Decoy-panel v6**: NOT EVALUABLE, MOOT — no decoy outputs filed at S3;
  rule 6 only voids validation claims and none exists (honest negative).
  Lesson: decoys filed S3-side next registration.
- **Five W8-only v3 cells**: w3k05.W08.can (19, collapse) = branch hit;
  w3q1m 16/18 + w3q1n 17/18 (instrument/intermediate) = floor-VOIDs, W8
  sensitivity only. Primary channel clean (min 23).
- **v2 void** (w3k05 W8|can): stands conservatively; branch-consistent read
  is branch-hit (collapse — A not read there).
- **S4 booked item 4**: RESOLVED — w3k06 IS the null corpus (seal-verified);
  signal-vs-noise pass stands.
- **Unexecuted registered expectation (disclosed)**: §2.5's cos(v̂_temp, Ŵ)
  calibration curve never ran in the blinded window; post-hoc-only now;
  booked for the next registration.

## 5. Next-wave generator change (S5 → next-registration handoff)

**Diagnosis:** α was injected into a channel the registered legs cannot see
(anchor upstream of the fiber). **Primary proposal:** re-point α into the
fiber's within-night target trajectory — `target_R(t) = pool + (1−α)·dev_R +
α·room(t)` (room(t) = the latent AR(1) wobble, already shared pairwise): at
α=1 readings track the moving room (time-varying room-carried offsets → P's
pre/post cosine decorrelates — the registered collapse signature becomes
reachable); at α=0 they track dev. Coordinate firewall intact; 2AFC pair
mode isolates it exactly. **Secondary:** register an anchor-reading leg as an
apparatus extension. **Rejected:** α-scaled room-path amplitudes (A/D would
fire on amplitude, not carrier). **Keep:** matched pairs (they proved
α-invisibility), sealed sidecars, S3-side decoys, pre-S4 calibration curve.

## 6. Dissertation-usable statement

> Wave-3 ran the registered field apparatus on a sealed, ground-truthed
> forward-model corpus (16 corpora: α ∈ {0,.25,.5,.75,1} + null + five
> α-only matched pairs) and returned the honest negative pre-stated as
> anti-hypothesis (ii): the apparatus discriminates signal-vs-noise (16/16;
> ICC .73–.88 vs .26) but cannot separate instrument from collapse even at
> endpoints — and the sealed α-truth verifies the localization: the branch
> parameter lives in a per-night persona anchor upstream of a
> within-night-constant charisma-pull fiber, a sufficient statistic to which
> every registered leg is provably blind (α-only pairs separate 1–2 orders
> below room-draw scatter on every statistic). The negative is a calibration
> bound on the apparatus's detection envelope, and the matched-pair design
> that established it is itself a registered methodological result.

## Provenance

Read: registration + G6 addendum; S3 run doc; S4 analysis + summary; 96 leg
files (S4 numbers); sealed sidecars (opened per procedure);
`riverbed_generator.py` line 845. Written: this document; elephant
`docs/wave3-S5-verdict-2026-08-21.md`, `s5-unblinded-summary.json`,
`s5-icc.json` (commit `6e7be88`); topic.md advisory line (annotate-only).
No frozen document edited; no sealed datum altered.
