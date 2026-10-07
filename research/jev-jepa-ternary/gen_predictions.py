#!/usr/bin/env python3
"""JEV-JEPA-ternary lane 3 — prediction generator.

Generates 200 JEPA-like predictions: each item is a predicted latent
TRAJECTORY (T=10 steps, scalar latent channel) plus its hidden ground-truth
actual trajectory. Derived scalars per trajectory:

  v*  = mean(x)                       -- predicted level
  kappa = linfit slope of x over t    -- increasing/decreasing trend
  coh  = coherence(second half) - coherence(first half)
        where coherence(h) = |mean of unit-signed deltas in h|
        -- is the trajectory becoming more internally coherent (+), stable (0),
           or less coherent (-) over its horizon

Ground truth construction: hidden regime (level_shift, trend, coh_dyn) each in
{-1,0,+1}; actual built from regime; prediction = actual + fidelity noise.
~15% of items are BROKEN (scrambled or regime-flipped) to give the JEV filter
something to catch (curl1 broken-phase methodology, seed 13 scrambled latents).

Seeded, stdlib+numpy only. Output: predictions.json
"""
import json
import numpy as np

SEED = 2718
N = 200
T = 10
BROKEN_FRAC = 0.15

rng = np.random.default_rng(SEED)

items = []
for i in range(N):
    # --- hidden regime ------------------------------------------------
    level_shift = int(rng.choice([-1, 0, 1], p=[0.30, 0.40, 0.30]))   # v* direction
    trend = int(rng.choice([-1, 0, 1], p=[0.25, 0.50, 0.25]))         # kappa direction
    coh_dyn = int(rng.choice([-1, 0, 1], p=[0.25, 0.50, 0.25]))       # coherence direction

    broken = bool(rng.random() < BROKEN_FRAC)
    broken_kind = None
    if broken:
        broken_kind = str(rng.choice(["scrambled", "regime_flip", "flatlined"], p=[0.4, 0.4, 0.2]))

    base = rng.normal(0.0, 0.35)          # starting latent level
    t = np.arange(T, dtype=float)

    # --- actual trajectory ---------------------------------------------
    # level shift: offset growing over the window
    lvl = base + level_shift * 0.12 * (t / (T - 1))
    # trend: linear ramp; curvature: trend strengthens in 2nd half
    trend_line = trend * 0.15 * t
    # coherence dynamics: low-coherence noise shrinks (coh_dyn=+1) or grows (-1)
    noise_scale_1 = 0.05 if coh_dyn >= 0 else 0.16
    noise_scale_2 = 0.02 if coh_dyn == 1 else (0.16 if coh_dyn == -1 else 0.05)
    half = T // 2
    noise = np.concatenate([
        rng.normal(0, noise_scale_1, half),
        rng.normal(0, noise_scale_2, T - half),
    ])
    actual = lvl + trend_line + noise

    # --- prediction -----------------------------------------------------
    if broken and broken_kind == "scrambled":
        # sick predictor: seed-13 scrambled latents (curl1 style)
        pred = rng.normal(0.0, 0.5, T)
    elif broken and broken_kind == "regime_flip":
        lvl_p = base - level_shift * 0.12 * (t / (T - 1))
        pred = lvl_p - trend * 0.15 * t + rng.normal(0, noise_scale_2, T)
    elif broken and broken_kind == "flatlined":
        pred = np.full(T, base) + rng.normal(0, 0.02, T)
    else:
        # fidelity noise: 0 (perfect) .. 0.18 (sloppy)
        fidelity = float(rng.uniform(0.0, 0.18))
        pred = actual + rng.normal(0, fidelity, T)

    items.append({
        "id": i,
        "regime": {"level_shift": level_shift, "trend": trend, "coh_dyn": coh_dyn},
        "broken": broken,
        "broken_kind": broken_kind,
        "actual": [round(float(x), 4) for x in actual],
        "pred": [round(float(x), 4) for x in pred],
    })

# --- derived scalars ---------------------------------------------------

def scalars(x):
    x = np.asarray(x, dtype=float)
    t = np.arange(len(x), dtype=float)
    v_star = float(np.mean(x))
    kappa = float(np.cov(t, x, bias=True)[0, 1] / np.var(t))
    d = np.sign(np.diff(x))
    def coh(seg):
        s = seg[seg != 0]
        return float(np.abs(np.mean(s))) if len(s) else 0.0
    half = len(d) // 2
    coh_delta = float(coh(d[half:]) - coh(d[:half]))
    return {"v_star": round(v_star, 4), "kappa": round(kappa, 4),
            "coh": round(coh_delta, 4)}


for it in items:
    it["sc_pred"] = scalars(it["pred"])
    it["sc_actual"] = scalars(it["actual"])
    # continuous error: 1 - cosine similarity (curl1 convention)
    a = np.asarray(it["actual"]); p = np.asarray(it["pred"])
    cos = float(np.dot(a, p) / (np.linalg.norm(a) * np.linalg.norm(p) + 1e-12))
    it["err_cos"] = round(1.0 - cos, 4)

with open("predictions.json", "w") as f:
    json.dump({"seed": SEED, "n": N, "T": T, "broken_frac": BROKEN_FRAC,
               "items": items}, f, indent=1)

# quick sanity
sc_p = np.array([[it["sc_pred"]["v_star"], it["sc_pred"]["kappa"], it["sc_pred"]["coh"]] for it in items])
sc_a = np.array([[it["sc_actual"]["v_star"], it["sc_actual"]["kappa"], it["sc_actual"]["coh"]] for it in items])
err = np.array([it["err_cos"] for it in items])
print("pred scalar ranges: v* [%.2f, %.2f]  k [%.2f, %.2f]  coh [%.2f, %.2f]" %
      (sc_p[:, 0].min(), sc_p[:, 0].max(), sc_p[:, 1].min(), sc_p[:, 1].max(),
       sc_p[:, 2].min(), sc_p[:, 2].max()))
print("axis corr pred-vs-actual: v* %.3f  k %.3f  coh %.3f" %
      tuple(np.corrcoef(sc_p[:, j], sc_a[:, j])[0, 1] for j in range(3)))
print("err_cos: clean mean %.3f  broken mean %.3f" %
      (err[[k for k, it in enumerate(items) if not it["broken"]]].mean(),
       err[[k for k, it in enumerate(items) if it["broken"]]].mean()))
print("n broken:", sum(it["broken"] for it in items))
