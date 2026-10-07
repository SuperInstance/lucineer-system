# PRE-REG — DL1-REAL-JEPA: JEPA on real dial data, JEV on real residuals

**Frozen 2026-10-06 ~16:40 AKDT, BEFORE any experiment fires.** Pattern follows the
five surface lanes (`jev-jepa-*`): pre-register methods → run → report negatives
first-class. No results seen before this freeze.

## 0. What "real" means here (and what does not count)

- **Real dial streams** = per-speak `field_raw_after` 7-dim room-field vectors in
  `projects/elephant/data/nights/*.jsonl` — the registered instrument's logged
  output on the frozen conversation scripts (wave-1 primary nights
  A, D, D-cold, S1, S2, S3, S4a, S4b, S5). These are measured room fields, not
  synthetic room-feature vectors as in the five surface lanes.
- **Honest exclusion (verified before freeze):** wave-2 T-night raw fields are
  **bit-identical** to their wave-1 S-family counterparts (max |Δ| = 0.0 on
  S1 vs T1) — the raw field is roster-invariant text content. Wave-2 adds zero
  new room-field data for this JEPA. Wave-3 (`data/wave3/`) is riverbed
  forward-model output — real instrument, synthetic dynamics, known ground
  truth — excluded from "real" for this lane (noted as future validation set).
- Reader-side readings (`field_eff_to_reader`) are personality-warped; out of
  scope for the room-field JEPA-v1 (the spec's q-rule exists to *ignore*
  personality variance).

## 1. Frozen encoder (no training)

`elephant/vmf.py::vmf_fit` verbatim (numpy), applied to z-standardized
per-speak field vectors (`z = 2(v−c)/(hi−lo)`, tapnight bounds). Two target
channels:

- **Primary: logged cumulative fits** — the instrument's own logged `fit`
  objects (μ̂, κ, ρ, n), produced at logging time by
  `vmf_fit(vmf_windowed(room, bank, W=8))`. **AMENDMENT (pre-data, method
  fix):** the logged sample is trailing *sub-room bank windows*, which the
  logs do not carry (message text is hashed) — so the original V1 plan
  (re-derive logged fits from `field_raw_after`) is impossible by
  construction. Corrected operationalization: consume logged fits verbatim
  (zero reconstruction — strictly MORE faithful). V1 becomes a consistency
  gate: ‖μ̂‖ ≈ 1, 0 ≤ ρ ≤ 0.999, κ > 0, n ≥ 10, monotone n, no NaN —
  hard stop if violated.
- **Secondary: sliding fits (computed)** — fit at speak i over the last K=16
  per-speak z-standardized `field_raw_after` vectors via the same frozen
  `vmf_fit` solver (needs ≥ NMIN=10; earlier speaks → no latent). Documented
  deviation: speak-level full-room readings stand in for sub-room bank
  windows (bank replay needs message text the logs hash, not store).
  More local dynamics; a robustness channel, not the primary gate.

**Latent (7-dim, per JEPA-v1 spec):** `ℓ = [v*ᵀμ̂, log1p(κ), ρ, v2ᵀμ̂, v3ᵀμ̂, v4ᵀμ̂, v5ᵀμ̂]`
where (v*, v2, …, v7) is the **wave-1 full-7 generalized eigenbasis**
(C_room v = λ C_pers v, floored whitening eps=1e-2), recomputed read-only via
`scripts/reg1_rotation.py` machinery. Verification gate V2: recomputed v* and
v2 match the filed `data/slope/reg1-rotation-results.json` values to |cos| > 0.999.

## 2. Task, split, predictor

- **Task:** one-step-ahead latent prediction. Input `x_t = [ℓ_t, ℓ_t − ℓ_{t−1}]`
  (14-d). Target `ℓ_{t+1}` (7-d). Transitions only within a night.
- **Split (frozen):** TEST = {D-cold, S4b}; TRAIN = {A, D, S1, S2, S3, S4a, S5}.
  No pooling across waves (moot — wave-2 identical).
- **Predictor:** MLP 14 → 64 → 7, ReLU hidden. Adam lr 1e-3, full-batch,
  ≤ 4000 epochs, early stop patience 300 on train loss. 10 seeds; report
  mean ± sd over seeds.
- **Loss:** weighted L1, weights w = [1.0 (v*), 1.0 (log κ), 0.5 (ρ), 0.25 (v2), 0.25 (v3), 0.25 (v4), 0.25 (v5)].
- **q-rule mask (operationalized, frozen):** for edge t→t+1, `q_t = ‖P_room Δμ̂_t‖ / ‖Δμ̂_t‖`
  with P_room = projection onto span(v*, v2, v3, v4) of the unit direction
  change Δμ̂_t = μ̂_{t+1} − μ̂_t (z-space, renormalized). Zero loss when
  q_t < 0.2 (motion is common-shift/personality-like, not room dynamics).
- **Baselines:** (B0) persistence ℓ̂_{t+1} = ℓ_t — the pre-registered
  falsification baseline; (B1) train-mean-delta ℓ̂ = ℓ_t + mean_train(Δℓ) —
  descriptive only.

## 3. Frozen gates

- **G1 (falsification, from JEPA-v1 spec):** JEPA beats persistence by >15%
  RMSE reduction on BOTH v*ᵀμ̂ and log1p(κ) on pooled held-out transitions
  (10-seed mean). If not → the JEPA hypothesis as pre-registered is
  **falsified on real data** and reported as the primary finding.
- **G2 (secondary):** same test on sliding-window (K=16) channel.
- **V1/V2 encoder/basis verification gates** (above) — hard stops.

## 4. JEV battery on REAL residuals (frozen question set)

Population: all held-out transitions of both channels (logged cumulative + sliding),
predicted with seed-0 JEPA model AND persistence control. Budget cap: 90 rows
(both channels, stratified by residual-magnitude terciles). Decode predictions
to dial space for rendering: reconstruct μ̂ from basis projections
(z-space, unit norm), destandardize v = z/s + c, clip to bounds, log clip
fraction. κ rendered on the κ scale (expm1).

State (per row): night id, speak index, elapsed speaks, named 7 dials with
ranges/centers for before / predicted-after / actual-after.

Questions (all `noul`, graded P(yes), jev-latest):
- `valid`: "Could the predicted after-state plausibly follow from the
  before-state as a real room-conversation evolution?"
- `coupling`: "Do the predicted changes respect room couplings — volume with
  presence/participation, mood with joke_landing and earnestness, cynicism
  anti-aligned with mood, panic rare — i.e. one coherent conversational cause?"
- `close`: "Is the predicted after-state close to the actual after-state on
  every dial?"
- `actual_valid` (reference arm): same as `valid` but for the ACTUAL
  after-state — JEV's ceiling on real dynamics.

Arms: JEPA-predicted vs persistence-predicted (same rows, same questions).
Retry policy: 5 tries exponential backoff; append-only resumable log.

## 5. Frozen analyses

- **A1:** noul(valid) JEPA vs persistence; noul(actual_valid) as ceiling.
- **A2:** Spearman(raw L1 dial residual, noul) — on synthetic data this was
  ≈0.01–0.03 (orthogonal). Pre-registered question: is it still orthogonal on
  real residuals?
- **A3:** low-noul (<0.5) rows: classify by hand-audited failure mode —
  coupling violation / range violation / breadth (many dials moderately off)
  / focal (few dials far off) — compare to the synthetic-lane fingerprints.
- **A4 (the 20% question):** OLS/RF regression of noul(valid) on interpretable
  residual features (per-dial scaled |err|, breadth count, coupling-gap
  features |Δvol−Δpres|, |Δmood+Δjoke|, |Δcyn+Δmood|, κ error, ρ error).
  Report R² and importances — this is "what does the unexplained variance
  look like on real data."

## 6. GPU law

Ramp receipt at process start: ≥3s warmup, ≥1000 matmuls on the RTX 4050
before any timing/training measurement; record in output JSON.

## 7. Honesty rules

- Negative results are first-class. If G1 fails, FINDINGS leads with it.
- No pooling across channels in gate reads.
- Report clipping, seed variance, and n at every gate.
- Key read from `~/.config/typesafe/token` at use-time; never echoed, never
  persisted. No key material in any output file.
