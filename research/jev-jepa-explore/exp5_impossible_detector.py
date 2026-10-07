#!/usr/bin/env python3
"""Exp 5 — the impossible-transition detector (+1 possible / 0 unlikely / -1 impossible).

90 events: 30 possible (normal physics), 30 unlikely-but-valid (slow drift,
rare-but-legal), 30 impossible (conservation/physics violations).
Classifiers:
  JEV-only binary    (noul >= 0.5 -> possible)
  JEPA-only binary   (residual <= soft threshold -> possible)
  COMBINED ternary   (-1 impossible if jev <= 0.30 OR resid > hard;
                       0 unlikely if not impossible AND (jev < 0.6 OR resid > soft);
                       +1 possible otherwise)
Truth labels: possible / unlikely / impossible.
The 3-way distinction (unlikely vs impossible) is what NEITHER binary
detector can express — that's the claimed ternary win.
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jev_noul, ledger, dump, SEED

HERE = os.path.dirname(os.path.abspath(__file__))
DIM = 6
STATE_NAMES = ["engine temp", "oil pressure", "rpm", "bilge level", "motion", "radio traffic"]
STEADY = np.array([0.0, 0.0, 1800.0, 0.1, 0.05, 0.1])


def state_text(s):
    return ("Vessel room state: engine temp %.1fC above baseline, oil pressure "
            "%.2f bar below nominal, rpm %.0f, bilge %.0f%% full, motion score "
            "%.2f, radio traffic %.2f." % tuple(s))


def desc(b, a):
    d = a - b
    parts = ["%s %+0.2f" % (STATE_NAMES[i], d[i]) for i in range(DIM) if abs(d[i]) > 1e-9]
    return "; ".join(parts) or "no change"


def make_events():
    """(before, after, label) — 30 possible / 30 unlikely / 30 impossible."""
    rng = np.random.default_rng(SEED + 5)
    ev = []

    def base():
        s = STEADY.copy()
        s[0] += rng.normal(0, 2); s[1] += rng.normal(0, 0.05)
        s[3] = np.clip(s[3] + rng.normal(0, 0.03), 0, 0.4)
        s[4] = np.clip(s[4] + rng.normal(0, 0.05), 0, 0.3)
        return s

    # possible: ordinary one-minute physics
    for _ in range(30):
        b = base(); a = b.copy()
        a[0] += rng.normal(0.4, 0.3); a[1] += rng.normal(-0.01, 0.02)
        a[3] += rng.normal(0.005, 0.004)
        ev.append((b, a, "possible"))

    # unlikely-but-VALID: surprising, rare, but does not violate physics
    for _ in range(30):
        b = base(); a = b.copy()
        kind = rng.integers(0, 4)
        if kind == 0:      # unusually fast but physically reachable warm-up
            a[0] += rng.uniform(2.5, 3.5)
        elif kind == 1:    # sudden maneuver traffic spike (legal)
            a[4] = np.clip(a[4] + rng.uniform(0.35, 0.5), 0, 0.6)
            a[5] = np.clip(a[5] + rng.uniform(0.2, 0.4), 0, 0.8)
        elif kind == 2:    # bilge pump cycle drops level fast (equipment acting)
            a[3] = np.clip(a[3] - rng.uniform(0.06, 0.09), 0, 0.4)
        else:              # throttle-up for passing (legal, brisk)
            a[2] += rng.uniform(150, 250); a[0] += rng.uniform(1.2, 1.8)
        ev.append((b, a, "unlikely"))

    # IMPOSSIBLE: violate physics/equipment limits outright
    for _ in range(30):
        b = base(); a = b.copy()
        kind = rng.integers(0, 5)
        if kind == 0:      # instant massive temp jump (no energy source)
            a[0] = b[0] + rng.choice([-1, 1]) * rng.uniform(25, 45)
        elif kind == 1:    # oil pressure step to zero without shutdown
            a[1] = b[1] - rng.uniform(1.5, 3.0)
        elif kind == 2:    # rpm doubles in one minute in gear
            a[2] = b[2] * rng.uniform(1.9, 2.4)
        elif kind == 3:    # bilge empties AND fills at once (conjunction violation)
            a[3] = 0.0; a[0] = b[0] - 30.0
        else:              # motion teleport: full reversal + magnitude explosion
            a[4] = np.clip(1.0 - b[4], 0.9, 1.0) + 0.4
        ev.append((b, a, "impossible"))
    rng.shuffle(ev)
    return ev


def fit_and_calibrate():
    rng = np.random.default_rng(SEED + 6)
    N = 1500
    B = np.tile(STEADY, (N, 1)) + rng.normal(0, 1, (N, DIM)) * np.array([2, .05, 80, .03, .05, .08])
    B[:, 3] = np.clip(B[:, 3], 0, .5); B[:, 4] = np.clip(B[:, 4], 0, .4)
    A = B + rng.normal(0, 1, (N, DIM)) * np.array([0.35, 0.025, 25, 0.006, 0.035, 0.05])
    X = np.hstack([B, np.ones((N, 1))])
    W, *_ = np.linalg.lstsq(X, A, rcond=None)
    rv = []
    for _ in range(400):
        b = STEADY + rng.normal(0, 1, DIM) * np.array([2, .05, 80, .03, .05, .08])
        a = b + rng.normal(0, 1, DIM) * np.array([0.35, 0.025, 25, 0.006, 0.035, 0.05])
        x = np.append(b, 1.0)
        rv.append(float(np.linalg.norm(a - x @ W)))
    return W, float(np.quantile(rv, 0.90)), float(np.quantile(rv, 0.995))


def main():
    W, RES_SOFT, RES_HARD = fit_and_calibrate()
    events = make_events()
    recs = []
    t0 = time.time()
    for n, (b, a, label) in enumerate(events):
        x = np.append(b, 1.0)
        resid = float(np.linalg.norm(a - x @ W))
        jev = jev_noul(
            state_text(b) + " Observed one-minute transition: " + desc(b, a) + ".",
            "Is this observed one-minute state transition physically possible "
            "for a small fishing vessel?",
            "Answer true only if every change could physically occur in one "
            "minute without violating thermodynamics or equipment limits. "
            "A transition that is merely unusual but physically reachable "
            "still counts as possible.")
        # combined ternary classifier
        if jev <= 0.30 or resid > RES_HARD:
            cls = -1   # impossible
        elif jev < 0.60 or resid > RES_SOFT:
            cls = 0    # unlikely
        else:
            cls = 1    # possible
        truth = {"possible": 1, "unlikely": 0, "impossible": -1}[label]
        recs.append({"label": label, "truth": truth, "jev": jev, "residual": resid,
                     "cls": cls, "desc": desc(b, a)})
        print("[%4.1fs] %2d %-10s jev=%.2f resid=%7.2f -> cls=%+d"
              % (time.time() - t0, n, label, jev, resid, cls), flush=True)

    def acc(fn):
        return sum(fn(r) for r in recs) / len(recs)

    combined_acc = acc(lambda r: r["cls"] == r["truth"])
    # binary baselines mapped to the 3-way problem: they CANNOT distinguish
    # unlikely from impossible -> their best case is collapsing both to one class
    jev_bin = acc(lambda r: (1 if r["jev"] >= 0.5 else -1) == r["truth"])
    jepa_bin = acc(lambda r: (1 if r["residual"] <= RES_SOFT else -1) == r["truth"])
    jev_bin_bin = acc(lambda r: (1 if r["jev"] >= 0.5 else -1) == (1 if r["truth"] == 1 else -1)
                      if r["truth"] in (1, -1) else False)
    # honest binary accuracy: only on the classes the binary detector CAN see
    seen = [r for r in recs if r["truth"] in (1, -1)]
    jev_bin_honest = sum((1 if r["jev"] >= 0.5 else -1) == r["truth"] for r in seen) / len(seen)
    jepa_bin_honest = sum((1 if r["residual"] <= RES_SOFT else -1) == r["truth"] for r in seen) / len(seen)

    per = {}
    for lab in ("possible", "unlikely", "impossible"):
        rs = [r for r in recs if r["label"] == lab]
        t = {"possible": 1, "unlikely": 0, "impossible": -1}[lab]
        per[lab] = {"recall": sum(r["cls"] == t for r in rs) / len(rs),
                    "pred_as": {k: sum(r["cls"] == v for r in rs) for k, v in
                                (("possible", 1), ("unlikely", 0), ("impossible", -1))}}
    imp_prec = (sum(r["cls"] == -1 and r["label"] == "impossible" for r in recs) /
                max(1, sum(r["cls"] == -1 for r in recs)))
    g1 = combined_acc >= 0.70
    g2 = per["unlikely"]["recall"] >= 0.60
    g3 = imp_prec >= 0.80
    out = {
        "experiment": "exp5 impossible-transition detector (+1/0/-1)",
        "n_events": len(recs),
        "thresholds": {"resid_soft": RES_SOFT, "resid_hard": RES_HARD},
        "combined_3way_acc": combined_acc,
        "binary_baselines_3way": {"jev_only": jev_bin, "jepa_only": jepa_bin},
        "binary_baselines_honest": {"jev_only": jev_bin_honest, "jepa_only": jepa_bin_honest},
        "per_class": per,
        "impossible_precision": imp_prec,
        "gates": {"G1_3way_acc_ge_0.70": {"value": combined_acc, "pass": g1},
                  "G2_unlikely_recall_ge_0.60": {"value": per["unlikely"]["recall"], "pass": g2},
                  "G3_impossible_precision_ge_0.80": {"value": imp_prec, "pass": g3}},
        "events": recs,
        "jev_ledger": ledger(),
        "wall_s": round(time.time() - t0, 1),
        "verdict": "TERNARY-DETECTOR-PASS" if (g1 and g2 and g3) else "TERNARY-DETECTOR-FAIL",
    }
    dump(os.path.join(HERE, "exp5_out.json"), out)


if __name__ == "__main__":
    main()
