#!/usr/bin/env python3
"""Experiments 3 + 4.

Exp 3 — self-consistency JEPA: room-state predictor f(before, cause, env) -> after,
trained with loss = MSE(pred, actual) + lambda * |g(pred) - g(actual)| where g is the
trained MLP surrogate of JEV's judgment (nn-surrogate.pt). lambda in {0, 0.25, 0.5}.

Exp 4 — JEV vs raw error: 60 held-out test transitions, predictions from each lambda
variant judged by the real JEV API; quadrant analysis vs raw prediction error.
"""
import json, os, sys, copy
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (load_transitions, features, svec, env_feats, DIMS, VAL, SIG,
                   state_from_vec)
import judge_transitions as jt

import torch, torch.nn as nn

HERE = os.path.dirname(os.path.abspath(__file__))
dev = torch.device("cuda")

CAUSES = ["heater_turned_on", "heater_turned_off", "window_opened", "window_closed",
          "person_entered", "person_left", "lights_turned_on", "lights_turned_off",
          "mug_moved", "fresh_coffee", "vacuum_cleaner_ran"]
CEN = np.array([22.0, 42, 300, 35, 700, 10, 0.3, 0.4, 1.5, 50, 2.5, 2.0])

def cause_oh(rec):
    v = np.zeros(len(CAUSES))
    for c in rec["causes"]:
        v[CAUSES.index(c)] = 1.0
    return v

def jepa_input(rec):
    return np.concatenate([(svec(rec["before"]) - CEN) / VAL, cause_oh(rec), env_feats(rec)])

CAUSE_DIM = len(CAUSES)
ENV_N = 12  # outdoor_temp, outdoor_pm25, elapsed + 5 tod + 4 scene

class WorldModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(12 + CAUSE_DIM + ENV_N, 128), nn.GELU(),
            nn.Linear(128, 128), nn.GELU(),
            nn.Linear(128, 12))
    def forward(self, x):
        return self.net(x)

class Surrogate(nn.Module):
    def __init__(self, n_feats):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_feats, 64), nn.GELU(),
            nn.Linear(64, 64), nn.GELU(),
            nn.Linear(64, 1), nn.Sigmoid())
    def forward(self, x):
        return self.net(x)

def load_g():
    ck = torch.load(os.path.join(HERE, "nn-surrogate.pt"), map_location=dev, weights_only=True)
    g = Surrogate(ck["n_feats"]).to(dev)
    g.load_state_dict(ck["state_dict"])
    g.eval()
    for p in g.parameters():
        p.requires_grad_(False)
    mu = ck["mu"].to(dev).float(); sd = ck["sd"].to(dev).float()
    def score(rec, after_vec):
        f = features(rec, after_state={d: float(after_vec[i]) for i, d in enumerate(DIMS)})
        return float(g((torch.tensor(f, dtype=torch.float32, device=dev) - mu) / sd))
    return g, mu, sd, score

def train_variant(recs_tr, ytr, lam, gn, seed=0):
    torch.manual_seed(seed)
    m = WorldModel().to(dev)
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=400)
    X = torch.tensor(np.stack([jepa_input(r) for r in recs_tr]), dtype=torch.float32, device=dev)
    Y = torch.tensor(ytr, dtype=torch.float32, device=dev)
    # differentiable feature path for the surrogate g:
    # feats = [b_norm(12), a_norm(12), d_scaled(12), l2, l1, soft_nshift, env(12)]
    vs = torch.tensor(VAL / SIG, dtype=torch.float32, device=dev)          # VAL/SIG
    dc = torch.tensor(np.stack([(CEN - svec(r["before"])) / SIG for r in recs_tr]),
                      dtype=torch.float32, device=dev)                      # (CEN-vb)/SIG
    bn = torch.tensor(np.stack([(svec(r["before"]) - CEN) / VAL for r in recs_tr]),
                      dtype=torch.float32, device=dev)
    envt = torch.tensor(np.stack([env_feats(r) for r in recs_tr]),
                        dtype=torch.float32, device=dev)
    with torch.no_grad():
        fa = torch.tensor(np.stack([features(r) for r in recs_tr]),
                          dtype=torch.float32, device=dev)
        g_act = gn(fa).squeeze(1)
    curve = []
    for ep in range(400):
        m.train()
        perm = torch.randperm(len(X), device=dev)
        ep_pred, ep_jud = 0.0, 0.0
        for chunk in torch.split(perm, 32):
            xb, yb = X[chunk], Y[chunk]
            opt.zero_grad()
            pred = m(xb)
            mse = ((pred - yb) ** 2).mean()
            loss = mse
            if lam > 0:
                d = pred[None if False else slice(None)] * vs[None, :] + dc[chunk]
                l2 = d.norm(dim=1, keepdim=True)
                l1 = d.abs().sum(dim=1, keepdim=True)
                nshift = torch.sigmoid(10 * (d.abs() - 1.0)).sum(dim=1, keepdim=True)
                feats = torch.cat([bn[chunk], pred, d, l2, l1, nshift, envt[chunk]], dim=1)
                jud = (gn(feats).squeeze(1) - g_act[chunk]).abs().mean()
                loss = mse + lam * jud
                ep_jud += float(jud) * len(chunk)
            loss.backward()
            opt.step()
            ep_pred += float(mse) * len(chunk)
        sched.step()
        if (ep + 1) % 20 == 0:
            curve.append({"epoch": ep + 1, "train_mse": ep_pred / len(X),
                          "train_judgment_gap": ep_jud / len(X)})
    return m, curve

def raw_err(pred_v, actual_v):
    return float(np.linalg.norm((pred_v - actual_v) / VAL))

def main():
    recs = [r for r in load_transitions() if r["clean"]]
    rng = np.random.default_rng(3)
    idx = rng.permutation(len(recs))
    tr_i, te_i = idx[:240], idx[240:]
    recs_tr = [recs[i] for i in tr_i]; recs_te = [recs[i] for i in te_i]
    ytr = np.stack([(svec(r["after"]) - CEN) / VAL for r in recs_tr])

    # GPU ramp receipt
    _w = torch.randn(2048, 2048, device=dev)
    for _ in range(80):
        _w = _w @ _w * 0.001
    torch.cuda.synchronize()

    g, mu, sd, g_score = load_g()
    gn = lambda feats: g((feats - mu) / sd)
    results = {"test_set_size": len(recs_te), "variants": {}}
    models = {}
    for lam in [0.0, 0.25, 0.5]:
        m, curve = train_variant(recs_tr, ytr, lam, gn)
        models[lam] = m
        m.eval()
        with torch.no_grad():
            Xte = torch.tensor(np.stack([jepa_input(r) for r in recs_te]),
                               dtype=torch.float32, device=dev)
            preds = m(Xte).cpu().numpy() * VAL + CEN
        errs = [raw_err(preds[k], svec(recs_te[k]["after"])) for k in range(len(recs_te))]
        results["variants"][str(lam)] = {
            "test_mse_normalized": float(np.mean(np.square(
                (preds - np.stack([svec(r['after']) for r in recs_te]) ) / VAL))),
            "test_raw_err_mean": float(np.mean(errs)),
            "test_raw_err_median": float(np.median(errs)),
            "curve_every20": curve,
        }
        print(f"lam={lam}: raw_err mean={np.mean(errs):.3f} median={np.median(errs):.3f}")

    # ---------- experiment 4: JEV judges the predictions ----------
    preds_store = {}
    judged_rows = []
    for lam in [0.0, 0.25, 0.5]:
        m = models[lam]; m.eval()
        with torch.no_grad():
            Xte = torch.tensor(np.stack([jepa_input(r) for r in recs_te]),
                               dtype=torch.float32, device=dev)
            P = m(Xte).cpu().numpy() * VAL + CEN
        preds_store[str(lam)] = P
        for k, r in enumerate(recs_te):
            pv = P[k]
            tmpl = copy.deepcopy(r["before"])
            rec2 = copy.deepcopy(r)
            rec2["after"] = state_from_vec(pv, tmpl)
            res = jt.call_jev(jt.payload_for(rec2))
            ans = res["answers"] if res else {}
            judged_rows.append({
                "lam": lam, "test_idx": k, "id": r["id"],
                "raw_err": raw_err(pv, svec(r["after"])),
                "noul_valid": ans.get("valid", {}).get("noul"),
                "noul_physical": ans.get("physical", {}).get("noul"),
                "noul_causal": ans.get("causal", {}).get("noul"),
                "category": ans.get("category", {}).get("choice"),
                "pred_state": rec2["after"], "actual_state": r["after"],
                "before_state": r["before"],
            })
        print(f"judged {len(recs_te)} predictions for lam={lam}")

    json.dump(judged_rows, open(os.path.join(HERE, "exp4-predictions-judged.json"), "w"), indent=1)
    json.dump(results, open(os.path.join(HERE, "exp3-results.json"), "w"), indent=1)
    torch.save({str(l): models[l].state_dict() for l in models},
               os.path.join(HERE, "world-models.pt"))
    print("saved exp3-results.json, exp4-predictions-judged.json, world-models.pt")

if __name__ == "__main__":
    main()
