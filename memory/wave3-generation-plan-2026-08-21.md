# WAVE-3 GENERATION-CORPUS PLAN — Path B (the endgame)

**Filed: 2026-08-21. Plan only — STRICT read-only. Nothing generated, nothing
run against registered data, no repos modified.** This document pre-registers
the wave-3 generation-corpus experiment now that the forward-model instrument
exists (`scripts/riverbed_generator.py`, landed 2026-08-21), and sequences it
behind REG-1.

Grounding: `memory/kimi-ideation-2026-08-21.md` (Path B = the instrument that
makes Path A's wave-3 interpretable), `memory/foundation-synthesis-2026-08-21.md`
(REG-1, skew-product axioms, q-rule), `memory/E2E3-premise-band-movers-design-2026-08-21.md`
(the registered A/D/P/S apparatus + VOID rules), `memory/elephant-next-move-research-2026-08-21.md`
(Path B requirements §3), `/home/eileen/projects/elephant/STAGE2-CORPUS-DESIGN-2026-08-20.md`
(attendance/ladder/gate), and code inspection of `riverbed_generator.py`,
`premise_band_movers.py`, `e2_instrument.py`, `stage2_wave_gate.py`,
`e2_nights.py`, `data/nights/night-{T2,T4a,T5}.jsonl` (all read-only, today).

---

## 1. The registered wave-3 design (generation corpus)

### 1.0 The reframe (what wave-3 now is)

The verdict question is no longer "does the field corpus clear its floors" but
**model selection**: which branch of the forward model (the time-indexed vMF
random field with branch parameter α) inverts to a given corpus? The field
corpus is the inverse problem; the generation corpus is the forward model with
known ground truth. Wave-3 = run the registered apparatus on forward-model
sample paths and score **branch recovery** under contamination control.

### 1.1 Hypothesis

**H-GEN:** the registered apparatus (legs A/D/P/S + slope/ICC machinery,
unmodified) discriminates the forward model's branches: it recovers
instrument (α=0), collapse (α=1), and noise, and orders intermediate α
correctly, when (and only when) the recovery is not an artifact of the
estimator's coordinate system — demonstrated by decoy-estimator agreement.

**Anti-hypotheses:** (i) recovery is estimator-specific (only the o/d
pipeline separates branches → contamination, booked as a method finding);
(ii) the apparatus cannot separate instrument from collapse even at endpoints
(the honest negative the research note §4 contemplates — then the Riverbed
localizes *which* sufficient statistic the estimator is blind to).

### 1.2 Corpus spec (Arm 1 — direct vMF sampler, cheap)

| condition | corpora | nights×readers | notes |
|---|---|---|---|
| α ∈ {0, 0.25, 0.5, 0.75, 1} | 5 | 9 × 21 each | STAGE2 §2 ATTENDANCE matrix verbatim; frozen family schedules (flip seqs 8/20; entry seqs 12/24/28 as κ-events); seed 20260821; distinct tag prefixes |
| null-mode | 1 | 9 × 21 | flat warmth, cohesion-only κ shift (T9-null = pure flat; flip-family nulls carry the common κ shift) |
| **total Arm 1** | **6 corpora** | 54 nights | minutes of CPU each; each corpus = one wave, **never pooled** |

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
  persona space (persona-resampling map, ideation §2.1). **Separate
  registration addendum when built** (Gap G2) — Arm 1's certificate covers
  the statistics; Arm 2 covers the text→dial→reading transformation.

### 1.3 The four statistics — reused verbatim, branch-conditional predictions pre-stated

The E2/E3 registered legs run **unmodified** (same thresholds: TOL=3 speaks,
HYST 0.05/3, edges 0.3/0.6, W=12 primary; seeds 20260821; B=2000/10,000).
What wave-3 adds is the **branch×leg discrimination matrix** — each cell a
pre-registered prediction:

| leg (threshold, unchanged) | instrument α=0 | collapse α=1 | noise | discriminates |
|---|---|---|---|---|
| **A** timing (circular-shift null, p<0.05) | fires (time-locks to flips) | fires weakly or not (no reader offsets to cross) | ≈ null (no lock beyond shared κ) | signal-vs-noise |
| **D** coverage (>50% vs null-night rate) | above null | low (offsets ≈ room ⇒ ρ small, few crossings) | ≈ null-night | signal-vs-noise |
| **P** persistence (P_trans ≥ 0.5×P_rest) | holds (0.99-class, as field) | **fails** (offsets are room, not reader ⇒ pre/post cosine ≈ 0) | **holds within-night** (dev constant within night by construction) — pre-stated NON-discriminator | instrument-vs-collapse |
| **S** exposure (x-coef CI ∌ 0 AND beats roster competitor) | x-invariant (CI ∋ 0, competitor not beaten) | **falsification fires** (the registered collapse signature) | x-invariant, inflated scatter | instrument-vs-collapse |
| **ICC** (baseline stability) | ∈ [0.85, 0.96] (brackets filed 0.9076) | room-driven (unstable as "reader" constants) | **collapses** (< filed CI floor 0.667 — the prediction, not a void) | instrument-vs-noise |

**Registered branch-conditional floor/guard rules** (the subtle part — write
these or the void rules misfire on generated data):

- The ≥20-crossing floor (§5.3) applies **only where A is read**
  (instrument + intermediate corpora). On collapse/noise corpora the
  pre-stated prediction is *fewer* crossings — a low count is a **branch
  hit, not a void**.
- The ICC guard (void if below [0.667, 0.810]) applies to instrument and
  intermediate corpora only; on the noise corpus ICC collapse **is the
  ground truth to be recovered**.
- 2AFC signed directions vs increasing α (pre-registered): baseline spread ↓,
  S x-slope ↑ toward the collapse signature, P_trans ↓, D ↓, A flat-to-↓.
  Pair-ranking pass: ≥ 8/10 adjacent-pair orderings correct per leg
  (binomial p ≈ 0.011 at 8/10 under fair-coin) — else that leg's ordering
  claim fails.

### 1.4 VOID rules (adapted, all pre-stated)

1. **Generated-corpus gate failure** (manifest-based, replaces the field
   gate — see Gap G4): logged roster == designed ATTENDANCE; determinism
   re-run byte-identical; logged strata-mean warmth within ±0.10 of the
   manifest schedule (cumulative-fit lag accounted); corpus_sd computed
   from the corpus itself, finite, and used as that corpus's normalization;
   a-priori x-design Sxx ≥ 0.19.
2. Null-night crossing rate ≥ 50% of signal-night rate (per-corpus, where A
   is read).
3. < 20 counted down-crossings (branch-conditional, §1.3).
4. Continuity ladder off by > 0.10 (within-corpus estimator gate).
5. Bootstrap effective draws < 1,500.
6. **Decoy-panel disagreement** (new): if only the o/d pipeline recovers the
   branch (per-reader detrending and mixed-effects decoys disagree), the
   recovery is estimator-specific → booked as a contamination finding; no
   apparatus-validation claim is licensed.
7. **Robustness manifold, not a point:** verdict *sets* over
   W ∈ {8, 12, 16}, margin ∈ {1.5, 2, 3}·SE, hold ∈ {2, 3, 4} (ideation
   §3.4) — reported as a registered sensitivity surface.

**Explicitly NOT voids:** the field corpus's VOID-by-§5.3 stands on its own;
a clean wave-3 calibration does not retroactively convert 17 events into 20.
It licenses the sentence "the instrument is sound; the field under-delivered
events — a power statement with a calibration certificate attached."

---

## 2. REG-1 integration (W-vs-v* rotation test)

**The test (foundation synthesis, axiom 7 + REG-1):** locate the room
temperature axis via the generalized eigenproblem **C_room v = λ C_pers v**
(solver to live in `scripts/slope_regression_w2.py`); annotate
**cos(W, v*)** (leading personality eigenvector) on every warmth output;
confirm cos(W, v_temp) ∈ [0.24, 0.40] (geometric team's validated range);
rotate the ICC subspace to decouple W from v_temp; run the q-rule across
≥ 10 referent choices.

**On the generated corpus — the calibration the real corpus can never give.**
The generator *plants* the truth: the temperature axis is literally Ŵ
(μ(t) = w(t)·Ŵ + √(1−w²)·e⊥(t) by construction, `riverbed_generator.py`
`room_path`), and the personality axes are the persona-anchored deviation
directions (`persona_deviations`). So on each α-corpus:

- **Recovery of the planted temperature axis:** cos(v̂_temp, Ŵ) from the
  eigenproblem vs ground truth. Pre-state: under instrument, ≥ 0.8 (well
  above the vMF-noise null, whose distribution REG-1-existing + noise-branch
  sweeps fix before any registered corpus is read).
- **Recovery of the planted personality axis:** leading C_pers eigenvector
  vs the leading anchor PC.
- **Dose-response with known truth:** under collapse, C_pers absorbs room
  variance → eigenvalue separation shrinks and cos(v̂*, Ŵ) inflates toward 1
  — the planted-axes replay of the field's cos(W, v*) = 0.978 confound
  annotation. The α-sweep turns REG-1 from a one-shot annotation into a
  measured calibration curve: *at what α does the confound annotation stop
  being diagnostic?* No field corpus can answer that.
- Thresholds are **fixed before generation** from REG-1-on-existing + null
  sweeps (sequencing §4); they are then frozen into the registration.

---

## 3. Generator gaps (before wave-3 is runnable)

Verified by code inspection today; file:line from the current
`scripts/riverbed_generator.py`.

- **G1 (blocking, fidelity): entrants are present from t=0.** Readers blocks
  are emitted for the full roster at every speak (lines 332–345, 379–395;
  `entry_mode` all "roster", line 420) and the author schedule draws from the
  full roster from t=0 (line 316). The field omits entrants from the
  `readers` block before entry (verified: `night-T4a.jsonl` seq 5 lacks
  drifter, seq 13 has him; `logged_readings` reads presence from first
  appearance, `e2_instrument.py:213-225`). Consequence: the full-window
  NaN-before-entry convention (`premise_band_movers.py` `night_windows`)
  never fires; entry nights lose the roster-composition event; generated
  corpora are strictly easier than field. **Fix:** per-family late-start
  masks from `entry_seqs`; gate readers/authors/lens emission; emit
  entry-mode transitions.
- **G2 (blocking for Arm 2): engine-native simulator missing.** Branch
  semantics must be a persona-resampling map on `e2_nights.py:121-125`
  constructor inputs (collapse = per-night warmth-conditioned persona
  redraw; the name persists, the instrument doesn't). No code path exists.
- **G3 (blocking, honesty): no blinding.** The manifest writes
  branch/alpha/null in the clear (line 511). Need `--blind`: redacted
  manifest (branch fields stripped, tags → opaque ids) + sealed sidecar
  (sha256-locked); verdicts filed before unsealing (ideation §2.3).
- **G4 (blocking): the wave gate cannot run verbatim.**
  `stage2_wave_gate.py` hard-codes the field ladder (LADDER, line 49) and
  corpus_sd 0.2367 (line 61, asserted 88–93). Generated corpora define their
  own corpus_sd (`corpus_sd(nights)` is generic — `e2_instrument.py:262`)
  and schedule-matched warmth with cumulative-fit lag. **Fix:** riverbed
  gate per §1.4.1 (manifest-driven), replacing — never relaxing — the field
  gate's roster/determinism discipline.
- **G5 (blocking, wiring): no Measurement path for generated nights.**
  Strata and night tables are hard-coded (`W2_NIGHTS`,
  `e2_instrument.py:73-84`; strata registered per family). Need an adapter
  building `Night` objects (file + strata + roster) from the riverbed
  manifest; `premise_band_movers` is otherwise generic over waves.
- **G6 (calibration): deadband floor untuned.** `ORTH_WALK=0.02` /
  `KAPPA_JITTER=0.03` (lines 106-107) have never been checked against the
  field stable-phase d_R floor ≈ 0.29 corpus-sd (ideation §1.4: "every
  hysteresis constant is calibrated against the wrong floor" otherwise).
  Add a sweep + assert on the stable-phase d distribution.
- **G7 (calibration): ICC honesty is analytic-only** (line 303). No
  self-test measures realized between-night ICC. Add: mini instrument wave →
  realized ICC ∈ [0.85, 0.96].
- **G8 (moderate): `entry_mode` semantics differ.** Real engine logs e.g.
  `lazy-neutral` members (verified T4a seq 5); generator writes "roster" for
  all. Verify no analysis consumer; replicate if consumed.
- **G9 (minor): staged-night parity untested.** Self-test compares T2 only
  (line 601); staged opens carry `staged_entries` (verified T4a/T5).
  Speak-row key sets are identical staged vs not (verified today) — extend
  the self-test to a staged family anyway.
- **G10 (minor): CLI conflict silently ignored.** `--branch X` plus
  `--alpha` rebuilds the branch tuple (line 485), dropping X's κ_R/redraw.
  Error instead.
- **G11 (minor): author coverage not guaranteed.** Uniform author draw
  (line 316) can leave a reader with zero speaks at small n; field
  guarantees everyone speaks. Assert coverage.
- **G12 (minor): manifest lacks per-night logged warmth + corpus_sd** for
  the gate to consume; `interactions_after` counts authorships, not pairwise
  interactions (verify consumers).
- **G13 (blocking for 2AFC): no pair-matching mode.** The per-night rng is
  keyed to the full tag (`(seed, zlib_crc(tag))`), so different-branch
  corpora get *different* room paths — "matched except α" fails. Add a pair
  mode: room path seeded by (pair_seed, family) with a separate fiber rng,
  so α enters only through the fiber. (Within-night fiber draw counts are
  κ-determined, so streams stay aligned across α at fixed κ_R.)

---

## 4. Sequencing (with effort estimates)

| # | step | depends on | effort | gate |
|---|---|---|---|---|
| S0 | **REG-1 on existing corpora** (filed waves 1+2): eigensolve in `slope_regression_w2.py`, cos(W, v_temp) + CI, cos(W, v*) annotations, q-rule over ≥10 referents, ICC-subspace rotation | nothing | **0.5–1 day** (one eigensolve + bootstrap) | branch-1 range 0.24–0.40 confirmed, or a dated deviation filed |
| S1 | Generator hardening: G1, G3, G4, G5, G13 + self-test extensions (G7, G9) | — | **~1 day** | self-test green incl. new checks |
| S2 | **Registration:** this doc distilled into the topic.md addendum; all thresholds frozen from S0 | S0 | **0.5 day** | committed **before any registered corpus is generated** |
| S3 | Generation: 6 Arm-1 corpora + pairs; sealed + redacted manifests; gate runs | S1, S2 | minutes of compute; **~0.5 day** with gates | §1.4.1 gate green per corpus |
| S4 | Blinded analysis: A/D/P/S per corpus + decoy panel (build detrending + mixed-effects decoys) + REG-1-generated + 2AFC ranking | S3 | **~1 day** (0.5 build decoys, 0.5 run) | verdicts filed before unseal |
| S5 | Unblind, verdict filing, RUN doc (E2/E3-style) | S4 | **0.5 day** | — |
| S6 | Arm 2 (engine-native, G2) — separate addendum | S1–S5 | **1–1.5 days** | own registration |

**Total to S5: ~3.5–4 working days.** S0 is deliberately first: it is cheap,
runs on already-filed data, and its outputs (thresholds, referent table) are
inputs to S2's frozen registration.

---

## 5. Honesty guards

1. **Registration-before-reading.** No generated corpus is read — no legs, no
   warmth curves beyond gate mechanics — until this plan's addendum is
   committed. Boundary: the generator's `--self-test` may run pre-registration
   on throwaway seeds in scratch dirs (schema/mechanics checks only, never the
   registered statistics, never the registered corpora).
2. **The q-rule** (foundation axiom 3): every verdict must be invariant
   across ≥ 10 referent choices; referent-dependent residual motion is
   reported, and common shift is read as measurable cohesion, never as
   warmth. REG-1 branch 3 operationalizes this; wave-3 inherits it as a
   robustness column, not an option.
3. **Coordinate firewall** (already in the generator, verified): branch
   parameters live in persona/field-measure space only; nothing computes an
   offset from a roster mean, a corpus_sd, or an o/d quantity on the
   generation side.
4. **Decoy-estimator panel:** o/d pipeline + per-reader detrending +
   mixed-effects model on every corpus; **pass = branch-consistent verdicts
   across all three** (ideation §2.2). Disagreement ⇒ contamination finding.
5. **Procedural blindness:** sealed manifests, opaque tags, one agent
   generates / another analyzes; verdicts filed before unsealing.
6. **Holdout of the gate targets:** corpus_sd and WARM-as-target are never
   handed to the generator; each corpus must pass the gate on its own
   numbers (G4 enforces; ideation §2.4 — otherwise the corpus is fit-to-gate).
7. **Append-only:** `generate_wave` refuses overwrite (verified, line ~497);
   filed wave-1/wave-2 corpora untouched; T-tag discipline preserved.
8. **Never pool:** each α-corpus is its own wave; pairs are ranked, never
   pooled; no cross-corpus primary number exists.
9. **Tautology guard inherited:** crossing *rate* is never evidence (the
   near-tautology of constant numerator × bimodal denominator); only A
   (timing), P (persistence), S (x-invariance) carry content — D and rates
   are context.
10. **Priors filed up front** (E2/E3 §6 discipline): apparatus recovers
    endpoints P≈0.7; intermediate-α ordering P≈0.5; Arm-2 engine recovery
    P≈0.4; decoy-panel full agreement P≈0.6.

---

## Provenance

- Read (read-only): the six grounding documents above; `riverbed_generator.py`
  (full), `premise_band_movers.py` (§estimator/legs), `e2_instrument.py`
  (`logged_readings`, `corpus_sd`, `W2_NIGHTS`), `stage2_wave_gate.py`
  (LADDER/CORPUS_SD asserts), `e2_nights.py` (STAGED_TAGS, ATTENDANCE),
  `data/nights/night-{T2,T4a,T5}.jsonl` (schema verification: staged vs
  non-staged opens/speaks, entrant presence semantics).
- No files outside this document were written; no generation, no analysis,
  no commits.
