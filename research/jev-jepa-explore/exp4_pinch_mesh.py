#!/usr/bin/env python3
"""Exp 4 — CM1 pinch mesh composed: GEN + JEPA + JEV + ternary routing.

A synthetic vessel room-state stream. A "generative cell" proposes the next
state transition; JEPA (transition-kernel-style predictor trained on the
stream's own history) scores structural validity via residual; JEV supplies
calibrated confidence via one noul judgment; a ternary route decides:
  +1 accept (jev >= 0.5 and residual ok)   -> commit transition
   0 hold   (mixed evidence)               -> defer to human/re-observe
  -1 reject (jev < 0.35 or residual hard-fail)
Ground truth: 30 valid + 30 invalid proposals (graded subtlety).
Arms: A accept-all · B JEPA-only · C JEV-only · D composed ternary.
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jev_noul, ledger, dump, SEED

HERE = os.path.dirname(os.path.abspath(__file__))
# room state vector: [engine_temp, oil_press, rpm, bilge_level, motion, radio_traffic]
DIM = 6
STATE_NAMES = ["engine temp (C above 80 baseline)", "oil pressure (bar below 4)",
               "rpm", "bilge level (fraction)", "motion (0-1)", "radio traffic (0-1)"]

STEADY = np.array([0.0, 0.0, 1800.0, 0.1, 0.05, 0.1])


def state_text(s):
    return ("Vessel room state: engine temp %.1fC above baseline, oil pressure "
            "%.2f bar below nominal, rpm %.0f, bilge %.0f%% full, motion score "
            "%.2f, radio traffic %.2f." % tuple(s))


def describe_transition(before, after):
    d = after - before
    parts = []
    for i, v in enumerate(d):
        if abs(v) > 1e-9:
            parts.append("%s %+0.2f" % (STATE_NAMES[i].split(" (")[0], v))
    return "; ".join(parts) if parts else "no change"


def make_corpus():
    """30 valid + 30 invalid (10 mild / 10 medium / 10 egregious) proposals."""
    rng = np.random.default_rng(SEED)
    trials = []

    def rand_state():
        s = STEADY.copy()
        s[0] += rng.normal(0, 2); s[1] += rng.normal(0, 0.05)
        s[3] = np.clip(s[3] + rng.normal(0, 0.03), 0, 0.4)
        s[4] = np.clip(s[4] + rng.normal(0, 0.05), 0, 0.3)
        return s

    # VALID: plausible one-minute evolutions
    for _ in range(30):
        b = rand_state()
        a = b.copy()
        a[0] += rng.normal(0.5, 0.3)          # temp drifts up slowly
        a[1] += rng.normal(-0.01, 0.02)       # oil sags a touch
        a[3] += rng.normal(0.005, 0.004)      # bilge slowly fills
        a[4] = np.clip(a[4] + rng.normal(0, 0.03), 0, 0.4)
        a = np.clip(a, [0, -1, 800, 0, 0, 0], [8, 0.5, 2200, 0.5, 0.5, 1])
        trials.append((b, a, "valid", "normal"))

    # INVALID graded:
    for lvl, (tj, bp, rz) in (("mild", (4.0, 0.25, 150)),
                              ("medium", (12.0, 0.8, 600)),
                              ("egregious", (35.0, 2.5, 1400))):
        for _ in range(10):
            b = rand_state()
            a = b.copy()
            i = rng.integers(0, 3)  # violate one of temp/oil/rpm
            if i == 0:
                a[0] = b[0] + (tj if rng.random() < 0.5 else -tj * 1.5)
            elif i == 1:
                a[1] = b[1] - bp
            else:
                a[2] = b[2] + (rz if rng.random() < 0.5 else -min(rz, b[2] - 500))
            trials.append((b, a, "invalid", lvl))
    rng.shuffle(trials)
    return trials


def fit_jepa_history():
    """JEPA predictor trained on VALID dynamics only (the room's physics)."""
    rng = np.random.default_rng(SEED + 1)
    N = 1500
    B = np.tile(STEADY, (N, 1)) + rng.normal(0, 1, (N, DIM)) * np.array([2, .05, 80, .03, .05, .08])
    B[:, 3] = np.clip(B[:, 3], 0, .5); B[:, 4] = np.clip(B[:, 4], 0, .4)
    A = B + rng.normal(0, 1, (N, DIM)) * np.array([0.35, 0.025, 25, 0.006, 0.035, 0.05])
    X = np.hstack([B, np.ones((N, 1))])
    W, *_ = np.linalg.lstsq(X, A, rcond=None)
    return W


def residual(W, b, a):
    x = np.append(b, 1.0)
    return float(np.linalg.norm(a - x @ W))


def main():
    W = fit_jepa_history()
    # calibrate residual threshold on valid-only training stream
    rng = np.random.default_rng(SEED + 2)
    res_valid = []
    for _ in range(400):
        b = np.tile(STEADY, (1, 1))[0] + rng.normal(0, 1, DIM) * np.array([2, .05, 80, .03, .05, .08])
        a = b + rng.normal(0, 1, DIM) * np.array([0.35, 0.025, 25, 0.006, 0.035, 0.05])
        res_valid.append(residual(W, b, a))
    RES_SOFT = float(np.quantile(res_valid, 0.90))   # hold boundary
    RES_HARD = float(np.quantile(res_valid, 0.995))  # reject boundary

    trials = make_corpus()
    recs = []
    t0 = time.time()
    for n, (b, a, truth, level) in enumerate(trials):
        resid = residual(W, b, a)
        desc = describe_transition(b, a)
        jev = jev_noul(
            state_text(b) + " Proposed one-minute transition: " + desc + ".",
            "Is this proposed one-minute state transition physically plausible "
            "for a small fishing vessel?",
            "Answer true only if the magnitude and direction of every change "
            "could occur in one minute under normal physics and equipment.")
        resid_ok = resid <= RES_SOFT
        resid_hard = resid > RES_HARD
        # composed ternary route
        if jev >= 0.5 and resid_ok:
            route = 1
        elif jev < 0.35 or resid_hard:
            route = -1
        else:
            route = 0
        # arms
        armA = 1                                   # accept-all
        armB = 1 if resid_ok else -1               # JEPA-only
        armC = 1 if jev >= 0.5 else -1             # JEV-only
        armD = route
        recs.append({"truth": truth, "level": level, "residual": resid,
                     "jev": jev, "resid_soft": RES_SOFT, "resid_hard": RES_HARD,
                     "armA": armA, "armB": armB, "armC": armC, "armD": armD,
                     "desc": desc})
        print("[%4.1fs] %2d %-7s %-9s resid=%7.2f jev=%.2f D=%+d"
              % (time.time() - t0, n, truth, level, resid, jev, route), flush=True)

    def score(arm):
        far = sum(r[arm] == 1 for r in recs if r["truth"] == "invalid") / \
            sum(r["truth"] == "invalid" for r in recs)
        frr = sum(r[arm] in (-1,) for r in recs if r["truth"] == "valid") / \
            sum(r["truth"] == "valid" for r in recs)
        held = sum(r[arm] == 0 for r in recs) / len(recs)
        return far, frr, held

    sc = {arm: score(arm) for arm in ("armA", "armB", "armC", "armD")}
    farD, frrD, heldD = sc["armD"]
    farB, frrB, _ = sc["armB"]
    farC, frrC, _ = sc["armC"]
    far_best_single = min(farB, farC)
    g1 = farD <= 0.7 * far_best_single
    g2 = frrD <= min(frrB, frrC) + 0.10
    disagree = sum((r["jev"] >= 0.5) != (r["residual"] <= RES_SOFT) for r in recs)
    out = {
        "experiment": "exp4 CM1 pinch mesh + JEV + JEPA composed",
        "n_trials": len(recs),
        "thresholds": {"resid_soft": RES_SOFT, "resid_hard": RES_HARD},
        "scores": {k: {"far_invalid_accept": v[0], "frr_valid_reject": v[1],
                       "held_rate": v[2]} for k, v in sc.items()},
        "gates": {"G1_farD_le_0.7x_best_single": {"value": [farD, far_best_single], "pass": g1},
                  "G2_frrD_within_10pts": {"value": [frrD, min(frrB, frrC)], "pass": g2}},
        "complementarity_jev_jepa_disagreements": disagree,
        "trials": recs,
        "jev_ledger": ledger(),
        "wall_s": round(time.time() - t0, 1),
        "verdict": "COMPOSED-PASS" if (g1 and g2) else "COMPOSED-FAIL",
    }
    dump(os.path.join(HERE, "exp4_out.json"), out)


if __name__ == "__main__":
    main()
