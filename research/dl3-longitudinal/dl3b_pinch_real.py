#!/usr/bin/env python3
"""DL3b — composed pinch route on REAL dial data (exp4 replication attempt).

Valid 60 = real consecutive transitions (30 bar-rail + 15/room roomd).
Invalid 60 = 4 families x 15: RATE / RANGE / BREADTH (real b, synthetic delta)
and SPLICE (real b, real a, forged adjacency — zero synthesis).
Arms A accept-all / B JEPA-only / C JEV-only / D composed (exp4 thresholds
verbatim). Gates H0/H0b/G1/G2/G3 frozen in PRE-REG.md before any run.
"""
import datetime
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dl3_common import (B_DIALS, B_Q, R_DIALS, R_Q, SEED, dump, fit_kernel,
                        jev_noul, ledger, load_barrail, load_roomd,
                        render_transition, residual, thresholds, warmup_receipt,
                        wilson)

CALIB_DAYS = ("2026-08-17", "2026-08-18", "2026-08-19")
GAP_S = 90 * 60


def iso_to_epoch(ts):
    return datetime.datetime.fromisoformat(ts).timestamp()


def barrail_transitions():
    rows = load_barrail()
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


def main():
    t0 = time.time()
    rec_w = warmup_receipt(3.0)
    rng = np.random.default_rng(SEED)

    # ---------- frozen kernels (identical recipe to DL3a) -------------
    bt = barrail_transitions()
    calib = [x for d in CALIB_DAYS for x in bt[d]]
    WB = fit_kernel(calib)
    thB = thresholds(WB, calib)
    rooms = load_roomd()
    Rk = {}
    for rn, rrows in rooms.items():
        blocks = roomd_room_blocks(rrows)
        tr = [(b, a) for (t1, b), (t2, a) in
              zip(blocks, blocks[1:]) if date_of(t1) == "2026-09-03"]
        if len(tr) >= 5:
            Rk[rn] = (fit_kernel(tr), thresholds(fit_kernel(tr), tr), blocks)

    # ---------- corpus construction (seeded, frozen) ------------------
    probe_days = [d for d in bt if d not in CALIB_DAYS]
    pool_B = [x for d in probe_days for x in bt[d]]
    pool_R = {}
    for rn, (W, th, blocks) in Rk.items():
        pool_R[rn] = [(b, a) for (t1, b), (t2, a) in zip(blocks, blocks[1:])
                      if date_of(t1) in ("2026-09-04", "2026-09-17")]

    trials = []

    def add(b, a, truth, family, src, W, th):
        trials.append({"b": b, "a": a, "truth": truth, "family": family,
                       "src": src, "W": W, "th": th})

    # VALID: 30 B + 15/room R
    for b, a in [pool_B[i] for i in rng.choice(
            len(pool_B), 30, replace=False)]:
        add(b, a, "valid", "real", "barrail", WB, thB)
    for rn, (W, th, blocks) in Rk.items():
        pp = pool_R[rn]
        for b, a in [pp[i] for i in rng.choice(len(pp), min(15, len(pp)),
                                               replace=False)]:
            add(b, a, "valid", "real", "roomd:" + rn, W, th)

    # helper pools for corrupted families: mix B + R states
    all_b = [(b, WB, thB, "barrail") for b, _ in
             [pool_B[i] for i in rng.choice(len(pool_B), 24, replace=False)]]
    for rn, (W, th, blocks) in Rk.items():
        pp = pool_R[rn]
        for b in [pp[i][0] for i in rng.choice(len(pp), min(11, len(pp)),
                                               replace=False)]:
            all_b.append((b, W, th, "roomd:" + rn))
    moving_B = [i for i, k in enumerate(B_DIALS) if k != "volume"]

    for fam in ("rate", "range", "breadth"):
        picks = [all_b[i] for i in rng.choice(len(all_b), 15, replace=False)]
        for b, W, th, src in picks:
            a = b.copy()
            n = len(b)
            if fam == "rate":
                moving = moving_B if src == "barrail" else list(range(n))
                i = int(rng.choice(moving))
                a[i] = b[i] + (1 if rng.random() < 0.5 else -1) * rng.uniform(0.5, 0.9)
            elif fam == "range":
                i = int(rng.integers(0, n))
                a[i] = (1 if rng.random() < 0.5 else -1) * rng.uniform(1.2, 1.6)
            else:  # breadth
                k = int(rng.integers(5, min(8, n) + 1))
                idx = rng.choice(n, k, replace=False)
                for i in idx:
                    a[i] = b[i] + (1 if rng.random() < 0.5 else -1) * rng.uniform(0.2, 0.5)
            add(b, np.clip(a, -2, 2), "invalid", fam, src, W, th)

    # SPLICE: 8 R cross-room (4 each dir) + 7 B cross-day — all-real states
    rns = list(Rk.keys())
    if len(rns) == 2:
        for direction in range(2):
            bx, ax = rns[direction], rns[1 - direction]
            pool_bx = pool_R[bx]
            pool_ax = pool_R[ax]
            for _ in range(4):
                b = pool_bx[int(rng.integers(0, len(pool_bx)))][0]
                a = pool_ax[int(rng.integers(0, len(pool_ax)))][1]
                W, th, _ = Rk[bx]
                add(b, a, "invalid", "splice", "roomd:%s->%s" % (bx, ax), W, th)
    for _ in range(7):
        d1, d2 = rng.choice(len(probe_days), 2, replace=False)
        b = bt[probe_days[int(d1)]][int(rng.integers(
            0, len(bt[probe_days[int(d1)]])))][0]
        a = bt[probe_days[int(d2)]][int(rng.integers(
            0, len(bt[probe_days[int(d2)]])))][1]
        add(b, a, "invalid", "splice", "barrail:crossday", WB, thB)

    rng.shuffle(trials)

    # ---------- run: residual + JEV + arms ----------------------------
    recs = []
    for n, tr in enumerate(trials):
        names = R_DIALS if tr["src"].startswith("roomd") else B_DIALS
        horizon = ("5-minute transition" if tr["src"].startswith("roomd")
                   else "30-minute transition")
        txt = render_transition(tr["b"], tr["a"], names, horizon)
        q = R_Q if tr["src"].startswith("roomd") else B_Q
        resid = residual(tr["W"], tr["b"], tr["a"])
        noul = jev_noul(txt, *q)
        soft, hard = tr["th"]["soft"], tr["th"]["hard"]
        resid_ok = resid <= soft
        resid_hard = resid > hard
        if noul >= 0.5 and resid_ok:
            route = 1
        elif noul < 0.35 or resid_hard:
            route = -1
        else:
            route = 0
        recs.append({"truth": tr["truth"], "family": tr["family"],
                     "src": tr["src"], "residual": round(resid, 4),
                     "noul": round(noul, 4), "text": txt,
                     "armA": 1, "armB": 1 if resid_ok else -1,
                     "armC": 1 if noul >= 0.5 else -1, "armD": route})
        print("[dl3b] %2d %-7s %-8s %-18s resid=%7.3f noul=%.2f D=%+d"
              % (n, tr["truth"], tr["family"], tr["src"], resid, noul, route),
              flush=True)

    # ---------- score (exp4 convention) -------------------------------
    def score(arm):
        inv = [r for r in recs if r["truth"] == "invalid"]
        val = [r for r in recs if r["truth"] == "valid"]
        far = sum(r[arm] == 1 for r in inv)
        frr = sum(r[arm] == -1 for r in val)
        return {"far": wilson(far, len(inv)), "frr": wilson(frr, len(val)),
                "held": round(sum(r[arm] == 0 for r in recs) / len(recs), 4)}

    sc = {arm: score(arm) for arm in ("armA", "armB", "armC", "armD")}
    valid_noul_mean = float(np.mean([r["noul"] for r in recs
                                     if r["truth"] == "valid"]))
    syn_inv = [r for r in recs if r["family"] in ("rate", "range", "breadth")]
    jepa_far_syn = wilson(sum(r["armB"] == 1 for r in syn_inv), len(syn_inv))
    h0 = valid_noul_mean >= 0.5
    h0b = jepa_far_syn[0] >= 0.5
    farD = sc["armD"]["far"][0]
    farB_, farC_ = sc["armB"]["far"][0], sc["armC"]["far"][0]
    frrD = sc["armD"]["frr"][0]
    frrB_, frrC_ = sc["armB"]["frr"][0], sc["armC"]["frr"][0]
    g1 = farD <= 0.7 * min(farB_, farC_)
    g2 = frrD <= min(frrB_, frrC_) + 0.10
    g3 = "SURVIVES" if farD <= 0.10 else ("BREAKS" if farD > 0.25 else "MARGINAL")
    fam = {}
    for f in ("real", "rate", "range", "breadth", "splice"):
        inv = [r for r in recs if r["family"] == f and r["truth"] == "invalid"]
        if inv:
            fam[f] = {"n": len(inv),
                      "farD": wilson(sum(r["armD"] == 1 for r in inv), len(inv)),
                      "farC": wilson(sum(r["armC"] == 1 for r in inv), len(inv)),
                      "farB": wilson(sum(r["armB"] == 1 for r in inv), len(inv))}
    disagree = 0
    for r, tr in zip(recs, trials):
        if (r["noul"] >= 0.5) != (r["residual"] <= tr["th"]["soft"]):
            disagree += 1

    out = {
        "experiment": "DL3b composed pinch route on real dial data",
        "warmup_receipt": rec_w,
        "n_trials": len(recs),
        "kernels": {"barrail": thB,
                    "roomd": {rn: th for rn, (W, th, bl) in Rk.items()}},
        "scores": sc,
        "per_family_far": fam,
        "valid_noul_mean": round(valid_noul_mean, 4),
        "gates": {
            "H0_valid_noul_ge_0.5": {"value": round(valid_noul_mean, 4),
                                     "pass": h0},
            "H0b_jepa_far_syn_ge_0.5": {"value": jepa_far_syn, "pass": h0b},
            "G1_composed_le_0.7x_best_single": {
                "value": [farD, min(farB_, farC_)], "pass": g1},
            "G2_frr_within_10pts": {"value": [frrD, min(frrB_, frrC_)],
                                    "pass": g2},
            "G3_replication": {"farD": farD, "verdict": g3}},
        "complementarity_jev_jepa_disagreements": disagree,
        "verdict": ("INVALID_HARNESS" if not (h0 and h0b) else
                    ("COMPOSED-PASS" if (g1 and g2) else "COMPOSED-FAIL")),
        "trials": recs,
        "jev_ledger": ledger(),
        "wall_s": round(time.time() - t0, 1),
    }
    dump(os.path.join(HERE, "dl3b_out.json"), out)


if __name__ == "__main__":
    main()
