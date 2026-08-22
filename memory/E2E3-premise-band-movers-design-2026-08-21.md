# E2/E3 PREMISE BAND-MOVERS — Experiment Design

**Filed: 2026-08-21 (design only).** Companion to `SLOPE-REGRESSION-2026-08-20.md` + `STAGE2-RUN-2026-08-20.md` (elephant) and `e2-e3-side-by-side.md` §7 (dissertation). The premise's static verdict is INDETERMINATE — pre-measurement 0.5599 (real-only) / 0.4898 (synthetic-grounded) and E2-at-power 0.6088 [0.371, 0.921] all sit in/touch the 0.3–0.6 kill band; E3 (prompted fleet) landed below band, weak evidence. No feasible N resolves the static ratio (n ≈ 14,533). This document designs the **temporal/exposure decomposition**: measure the premise score *in a moving window*, identify readers whose score **moves across the band** (band-movers), and test whether that movement carries room signal. It changes nothing: read-only on all repos; code and registration changes are named (§8), not made.

## Verdict (6 lines)

1. **Hypothesis (H-BM):** the static in-band ratio is a phase-average — above band in stable strata (idiosyncrasy ≫ local drift) and below band at room steps (drift spikes) — and band-movers' crossings are *structured*: down-crossings time-lock to registered strata transitions, idiosyncratic offsets persist through them, and per-night score is room-warmth-invariant (H-reader≡room alignment arm). Anti-hypotheses: crossings are estimator noise; or score moves with room warmth x (collapse arm).
2. **Corpus:** PRIMARY = wave-2 T-nights (T1–T9, 21 readers × 3–4 nights, 73 reader-nights, 66 signal; designed attendance, 15 distinct x, T9 = null night). REPLICATION (labeled, per-wave, never pooled) = wave-1 S1–S5 (15 readers, 73 reader-nights; orig-6 span all 9 incl. S5 null). A–D-cold (v:1, replay-mediated) anchor the estimator-continuity ladder only; S6/S7 and night-H* excluded from primary (exploratory).
3. **Moving-window premise score:** within each night, slide W=12-speak windows (stride 1); per present reader R: idiosyncratic offset o_R(t) = ‖m_R(t) − b̄(t)‖ / corpus_sd (m_R = windowed mean of logged v:2 readings; b̄ = across-roster windowed mean), local drift d_R(t) = split-half displacement ‖mean(2nd half) − mean(1st half)‖ / corpus_sd; **score ρ_R(t) = o_R(t) / d_R(t)**, band states by 0.3/0.6 with hysteresis (exit ≥ 0.05 beyond edge, persist ≥ 3 windows). Population trajectory R(t) = RMS_R o_R / mean_R d_R is the headline decomposition; continuity ladder: full-night window reproduces each wave's filed spread/drift ratio within ±0.10.
4. **Band-crossing statistics (registered):** (A) timing — mean over hysteresis-clean down-crossings of 1[within 3 speaks of a registered transition], vs 10,000 circular-shift nulls per reader-night; (D) direction — fraction of signal transitions with a down-crossing in ±3 speaks vs null-night (T9/S5) rate; (P) persistence — corr across readers of pre- vs post-transition windowed offsets vs stable-phase reference; (S) exposure — within-reader regression of per-night median score on night warmth x (signal nights, ≥2 distinct x per reader), vs a roster-composition competitor, reader-clustered bootstrap B=2000, seed 20260821.
5. **Kill/void:** H-BM dies if A ≤ null 95th pct AND D ≤ 50% at α=0.05 (crossings are noise → static in-band verdict stands as phase-averaged noise; retirement confirmed). The premise dies *temporally* if P < 0.5× stable-phase reference (the step erases idiosyncrasy — readers are not instruments through steps). The alignment arm of H-reader≡room is falsified if S's x-coefficient CI excludes 0 and beats the roster competitor (score is room geometry wearing a reader's name — collapse, with explanation). VOID-by-rule: Stage-2 wave gate fails; null-night crossing rate ≥ 50% of signal-night rate (estimator noise); < 20 crossing events; continuity ladder off by > 0.10.
6. **Honesty guard (the night-H lesson, registered up front):** crossings are *near-tautological* — numerator ≈ constant (0.46–0.56 corpus-sd, three measurements) over a bimodal denominator (noise floor ~0.29, transition spikes ~0.75–0.93) ⇒ band movement is guaranteed by arithmetic. **The bare crossing rate is not evidence.** Only timing precision (A), persistence (P), and x-invariance (S) carry content. Priors: A fires 0.55, P holds 0.50, x-invariance 0.60 (wave-2 slope leaned alignment: −0.3588, CI contains 0, excludes 1).

---

## §0 Terminology (registered)

- **Premise score** — the kill-band quantity computed at reader grain: idiosyncratic baseline offset ÷ local within-reader drift, corpus-sd units, so that 0.3/0.6 apply unchanged. The population ratio filed by E2 (spread/drift) is the RMS/mean aggregate of the same two quantities; §3's continuity ladder pins the exact relationship.
- **Band state** — clear (> 0.6), in-band (0.3–0.6), kill (< 0.3). High = idiosyncrasy dominates drift (premise holds locally); low = the room's step dominates (premise fails locally).
- **Band-mover** — a reader-night whose ρ_R(t) crosses a band edge under hysteresis (within-night mover); or a reader whose per-night median score changes band across attended nights (cross-night mover).
- **Down-crossing** — a crossing downward through 0.6 or 0.3 (idiosyncrasy losing to drift); **up-crossing** the reverse.

## §1 Hypothesis, anti-hypotheses, and what each leg decides

**H-BM (primary):** the premise ratio is not a constant of the reader population but a function of room phase, and its movement is structured:

- **H-BM-t (temporal):** down-crossings time-lock to registered strata transitions; up-crossings occur in stable strata; the idiosyncratic offset survives the step (reader-specific direction, not just archetype).
- **H-BM-x (exposure):** per-night score is a reader constant — invariant to the night's warmth ladder position x and to roster composition (alignment arm of H-reader≡room). Its negation (score = f(x)) is the collapse arm.

**Anti-hypotheses (each falsifiable by a registered leg):**

1. **Noise:** crossings are window-estimator jitter — no timing structure, no direction structure. Decided by A and D (§4) plus the null-night void rule (§5).
2. **Collapse (H-reader≡room's warning arm):** the numerator is room geometry — scores move systematically with x across nights; idiosyncratic offsets converge to the room in stable phases and regenerate from archetype after steps. Decided by S and P.
3. **Identity-propagation null (E5):** offsets persist but are archetype structure (93–96% of baseline variance between-archetype), not individual. Decided by P's class-residual sensitivity (§4).

**Why this is the right next test given the filed record:** the side-by-side's structural finding is numerator agreement (0.46–0.56, three instruments) + denominator divergence (0.748 vs 3.46) — i.e., the *denominator is the frame-dependent half*, and the denominator is exactly what a moving window resolves in time (drift is episodic; spread is not). The wave-2 slope leaned alignment but the class-residual tripwire fired (knife-edge) — the exposure leg S re-tests the same hinge at per-night grain with within-reader x-variation the slope design did not use (each reader attends nights at different ladder positions). And the wave-2 ICC (0.9076 [0.7832, 0.9112]) predicts P holds if offsets are the same object ICC measured — a built-in consistency check.

## §2 Corpus selection

| tier | nights | readers | role |
|---|---|---|---|
| PRIMARY | T1, T2, T3, T4a, T4b, T5, T5c, T8 (signal) + T9 (null, S5-family) | all 21 (FIELD_NIGHTS_W2 matrix; drifter cold-entry T4a/T4b; staged T5/T5c lines are warmth content, not attendance — same convention as the wave-2 run) | 73 reader-nights, 66 signal; designed stratification (cold/mid/warm bands), ≥2 signal transitions per reader by construction; T9 = internal null |
| REPLICATION | S1, S2, S3, S4a, S4b (signal) + S5 (null) | 15 (FIELD_NIGHTS; orig-6 attend all nine incl. S5) | 73 reader-nights; labeled per-wave replication — **never pooled** with wave-2 in a primary number (E-cont convention); orig-6 give the largest within-reader x-range (0.3187–0.7589) |
| Continuity anchor | A, B, C, D, D-cold (v:1) | 7 (replay) | estimator-continuity only: the moving-window estimator at W = full night must reproduce the pre-measurement 0.5599/0.4898 arithmetic channel within ±0.10 (replay-mediated — same caveat as the filed note) |
| EXCLUDED (primary) | S6, S7 (non-monotonic, addendum-3), night-H*, A-repro, coarse-anchor | — | S6/S7 and H* exploratory only (H is pro-premise by construction); A-repro/coarse-anchor excluded per the pre-measurement note |

Guards reused verbatim before any analysis: Stage-2 wave gate (`scripts/stage2_wave_gate.py`) — logged rosters == designed attendance, corpus_sd 0.2367, per-night warmth ladder to 4 decimals — plus `assert_replay_matches_log` on a sampled set of v:2 nights. Gate failure ⇒ VOID (§5), no reading taken.

Per-wave corpus_sd: wave-2 0.2367 (re-asserted by gate); wave-1 its filed value (0.2367, E2 field corpus). Never cross-wave.

## §3 Moving-window premise measurement (exact estimator)

**Readings (input, logged facts only on primary/replication):** reading_R(t) = CENTER + g_R ⊙ (field_eff_to_reader[R](t) − CENTER), consumed from v:2 `readers` blocks exactly as `e2_instrument.logged_readings` does; g_R = dial_weights/max. Presence = roster membership (windows before a cold entrant's first speak simply lack that reader). Channel: canonical-presence logging convention (the premise-favorable, participation-deconflected channel, per the E2 asymmetry lesson); actual-presence replay = labeled sensitivity.

**Window:** W = 12 consecutive speaks (by `seq`), stride 1, halves of 6/6. Sensitivities: W ∈ {8, 16}. All nights in scope have ≥ 20 speaks (min: S5/T9 = 20 ⇒ ≥ 9 window positions; max: T4a/T5 = 46 ⇒ 35 positions).

At window position t on night N:

- m_R(t) = mean of R's readings in the window; b̄(t) = mean of m_R over readers present in the window.
- **o_R(t)** = ‖m_R(t) − b̄(t)‖ / corpus_sd — idiosyncratic offset (numerator; the reader's windowed baseline displaced from the room-population windowed mean).
- **d_R(t)** = ‖ mean(readings, 2nd half) − mean(readings, 1st half) ‖ / corpus_sd — split-half local drift (denominator; label-free, responds to any local trend; noise floor ≈ the 0.291 no-flip null analog in stable strata, spikes ≈ 0.75–0.93 at transitions per filed per-transition means).
- **ρ_R(t) = o_R(t) / d_R(t)** — per-reader windowed premise score.
- **R(t)** = RMS_R o_R(t) / mean_R d_R(t) — population windowed ratio (headline trajectory).

**Hysteresis (anti-jitter, fleet deadband doctrine `exit = enter × hysteresis` analog):** a band-state change is *counted* only when the score moves ≥ 0.05 beyond the edge and holds the new state ≥ 3 consecutive positions. All crossing statistics consume counted crossings only.

**Continuity ladder (estimator gate, mandatory before any leg runs):**
1. W = full night, halves = registered strata split: R(t) must reproduce each wave's filed ratio channel within ±0.10 (wave-1: 0.6088 E-seg / 0.5599 E-cont arithmetic; wave-2: recompute, must land in-band, matching the wave-2 gate's own spread/drift).
2. On the v:1 anchor corpus, the same estimator must reproduce 0.5599 (real-only) / 0.4898 (grounded) within ±0.10.
3. Failure ⇒ VOID (estimator does not measure the filed object).

**Class-residual variant (E5 discipline):** o_R computed against the window's archetype-mean (labels from `e2-personas.json`) instead of the grand mean — the within-archetype idiosyncrasy score; labeled sensitivity on every leg (the primary is unresidualized, matching the slope run's convention).

## §4 Band-crossing statistics (registered, four legs)

**Leg A — timing (does the movement time-lock to the room?).** Statistic: A = mean over all counted down-crossings (pooled over reader-nights, wave-2 primary) of 1[|crossing position − nearest registered transition boundary| ≤ 3 speaks]. Null: per reader-night, circular shift of the ρ_R(t) series by a uniform offset (preserves autocorrelation and margin distribution), 10,000 draws, seed 20260821; p = P(A_null ≥ A_obs). Up-crossings tested against *mid-stable-stratum* anchors (transition + W/2) as the mirror statistic (labeled secondary).

**Leg D — direction/transition coverage (is a step always a down-cross somewhere?).** Statistic: D = fraction of registered signal transitions (night-level, wave-2: 1–3 per night) with ≥ 1 counted reader down-crossing within ±3 speaks, vs the null-night pseudo-transition rate (T9, S5 at their midpoints). Register: D_signal − D_null with exact binomial CI; D_signal ≤ 50% ⇒ H-BM-t fails on direction.

**Leg P — offset persistence (does idiosyncrasy survive the step? — the premise's content).** For each signal transition: correlate (across the night's roster) pre-transition windowed offsets o_R(t_pre) with post-transition o_R(t_post) — cosine over the 7-dim offset vectors, readers as observations, restricted to the ICC-reliable subspace (mood/volume/earnestness/presence; panic excluded by the two-line schema rule). Reference: the same correlation across two stable-phase windows equidistant within a stratum (persistence-at-rest). Register: **P_trans ≥ 0.5 × P_rest ⇒ idiosyncrasy survives the step** (threshold pre-committed; the 0.5 factor absorbs one step of drift dilution). Class-residual sensitivity: persistence of residual offsets (E5 null says residuals may not persist — if population-P holds but residual-P fails, the surviving structure is archetype, and the finding is booked as identity propagation, not premise support).

**Leg S — exposure (cross-night band-movers; the H-reader≡room hinge at per-night grain).** Per reader per *signal* night: score_R,N = median over that night's windows of ρ_R(t). Regress (all reader-night cells, wave-2 primary): score ~ x_N + reader fixed effect, where x_N = the night's filed warmth ladder value (roster-invariant, known a priori: T2 .3187, T4a .4465, T5/T5c .6293, T4b .6319, T1/T3 .6551, T8 .7409). Inference: reader-clustered bootstrap, B = 2000. Competitor model: score ~ roster-composition covariates (night roster size; roster mean archetype-baseline warmth) — because b̄(t) is roster-dependent and the design must separate "room moved the reader" from "roster moved the mean." Decision: x-coefficient CI excluding 0 AND beating the competitor (nested permutation, 10,000) ⇒ score is exposure-dependent ⇒ collapse arm; CI containing 0 with the competitor not beating it ⇒ x-invariant reader constant ⇒ alignment arm support. Null nights (T9/S5) are excluded from S (no signal transitions — their scores are noise-saturation references, reported, not regressed). Wave-1 replication: identical procedure on S-nights; orig-6 (9 nights each) are the sharpest cells.

**Population trajectory (headline, descriptive):** R(t) aligned at transition boundaries, pooled per wave, with the band drawn — the static 0.6088/0.5599 decomposed into stable-phase (predict: clear-side) and transition-phase (predict: kill-side) components. Descriptive only; no branch is read off it (the §0 tautology guard).

## §5 Kill criteria and void-by-rule

**H-BM killed (the movement carries no signal):**
- A ≤ circular-shift null 95th percentile (p > 0.05) **AND** D_signal ≤ 50% or D_signal − D_null CI contains 0. Booked: the static in-band verdict is a phase-average of *noise*; the premise stays retired-leaning-false with a sharpened sentence ("not even temporally structured"); no further temporal decomposition of the ratio is warranted.
- Either clause alone ⇒ INDETERMINATE leg, both clauses reported (two-branch discipline).

**The premise killed temporally (stronger than E2's shrug — a *mechanism* kill):**
- P_trans < 0.5 × P_rest with the gap CI excluding overlap ⇒ the room's step erases individual idiosyncrasy; readers are not instruments through steps; nurse-as-index usable only in stable phases — a boundary condition with a mechanism, promotable in Chapter 6 language.

**The alignment arm of H-reader≡room falsified:**
- S's x-coefficient CI excludes 0 and beats the roster competitor ⇒ per-night score is room-warmth geometry (collapse arm) — the strongest possible cross-grain confirmation of the slope warning; the leaning-alignment of wave-2 was the artifact. Booked as the premise's death with an explanation, exactly as side-by-side §7.2 anticipated.

**VOID-by-rule (no branch read; fix or abandon, never re-read silently):**
1. Stage-2 wave gate failure (roster/log mismatch, corpus_sd, ladder drift).
2. Null-night crossing rate ≥ 50% of signal-night rate — the window statistic cannot separate room steps from noise at this W; the run reports the estimator finding, not a premise verdict.
3. < 20 counted down-crossings across the primary corpus — nothing to test.
4. Continuity ladder (§3) off by > 0.10 on any wave — estimator measures the wrong object.
5. Bootstrap effective draws < 1,500 (small-n degradation; report and void).

**Explicitly NOT a kill:** S's x-invariance + P holding + A firing together = the pro-premise composite ("instrument except at steps; kill band is a phase-averaging statement"). This upgrades the premise from shrug to *phase-conditional claim* — but the upgrade is capped: it does not reopen Branch A/B of the cross-instrument tree, which required a static clear (side-by-side §4). It is booked as a boundary condition, the same size as Branch B would have been.

## §6 What would falsify the thesis (summary table)

| outcome | kills / falsifies | sentence it licenses |
|---|---|---|
| A fires, P holds, S x-invariant (wave-2, replicated wave-1) | nothing; supports premise (capped) | "readers are instruments except at steps; the in-band ratio was an average over phases" |
| A fails AND D fails | H-BM (temporal signal) | "the ratio's movement is noise; retirement stands, sharpened" |
| P_trans ≪ P_rest | the premise (mechanism kill) | "steps erase idiosyncrasy; nurse-as-index is stable-phase-only" |
| S: x-coef CI ∌ 0, beats roster | H-reader≡room alignment arm; premise via collapse | "the idiosyncrasy was room geometry wearing a reader's name" |
| P population holds, P residual fails | E5 identity-propagation null extended temporally | "what persists through steps is archetype, not individual" |
| null-night crossings ≈ signal-night | the estimator, not the premise | "the field cannot currently measure the premise's dynamics" |

## §7 Inference and power (the math, shown)

- **Events:** wave-2 signal nights carry 1–3 registered transitions each (T1/T2/T3/T5/T5c/T8: 1; T4a/T4b: 2) → ≈ 85 reader-night transition events over 66 signal reader-nights; if even half produce hysteresis-clean down-crossings, ≥ 40 events. One-proportion test of A at 0.60 observed vs 0.25 null-shift expectation: n = 40 ⇒ power > 0.9 at α = 0.05. Below 20 events ⇒ VOID by rule (§5.3).
- **P:** roster sizes 7–10 ⇒ per-transition correlation over 7–10 readers; pooled across ≈ 85 events via Fisher z (readers-as-observations within night; nights pooled by z, never across waves). Detectable gap: P_rest − P_trans ≥ 0.25 at the pooled level.
- **S:** 66 wave-2 signal reader-night cells; within-reader x-range 0.28–0.44 (e.g., writer: .3187→.6293; warm-band: .6319→.7409); reader fixed effects absorb the 93–96% between-archetype variance (E5), so the residual x-test is the same guard the class-residual tripwire gave the slope run — but *pre-registered* here, not post-hoc.
- **Multiplicity:** four legs, one registered primary each; A is the H-BM primary; S is the thesis-hinge primary; D and P are registered with thresholds above. No other comparisons are read (everything else is labeled sensitivity: W ∈ {8,16}, actual-presence channel, class-residual, up-crossing mirror, null-night scores).

## §8 Implementation route (named, not made)

1. `scripts/premise_band_movers.py` (new, numpy-only, CPU, read-only against `data/nights/`; seeds 20260821; imports `Night`, `logged_readings`, `corpus_sd`, `FIELD_NIGHTS`, `FIELD_NIGHTS_W2`, `archetype_labels` from the unmodified `scripts/e2_instrument.py`; writes `data/premise-band-movers/results.json` + per-wave JSONs). Sections mirroring §3–§5.
2. No changes to `e2_instrument.py`, `slope_regression.py`, `e2_nights.py`, or any filed artifact; the Stage-2 wave gate is *invoked*, not edited.
3. Registration: dated addendum appended to `research/topic.md` (dissertation repo; annotate-only, nothing above altered) registering H-BM, the four statistics, thresholds, void rules, and priors — committed before the first analysis run (doctrine: registration before code-before-measurement ordering already satisfied by this design).
4. Reproduce sequence for whoever builds it: wave gate → continuity ladder → legs A/D/P/S → wave-1 replication → sensitivities. Runtime < 2 min CPU.

## §9 Failure modes and guards

| # | failure mode | guard |
|---|---|---|
| 1 | **Tautology misread as signal** (numerator constant × bimodal denominator ⇒ crossings guaranteed) | §0/§6 registered up front: crossing *rate* is never evidence; only A (timing vs circular-shift null), P (persistence), S (x-invariance) carry content |
| 2 | **Window-noise crossings** | hysteresis (0.05 / 3 positions) + null-night rate void rule (§5.2) + W-sensitivity |
| 3 | **Roster-composition confound in b̄(t)** (wave-2 rosters deliberately vary) | S's competitor model; per-window b̄ over present readers only; wave-1 orig-6 (constant roster) as the deconfounded replication |
| 4 | **Archetype structure masquerading as idiosyncrasy** (E5: 93–96%) | class-residual sensitivity on P and S; population-vs-residual divergence ⇒ booked as identity propagation, never as premise support |
| 5 | **Channel/treatment laundering** (canonical vs actual presence moved E2's number 0.6088→0.3815) | primary = the premise-favorable logged channel, fixed a priori; actual-presence = labeled sensitivity; no channel chosen after seeing legs |
| 6 | **Attendance/log drift** | Stage-2 wave gate re-run verbatim; `assert_replay_matches_log` sampled |
| 7 | **Cross-wave pooling** (waves have different rosters/attendance ⇒ different guard numbers) | per-wave analysis throughout; wave-1 labeled REPLICATION; no pooled primary number exists in this design |
| 8 | **Small-n bootstrap degradation** | effective-draws report; void rule §5.5 |
| 9 | **Post-hoc threshold drift** | all thresholds (3 speaks, 0.05 hysteresis, 3 positions, 0.5×P_rest, 50% D, ±0.10 ladder) are in this document and the topic.md addendum before any run; deviations require a dated deviation note, as the wave-2 run modeled |

## Provenance

- Grounding: elephant `RESEARCH-NOTE-PREMISE-MEASUREMENT-2026-08-19.md` (kill band, 0.5599/0.4898, per-reader displacement model), `SLOPE-REGRESSION-2026-08-20.md` (registered ratio machinery, committee-open list), `STAGE2-CORPUS-DESIGN/RUN-2026-08-20.md` (wave-2 attendance, guards, gate), `scripts/e2_instrument.py` (estimator semantics, KILL_LO/HI = 0.3/0.6, FIELD_NIGHTS/W2), `data/nights/night-{S*,T*}.jsonl` (v:2 per-reader facts; verified today: 20–46 speaks/night, rosters match the matrices); dissertation `e2-e3-side-by-side.md` (Branch C, numerator/denominator divergence, "decisive next"), `research/topic.md` v3 + 2026-08-20 addendum, `chapter-7-future-work.md` §7.4–7.5 (the original "premise-band movers" ranking).
- No files outside this document were written; no commits; repos untouched (read-only verified by inspection only).
