# κ(t)-Around-Entry-Steps Check — 2026-08-21

**Read-only experiment.** No commits, no corpus writes. Analysis script at
`/tmp/kappa_check.py` (temp, not in the repo). Grounding: Claude's
orchestration view §5 move 1 — "κ(t) check verdict by Monday: kills the last
design unknown, clarifies whether wave-3 ships or riverbed needs a rebuild."

**Verdict (4 lines):**

1. **Entry-steps are DIRECTION events (μ-response), not concentration events.** The mean direction moves at entry **at the same magnitude as a warm→cynical flip** (dwarmth −0.147 vs −0.151, permutation p = 0.68; ‖Δμ̂‖ +0.301 vs +0.329, p = 0.48). μ is **not** continuous at entry — the generator's defining "entry = κ-event" prediction is falsified.
2. **κ does not spike at entry; it *loosens*.** Pooled Δlogκ = −0.320 [−0.418, −0.205] (κ falls ~27%), and it falls **less** than at a flip (−0.746, p = 0.000). Opposite sign to the generator's +12 tightening pulse.
3. **The null contrast is decisive:** non-entry transitions (flips) also produce a κ response — **larger** than entry's. So "κ responds" is generic to all transitions, not specific to entry.
4. **Consequence for wave-3:** the generator's κ-trajectory-first model ("entry = κ event, μ continuous") is **not supported** → do **not** ship the wave-3 power design as-is; the K-leg needs rework (see §7).

---

## 1. The question

Does a reader entering a room at a strata transition (an *entry-step*) make the
field's concentration κ(t) spike — i.e., is entry a **concentration (κ) event**
rather than a **mean-direction (μ) event**? The wave-3 generator
(`scripts/riverbed_generator.py`) *pre-supposes the answer* in its
"κ-trajectory-first" design header:

> "entry steps are concentration and roster-composition events; flips are
> mean-direction events … Flips are warmth-schedule jumps (μ events); entries
> are κ events with μ continuous by construction."

This check tests that presupposition against the **field** corpora (the wave-2
T-nights and the wave-1 S/D nights), using only already-logged per-speak vMF
fits and per-step edges. Nothing is regenerated, nothing is re-fit.

## 2. Data and instrument

Per speak, the logs already carry the room-field vMF MLE and its step deltas
(`elephant/vmf.py::vmf_fit`, `tapnight.py::_speak_event`):

- `fit.kappa` — κ(t), the concentration (rotation-invariant, reads ρ only).
- `fit.mu_hat` — μ(t), the mean direction (7-vector on S⁶).
- `fit.warmth_vmf` = Ŵ·μ̂ — the direction-only warmth (reads μ only).
- `edge.d_mu` / `edge.d_warmth` / `edge.d_log_kappa` — per-step Δμ / Δwarmth / Δlogκ.

**Critical property (from the code):** `fit` is computed from
`vmf_fit(vmf_windowed(room, bank, W=8))` over the **text dial readings** —
roster-invariant by construction. κ(t) and μ(t) therefore reflect the room's
*text content*, not the roster composition. (This matters — see §6.)

**Events (detected from data, first-speak of the staged drifter; flips from the
registered strata):**

| class | events | n |
|---|---|---|
| **ENTRY** (reader enters at a strata transition) | T4a@12, S4a@12 · T4b@28, S4b@28 · T5@24, T5c@24, D@24, D-cold@24 | 8 |
| **FLIP** (warm→cynical, no entrant — the canonical μ event) | T1@20, T3@20, T8@20, S1@20, S3@20, A@20 · T2@8, S2@8 | 8 |
| **QUIET** (stable-stratum interior, ≥8 speaks from any boundary) | interior steps of 18 nights, subsampled | 47 |

Per-event response metrics (window [e−1, e+7], the trailing-window W=8 span):
`dlogk = log κ(e+7)−log κ(e−1)` (κ response); `dwarmth = w(e+7)−w(e−1)` and
`dmu_net = ‖μ̂(e+7)−μ̂(e−1)‖` (μ response); `path_logk`, `path_mu` (cumulative
movement); `edge_*` (instantaneous step deltas at the event speak).

## 3. Per-step table

| night | seq | Δlogκ | Δwarmth | ‖Δμ̂‖ | Σ‖Δμ̂‖ | Σ|Δlogκ| | edge Δlogκ |
|---|---|---|---|---|---|---|---|---|
| **ENTRY** | | | | | | | |
| T4a | 12 | **−0.461** | −0.183 | +0.438 | +0.444 | +0.479 | −0.162 |
| S4a | 12 | −0.461 | −0.183 | +0.438 | +0.444 | +0.479 | −0.162 |
| T5 | 24 | −0.374 | −0.141 | +0.280 | +0.286 | +0.384 | −0.053 |
| T5c | 24 | −0.374 | −0.141 | +0.280 | +0.286 | +0.384 | −0.053 |
| D | 24 | −0.374 | −0.141 | +0.280 | +0.286 | +0.384 | −0.053 |
| D-cold | 24 | −0.374 | −0.141 | +0.280 | +0.286 | +0.384 | −0.053 |
| T4b | 28 | −0.068 | −0.123 | +0.207 | +0.225 | +0.122 | −0.036 |
| S4b | 28 | −0.068 | −0.123 | +0.207 | +0.225 | +0.122 | −0.036 |
| **FLIP** | | | | | | | |
| T1 | 20 | −0.746 | −0.151 | +0.329 | +0.335 | +0.746 | −0.126 |
| T3 | 20 | −0.746 | −0.151 | +0.329 | +0.335 | +0.746 | −0.126 |
| T8 | 20 | −0.746 | −0.151 | +0.329 | +0.335 | +0.746 | −0.126 |
| S1 | 20 | −0.746 | −0.151 | +0.329 | +0.335 | +0.746 | −0.126 |
| S3 | 20 | −0.746 | −0.151 | +0.329 | +0.335 | +0.746 | −0.126 |
| A | 20 | −0.746 | −0.151 | +0.329 | +0.335 | +0.746 | −0.126 |
| T2 | 8 | — (no pre-fit) | — | — | +0.466 | +0.350 | — |
| S2 | 8 | — (no pre-fit) | — | — | +0.466 | +0.350 | — |

κ response is **negative everywhere** (loosening). The warm-era entries
(T4a/S4a@12) show the *largest* entry κ-drop (−37%) — but they also show the
*largest* μ-movement (‖Δμ̂‖ +0.438), i.e. the entry with the biggest κ response
is simultaneously the entry with the biggest **direction** response.

## 4. Pooled results (bootstrap 95% CI over events, seed 20260821, B=2000)

| metric | ENTRY mean [CI] | FLIP mean [CI] | QUIET mean [CI] |
|---|---|---|---|
| Δlogκ (κ response) | **−0.320 [−0.418, −0.205]** | −0.746 [−0.746, −0.746] | +0.008 [−0.032, +0.045] |
| Δwarmth (μ projection) | **−0.147 [−0.162, −0.132]** | −0.151 [−0.151, −0.151] | −0.038 [−0.056, −0.020] |
| ‖Δμ̂‖ (μ direction) | **+0.301 [+0.243, +0.359]** | +0.329 [+0.329, +0.329] | +0.188 [+0.179, +0.196] |
| Σ‖Δμ̂‖ (μ path) | +0.310 [+0.256, +0.365] | +0.368 [+0.335, +0.417] | +0.222 [+0.214, +0.230] |
| Σ\|Δlogκ\| (κ path) | +0.342 [+0.244, +0.431] | +0.647 [+0.499, +0.746] | +0.225 [+0.204, +0.248] |
| edge Δlogκ (instant κ) | −0.076 [−0.108, −0.045] | −0.126 [−0.126, −0.126] | +0.011 [+0.005, +0.018] |
| edge Δμ (instant μ) | +0.047 [+0.037, +0.056] | +0.045 [+0.045, +0.045] | +0.033 [+0.031, +0.034] |

**Contrasts (permutation, two-sided; d = mean difference):**

| metric | entry vs flip | entry vs quiet | flip vs quiet |
|---|---|---|---|
| Δlogκ | **p = 0.000** (d = +0.427) | p = 0.000 (d = −0.327) | p = 0.000 (d = −0.754) |
| Δwarmth | **p = 0.682** (d = +0.004) | p = 0.001 (d = −0.109) | p = 0.002 (d = −0.113) |
| ‖Δμ̂‖ | **p = 0.479** (d = −0.028) | p = 0.000 (d = +0.113) | p = 0.000 (d = +0.142) |
| Σ\|Δlogκ\| | p = 0.004 (d = −0.305) | p = 0.010 (d = +0.117) | p = 0.000 (d = +0.422) |
| edge Δlogκ | p = 0.051 (d = +0.050) | p = 0.000 (d = −0.088) | p = 0.000 (d = −0.137) |
| edge Δμ | p = 0.743 (d = +0.002) | p = 0.001 (d = +0.014) | p = 0.002 (d = +0.012) |

The two contrasts that decide the question are the bolded rows:
- **Δwarmth: entry ≡ flip (p = 0.68).** μ moves at entry exactly as much as at a
  flip. Entry is *not* "μ-continuous".
- **Δlogκ: entry < flip (p = 0.000).** κ moves *less* at entry than at a flip.

## 5. The null contrast (what separates "entry is concentration" from "all transitions are concentration")

Task item 4 asks: do **non-entry** transitions also show a κ response? **Yes —
and larger than entry's.** A warm→cynical flip drops κ by −0.746 (≈53%), nearly
2.3× the entry's −0.320. κ responds to *every* content transition, and its
magnitude tracks the *direction* change, not the entry event. There is no
κ-signature that is **specific** to entry; entry's κ response is a strictly
smaller version of the flip's. This collapses the "entry is a concentration
event" hypothesis: if concentration response were entry's mechanism, entry
would show κ movement that flips do not — the opposite is observed.

## 6. Why this happens (the structural finding)

The field's κ(t) and μ(t) are **text-content** quantities (roster-invariant, by
measurement — STAGE2 §1). A staged entry changes the room *only through the
entrant's text* (the cynical `DRIFTER_LINES`). That text is a **direction**
perturbation: a cynical line in a warm window pulls μ̂ toward cynical (Δwarmth
drops) and, secondarily, makes the trailing window *heterogeneous*, which lowers
ρ and hence loosens κ. So in the engine, **entry is mechanically a μ-event with
a secondary κ side-effect** — the generator's model has it backwards.

Two further generator/field mismatches surfaced along the way:

1. **κ polarity is sign-flipped.** Field: warm (SEG1) content → κ ≈ 24 (tight);
   cynical (SEG2) content → κ ≈ 11 (loose). Generator
   (`riverbed_generator.py::room_schedule`): warm strata κ = 10 ("loose"),
   cold strata κ = 18 ("tight"). The generator's κ stratum levels run **opposite**
   to the engine's measured κ.
2. **Entry κ-pulse sign is wrong.** Generator adds a **+12 tightening pulse**
   decaying from each entry; the field shows entry **loosens** κ (all Δlogκ < 0).

## 7. Verdict and what it means for wave-3

**VERDICT: DIRECTION-EVENT.** Entry-steps are mean-direction (μ) events — μ
moves at flip-magnitude, κ moves at sub-flip magnitude, and κ's sign is
loosening (not the generator's tightening spike). The generator's
"entry = κ event, μ continuous" presupposition is **falsified** by the field.

**Consequence — do not ship wave-3 as-is.** The κ-trajectory-first model is the
wrong mechanism for entry. The K-leg does **not** stand as the primary path in
its current form; instead the generator needs one of:

- **Model entry as a μ (direction) event** — the entrant's text shifts μ̂ toward
  the entrant's vibe, exactly as a smaller flip. This is what the engine does;
  the generator should reproduce it, with κ as a derived (heterogeneity)
  response, not a designed control channel.
- **Or rebuild the K-leg honestly** — if κ is to remain the primary channel, it
  must match the engine's κ semantics: text-determined (not roster-driven),
  warm=tight / cynical=loose, entry=loosening. The current κ-trajectory design
  (`room_schedule`'s stratum levels and entry pulses) is sign-flipped on both
  counts.

Either way, the wave-3 plan's §1.2 treatment ("entry seqs 12/24/28 as
κ-events") and the generator's κ-first header are **pre-registered assumptions
that the field does not support**; they should be revised before any wave-3
corpus is generated. The riverbed harness (Claude's fallback) is now the
confirmed next block, not a contingency.

## 8. Honesty notes

- **Replica structure:** the 8 "entry" events are 3 distinct script families
  (warm-entry@12 ×2, cynical-entry@28 ×2, D-entry@24 ×4 — wave-1/wave-2
  replays); the 8 "flip" events are 2 distinct families (flip@20 ×6, flip@8 ×2).
  Bootstrap CIs over "events" therefore partly overstate independent evidence
  (the flip CI is degenerate by construction). The *conclusions* are robust at
  the family level: all 3 entry families show Δlogκ < 0 and Δwarmth ≈ the flip's
  −0.151; both flip families show larger κ drops than the entry families.
- **Small n:** 8 entry / 8 flip events; inference is permutation + bootstrap
  over events, not a parametric test. CIs are honest about the n.
- **Window alignment:** the trailing window (W=8) means fits are autocorrelated
  and warmth/κ change *gradually* — no step is a true jump; "response" is a
  window-span (8-speak) net change, which is why the flip also looks smooth.
- **Early-flip truncation:** T2/S2 flip@8 has no pre-fit (fits begin at seq 9);
  its dlogk/dwarmth/dmu_net are therefore unobserved and only path statistics
  are reported for it.

*Analysis scripts in `/tmp/kappa_check.py` + `/tmp/kappa_check_out.json`; no
repo file written, no commit, no corpus change.*
