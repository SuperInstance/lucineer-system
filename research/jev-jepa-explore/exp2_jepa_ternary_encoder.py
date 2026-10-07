#!/usr/bin/env python3
"""Exp 2 — JEPA as ternary encoder: ternary manifold learning (GPU torch).

Question: does {-1,0,+1}^9 (the JEPA dial alphabet, ternarized) sit on a
SMOOTH low-dimensional manifold? Train tiny autoencoders with continuous
latents of dim k < 9, decode back to ternary per-dim, measure error +
geometry (Hamming distance vs latent Euclidean distance).

If decode error is low at small k, the ternary cube has a smooth geometry
a continuous JEPA latent can carry — the bridge between the two worlds.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = 9
SEED = 2718


def ramp_and_warmup():
    """INSTRUMENT-01: 0.6s sustained synced load BEFORE any measurement."""
    import torch
    a = torch.randn(2048, 2048, device="cuda")
    torch.cuda.synchronize()
    import time
    t0 = time.time()
    while time.time() - t0 < 0.6:
        b = a @ a
        torch.cuda.synchronize()
    ms = (time.time() - t0) * 1000
    return {"warmup_ms": round(ms, 1), "device": torch.cuda.get_device_name(0)}


def ternary_decode(z):
    """Per-dim nearest ternary: z<-0.5 -> -1, |z|<=0.5 -> 0, z>0.5 -> +1."""
    return np.where(z > 0.5, 1, np.where(z < -0.5, -1, 0))


def train_ae(Xtr, Xte, k, seed, epochs=400, lr=1e-2):
    import torch
    import torch.nn as nn
    torch.manual_seed(seed)
    dev = "cuda"
    enc = nn.Sequential(nn.Linear(D, 32), nn.GELU(), nn.Linear(32, k)).to(dev)
    dec = nn.Sequential(nn.Linear(k, 32), nn.GELU(), nn.Linear(32, D)).to(dev)
    opt = torch.optim.Adam(list(enc.parameters()) + list(dec.parameters()), lr=lr)
    xt = torch.tensor(Xtr, dtype=torch.float32, device=dev)
    lossf = nn.MSELoss()
    for ep in range(epochs):
        opt.zero_grad()
        out = dec(enc(xt))
        loss = lossf(out, xt)
        loss.backward()
        opt.step()
    with torch.no_grad():
        Xte_t = torch.tensor(Xte, dtype=torch.float32, device=dev)
        lat = enc(Xte_t).cpu().numpy()
        rec = dec(torch.tensor(lat, dtype=torch.float32, device=dev)).cpu().numpy()
    return lat, rec


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    return float((rx * ry).sum() / np.sqrt((rx ** 2).sum() * (ry ** 2).sum() + 1e-12))


def eval_run(lat, rec, Xte):
    pred = ternary_decode(rec)
    trit_err = float((pred != Xte).mean())
    # geometry: subsample pairs, Hamming(x,y) vs ||lat(x)-lat(y)||
    rng = np.random.default_rng(7)
    n = len(Xte)
    i = rng.integers(0, n, 800); j = rng.integers(0, n, 800)
    keep = i != j
    ham = (Xte[i[keep]] != Xte[j[keep]]).sum(axis=1)
    euc = np.linalg.norm(lat[i[keep]] - lat[j[keep]], axis=1)
    rho = spearman(ham.astype(float), euc)
    return trit_err, rho


def main():
    import torch
    receipt = ramp_and_warmup()
    rng = np.random.default_rng(SEED)
    # corpus: all ternary states of dim 9 is 19683 — sample train/test
    states = rng.integers(0, 3, size=(5000, D)) - 1  # uniform {-1,0,+1}^9
    Xtr, Xte = states[:3000].astype(np.float32), states[3000:].astype(np.float32)

    runs = []
    for k in (1, 2, 3, 4, 5):
        for seed in range(20):
            lat, rec = train_ae(Xtr, Xte, k, SEED + seed)
            # decode error vs identity baseline
            terr, rho = eval_run(lat, rec, Xte.astype(int))
            runs.append({"k": k, "seed": seed, "trit_err": terr,
                         "hamming_euclid_spearman": rho})
            print("k=%d seed=%2d trit_err=%.4f rho=%.3f" % (k, seed, terr, rho), flush=True)
    # random-projection baseline per k (no learning)
    base = []
    for k in (1, 2, 3, 4, 5):
        Rp = rng.standard_normal((D, k)).astype(np.float32) / np.sqrt(k)
        lat = Xte @ Rp
        pred = ternary_decode(Xte @ (Rp @ np.linalg.pinv(Rp)))  # best linear decode
        base.append({"k": k, "baseline": "random_proj",
                     "trit_err": float((pred != Xte).mean())})

    agg = {}
    for k in (1, 2, 3, 4, 5):
        rs = [r for r in runs if r["k"] == k]
        agg[k] = {"trit_err_mean": float(np.mean([r["trit_err"] for r in rs])),
                  "trit_err_min": float(np.min([r["trit_err"] for r in rs])),
                  "rho_mean": float(np.mean([r["hamming_euclid_spearman"] for r in rs]))}
    g1 = agg[4]["trit_err_min"] <= 0.02
    g2 = agg[4]["rho_mean"] >= 0.90
    g3 = agg[5]["trit_err_min"] <= agg[3]["trit_err_min"]  # no cliff
    out = {
        "experiment": "exp2 JEPA ternary encoder (ternary manifold learning)",
        "n_runs": len(runs), "d": D,
        "gpu_ramp_receipt": receipt,
        "aggregate_by_k": agg, "random_proj_baseline": base,
        "identity_trit_err": 0.0,
        "gates": {"G1_k4_trit_err_le_0.02": {"value": agg[4]["trit_err_min"], "pass": g1},
                  "G2_k4_rho_ge_0.90": {"value": agg[4]["rho_mean"], "pass": g2},
                  "G3_no_cliff": {"value": [agg[5]["trit_err_min"], agg[3]["trit_err_min"]], "pass": g3}},
        "runs": runs,
        "verdict": "SMOOTH-GEOMETRY-PASS" if (g1 and g2 and g3) else "SMOOTH-GEOMETRY-FAIL",
    }
    with open(os.path.join(HERE, "exp2_out.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote exp2_out.json — verdict:", out["verdict"])


if __name__ == "__main__":
    main()
