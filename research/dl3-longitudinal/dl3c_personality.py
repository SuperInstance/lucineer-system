#!/usr/bin/env python3
"""DL3c — personality vs room boundary on the nights corpus (182 sessions).

Within-night consecutive-speak transitions (valid, 30) vs cross-night splices:
NEAR (same roster composition, below-median vibe distance, 15) and FAR
(top-tercile roster Jaccard distance >= 0.5, 15). Does the composed pinch
reject personality shifts more than composition-preserving splices?
Gates C0/C1/C2 frozen in PRE-REG.md; C3 (per-composition noul spread) booked.
"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dl3_common import (N_DIALS, N_Q, SEED, dump, fit_kernel, jev_noul,
                        ledger, load_nights, render_transition, residual,
                        thresholds, warmup_receipt, wilson)

N_TRAIN = 100


def roster_names(s):
    return set(s["roster"].keys())


def jaccard(a, b):
    u = len(a | b)
    return 0.0 if u == 0 else 1.0 - len(a & b) / u


def vibe_distance(sx, sy):
    """Mean L1 distance of 7-dial vibes over shared members (max if none)."""
    shared = roster_names(sx) & roster_names(sy)
    if not shared:
        return 4.0
    ds = []
    for name in shared:
        vx = np.array(sx["roster"][name]["vibe"])
        vy = np.array(sy["roster"][name]["vibe"])
        ds.append(float(np.abs(vx - vy).sum()))
    return float(np.mean(ds))


def main():
    t0 = time.time()
    rec_w = warmup_receipt(3.0)
    rng = np.random.default_rng(SEED)
    sessions = load_nights()
    print("[dl3c] sessions loaded:", len(sessions), flush=True)

    train, ev = sessions[:N_TRAIN], sessions[N_TRAIN:]

    # ---- frozen kernel on train sessions' within-night transitions ----
    tr_pairs = []
    for s in train:
        F = s["field"]
        tr_pairs.extend(list(zip(F[:-1], F[1:])))
    W = fit_kernel(tr_pairs)
    th = thresholds(W, tr_pairs)
    print("[dl3c] kernel: train_pairs=%d soft=%.4f hard=%.4f"
          % (len(tr_pairs), th["soft"], th["hard"]), flush=True)

    def sample_within(s):
        F = s["field"]
        i = int(rng.integers(5, len(F) - 1))  # avoid opening ramp
        return F[i], F[i + 1]

    def sample_state(s, quarter="late"):
        F = s["field"]
        lo = int(len(F) * (0.5 if quarter == "late" else 0.0))
        i = int(rng.integers(lo, len(F)))
        return F[i]

    # ---- valid 30: within-night, across eval sessions ------------------
    trials = []
    pool = [s for s in ev if len(s["field"]) >= 10]
    for s in [pool[i] for i in rng.choice(len(pool), 30, replace=False)]:
        b, a = sample_within(s)
        trials.append({"b": b, "a": a, "truth": "valid", "group": "within",
                       "comp": "+".join(sorted(roster_names(s)))[:40],
                       "src": os.path.basename(s["file"])})

    # ---- splice candidates --------------------------------------------
    same_pairs, far_pairs = [], []
    for i in range(len(pool)):
        for j in range(len(pool)):
            if i == j:
                continue
            sx, sy = pool[i], pool[j]
            jd = jaccard(roster_names(sx), roster_names(sy))
            if jd == 0.0:
                same_pairs.append((i, j, vibe_distance(sx, sy)))
            elif jd >= 0.5:
                far_pairs.append((i, j, jd))
    vd = sorted(p[2] for p in same_pairs)
    vmed = vd[len(vd) // 2] if vd else 0.0
    near_pool = [p for p in same_pairs if p[2] <= vmed]
    print("[dl3c] same-comp pairs=%d (near<=vmed %.3f: %d), far pairs=%d"
          % (len(same_pairs), vmed, len(near_pool), len(far_pairs)),
          flush=True)

    def take(pairs, k, group):
        idx = rng.choice(len(pairs), min(k, len(pairs)), replace=False)
        for p in [pairs[i] for i in idx]:
            i, j = p[0], p[1]
            b = sample_state(pool[i], "late")
            a = sample_state(pool[j], "any")
            trials.append({"b": b, "a": a, "truth": "invalid", "group": group,
                           "comp": "splice jd=%.2f" % jaccard(
                               roster_names(pool[i]), roster_names(pool[j])),
                           "src": "%s->%s" % (os.path.basename(pool[i]["file"]),
                                              os.path.basename(pool[j]["file"]))})

    take(near_pool, 15, "near")
    take(far_pairs, 15, "far")
    rng.shuffle(trials)

    # ---- run ------------------------------------------------------------
    recs = []
    for n, tr in enumerate(trials):
        txt = render_transition(tr["b"], tr["a"], N_DIALS,
                                "next-speak transition")
        resid = residual(W, tr["b"], tr["a"])
        noul = jev_noul(txt, *N_Q)
        resid_ok = resid <= th["soft"]
        resid_hard = resid > th["hard"]
        if noul >= 0.5 and resid_ok:
            route = 1
        elif noul < 0.35 or resid_hard:
            route = -1
        else:
            route = 0
        recs.append({"truth": tr["truth"], "group": tr["group"],
                     "comp": tr["comp"], "src": tr["src"],
                     "residual": round(resid, 4), "noul": round(noul, 4),
                     "armB": 1 if resid_ok else -1,
                     "armC": 1 if noul >= 0.5 else -1, "armD": route,
                     "text": txt})
        print("[dl3c] %2d %-7s %-6s %-24s resid=%7.3f noul=%.2f D=%+d"
              % (n, tr["truth"], tr["group"], tr["comp"], resid, noul, route),
              flush=True)

    # ---- score ----------------------------------------------------------
    def rr(group, arm="armD"):
        g = [r for r in recs if r["group"] == group]
        return wilson(sum(r[arm] == -1 for r in g), len(g)), len(g)

    within_frr, n_within = rr("within")
    near_rej, n_near = rr("near")
    far_rej, n_far = rr("far")
    within_noul = [r["noul"] for r in recs if r["group"] == "within"]
    c0 = float(np.mean(within_noul)) >= 0.5
    diff = far_rej[0] - near_rej[0]
    c1 = diff >= 0.20
    c2 = abs(diff) < 0.20 and abs(near_rej[0] - within_frr[0]) <= 0.20

    # C3 booked: per-composition noul on within-night valids
    comps = {}
    for r in recs:
        if r["group"] == "within":
            comps.setdefault(r["comp"], []).append(r["noul"])
    comp_means = {k: round(float(np.mean(v)), 4)
                  for k, v in sorted(comps.items()) if len(v) >= 2}

    out = {
        "experiment": "DL3c personality vs room boundary (nights corpus)",
        "warmup_receipt": rec_w,
        "n_sessions": len(sessions), "n_eval_sessions": len(pool),
        "kernel": {"train_pairs": len(tr_pairs), **th},
        "n_trials": len(recs),
        "groups": {"within": within_frr + [n_within],
                   "near": near_rej + [n_near],
                   "far": far_rej + [n_far]},
        "within_noul_mean": round(float(np.mean(within_noul)), 4),
        "gates": {
            "C0_within_noul_ge_0.5": {"value": round(float(np.mean(within_noul)), 4),
                                      "pass": c0},
            "C1_boundary_encodes_personality": {
                "far_minus_near_reject": round(diff, 4), "pass": c1},
            "C2_room_only_null": {"value": round(diff, 4), "pass": c2}},
        "C3_booked_per_composition_noul": comp_means,
        "verdict": ("INVALID_HARNESS" if not c0 else
                    ("PERSONALITY_BOUNDARY" if c1 else
                     ("ROOM_ONLY" if c2 else "MIXED"))),
        "trials": recs,
        "jev_ledger": ledger(),
        "wall_s": round(time.time() - t0, 1),
    }
    dump(os.path.join(HERE, "dl3c_out.json"), out)


if __name__ == "__main__":
    main()
