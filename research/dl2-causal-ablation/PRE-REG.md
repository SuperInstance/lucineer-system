# PRE-REG: DL2 Causal Ablation — Mapping JEV's Implicit Room Physics

**Written:** 2026-10-06, 16:30 AKDT (file mtime; the measured batch began 16:32) — BEFORE any experimental arm was run.
**Apparatus check done prior to this document:** one (1) JEV call on a handcrafted benign transition (apparatus/key verification only; not part of any arm; result not used in any analysis below).

## Question

Which physical couplings (co-movement relations between dimensions) does JEV actually encode, and which does it ignore? Lane 2 showed JEV's noul is 81% predictable from marginals (L1-norm 63% of importance); the residual ~20% is hypothesized to be coupling sensitivity. This lane makes that residual causal: remove or invert specific couplings from clean transitions and measure the judgment shift beyond what marginal features explain.

## Design

### Data
300 clean transitions from `research/jev-jepa-meta/transitions.jsonl` (fixed, ids 0–499 interleaved; generator ground truth for couplings is known from `gen_transitions.py`). Corrupted transitions are excluded.

### Conditions (frozen)

For each coupling C with leader→follower structure, on its **active set** (rule frozen below):

1. **REMOVE**: freeze the follower dim at its before-value (the coupled consequence goes missing; leader unchanged).
2. **INVERT**: move the follower the wrong way relative to the coupling (same-order magnitude, opposite sign of the physical expectation).

Sample size: `min(20, n_active)` per coupling per condition, sampled with `numpy.random.default_rng(202)`, ids frozen in `manifest.json` before any call.

| ID | Edge (leader→follower) | Active rule (on clean transitions) | Remove edit | Invert edit |
|---|---|---|---|---|
| C1 | temp→humidity (psychrometric: warming ⇒ RH falls) | \|Δtemp_c\| > 0.5 | RH_after := RH_before | RH_after := RH_before + 4·sign(Δtemp) |
| C2 | occupants→CO₂ | Δoccupants ≠ 0 | CO₂_after := CO₂_before | CO₂_after := CO₂_before + 120·sign(Δocc) |
| C3 | ventilation→CO₂ (decay toward 420) | Δdoor_open_frac > 0.2 OR Δair_flow > 0.15 | CO₂_after := CO₂_before | CO₂_after := CO₂_before + 150 |
| C4 | ventilation→PM2.5 (drift toward outdoor) | Δdoor_open_frac > 0.2 AND \|pm25 − outdoor_pm25\| > 4 | PM_after := PM_before | PM_after := PM_before + 6 |
| C5 | ventilation→temp (relax toward outdoor) | Δdoor_open_frac > 0.2 AND \|temp − outdoor_temp\| > 5 | T_after := T_before | T_after := T_before + 1.5·sign(T_before − T_out) |
| C6 | lights_on↔lux | Δlights_on ≠ False | lux_after := lux_before | lights ON⇒lux := max(0, before−200); OFF⇒lux := before+250 |
| C7 | room_temp→mug_temp (Newton cooling) | \|mug−room\|>3 AND \|Δmug\|>0.3 | mug_after := mug_before | Δmug := −Δmug (same magnitude, away from room temp) |
| C8 | door_open→air_flow | Δdoor_open_frac ≠ 0 | flow_after := flow_before | door opened⇒flow := max(0, before−0.3); closed⇒flow := min(1.5, before+0.3) |
| C9 | occupants→sound | Δoccupants ≠ 0 | sound_after := sound_before | sound_after := sound_before − 5·sign(Δocc) |
| C10 | ventilation→sound (outdoor noise) | Δdoor_open_frac > 0.2 | sound_after := sound_before | sound_after := sound_before − 5 |
| C11 | heater_on→temp↑ | heater turned on (before false, after true) | T_after := T_before | T_after := T_before − 1.0 |

All edits keep the leader untouched (the cause stays visible; only the consequence is tampered). Clamps keep values in physically printable ranges.

### Probes (couplings NOT in the generator — JEV prior tests)

| ID | Hypothesis | Active rule | Edit |
|---|---|---|---|
| P1 | rain⇒humidity rises (even w/ window closed) | scene="light rain", Δdoor=0, \|ΔRH\|<1 | inject: RH_after := RH_before + 6 |
| P2 | night + lights off ⇒ near-dark lux | after: night, lights_on=false, lux>200 | repair: lux_after := 4 |
| P3 | empty room ⇒ no CO₂ source | occupants=0 in both states | inject: CO₂_after := CO₂_before + 150 |
| P4 | NO-EDGE control: lights⇏humidity (generator has none; JEV should not care) | \|Δlux\|>200, Δdoor=0, \|Δtemp\|<0.3 | inject: RH_after := RH_before + 5 |

P1–P3 test hallucinated/prior edges (JEV physics beyond generator); P4 tests specificity (JEV should show CE≈0 for a non-physics coupling). n = min(15, n_active), same seed 202.

### Sham (procedure/marginal control)

For each coupling C (follower dim d): 12 transitions from C's INACTIVE set, edit `d_after := d_before + δ` with δ = median active-arm edit magnitude, random sign (seeded). Sham CE should be ≈ 0 for a clean procedure.

### Baselines (drift control)

- **Fresh baseline**: every original transition used in any arm is re-judged in the same session (paired Δnoul = orig − edited, both fresh). Lane 2 judgments are NOT used as baselines.
- **Drift check**: 20 extra clean originals re-judged and compared to Lane 2 judgments.jsonl. Gate: Spearman ≥ 0.8 and mean |Δ| ≤ 0.15 → "consistent"; else flagged (paired analysis unaffected).

### JEV protocol (frozen)

- Endpoint `https://api.typesafe.ai/v1/systemone`, model `jev-latest`, key read at use-time from `~/.config/typesafe/token` (never echoed).
- 3 questions per call: `valid` (noul), `causal` (noul), `category` (choice) — same wording as Lane 2's judge_transitions.py.
- **Ramp receipt**: 3 warm-up calls discarded before the measured batch (no local GPU timing is involved in an API lane; warm-up is logged as the ramp receipt, plus a 3-second pre-batch pause).
- 6 workers, retries on 429/5xx with exponential backoff (as Lane 2). Every call logged to `ablation-judgments.jsonl` (append-only, resumable by id+arm).

### Marginal-null model (frozen)

RandomForestRegressor(400 trees, random_state=0, n_jobs=-1) retrained on ALL 500 Lane-2 transitions with Lane-2 `common.py` features (51 features, after-state overridable). Sanity gate: held-out R² (80/20 split, random_state=7, stratified) ∈ [0.70, 0.90]. The RF sees every ablated after-state's marginal features but encodes no couplings → Δrf = RF(orig) − RF(edited) is the marginal-predicted judgment shift.

## Metrics (frozen)

Primary: **CE_remove(C) = mean[ noul_orig − noul_edited ] − mean[ rf_orig − rf_edited ]** (paired per transition, then averaged). CE_invert same formula. Excess over the marginal-null = the coupling's causal weight in JEV's judgment.

Secondary: raw Δnoul, Δcausal-noul, P(category=unnatural | edited) − P(unnatural | orig), pinch-crossing rates (noul < 0.45 and < 0.50, Lane 1 thresholds).

Inference: bootstrap 95% CI (10,000 resamples, seed 7) on CE; paired Wilcoxon signed-rank p; Benjamini–Hochberg FDR across the 11 couplings, α = 0.05.

**Edge detection rule (frozen):** JEV "encodes" edge C iff CE_remove 95% CI excludes 0 AND FDR-adjusted p < 0.05. Sign encoding iff additionally CE_invert > CE_remove. Ranking = CE_remove point estimate.

## Outputs (frozen)

1. Causal map: generator-truth edges vs JEV-detected edges → precision/recall of JEV's implicit physics, plus prior-edges (P1–P4) as JEV-only additions.
2. `FINDINGS.md` with honest negatives (edges JEV does NOT encode count as first-class results).
3. `paper-causal-ablation.md`.

## What would falsify the framing

- If sham CE ≫ 0, the edit procedure itself is visible → all CE values discounted.
- If CE_remove ≈ 0 across the board, Lane 2's unexplained variance is NOT coupling sensitivity (it would then be noise, context effects, or drift).
- If RF held-out R² falls outside [0.70, 0.90], the marginal-null is unfit and CE is uninterpretable as "excess".

*Audit note (post-run edit):* this file was first written 16:30 AKDT, before the measured batch (16:32, see `manifest.json` mtime 16:30:36 and first `ablation-judgments.jsonl` write 16:32:02). The only edit after the run was correcting the header timestamp and adding this note — arm definitions, sampling rules, and gates are untouched.
