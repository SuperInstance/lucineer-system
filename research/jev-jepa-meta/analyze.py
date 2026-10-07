#!/usr/bin/env python3
"""Experiment 2 (residual analysis) + final assembly of meta-results.json."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_transitions, load_judgments, features, svec, DIMS, SIG

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))

def structure_metrics(rec):
    d = np.array([rec["delta"][k] for k in DIMS]) / SIG
    shifted = np.abs(d) > 1.0
    n = int(shifted.sum())
    if n > 0:
        signs = np.sign(d[shifted])
        consist = float(abs(signs.sum()) / n)
    else:
        consist = 0.0
    l1 = float(np.abs(d).sum())
    conc = float(np.abs(d).max() / l1) if l1 > 1e-9 else 0.0
    return {"n_shifted": n, "sign_consistency": consist,
            "concentration": conc, "l1": l1}

def main():
    recs = load_transitions()
    jd = load_judgments()
    X = np.stack([features(r) for r in recs])
    y = np.array([jd[r["id"]]["raw"]["valid"]["noul"] for r in recs])
    clean = np.array([r["clean"] for r in recs])

    # honest OOF predictions for residuals
    rf = RandomForestRegressor(n_estimators=400, random_state=0, n_jobs=-1)
    oof = cross_val_predict(rf, X, y, cv=list(StratifiedKFold(5, shuffle=True,
                 random_state=1).split(X, clean)))
    resid = y - oof

    low = y < 0.5
    exp2 = {
        "n_low_noul": int(low.sum()),
        "low_noul_composition": {
            "corrupt": int((~clean[low]).sum()), "clean": int(clean[low].sum())},
        "by_mode": {},
    }
    rows_low = []
    for i, r in enumerate(recs):
        if not low[i]:
            continue
        sm = structure_metrics(r)
        rows_low.append({
            "id": r["id"], "clean": r["clean"],
            "mode": (r.get("corruption") or {}).get("mode"),
            "severity": (r.get("corruption") or {}).get("severity"),
            "noul": float(y[i]), "oof_pred": float(oof[i]), "residual": float(resid[i]),
            **sm})
    for mode in sorted({row["mode"] for row in rows_low if row["mode"]}):
        grp = [row for row in rows_low if row["mode"] == mode]
        exp2["by_mode"][mode] = {
            "n": len(grp),
            "mean_n": float(np.mean([g["n_shifted"] for g in grp])),
            "mean_sign_consistency": float(np.mean([g["sign_consistency"] for g in grp])),
            "mean_concentration": float(np.mean([g["concentration"] for g in grp])),
            "mean_noul": float(np.mean([g["noul"] for g in grp])),
        }
    # structured vs random verdict among low-noul corrupt rows
    cr = [row for row in rows_low if not row["clean"]]
    structured = [row for row in cr if row["sign_consistency"] > 0.6 or
                  (row["mode"] in ("global_shift", "inversion", "dim_swap", "rate_violation"))]
    exp2["structured_fraction_of_low_noul_corrupt"] = \
        round(len(structured) / max(1, len(cr)), 3)
    exp2["random_like_fraction"] = round(1 - len(structured) / max(1, len(cr)), 3)
    # sign consistency: low-noul corrupt vs clean transitions overall
    cc = [structure_metrics(r) for i, r in enumerate(recs) if clean[i]]
    exp2["clean_baseline_sign_consistency"] = float(
        np.mean([c["sign_consistency"] for c in cc]))
    exp2["clean_baseline_n_shifted"] = float(np.mean([c["n_shifted"] for c in cc]))

    # top residual surprises (JEV vs model disagreement)
    order = np.argsort(-np.abs(resid))[:10]
    exp2["top_meta_residuals"] = [{
        "id": recs[i]["id"], "clean": bool(clean[i]),
        "mode": (recs[i].get("corruption") or {}).get("mode"),
        "noul": float(y[i]), "oof_pred": float(oof[i]),
        "residual": float(resid[i])} for i in order]

    # JEV misses by GT
    misses = [r for i, r in enumerate(recs) if (not clean[i]) and y[i] >= 0.7]
    sev_ct = {}
    for r in misses:
        key = (r["corruption"]["mode"], r["corruption"]["severity"])
        sev_ct[str(key)] = sev_ct.get(str(key), 0) + 1
    exp2["jev_misses_noul_ge_0.7"] = {"count": len(misses), "by_mode_severity": sev_ct}
    fn = [r for i, r in enumerate(recs) if clean[i] and y[i] < 0.5]
    exp2["jev_false_negatives"] = [{"id": r["id"], "noul": float(y[i]),
                                    "causes": r["causes"]} for i, r in enumerate(recs)
                                   if clean[i] and y[i] < 0.5]

    json.dump(exp2, open(os.path.join(HERE, "exp2-residuals.json"), "w"), indent=1)
    print(json.dumps(exp2, indent=1)[:3000])

    # ---------- assemble meta-results.json ----------
    meta_summary = json.load(open(os.path.join(HERE, "meta-summary.json")))
    exp3 = json.load(open(os.path.join(HERE, "exp3-results.json")))
    exp4rows = json.load(open(os.path.join(HERE, "exp4-predictions-judged.json")))

    def quadrants(rows):
        errs = np.array([r["raw_err"] for r in rows])
        nouls = np.array([r["noul_valid"] for r in rows], dtype=float)
        med = float(np.median(errs))
        q = {
            "median_err": med,
            "mean_noul": float(nouls.mean()),
            "frac_noul_ge_0.7": float((nouls >= 0.7).mean()),
            "frac_noul_lt_0.5": float((nouls < 0.5).mean()),
            "hi_err_valid": [r["id"] for r in rows if r["raw_err"] > med and r["noul_valid"] >= 0.7],
            "lo_err_invalid": [r["id"] for r in rows if r["raw_err"] <= med and r["noul_valid"] < 0.5],
            "corr_err_noul": float(spearmanr(errs, nouls).statistic),
        }
        return q

    exp4 = {"per_lambda": {
        lam: quadrants([r for r in exp4rows if str(r["lam"]) == lam])
        for lam in ("0.0", "0.25", "0.5")},
        "example_hi_err_valid": [
            {"id": r["id"], "lam": r["lam"], "raw_err": round(r["raw_err"], 3),
             "noul": r["noul_valid"], "category": r["category"],
             "pred": r["pred_state"], "actual": r["actual_state"]}
            for r in exp4rows if r["noul_valid"] and r["noul_valid"] >= 0.85][:4],
        "example_lo_err_invalid": [
            {"id": r["id"], "lam": r["lam"], "raw_err": round(r["raw_err"], 3),
             "noul": r["noul_valid"], "category": r["category"],
             "pred": r["pred_state"], "actual": r["actual_state"]}
            for r in exp4rows if r["noul_valid"] and r["noul_valid"] < 0.3][:4]}

    # all 500 judgments record
    all_j = []
    usage_tot = {"input_tokens": 0, "output_tokens": 0}
    for i, r in enumerate(recs):
        a = jd[r["id"]]
        usage_tot["input_tokens"] += a["usage"].get("input_tokens", 0)
        usage_tot["output_tokens"] += a["usage"].get("output_tokens", 0)
        all_j.append({
            "id": r["id"], "clean": r["clean"], "causes": r["causes"],
            "corruption": r.get("corruption"), "elapsed_minutes": r["elapsed_minutes"],
            "delta": r["delta"],
            "noul_valid": a["raw"]["valid"]["noul"],
            "noul_physical": a["raw"]["physical"]["noul"],
            "noul_causal": a["raw"]["causal"]["noul"],
            "category": a["raw"]["category"]["choice"],
            "category_conf": a["raw"]["category"].get("confidence"),
            "oof_rf_pred": float(oof[i]),
        })

    out = {
        "meta": {"model": jd[recs[0]["id"]]["model"], "n_transitions": len(recs),
                 "judge_api": "typesafe.ai /v1/systemone", "usage_total": usage_tot,
                 "date": "2026-10-06"},
        "experiment1_meta_predictor": meta_summary,
        "experiment2_residuals": exp2,
        "experiment3_self_consistency": exp3,
        "experiment4_jev_vs_raw_error": exp4,
        "judgments_500": all_j,
    }
    json.dump(out, open(os.path.join(HERE, "meta-results.json"), "w"), indent=1)
    sz = os.path.getsize(os.path.join(HERE, "meta-results.json"))
    print(f"\nmeta-results.json assembled ({sz/1024:.0f} KB), usage={usage_tot}")

if __name__ == "__main__":
    main()
