# LANE 2 — JEPA PREDICTS JEV'S JUDGMENT (meta-confidence)

**Date:** 2026-10-06 · **Judge:** `jev-1.13.0` via typesafe.ai `/v1/systemone` (`noul` question type) · **Data:** 500 synthetic room transitions (300 clean / 200 corrupted) · **Cost:** ~670k input / ~90k output tokens across 680 judge calls

## TL;DR

1. **Yes — JEV's judgment is highly predictable.** A random forest on raw transition features predicts JEV's noul score at **R² = 0.81, Spearman 0.90, MAE 0.087**. The judgment is "structured" in the technical sense: mostly a function of *how much* changed (scaled |Δ| L1 norm alone carries 63% of RF importance) plus a few physical-range features.
2. **JEV separates ground truth at AUC 0.91** (clean mean noul 0.77 vs corrupt 0.41; only 1/300 clean rows fell below 0.5; graded monotone by corruption severity: 0.50 → 0.40 → 0.35).
3. **The "surprise" is structured, not random.** 79% of low-noul (<0.5) corruptions fall in structured anomaly families; even the "random noise" rows are recognizable by *breadth* (6.6 dims shifted vs 1.55 for clean transitions). Corruption families have distinct signatures (dims-shifted-count × concentration).
4. **Raw prediction error and JEV judgment are ~orthogonal (ρ ≈ 0.015).** JEV catches what MSE tolerates (22 predictions output *negative lux*; MSE barely noticed, JEV scored them 0.14 mean noul) and tolerates what MSE punishes (large but structured misses score 0.56 mean noul).
5. **Self-consistency training (exp 3) is a leaky proxy.** With loss += λ·|g(pred) − g(actual)|, the world model drove the surrogate's judgment gap to ~0 (0.034 → 0.0002) — but **real-JEV scores on its predictions did not improve** (0.566 → 0.562 mean noul, within noise; λ=0.5 even slightly reduced the ≥0.7 fraction). A surrogate at R² ≈ 0.73 can be satisfied without moving the true judge. Distillation needs a much more faithful g before λ helps.

## Setup

**Discovery:** the TYPESAFE_AI_KEY is for typesafe.ai's SystemOne API — and "JEV" is literally their System One model (`jev-1.13.0`, released 2026-09-10). Its native `noul` question type returns P(yes) ∈ [0,1] — exactly the "noul_confidence" the lane asks for. No prompt-hacking a chat model needed; JEV is a purpose-built judge with a calibrated probability output.

**Room field (12 dims):** temp, humidity, lux, sound dB, CO₂, PM2.5, airflow, door-open fraction, occupants, mug temperature, mug x/y. Clean transitions are *cause-driven* (heater on/off, window open/close, person in/out, lights, mug moved, fresh coffee, vacuum) with passive physics always running (Newton cooling of mug & room toward outdoor baseline, CO₂ generation by occupants, RH drop on warming). Corruptions (7 modes × severity 1–3): random noise, global shift, object teleport, rate violation, range violation, impossible inversion, dimension swap. Each judged with 3 noul questions (valid / physical / causal) + 1 category choice. All 500 judgments + curves in `meta-results.json`.

## Experiment 1 — meta-predictor

| Model | R² | MAE | Spearman |
|---|---|---|---|
| Random forest (400 trees) | **0.806** | 0.087 | 0.899 |
| MLP 51→64→64→1 (GPU, 400 ep) | 0.729 | 0.098 | 0.849 |

**What it learned** (RF feature importances): f37 = L1 of scaled delta **0.63**, after-lux 0.061, ΔPM2.5 0.045, Δtemp 0.045, L2 0.028, Δhumidity 0.021. JEV's judgment is dominated by *gross change magnitude*, refined by light-level context and a couple of physically-salient deltas. The ~20% unexplained variance is where JEV's "taste" lives — physical-coupling violations (co2↑ with window open & nobody home) that don't show up in marginals.

Sub-score structure on ground truth: `causal` is the sharpest discriminator on clean-vs-corrupt means (0.775 vs 0.597) — i.e., "is there one coherent cause" is where corruption hurts most.

## Experiment 2 — residual analysis of the surprise (noul < 0.5)

112 low-noul rows: 111 corrupt, 1 clean. Per-mode structure of the surprise:

| mode | n | dims shifted | concentration | sign-consist. | mean noul |
|---|---|---|---|---|---|
| global_shift | 24 | **9.2** | 0.17 (broad) | 0.30 | 0.20 |
| random_noise | 19 | 6.6 | 0.21 | 0.36 | 0.18 |
| dim_swap | 26 | 4.0 | 0.52 | 0.37 | 0.16 |
| inversion | 2 | 4.5 | 0.29 | 0.55 | 0.47 |
| rate_violation | 19 | 2.9 | **0.54** (focal) | 0.58 | 0.34 |
| range_violation | 21 | 2.7 | **0.60** (focal) | 0.62 | 0.19 |
| *clean baseline* | 300 | *1.55* | — | *0.54* | *0.77* |

**Verdict: structured.** Two clean fingerprints: (a) *breadth* — corrupted transitions shift 2–6× more dimensions than real dynamics ever touch (clean evolutions are local: ~1.5 dims); (b) *focal vs broad profile* separates range/rate violations (few dims, huge magnitude) from global shifts (many dims, moderate). Nothing in the low-noul set looks like unstructured sensor noise — even "random noise" corruptions betray themselves by breadth. A "personality artifact" (all dims drifting together) would sit in the high-breadth / low-concentration corner, distinguishable from genuine room change by count alone.

**JEV's misses:** 29/200 corruptions scored ≥0.7 — overwhelmingly severity-1 (mild) cases (mean noul of sev-1 corruptions is 0.501, right at the fence). Its single clean false-negative (noul 0.49) was a 3-cause chain (fresh coffee + vacuum + person left) — legitimately a lot happening at once. Top meta-predictor residuals (JEV harsher than model by >0.3) concentrated in rate_violation/global_shift/random_noise — JEV reads *rates and couplings* the feature set underspecifies.

## Experiment 3 — self-consistency JEPA

World model f(before, causes, env) → after (MLP 35→128→128→12, GPU), trained on 240 clean transitions, loss = MSE + λ·|g(pred) − g(actual)| with g = the exp-1 MLP as a differentiable JEV surrogate (feature path rebuilt in torch; soft dimension-count for gradient flow).

| λ | test raw-err mean | surrogate judgment gap (train, end) |
|---|---|---|
| 0.0 | 0.937 | — |
| 0.25 | 0.934 | 0.0003 |
| 0.5 | 0.921 | 0.0002 |

The λ term is *satisfiable*: the world model gamed its internal judge to a ~0 gap (from 0.034) at negligible MSE cost. But real-JEV scores on λ-model predictions were flat-to-slightly-worse (mean noul 0.566 / 0.557 / 0.562 for λ = 0 / 0.25 / 0.5; fraction ≥0.7 fell 0.38 → 0.30). **Conclusion: g at R²=0.73 is a leaky proxy — it can be driven to zero error without moving the true judge.** Judgment-distillation needs a surrogate good enough that "fooling g" and "convincing JEV" coincide; here they decoupled. (Engineering note: the first implementation computed the judgment term on detached predictions — no gradient — which silently made all λ variants identical. The committed version is the fully-differentiable one.)

## Experiment 4 — what JEV catches that raw error misses

60 held-out test transitions; predictions from each λ judged by the real JEV (180 calls). **Spearman(raw_err, noul) ≈ 0.01–0.03 — orthogonal.**

- **High error, JEV-valid (14/60 at λ=0):** e.g. err 0.92, noul 0.85 — predicted 24.2°C vs actual 22.4°C, mug 0.5m off — every number physically sensible, just imprecise. *Structured but large change is still a valid room.*
- **Low error, JEV-invalid (9/60 at λ=0):** e.g. noul 0.12, category "unnatural" — raw L2 spread thinly across dims, but one lethal flaw: **predicted lux = −161**. MSE amortizes a range violation across twelve dims; JEV treats it as disqualifying. Across all predictions, the 22 with negative lux scored mean noul **0.14**.
- Predictions with err > 1.2 (large misses) still averaged noul 0.56 — large-but-plausible ≈ small-but-broken in raw error, wildly different in judgment.

## Answers to the brief

- **Fraction structurally valid vs random:** 54.4% of all 500 judged ≥0.7 (272), 22.4% below 0.5 (112). Of the low-noul surprises, **~79% are structured** (identifiable mode or systematic sign/concentration signature); effectively none is irreducible noise — even noise corruptions are recognizable by dimension-breadth.
- **What the meta-predictor learns:** gross scaled-change magnitude first (63% importance), then light context and a few physical deltas; the residual ~20% variance is JEV's rate/coupling sensitivity.
- **Meta-confidence verdict:** JEV's judgment is *predictable enough to distill a warning signal from* (RF OOF residuals flag exactly the rows where JEV sees coupled impossibilities), but *not yet faithful enough to train against* (exp 3). The practical lane-2 product is a cheap RF "expected judgment" filter that flags transitions a judge would question — not a loss term.

## Files

- `meta-results.json` — all 500 judgments (3 noul scores + category each), RF/MLP metrics + curves, exp2 residuals, exp3 curves, exp4 quadrants. 319 KB.
- `transitions.jsonl`, `judgments.jsonl`, `exp2-residuals.json`, `exp3-results.json`, `exp4-predictions-judged.json` — raw intermediates.
- `gen_transitions.py`, `judge_transitions.py`, `meta_predictor.py`, `jepa_train.py`, `analyze.py`, `common.py` — reproducible pipeline (system python for gen/judge; GPU venv for torch; all API scripts resumable).
- `nn-surrogate.pt`, `world-models.pt` — trained weights.

**Threats to validity:** single judge model (jev-1.13.0) with one fixed question phrasing; synthetic ground truth from my own physics generator (JEV's 0.91 AUC is against *my* corruption distribution); 60-sample exp4 quadrant counts are ±~6pp; the surrogate and world model share generator-induced structure, so exp 3's null result may be partly "same-data circularity" — but that cuts toward, not against, its conclusion (even with home-field structure, g wasn't faithful enough).
