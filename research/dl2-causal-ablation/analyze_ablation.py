#!/usr/bin/env python3
"""DL2 analysis per PRE-REG: CE per coupling, bootstrap CIs, Wilcoxon+BH-FDR, shams, probes, causal map."""
import json, os, sys, pickle
import numpy as np
sys.path.insert(0, os.path.join(HERE := os.path.dirname(os.path.abspath(__file__)), "..", "jev-jepa-meta"))
from common import load_transitions, load_judgments, features
from scipy.stats import wilcoxon, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
recs = {r["id"]: r for r in load_transitions()}
manifest = json.load(open(os.path.join(HERE, "manifest.json")))
rf = pickle.load(open(os.path.join(HERE, "rf_null.pkl"), "rb"))
jd2 = load_judgments()

rows = {}
for l in open(os.path.join(HERE, "ablation-judgments.jsonl")):
    r = json.loads(l)
    rows[(r["arm"], r["id"])] = r

def noul(arm, i, q="valid"): return rows[(arm, i)]["raw"][q]["noul"]
def cat(arm, i): return rows[(arm, i)]["raw"]["category"]["choice"]

# ---- drift check ----
drift = [(noul("DRIFT", i), jd2[i]["raw"]["valid"]["noul"]) for i in manifest["drift_check_ids"]]
d1, d0 = zip(*drift)
drift_stats = {"n": len(d1), "spearman": float(spearmanr(d1, d0).statistic),
               "mean_abs_diff": float(np.mean(np.abs(np.array(d1) - np.array(d0)))),
               "gate_pass": bool(spearmanr(d1, d0).statistic >= 0.8 and np.mean(np.abs(np.array(d1) - np.array(d0))) <= 0.15)}
print("DRIFT CHECK:", drift_stats)

def rf_pred(i, after_state): return float(rf.predict(features(recs[i], after_state=after_state).reshape(1, -1))[0])

# rebuild edited states exactly as the runner did (shared edits module)
import edits
edits.set_records(recs)

BOOT = np.random.default_rng(7)
def boot_ci(vals, n=10000):
    vals = np.array(vals, dtype=float); m = len(vals)
    idx = BOOT.integers(0, m, size=(n, m))
    bs = vals[idx].mean(axis=1)
    return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

results = {"drift": drift_stats, "couplings": {}, "probes": {}, "sham": {}}

def ce_for(arm_prefix, ids, direction="drop"):
    """CE = mean[noul_orig - noul_edited] - mean[rf_orig - rf_edited]; per-transition paired."""
    dn, drf, dcausal, cross45, cross50, cats = [], [], [], 0, 0, []
    for i in ids:
        orig_st = recs[i]["after"]
        arm = arm_prefix
        edited_st = (edits.edit_state(arm.split("|")[0], "remove", recs[i]) if "|remove" in arm else
                     edits.edit_state(arm.split("|")[0], "invert", recs[i]) if "|invert" in arm else
                     edits.edit_probe(arm.split("|")[0], recs[i]) if "|probe" in arm else
                     edits.edit_sham(arm.split("|")[0], recs[i]))
        dn.append(noul("BASE", i) - noul(arm, i))
        drf.append(rf_pred(i, orig_st) - rf_pred(i, edited_st))
        dcausal.append(noul("BASE", i, "causal") - noul(arm, i, "causal"))
        cross45 += noul(arm, i) < 0.45
        cross50 += noul(arm, i) < 0.50
        cats.append(cat(arm, i))
    dn, drf = np.array(dn), np.array(drf)
    ce = dn - drf
    lo, hi = boot_ci(ce)
    try: p = float(wilcoxon(ce).pvalue)
    except Exception: p = 1.0
    return {"n": len(ids), "mean_d_noul": float(dn.mean()), "mean_d_rf": float(drf.mean()),
            "CE": float(ce.mean()), "ci_lo": lo, "ci_hi": hi, "wilcoxon_p": p,
            "mean_d_causal": float(np.mean(dcausal)),
            "cross_045": cross45 / len(ids), "cross_050": cross50 / len(ids),
            "p_unnatural": float(np.mean([c == "unnatural" for c in cats])),
            "base_p_unnatural": float(np.mean([cat("BASE", i) == "unnatural" for i in ids])),
            "ce_vals": [float(x) for x in ce]}

for cid, v in manifest["couplings"].items():
    results["couplings"][cid] = {
        "remove": ce_for(f"{cid}|remove", v["ids"]),
        "invert": ce_for(f"{cid}|invert", v["ids"]),
        "n_active_total": v["n_active"]}

for pid, v in manifest["probes"].items():
    if v["ids"]:
        results["probes"][pid] = ce_for(f"{pid}|probe", v["ids"])
    else:
        results["probes"][pid] = {"n": 0, "note": "empty active set — arm could not run (see PRE-REG/FINDINGS)"}

for cid, v in manifest["sham"].items():
    results["sham"][cid] = ce_for(f"{cid}|sham", v["ids"])

# BH-FDR across 11 couplings (remove condition)
def bh(pvals):
    p = np.array(pvals); n = len(p)
    order = np.argsort(p); ranked = p[order] * n / (np.arange(n) + 1)
    ranked = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(n); out[order] = np.minimum(ranked, 1.0)
    return out
premove = [results["couplings"][c]["remove"]["wilcoxon_p"] for c in results["couplings"]]
q = bh(premove)
for k, cid in enumerate(results["couplings"]):
    r = results["couplings"][cid]["remove"]
    r["fdr_q"] = float(q[k])
    r["edge_detected"] = bool(r["ci_lo"] > 0 and r["fdr_q"] < 0.05)
    ri = results["couplings"][cid]["invert"]
    results["couplings"][cid]["sign_encoded"] = bool(ri["CE"] > r["CE"])

with open(os.path.join(HERE, "ablation-results.json"), "w") as f:
    json.dump(results, f, indent=1)

# ---- console report ----
print("\n=== COUPLINGS (remove | invert) — CE = judgment shift beyond marginal-null ===")
rank = sorted(results["couplings"], key=lambda c: -results["couplings"][c]["remove"]["CE"])
for cid in rank:
    r, ri = results["couplings"][cid]["remove"], results["couplings"][cid]["invert"]
    star = "EDGE" if r["edge_detected"] else "  . "
    print(f"{star} {cid:20s} CE_rm={r['CE']:+.3f} [{r['ci_lo']:+.3f},{r['ci_hi']:+.3f}] q={r['fdr_q']:.4f} "
          f"| CE_inv={ri['CE']:+.3f} | dN={r['mean_d_noul']:+.3f} dRF={r['mean_d_rf']:+.3f} "
          f"| causalΔ={r['mean_d_causal']:+.3f} | cross50={r['cross_050']:.2f} sign={results['couplings'][cid]['sign_encoded']}")
print("\n=== PROBES ===")
for pid, r in results["probes"].items():
    if r["n"] == 0:
        print(f"  {pid:20s} NOT RUN (empty active set)")
        continue
    print(f"  {pid:20s} CE={r['CE']:+.3f} [{r['ci_lo']:+.3f},{r['ci_hi']:+.3f}] p={r['wilcoxon_p']:.4f} dN={r['mean_d_noul']:+.3f} dRF={r['mean_d_rf']:+.3f} cross50={r['cross_050']:.2f}")
print("\n=== SHAMS (should be ~0) ===")
for cid, r in results["sham"].items():
    print(f"  {cid:20s} CE={r['CE']:+.3f} [{r['ci_lo']:+.3f},{r['ci_hi']:+.3f}] dN={r['mean_d_noul']:+.3f} dRF={r['mean_d_rf']:+.3f}")
neg = [r["CE"] for r in results["sham"].values()]
print(f"sham |CE| mean = {np.mean(np.abs(neg)):.3f}")
det = [c for c in rank if results["couplings"][c]["remove"]["edge_detected"]]
print(f"\nEdges detected: {len(det)}/11 -> {det}")
