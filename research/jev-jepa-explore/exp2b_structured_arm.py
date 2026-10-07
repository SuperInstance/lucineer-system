#!/usr/bin/env python3
"""Exp 2b — POST-HOC arm: structured ternary manifold (labeled post-hoc).

Exp2 falsified smooth geometry on the UNIFORM {-1,0,+1}^9 cube (err ~0.20 at
k=4, rho ~0.38). Post-hoc question: the JEPA dial alphabet is never uniformly
visited — rooms concentrate mass on a small reachable set. Does STRUCTURED
ternary data (transition-kernel fields ternarized, deadband mass at 0) have
the smooth geometry the uniform cube lacks?
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 2718
D = 9


def ternarize(x, thr=0.15):
    return np.where(x > thr, 1, np.where(x < -thr, -1, 0))


def make_structured(n, noise=0.3, seed=SEED):
    import sys
    sys.path.insert(0, "/home/eileen/projects/quilt-gpu-lab")
    from tools.transition_kernel import make_tripartite_transitions
    fb, corr, _, fa, _ = make_tripartite_transitions(
        n_agents=8, field_dim=D, n_steps=n, push=0.5, noise=noise, seed=seed)
    states = np.vstack([ternarize(fb), ternarize(fa), corr])
    return states


def ternary_decode(z):
    return np.where(z > 0.5, 1, np.where(z < -0.5, -1, 0))


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    return float((rx * ry).sum() / np.sqrt((rx ** 2).sum() * (ry ** 2).sum() + 1e-12))


def train_ae(Xtr, Xte, k, seed, epochs=400):
    import torch
    import torch.nn as nn
    torch.manual_seed(seed)
    dev = "cuda"
    enc = nn.Sequential(nn.Linear(D, 32), nn.GELU(), nn.Linear(32, k)).to(dev)
    dec = nn.Sequential(nn.Linear(k, 32), nn.GELU(), nn.Linear(32, D)).to(dev)
    opt = torch.optim.Adam(list(enc.parameters()) + list(dec.parameters()), lr=1e-2)
    xt = torch.tensor(Xtr, dtype=torch.float32, device=dev)
    lossf = nn.MSELoss()
    for ep in range(epochs):
        opt.zero_grad(); loss = lossf(dec(enc(xt)), xt); loss.backward(); opt.step()
    with torch.no_grad():
        Xte_t = torch.tensor(Xte, dtype=torch.float32, device=dev)
        lat = enc(Xte_t).cpu().numpy()
        rec = dec(torch.tensor(lat, dtype=torch.float32, device=dev)).cpu().numpy()
    return lat, rec


def main():
    import time
    import torch
    # INSTRUMENT-01 warmup
    a = torch.randn(2048, 2048, device="cuda"); torch.cuda.synchronize()
    t0 = time.time()
    while time.time() - t0 < 0.6:
        b = a @ a; torch.cuda.synchronize()

    runs = []
    for noise in (0.1, 0.3, 0.7):
        S = make_structured(4000, noise=noise, seed=SEED + int(noise * 10))
        # dedupe — structured data lives on a SMALL reachable set
        uniq = np.unique(S, axis=0)
        rng = np.random.default_rng(SEED)
        rng.shuffle(uniq)
        ntr = min(2000, int(0.75 * len(uniq)))
        Xtr, Xte = uniq[:ntr].astype(np.float32), uniq[ntr:].astype(np.float32)
        for k in (2, 3, 4, 5):
            for seed in range(10):
                lat, rec = train_ae(Xtr, Xte, k, SEED + seed)
                pred = ternary_decode(rec)
                terr = float((pred != Xte.astype(int)).mean())
                i = rng.integers(0, len(Xte), 600); j = rng.integers(0, len(Xte), 600)
                keep = i != j
                ham = (Xte[i[keep]].astype(int) != Xte[j[keep]].astype(int)).sum(1)
                euc = np.linalg.norm(lat[i[keep]] - lat[j[keep]], axis=1)
                rho = spearman(ham.astype(float), euc)
                runs.append({"noise": noise, "k": k, "seed": seed,
                             "unique_states": int(len(uniq)),
                             "trit_err": terr, "rho": rho})
                print("noise=%.1f k=%d seed=%2d uniq=%5d err=%.4f rho=%.3f"
                      % (noise, k, seed, len(uniq), terr, rho), flush=True)
    out = {
        "experiment": "exp2b POST-HOC structured ternary manifold",
        "post_hoc": True,
        "note": "uniform-cube arm failed (exp2); this arm asks whether "
                "STRUCTURED ternary (reachable set of the transition kernel, "
                "deadband mass at 0) is smooth.",
        "runs": runs,
    }
    agg = {}
    for noise in (0.1, 0.3, 0.7):
        for k in (2, 3, 4, 5):
            rs = [r for r in runs if r["noise"] == noise and r["k"] == k]
            agg["noise%.1f_k%d" % (noise, k)] = {
                "unique_states": rs[0]["unique_states"],
                "trit_err_min": min(r["trit_err"] for r in rs),
                "trit_err_mean": float(np.mean([r["trit_err"] for r in rs])),
                "rho_mean": float(np.mean([r["rho"] for r in rs]))}
    out["aggregate"] = agg
    with open(os.path.join(HERE, "exp2b_out.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote exp2b_out.json")


if __name__ == "__main__":
    main()
