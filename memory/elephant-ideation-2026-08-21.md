# Elephant Ideation — The Next Move

**Filed: 2026-08-21 (ideation only).** Strictly read-only on all repos; nothing here is built, run, or committed. Inputs: `elephant-next-move-research-2026-08-21.md` (state of evidence + two paths), `E2E3-premise-band-movers-design-2026-08-21.md` (registered design), `data/slope/premise-band-movers-results.json` (the VOID run), the advisor note (Path B = endgame, Path A = vanguard), and `scripts/premise_band_movers.py` (the estimator as-implemented).

**Where we stand:** VOID by rule §5.3 (17/20 counted down-crossings). A fires hard (0.647, p=0.0013; W=8: 0.917). P is a landslide (0.994 vs 0.9935, threshold 0.497). D is borderline (0.40, null 0/7). S is the hinge (wave-2 x-invariant, wave-1 indeterminate). The void is a coverage problem, not a content problem.

---

## 1. Path A — More Reader-Nights Without Looking Like Threshold-Shopping

The structural problem: crossing yield was 17/85 transition-events ≈ 20%. The mechanism is now visible in the results: the numerator o is pinned at 0.46–0.56 corpus-sd (three instruments agree), so a down-crossing through 0.6 with the 0.05 hysteresis margin requires d ≳ 0.55/0.85 ≈ 0.65 sustained for 3 windows. Hard SEG warm→cynical steps spike d to 0.75–0.93 — those cross. Mild entry steps (T5/T5c, D/D-cold at speak 24) don't reach that denominator — those don't. **Crossings are manufactured by transition hardness × reader offset size.** That sentence is the design handle for wave-3.

### 1.1 The anti-shopping doctrine: change the *design*, not the *ruler*

The clean Path A keeps every registered constant untouched (W=12, 0.05 margin, 3-window hold, ≥20 floor) and changes only what was always a design parameter: **the attendance matrix and the night mix**. The rule we pre-commit:

> **Wave-3 rule (file before generation):** same 9 frozen families, same estimator, same thresholds, same void rules. New attendance matrix only, designed against *filed* wave-2 quantities (transition d-spikes, reader offset magnitudes) to maximize expected crossing yield. Wave-3 is a labeled replication wave — never pooled with wave-1/2. Falsifier: if a yield-maximized wave-3 still produces < 20 counted down-crossings, the temporal decomposition is declared underpowered-in-principle for this engine, Path A closes permanently, and the verdict moves to Path B.

That falsifier is what separates this from shopping: we name, in advance, the outcome that *kills the path*, not just the outcome that saves it. The wave-2 legs (A, P, D, S values) stay booked exactly as filed — a below-floor sensitivity reading, never retro-promoted.

### 1.2 If the hysteresis must move: re-register the rule for changing rules

If 1.1's power math says attendance alone can't reach 20 (see 1.3), then a re-registration (3→2 window hold, or W=8 dual-primary) is legitimate *only* under a meta-rule filed before any wave-3 measurement:

1. The new constant must be justified by a filed artifact (e.g., "W=8 fires A at 0.917 in both waves" is filed), never by wave-3 output.
2. The re-registered variant runs as a **parallel registered test**, not a replacement — the W=12/3-hold analysis is still run and reported, whatever it says.
3. The floor itself is re-derived from a power computation on filed effect sizes (A's null mean 0.246 vs observed 0.647), with the derivation in the addendum. If the honest power calc says 14 events suffice for the A-leg at α=0.05, the floor becomes 14 *for the re-registered test* and the 20-floor test is marked abandoned-with-reason. Two tests, two registrations, no silent substitution.
4. The deviation is disclosed in the same sentence as any result that uses it — the night-H lesson, applied to ourselves.

The thing to refuse absolutely: picking the constant *after* seeing wave-3's event count. One look at the number and every subsequent choice is contaminated.

### 1.3 Wave-3 night design (the concrete part)

The yield equation: crossings ≈ (reader-nights on hard-transition nights) × P(reader offset small enough that o/d dips below 0.55 for 3 windows). Three levers:

- **Attendance matrix as treatment assignment.** Rank the 21 (or a wave-3 roster) readers by filed offset magnitude; assign the small-offset readers to the hard-SEG nights (T1/T3/T8-family warm→cynical at speak 20). This is exactly the Stage-2 attendance-design methodology — the matrix was always a design parameter, and designing it against filed offsets is no more rigging than a factorial design choosing cell sizes. **Registered guard against the rigging reading:** assignments must be computed by a deterministic, filed rule (e.g., "lowest-o readers to highest-d-spike nights, greedy, tie-broken alphabetically"), not hand-tuned per reader-night.
- **Double-transition nights.** T4a/T4b carry 2 signal transitions and produced the richest event structure (and the only mid-night transitions at speaks 12/28). A wave-3 night mix weighted toward 2-transition families roughly doubles transition-events per reader-night. Target: ~60 signal reader-nights × 2 transitions × improved yield (30–40% with offset-matched attendance) ⇒ 35–45 expected crossings. Comfortable margin over 20.
- **One registered null night** (T9/S5 pattern), unchanged — §5.2 must remain satisfiable, and wave-3's null rate of 0/7 reader-nights in wave-2 is the estimator's cleanest credential.

Also register one **D-repair night**: a night whose entry step is engineered harder than T5/T5c's — if the frozen families don't contain one, that's the honest finding ("the family set's entry steps are sub-threshold for this estimator"), booked as a boundary condition on D, not patched by inventing a new family mid-stream. If a new family *is* wanted, it enters as wave-3-only content with its own reproduction checks — but the conservative play is families-frozen, attendance-free.

**Cost:** ~5 min generation + ~5 min analysis. **Single risk:** the D leg — if only hard SEG transitions ever cross, D is capped near the fraction of transitions that are hard, and no attendance matrix fixes a numerator measured per-transition. Accept this up front: register D's ceiling explicitly ("D > 50% requires entry-step coverage; if the family set lacks hard entry steps, D's failure is booked as a coverage boundary, not an H-BM-t failure"). That pre-statement converts wave-2's most ambiguous leg from a liability into a designed test of the coverage mechanism.

---

## 2. Path B — The Length-Matched Generation Corpus (Endgame)

The point of Path B is not a bigger N; it's **known ground truth**. The field corpus can never tell us whether reader baselines are instruments or room-warmth proxies because we can't see the generative process. In a generation corpus we *set* α (0 = instrument, 1 = collapse, noise = no structure) and check whether the registered statistics name the right branch. The design requirement that makes this evidence rather than theater: **the analysis must be blind, and the generation must not share the estimator's skeleton.**

### 2.1 Design angles

- **Minimal sufficient corpus.** Don't match all 36 field night-logs. One wave-2-shaped unit (9 nights: 8 signal + 1 null, 21 synthetic readers, 3–4 nights each, 20–46 speaks/night, warmth ladder spanning 0.319–0.759, Sxx ≥ 0.19) per branch condition. Conditions: α ∈ {0.0, 0.3, 0.7, 1.0} + pure-noise = 5 corpora, 45 night-logs. Add 2 undisclosed conditions (see 2.2, mechanism 3). Registered prediction per condition (spec §7): α=0 → slope CI contains 0, A fires, P holds; α=1 → slope CI contains 1, S falsifies alignment; noise → void or legs fail. The α=0.3/0.7 intermediates are the actual discrimination measurement — recovering *endpoints* is easy; locating the crossover is the instrument's resolving power.
- **Generate at the text level, never at the reading level.** Synthetic scripts through the elephant engine (TapNightSession, SEG banks, vmf) producing field_eff readings — the same nonlinear transform the field data passed through. The estimator consumes `readers` blocks, identical format to `data/nights/night-*.jsonl`. Ground truth lives in the generation parameters, which the analysis pipeline never imports.
- **Length-matching as a registered distributional check** (KS on speak counts, roster sizes, transition counts, plus speak-level autocorrelation matching — the last one is easy to forget and is exactly the statistic a windowed estimator feeds on).

### 2.2 Contamination control — the hard problem, five mechanisms

The failure mode: if the generator writes "reader baseline = room mean + fixed offset vector," then the estimator's o_R *is the generation parameter* and recovery is tautological. The calibration would "pass" because the answer was engraved on the apparatus. Five distinct defenses, in increasing order of strength — the design should stack at least three:

1. **Text-level indirection (the baseline defense).** The generator specifies *personas and scripts*; reader offsets emerge from the engine's vmf/SEG dynamics. The generator's α controls persona parameters (e.g., how strongly a persona's vibe_start couples to room warmth), never coordinates in reading-space. Contamination channel remaining: the engine itself might make emergent offsets trivially recoverable. Necessary, not sufficient.

2. **Generator ensemble (mechanism diversity).** Three independent reader-baseline generators with *different internal mechanics*: (a) the elephant engine with persona coupling α; (b) a Markov persona process — each reader's reading is a state machine over moods with transition matrices that either ignore room warmth (α=0) or track it (α=1); (c) a mixture model — reader readings drawn from archetype-conditional distributions whose means are warmth-coupled to degree α. Same branch labels, same output schema, same analysis. **Recovery must hold across all three generators.** A result that survives generator-swapping is a property of the estimator; a result that holds only under (a) is a property of the elephant. This directly answers "did we measure the apparatus or the engine?"

3. **Adversarial blind split with canaries and open-set conditions.** Agent G designs generation; agent A runs the analysis with no access to generation code or parameters — only the JSONL corpora and a condition manifest with *shuffled labels*. G additionally injects: (i) **a contamination canary** — one corpus deliberately built in the tautological way (baseline = roster-mean deviation), which A's pipeline should flag as *suspiciously perfect* (recovery too exact, residuals too clean) — if the canary is indistinguishable from honest corpora, the calibration can't detect contamination and the whole exercise voids; (ii) **two open-set conditions** whose branch is not in the registered {0, 0.3, 0.7, 1.0, noise} set (say α=0.5 and a time-varying α(t) that starts instrumental and collapses mid-corpus) — A must estimate α, not just classify. Open-set performance is the real discrimination certificate; closed-set accuracy can be gamed by priors.

4. **Independence audit statistic (the self-test).** For each corpus, compute a registered *contamination diagnostic*: refit the analysis with a modified estimator (e.g., o measured against a leave-one-out roster mean, or against the archetype mean — the class-residual variant already exists) and check that recovery is stable under estimator perturbation. Tautological recovery is *fragile* to estimator changes (it keys on the exact reference the generator used); genuine structure survives reference-frame swaps. Also: shuffle reader labels across nights *within the generation* for one decoy corpus — if P "holds" on the shuffled corpus, P is measuring arithmetic, not identity. (The field corpus can't run this decoy; the generation corpus can. That's new information Path A can never produce.)

5. **Parameter-veil randomization (distribution-level honesty).** G draws the generation hyperparameters (noise scales, SEG bank strengths, persona variances, drift magnitudes) from a distribution, logs the draw under seal, and gives A only the readings. Prevents G from hand-tuning to the estimator's sweet spots (e.g., placing every transition spike at 0.75–0.93 where the estimator is most sensitive). The sealed log is opened only at scoring time and filed with the results — the generation-side analog of registration-before-measurement.

**Stacking recommendation:** 1 + 2 + 3 at minimum; 4 is nearly free (reuses the class-residual machinery); 5 is the strongest and the most expensive. The α(t) time-varying condition in mechanism 3 is a bonus worth its own sentence: it directly tests the premise's actual claim — that a reader can *become* a room — which no static-α condition touches.

---

## 3. The Top Open Question: Does a Synthetic Calibration Validate the Field VOID?

### The case for "the void stands regardless"

The VOID is a statement about a *dataset*, not an instrument: on 2026-08-21, the wave-2 primary produced 17 countable events against a registered floor of 20. No synthetic corpus adds an 18th event to that file. Registration discipline is the thesis's actual contribution (claim 6: reproducibility makes cheap adversarial audits possible) — and the discipline's whole value is that registered outcomes are not negotiable after the fact. If a clean calibration could launder a void into a verdict, every null result in the literature would come with a calibration appendix arguing the instrument was fine. The void also carries real information the calibration can't: the field *yield* was 20%, meaning the field's transition hardness distribution is mostly sub-threshold for this estimator — a fact about the field, not the apparatus. Verdicts attach to measurements; calibrations attach to instruments. Different objects.

### The case for "calibration recontextualizes the void"

§5.3 is an *instrument-sufficiency gate*, not a premise verdict — it says "below 20 events we don't trust ourselves to read the legs." But that trust boundary was set by a power analysis that assumed a weaker effect than what was filed: A fired at 0.647 vs null-mean 0.246 with p=0.0013 *on 17 events*; the design's own §7 math had power > 0.9 at n=40 for a *smaller* gap. If a blind calibration shows the estimator is unbiased and branch-recovering at synthetic event counts of 15–20, then the floor was conservative, the 17 readings were above the *true* sufficiency threshold, and the void is a registered-rule artifact — honest, but artifact. The calibration also distinguishes the two worlds the void leaves open: "instrument unsound, field unreadable" vs "instrument sound, field underpowered." Those worlds imply completely different next steps, and only Path B can tell them apart. A thesis that reports "VOID" without resolving which world it's in is leaving its own central question ambiguous.

### Position

**The field void stands as a verdict — permanently — and the calibration's job is not to overturn it but to assign it a meaning.** Concretely:

- Wave-2's 17 events never become a verdict. The discipline is the contribution; the day we let a calibration promote a below-floor reading into a branch declaration, the registration layer becomes decorative and the thesis loses its load-bearing claim.
- But the calibration determines what the void *costs*. If Path B recovers branches blind at event counts ≤ 17, the void is booked as "known-good instrument, underpowered field; wave-3 is a power fix, not a validity fix" — and the wave-2 legs stand in the record as labeled below-floor sensitivities that a reader may weigh accordingly. If Path B fails to recover (or only recovers on the elephant-generated condition), the void deepens to "instrument cannot discriminate instrument from collapse even with ground truth available" — the research doc's thesis-killer — and the field corpus's indeterminacy is no longer a coverage problem at all; it's the finding.
- So: **validate the verdict, no; explain the void, yes — and explanation is the thing the dissertation actually needs.** The field void and the synthetic calibration are answers to different questions, and the thesis is only in trouble if it confuses them.

---

## 4. Wilder Third Paths the Research Didn't Consider

### 4.1 The prediction path — kill the ratio, keep the registration

The band machinery is where all the pain lives (floors, hysteresis, window referents, the §0 tautology guard). Replace the question "does ρ cross 0.6 at transitions" with a **registered out-of-sample forecast**: fit each reader's baseline on wave-1+2 (ICC = 0.907 says these are stable constants), then *before* wave-3 generation, file per-reader predicted offset vectors ô_R for each wave-3 night, under two models — (M1) instrument: ô_R = the reader's fitted constant, regardless of night; (M2) collapse: ô_R = f(night warmth, roster). Score with a proper scoring rule (log-loss on direction-of-deviation, or MSE in the reliable subspace) against the logged wave-3 readings. No band, no floor, no crossings — just "which model of the reader predicts better, filed before measurement." The band becomes a descriptive visualization, not an inferential gate. This is the cheapest path of all: it reuses everything, needs no new statistics, and its verdict (M1 vs M2) *is* the instrument-vs-collapse question in betting form. Weakness: it tests predictiveness, not mechanism — a reader can be predictable for the wrong reasons (archetype). Pair with the class-residual variant: M1-residual vs M2-residual.

### 4.2 The adversarial-reader path — turn "P holds" from observation into theorem-or-finding

P held at 0.994 — suspiciously perfectly. Maybe idiosyncrasy is robust; maybe the engine simply cannot express a reader whose offset doesn't survive a step, in which case P holding is a theorem of the elephant and carries no empirical content about readers. Test: **commission an adversarial persona** — a design exercise whose explicit goal is to break P (maximize step-driven drift while holding pre-step offset; e.g., a persona whose vibe couples to stratum identity rather than warmth). If the engine + persona-design space *cannot* produce a P-breaking reader after a genuine adversarial effort, book it: "P is engine-necessary, not reader-true; demote P from evidence to consistency check." If it *can*, run the night, and P's survival on the honest roster becomes meaningful against a demonstrated alternative. This is the night-H honesty guard applied to a leg instead of a night: every leg that never fails needs a demonstrated failure mode to be evidence.

### 4.3 The cross-species path — replicate the structure, not the numbers

The naming doctrine already reserves "the next major species earns a new name." Make the next species do epistemic work: implement the *minimal* room engine that still produces strata, warmth, and reader readings (a few hundred lines, different dynamics — not vmf, not SEG), run the same registered four legs on it. If A fires and P holds there too, the temporal structure is a property of the *measurement framework applied to stratified rooms*, not of elephant's quirks — the strongest possible answer to "is this just the elephant's engine talking." If it doesn't replicate, the elephant-specificity is itself the finding (and sharpens what the dissertation may claim). This is generator-ensemble contamination control (mechanism 2) promoted to the field's primary evidence.

### 4.4 The mid-night reader-swap intervention

All current evidence is observational. One designed intervention night: mid-night, at a registered speak, swap one reader for a persona with a *different* fixed offset, same archetype. Registered predictions: P breaks at the swap and nowhere else; A ignores it (it's not a strata transition); the swapped-out reader's offset reappears attached to the new name if the offset is archetype (E5 null) and does not if it's individual. One night, three legs get an interventional anchor. Cheap, and it converts P from correlational persistence to something closer to a causal claim about identity.

---

## Summary (5 lines)

1. **Path A is viable without shopping:** keep every registered constant, change only the attendance matrix via a filed deterministic rule (small-offset readers → hard-SEG nights, double-transition families); the anti-shopping device is a named falsifier — if yield-maximized wave-3 still misses 20 events, Path A closes permanently.
2. **Path B's contamination problem has a concrete answer:** generate at text level, across ≥3 independent generator mechanisms, under an adversarial blind split with a contamination canary and open-set α conditions (including time-varying α(t)); tautological recovery is fragile to estimator/reference-frame perturbation — use that as the audit statistic.
3. **The field void stands, always:** calibration cannot promote 17 events into a verdict without destroying the registration layer that is the thesis's contribution — but calibration assigns the void its meaning ("sound instrument, underpowered field" vs "instrument cannot discriminate"), which is the resolution the dissertation actually needs.
4. **Boldest cheap move: the prediction path** — registered pre-wave-3 forecasts of per-reader offsets under instrument vs collapse models, scored out-of-sample; no band, no floor, no crossings, and the instrument-vs-collapse question answered in betting form.
5. **Boldest true move: adversarial-reader + cross-species** — prove P *can* fail (or book it as an engine theorem), and replicate the four legs on a non-elephant engine, converting "the elephant says so" into "the framework says so."

*No files modified beyond this document; no commits; no runs. Ideation only.*
