#!/usr/bin/env python3
"""Post-hoc analyses for DL3 (clearly labeled; no new JEV calls).

P1: ridge-kernel variant of the DL3b composed route — recompute residuals with
    a ridge-regularized kernel (lambda by leave-one-out CV on the TRAIN split
    only), reuse the recorded noul scores, recompute arms B/D.
P2: DL3b FRR decomposition by source (which valids did armB reject, and why).
P3: DL3a drift drivers — daily dial-movement magnitude vs daily noul mean.
"""
import datetime
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dl3_common as C

CALIB_DAYS = ("2026-08-17", "2026-08-18", "2026-08-19")
GAP_S = 90 * 60


def iso_to_epoch(ts):
    return datetime.datetime.fromisoformat(ts).timestamp()


def barrail_transitions():
    rows = C.load_barrail()
    days = sorted({r["day"] for r in rows})
    by_day = {d: [] for d in days}
    for r in rows:
        by_day[r["day"]].append(r)
    trans = {}
    for d in days:
        rr = sorted(by_day[d], key=lambda x: x["ts"])
        trans[d] = [(np.array(b["vec"]), np.array(a["vec"]))
                    for a, b in zip(rr[1:], rr)
                    if 0 < iso_to_epoch(a["ts"]) - iso_to_epoch(b["ts"]) <= GAP_S]
    return trans


def ridge_kernel(pairs, lam):
    B = np.array([np.append(b, 1.0) for b, _ in pairs])
    A = np.array([a for _, a in pairs])
    mu, sd = B.mean(0), B.std(0) + 1e-9
    X = (B - mu) / sd
    Xb = np.hstack([X, np.ones((len(X, ), 1))])
    G = Xb.T @ Xb + lam * np.eye(Xb.shape[1])
    Wst = np.linalg.solve(G, Xb.T @ (A - A.mean(0)))
    return {"mu": mu, "sd": sd, "Wst": Wst, "a_mean": A.mean(0)}


def ridge_predict(K, b):
    x = (np.append(b, 1.0) - K["mu"]) / K["sd"]
    x = np.append(x, 1.0)
    return x @ K["Wst"] + K["a_mean"]


def loo_lambda(pairs, grid=(0.1, 1.0, 10.0, 100.0)):
    """Pick lambda by leave-one-out CV on the train split only."""
    best, best_err = None, np.inf
    for lam in grid:
        err = 0.0
        for i in range(len(pairs)):
            tr = pairs[:i] + pairs[i + 1:]
            K = ridge_kernel(tr, lam)
            b, a = pairs[i]
            err += float(np.sum((a - ridge_predict(K, b)) ** 2))
        if err < best_err:
            best, best_err = lam, err
    return best


def main():
    bt = barrail_transitions()
    calib = [x for d in CALIB_DAYS for x in bt[d]]
    lam = loo_lambda(calib)
    K = ridge_kernel(calib, lam)
    rs = [float(np.linalg.norm(a - ridge_predict(K, b))) for b, a in calib]
    th = {"soft": float(np.quantile(rs, 0.90)),
          "hard": float(np.quantile(rs, 0.995))}
    print("[P1] ridge lambda(LOO) =", lam, "thresholds", th)

    b = json.load(open(os.path.join(HERE, "dl3b_out.json")))
    # reconstruct (b, a) arrays from recorded trial text is fragile; re-run the
    # corpus construction deterministically (same seed) to recover vectors.
    import dl3b_pinch_real as B
    rng = np.random.default_rng(C.SEED)
    # replicate corpus construction exactly as dl3b (copy of its logic)
    probe_days = [d for d in bt if d not in CALIB_DAYS]
    pool_B = [x for d in probe_days for x in bt[d]]
    rooms = C.load_roomd()
    # roomd kernels/pools replicated
    def roomd_room_blocks(rrows):
        segs, last = [], None
        for ts, vec, _m in rrows:
            if last is None or ts - last > 60:
                segs.append([])
            segs[-1].append((ts, vec))
            last = ts
        blocks = []
        for seg in segs:
            t0s = seg[0][0]
            bucket = {}
            for ts, vec in seg:
                bucket.setdefault(int((ts - t0s) // 300), []).append(vec)
            for k in sorted(bucket):
                blocks.append((t0s + k * 300, np.mean(bucket[k], axis=0)))
        return blocks

    def date_of(ts):
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

    Rk = {}
    for rn, rrows in rooms.items():
        blocks = roomd_room_blocks(rrows)
        tr = [(bb, aa) for (t1, bb), (t2, aa) in
              zip(blocks, blocks[1:]) if date_of(t1) == "2026-09-03"]
        if len(tr) >= 5:
            lam_r = loo_lambda(tr)
            Kr = ridge_kernel(tr, lam_r)
            rsr = [float(np.linalg.norm(a - ridge_predict(Kr, bb))) for bb, a in tr]
            Rk[rn] = (Kr, {"soft": float(np.quantile(rsr, 0.90)),
                           "hard": float(np.quantile(rsr, 0.995))},
                      blocks, lam_r)
    out = {"label": "POST-HOC (not pre-registered)",
           "barrail": {"lam_loo": lam, "thresholds": th},
           "roomd": {rn: {"lam_loo": v[3], "thresholds": v[1]}
                     for rn, v in Rk.items()}}
    # recover trial vectors: reuse recorded text ordering is hard; instead we
    # REBUILD the trials list with the identical rng sequence and zip against
    # the recorded noul/truth/family in shuffled order. The shuffle in dl3b was
    # applied to `trials` list; rebuilding gives the same order before shuffle.
    trials = []

    def add(bb, aa, truth, family, src, key):
        trials.append({"b": bb, "a": aa, "truth": truth, "family": family,
                       "src": src, "key": key})

    for bb, aa in [pool_B[i] for i in rng.choice(len(pool_B), 30, replace=False)]:
        add(bb, aa, "valid", "real", "barrail", "barrail")
    pool_R = {}
    for rn, (Kr, thr, blocks, _lam) in Rk.items():
        pool_R[rn] = [(bb, aa) for (t1, bb), (t2, aa) in
                      zip(blocks, blocks[1:])
                      if date_of(t1) in ("2026-09-04", "2026-09-17")]
    for rn, (Kr, thr, blocks, _lam) in Rk.items():
        pp = pool_R[rn]
        for bb, aa in [pp[i] for i in rng.choice(len(pp), min(15, len(pp)),
                                                 replace=False)]:
            add(bb, aa, "valid", "real", "roomd:" + rn, rn)
    all_b = [(bb, "barrail") for bb, _ in
             [pool_B[i] for i in rng.choice(len(pool_B), 24, replace=False)]]
    for rn, (Kr, thr, blocks, _lam) in Rk.items():
        pp = pool_R[rn]
        for bb in [pp[i][0] for i in rng.choice(len(pp), min(11, len(pp)),
                                                replace=False)]:
            all_b.append((bb, "roomd:" + rn))
    moving_B = [i for i, k in enumerate(C.B_DIALS) if k != "volume"]
    for fam in ("rate", "range", "breadth"):
        picks = [all_b[i] for i in rng.choice(len(all_b), 15, replace=False)]
        for bb, src in picks:
            aa = bb.copy()
            n = len(bb)
            if fam == "rate":
                moving = moving_B if src == "barrail" else list(range(n))
                i = int(rng.choice(moving))
                aa[i] = bb[i] + (1 if rng.random() < 0.5 else -1) * rng.uniform(0.5, 0.9)
            elif fam == "range":
                i = int(rng.integers(0, n))
                aa[i] = (1 if rng.random() < 0.5 else -1) * rng.uniform(1.2, 1.6)
            else:
                k = int(rng.integers(5, min(8, n) + 1))
                for i in rng.choice(n, k, replace=False):
                    aa[i] = bb[i] + (1 if rng.random() < 0.5 else -1) * rng.uniform(0.2, 0.5)
            add(bb, np.clip(aa, -2, 2), "invalid", fam, src,
                "barrail" if src == "barrail" else src.split(":")[1])
    rns = list(Rk.keys())
    if len(rns) == 2:
        for direction in range(2):
            bx, ax = rns[direction], rns[1 - direction]
            for _ in range(4):
                bb = pool_R[bx][int(rng.integers(0, len(pool_R[bx])))][0]
                aa = pool_R[ax][int(rng.integers(0, len(pool_R[ax])))][1]
                add(bb, aa, "invalid", "splice", "roomd:%s->%s" % (bx, ax), bx)
    for _ in range(7):
        d1, d2 = rng.choice(len(probe_days), 2, replace=False)
        bb = bt[probe_days[int(d1)]][int(rng.integers(
            0, len(bt[probe_days[int(d1)]])))][0]
        aa = bt[probe_days[int(d2)]][int(rng.integers(
            0, len(bt[probe_days[int(d2)]])))][1]
        add(bb, aa, "invalid", "splice", "barrail:crossday", "barrail")
    rng.shuffle(trials)
    # sanity: order must match recorded trials
    ok_order = all((t["truth"] == r["truth"]) and (t["family"] == r["family"])
                   and (t["src"] == r["src"])
                   for t, r in zip(trials, b["trials"]))
    out["corpus_order_matches_recorded"] = bool(ok_order)
    if not ok_order:
        dump_note = "ORDER MISMATCH — post-hoc ridge variant not computable"
        print(dump_note)
        out["note"] = dump_note
        json.dump(out, open(os.path.join(HERE, "dl3_posthoc.json"), "w"),
                  indent=2, default=float)
        return

    recs = []
    for t, r in zip(trials, b["trials"]):
        if t["src"].startswith("barrail"):
            Kr, thr = K, th
        else:
            Kr, thr = Rk[t["key"]][0], Rk[t["key"]][1]
        resid = float(np.linalg.norm(
            np.asarray(t["a"]) - ridge_predict(Kr, np.asarray(t["b"]))))
        noul = r["noul"]
        resid_ok = resid <= thr["soft"]
        resid_hard = resid > thr["hard"]
        if noul >= 0.5 and resid_ok:
            route = 1
        elif noul < 0.35 or resid_hard:
            route = -1
        else:
            route = 0
        recs.append({"truth": t["truth"], "family": t["family"],
                     "src": t["src"], "resid_ridge": round(resid, 4),
                     "noul": noul,
                     "armB": 1 if resid_ok else -1, "armD": route})

    def score(arm):
        inv = [x for x in recs if x["truth"] == "invalid"]
        val = [x for x in recs if x["truth"] == "valid"]
        return {"far": C.wilson(sum(x[arm] == 1 for x in inv), len(inv)),
                "frr": C.wilson(sum(x[arm] == -1 for x in val), len(val)),
                "held": round(sum(x[arm] == 0 for x in recs) / len(recs), 4)}
    out["scores_ridge"] = {a: score(a) for a in ("armB", "armD")}
    out["per_family_far_ridge_D"] = {
        f: C.wilson(sum(x["armD"] == 1 for x in recs if x["family"] == f),
                    sum(1 for x in recs if x["family"] == f))
        for f in ("rate", "range", "breadth", "splice")}

    # P2: FRR decomposition (pre-registered kernel)
    decomp = {}
    for src_key in ("barrail", "roomd:the-bridge", "roomd:doctor-canary"):
        val = [r for r in b["trials"]
               if r["truth"] == "valid" and r["src"] == src_key]
        decomp[src_key] = {
            "n": len(val),
            "armB_reject": C.wilson(sum(r["armB"] == -1 for r in val), len(val)),
            "armD_reject": C.wilson(sum(r["armD"] == -1 for r in val), len(val))}
    out["P2_frr_decomposition"] = decomp

    # P3: DL3a drift drivers
    a = json.load(open(os.path.join(HERE, "dl3a_out.json")))
    days = sorted(a["barrail"]["transitions_per_day"].keys())
    # daily L1 dial movement and daily noul mean
    daily_l1, daily_noul, daily_dates = [], [], []
    for d in days:
        tt = bt[d]
        if not tt:
            continue
        l1 = [float(np.abs(aa - bb).sum()) for bb, aa in tt]
        daily_l1.append(float(np.median(l1)))
        daily_dates.append(d)
    probs = {p["date"]: np.mean([r["noul"] for r in p["real"]])
             for p in a["barrail"]["jev_probes"] if "real" in p}
    xs, ys = [], []
    for d, l1 in zip(daily_dates, daily_l1):
        if d in probs:
            xs.append(l1); ys.append(probs[d])
    out["P3"] = {
        "daily_median_L1": dict(zip(daily_dates,
                                    [round(x, 4) for x in daily_l1])),
        "spearman_dailyL1_noulmean": round(C.spearman(xs, ys), 4),
        "p_spearman": C.perm_p_spearman(xs, ys)}
    json.dump(out, open(os.path.join(HERE, "dl3_posthoc.json"), "w"),
              indent=2, default=float)
    print(json.dumps({k: v for k, v in out.items()
                      if k in ("scores_ridge", "per_family_far_ridge_D",
                               "P2_frr_decomposition", "P3",
                               "corpus_order_matches_recorded")},
                     indent=1, default=float))
    print("wrote dl3_posthoc.json")


if __name__ == "__main__":
    main()
