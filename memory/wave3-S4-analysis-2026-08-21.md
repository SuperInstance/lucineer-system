# WAVE-3 S4 — BLINDED ANALYSIS (the leg battery vs the α-gradient)

**Filed: 2026-08-21 (S4). Analyst session: subagent (procedurally blinded).**
Window read (nothing else): `memory/wave3-registration-2026-08-21.md` (frozen
registration), `memory/wave3-registration-addendum-g6-2026-08-21.md`,
`projects/elephant/data/wave3/legs/` (96 files: 16 corpora × W∈{12,8,16} ×
presence∈{canonical,actual}), `scripts/wave3_s3_legs.py`,
`scripts/wave3_s4_analyze.py` (written this step). The S3 run doc, sealed
sidecars, manifests, and corpus directories were NOT read. No α value, branch
assignment, or seal content appears below — pattern labels only. Primary
channel: **W=12, presence=canonical** (registered); W=8/16 + actual = the
registered sensitivity manifold (void rule 7). Machine-readable companion:
`projects/elephant/data/wave3/s4-blinded-summary.json`.

---

## 1. Corpus set structure (as recoverable from the leg window)

- 16 corpora: `w3k01–w3k06` (six standalone) + `w3q1m/n … w3q5m/n` (five
  matched pairs). Pair membership is structural, not α information: pair
  members share corpus_sd to 6 decimals and their night-family-matched
  trajectories correlate at **r = 0.996–0.9998** (cross-corpus max over all
  115 non-pair combinations: **0.666**, median 0.528) — the registered
  pair-mode "same room paths, same rosters" signature.
- The x-ladder (field X_W2 by family) is identical in all 16 corpora by
  construction; cell-level regression Sxx = 1.058 everywhere (≥ 0.19; the
  exact S3-side gate formula may differ — design is corpus-invariant either
  way).

## 2. Per-corpus leg table — primary channel (W=12, canonical)

| corpus | nEv | A rate | A p | A↑ | A_start | D_sig | D_null | P_trans | P hold | S slope | S x-inv | spread | pattern |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w3k01 | 37 | .892 | .000 | .000 | .998 | .8 | 0.0 | .990 | T | +.186 | T | .520 | instrument |
| w3k02 | 33 | .939 | .000 | .000 | .998 | .7 | 0.0 | .986 | T | +.644 | T | .392 | instrument |
| w3k03 | 36 | .722 | .000 | .000 | .933 | .8 | 0.0 | .981 | T | −.160 | T | .553 | instrument |
| w3k04 | 41 | .683 | .000 | .000 | .971 | .8 | 0.0 | .987 | T | +.662 | T | .388 | instrument |
| w3k05 | 36 | .917 | .000 | .000 | .999 | .8 | 0.0 | .983 | T | −.251 | T | .533 | instrument |
| w3k06 | 26 | .346 | .400 | .738 | .031 | .4 | 0.0 | .995 | T | +.545 | T | .389 | **noise** |
| w3q1m | 31 | .806 | .000 | .000 | .945 | .9 | 0.0 | .990 | T | +.128 | T | .460 | instrument |
| w3q1n | 30 | .800 | .000 | .000 | .931 | .9 | 0.0 | .990 | T | +.168 | T | .462 | instrument |
| w3q2m | 34 | .676 | .000 | .000 | .965 | .7 | 0.0 | .982 | T | +.078 | T | .487 | instrument |
| w3q2n | 34 | .676 | .000 | .000 | .989 | .7 | 0.0 | .982 | T | +.057 | T | .487 | instrument |
| w3q3m | 36 | .778 | .000 | .000 | .996 | .8 | 0.0 | .984 | T | −.421 | T | .386 | instrument |
| w3q3n | 39 | .769 | .000 | .000 | .998 | .9 | 0.0 | .984 | T | −.425 | T | .382 | instrument |
| w3q4m | 31 | .806 | .000 | .000 | 1.00 | .7 | 0.0 | .989 | T | −.159 | T | .325 | instrument |
| w3q4n | 31 | .774 | .000 | .000 | 1.00 | .7 | 0.0 | .989 | T | −.138 | T | .326 | instrument |
| w3q5m | 23 | .957 | .000 | .000 | 1.00 | .7 | 1.0 | .989 | T | −.578 | T | .402 | mixed* |
| w3q5n | 24 | .875 | .000 | .000 | .981 | .7 | 1.0 | .989 | T | −.514 | T | .385 | mixed* |

\* `mixed` = A fires (p≈0) but D cannot clear the null comparison: the single
null-night midpoint was covered (D_null = 1.0 on n=1), so "D above null" is
uninformative — not a KILL. rn-level null rate 0.143 vs signal 0.308 (ratio
0.46 < 0.5 → no v2 void). `spread` = derived diagnostic (night-demeaned
reader-mean dispersion of S cells; the registered 2AFC "baseline spread"
direction as measurable from the leg window). A↑ = up-mirror p (fires
wherever A fires; silent where A is silent). A_start = start-referent p —
silent in 15/16 at primary; fires only in w3k06 (p=.031; 1/48 referent tests
≈ chance; the timing lock is boundary-centered everywhere else).

**Pattern census (primary): 13 instrument-pattern, 2 mixed (D-uninformative),
1 noise-pattern, 0 collapse-pattern, 0 VOID.** The registered collapse
signature — P fails (pre/post cosine ≈ 0) and/or S falsification fires
(CI ∌ 0 AND beats roster competitor) — appears in **zero** corpora, in **zero**
of 96 channels corpus-wide (P_trans ∈ [.981,.995] wherever readable; S
x-invariant 96/96; the S signature cell count is empty; one ambiguous cell
w3k03 W16|actual, CI ∋ 0 but beats competitor).

**w3k06** is the sole silent corpus: A never fires at center-reference in any
of its 6 channels (p = .12–.89), lowest D (0.4–0.6), lowest signal-rn rate,
lowest corpus_sd (0.190 vs 0.236–0.248 elsewhere). It matches the registered
**noise** row (A ≈ null; D ≈ null-night; P holds — the pre-stated
non-discriminator; S x-invariant).

## 3. Sensitivity manifold (W∈{8,16}, presence=actual)

- **W=8:** A fires (p≈0) in all 15 firing corpora; w3k06 silent (p=.12/.55).
  Five low-crossing cells (< 20): w3k05 W8can (19), w3q1m (16/18),
  w3q1n (17/18) — all W8-only; primary unaffected (min 23).
- **W=16:** mechanically degenerate for A/P — A rates collapse (0.03–0.25),
  p flips to 0.8–1.0 for nearly all corpora, and P_rest is structurally
  absent (no stable strata fit a W=16 window; `holds=False` there is a
  channel artifact, **not** a P failure — read as P-unreadable). The S slope
  estimate is window-unstable (sign flips W8→W16 for most corpora) though the
  x-invariant verdict itself never flips.
- presence=actual tracks canonical closely everywhere (no verdict flips at
  W=12; the two q5 "mixed" cells and one k05 v2 void cell are
  canonical-side).

## 4. 2AFC pairs — the α-only differences

Within-pair |relative gaps| vs between-corpus gaps (primary channel):

| statistic | within-pair med (max) | between standalone med (max) | ratio |
|---|---|---|---|
| A rate | .011 (.085) | .201 (.273) | ~18× |
| n_events | .032 (.077) | .090 (.195) | ~3× |
| D_sig | .000 (.111) | .000 (.125) | — (coarse) |
| P_trans | .0002 (.0005) | .0033 (.0082) | ~16× |
| S slope | .129 (.273) | 1.245 (1.862) | ~10× |
| spread | .0033 (.041) | .249 (.298) | **~75×** |

The between-corpus variation the battery does see (e.g. spread clusters
{w3k01,03,05} ≈ .52–.55 vs {w3k02,04} ≈ .39, ratio 1.34 — right at the G6
addendum's disclosed 1.3× instrument/collapse effect size) is **not
α-carried**: the matched pairs, which share rooms/rosters and differ only in
α, are separated by 1–2 orders of magnitude less than unrelated corpora on
every statistic. The 2AFC converts "between-corpus differences exist" into
"they are design/room draws, not branch."

Per-leg pair rankings filed for the unblinding step (member read as
more-instrument per each pre-stated signed direction): spread↓ → m wins
q1/q3/q5, n wins q4, tie q2; S-slope↑(toward collapse) → m more-collapse in
q1/q2/q4/q5, ~tie q3; P_trans↓ → n more instrument 5/5 (gaps ≈ 2e-4, pure
noise); D↓ → m wins q3, ties elsewhere; A-rate↓ → m more instrument 4/5,
tie q2. Majority "more-instrument" member: q1=m, q3=m, q5=m, q2=n (weak),
q4=none. **No leg's within-pair ranking set is internally coherent beyond
chance, and no pair is separable at any channel** — the instrument cannot
rank the members of any pair.

## 5. Gradient ordering among the standalone six

Latent-chain search: is there ANY total order of {w3k01..05} satisfying all
six pre-stated signed directions (spread↓, S-slope↑, P_trans↓, D↓, A↓,
nEv↓)? Best achievable: **18/60 pairwise violations** (perfect = 0). No
one-dimensional gradient explains the five corpora; P_trans alone contributes
5/10 violations (unorderable), D ties 6/10 (coarse). Among the five,
spread~S-slope correlate r = −0.95 — a two-cluster structure, not a ladder.
**The battery finds no monotone α-gradient in the standalone set.**

## 6. VOID rulings (evaluable-in-window only)

| rule | ruling |
|---|---|
| v2 null-rn ≥ 50% signal-rn | ONE sensitivity cell: w3k05 W8\|canonical (0.143 vs 0.246). That cell is VOID; primary channel clean for all 16. No corpus-level void. |
| v3 < 20 crossings | 5 W8-only cells (listed §3). Branch-conditional blinded dual-read: floor-void if instrument-side, branch-hit if collapse/noise-side. Primary: none (min 23). |
| v5 effective draws | none (2000/2000 everywhere) |
| v1 gate (Sxx/sd part) | x-design identical corpus-invariant, Sxx = 1.058 cells ≥ 0.19; corpus_sd finite/used everywhere (0.190–0.248). Determinism/roster/strata-warmth parts are S3-side — not re-derivable here. |
| v4 continuity ladder | not a filed channel — not evaluable in window |
| v6 decoy panel | per-reader-detrending / mixed-effects decoys NOT filed by S3 — cannot fire here. Available estimator-variation columns: A vs up-mirror agree in all 16 at primary (fire together / silent together); start-ref is uniformly silent (boundary-centered lock), except the lone chance-level k06 firing. Referent-dependence is uniform, not differential — no contamination evidence in-window, but the registered decoy gate remains OPEN at unblinding. |
| ICC leg | not filed by S3 (G6 addendum re-band [0.60,0.80], instrument-vs-noise target) — deferred to the unblinding step; the derived spread diagnostic above is context only, carries no verdict. |

**No corpus is VOID at the primary channel on the evaluable rules.**

## 7. THE VERDICT — does the leg battery discriminate the α-gradient?

**No. H-GEN's branch-recovery claim fails on the instrument-vs-collapse
axis; the battery discriminates signal-vs-noise only.**

| leg | registered to discriminate | observed |
|---|---|---|
| **A** timing | signal-vs-noise (fires instrument, weak/absent collapse, ≈null noise) | **PARTIAL PASS**: cleanly separates the one silent corpus (noise-pattern) from 15 firing corpora, robustly across W8/W12 and both presences. But NO weakening gradient exists — every other corpus fires at p≈0 with rates .68–1.00; if collapse-branch corpora are among the 15, A reads them as instrument. Flat, not ↓. |
| **D** coverage | signal-vs-noise | **PARTIAL PASS**: lowest in the silent corpus (.4 vs .7–.9 night-level); coarse (10 transitions, 6 ties among standalone five); rn-rates overlap; q5's null estimate uninformative. Directionally consistent, weakly powered. |
| **P** persistence | **instrument-vs-collapse** | **FAIL**: holds (.981–.995 ≈ P_rest) in every readable channel of every corpus; the registered collapse prediction (pre/post cosine ≈ 0) is absent corpus-wide. Non-discriminating on this corpus set. |
| **S** x-invariance | **instrument-vs-collapse** | **FAIL**: x-invariant in 96/96 channels; the registered collapse signature (CI ∌ 0 AND beats roster competitor) fires nowhere; slope estimate window-unstable. Non-discriminating. |
| **ICC** | instrument-vs-noise (post-G6) | not evaluable in this window (not filed). |
| **2AFC** (all legs) | pairs rankable; ≥8/10 orderings | **FAIL**: within-pair gaps 1–2 orders below between-corpus gaps on every statistic; no pair separable at any channel; rankings chance-level. |
| **gradient** (standalone) | intermediate α ordered | **FAIL**: no total order satisfies the six signed directions (best 18/60 violations); two-cluster structure, not a ladder. |

This is the registration's pre-stated **anti-hypothesis (ii)** — the honest
negative — not a void: the apparatus runs clean (no primary-channel voids,
seeds/draws all valid, referent columns uniform) and recovers the noise
endpoint, but cannot separate instrument from collapse even at endpoints.

**Localization (which sufficient statistic the estimator is blind to):**
after the G6 rework α lives only in the per-night persona anchor
(`vibe = pool + (1−α)·dev`); the legs registered to carry the α signal are
blind to it — P's offset-cosine is pinned by the within-night-constant
charisma-pull fiber state (holds whether offsets are reader- or
room-carried), and S's x-regression never rejects x-invariance (anchor-scale
variation is small against per-speak noise at this n: within-pair spread
gaps ≈ 0.3%). The legs that DO vary across corpora (A, D, spread) ride
α-invariant channels — κ(t), latent room draws — which is exactly what the
matched-pair design demonstrates. The between-corpus spread clusters at
1.34× (near the addendum's 1.3×) exist but are room-confounded, not
α-carried.

**Booked for the unblinding step:** (1) sealed sidecar comparison against
the §2 pattern census and §4 pair rankings; (2) the ICC leg through the
registered Measurement; (3) the decoy-panel gate (v6) — the one registered
void rule this window cannot evaluate; (4) whether the lone silent corpus is
indeed the null-mode corpus (its pattern matches the registered noise row;
if it is not, the signal-vs-noise pass degrades too).

---

**Provenance:** read: registration + G6 addendum + 96 leg files + the two
named scripts. Written: this document, `scripts/wave3_s4_analyze.py`,
`data/wave3/s4-blinded-summary.json`. Not read: the S3 run doc, sealed
sidecars/manifests, corpus directories, git history. No α guessed anywhere
above; all labels are pattern labels. No commit made (blinding: commit
messages can leak; the unblinding step should commit).
