# Novelty Research — the Elephant/JEPA Foundation vs. the Literature

*Research subagent, 2026-08-21. Read-only on repos; web search encouraged. Companion to the foundation files (`foundation-synthesis`, `math-foundation-{geometric,probabilistic,algebraic,redteam}-2026-08-21.md`), the dissertation's own `jepa-field-guide.md`, and `related-work.md`.*

**Method note.** Web search was run against the seven load-bearing claims named in the directive. Where I could reach a primary source or an arXiv/PMLR/ResearchGate record I name it; where a search returned a descriptive summary rather than a citable paper, I flag it `[verify-before-filing]`. The verdict scale: **NOVEL** (doesn't exist anywhere, to the best of search), **INCREMENTAL** (a real twist on existing work, gap is nameable), **KNOWN-REAPPLIED** (standard machinery applied to a new object; the object is new, the machinery is not).

---

## 0. One-paragraph bottom line (read this first)

The integrated riverbed — "a registered skew-product random field over S⁶, room base orbit ⊕ personality fiber, q-rule, data-derived warmth via the generalized eigenproblem C_room v = λ C_pers v" — is **mathematically near-100% re-application of classical machinery**. Every named object has a textbook or established antecedent: vMF on S⁶ is Mardia–Jupp + Banerjee (directional statistics canon); the "skew-product base ⊕ fiber" is a mixed-effects / random-effects variance decomposition wearing fiber-bundle language; the "data-derived warm direction" is **Fisher's linear discriminant / common spatial patterns** (the generalized eigenproblem between two covariance matrices, 1936); the hysteresis relay is Preisach (textbook, and already applied to *social* hysteresis in opinion dynamics); the "field-edge" is distributional drift/change-point detection (CUSUM/Page 1954, DDM/Gama 2004, KL divergence); "conversation temperature" already exists as a term in social signal processing and organizational psychology. The honest contribution is **not a new mathematics** — it is (a) a *sharply measured structural confound* (the warmth axis is parallel to the leading personality eigenvector, cos 0.978, so the "room thermometer" reads the readers, not the room), and (b) the *placement* already conceded in `related-work.md` (a century-old drift instrument pointed at a known reader's readings, consumed as a retrieval key), plus (c) the operationalized Agrippa regress. Everything else should be *cited as its ancestor*, not claimed.

---

## 1. Prior-art map (per claim)

### Claim 1 — von Mises–Fisher random fields for group/room state estimation

- **Closest known work.** (a) vMF as *the* model for directional data on the hypersphere: R. A. Fisher, "Dispersion on a Sphere," *Proc. Roy. Soc. A* 217 (1953); canon in K. V. Mardia & P. E. Jupp, *Directional Statistics*, Wiley (2000). (b) vMF **random fields / spatial regression** for spatially-correlated directional data — wind fields, DTI fiber orientations, material fiber orientations — is an established geostatistics sub-literature; e.g. "Spatial von Mises–Fisher regression for directional data" (Figshare dataset, T&F; AIMS journals). (c) vMF **mixture models** for high-dim normalized embeddings/clustering: A. Banerjee, I. Dhillon, J. Ghosh, S. Sra, "Clustering on the Unit Hypersphere using von Mises–Fisher Distributions," *JMLR* 6 (2005); S. Gopal & Y. Yang, "Von Mises–Fisher Clustering Models," ICML 2014 (PMLR v32) — including a *Temporal* variant (T-vMFmix) for evolving clusters; the `movMF` R package (Hornik & Grün).
- **How close.** Very close. Summarizing a batch of unit-normalized vectors as (μ̂, κ) is *exactly* Banerjee/Gopal–Yang; the elephant's `vmf_fit` is the Mardia–Jupp MLE with the Banerjee κ₀ initializer (already conceded in `related-work.md` C2). The "field" label is the main gap: what the code computes is a **per-window point fit** (μ̂, κ), not a vMF *random field* in the geostatistical sense (a spatial/spatiotemporal process with a specified cross-location dependence for μ and κ). A directional-statistics reviewer will read "random field over S⁶" as overclaiming a time series of point estimates.
- **Gap.** The *specific* combination — a 7-dial conversational instrument summarized as a vMF whose κ is "choppiness" and whose projected warmth is "tide height" — is an application-domain mapping, not a statistical novelty. The vMF-as-topic/temporal-cluster machinery (T-vMFmix) already covers "evolving directional cluster states."

### Claim 2 — "Skew product" / fiber-bundle decomposition of collective behavior into shared dynamics ⊕ individual idiosyncrasy

- **Closest known work.** (a) **Skew-product dynamical systems** are a standard ergodic-theory construction (base dynamics + fiber dynamics parameterized by the base); fiber bundles are standard topology. (b) The *statistical* form of "shared dynamics ⊕ per-unit offset" is a **mixed-effects / multilevel / random-effects model** — random intercepts and slopes — going back to Fisher's variance decomposition and canonically Laird & Ware (1982); there is an entire literature on multilevel models for **group dynamics**, including by the directional-statistics author himself: K. V. Mardia, "Statistical aspects of group dynamics: multilevel methods for emergent properties" (Leeds). (c) In affective computing, **Group Affect Recognition (GAR)** explicitly decomposes group affect into individual-member contributions + interaction + context (e.g. "Most Important Person-Guided … Group Affect Recognition," ICCV 2023; audio-visual group affect analysis).
- **How close.** Extremely close. The geometric team's "skew product: low-dim base orbit × 3-dim personality fiber, flow trivial to ~5°" *is* a mixed-effects model whose random-effect (reader-offset) variance dominates the fixed (room) effect — a standard variance-components finding. The fiber-bundle/skew-product language is a *re-description*, and the empirical upshot (the fiber dominates every scalar statistic) is a confound warning, not a new decomposition.
- **Gap.** What is modestly distinctive: carrying the *geometric* structure (S⁶, geodesic/parallel-transport composition of edges, holonomy) on top of the mixed-effects split. But the geometric team itself flags this as currently untestable (loop events rare). The substance is INCREMENTAL at best, and the honest read is "mixed-effects model on a sphere."

### Claim 3 — Hysteresis (Prager, Preisach) applied to agent/affective threshold systems

- **Closest known work.** (a) Preisach hysteresis operators are textbook (F. Preisach 1935; Krasnosel'skii–Pokrovskii); the relay/hysteron is the atomic operator. (b) **Social hysteresis in opinion dynamics is an active literature**: q-voter models, bounded-confidence models exhibiting nonequilibrium hysteresis and "heterogeneity-assisted ordering," hysteresis from cognitive dissonance (expressed-vs-private opinions model); e.g. arXiv:2410.16934 ("Impact of Cognitive Dissonance on Social Hysteresis"), arXiv:2002.09366 (q-voter/bounded-confidence hysteresis). (c) Emotional/affective *inertia* and hysteresis in affective-state transitions is a known psychometrics idea (Kuppens & Verduyn on emotional inertia; set-point/threshold models of mood).
- **How close.** Very close. The red-team/geometric docs already state the code's automaton is "a two-relay Preisach cell with shared thresholds" and that the relay topology is genuine but the level-sets {ρ=0.3, 0.6} are reader-personality artifacts. The *application* of Preisach to opinion/affect already exists in print.
- **Gap.** The sharp and honest finding — "the 0.3/kill edge is decorative; the three-state automaton operates as a single relay at 0.6, and the band edges are personality-scaled images of the drift field's level sets" — is a *diagnosis of a specific instrument*, and a good one, but it is not a new theory of hysteresis. The hysteresis itself is textbook; the contribution is the diagnostic, and it lands as a *critique* of the code, not a positive result.

### Claim 4 — The "field-edge" as a unit of comparable sameness vs. change-point / drift detection

- **Closest known work.** (a) Change-point detection: E. S. Page, "Continuous Inspection Schemes," *Biometrika* 41 (1954) — CUSUM; PELT/ruptures (Killick et al.), and the whole offline/online CPD toolbox. (b) Sequential drift detection: Gama, Medas, Castillo, Rodrigues, "Learning with Drift Detection" (DDM), SBIA 2004; ADWIN (Bifet & Gavaldà); Page–Hinkley. (c) Distributional divergence between two measures: KL / Jensen–Shannon / optimal transport — the probabilistic doc's own §1.3 derives the vMF KL edge. (d) MLOps drift monitoring (PSI, KS-test) — already conceded in `related-work.md` A4.
- **How close.** As close as it gets. The "edge" = chord distance / symmetric vMF divergence between two snapshots **is** change-point detection with a distributional divergence statistic, plus the deadband = a CI-gated alarm. `related-work.md` A1/A4 already concede CUSUM and DDM by name.
- **Gap.** Only the *placement*: using the divergence between two room-field measures as the atomic object of *comparison across conversations* (an indexing key) rather than a detection alarm on one stream. This is the same "placement" residual the whole dissertation already owns — re-placement, not new detection.

### Claim 5 — JEPA (LeCun et al.) actual landscape vs. the elephant's aspirational stub

- **Closest known work.** Fully mapped in the dissertation's own `jepa-field-guide.md`: LeCun (2022) position paper; I-JEPA (Assran et al., CVPR 2023); V-JEPA (Bardes et al., 2024) and V-JEPA 2 (2025); A-JEPA (2023); IWM (2024); LLM-JEPA / VL-JEPA (2025); anti-collapse lineage (CPC 2018, BYOL 2020, SimSiam 2021, data2vec 2022, VICReg/Barlow/W-MSE 2021). The field guide's §7 and `related-work.md` B3 both already concede: **no fleet component implements a JEPA architecture; the elephant's training is contrastive (InfoNCE/FaceNet); "JEPA" is doctrinal, not shipped.**
- **How close.** This claim is not novel and is *already honestly conceded* in the dissertation's own files. The "aspirational stub" is an acknowledged gap, and the field guide §9 flag 3 states that no JEPA-of-social-latents work exists as of 2026-08 — meaning the only novelty available here is a *future-work proposal* (the frozen-target JEPA over room edges, field guide §7.6), which is unbuilt.
- **Gap.** If built, a frozen-target JEPA over room edges would be a small, defensible novelty (external frozen encoder ⇒ no collapse channel). As it stands: a proposal, not a result.

### Claim 6 — Directional-statistics personality/trait decomposition (ICC-reliable subspaces in directional data)

- **Closest known work.** (a) ICC reliability is canon: P. E. Shrout & J. L. Fleiss, "Intraclass Correlations," *Psychological Bulletin* 86 (1979) — already named as a candidate in `related-work.md` flag 10c. (b) **Circular / von Mises mixed-effects models** for individual differences in directional data exist: Bayesian circular mixed models, the `bpnreg` R package (projected-normal / von Mises mixed effects), random effects on both mean direction and concentration. (c) Mardia's group-dynamics multilevel work (again). (d) Eigen-decomposition of personality covariance / PCA of trait space is textbook.
- **How close.** Very close. The "ICC-reliable subspace" is a standard reliability decomposition; the "personality eigenvector ∥ WARM" (cos 0.978) is an empirical *confound* finding, produced by standard PCA + ICC + cosine. The directional wrapper (circular mixed effects) already exists.
- **Gap.** The genuinely useful content is the *caution*, not the method: "ICC selects for the wrong invariance for a room thermometer — it picks directions where readers differ and rooms barely matter, while the room's dominant dynamical dial (cynicism) is the one excluded from the reliable subspace." This is a real, generalizable, quotable insight — but it is a *negative structural finding*, delivered by textbook machinery.

### Claim 7 — "Room-field thermometer" / conversation-temperature metrics

- **Closest known work.** (a) **"Conversational temperature"** is already a term in social signal processing — operationalized via turn-taking dynamics (speaker switches/min, response times, overlapping speech), silence patterns, behavioral synchrony/mimicry, and paralinguistic cues; a "Conversational Temperature" table appears in the SSP literature (ResearchGate record `221487160` — `[verify-before-filing]`), plus a Rice Univ. thesis on group-interaction analysis. (b) **"Team temperature check"** is a standard organizational-psychology practice (engagement/pulse surveys). (c) **Group Affect Recognition (GAR)** is an active CV/affective-computing subfield (ICCV 2023 MIP-guided; audio-visual group affect). (d) Emotional contagion / group mood (Hatfield et al.; Barsade) is a large literature. (e) "Social thermodynamics" analogies recur.
- **How close.** The *metaphor* is crowded; the *operationalization* (a 7-dial conversational state as a direction on S⁶, κ as "choppiness," warmth as a height function h_W = W·x) is a modest re-specification whose components are all standard.
- **Gap.** The distinctive and honest thing here is the *result*: the thermometer's warm axis is a **personality detector**, not a room sensor (cos(W, v*) = 0.978; 99.5% of W-variance is between-reader). That is a valuable, citable negative/cautionary finding about group-state instruments — not a new temperature metric.

---

## 2. Novelty verdict per claim

| # | Claim | Verdict | The gap, named |
|---|-------|---------|----------------|
| 1 | vMF random field for room state | **KNOWN-REAPPLIED** | vMF-on-embeddings is Banerjee/Gopal–Yang; "random field" overstates a time series of point fits (Mardia–Jupp). Application domain is the only novelty. |
| 2 | Skew-product / fiber-bundle base⊕fiber | **INCREMENTAL** (leaning known) | The decomposition *is* a mixed-effects/random-effects model (Mardia group-dynamics; Laird–Ware). The fiber-bundle language re-describes it; the empirical content is "the fiber dominates" — a confound, not a new object. |
| 3 | Preisach/Prager hysteresis for affect thresholds | **KNOWN-REAPPLIED** | Relay/Preisach is textbook; *social* hysteresis in opinion dynamics already exists (q-voter, cognitive-dissonance). The contribution is a diagnostic critique (kill edge is decorative), not new hysteresis theory. |
| 4 | Field-edge as unit of comparable sameness | **KNOWN-REAPPLIED** | Distributional drift/change-point detection (CUSUM/Page 1954; DDM/Gama 2004; KL divergence). Only the *placement* (edge-as-comparison-key) is new. |
| 5 | JEPA implementation landscape | **KNOWN** (already conceded) | No fleet JEPA exists; training is contrastive. The only novelty is an unbuilt future-work proposal (frozen-target JEPA). Honest status is "proposal, not result." |
| 6 | Directional personality/ICC decomposition | **KNOWN-REAPPLIED** | ICC (Shrout–Fleiss) + circular mixed effects (`bpnreg`) + PCA. The *caution* (ICC selects the wrong invariance) is the real, citable content — a negative finding. |
| 7 | Room-field thermometer / conversation temperature | **INCREMENTAL** | "Conversational temperature" and "team temperature" already exist (SSP, org psych, GAR). The vMF dial-bank spec is a modest re-spec; the genuine value is the measured confound. |

**Net: zero NOVEL machinery; two INCREMENTAL; five KNOWN-REAPPLIED (one of which is already conceded by the dissertation itself).**

---

## 3. The genuinely novel core (conservative)

If the bar is "what contributes something that does not already exist anywhere," the honest answer is narrow and mostly negative. Ranked:

1. **The structural confound as a *measured, generalizable* caution — not a new instrument.** The claim that, for a group-state instrument, *reliability (ICC) selects for the wrong invariance* — the ICC-reliable subspace is reader-stable, and the room's dominant dynamical dial (cynicism, 73% of step variance) is precisely the dial *excluded* from the reliable subspace — with the numbers to back it (cos(W, v*) = 0.978; 99.5% of W-variance between-reader; warmth is the *second* room axis, cos 0.24–0.40). I did not find this stated in exactly this directional form in the psychometrics/SSP literature, but I cannot rule out that a close cousin exists (the ICC-selects-stability-not-signal point is adjacent to known reliability critiques). **Status: original to this corpus, probably not unprecedented in the literature — claim cautiously as a finding, not as a theorem.**

2. **The q-rule** (red team): decompose each step into common translation ĉ + residual r_R, and use q = RMS(r_R)/RMS(o_pre) to separate "idiosyncrasy survives a *real* step" from "the step is a rigid common shift" (which saturates the P statistic by construction). This is a small but real methodological catch — a variance-components / common-vs-idiosyncratic decomposition turned into a falsifiability guard. **Status: genuinely useful; the underlying decomposition is textbook, but the specific falsifiability-trap it defuses is a real contribution to the instrument-design literature.**

3. **The operationalized Agrippa regress** — already claimed and correctly sized in `related-work.md` D1 ("possibly the sturdiest residual"): the interpreter regress turned into a falsifiable convergence measurement with booked negative numbers. **Status: pre-existing claim in the dissertation; not re-derived here.**

4. **The placement** — already claimed in `related-work.md`: a century-old drift-from-baseline instrument pointed at a *reader's readings of a room*, consumed as a retrieval key into a stratified half-life memory. **Status: pre-existing claim; placement, not new instrument.**

**Honest one-liner:** *The foundation's mathematics is a careful, well-named re-application of classical machinery (vMF, mixed-effects/skew-product, Preisach, change-point detection, ICC, LDA). What survives as genuinely the dissertation's own is (a) a measured structural confound that indicts its own "thermometer" (personality reads as warmth), (b) the q-rule as a falsifiability guard, (c) the operationalized regress, and (d) the placement — and all four were already, correctly, sized as such in `related-work.md`.*

---

## 4. Novelty risk (which claims would embarrass, and the citations to preempt them)

Ranked by embarrassment severity if a reviewer knows the literature:

1. **"Skew-product random field over S⁶" (foundation Axiom 1).** A reviewer in multilevel modeling or dynamical systems will instantly read this as *a mixed-effects model on a sphere with fiber-bundle vocabulary*. Preempt by citing **Mardia, "Statistical aspects of group dynamics: multilevel methods"** and **Laird & Ware (1982)** alongside the skew-product definition, and stating plainly that the structure is a mixed-effects decomposition *named* as a skew product, with the empirical upshot being a variance-components finding (fiber dominates), not a new dynamical object.

2. **"Data-derived warm direction via the generalized eigenproblem C_room v = λ C_pers v" (foundation Axiom 7).** This is **Fisher's linear discriminant** — the ratio of between-room to between-person covariance, solved by generalized eigendecomposition — and identically **Common Spatial Patterns** (CSP, Koles–Lazar–Zhou 1990, EEG). Preempt by citing **Fisher (1936)** and **Koles et al. (1990)** explicitly, and describing the "clean temperature axis" as "a Fisher/CSP discriminant between room response and personality variance," not a new construction.

3. **"Room-field thermometer" / "conversation temperature" (Axioms 3, 6 and the creative team's tide-table metaphor).** "Conversational temperature," "team temperature check," and Group Affect Recognition already exist as terms. Preempt by citing the SSP survey (**Vinciarelli, Pantic & Bourlard, "Social Signal Processing," 2009**) and a GAR source (ICCV 2023), and frame the contribution as *the measured failure mode* of such thermometers (they read personality), not the metaphor.

4. **"Field-edge as a unit of comparable sameness."** This is distributional drift/change-point detection. `related-work.md` A1/A4 already concede CUSUM and DDM — keep those, and add the **KL/JS divergence** framing (the probabilistic doc's own §1.3) so the edge is presented as a named divergence, not an invention.

5. **"vMF random field."** The "random field" label is the one a spatial statistician will flag hardest (the code fits a per-window point estimate). Preempt by citing **Mardia & Jupp (2000)** and **Gopal & Yang (2014, T-vMFmix)** and calling the object what it is: a **vMF time series / temporal vMF state**, reserving "random field" for the (unbuilt) spatiotemporal version.

6. **Preisach/social hysteresis.** Preempt by citing the **social-hysteresis opinion-dynamics literature** (q-voter, cognitive-dissonance hysteresis — arXiv:2410.16934 etc.) and **Preisach (1935) / Krasnosel'skii–Pokrovskii**, so the relay reading is presented as "an instance of known social hysteresis," not a discovery of hysteresis.

---

## 5. Where the dissertation must cite (the 3–5 load-bearing works)

These are the ancestors that must appear in the bibliography for the foundation to be honest. (All already partially in `related-work.md`; the foundation docs must *inherit* them.)

1. **Mardia, K. V., & Jupp, P. E. (2000). *Directional Statistics*. Wiley.** — the canon that covers vMF, the MLE/Newton solve, and (via Mardia's own work) *multilevel/group-dynamics directional models*. This single citation preempts claims 1, 2, and 6 at once.

2. **Fisher, R. A. (1936). "The Use of Multiple Measurements in Taxonomic Problems." *Annals of Eugenics* 7(2):179–188.** — the generalized eigenproblem `C_room v = λ C_pers v` is Fisher's linear discriminant. Cite this (and optionally **Koles, Lazar & Zhou (1990)** for CSP) so the "data-derived warm direction" is honestly framed.

3. **Banerjee, A., Dhillon, I. S., Ghosh, J., & Sra, S. (2005). "Clustering on the Unit Hypersphere using von Mises–Fisher Distributions." *JMLR* 6:1345–1382** — and **Gopal, S., & Yang, Y. (2014). "Von Mises–Fisher Clustering Models." ICML/PMLR v32.** — the direct prior art for "summarize normalized embeddings as vMF," including a temporal variant (T-vMFmix). Preempts claim 1.

4. **Page, E. S. (1954). "Continuous Inspection Schemes." *Biometrika* 41(1/2):100–115** — and **Gama, J., Medas, P., Castillo, G., & Rodrigues, P. (2004). "Learning with Drift Detection." SBIA (LNCS 3171).** — the drift/change-point ancestors of the "field-edge." Preempts claim 4 (already in `related-work.md` A1/A4).

5. **Vinciarelli, A., Pantic, M., & Bourlard, H. (2009). "Social Signal Processing: Survey of an Emerging Domain." *Image and Vision Computing*** — plus a group-affect/conversation-temperature source (e.g. the ICCV 2023 GAR paper, or the SSP "conversational temperature" record). Preempts claim 7's metaphor.

**Secondary (cite if the specific mechanism is claimed):** Shrout & Fleiss (1979) for ICC (claim 6); Preisach (1935) + a social-hysteresis opinion-dynamics paper for claim 3; LeCun (2022) + I-JEPA/V-JEPA for claim 5 (already fully cited in `jepa-field-guide.md`).

---

## 6. Flags for the Captain (what I could *not* verify to citable certainty)

- **"Conversational temperature" as a formal term** — appears in SSP material (ResearchGate record `221487160`, a Rice thesis, several practitioner pieces) but I could not pin a canonical peer-reviewed definition. `[verify-before-filing]`.
- **Mardia's group-dynamics paper** — "Statistical aspects of group dynamics: multilevel methods for emergent properties" surfaced via a Leeds conference URL; verify exact title/venue before citing. `[verify-before-filing]`.
- **Social-hysteresis opinion-dynamics citations** (arXiv:2410.16934 "Impact of Cognitive Dissonance on Social Hysteresis"; arXiv:2002.09366 q-voter/bounded-confidence) — found as arXiv records; verify author/venue status before citing as more than preprints.
- **Spatial vMF random-field / regression sources** — found as Figshare/AIMS/arXiv records; verify the canonical citation (likely a *Statistics & Computing* or *Spatial Statistics* paper) before filing.

---

*End. Read-only; no repo or memory files beyond this one were written. The verdict in one line: **the foundation is a disciplined re-application of classical machinery (vMF, mixed-effects, Preisach, change-point detection, ICC, LDA); nothing in the mathematics is new; the honest contribution is a measured structural confound (the thermometer reads personality, cos 0.978), the q-rule, the operationalized regress, and the placement — and the dissertation already concedes this.***
