# The Judge's Physics: Causal Ablation of JEV's Room Model

**Lane DL2** · 2026-10-06 · pre-registered (`PRE-REG.md`) · 821 measured JEV calls, 0 failures · model `jev-1.13.0`

## Abstract

Lane 2 showed JEV's validity judgment (`noul`) is 81% predictable from marginal features, leaving ~20% variance attributed — speculatively — to sensitivity for physical couplings invisible in marginals. We tested that attribution causally. For 11 generator-true couplings in a synthetic room (window↔temperature, occupancy↔CO₂, psychrometrics, …) we removed (froze the follower) and inverted (moved it the wrong way) each coupling in clean transitions, judged the edited states with JEV, and subtracted the shift predicted by a retrained marginal-null random forest (R² = 0.806). The excess — the coupling effect, CE — maps JEV's implicit physics. **JEV encodes 3 of 11 true couplings (precision 3/3): window→temperature dominates (CE 0.094, q=0.0004), with room→mug (0.028, sham-confounded) and occupants→sound (0.017) far behind. JEV hallucinates no physics. Inversion effects dwarf removal effects (0.166, 0.165 for the top two), and 55% of mug-inversions fall below JEV's 0.45–0.50 pinch threshold — while removals essentially never flip the gate (≤5%). The Lane-2 "CO₂ taste" story is refuted: neither CO₂-rise-in-an-empty-room nor frozen-CO₂-under-open-window exceeds the marginal null. JEV's room model is sparse, thermodynamic, sign-aware, and lenient about absence — a filter for contradictions between causes and consequences, not a simulator that expects them.**

## 1. Background

- **Lane 2** (`jev-jepa-meta`): RF on 51 marginal features predicts JEV's noul at R² = 0.806 (L1-norm of scaled delta: 63% of importance). Residual ≈ 20%.
- **Lane 1** (`jev-jepa-bilateral`): JEV's noul is calibrated (ROC AUC 0.995 vs plausible/implausible), natural pinch threshold 0.45–0.50.

The residual was hypothesized to be coupling sensitivity — "CO₂ rising with the window open and nobody home." Hypotheses are cheap; this lane prices them.

## 2. Method (frozen in PRE-REG before any measured call)

**Data.** 300 clean transitions from Lane 2's generator (cause-driven physics: heaters, windows, occupants, lights, mug; ground-truth couplings known). Corrupted transitions excluded.

**Design.** 11 couplings C with leader→follower structure; arms on active sets (rules pre-registered; n = min(20, active), seed 202, ids frozen in `manifest.json`):

- **REMOVE**: freeze follower at its before-value (consequence goes missing; cause stays visible).
- **INVERT**: move follower against the physical expectation (same order of magnitude).
- **SHAM**: same follower-dim edit of median active magnitude, random sign, on inactive transitions (procedure control).
- **PROBES** P1–P4: couplings absent from the generator, to test JEV's prior beyond ground truth (rain→humidity, empty-room→no-CO₂-source, no-edge lux⇏humidity control).

**Judging.** Same-session paired baselines (every original re-judged fresh; Lane-2 judgments used only for a drift check: Spearman 0.97, mean |Δnoul| = 0.014 — gate passed). Three questions per call (valid, causal, category), identical wording to Lane 2. Ramp receipt: 3 warm-up calls discarded + 3 s pause; no local GPU timing exists in an API lane (reported, not fabricated).

**Estimand.** CE(C) = mean[noul_orig − noul_edited] − mean[RF_orig − RF_edited]. The RF (400 trees, seed 0, retrained on all 500 Lane-2 rows) sees every edit's marginal features but no couplings; its predicted shift is subtracted. Detection: 95% bootstrap CI (10k, seed 7) excludes 0 **and** BH-FDR q < 0.05 across the 11 couplings.

## 3. Results

### 3.1 The causal map

| Rank | Coupling | CE remove [95% CI] | q | CE invert | Sham CE | Verdict |
|---|---|---|---|---|---|---|
| 1 | window→temp | **+0.094** [+0.059, +0.135] | 0.0004 | +0.166 | +0.019 | **DETECTED**, sign-aware |
| 2 | heater→temp↑ | +0.051 [+0.006, +0.095] | 0.136 | +0.005 | +0.059 | not detected (n=14, underpowered) |
| 3 | room→mug | +0.028 [+0.009, +0.048] | 0.0499 | +0.165 | **+0.198** | borderline; sham-confounded |
| 4 | occupants→sound | +0.017 [+0.005, +0.031] | 0.0499 | +0.017 | −0.020 | **DETECTED**, small |
| 5 | temp→RH (psychro.) | +0.017 [+0.001, +0.035] | 0.164 | −0.006 | +0.008 | not detected |
| 6–11 | door→airflow, lights↔lux, window→PM2.5, window→sound, occ→CO₂, window→CO₂ | −0.007 … +0.016 (CIs cross 0) | ≥0.26 | ≤+0.036 | ≈0 | not detected |

Probes: rain→humidity CE −0.015 [−0.039, +0.010] — no prior edge. Empty-room CO₂ injection CE +0.025 [−0.023, +0.074], p = 0.42 — not significant. No-edge control (lux⇏humidity) CE −0.041 [−0.064, −0.021] — JEV confirmed *not* to hallucinate this edge (it is in fact more tolerant of the small RH shift than the marginal null expects).

**Against generator truth: recall 3/11, precision 3/3.**

### 3.2 Asymmetry: contradiction vs absence

Inversion ≫ removal everywhere the effect exists (C5: 0.166 vs 0.094; C7: 0.165 vs 0.028). Gate-crossing makes it vivid: mug-inversion sends 55% of states below noul 0.50 (35% below 0.45) and draws the study's only "unnatural" category calls (5%); window-temp inversion crosses 0.50 in 16%. **No removal arm exceeds 5% crossings.** The 0.45–0.50 pinch threshold of Lane 1 is a contradiction detector; withheld evidence does not trip it.

### 3.3 The marginal-null correction matters

For C5-remove, the RF predicts noul should *rise* 0.028 (freezing temp shrinks L1, and L1 is 63% of the RF); JEV instead *drops* 0.066. Raw Δnoul would have understated JEV's coupling weight by 3×. Conversely for P4 (no-edge control) the RF over-predicts the penalty for a +5 RH shift; the negative CE is the RF's error, not JEV's preference. Excess-over-null is the only honest estimand here.

### 3.4 What the residual is not

The refuted story: Lane 2's residual-variance narrative centered on air-chemistry couplings (CO₂ with window/nobody-home). Tested directly (P3, C2, C3): all null. Detected couplings are thermal/acoustic. And their CEs (≤0.094, ≈ 0.9σ of the residual) cannot alone account for ~20% unexplained variance — the residual is plausibly compound-coherence and rate-vs-elapsed-time context, which single-edge ablation cannot reach (see §5).

## 4. JEV's implicit physics, stated plainly

1. **Sparse.** Three edges, one dominant. The air-quality layer has no edges JEV checks.
2. **Thermodynamic, not chemical.** The single hard check is the highest-power energy channel (window↔heat). Psychrometrics (temp→RH), though present in *every* clean transition, are invisible.
3. **Sign-aware.** Wrong-way motion is punished 2–6× more than missing motion.
4. **Lenient to absence, strict to contradiction.** Causes without consequences pass; consequences against causes trip the gate.
5. **No hallucinated physics.** Every detected edge is generator-true; probes for prior-beyond-truth edges are negative.

## 5. Limitations

- Single-coupling ablation cannot see higher-order interactions (e.g., "rate vs elapsed_minutes" or multi-cause coherence) — likely where much of the residual lives.
- C7's evidence is discountable: the mug-dim sham (CE 0.198) shows large focal edits are penalized well beyond RF-null regardless of coupling.
- C11 is a credible near-miss under power (CI excludes 0; q = 0.136 at n = 14); a confirmatory run at n ≥ 40 is the obvious follow-up.
- Generator circularity (Lane 1's caveat) is inverted here in our favor: the generator supplies *known-false* probe edges, but JEV's notion of physics could differ from real-room physics in ways this substrate cannot reveal.
- Bootstrap CIs are transition-level; JEV's per-call stochasticity is small (drift check mean |Δ| = 0.014) but nonzero.

## 6. Implications

For the fleet: marginal monitors suffice for CO₂/PM channels (JEV judges them magnitude-only); window/temp and mug trajectories need coupling-aware residual monitors; the pinch gate should be positioned as a **violation** tripwire — do not expect it to catch silent failure modes where an expected change simply fails to happen. For Lane 3 (anti-collapse): the judgement layer's physics priors are weak enough that a world model will not be *rewarded* for encoding air-chemistry couplings — only thermal exchange — which predicts exactly the collapse pattern Lane 3 observed.

## Artifacts

`PRE-REG.md`, `manifest.json`, `ablation-judgments.jsonl` (824 rows), `ablation-results.json`, `rf_null.pkl`, `causal-map.png`, `run.log`, `analysis.log`.
