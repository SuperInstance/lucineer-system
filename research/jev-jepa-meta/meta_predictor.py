#!/usr/bin/env python3
"""Experiment 1: meta-predictor — learn to predict JEV's noul judgment.

Random forest baseline, then a small torch MLP (GPU) that doubles as the
differentiable JEV surrogate g() for self-consistency JEPA training (exp 3).
Outputs: meta-summary.json, nn-surrogate.pt, curves in meta-results.json
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_transitions, load_judgments, features, N_FEATS

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    recs = load_transitions()
    jd = load_judgments()
    assert len(jd) == len(recs), f"judgments {len(jd)} != recs {len(recs)}"

    X = np.stack([features(r) for r in recs])
    y_valid = np.array([jd[r["id"]]["raw"]["valid"]["noul"] for r in recs])
    y_phys = np.array([jd[r["id"]]["raw"]["physical"]["noul"] for r in recs])
    y_causal = np.array([jd[r["id"]]["raw"]["causal"]["noul"] for r in recs])
    clean = np.array([r["clean"] for r in recs])
    ids = np.array([r["id"] for r in recs])

    idx = np.arange(len(recs))
    tr, te = train_test_split(idx, test_size=0.2, random_state=7, stratify=clean)
    print(f"X={X.shape}  train={len(tr)} test={len(te)}  N_FEATS={N_FEATS}")

    summary = {"n": len(recs), "n_feats": N_FEATS,
               "noul_stats": {"valid": [float(y_valid.mean()), float(y_valid.std())],
                              "physical": [float(y_phys.mean()), float(y_phys.std())],
                              "causal": [float(y_causal.mean()), float(y_causal.std())]}}

    # ---------- separability of JEV by ground truth ----------
    from scipy.stats import mannwhitneyu
    u = mannwhitneyu(y_valid[clean], y_valid[~clean])
    summary["jev_gt_separation"] = {
        "noul_clean_mean": float(y_valid[clean].mean()),
        "noul_corrupt_mean": float(y_valid[~clean].mean()),
        "auc": float(u.statistic / (clean.sum() * (~clean).sum())),
        "valid_lt_0.5_clean_frac": float((y_valid[clean] < 0.5).mean()),
        "valid_lt_0.5_corrupt_frac": float((y_valid[~clean] < 0.5).mean()),
    }
    print("JEV vs ground truth:", json.dumps(summary["jev_gt_separation"], indent=1))

    # ---------- random forest ----------
    rf = RandomForestRegressor(n_estimators=400, random_state=0, n_jobs=-1)
    t0 = time.time()
    rf.fit(X[tr], y_valid[tr])
    rf_pred = rf.predict(X[te])
    rf_r2 = 1 - np.sum((rf_pred - y_valid[te])**2) / np.sum((y_valid[te] - y_valid[te].mean())**2)
    rf_sp = spearmanr(rf_pred, y_valid[te]).statistic
    summary["random_forest"] = {
        "r2": float(rf_r2), "mae": float(np.abs(rf_pred - y_valid[te]).mean()),
        "spearman": float(rf_sp), "fit_s": round(time.time() - t0, 2),
        "top_features": sorted(
            zip([f"f{i}" for i in range(N_FEATS)], rf.feature_importances_.round(4).tolist()),
            key=lambda kv: -kv[1])[:12],
    }
    print("RF:", json.dumps(summary["random_forest"], indent=1))

    # ---------- torch MLP ----------
    import torch, torch.nn as nn
    dev = torch.device("cuda")
    # GPU ramp receipt (INSTRUMENT-01): sustained load before any timing
    _w = torch.randn(2048, 2048, device=dev)
    for _ in range(80):
        _w = _w @ _w * 0.001
    torch.cuda.synchronize()
    ramp = {"warmup_matmuls": 80, "note": "0.3s+ sustained load before training"}

    mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-8
    Xt = torch.tensor((X - mu) / sd, dtype=torch.float32)
    yt = torch.tensor(y_valid, dtype=torch.float32).unsqueeze(1)
    trt, tet = torch.tensor(tr), torch.tensor(te)

    class MLP(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(N_FEATS, 64), nn.GELU(),
                nn.Linear(64, 64), nn.GELU(),
                nn.Linear(64, 1), nn.Sigmoid())
        def forward(self, x):
            return self.net(x)

    torch.manual_seed(0)
    m = MLP().to(dev)
    opt = torch.optim.AdamW(m.parameters(), lr=2e-3, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=400)
    lossf = nn.MSELoss()
    curve = []
    te_dev = Xt[tet].to(dev)
    for ep in range(400):
        m.train()
        perm = trt[torch.randperm(len(trt))]
        ep_loss = 0.0
        for chunk in torch.split(perm, 64):
            xb, yb = Xt[chunk].to(dev), yt[chunk].to(dev)
            opt.zero_grad()
            loss = lossf(m(xb), yb)
            loss.backward()
            opt.step()
            ep_loss += float(loss) * len(chunk)
        sched.step()
        if (ep + 1) % 10 == 0:
            m.eval()
            with torch.no_grad():
                pv = m(te_dev).squeeze(1).cpu().numpy()
            r2 = 1 - np.sum((pv - y_valid[te])**2) / np.sum((y_valid[te] - y_valid[te].mean())**2)
            curve.append({"epoch": ep + 1, "train_mse": ep_loss / len(trt),
                          "val_mse": float(np.mean((pv - y_valid[te])**2)), "val_r2": float(r2)})
    m.eval()
    with torch.no_grad():
        pv = m(te_dev).squeeze(1).cpu().numpy()
    nn_r2 = curve[-1]["val_r2"]
    summary["mlp"] = {
        "r2": float(nn_r2),
        "mae": float(np.abs(pv - y_valid[te]).mean()),
        "spearman": float(spearmanr(pv, y_valid[te]).statistic),
        "epochs": 400, "hidden": 64, "gpu_ramp": ramp,
        "curve_every10": curve,
    }
    print("MLP final r2=%.3f mae=%.3f sp=%.3f" %
          (nn_r2, summary["mlp"]["mae"], summary["mlp"]["spearman"]))

    torch.save({"state_dict": m.state_dict(), "mu": mu, "sd": sd, "n_feats": N_FEATS},
               os.path.join(HERE, "nn-surrogate.pt"))

    json.dump(summary, open(os.path.join(HERE, "meta-summary.json"), "w"), indent=1)
    print("saved meta-summary.json + nn-surrogate.pt")

if __name__ == "__main__":
    main()
