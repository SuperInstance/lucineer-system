# WAVE-3 GENERATION-CORPUS — S2 FROZEN REGISTRATION

**Filed: 2026-08-21. This is the frozen registration.** It executes S2 of
`memory/wave3-generation-plan-2026-08-21.md` — "this doc distilled into the
topic.md addendum; all thresholds frozen from S0; committed BEFORE any
registered corpus is generated." Nothing in this document may be altered
after commit except by dated addendum; every number below is frozen as of the
commit line in §6.

**Inputs (read, all frozen):**
- `memory/wave3-generation-plan-2026-08-21.md` — the full registered design
  (Path B, the endgame; H-GEN reframe; corpus spec; A/D/P/S apparatus; VOID
  rules; honesty guards; sequencing).
- `projects/elephant/REG1-RUN-2026-08-21.md` + `data/slope/reg1-rotation-results.json`
  — the S0 threshold source (branch verdict B; thresholds 0.80/0.60/0.80;
  ε = 1e-2 floored-whitening; reader-clustered bootstrap B=2000 seed 20260821).
- `memory/kappa-t-check-2026-08-21.md` — the K-leg rework verdict (entries are
  μ-events, not κ-events; κ polarity warm-tight/cold-loose; entry loosens κ).
  The registration reflects the **corrected** generator, not the falsified one.
- `projects/zeroclaw-dissertation/research/topic.md` — the claim inventory
  (append-only, R4 discipline; advisory lines annotate, never rewrite).

---

## 1. Pre-registered design (frozen)

### 1.0 The reframe

Wave-3 is **model selection, not field verdict.** The verdict question is
which branch of the forward model (the time-indexed vMF random field with
branch parameter α) inverts to a given corpus. The field corpus is the inverse
problem; the generation corpus is the forward model with known ground truth.
Wave-3 runs the registered apparatus on forward-model sample paths and scores
**branch recovery** under contamination control.

### 1.1 Hypothesis (frozen)

**H-GEN:** the registered apparatus (legs A/D/P/S + slope/ICC machinery,
unmodified) discriminates the forward model's branches: it recovers
instrument (α=0), collapse (α=1), and noise, and orders intermediate α
correctly, when (and only when) the recovery is not an artifact of the
estimator's coordinate system — demonstrated by decoy-estimator agreement.

**Anti-hypotheses:** (i) recovery is estimator-specific (only the o/d
pipeline separates branches → contamination, booked as a method finding);
(ii) the apparatus cannot separate instrument from collapse even at endpoints
(the honest negative — then the Riverbed localizes *which* sufficient
statistic the estimator is blind to).

### 1.2 Corpus spec (Arm 1 — direct vMF sampler)

| condition | corpora | nights×readers | notes |
|---|---|---|---|
| α ∈ {0, 0.25, 0.5, 0.75, 1} | 5 | 9 × 21 each | STAGE2 §2 ATTENDANCE matrix verbatim; frozen family schedules (flip seqs 8/20; entry seqs 12/24/28 as **μ-events** per the K-leg rework, §3); seed 20260821; distinct tag prefixes |
| null-mode | 1 | 9 × 21 | flat warmth, cohesion-only κ shift (T9-null = pure flat; flip-family nulls carry the common κ shift) |
| **total Arm 1** | **6 corpora** | **54 nights** | minutes of CPU each; each corpus = one wave, **never pooled** |

- **Strata transitions:** the 9 frozen T-family schedules (manifest
  `flip_seq`/`entry_seqs`); strata labels mirror `W2_NIGHTS` per family.
- **Null nights:** T9-null (and S5-analog) inside every corpus — the
  null-night void rule must be satisfiable per-corpus.
- **Adversarial pairs (2AFC):** adjacent-α pairs (0/0.25, 0.25/0.5, 0.5/0.75,
  0.75/1) + endpoint pair (0/1), matched in everything but α — same room
  paths, same rosters, same κ(t) (requires Gap G13's pair mode). The
  registered pipeline *ranks* each pair; pre-registered signed directions
  (§1.4). Robust to any bias affecting both conditions equally.
- **Arm 2 (engine-native, the hard version):** 3 corpora at α ∈ {0, 1, α*}
  through `TapNightSession` with branch parameters expressed purely in
  persona space. **Separate registration addendum when built** (Gap G2) —
  Arm 1's certificate covers the statistics; Arm 2 covers the
  text→dial→reading transformation.

### 1.3 The four statistics — verbatim, branch-conditional predictions pre-stated

The E2/E3 registered legs run **unmodified**. Frozen thresholds: TOL = 3
speaks, HYST 0.05/3, edges 0.3/0.6, W = 12 primary; seeds 20260821;
B = 2000 / 10,000. The four statistics, verbatim:

- **(A) timing** — mean over counted down-crossings of 1[within 3 speaks of a
  registered transition] vs 10,000 per-reader-night circular-shift nulls,
  seed 20260821.
- **(D) coverage** — fraction of night-level signal transitions with a
  counted down-crossing within ±3 speaks vs the null-night midpoint rate
  (T9/S5), exact binomial.
- **(P) persistence** — cosine of pre- vs post-transition offset vectors over
  the roster (ICC-reliable subspace), Fisher-z pooled, vs persistence-at-rest
  within a stratum; threshold P_trans ≥ 0.5×P_rest.
- **(S) exposure** — per-night median ρ regressed on night warmth x with
  reader fixed effects vs a roster-composition competitor (size,
  archetype-baseline warmth), reader-clustered bootstrap B = 2000, nested
  permutation 10,000.

**The branch×leg discrimination matrix** (each cell a pre-registered
prediction; frozen):

| leg (threshold, unchanged) | instrument α=0 | collapse α=1 | noise | discriminates |
|---|---|---|---|---|
| **A** timing (circular-shift null, p<0.05) | fires (time-locks to flips) | fires weakly or not (no reader offsets to cross) | ≈ null (no lock beyond shared κ) | signal-vs-noise |
| **D** coverage (>50% vs null-night rate) | above null | low (offsets ≈ room ⇒ ρ small, few crossings) | ≈ null-night | signal-vs-noise |
| **P** persistence (P_trans ≥ 0.5×P_rest) | holds (0.99-class, as field) | **fails** (offsets are room, not reader ⇒ pre/post cosine ≈ 0) | **holds within-night** (dev constant within night by construction) — pre-stated NON-discriminator | instrument-vs-collapse |
| **S** exposure (x-coef CI ∌ 0 AND beats roster competitor) | x-invariant (CI ∋ 0, competitor not beaten) | **falsification fires** (the registered collapse signature) | x-invariant, inflated scatter | instrument-vs-collapse |
| **ICC** (baseline stability) | ∈ [0.85, 0.96] (brackets filed 0.9076) | room-driven (unstable as "reader" constants) | **collapses** (< filed CI floor 0.667 — the prediction, not a void) | instrument-vs-noise |

**Registered branch-conditional floor/guard rules** (frozen — the subtle part
that keeps the void rules from misfiring on generated data):

- The ≥20-crossing floor applies **only where A is read** (instrument +
  intermediate corpora). On collapse/noise corpora the pre-stated prediction
  is *fewer* crossings — a low count is a **branch hit, not a void**.
- The ICC guard (void if below [0.667, 0.810]) applies to instrument and
  intermediate corpora only; on the noise corpus ICC collapse **is the ground
  truth to be recovered**.
- 2AFC signed directions vs increasing α (pre-registered): baseline spread ↓,
  S x-slope ↑ toward the collapse signature, P_trans ↓, D ↓, A flat-to-↓.
  Pair-ranking pass: ≥ 8/10 adjacent-pair orderings correct per leg
  (binomial p ≈ 0.011 at 8/10 under fair-coin) — else that leg's ordering
  claim fails.

### 1.4 VOID rules (frozen, all pre-stated)

1. **Generated-corpus gate failure** (manifest-based, replaces the field
   gate — Gap G4): logged roster == designed ATTENDANCE; determinism re-run
   byte-identical; logged strata-mean warmth within ±0.10 of the manifest
   schedule (cumulative-fit lag accounted); corpus_sd computed from the corpus
   itself, finite, and used as that corpus's normalization; a-priori x-design
   Sxx ≥ 0.19.
2. Null-night crossing rate ≥ 50% of signal-night rate (per-corpus, where A
   is read).
3. < 20 counted down-crossings (branch-conditional, §1.3).
4. Continuity ladder off by > 0.10 (within-corpus estimator gate).
5. Bootstrap effective draws < 1,500.
6. **Decoy-panel disagreement** (new): if only the o/d pipeline recovers the
   branch (per-reader detrending and mixed-effects decoys disagree), the
   recovery is estimator-specific → booked as a contamination finding; no
   apparatus-validation claim is licensed.
7. **Robustness manifold, not a point:** verdict *sets* over W ∈ {8, 12, 16},
   margin ∈ {1.5, 2, 3}·SE, hold ∈ {2, 3, 4} — reported as a registered
   sensitivity surface.

**Explicitly NOT voids:** the field corpus's VOID-by-§5.3 stands on its own;
a clean wave-3 calibration does not retroactively convert 17 events into 20.
It licenses the sentence "the instrument is sound; the field under-delivered
events — a power statement with a calibration certificate attached."

---

## 2. Frozen thresholds (from REG-1, S0)

Frozen from `REG1-RUN-2026-08-21.md` and `reg1-rotation-results.json`
(branch verdict B — warmth is reader personality; the confound annotation
cos(W, v*) ≤ 0.44 with CI ≤ 0.50 on field data is a filed quantity):

1. **Branch thresholds: 0.80 / 0.60 / 0.80.** Pre-stated in the REG-1 script
   header before the run: A (room temperature) iff cos(W, v*) ≥ 0.80 and
   CI-lo > 0.60; B (reader personality) iff cos(W, PC1_pers) ≥ 0.80 and
   cos(W, v*) < 0.80; C (rotated axis) otherwise. Frozen as the S2
   registration inputs.
2. **Solver: floored-whitening generalized eigensolve, ε = 1e-2.** C_pers
   eigenvalue floor at ε·λ_max(C_pers); the reliable-subspace answer is
   ε-stable (0.142/0.106 across ε ∈ [1e-4, 5e-2], 0 floored dirs) and is the
   anchor; the full-7 answer is ε-sensitive and is not the headline.
3. **Dead-dial warning (frozen):** any corpus where a dial has < ~1% of the
   leading personality variance (panic in wave-1) must floor, not ridge — the
   unfloored solve fabricates a temperature axis from the null space.
4. **Bootstrap: reader-clustered, B = 2000, seed 20260821** — CIs.
5. **On the generated corpus — the calibration the real corpus can never
   give (frozen expectations):** recovery of the planted temperature axis
   cos(v̂_temp, Ŵ) ≥ 0.8 under instrument (well above the vMF-noise null);
   recovery of the planted personality axis = leading C_pers eigenvector vs
   the leading anchor PC; dose-response under collapse (C_pers absorbs room
   variance → eigenvalue separation shrinks, cos(v̂*, Ŵ) inflates toward 1).
   The α-sweep turns REG-1 from a one-shot annotation into a measured
   calibration curve: *at what α does the confound annotation stop being
   diagnostic?*
6. **Priors (filed up front, E2/E3 §6 discipline):** apparatus recovers
   endpoints P≈0.7; intermediate-α ordering P≈0.5; Arm-2 engine recovery
   P≈0.4; decoy-panel full agreement P≈0.6.

---

## 3. The corrected generator contract (K-leg rework)

The κ(t)-around-entry-steps check (`memory/kappa-t-check-2026-08-21.md`)
falsified the generator's κ-trajectory-first presupposition. **The registered
generator is the corrected one, not the falsified one.** The corrected
contract, frozen here:

1. **Entries are μ-events (direction events), not κ-events.** The mean
   direction μ moves at entry at the same magnitude as a warm→cynical flip
   (dwarmth −0.147 vs −0.151, p = 0.68; ‖Δμ̂‖ +0.301 vs +0.329, p = 0.48).
   The generator must model entry as the entrant's text shifting μ̂ toward
   the entrant's vibe (a smaller flip), with κ as a derived (heterogeneity)
   response — not a designed control channel.
2. **κ polarity: warm-tight / cold-loose.** Field: warm (SEG1) content →
   κ ≈ 24 (tight); cynical (SEG2) content → κ ≈ 11 (loose). The falsified
   generator ran warm strata κ = 10 ("loose"), cold strata κ = 18 ("tight")
   — opposite. Corrected: warm = tight, cold = loose.
3. **Entry loosens κ (not a +12 tightening pulse).** Field shows all entry
   Δlogκ < 0; the generator's +12 tightening pulse decaying from each entry
   is sign-wrong and must be removed/reversed.

**Commit status: PENDING-IF-NOT-LANDED.** As of this registration the K-leg
rework has not landed in `scripts/riverbed_generator.py` (the falsified
κ-first header, warm-loose/cold-tight stratum levels at lines 147–148/300, and
the +12 entry pulse at lines 305–307 remain). The elephant S1 commit
`1c7d790` closed G1/G3/G4/G5/G13 but did **not** include the κ rework. The
rework commit is hereby registered as a required dependency of wave-3
generation (S3): **S3 may not begin until the K-leg rework lands and is
referenced by SHA in a dated addendum to this document.** If it does not land,
wave-3 generation does not proceed and the registration stands unread.

---

## 4. Branch tables (R5) — verdicts pre-stated for every branch of every leg

No post-hoc reading is possible. For each (branch, leg) cell the observed
outcome maps to exactly one pre-stated verdict. The four branches: **instrument**
(α=0), **intermediate** (α ∈ {0.25, 0.5, 0.75}), **collapse** (α=1), **noise**
(null-mode). Legs: A, D, P, S, ICC.

### 4.1 Leg A — timing (circular-shift null, p < 0.05)

| branch | PASS | KILL | INDETERMINATE | VOID |
|---|---|---|---|---|
| instrument | A fires (time-locks to flips, p < 0.05) | A does not fire (p ≥ 0.05) | — | < 20 crossings (floor applies; A not read) |
| intermediate | A fires (time-locks, weakening with α) | A does not fire while ≥ 20 crossings exist | — | < 20 crossings (floor applies; A not read) |
| collapse | A fires weakly or not (low count is the branch hit) | A fires strongly (time-locks, p < 0.05) — misread as instrument | — | *no void on low count* (branch hit, not void) |
| noise | A ≈ null (no lock beyond shared κ, p ≥ 0.05) | A fires (p < 0.05) — spurious lock | — | *no void on low count* (branch hit, not void) |

### 4.2 Leg D — coverage (> 50% vs null-night rate)

| branch | PASS | KILL | INDETERMINATE | VOID |
|---|---|---|---|---|
| instrument | D above null (signal ≫ null-night rate) | D ≤ null (signal not covered) | — | null-night crossing rate ≥ 50% of signal (void rule 2) |
| intermediate | D above null, decreasing with α | D ≤ null | — | null-night crossing rate ≥ 50% of signal |
| collapse | D low (few crossings; ≈ null-night) | D clearly above null (misread as instrument) | — | *low D is the branch hit, not a void* |
| noise | D ≈ null-night | D clearly above null | — | *low D is the branch hit, not a void* |

### 4.3 Leg P — persistence (P_trans ≥ 0.5×P_rest)

| branch | PASS | KILL | INDETERMINATE | VOID |
|---|---|---|---|---|
| instrument | P holds (P_trans ≥ 0.5×P_rest; 0.99-class) | P fails (P_trans < 0.5×P_rest) | — | < 20 crossings (P unreadable with A) |
| intermediate | P holds, P_trans decreasing with α | P fails | — | < 20 crossings |
| collapse | **P fails** (offsets are room ⇒ pre/post cosine ≈ 0) | P holds (offsets persist — misread as instrument) | — | — |
| noise | P holds within-night — **pre-stated NON-discriminator** (dev constant within night by construction; carries no branch information) | — | — | — |

### 4.4 Leg S — exposure (x-coef CI ∌ 0 AND beats roster competitor)

| branch | PASS | KILL | INDETERMINATE | VOID |
|---|---|---|---|---|
| instrument | x-invariant (CI ∋ 0, competitor not beaten) | falsification fires (CI ∌ 0 AND beats competitor) — misread as collapse | — | — |
| intermediate | x-invariant trending toward collapse signature (S x-slope ↑ with α) | — | — | — |
| collapse | **falsification fires** (the registered collapse signature: CI ∌ 0 AND beats competitor) | x-invariant (collapse signature absent) | — | — |
| noise | x-invariant, inflated scatter | CI ∌ 0 AND beats competitor | — | — |

### 4.5 Leg ICC — baseline stability

| branch | PASS | KILL | INDETERMINATE | VOID |
|---|---|---|---|---|
| instrument | ICC ∈ [0.85, 0.96] (brackets filed 0.9076) | ICC outside the bracket | ICC ∈ (0.810, 0.85) — above guard, below bracket | ICC below guard [0.667, 0.810] (void rule — guard applies to instrument) |
| intermediate | ICC within/near the instrument bracket | ICC collapses | ICC ∈ (0.810, 0.85) | ICC below guard [0.667, 0.810] (guard applies to intermediate) |
| collapse | ICC room-driven (unstable as "reader" constants) | ICC stable (misread as instrument) | — | — |
| noise | **ICC collapses** (< filed CI floor 0.667 — the prediction, not a void) | ICC stable | — | *collapse is the ground truth, not a void* |

### 4.6 Decoy-panel — the estimator-independence gate (every branch, every leg)

| outcome | verdict |
|---|---|
| o/d pipeline + per-reader detrending + mixed-effects decoys all agree on the branch | **PASS** — branch-consistent verdicts across all three |
| only the o/d pipeline recovers the branch; the two decoys disagree | **VOID (contamination finding)** — recovery is estimator-specific; no apparatus-validation claim is licensed (void rule 6) |

---

## 5. Honesty guards (frozen)

1. **Registration-before-reading.** No generated corpus is read — no legs, no
   warmth curves beyond gate mechanics — until this registration is committed.
   The generator's `--self-test` may run pre-registration on throwaway seeds
   in scratch dirs (schema/mechanics checks only, never the registered
   statistics, never the registered corpora).
2. **Sealed manifests + procedural blindness.** Redacted manifests (branch
   fields stripped, tags → opaque ids) + sealed sidecar (sha256-locked); one
   agent generates, another analyzes; verdicts filed before unsealing
   (Gap G3).
3. **Decoy-estimator panel.** o/d pipeline + per-reader detrending +
   mixed-effects model on every corpus; pass = branch-consistent verdicts
   across all three (void rule 6).
4. **Gate-target holdout.** corpus_sd and WARM-as-target are never handed to
   the generator; each corpus must pass the gate on its own numbers (Gap G4).
5. **Never pool.** Each α-corpus is its own wave; pairs are ranked, never
   pooled; no cross-corpus primary number exists.
6. **Coordinate firewall.** Branch parameters live in persona/field-measure
   space only; nothing computes an offset from a roster mean, a corpus_sd, or
   an o/d quantity on the generation side (verified in the generator).
7. **q-rule referent-invariance.** Every verdict must be invariant across
   ≥ 10 referent choices; referent-dependent residual motion is reported;
   common shift is read as measurable cohesion, never as warmth. Inherited as
   a robustness column, not an option.
8. **Tautology guard.** Crossing *rate* is never evidence; only A (timing),
   P (persistence), S (x-invariance) carry content — D and rates are context.
9. **Append-only.** `generate_wave` refuses overwrite; filed wave-1/wave-2
   corpora untouched; T-tag discipline preserved.

---

## 6. The commit line (for the topic.md ADVISORY append)

The single sentence appended to `zeroclaw-dissertation/research/topic.md`
(annotate-only, append-only; nothing above the last line changes):

> **Filed:** wave-3 generation-corpus experiment registered and frozen
> (`memory/wave3-registration-2026-08-21.md`) — H-GEN branch-recovery design,
> REG-1 thresholds 0.80/0.60/0.80 and ε=1e-2, every branch×leg verdict
> pre-stated (R5), K-leg rework pending, committed before any registered
> corpus is generated.

---

## Provenance

Read (read-only): the four input documents above; the topic.md claim inventory
(append target). No registered corpus generated; no generated corpus read;
no registered claim modified. Written: this document; the topic.md advisory
line (append-only); the master-branch commit (below).
