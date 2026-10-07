#!/usr/bin/env python3
"""DL1-REAL-JEPA step 4: frozen analyses A1-A4 on real-residual judgments."""
import json, os
import numpy as np
from collections import defaultdict
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

HERE = os.path.dirname(os.path.abspath(__file__))
DIALS = ["mood", "volume", "earnestness", "cynicism", "joke_landing",
         "panic", "presence"]

rows = json.load(open(os.path.join(HERE, "jev-rows.json")))
byrow = {(r["channel"], r["night"], r["seq_t"]): r for r in rows}
J = [json.loads(l) for l in open(os.path.join(HERE, "jev-real-judgments.jsonl"))]
print(f"judgments: {len(J)}")

# ---------------- A1: arm means ----------------
agg = defaultdict(list)
for j in J:
    agg[(j["channel"], j["arm"], j["question"])].append(j["noul"])
print("\n== A1: mean noul by (channel, arm, question) ==")
a1 = {}
for k in sorted(agg):
    v = agg[k]
    a1["/".join(k)] = {"mean": round(float(np.mean(v)), 3),
                       "sd": round(float(np.std(v)), 3), "n": len(v)}
    print(f"  {'/'.join(k):38s} {np.mean(v):.3f} ± {np.std(v):.3f} (n={len(v)})")

# paired deltas jepa - pers per question (pooled channels)
print("\n== A1b: paired JEPA − persistence (noul) ==")
pair = defaultdict(lambda: defaultdict(dict))
for j in J:
    if j["arm"] in ("jepa", "pers"):
        pair[(j["question"])][j["channel"]].setdefault(j["seq_t"], {})
        pair[j["question"]][j["channel"]][j["seq_t"]][j["arm"]] = j["noul"]
for q, chans in pair.items():
    ds = []
    for ch, rr in chans.items():
        for st, arms in rr.items():
            if "jepa" in arms and "pers" in arms:
                ds.append(arms["jepa"] - arms["pers"])
    ds = np.array(ds)
    from scipy.stats import wilcoxon
    w = wilcoxon(ds) if len(ds) > 5 and np.any(ds != 0) else (None, 1.0)
    print(f"  {q:12s} meanΔ {ds.mean():+.4f} sd {ds.std():.4f} n={len(ds)} "
          f"wilcoxon p={w[1]:.4g}")

# ---------------- A2: Spearman(resid, noul) ----------------
print("\n== A2: Spearman(raw decoded L1 residual, noul) ==")
a2 = {}
for j in J:
    if j["arm"] in ("jepa", "pers") and j["question"] in ("valid", "coupling", "close"):
        a2.setdefault((j["arm"], j["question"]), []).append((j["resid_l1"], j["noul"]))
for k, v in sorted(a2.items()):
    r, p = spearmanr([x[0] for x in v], [x[1] for x in v])
    print(f"  {k}: rho={r:+.3f} p={p:.4g} n={len(v)}")

# ---------------- A3: low-noul audit ----------------
print("\n== A3: low-noul (<0.5) rows ==")
feats = {}
def row_features(r, arm):
    b = np.array([r["before"]["room_conversation_field"][d] for d in DIALS])
    a = np.array([r["actual"]["room_conversation_field"][d] for d in DIALS])
    p = np.array([r[f"pred_{arm}"]["room_conversation_field"][d] for d in DIALS])
    e = np.abs(p - a)
    d_pred = p - b; d_act = a - b
    return {
        "l1": float(e.sum()),
        "per_dial": e.tolist(),
        "breadth": int((e > 0.01).sum()),
        "focal_max": float(e.max()),
        "dk_vol_pres": float(abs(d_pred[1] - d_pred[6] - (d_act[1] - d_act[6]))),
        "dk_mood_joke": float(abs(d_pred[0] - d_act[0] + (d_pred[4] - d_act[4]))),
        "dk_cyn_mood": float(abs(-(d_pred[3] - d_act[3]) - (d_pred[0] - d_act[0]))),
        "kappa_err": abs(r[f"pred_{arm}"]["field_concentration_kappa"]
                         - r["actual"]["field_concentration_kappa"]),
        "rho_err": abs(r[f"pred_{arm}"]["field_mean_resultant_rho"]
                       - r["actual"]["field_mean_resultant_rho"]),
        "pred_delta_l1": float(np.abs(d_pred).sum()),
    }

low = [j for j in J if j["arm"] == "jepa" and j["question"] == "valid"
       and j["noul"] < 0.5]
print(f"  count: {len(low)} / {sum(1 for j in J if j['arm']=='jepa' and j['question']=='valid')}")
for j in low:
    r = byrow[(j["channel"], j["night"], j["seq_t"])]
    f = row_features(r, "jepa")
    print(f"  {j['night']} seq{j['seq_t']} ch{j['channel']} noul={j['noul']:.2f} "
          f"l1={f['l1']:.3f} breadth={f['breadth']} focal={f['focal_max']:.3f} "
          f"dkVP={f['dk_vol_pres']:.3f} dkMJ={f['dk_mood_joke']:.3f} "
          f"kerr={f['kappa_err']:.2f}")

# ---------------- A4: what explains noul(valid) on real residuals ----------------
print("\n== A4: explain noul(valid, jepa) from residual features ==")
X, Y, tags = [], [], []
for j in J:
    if j["arm"] != "jepa" or j["question"] != "valid":
        continue
    r = byrow[(j["channel"], j["night"], j["seq_t"])]
    f = row_features(r, "jepa")
    X.append(f["per_dial"] + [f["breadth"], f["focal_max"], f["dk_vol_pres"],
                              f["dk_mood_joke"], f["dk_cyn_mood"],
                              f["kappa_err"], f["rho_err"], f["pred_delta_l1"]])
    Y.append(j["noul"]); tags.append((j["channel"], j["night"]))
X, Y = np.array(X), np.array(Y)
names = [f"err_{d}" for d in DIALS] + ["breadth", "focal_max", "dk_vol_pres",
        "dk_mood_joke", "dk_cyn_mood", "kappa_err", "rho_err", "pred_delta_l1"]
# night-held-out honesty + 5-fold CV
mask = np.array([t[1] != "D-cold" for t in tags])
rf = RandomForestRegressor(400, random_state=0).fit(X[mask], Y[mask])
from sklearn.model_selection import cross_val_predict
pred = cross_val_predict(RandomForestRegressor(400, random_state=0), X, Y, cv=5)
r2 = 1 - ((pred - Y) ** 2).sum() / ((Y - Y.mean()) ** 2).sum()
rho, _ = spearmanr(pred, Y)
print(f"  RF 5-fold CV: R²={r2:.3f} Spearman={rho:.3f} (n={len(Y)})")
imp = sorted(zip(names, rf.feature_importances_), key=lambda x: -x[1])
for n, v in imp[:8]:
    print(f"    {n:16s} {v:.3f}")
# night-held-out: train S4b, test D-cold and vice versa
for test_night in ("D-cold", "S4b"):
    m = np.array([t[1] == test_night for t in tags])
    if m.sum() >= 5 and (~m).sum() >= 5:
        rf2 = RandomForestRegressor(400, random_state=0).fit(X[~m], Y[~m])
        p2 = rf2.predict(X[m])
        r2n = 1 - ((p2 - Y[m]) ** 2).sum() / max(((Y[m] - Y[m].mean()) ** 2).sum(), 1e-9)
        print(f"  night-held-out (test={test_night}): R²={r2n:.3f} n={m.sum()}")

out = {"A1": a1}
json.dump(out, open(os.path.join(HERE, "analyze-summary.json"), "w"), indent=1)
print("\n[OK] analyze-summary.json")
