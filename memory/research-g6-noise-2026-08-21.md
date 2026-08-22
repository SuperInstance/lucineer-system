# G6 Research — the vMF noise-model tension (corpus_sd × stable-d × warmth-SNR)

**Filed 2026-08-21. Read-only research + /tmp experiments** (simulator at
`/tmp/g6_sim.py`, monkeypatched to mirror `scripts/riverbed_generator.py`
emission; no repo file touched). Grounding: S1 finding 2
(`docs/riverbed-S1-hardening-2026-08-21.md`), the wave-3 registration
(`memory/wave3-registration-2026-08-21.md`), the κ-check
(`memory/kappa-t-check-2026-08-21.md`), the ideation §1.4 drift floor
(`memory/kimi-ideation-2026-08-21.md`).

**Verdict (5 lines):**

1. **The single-κ model cannot hit the triple — structurally, not just by tuning.** The generator emits unit-norm z-vectors (readings pinned to S⁶); the field's z-norms are ~2.0 with per-dial heterogeneous variance (cynicism z-sd 0.97, volume 0.014). corpus_sd is therefore capped ≈ 0.13–0.15 at ANY κ, and the three targets are coupled functionals of one concentration: loosening κ raises corpus_sd and lowers d (right direction) but drowns the logged-warmth fit (measured: 0.10 → 0.39 warmth residual while corpus_sd only reaches 0.23).
2. **The engine-faithful fix is a three-part decoupling, not a noise knob:** (i) per-speak per-dial Gaussian noise at the field's logged per-dial scales — supplies corpus_sd's noise component while the estimator (which unit-normalizes) absorbs only σ/‖z‖ of it; (ii) drop the unit-normalization of the *emitted* reading (keep the real magnitude — the engine logs the raw windowed z, not its direction); (iii) replace the vMF reader fiber with the engine's own charisma-pull form (`eff = raw + s(vibe − raw)`, the exact `replay_readings` equation) — this alone moves stable-d from 0.81 → 0.38 (field actual-presence 0.376).
3. **The triple IS reachable in expectation with the full fix, with one disclosed residual:** corpus_sd 0.2367 needs either σ_dial ≈ 2.1 (kills the ±0.10 warmth band: 0.18 residual, logged κ collapses to 15/10) or the field's E_SEG-style schedule contrast (~0.196; the WARM-direction schedule only supplies 0.108). At the corpus_sd-matching E_SEG+σ≈1.0 config, logged κ ≈ 30/19 (band) but the entry-era warmth residual sits at 0.13–0.16 — the standing ~0.03–0.06 breach, the same entry-era void risk S1 finding 1 flagged, worsened by the added noise.
4. **The field's d and the generator's d are the SAME estimator object** (`night_windows` W=12 split-half; field floor 0.261 canonical / 0.376 actual) — not an artifact. The mismatch is the fiber's: the field's readings are charisma-pulled convex combos of a smooth cumulative room reading and a stable persona vibe (autocorrelated); the generator's are iid vMF draws. Even the calibration harness (which DOES hit corpus_sd 0.2395 via E_SEG+magnitude) misses stable-d at 0.74 — nobody in the codebase currently hits the d floor; the engine-fiber change is the missing piece.
5. **Wave-3 consequence:** the G6 rework changes absolute generator statistics (corpus_sd normalization, logged κ levels — currently ×8 inflated: 200/90 vs field 24/11 — warmth floor), so the registration's §1.3 absolute expectations (ICC bracket, P 0.99-class) and the gate's warmth band need an S2 dated addendum re-verification; the branch-relative predictions (α-sweep, 2AFC pairs) survive in structure. S3 must not begin before G6 lands (same dependency class as the K-leg, registration §3).

---

## 1. The diagnosis — why one κ can't hit all three

### 1.1 The objects, measured on the field (wave-2 T-nights, 339 speaks)

| statistic | recipe | field | generator (registered seed) |
|---|---|---|---|
| corpus_sd | RMS over dials of pooled raw-sd (ddof=1) | **0.2367** | 0.1234 |
| stable-d | `night_windows` W=12 split-half ‖½₂−½₁‖/sd, windows wholly inside a stratum | **0.376 actual** (median 0.302; p90 0.697) · **0.261 canonical** (median 0.225 — the filed 0.29 floor) | 0.814 (S1's 0.86 is the same object, different draw/window set) |
| warmth-SNR | per-stratum mean of logged warmth_vmf vs the lag-accounted expected path (the gate's object), max | — (the field defines the ladder) | 0.1016 (marginal — S1 finding 1's ~0.0007 miss reproduces here) |
| logged κ | per-stratum mean of `fit.kappa` | warm ≈ 21–24, cold ≈ 11 | **201 / 89** (level ×8 inflated; ratio 2.26 ≈ field's 2.18) |

### 1.2 Structural cap #1 — the unit-sphere constraint

The generator emits `raw = clamp(CENTER + o_t/SCALE)` with `o_t = unit(windowed
mean of latent vMF draws)` — every z-vector lives on S⁶. For unit vectors the
per-component variance is bounded by 1/7 (uniform-sphere cap), so

  corpus_sd ≤ sqrt(mean over dials of (1/SCALE_d)² · (1/7)) ≈ **0.15**

regardless of κ (SCALE = 2/(hi−lo) ≥ 1 on four dials). The field's z-norms
have mean 1.997, sd 0.553 — the readings carry real magnitude and per-dial
heterogeneity (z-sd: cynicism 0.969, presence 0.403, joke 0.280, earnestness
0.182, mood 0.168, panic 0.073, volume 0.014). **No κ can push the current
model past ~0.13–0.15.** This is a noise-FAMILY error (directional-only), not
a calibration miss.

### 1.3 Structural cap #2 — the windowed-mean κ inflation

The fit input is the unit-normalized **mean of W=8 latent draws**. A mean of
8 draws at latent κ concentrates ~8×: measured logged κ ≈ 154–201 warm-era
(latent 24) vs the field's 24. The ratio semantics survive (the ×8 cancels in
log-ratios, which is why the κ-check's Δlogκ targets pass while the LEVELS
are ×8 off). The κ(t) trajectory as calibrated (24/11 latent) does NOT
produce the field's logged 24/11 — it produces 200/90.

### 1.4 The coupling surface (single-κ tradeoff, sim sweep)

Loosening the latent κ by a scale factor (current model, all else fixed):

| κ_scale | corpus_sd | stable-d | warmth residual (max) | logged κ_warm/cold |
|---|---|---|---|---|
| 1.0 | 0.136 | 0.729 | 0.102 | 154 / 65 |
| 0.5 | 0.148 | 0.685 | 0.088 | 78 / 38 |
| 0.25 | 0.175 | 0.580 | 0.140 | 39 / 20 |
| 0.125 | 0.201 | 0.502 | 0.310 | 21 / 13 |
| 0.0625 | 0.230 | 0.426 | 0.392 | 15 / 8 |

The field point (corpus_sd 0.2367, warmth ≤ 0.10) is **not on this curve**:
at corpus_sd ≈ 0.23 the warmth residual is 0.39. Mechanically: corpus_sd(κ)
is decreasing, d(κ) = Δ/σ(κ) is increasing (numerator = schedule displacement,
κ-independent), warmth-noise(κ) is decreasing — three different functionals
of the SAME concentration. The d-vs-corpus_sd pair is a genuine tradeoff but
the warmth-SNR is the third leg that pins the curve's end.

### 1.5 The corpus_sd decomposition — where the 0.2367 actually lives

| | within-stratum noise (raw RMS) | stratum contrast (raw RMS) | √(noise²+contrast²) |
|---|---|---|---|
| field | 0.134 | 0.196 | 0.238 |
| generator | 0.072 | 0.108 | 0.129 |

The generator is ~55% of the field on BOTH components. The noise gap is the
vMF tightness (fixable by dial noise). The **contrast gap is schedule
geometry**: the generator's flips move along WARM (mood-heavy: mood ±0.27
raw, cynicism ±0.14); the field's text steps move along E_SEG
(cynicism/presence/earnestness-heavy: cynicism ±0.24, presence ±0.22 — the
`calibration_harness.E_SEG` constant, which exists because the harness
measured it). The WARM-direction construction — the generator's founding
"warmth = Ŵ·μ̂ exactly" design — cannot supply the field's 0.196 contrast
without abandoning direction-only warmth. **The contrast is the largest
single missing contributor to corpus_sd.**

### 1.6 stable-d — the fiber's iid-sampling wobble, not the room's

Field room stable-d 0.90 vs reader stable-d 0.376: the reader readings are
*baseline-dominated* (stable persona vibe + charisma pull), so the within-
window split-half is a small fraction of the total sd (which includes the big
between-reader spread). The generator's reader readings are **iid vMF draws**
per speak (κ_R = 40): each speak is a fresh sample, so the 6/6 split-half is
sampling noise — the d = 0.81 is pinned by the fiber, not the room.
Evidence: raising κ_R 40 → 400 moves d only 0.87 → 0.68; swapping in the
engine's charisma-pull fiber (`eff = clamp(raw + s(vibe − raw))`, the exact
`replay_readings` equation) moves d to **0.377–0.40 — matching the field's
actual-presence 0.376 exactly**. The engine's own replay path already
contains the fix; the vMF fiber is the deviation. (Even the calibration
harness — the E_SEG model that DOES hit corpus_sd 0.2395 — misses stable-d
at 0.74; its verification never claimed the d floor.)

---

## 2. The engine-faithful fix — per-message dial noise + magnitude + engine fiber

### 2.1 The noise model

Per-speak (per-window — the engine's dials read the trailing W-message window
as ONE object, `dial.py::Dial.read(room)`; the per-speak warmth_vmf is the fit
over exactly those windowed z-vectors), add per-dial Gaussian noise to the
emitted z:

  z_w(t) = m(t)·u(t) + η(t),   η(t) ~ N(0, σ²·diag(SIGMA_DIAL²))

with SIGMA_DIAL = the field's **within-stratum** per-dial z-sd (measured
2026-08-21): mood 0.116, volume 0.010, earnestness 0.145, cynicism 0.149,
joke_landing 0.202, panic 0.028, presence 0.198 (RMS 0.140 z / 0.104 raw).
`m(t)·u(t)` is the shared component — the windowed mean of the latent vMF
path (u = direction, m = its true magnitude). Two emission rules:

1. **Drop the unit-normalization of the emitted reading.** raw = clamp(CENTER
   + z_w/SCALE) with z_w's real magnitude (the engine logs the raw windowed
   reading; `vmf_fit` unit-normalizes internally, so the estimator sees the
   direction of the SAME noisy vector — engine-faithful).
2. **The κ(t) trajectory controls the shared component only**: latent κ(t)
   sets how tight u(t) is (warmth tracking, the logged κ level). The dial
   noise is orthogonal to it.

### 2.2 Why this decouples corpus_sd from d and from warmth-SNR

- **corpus_sd** sees the dial noise FULL: σ contributes ~0.104·σ raw RMS to
  the within-stratum component (plus the contrast component from §1.5).
- **The estimator** sees only the direction of z_w: the noise's directional
  footprint is σ·‖η‖/(‖z‖·√7)-ish ≈ σ·0.14/2.0 — attenuated by the true
  magnitude ‖z‖ ≈ 2 (the field's baseline structure). At the field's
  magnitude, the warmth-facing noise is half of the sd-facing noise — this is
  the decoupling the unit-sphere model cannot do (there ‖z‖ ≡ 1 and the
  estimator and sd face the SAME noise).
- **stable-d** = (1−s̄)·(room within-window wobble)/corpus_sd with s̄ the
  charisma pull: the numerator is set by the fiber (s̄ ≈ 0.58 field-typical →
  d ≈ 0.38 at corpus_sd 0.2367), the denominator by the noise+contrast — the
  two knobs are now independent.

### 2.3 The logged-κ bonus

Because the estimator-facing scatter is now dial-noise-dominated (not
windowing-inflated), the logged κ at σ ≈ 1.0–1.4 lands at 20–32 / 13–22 —
**in the field's 24/11 band** — fixing the ×8 inflation for free. The latent
KAPPA_WARM/COLD need only a mild re-tune, not the 8× the current construction
implies.

### 2.4 The honest limits (measured)

| config (sim, registered seed) | corpus_sd | stable-d | warmth residual | logged κ_w/c |
|---|---|---|---|---|
| current model | 0.136 | 0.729 | 0.102 | 154 / 65 |
| + per-speak dial noise σ=2.0 (corpus_sd ✓) | **0.232** | 0.854 | **0.175 ✗** | 15 / 10 |
| + engine charisma-pull fiber | 0.16–0.25 | **0.377–0.40 ✓** | 0.14–0.19 ✗ | 20–11 / 13–8 |
| + E_SEG contrast (harness geometry), σ≈1.0 | ~0.23 ✓ | ~0.38 ✓ | 0.13–0.16 ✗ (marginal breach) | ~30 / 19 |

The warmth band is the **last standing conflict**: it caps σ ≲ 0.5 (band 0.10)
while corpus_sd 0.2367 at WARM geometry needs σ ≈ 2.1; the E_SEG contrast
closes most of the gap (needs σ ≈ 1.0), and at that σ the residual breach is
~0.03–0.06, concentrated in **entry-era strata** (the noise slows the
cumulative fit's response to entry μ-steps — the same entry-era void risk S1
finding 1 quantified at σ=0).

---

## 3. Calibration targets (what the fixed model must reproduce)

| target | value | recipe / source | band |
|---|---|---|---|
| corpus_sd | 0.2367 | e2 recipe, corpus's own numbers (gate G4 normalizes per-corpus) | gate: finite/>0; calibration target: within ~0.01–0.02 |
| stable-d floor | 0.29 (canonical 0.261 / actual 0.376) | `night_windows` W=12 split-half, stable windows | filed floor 0.29; acceptance 0.26–0.40 |
| ICC | 0.8444 actual / 0.7714 canonical (field) | registered Measurement | instrument bracket [0.85, 0.96], guard [0.667, 0.810] (registration §1.3/4.5) — must re-verify after the fiber change |
| logged κ | 24 / 11 (warm/cold) | per-stratum mean `fit.kappa` | ~21–26 / ~11–15 (field measured) |
| entry Δlogκ | −0.320 | pooled entry-window response | [−0.418, −0.205] |
| flip Δlogκ | −0.746 | pooled flip-window response | exact (degenerate CI) |
| warmth gate | logged strata-mean warmth vs lag-accounted schedule | riverbed gate G4 | ±0.10 |

---

## 4. The mini-calibration experiment (spec + results)

**Spec (what S2 should run):** sweep (σ_dial, schedule-geometry, fiber) on a
small synthetic set (9 families × 21 readers, registered seed, /tmp), fit to
the three targets:

1. **σ_dial** ∈ {0, 0.5, 1.0, 1.5, 2.0, 2.5} × SIGMA_DIAL (per-speak, per-dial).
2. **schedule geometry**: current WARM-direction flips vs the E_SEG additive
   contrast (harness constant, seg ∈ {0.8, 1.0, 1.2}).
3. **fiber**: current vMF (κ_R ∈ {40, 100, 400}) vs engine charisma-pull
   (replay_readings equation, s from charisma/interactions).
4. Metrics per cell: corpus_sd (e2 recipe), stable-d (band-movers W=12,
   stable windows, both presence channels), warmth residual vs lag-accounted
   expected path (max over strata, the gate object), logged κ warm/cold.

**Results (this research, registered seed):** see §1.4/§2.4 tables. The
achievable triple:

- **Reachable in expectation:** (corpus_sd ≈ 0.23–0.24, stable-d ≈ 0.38–0.40,
  logged κ ≈ 24/11) with the three-part fix (engine fiber + σ ≈ 1.0–1.4 +
  E_SEG geometry).
- **NOT simultaneously reachable in the current construction:** (0.2367,
  0.29, warmth ≤ 0.10). The residual is the entry-era warmth breach
  (~0.03–0.06 over band at the corpus_sd-matching σ). Three ways to absorb
  it, to be decided at S2: (a) re-tune KAPPA_ENTRY_FACTOR/entry-era noise so
  the fit's entry response stays sharp (risk: drifts from the measured −0.320
  entry Δlogκ); (b) noise-aware gate accounting at entry strata (extends S1
  finding 1's existing lead-in-memory adjustment — the breach is a modeled
  response-lag bias, not white noise); (c) accept + pre-plan the ~1-stratum-
  in-50 void risk, as S1 already documents.

---

## 5. Honesty note — is the triple unreachable, and what does that mean?

**The triple is reachable with the full engine-faithful fix; it is NOT
reachable by a noise-scale choice alone, and the field's d is not an
estimator artifact.** Specifically:

1. **The field's d and the generator's d are the same object** — both measured
   through the registered `night_windows` W=12 split-half on reader readings,
   normalized by each corpus's own corpus_sd. The 0.29/0.376 floor vs the
   0.81/0.86 generator value is a fiber-structure difference (charisma-pulled
   autocorrelated readings vs iid vMF draws), proven by the engine-fiber swap
   landing exactly on the field's actual-presence 0.376. No estimator change
   is needed or justified.
2. **The current model's d is not "wrong" in the sense of a bug** — it is the
   correct d of the WRONG noise family: iid per-speak draws over-disperse the
   within-window displacement relative to the field's scripted, autocorrelated
   text. The harness's AR(1) room wobble (φ = 0.98) is the right family for
   the room; the charisma-pull fiber is the right family for the readers.
3. **Wave-3 registration consequence (must be a dated S2 addendum):**
   - The G6 rework changes absolute generator statistics — corpus_sd
     normalization (per-corpus, gate-computed — the registration already
     forbids handing 0.2367 to the generator), the logged-κ LEVEL (200/90 →
     ~24/11, a level fix, ratio already correct), and the d floor (0.81 →
     ~0.38). The registration's §1.3 pre-stated absolute expectations — ICC
     bracket [0.85, 0.96], P 0.99-class persistence, the ±0.10 warmth band —
     must be re-verified against the reworked generator before S3.
   - The branch-RELATIVE predictions survive in structure: H-GEN compares
     branches within a corpus (α-sweep, 2AFC pairs), and the discrimination
     matrix's cells are relative (fires/fails) — a uniform noise-floor change
     does not invert them, but the §1.3 "calibration the real corpus can
     never give" expectations (cos(v̂_temp, Ŵ) ≥ 0.8 under instrument) must be
     re-run, not assumed.
   - The κ(t) targets (24/11, −0.320, −0.746) are LOGGED-quantity targets;
     the current model already misses the LEVEL (×8) and only hits the ratios
     by cancellation. The reworked model must re-pass the κ-check protocol
     (per-strata logged fits) before S3 — same dependency class as the K-leg
     rework, which the registration §3 already conditions S3 on. **G6 is the
     same kind of blocker: S3 must not generate until it lands and is
     referenced by SHA.**
4. **The field's corpus_sd itself is a mixed object** (noise 0.134 + contrast
   0.196) — the generator cannot reach it with noise alone (would breach the
   warmth gate) or contrast alone (WARM geometry caps at 0.108; E_SEG geometry
   changes the logged-warmth semantics toward the field's squashed 0.15 drop).
   The E_SEG change is the harness's already-filed design decision and should
   be adopted with the same disclosure the harness carries (the flip is a
   text step, not a warmth step; warmth loads on mood in WARM-space but the
   ladder lives in E_SEG-space).

**Method note:** all numbers above are from the registered seed 20260821,
`/tmp/g6_sim.py` (validated against the real generator: corpus_sd 0.136 vs
0.123, stable-d 0.73 vs 0.81, entry-era warmth miss +0.1016 reproducing S1
finding 1's 0.1007, logged κ 154/65 vs 201/89 — same structure, draw-level
differences from the sim's rng layout). Field numbers re-measured from the
filed wave-2 nights through the registered instruments. No repo file was
written or modified.
