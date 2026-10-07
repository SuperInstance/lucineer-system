# FINDINGS — DL2 Causal Ablation: JEV's Implicit Model of Room Physics

**Date:** 2026-10-06 · **Calls:** 824 logged (3 warm-up + 821 measured, 0 failures) · **Model:** jev-1.13.0
**Pre-registered:** `PRE-REG.md` (written 16:40 AKDT, before any arm ran). All gates passed.

## Headline

**JEV's implicit physics is sparse, sign-aware, and thermodynamic.** Of 11 generator-true couplings, the frozen detection rule confirms 3:

1. **window → temperature** (CE_remove = +0.094, CI [+0.059, +0.135], q = 0.0004) — the strongest edge by 3–5×. When the window opens, JEV expects indoor temp to relax toward outdoor; freezing it drops noul 0.066 even though the marginal-null model predicts noul should *improve* by 0.028 (less change = more plausible). The RF-null correction is doing real work here.
2. **room_temp → mug_temp** (CE_remove = +0.028 [+0.009, +0.048], q = 0.0499) — borderline, **and confounded**: the mug-dim sham produced CE = +0.198 [+0.048, +0.360]. JEV is extremely sensitive to large acausal mug jumps in general; the *coupling-specific* removal effect is small. See honest negatives.
3. **occupants → sound** (CE_remove = +0.017 [+0.005, +0.031], q = 0.0499, sham ≈ 0) — small but clean.

**Sign sensitivity:** for detected edges, inversion ≫ removal. C5 invert CE = +0.166; C7 invert CE = +0.165 with **55% of mug-inverted states falling below the 0.50 pinch threshold** (35% below 0.45) and the only "unnatural" category calls in the entire study (5%). C5 invert crosses 0.50 in 16% of cases. **JEV punishes contradictions far more than missing evidence.**

**Removals never flip the gate:** every removal arm's cross-0.50 rate ≤ 0.05. A clean state stays clean-graded even when an expected consequence is absent. JEV's 0.45–0.50 pinch (Lane 1) is asymmetric: it triggers on injected violations, not on withheld couplings.

## The Causal Map (generator truth vs JEV)

```
                    generator    JEV (this lane)
window  → temp        TRUE     ✔ DETECTED (strongest, sign-aware)
roomT   → mug         TRUE     ~ borderline (sham-confounded), inversion strong
people  → sound       TRUE     ✔ DETECTED (small, clean)
heater  → temp↑       TRUE     ✗ not detected (q=0.136, CI excludes 0 — underpowered, n=14)
temp    → RH↓         TRUE     ✗ not detected (CE +0.017, q=0.164)  ← no psychrometrics
people  → CO₂         TRUE     ✗ not detected (CE −0.002)             ← flat zero
window  → CO₂↓        TRUE     ✗ not detected (CE −0.007)
window  → PM2.5       TRUE     ✗ not detected (CE +0.008)
window  → sound       TRUE     ✗ not detected (CE −0.001)
lights  ↔ lux         TRUE     ✗ not detected (CE +0.010; freezing lux made noul RISE)
door    → airflow     TRUE     ✗ not detected (CE +0.016, sham +0.019)

Probes (JEV prior beyond generator):
rain → humidity       ✗ no prior edge (CE −0.015)
no-people → no CO₂    ✗ NOT significant (CE +0.025, CI [−0.023,+0.074])   ← kills the Lane-2 story
lux ⇏ humidity        ✔ confirmed no hallucinated edge (CE −0.041 — JEV *more* tolerant than RF)
```

**Recall 3/11 (27%) against generator truth; precision 3/3 (100%).** JEV hallucinates no physics; it simply encodes very little of the air-chemistry layer.

## Honest Negatives (first-class findings)

1. **The Lane-2 "CO₂ taste" hypothesis is refuted in removal/injection form.** Lane 2's paper speculated the unexplained variance was things like "CO₂ rising with the window open and nobody home." We tested exactly this (P3: inject +150 ppm into an empty room; C3: freeze CO₂ under open window). **Neither is detected.** The raw noul drop for P3 (+0.058) is fully explained by the marginal size of the CO₂ change (RF-null +0.033, remainder CI crosses 0). JEV's rejection of that pattern — when it happens — is magnitude-driven, not coupling-driven.
2. **No psychrometrics.** JEV does not expect RH to fall when the room warms (CE +0.017, q = 0.16), nor does inverting it register (CE_inv = −0.006). The temp→humidity edge — real physics, present in every clean transition — is invisible to the judge.
3. **The mug edge is mostly focal-magnitude sensitivity, not coupling.** Sham-controlled: a median-size random mug jump (±~7 °C) yields CE 0.198, comparable to the inversion effect (0.165). JEV flags *implausible mug change*, not *mug-vs-room thermal inconsistency*, though the inversion's 55% gate-crossing rate shows the away-from-room-temp direction is special.
4. **Couplings explain only a slice of the Lane-2 residual.** Detected CE values (0.017–0.094) are modest against RF MAE 0.087 / residual σ ≈ 0.11. Only C5 approaches residual scale. The unexplained 20% is likely dominated by compound/context effects (multi-cause coherence, rate-vs-elapsed-time) rather than single-coupling checks.
5. **P2 (night-lights repair) could not run** — the generator never produces night + lights-off + bright lux, so the probe's active set is empty. Absence of substrate, not a result.
6. **Procedure controls held:** sham |CE| mean = 0.040, dominated by the mug and lux arms; 7 of 11 sham CIs include 0; the outliers (mug, PM2.5, lux dims) are flagged above. Drift check: Spearman 0.97 vs Lane-2 judgments, mean |Δnoul| = 0.014 — JEV is highly self-consistent across sessions (gate passed).

## Interpretation

JEV's room model is **bulk-energy-flow first**: the one coupling it checks hard is the most consequential heat-exchange channel (window↔temperature). It is *lenient about absence* (a cause without its consequence stays plausible) and *strict about contradiction* (a consequence moving the wrong way trips the gate). The air-quality layer (CO₂, PM2.5) — the coupling-rich chemistry — is judged almost purely by marginal magnitude. **JEV is a thermodynamic bouncer, not an indoor-air scientist.**

Practical consequences for the fleet: (a) marginal monitors (the RF at R²=0.81) capture nearly all of JEV's CO₂/PM judgment behavior — cheap filtering is safe there; (b) window/temp and mug dynamics deserve coupling-aware monitors; (c) the pinch threshold is a violation detector, not an incompleteness detector — absences will sail through unless magnitudes are also wrong.

## Artifacts

- `PRE-REG.md` (frozen before run) · `manifest.json` (sampled ids, seed 202) · `rf_null.pkl` (marginal-null, R²=0.806 held-out)
- `ablation-judgments.jsonl` (824 rows) · `ablation-results.json` (all stats) · `causal-map.png` · `run.log` / `analysis.log`
- Ramp receipt: 3/3 warm-up calls + 3 s pause before the measured batch (API lane; no local GPU timing exists to report — noted rather than fabricated).
