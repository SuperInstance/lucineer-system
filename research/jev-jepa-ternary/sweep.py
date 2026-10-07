#!/usr/bin/env python3
"""Experiment 1 — threshold sensitivity sweep.

Per axis (v_star, kappa, coh):
  A) symmetric half-width sweep tau = 0.01..0.50 (step 0.01), other axes at spec defaults
  B) center x half-width grid: c in -0.5..+0.5 step 0.05, w in 0.05..0.50 step 0.05
     (this is the task's literal "sweep thresholds from -0.5 to +0.5 in steps of 0.05")

For every config: 27-bucket distribution of the 200 predictions, per-bucket JEV
judgment quality (battery-1 noul), separation metrics between high- and
low-confidence predictions, local routing accuracy vs hidden ground truth,
plus a mixed-path load.

Joint optima (both reported):
  sep_optimal   — maximize composite separation F + corner + MI (guarded)
  route_optimal — maximize routing accuracy, tie-broken by composite
Found by 5000-config bounded random search (centers +-0.1, widths 0.02..0.30)
plus greedy bounded refine. Writes sweep-results.json and operating-config.json
(route_optimal -> used by batteries 2+).
"""
import json
import itertools
import numpy as np

TAU_GRID = [round(0.01 * k, 2) for k in range(1, 51)]
CENTERS = [round(-0.5 + 0.05 * k, 2) for k in range(21)]
WIDTHS = [round(0.05 * k, 2) for k in range(1, 11)]
AXES = ["v_star", "kappa", "coh"]
DEFAULTS = {"v_star": 0.2, "kappa": 0.1, "coh": 0.1}  # task spec


def tern(x, c, w):
    if x > c + w:
        return 1
    if x < c - w:
        return -1
    return 0


def bucket_of(sc, cfg):
    return (tern(sc["v_star"], *cfg["v_star"]),
            tern(sc["kappa"], *cfg["kappa"]),
            tern(sc["coh"], *cfg["coh"]))


def path_of(sig):
    if sig == (1, 0, 1):
        return "strong_positive_transition"
    if sig == (0, 0, 0):
        return "stable_no_change"
    if sig == (-1, -1, -1):
        return "complete_reversal"
    return "mixed_uncertain"


def mi_discrete(x, y):
    n = len(x)
    px, py, pxy = {}, {}, {}
    for a, b in zip(x, y):
        px[a] = px.get(a, 0) + 1
        py[b] = py.get(b, 0) + 1
        pxy[(a, b)] = pxy.get((a, b), 0) + 1
    mi = 0.0
    for (a, b), c in pxy.items():
        pab = c / n
        mi += pab * np.log2(pab / (px[a] / n * py[b] / n))
    return float(mi)


def fstat(groups):
    groups = [g for g in groups if len(g) >= 4]
    if len(groups) < 2:
        return 0.0
    allv = np.concatenate([np.asarray(g) for g in groups])
    grand = allv.mean()
    ssb = sum(len(g) * (np.asarray(g).mean() - grand) ** 2 for g in groups)
    ssw = sum(((np.asarray(g) - np.asarray(g).mean()) ** 2).sum() for g in groups)
    k = len(groups)
    dfb, dfw = k - 1, len(allv) - k
    if dfb <= 0 or dfw <= 0 or ssw == 0:
        return 0.0
    return float((ssb / dfb) / (ssw / dfw))


def config_eval(preds, actuals, quality, conf_hi, cfg):
    sigs = [bucket_of(p, cfg) for p in preds]
    sigs_a = [bucket_of(a, cfg) for a in actuals]
    degenerate = False
    for a in range(3):
        counts = [sum(1 for s in sigs if s[a] == t) for t in (-1, 0, 1)]
        if max(counts) > 0.85 * len(sigs):
            degenerate = True
    buckets = {}
    for s, q in zip(sigs, quality):
        buckets.setdefault(s, []).append(q)
    dist = {str(s): len(v) for s, v in buckets.items()}
    bq = {str(s): round(float(np.mean(v)), 4) for s, v in buckets.items()}
    corner_p = buckets.get((1, 1, 1))
    corner_n = buckets.get((-1, -1, -1))
    corner_sep = (round(abs(np.mean(corner_p) - np.mean(corner_n)), 4)
                  if corner_p and corner_n
                  and len(corner_p) >= 4 and len(corner_n) >= 4 else None)
    hi = [int(h) for h in conf_hi]
    mi_bucket = mi_discrete([s[0] * 9 + s[1] * 3 + s[2] for s in sigs], hi)
    acc = float(np.mean([path_of(s) == path_of(sa)
                         for s, sa in zip(sigs, sigs_a)]))
    mixed = float(np.mean([path_of(s) == "mixed_uncertain" for s in sigs]))
    # special-path precision / recall / F1 (mixed = abstain: no credit)
    tp = sum(1 for s, sa in zip(sigs, sigs_a)
             if path_of(s) != "mixed_uncertain" and path_of(s) == path_of(sa))
    fp = sum(1 for s, sa in zip(sigs, sigs_a)
             if path_of(s) != "mixed_uncertain" and path_of(s) != path_of(sa))
    fn = sum(1 for s, sa in zip(sigs, sigs_a)
             if path_of(s) == "mixed_uncertain" and path_of(sa) != "mixed_uncertain")
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {
        "dist": dist, "bucket_quality": bq, "n_nonempty": len(buckets),
        "degenerate": degenerate,
        "f_stat": round(fstat(list(buckets.values())), 3),
        "corner_sep": corner_sep, "mi_bits": round(mi_bucket, 4),
        "route_acc": round(acc, 4), "mixed_frac": round(mixed, 4),
        "special_precision": round(prec, 4), "special_recall": round(rec, 4),
        "special_f1": round(f1, 4), "n_special_routed": tp + fp,
    }


def main():
    data = json.load(open("predictions.json"))
    items = data["items"]
    b1 = {}
    with open("jev-battery1.jsonl") as f:
        for line in f:
            r = json.loads(line)
            if "error" not in r:
                b1[r["id"]] = r
    assert len(b1) >= len(items) - 5, f"battery1 incomplete: {len(b1)}"
    preds = [it["sc_pred"] for it in items]
    actuals = [it["sc_actual"] for it in items]
    quality = [np.mean([b1[it["id"]][k] for k in ("q_v", "q_k", "q_c")])
               for it in items]
    conf = [b1[it["id"]]["q_conf"] for it in items]
    conf_hi = [c >= 0.6 for c in conf]
    err = np.array([it["err_cos"] for it in items])
    broken = [it["broken"] for it in items]

    out = {"n_items": len(items), "n_judged": len(b1)}

    # ---- per-axis information content (axis trit vs labels) -------------
    axis_info = {}
    for ax in AXES:
        vals = [p[ax] for p in preds]
        for tau in (DEFAULTS[ax], 0.05, 0.1):
            trits = [tern(v, 0.0, tau) + 1 for v in vals]
            axis_info[f"{ax}@tau={tau}"] = {
                "mi_conf_bits": round(mi_discrete(trits, [int(h) for h in conf_hi]), 4),
                "mi_lowerr_bits": round(mi_discrete(trits, [int(e <= np.median(err)) for e in err]), 4),
                "mi_broken_bits": round(mi_discrete(trits, [int(b) for b in broken]), 4),
                "dist": {str(k - 1): trits.count(k) for k in range(3)},
            }
    out["axis_information"] = axis_info

    # ---- A) symmetric sweep per axis (others at defaults) ----------------
    sym = {}
    for ax in AXES:
        rows = []
        for tau in TAU_GRID:
            cfg = {a: (0.0, DEFAULTS[a]) for a in AXES}
            cfg[ax] = (0.0, tau)
            rows.append({"tau": tau, **config_eval(preds, actuals, quality, conf_hi, cfg)})
        sym[ax] = rows
    out["symmetric_sweep"] = sym

    # ---- B) center x width grid per axis ---------------------------------
    grid = {}
    for ax in AXES:
        rows = []
        for c, w in itertools.product(CENTERS, WIDTHS):
            cfg = {a: (0.0, DEFAULTS[a]) for a in AXES}
            cfg[ax] = (c, w)
            rows.append({"center": c, "width": w,
                         **config_eval(preds, actuals, quality, conf_hi, cfg)})
        grid[ax] = rows
    out["center_width_grid"] = grid

    # ---- composite separation score ---------------------------------------
    allf = [r["f_stat"] for ax in AXES for r in sym[ax]]
    allc = [r["corner_sep"] for ax in AXES for r in sym[ax] if r["corner_sep"] is not None]
    allm = [r["mi_bits"] for ax in AXES for r in sym[ax]]
    muf, sdf = np.mean(allf), np.std(allf)
    muc, sdc = np.mean(allc), np.std(allc)
    mum, sdm = np.mean(allm), np.std(allm)

    def z(v, mu, sd):
        return (v - mu) / (sd + 1e-9)

    def sep_score(ev):
        if ev["degenerate"]:
            return -1e9
        cs = ev["corner_sep"] if ev["corner_sep"] is not None else muc
        return (0.5 * z(ev["f_stat"], muf, sdf)
                + 0.3 * z(cs, muc, sdc)
                + 0.2 * z(ev["mi_bits"], mum, sdm))

    # ---- joint optima via bounded random search + greedy refine ----------
    rng = np.random.default_rng(4242)
    cands = []
    for _ in range(5000):
        trial = {ax: (round(float(rng.uniform(-0.1, 0.1)), 3),
                      round(float(rng.uniform(0.02, 0.30)), 3)) for ax in AXES}
        ev = config_eval(preds, actuals, quality, conf_hi, trial)
        cands.append((trial, ev))

    def refine(cfg, objective):
        cfg = {ax: (cfg[ax][0], cfg[ax][1]) for ax in AXES}
        ev = config_eval(preds, actuals, quality, conf_hi, cfg)
        for _ in range(3):
            improved = False
            for ax in AXES:
                for c in np.arange(max(-0.1, cfg[ax][0] - 0.05),
                                   min(0.1, cfg[ax][0] + 0.051), 0.025):
                    for w in np.arange(max(0.02, cfg[ax][1] - 0.04),
                                       min(0.30, cfg[ax][1] + 0.041), 0.01):
                        t = dict(cfg)
                        t[ax] = (round(float(c), 3), round(float(w), 3))
                        tev = config_eval(preds, actuals, quality, conf_hi, t)
                        if objective(tev) > objective(ev):
                            cfg, ev, improved = t, tev, True
            if not improved:
                break
        return cfg, ev

    best_sep = max(cands, key=lambda ce: sep_score(ce[1]))
    best_route = max(cands, key=lambda ce: (ce[1]["special_f1"], sep_score(ce[1])))
    sep_cfg, sep_ev = refine(best_sep[0], sep_score)
    route_cfg, route_ev = refine(best_route[0], lambda e: (e["special_f1"], sep_score(e)))

    out["sep_optimal"] = {
        "thresholds": {ax: {"center": sep_cfg[ax][0], "width": sep_cfg[ax][1]} for ax in AXES},
        "eval": sep_ev, "sep_score": round(sep_score(sep_ev), 3),
    }
    out["route_optimal"] = {
        "thresholds": {ax: {"center": route_cfg[ax][0], "width": route_cfg[ax][1]} for ax in AXES},
        "eval": route_ev, "sep_score": round(sep_score(route_ev), 3),
    }
    cfg = route_cfg  # operating point for batteries 2+

    # ---- default config for comparison ------------------------------------
    dcfg = {ax: (0.0, DEFAULTS[ax]) for ax in AXES}
    out["default_config"] = {
        "thresholds": {ax: {"center": 0.0, "width": DEFAULTS[ax]} for ax in AXES},
        "eval": config_eval(preds, actuals, quality, conf_hi, dcfg),
    }

    # ---- per-axis summary at symmetric sweep -------------------------------
    out["per_axis_symmetric_summary"] = {}
    for ax in AXES:
        rows = [r for r in sym[ax] if not r["degenerate"]]
        bf = max(rows, key=lambda r: r["f_stat"])
        ba = max(rows, key=lambda r: r["route_acc"])
        bm = max(rows, key=lambda r: r["mi_bits"])
        dflt = next(r for r in rows if abs(r["tau"] - DEFAULTS[ax]) < 1e-9)
        out["per_axis_symmetric_summary"][ax] = {
            "default_tau": DEFAULTS[ax],
            "argmax_f": {"tau": bf["tau"], "f": bf["f_stat"], "acc": bf["route_acc"]},
            "argmax_acc": {"tau": ba["tau"], "acc": ba["route_acc"], "f": ba["f_stat"]},
            "argmax_mi": {"tau": bm["tau"], "mi": bm["mi_bits"]},
            "default": {"f": dflt["f_stat"], "mi": dflt["mi_bits"], "acc": dflt["route_acc"]},
        }

    # ---- jev judgment vs ground truth quality ------------------------------
    out["jev_discrimination"] = {
        "corr_qconf_err": round(float(np.corrcoef(conf, err)[0, 1]), 4),
        "corr_quality_err": round(float(np.corrcoef(quality, err)[0, 1]), 4),
        "mean_qconf_broken": round(float(np.mean([c for c, b in zip(conf, broken) if b])), 4),
        "mean_qconf_clean": round(float(np.mean([c for c, b in zip(conf, broken) if not b])), 4),
        "mean_quality_broken": round(float(np.mean([q for q, b in zip(quality, broken) if b])), 4),
        "mean_quality_clean": round(float(np.mean([q for q, b in zip(quality, broken) if not b])), 4),
        "err_median": round(float(np.median(err)), 4),
    }

    json.dump(out, open("sweep-results.json", "w"), indent=1)
    json.dump({"thresholds": {ax: {"center": cfg[ax][0], "width": cfg[ax][1]} for ax in AXES}},
              open("operating-config.json", "w"), indent=1)
    print("sep_optimal:", json.dumps(out["sep_optimal"]["thresholds"]),
          "acc", sep_ev["route_acc"], "f", sep_ev["f_stat"], "mi", sep_ev["mi_bits"])
    print("route_optimal:", json.dumps(out["route_optimal"]["thresholds"]),
          "acc", route_ev["route_acc"], "f", route_ev["f_stat"], "mi", route_ev["mi_bits"])
    print("default acc:", out["default_config"]["eval"]["route_acc"],
          "f", out["default_config"]["eval"]["f_stat"])
    print("per-axis summary:", json.dumps(out["per_axis_symmetric_summary"], indent=1))
    print("jev discrimination:", out["jev_discrimination"])


if __name__ == "__main__":
    main()
