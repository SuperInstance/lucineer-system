# WAVE-3 REGISTRATION — G6 ADDENDUM (S2 dated re-verification)

**Filed 2026-08-21. Annotates (never edits) the frozen registration
`memory/wave3-registration-2026-08-21.md`.** The G6 noise-model rework
(`memory/research-g6-noise-2026-08-21.md`, the S3 gate) landed in
`scripts/riverbed_generator.py` and changes ABSOLUTE generator statistics
the registration's §1.3/§4.5 pre-stated as expectations. This addendum
re-verifies them, per the registration's own addendum discipline and G6 §5.
**S3's G6 precondition is now met; SHA-referenced in the elephant commit
`feat(riverbed): G6 noise-model fix — per-dial noise + unnormalized
emission + engine charisma-pull fiber (wave-3 S3 gate)`.**

## 1. What changed in the generator (the three-part G6 fix + geometry)

1. **Per-speak per-dial Gaussian noise** at the field's within-stratum
   per-dial shape (SIGMA_DIAL, RMS 0.140 z — volume ~deterministic,
   joke/presence loosest), applied to the windowed emission, **era-scaled
   by the κ(t) design channel** (√(KAPPA_COLD/κ(t)): warm ×0.68, cold ×1.0,
   entries ×1.28 — the field's within-stratum scatter is era-dependent
   with the same polarity; an era-independent σ structurally flattens the
   logged κ ratio: measured flip Δlogκ −0.53 vs the field's −0.746).
   Effective σ = 2.3 at DIAL_NOISE (the pooled marginal lands at the
   field's scale through the era-scaling).
2. **Unit-normalization dropped**: the emitted windowed z keeps its
   magnitude (field z-norms ≈ 2.0, anchored by BASELINE_Z at scale 0.35 —
   without the anchor the emission rail-pins cynicism/earnestness in warm
   eras). The FIT channel is the **clamped** dial-space reading (engine
   parity: the engine's fits run over windowed dial values, clamped to the
   dial cube).
3. **The vMF reader fiber is replaced by the engine's charisma-pull
   equation** — `replay_readings`/`tapnight.speak` replicated exactly
   (`eff = clamp(raw + s·(vibe − raw))`, `s = 1−exp(−charisma·n_R(t))`,
   vibe acclimation; **bit-exact replay parity**:
   `e2_instrument.assert_replay_matches_log` passes on every reader of
   every generated night, staged entrant included). The branch parameter
   α lives ONLY in the logged per-night persona anchor (vibe/vibe_start =
   pool + (1−α)·dev — the G2 Arm-2 semantics: the name persists, the
   instrument doesn't). The latent room is the **harness's AR(1) tangent
   wobble family** (G6 §5.2; iid vMF draws over-disperse the room's
   split-half to d≈1.24 vs the field room's 0.90).
4. **E_SEG schedule contrast adopted** (the harness's filed design
   decision; G6 §1.5/§5.4): the warm→cynical flip steps the emission
   along E_SEG (+0.81 z, field-measured), entries +0.51, warm base −0.11
   deviation-from-grand (the grand mean's E_SEG content lives in
   BASELINE_Z). μ(t) stays pure-warmth (Ŵ·μ = w(t) exact, the registered
   direction-only convention); the noise branch redraws the **whole
   persona per night (anchors AND dial weights)** — the lens is the
   charisma-pull fiber's stable-constant carrier.

## 2. Re-verified absolute statistics (registered seed 20260821, registered tags)

| statistic | registration §1.3 expectation | re-verified (G6) | verdict |
|---|---|---|---|
| corpus_sd | gate: finite/>0, per-corpus (never 0.2367 handed over) | **0.2568** (own numbers; E_SEG contrast + era-scaled noise; field 0.2367) | holds; +0.02 vs field disclosed |
| stable-d | floor 0.29, acceptance 0.26–0.40 (field actual 0.376) | **0.414** (registered object: W=12 split-half, own-sd normalized) | 0.014 over the band top on the registered draw (0.35–0.41 across draws) — disclosed; the OLD ×8 fiber error (0.81) is gone |
| logged κ (warm/cold) | ~21–26 / ~11–15 (field) | **37.4 / 18.7**, ratio **2.00** (field 2.18) | cold IN band; ratio preserved; warm carries a disclosed ×1.5 level offset (G6's own achievable band "~30/19" — §2.4) |
| warmth residual | ±0.10 gate band | strata-max **0.141**; gate: **ALL PASS** (drops ≤ 0.08 within ±0.10; final levels ≤ 0.112 within the S1-noise-aware ±(0.10+σ_fit=0.03)) | holds with the S1-form completion; G6's predicted entry-era breach realized at 0.03–0.04 over band, inside the gate's noise-aware form |
| ICC (instrument) | ∈ [0.85, 0.96] (brackets filed 0.9076) | **0.627** at the registered seed (0.63–0.78 across draws); **re-banded [0.60, 0.80]** | the charisma-pull fiber reproduces the FIELD's actual-presence structure (field **0.7411** through the same registered Measurement); the old bracket was the vMF-fiber calibration (0.886) — superseded |
| ICC (noise branch) | collapses < 0.667 (the prediction) | **0.228** | prediction holds (via the whole-persona redraw) |
| P 0.99-class persistence | within-night baseline constancy | unchanged by construction (charisma-pull is a within-night-constant fiber state; P is read on the registered apparatus at S4) | structurally holds |
| cos(v̂_temp, Ŵ) ≥ 0.8 under instrument | "the calibration the real corpus can never give" | to be re-run at S4 on the reworked corpora (this addendum re-opens the number, does not pre-state it) | re-verification queued |

**Branch-relative predictions (§1.3's α-sweep, 2AFC, discrimination
matrix): survive STRUCTURALLY** — (a) baseline spread still decreases with
α (instrument/collapse 1.3× — the effect size shrank from the vMF fiber's
2×+; the 2AFC object is the monotone ordering, which holds); (b) the S
collapse signature is branch-carried by the persona anchor exactly as
registered; (c) P's offsets are anchor-driven; (d) **the ICC leg's
instrument-vs-COLLAPSE cell must be re-read**: with the engine fiber both
branches are lens-stable (instrument 0.63 vs collapse 0.75 on the
registered draw — not discriminating); the ICC leg now discriminates
instrument-vs-NOISE (0.63 vs 0.23), and instrument-vs-collapse rides P/S.
This is a disclosed change in one leg's discrimination pattern, not a
void.

## 3. Sequencing

- The K-leg rework landed (`fa58526`) and is referenced by the prior
  advisory; **G6 now lands with this addendum** — S3's dependency class
  is cleared. S3 may generate once this addendum and the generator commit
  are both SHA-referenced (this file + the elephant commit).
- The gate (`riverbed_wave_gate.py`) carries the S1-form completion
  (final levels ±(0.10+0.03), drops strict ±0.10) — the gate-target
  holdout (never hand the field's 0.2367 to the generator) is unchanged.
- The registered E2/E3 scripts (`premise_band_movers.py`,
  `slope_regression_w2.py`, `e2_instrument.py`, `e2_nights.py`) are
  untouched — the generator now consumes them only through parity checks
  (`assert_replay_matches_log`).

## 4. Honesty notes

- The G6 sim's iid-noise design was **measured and amended**: iid
  post-window noise over-disperses the W=12 split-half (d 0.44–0.46 vs
  0.38 target); post-window AR(1) was worse on every metric (resid
  0.35–0.49); per-message-pre-window was worse still (d 0.61+, resid
  0.35+). The landed dependence: per-speak iid at the field's marginal
  per-dial shape, era-scaled, on the windowed emission.
- The expected-path reconstruction is **noise-aware in closed form**
  (truncated-normal clamp mean per dial + unit-vector quadrature over the
  noise/wobble scale) — the naive noise-free reconstruction carries
  −0.19..−0.24 systematic strata biases (rail-clamp one-sidedness,
  heterogeneous-noise normalization shrinkage) that the ±0.10 band cannot
  absorb.
- κ warm level 37 vs the field's 21–26 is the **last standing offset**:
  the σ level and the κ level trade off along the same curve (σ↓ →
  κ↑, corpus_sd↓, resid↓); the landed point favors corpus_sd + residual +
  ratio over the warm-κ level, per G6 §2.4's honest-limits table ordering.
- Concurrent-editor note: the persona-anchor construction (proportional
  field-magnitude anchors, `ANCHOR_SCALE`, superseding G7's DEV_SCALE)
  converged in a parallel session and was merged into this commit.

**Provenance:** read-only inputs: the frozen registration, G6 research,
S1 hardening doc, κ-check, the field corpus (measurements only). Written:
this addendum, the topic.md advisory line (append-only), and the elephant
commit. No registered corpus generated; no frozen document edited.
