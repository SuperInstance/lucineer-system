#!/usr/bin/env python3
"""DL1-REAL-JEPA step 2: train the MLP predictor on REAL dial latents.

Frozen per PRE-REG: MLP 14->64->7, weighted L1, q-rule mask (q<0.2),
10 seeds, persistence + mean-delta baselines, G1/G2 falsification gates.
GPU ramp receipt at start (>=3s warmup, >=1000 matmuls, RTX 4050).
Outputs: train-results.json, heldout-predictions.json
"""
import json, os, time
import numpy as np
import torch
import torch.nn as nn

HERE = os.path.dirname(os.path.abspath(__file__))
torch.manual_seed(0); np.random.seed(0)

# ---------------- GPU ramp receipt (PRE-REG §6) ----------------
dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
assert dev.type == "cuda", "GPU required (RTX 4050)"
info = torch.cuda.get_device_name(0)
t0 = time.time(); matmuls = 0; warm = torch.randn(1024, 1024, device=dev)
while time.time() - t0 < 3.0:
    for _ in range(50):
        warm = warm @ torch.randn(1024, 1024, device=dev) * 0.001 + warm * 0.999
        matmuls += 1
torch.cuda.synchronize()
RAMP = {"device": info, "warmup_s": round(time.time() - t0, 2),
        "matmuls": matmuls, "receipt": "PASS" if matmuls >= 1000 else "FAIL"}
print(f"[RAMP] {RAMP}")

PRIMARY = ["A", "D", "D-cold", "S1", "S2", "S3", "S4a", "S4b", "S5"]
TEST = ["D-cold", "S4b"]; TRAIN = [n for n in PRIMARY if n not in TEST]
W_LOSS = torch.tensor([1.0, 1.0, 0.5, 0.25, 0.25, 0.25, 0.25])
LAT_NAMES = ["v*proj", "log1p_kappa", "rho", "v2proj", "v3proj", "v4proj", "v5proj"]

z = np.load(os.path.join(HERE, "real_latents.npz"))
basis = z["basis"]  # 7x7, columns v*, v2..v7

def transitions(ch):
    """ch in {'A','B'} -> (X, Y, mask_q, night, seq_t, seq_t1, lat_t, lat_true)"""
    X, Y, Q, NT, ST, S1, LT, LY = [], [], [], [], [], [], [], []
    for n in PRIMARY:
        L = z[f"lat{ch}_{n}"]; S = z[f"seq{ch}_{n}"]
        for i in range(len(L) - 1):
            if S[i + 1] != S[i] + 1:      # consecutive speaks only
                continue
            x = np.concatenate([L[i], L[i] - (L[i - 1] if i > 0 and S[i - 1] == S[i] - 1
                                              else L[i])])
            # q-rule: motion on room subspace / total motion (truncated basis)
            d = L[i + 1][:5] - L[i][:5]   # projections v*..v5 (v6,v7 not logged)
            if i == 0 or S[i - 1] != S[i] - 1:
                d_prev = np.zeros(5)
            else:
                d_prev = L[i][:5] - L[i - 1][:5]
            dmu_room = basis[:, :4] @ d[:4]
            dmu_all = basis[:, :5] @ d
            dn_room = np.linalg.norm(basis[:, :4] @ d_prev[:4])
            dn_all = np.linalg.norm(basis[:, :5] @ d_prev)
            q = dn_room / max(dn_all, 1e-9)   # q of the EDGE motion
            X.append(x); Y.append(L[i + 1]); Q.append(q)
            NT.append(n); ST.append(int(S[i])); S1.append(int(S[i + 1]))
            LT.append(L[i]); LY.append(L[i + 1])
    return (np.array(X, np.float32), np.array(Y, np.float32),
            np.array(Q), NT, np.array(ST), np.array(S1),
            np.array(LT, np.float32), np.array(LY, np.float32))

def train_seed(Xtr, Ytr, Mtr, seed):
    torch.manual_seed(seed)
    net = nn.Sequential(nn.Linear(14, 64), nn.ReLU(), nn.Linear(64, 7)).to(dev)
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    Xt = torch.tensor(Xtr).to(dev); Yt = torch.tensor(Ytr).to(dev)
    Mt = torch.tensor(Mtr, dtype=torch.float32).to(dev)  # 1 keep, 0 mask
    w = W_LOSS.to(dev)
    best, best_state, patience = 1e18, None, 0
    for ep in range(4000):
        opt.zero_grad()
        loss = (Mt[:, None] * (net(Xt) - Yt).abs() * w).sum(1).mean()
        loss.backward(); opt.step()
        lv = float(loss)
        if lv < best - 1e-7:
            best, best_state, patience = lv, {k: v.detach().clone()
                                              for k, v in net.state_dict().items()}, 0
        else:
            patience += 1
            if patience >= 300:
                break
    net.load_state_dict(best_state)
    return net, best, ep + 1

def rmse_by_dim(pred, true):
    return np.sqrt(((pred - true) ** 2).mean(0))

def run(ch):
    X, Y, Q, NT, ST, S1, LT, LY = transitions(ch)
    tr = np.array([n in TRAIN for n in NT]); te = ~tr
    keep = (Q >= 0.2)
    print(f"\n[channel {ch}] transitions: train={tr.sum()} (kept {(tr&keep).sum()}, "
          f"masked {(tr&~keep).sum()}), test={te.sum()}")
    res = {"channel": ch, "n_train": int(tr.sum()), "n_train_kept": int((tr & keep).sum()),
           "n_test": int(te.sum()), "n_masked_train": int((tr & ~keep).sum())}
    # baselines (evaluated on ALL test transitions, unmasked — honest test dist)
    pers = LT[te]
    md = np.mean(Y[tr & keep] - LT[tr & keep], 0)
    meandelta = LT[te] + md
    seeds_pred = []
    for seed in range(10):
        net, bl, eps = train_seed(X[tr], Y[tr], keep[tr].astype(np.float32), seed)
        with torch.no_grad():
            p = net(torch.tensor(X[te]).to(dev)).cpu().numpy()
        seeds_pred.append(p)
        if seed == 0:
            torch.save(net.state_dict(), os.path.join(HERE, f"jepa_{ch}.pt"))
    P = np.stack(seeds_pred)  # 10 x n x 7
    Pm = P.mean(0); Ps = P.std(0)
    def gate(pred, name):
        r = rmse_by_dim(pred, Y[te])
        return {"model": name, "rmse_vstar": float(r[0]),
                "rmse_logkappa": float(r[1]), "rmse_all": [float(x) for x in r]}
    res["rmse"] = [gate(pers, "persistence"), gate(meandelta, "mean-delta"),
                   gate(Pm, "jepa-mean10")]
    res["jepa_seed_sd_vstar"] = float(Ps[:, 0].mean()); res["jepa_seed_sd_logkappa"] = float(Ps[:, 1].mean())
    g1_v = 1 - res["rmse"][2]["rmse_vstar"] / res["rmse"][0]["rmse_vstar"]
    g1_k = 1 - res["rmse"][2]["rmse_logkappa"] / res["rmse"][0]["rmse_logkappa"]
    res["G1"] = {"improve_vstar_pct": round(100 * g1_v, 2),
                 "improve_logkappa_pct": round(100 * g1_k, 2),
                 "gate_pass": bool(g1_v > 0.15 and g1_k > 0.15)}
    print(f"  persistence v* RMSE {res['rmse'][0]['rmse_vstar']:.4f} | "
          f"logκ {res['rmse'][0]['rmse_logkappa']:.4f}")
    print(f"  JEPA(10-seed) v* RMSE {res['rmse'][2]['rmse_vstar']:.4f} | "
          f"logκ {res['rmse'][2]['rmse_logkappa']:.4f}")
    print(f"  G1: v* {100*g1_v:+.1f}% logκ {100*g1_k:+.1f}% -> "
          f"{'PASS' if res['G1']['gate_pass'] else 'FALSIFIED'}")
    # per-transition predictions for JEV (seed-0 + persistence)
    preds = {"night": [n for n in np.array(NT)[te]],
             "seq_t": ST[te].tolist(), "seq_t1": S1[te].tolist(),
             "lat_t": LT[te].tolist(), "lat_true": Y[te].tolist(),
             "lat_pred_jepa": seeds_pred[0].tolist(),
             "lat_pred_pers": pers.tolist()}
    return res, preds

out = {"ramp": RAMP, "torch": torch.__version__, "date": "2026-10-06"}
resA, predA = run("A")
resB, predB = run("B")
out["channels"] = {"A_logged_cumulative": resA, "B_sliding16": resB}
json.dump(out, open(os.path.join(HERE, "train-results.json"), "w"), indent=1)
json.dump({"A": predA, "B": predB},
          open(os.path.join(HERE, "heldout-predictions.json"), "w"))
print("\n[OK] train-results.json + heldout-predictions.json")
