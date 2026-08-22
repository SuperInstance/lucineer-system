# Truthfulness Audit — elephant/JEPA work (claim chain, end-to-end)

**Filed 2026-08-21. Read-only.** Auditor: subagent (deepseek-v4-pro), tasked by the
Captain's 11:11 directive to audit novelty/truthfulness/impact/applications. This doc is
the *truthfulness* slice. Scope: the foundation docs in `memory/`, the elephant repo's
claim docs + JSON artifacts, and the dissertation claim inventory. Nothing written to any
repo; this is one new memory file.

**Method:** read every headline claim, then check it against the filed JSON artifacts and
the adversarial team docs (red-team, geometric, algebraic, ZeroClaw keeper). Where a claim
is a *number*, I reproduced it from `data/slope/*.json`. Where a claim is *prose about a
number*, I checked the prose against the same JSON.

---

## 1. Verdict per claim (file:line)

| # | Headline claim | Where filed | Verdict | Notes |
|---|---|---|---|---|
| 1 | **Premise retired, leaning false** | `zeroclaw-dissertation/research/topic.md:37,52` | **HONEST** | E3 R=0.140 [0.111,0.163] below band; E2 ratio 0.6088 touches band; "retired, leaning false — *not proven false*" is the correct epistemic register. No inflation. |
| 2 | **Band VOID by rule (17<20)** | `PREMISE-BAND-MOVERS-RUN-2026-08-21.md:1` + `data/slope/premise-band-movers-results.json` `verdict.void=true` | **HONEST** | Void declared *first*, in verdict line 1, before any leg. JSON confirms 17 (w2) / 19 (w1). The void-reason is exact. |
| 3 | **P holds 0.994** | `...RUN-2026-08-21.md:26` + JSON `P.P_trans=0.9940217, P_rest=0.9935313` | **ANNOTATED-OK, but the word "decisively" OVERCLAIMS** | The *number* is true to 6 decimals. The *adjective* "decisively" (line 26) is wrong in a specific, findable way: the red-team's q-rule shows q_trans≈q_rest≈0.132, i.e. the step is a rigid translation on the exact 4-dial subspace P measures, so P is *saturated/uninformative*, not "decisive." The kill branch (trans < 0.5×rest) can never fire (CI gap ~0.5 vs width 0.005). "Holds trivially" ≠ "holds decisively." |
| 4 | **A fires p=0.0013** | `...RUN-2026-08-21.md:21` + JSON `A=0.6470588, p=0.0013` | **HONEST number; ANNOTATED-OK framing** | p-value exact. But it is *carried* with full branch language ("fires") inside a VOIDed run, and the referent that makes it fire (window-center) was chosen *after* seeing the start-referent result give 0.0 (see §5 below). The number is honest; the confidence it is stated with is not fully earned. |
| 5 | **ICC 0.7714 [0.667, 0.810]** | `topic.md:37` | **HONEST (wave-1); incomplete** | Wave-1 filed number is correct. Wave-2 re-measured **0.9076 [0.7832, 0.9112]** (`slope-regression-w2-results.json`). Both are filed; the headline keeps only the lower wave-1 number while the geometric doc cites "0.77–0.91." Not misleading, but the *stronger* number (0.9076) exists and is rarely cited forward. |
| 6 | **imbalance ≡ d_mu (1e-12)** | `memory/quilt-synergy-map-2026-08-21.md:16`; `memory/collective-unconscious-synergy-2026-08-20.md:30` | **MISLEADING (near-tautology + internally contradictory filing)** | `imbalance = ‖after − before‖` and elephant `d_mu = ‖μ̂_B − μ̂_A‖` are *the same norm by definition*. "Proven to 1e-12" is proving two float computations of one norm agree to float precision — a definitional agreement dressed as a deep identity. Worse: `collective-unconscious-synergy-2026-08-20.md:30` headers it "documented, **unproven in code yet**" then asserts "prove (to 1e-12, numpy)" in the same line. The claim is also cross-repo (quilt-side `field-edge-ledger-bridge.md`), not an elephant finding. |
| 7 | **277 tests** | `README.md:422-425`; `pyproject.toml:20` | **ANNOTATED-OK, with two gaps** | Count is real: 277 total (276 pass + 1 flaky), 25 files. BUT (a) the E2/E3 pipeline (`premise_band_movers.py`, `e2_instrument.py`, `night_windows`, `leg_P/A/D/S`) has **zero** tests — the headline A/P/D/S numbers are protected by nothing automated; (b) I found **1 flaky test** (`tests/test_roomd.py::test_ring_rearms_on_fall`) that passes in isolation and intermittently fails in the full suite (millisecond-timestamp collision on the ring file name). "277 pass in 12s" (red-team) was a lucky run; under a faster run it is "276 passed, 1 failed." The *count* is honest; "all pass" is not robust. |
| 8 | **Personality confound cos(W,v*)=0.978** | `memory/math-foundation-geometric-2026-08-21.md:§3.2`; synthesis `:§Settled` | **HONEST, and honestly caveated** | The geometric doc itself insists on the *precise* form: a random direction already has median between-reader share 0.990, so the *non-generic* fact is the axis alignment (0.978), not the variance share (99.5%). The caveat is filed, not hidden. |
| 9 | **Confound ruling = ANNOTATE-not-kill** | `memory/math-foundation-dissertation-2026-08-21.md:§2` | **DEFENSIBLE, not under-stated** | ZeroClaw's ruling is grounded in three things that already exist: the confound is *named* (Ch 4.3), *half-measured* (E5 class-residual 0.1342), and *scheduled* (slope regression Ch 6.3). It does not under-state the damage to warmth claims because warmth claims were already retired/voided before the confound landed — there is no live warmth claim for it to kill. The two required guards (collider sensitivity, common-shift P guard) are the right sharpening. |
| 10 | **E2/E3 legs "indicative" after VOID** | `...RUN-2026-08-21.md:2` | **HONEST structure, leaning overclaim in verbs** | The *structure* is honest: "never pooled," "no branch read off it," "nothing in §3 is declared," void caps the reading. But the *verbs* are committed ("A fires," "P holds decisively"), and priors are updated (0.55→0.571, etc.) which is a soft Bayesian claim that evidence moved the needle inside a voided run. §6's concrete route to "SURVIVED (capped)" reads as a near-promise. This is humility on the wrapper, confidence in the body. |

---

## 2. The three biggest truthfulness risks (ranked)

**Risk 1 — The descriptive drift-spike overclaim (the one clear numeric inflation).**
`PREMISE-BAND-MOVERS-RUN-2026-08-21.md:35` (verdict §3) and `:177` (§6) claim the
transition drift spike is "**d ≈ 0.6–0.9 corpus-sd vs stable ≈ 0.15–0.3**." The run's
**own filed JSON** says the opposite: `mean_d_by_phase` = **transition 0.3627 vs stable
0.3167** (wave-2 canonical) — a 1.27× contrast, not the 2–6× the prose implies. The
0.6–0.9 figures belong to a *different* treatment (`actual_presence` sensitivity: 0.667 vs
0.444), not the canonical primary. The probabilistic team doc then inherited this as
`δ₁ ≈ 0.6–0.9` dilution arithmetic. This is the cleanest OVERCLAIM in the chain: a headline
RUN doc stating effect sizes that contradict its own artifact. **Fix:** replace "0.6–0.9 vs
0.15–0.3" with the filed phase means (0.36 vs 0.32, straddle median 0.30), and note the
spike is a tail phenomenon (hard SEG shifts only, 25% of straddle windows reach ≥0.6).

**Risk 2 — "P holds decisively" when P is saturated.**
`...RUN-2026-08-21.md:26` reports P_trans=0.994 as "decisive" persistence of idiosyncrasy.
The red-team measured q_trans ≈ q_rest ≈ 0.132: the step is a rigid common translation on
the exact subspace P uses, so P ≈ 1 is the *noise floor*, not evidence of survival. The kill
branch is unreachable by construction (needs a 0.5 gap on a 0.005-wide CI). "Decisively"
is the single most consequential word in the run doc and it is wrong — the correct word is
"uninformative." **Fix:** re-file P as "saturated — q_trans ≈ q_rest, cannot distinguish
persistence from rigid shift," and route the q-rule (red-team §1.4, ~5 lines) as the
replacement statistic before any future SURVIVED verdict.

**Risk 3 — "JEPA" as the load-bearing noun for a hand-crafted stub.**
`README.md`'s "five lines" are honest ("'JEPA' is the aspiration, not yet an implementation
(the backbone is a stub)"). But the rest of the README, the hero, the architecture diagram,
and the entire brand framing use "JEPA dials," "JEPA correlates; it never replaces," "many
JEPA models" as if the learned model exists. It does not — the dials are keyword heuristics,
the backbone is a stub, and the only contrastive component (the 2026-08-19 contrast head) is
explicitly excluded from the JEPA label in `topic.md`. The aspiration is packaged as the
thing. This is the single most *pervasive* overclaim — not a false number, but a false
implication carried by every sentence that says "JEPA" without "aspiration-to."

---

## 3. What's genuinely well-handled (credit where the discipline works)

1. **The VOID is declared first, loudly, with an exact rule citation.** Verdict line 1 of the
   band-movers run is "VOID BY RULE §5.3 — 17 counted down-crossings < 20," before any leg is
   shown. This is the opposite of p-hacking-by-framing; most groups would bury it.
2. **The referent sensitivity is filed in full, not swept.** A_start=0.0/p=1.0 sits in the
   JSON alongside A_center=0.647/p=0.0013, and the RUN doc's deviation note 1 explains the
   arithmetic reason (W/2=6 > TOL=3). Even though the *choice* is post-hoc (see §5), the
   *disclosure* is not.
3. **The erratum is an annotation, not a silent fix.** E5's 0.4366 → 0.1342 (in-place-mutation
   bug) is crossed out with the bug named and the commit (`de228ec`) cited, not quietly
   rewritten (`topic.md:37`). The R4 "no deleted numbers" rule is actually holding here.
4. **The confound is named, measured, and caveated at the right granularity.** The geometric
   doc refuses to overclaim: it insists the *generic* baseline share is 0.990 and the *specific*
   fact is axis alignment (0.978) — a precision that would be easy to skip.
5. **The adversarial teams are preserved, not suppressed.** Red-team's "the guard is a no-op,"
   ZeroClaw's "full unification is the anti-R1 move," geometric's "the sphere is the wrong
   primary object" — all filed as dissents, none laundered into agreement. The synthesis doc
   records "DISSENT" explicitly for the algebraic team rather than forcing consensus.
6. **Ordering honesty.** The 2026-08-21 addendum's provenance note admits "the addendum
   ordering deviation is disclosed rather than backdated" — a self-aware acknowledgment that
   the pre-registration is softer than it looks.

---

## 4. The truthfulness score

**Grade: B+**

**Reasoning.** The *posture* is A-level — void-first, sensitivity-carried, erratum-annotated,
dissent-preserved, ordering-disclosed. That is rare, and it is the reason this is not a C or
lower. But the audit is about whether the *claims as filed* are true at the strength stated,
and three concrete things fail that test: (1) the descriptive drift-spike numbers (0.6–0.9 vs
0.15–0.3) contradict the run's own JSON (0.36 vs 0.32) — a headline RUN doc stating an effect
size its own artifact refutes; (2) "P holds decisively" is stated where "P saturated,
uninformative" is the truth; (3) "imbalance ≡ d_mu proven to 1e-12" is a definitional norm
agreement (one filing even says "unproven in code yet") presented as a deep identity. Add the
zero-test pipeline that produces the headline A/P/D/S numbers, and the grade cannot be in the
A range. B+ recognizes that the structure is honest and most numbers reproduce exactly, while
flagging that the narrative layer — the adjectives and the descriptive effect sizes — runs
ahead of the evidence in exactly the places a reader is most likely to quote.

**This is not "dishonest work." It is honest work with a marketing layer.** The numbers are
real and reproducible; the sentences around them overreach. One disciplined revision closes
most of the gap.

---

## 5. Concrete correction list (3–5 edits that move the grade up)

1. **`PREMISE-BAND-MOVERS-RUN-2026-08-21.md:35` and `:177`** — replace "split-half d ≈ 0.6–0.9
   corpus-sd, vs stable ≈ 0.15–0.3" with the filed `mean_d_by_phase` values (transition 0.36,
   stable 0.32, canonical; straddle median 0.30), and state that the 0.6–0.9 range is the
   `actual_presence` sensitivity channel, not the primary. This is the single highest-leverage
   edit — it is a real numeric inflation in the run's headline mechanism paragraph.

2. **`PREMISE-BAND-MOVERS-RUN-2026-08-21.md:26`** — change "P holds decisively" to "P is
   saturated (q_trans ≈ q_rest ≈ 0.13 on the 4-dial subspace; the step is a rigid translation
   there, so P_trans ≈ 1 is the estimator's noise floor, not evidence of persistence)," and add
   the q-rule as the registered replacement (red-team §1.4, ~5 lines in `leg_P`).

3. **`README.md` "What this is in five lines" vs body** — add one sentence at the top of the
   Architecture/Dials sections making the five-lines honesty load-bearing throughout: "In v0,
   'JEPA dial' means *hand-crafted keyword heuristic with a JEPA-shaped interface*; the learned
   backbone (`jepa.py`) is a stub and v1 trains it." Currently the "five lines" honesty and the
   body's "many JEPA models" are in tension; a reader who skips the five lines is misled.

4. **`memory/collective-unconscious-synergy-2026-08-20.md:30`** — reconcile the internal
   contradiction: either "proven to 1e-12 (numpy, bridge_demo.py)" *or* "documented, unproven in
   code yet," not both. And wherever "imbalance ≡ d_mu" is claimed, add the one-word qualifier
   "definitionally" — both are ‖after − before‖; the 1e-12 is float agreement on a tautology,
   not an empirical identity.

5. **`README.md` Tests section (and `pyproject.toml:20`)** — either add a pytest module for the
   E2/E3 pipeline (`leg_P`, `leg_A`, `night_windows`, the ladder gate) so the headline A/P/D/S
   numbers are regression-protected, or qualify the "277" line with "the premise-band-movers
   pipeline has no automated tests; its assertions run only under `main()`." As it stands, "277
   tests" is true but implies coverage the exact pipeline producing the headline claims does not
   have.

---

## The 5-line truthfulness verdict

The elephant/JEPA work is **structurally honest and numerically reproducible** — the void is
declared first, the referent flip is filed, the E5 erratum is annotated not deleted, and the
adversarial dissents are preserved. Its **headline numbers (A 0.647/p=0.0013, P 0.994, ICC
0.7714/0.9076, 277 tests, void 17<20) all reproduce exactly** from the JSON artifacts. Its
**weakness is the narrative layer, not the data**: one RUN doc states a drift-spike effect size
(0.6–0.9 vs 0.15–0.3) its own JSON refutes (0.36 vs 0.32), "P holds decisively" is stated where
"saturated/uninformative" is true, and "imbalance ≡ d_mu proven to 1e-12" is a definitional norm
agreement wearing a deep-identity costume. **Grade: B+** — honest work with a marketing layer;
one disciplined revision (fix the two verbs/numbers, qualify the JEPA branding, test or qualify
the pipeline) moves it to A−.

*Read-only. No repo files modified. Sources: `memory/{foundation-synthesis, math-foundation-redteam, math-foundation-dissertation, math-foundation-geometric}-2026-08-21.md`, `memory/collective-unconscious-synergy-2026-08-20.md`, `memory/quilt-synergy-map-2026-08-21.md`, elephant `README.md`/`PREMISE-BAND-MOVERS-RUN-2026-08-21.md`/`STAGE2-RUN-2026-08-20.md`/`pyproject.toml`/`data/slope/*.json`, `zeroclaw-dissertation/research/topic.md`. Verified by reproduction against `data/slope/premise-band-movers-results.json` and a live `pytest` run (276 passed + 1 flaky).*
