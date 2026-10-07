#!/usr/bin/env python3
"""Experiments 2-4 + final assembly of ternary-results.json.

  E2  ternary-guided routing: per-path stats at operating + default thresholds,
      JEV routing quality (q_route) vs local routing truth, confusion matrices.
  E3  ternary as filter: survival + survivor quality sweeping filter cut,
      JEV (q_filter / q_conf) vs local proxies vs oracle.
  E4  cross-repo synergy:
      4a ternary-route: JEV-noul admission tiers {accept, queue, reject} with
         swept cut points; throughput/quality tradeoff.
      4b ternary-consensus: K=5 jittered-threshold jurors, majority vote per
         axis; byzantine juror variant.
      4c ternary-engine: trit-population metrics (gamma, |gamma|+H, frac_zero),
         EngineHealth classification, 0-trap overload + forgiveness tunneling
         sweep (re-examining a fraction of (0,0,0) with fine thresholds).
      4d ternary-minority: population regime classification (consensus /
         polarization / chaos) via path participation.
  Bootstrap CIs on key F1s. Everything local; JEV data from batteries 1/2/2b.
"""
import json
import numpy as np

AXES = ["v_star", "kappa", "coh"]
SPEC = {"v_star": 0.2, "kappa": 0.1, "coh": 0.1}
SEED = 4242


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


PATHS = ["strong_positive_transition", "stable_no_change",
         "complete_reversal", "mixed_uncertain"]


def prf(pred_paths, true_paths):
    tp = sum(1 for p, t in zip(pred_paths, true_paths)
             if p != "mixed_uncertain" and p == t)
    fp = sum(1 for p, t in zip(pred_paths, true_paths)
             if p != "mixed_uncertain" and p != t)
    fn = sum(1 for p, t in zip(pred_paths, true_paths)
             if p == "mixed_uncertain" and t != "mixed_uncertain")
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"precision": round(prec, 4), "recall": round(rec, 4),
            "f1": round(f1, 4), "n_special": tp + fp}


def boot_ci(f, arrays, n=1000, seed=SEED):
    rng = np.random.default_rng(seed)
    idx = np.arange(len(arrays[0]))
    vals = []
    for _ in range(n):
        sel = rng.choice(idx, size=len(idx), replace=True)
        vals.append(f(*[np.asarray(a)[sel] for a in arrays]))
    v = np.percentile(vals, [2.5, 97.5])
    return [round(float(v[0]), 4), round(float(v[1]), 4)]


def load():
    items = json.load(open("predictions.json"))["items"]
    b1 = {}
    for line in open("jev-battery1.jsonl"):
        r = json.loads(line)
        if "error" not in r:
            b1[r["id"]] = r
    b2 = {}
    for line in open("jev-battery2.jsonl"):
        r = json.loads(line)
        if "error" not in r:
            b2[r["id"]] = r
    b2b = {}
    for line in open("jev-battery2b.jsonl"):
        r = json.loads(line)
        if "error" not in r:
            b2b[r["id"]] = r
    return items, b1, b2, b2b


def main():
    items, b1, b2, b2b = load()
    ocfg = json.load(open("operating-config.json"))["thresholds"]
    ocfg = {ax: (ocfg[ax]["center"], ocfg[ax]["width"]) for ax in AXES}
    dcfg = {ax: (0.0, SPEC[ax]) for ax in AXES}

    sigs_o = [bucket_of(it["sc_pred"], ocfg) for it in items]
    sigs_d = [bucket_of(it["sc_pred"], dcfg) for it in items]
    sigs_a_o = [bucket_of(it["sc_actual"], ocfg) for it in items]
    sigs_a_d = [bucket_of(it["sc_actual"], dcfg) for it in items]
    paths_o = [path_of(s) for s in sigs_o]
    paths_d = [path_of(s) for s in sigs_d]
    paths_a_o = [path_of(s) for s in sigs_a_o]
    err = np.array([it["err_cos"] for it in items])
    broken = np.array([it["broken"] for it in items])
    qfilter = np.array([b2[it["id"]]["q_filter"] for it in items])
    qroute = np.array([b2[it["id"]]["q_route"] for it in items])
    qroute_d = np.array([b2b[it["id"]]["q_route"] for it in items])
    qconf = np.array([b1[it["id"]]["q_conf"] for it in items])
    qaxes = {k: np.array([b1[it["id"]][k] for it in items])
             for k in ("q_v", "q_k", "q_c")}

    res = {"meta": {
        "n_items": len(items), "n_broken": int(broken.sum()),
        "jev": {"model": "jev-latest", "endpoint": "api.typesafe.ai/v1/systemone",
                "calls": {"battery1": len(b1), "battery2_operating": len(b2),
                          "battery2_default": len(b2b)},
                "questions_per_call": 4, "errors": 0},
        "thresholds": {"operating": {ax: {"center": ocfg[ax][0], "width": ocfg[ax][1]} for ax in AXES},
                        "default": {ax: {"center": 0.0, "width": SPEC[ax]} for ax in AXES}},
    }}

    # ================= E2: ternary-guided routing =========================
    e2 = {}
    for tag, paths, sigs, sigs_a, qr in (("operating", paths_o, sigs_o, sigs_a_o, qroute),
                                          ("default", paths_d, sigs_d, sigs_a_d, qroute_d)):
        per_path = {}
        for p in PATHS:
            m = [i for i, pp in enumerate(paths) if pp == p]
            if not m:
                per_path[p] = {"n": 0}
                continue
            acc = float(np.mean([paths[i] == paths_a[i] for i in m]))
            per_path[p] = {
                "n": len(m),
                "jev_route_quality": round(float(np.mean(qr[m])), 4),
                "local_route_acc": round(acc, 4),
                "mean_qfilter": round(float(np.mean(qfilter[m])), 4),
                "broken_frac": round(float(np.mean(broken[m])), 4),
            }
        conf = {}
        for p in PATHS:
            conf[p] = {q: sum(1 for i, pp in enumerate(paths)
                              if pp == p and paths_a[i] == q) for q in PATHS}
        e2[tag] = {
            "per_path": per_path,
            "confusion_pred_x_actual": conf,
            "overall_jev_route_quality": round(float(np.mean(qr)), 4),
            "overall_route_acc": round(float(np.mean([p == a for p, a in zip(paths, paths_a)])), 4),
            "prf": prf(paths, paths_a),
            "prf_ci95": boot_ci(lambda pp, aa: prf(list(pp), list(aa))["f1"],
                                [paths, paths_a]),
        }
    # judgment-vs-truth agreement on routing
    truth_ok = np.array([p == a for p, a in zip(paths_o, paths_a_o)])
    e2["jev_vs_truth"] = {
        "mean_qroute_when_correct": round(float(qroute[truth_ok].mean()), 4),
        "mean_qroute_when_wrong": round(float(qroute[~truth_ok].mean()), 4),
        "corr_qroute_err": round(float(np.corrcoef(qroute, err)[0, 1]), 4),
        "corr_qfilter_err": round(float(np.corrcoef(qfilter, err)[0, 1]), 4),
    }
    res["experiment2_routing"] = e2

    # ================= E3: ternary as filter ===============================
    e3 = {"sweep": []}
    base_quality = {"mean_err": round(float(err.mean()), 4),
                    "broken_frac": round(float(broken.mean()), 4),
                    "sig_acc": round(float(np.mean([s == sa for s, sa in zip(sigs_o, sigs_a_o)])), 4)}
    e3["unfiltered"] = base_quality
    for tau in np.arange(0.30, 0.81, 0.05):
        for fname, fvals in (("q_filter", qfilter), ("q_conf", qconf),
                             ("q_axes_mean", np.mean(list(qaxes.values()), axis=0))):
            keep = fvals >= tau
            if keep.sum() < 5:
                continue
            e3["sweep"].append({
                "filter": fname, "cut": round(float(tau), 2),
                "survival": round(float(keep.mean()), 4),
                "survivor_mean_err": round(float(err[keep].mean()), 4),
                "survivor_broken_frac": round(float(broken[keep].mean()), 4),
                "survivor_sig_acc": round(float(np.mean(
                    [s == sa for s, sa, k in zip(sigs_o, sigs_a_o, keep) if k])), 4),
                "survivor_route_f1": prf([p for p, k in zip(paths_o, keep) if k],
                                         [a for a, k in zip(paths_a_o, keep) if k])["f1"],
            })
    # oracle + local proxy for reference
    e3["reference_filters"] = {
        "oracle_lowerr(error<=median)": {
            "survival": 0.5,
            "survivor_broken_frac": round(float(broken[err <= np.median(err)].mean()), 4),
            "survivor_mean_err": round(float(err[err <= np.median(err)].mean()), 4)},
        "local_|kappa|>0.05": {
            "survival": round(float(np.mean([abs(it["sc_pred"]["kappa"]) > 0.05 for it in items])), 4),
            "survivor_broken_frac": round(float(broken[
                [abs(it["sc_pred"]["kappa"]) > 0.05 for it in items]].mean()), 4)},
    }
    # broken detection AUC for each judgment signal
    def auc(score, label):
        order = np.argsort(score)
        ranks = np.empty(len(score))
        ranks[order] = np.arange(1, len(score) + 1)
        n1 = label.sum(); n0 = len(label) - n1
        return float((ranks[label].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
    e3["broken_detection_auc"] = {
        k: round(auc(v, broken), 4) for k, v in
        {"q_filter": qfilter, "q_conf": qconf, "q_v": qaxes["q_v"],
         "q_k": qaxes["q_k"], "q_c": qaxes["q_c"]}.items()
    }
    res["experiment3_filter"] = e3

    # ================= E4a: ternary-route admission tiers ==================
    # JEV noul -> {+1 accept, 0 queue, -1 reject}; queued items go to the
    # mixed/hold path (re-examination), rejected items fall back to persist.
    e4a = {"sweep": []}
    for acc_cut in np.arange(0.5, 0.75, 0.05):
        for rej_cut in np.arange(0.2, 0.45, 0.05):
            verdict = np.where(qfilter >= acc_cut, 1, np.where(qfilter <= rej_cut, -1, 0))
            routed = [p if v == 1 else ("mixed_uncertain" if v == 0 else "persist_fallback")
                      for p, v in zip(paths_o, verdict)]
            # quality: among accepted, is the special-path decision right?
            acc_m = verdict == 1
            f1a = prf([p for p, k in zip(paths_o, acc_m) if k],
                      [a for a, k in zip(paths_a_o, acc_m) if k])
            e4a["sweep"].append({
                "accept_cut": round(float(acc_cut), 2), "reject_cut": round(float(rej_cut), 2),
                "frac_accept": round(float((verdict == 1).mean()), 4),
                "frac_queue": round(float((verdict == 0).mean()), 4),
                "frac_reject": round(float((verdict == -1).mean()), 4),
                "accepted_route_f1": f1a["f1"],
                "accepted_broken_frac": round(float(broken[acc_m].mean()), 4),
                "rejected_broken_frac": round(float(broken[verdict == -1].mean()), 4),
            })
    res["experiment4a_ternary_route_admission"] = e4a

    # ================= E4b: ternary-consensus voting =======================
    rng = np.random.default_rng(SEED)
    K = 5
    juror_sigs = []
    for j in range(K):
        jc = {ax: (float(rng.normal(ocfg[ax][0], 0.03)),
                   float(max(0.01, rng.normal(ocfg[ax][1], 0.03)))) for ax in AXES}
        juror_sigs.append(([bucket_of(it["sc_pred"], jc) for it in items], jc))
    cons_paths = []
    for i in range(len(items)):
        csig = tuple()
        for a in range(3):
            votes = [js[0][i][a] for js in juror_sigs]
            # majority with 0-wins-ties (deterministic, fleet convention)
            counts = {v: votes.count(v) for v in (-1, 0, 1)}
            top = max(counts.values())
            winners = sorted([v for v, c in counts.items() if c == top])
            csig += (winners[0],)  # 0 wins ties (smallest magnitude first)
        cons_paths.append(path_of(csig))
    e4b = {
        "n_jurors": K, "jitter_sigma": 0.03,
        "consensus_prf": prf(cons_paths, paths_a_o),
        "single_prf": prf(paths_o, paths_a_o),
        "consensus_ci95": boot_ci(lambda cp, aa: prf(list(cp), list(aa))["f1"],
                                  [cons_paths, paths_a_o]),
        "agreement_with_single": round(float(np.mean(
            [c == p for c, p in zip(cons_paths, paths_o)])), 4),
    }
    # byzantine: juror 0 scrambled (uniform random trits)
    bz = [tuple(int(x) for x in rng.choice([-1, 0, 1], 3)) for _ in range(len(items))]
    juror_sigs_bz = [(bz, None)] + juror_sigs[1:]
    cons_bz = []
    for i in range(len(items)):
        csig = tuple()
        for a in range(3):
            votes = [js[0][i][a] for js in juror_sigs_bz]
            counts = {v: votes.count(v) for v in (-1, 0, 1)}
            top = max(counts.values())
            winners = sorted([v for v, c in counts.items() if c == top])
            csig += (winners[0],)
        cons_bz.append(path_of(csig))
    e4b["byzantine_prf"] = prf(cons_bz, paths_a_o)
    # majority vote among the 4 path labels directly (ternary-consensus style)
    e4b["note"] = ("0-wins-ties majority per axis (deterministic tie-break, "
                   "ternary-consensus convention); byzantine = juror 0 scrambled")
    res["experiment4b_consensus"] = e4b

    # ================= E4c: ternary-engine metrics + forgiveness ===========
    def pop_metrics(sigs):
        trits = np.array([[s[a] for a in range(3)] for s in sigs])
        gamma = float(trits.mean())
        abs_gamma = float(np.abs(trits).mean())
        # joint entropy over signatures
        n = len(sigs)
        counts = {}
        for s in sigs:
            counts[s] = counts.get(s, 0) + 1
        H = -sum((c / n) * np.log(c / n) for c in counts.values())
        fz = float((trits == 0).mean())
        health = ("DEAD" if 1 - fz < 0.01 else
                  "CRITICAL" if 1 - fz < 0.3 else
                  "VIBRANT" if H > np.log(9) and 1 - fz > 0.7 else
                  "CONSENSUS" if 1 - fz > 0.9 else "TRANSITIONING")
        return {"signed_gamma": round(gamma, 4), "abs_gamma": round(abs_gamma, 4),
                "shannon_H": round(float(H), 4), "abs_gamma_plus_H": round(abs_gamma + float(H), 4),
                "frac_zero": round(fz, 4), "engine_health": health}
    e4c = {
        "population_operating": pop_metrics(sigs_o),
        "population_actual": pop_metrics(sigs_a_o),
    }
    # 0-trap overload: use WIDE thresholds to force absorption into (0,0,0)
    wide = {ax: (0.0, 0.5) for ax in AXES}
    sigs_w = [bucket_of(it["sc_pred"], wide) for it in items]
    sigs_a_w = [bucket_of(it["sc_actual"], wide) for it in items]
    e4c["wide_threshold_population"] = pop_metrics(sigs_w)
    e4c["wide_prf"] = prf([path_of(s) for s in sigs_w], [path_of(s) for s in sigs_a_w])
    # forgiveness sweep: re-examine fraction f of (0,0,0) with fine thresholds
    trap_idx = [i for i, s in enumerate(sigs_w) if s == (0, 0, 0)]
    fine = {ax: (ocfg[ax][0], ocfg[ax][1] / 4) for ax in AXES}
    rng2 = np.random.default_rng(SEED)
    forg = []
    for f in [0.0, 0.006, 0.02, 0.05, 0.10, 0.20, 0.40, 0.60, 1.0]:
        accs = []
        for rep in range(200):
            sigs_f = list(sigs_w)
            k = int(round(f * len(trap_idx)))
            chosen = rng2.choice(trap_idx, size=k, replace=False) if k else []
            for i in chosen:
                sigs_f[i] = bucket_of(items[i]["sc_pred"], fine)
            pp = [path_of(s) for s in sigs_f]
            aa = [path_of(s) for s in sigs_a_w]
            accs.append(prf(pp, aa)["f1"])
        forg.append({"forgiveness_rate": f, "route_f1_mean": round(float(np.mean(accs)), 4),
                     "route_f1_sd": round(float(np.std(accs)), 4)})
    e4c["forgiveness_sweep"] = forg
    e4c["engine_default_tunnel_rate"] = 0.006
    res["experiment4c_engine"] = e4c

    # ================= E4d: ternary-minority regimes =======================
    frac = {p: np.mean([pp == p for pp in paths_o]) for p in PATHS}
    top2 = sorted(frac.values(), reverse=True)[:2]
    participation = sum(x ** 2 for x in frac.values())
    regime = ("CHAOS" if frac["mixed_uncertain"] > 0.5 else
              "POLARIZATION" if top2[1] > 0.2 else "CONSENSUS")
    e4d = {
        "path_fractions": {k: round(v, 4) for k, v in frac.items()},
        "participation_ratio": round(participation, 4),
        "regime": regime,
        "regime_operating": regime,
        "regime_default": ("CHAOS" if np.mean([pp == "mixed_uncertain" for pp in paths_d]) > 0.5
                           else "POLARIZATION"),
        "note": ("minority-rule lens: a router dominated by mixed_uncertain is in "
                 "the chaos regime (no path has a quorum); two strong corners = "
                 "polarization; one dominant path = consensus"),
    }
    res["experiment4d_minority_regimes"] = e4d

    # ================= assemble with sweep results =========================
    sw = json.load(open("sweep-results.json"))
    res["experiment1_sweep"] = {
        k: sw[k] for k in ("axis_information", "symmetric_sweep", "center_width_grid",
                           "sep_optimal", "route_optimal", "default_config",
                           "per_axis_symmetric_summary", "jev_discrimination")
    }
    json.dump(res, open("ternary-results.json", "w"), indent=1)

    # ---- console digest ---------------------------------------------------
    print("== E2 routing")
    for tag in ("operating", "default"):
        print(f"  {tag}: jev_route {e2[tag]['overall_jev_route_quality']:.3f} "
              f"acc {e2[tag]['overall_route_acc']:.3f} prf {e2[tag]['prf']} "
              f"ci {e2[tag]['prf_ci95']}")
    print("  jev_vs_truth:", e2["jev_vs_truth"])
    print("== E3 filter: broken AUC", e3["broken_detection_auc"])
    best = max([r for r in e3["sweep"] if r["filter"] == "q_filter"],
               key=lambda r: r["survivor_route_f1"])
    print("  best q_filter cut:", best)
    print("== E4a best admission:",
          max(e4a["sweep"], key=lambda r: r["accepted_route_f1"]))
    print("== E4b consensus:", e4b["consensus_prf"], "single:", e4b["single_prf"],
          "byz:", e4b["byzantine_prf"])
    print("== E4c engine:", e4c["population_operating"], "wide:", e4c["wide_prf"])
    print("  forgiveness:", [(r["forgiveness_rate"], r["route_f1_mean"]) for r in forg])
    print("== E4d regimes:", e4d["path_fractions"], e4d["regime"])


if __name__ == "__main__":
    main()
