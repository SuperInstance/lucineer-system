#!/usr/bin/env python3
"""Exp 5b — POST-HOC: per-dim standardized residuals as the surprise oracle.

Exp5 failed: the residual NORM collapses unlikely-vs-impossible. Post-hoc
hypothesis: unlikely events = ONE dim briskly off (max per-dim z moderate);
impossible = single dim beyond hard physics OR multi-dim conjunction.
Classifier: -1 if jev<=0.30 or zmax>HARD; 0 if zmax>SOFT; +1 else.
Honest split: thresholds fit on half the events, evaluated on held-out half.
JEV values reused from exp5_out.json (deterministic corpus regeneration).
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 2718
DIM = 6
STEADY = np.array([0.0, 0.0, 1800.0, 0.1, 0.05, 0.1])


def regen_events():
    """Same generator as exp5 (SEED+5, same call order)."""
    rng = np.random.default_rng(SEED + 5)
    ev = []

    def base():
        s = STEADY.copy()
        s[0] += rng.normal(0, 2); s[1] += rng.normal(0, 0.05)
        s[3] = np.clip(s[3] + rng.normal(0, 0.03), 0, 0.4)
        s[4] = np.clip(s[4] + rng.normal(0, 0.05), 0, 0.3)
        return s

    for _ in range(30):
        b = base(); a = b.copy()
        a[0] += rng.normal(0.4, 0.3); a[1] += rng.normal(-0.01, 0.02)
        a[3] += rng.normal(0.005, 0.004)
        ev.append((b, a, "possible"))
    for _ in range(30):
        b = base(); a = b.copy()
        kind = rng.integers(0, 4)
        if kind == 0: a[0] += rng.uniform(2.5, 3.5)
        elif kind == 1:
            a[4] = np.clip(a[4] + rng.uniform(0.35, 0.5), 0, 0.6)
            a[5] = np.clip(a[5] + rng.uniform(0.2, 0.4), 0, 0.8)
        elif kind == 2: a[3] = np.clip(a[3] - rng.uniform(0.06, 0.09), 0, 0.4)
        else:
            a[2] += rng.uniform(150, 250); a[0] += rng.uniform(1.2, 1.8)
        ev.append((b, a, "unlikely"))
    for _ in range(30):
        b = base(); a = b.copy()
        kind = rng.integers(0, 5)
        if kind == 0: a[0] = b[0] + rng.choice([-1, 1]) * rng.uniform(25, 45)
        elif kind == 1: a[1] = b[1] - rng.uniform(1.5, 3.0)
        elif kind == 2: a[2] = b[2] * rng.uniform(1.9, 2.4)
        elif kind == 3: a[3] = 0.0; a[0] = b[0] - 30.0
        else: a[4] = np.clip(1.0 - b[4], 0.9, 1.0) + 0.4
        ev.append((b, a, "impossible"))
    rng.shuffle(ev)
    return ev


def main():
    exp5 = json.load(open(os.path.join(HERE, "exp5_out.json")))
    jevs = [e["jev"] for e in exp5["events"]]
    events = regen_events()
    assert len(events) == len(jevs) == 90
    # per-dim delta scale from VALID training stream
    rng = np.random.default_rng(SEED + 6)
    deltas = []
    for _ in range(2000):
        b = STEADY + rng.normal(0, 1, DIM) * np.array([2, .05, 80, .03, .05, .08])
        a = b + rng.normal(0, 1, DIM) * np.array([0.35, 0.025, 25, 0.006, 0.035, 0.05])
        deltas.append(a - b)
    deltas = np.array(deltas)
    mu, sd = deltas.mean(0), deltas.std(0) + 1e-9

    rows = []
    for (b, a, label), jev in zip(events, jevs):
        z = np.abs((a - b - mu) / sd)
        rows.append({"label": label, "jev": jev, "zmax": float(z.max()),
                     "zsum2": float((z ** 2).sum()), "n_big": int((z > 3).sum())})

    # honest split: fit thresholds on half, evaluate on other half (both halves reported)
    rng2 = np.random.default_rng(SEED + 9)
    idx = rng2.permutation(len(rows))
    fit_i, ev_i = idx[:45], idx[45:]

    def grid():
        for SOFT in (2.0, 2.5, 3.0, 3.5, 4.0):
            for HARD in (6.0, 8.0, 10.0, 14.0, 20.0):
                if HARD <= SOFT:
                    continue
                yield SOFT, HARD

    def classify(r, SOFT, HARD):
        if r["jev"] <= 0.30 or r["zmax"] > HARD:
            return -1
        if r["zmax"] > SOFT:
            return 0
        return 1

    best = None
    for SOFT, HARD in grid():
        acc = np.mean([classify(rows[i], SOFT, HARD) ==
                       {"possible": 1, "unlikely": 0, "impossible": -1}[rows[i]["label"]]
                       for i in fit_i])
        if best is None or acc > best[0]:
            best = (acc, SOFT, HARD)
    _, SOFT, HARD = best
    truth_map = {"possible": 1, "unlikely": 0, "impossible": -1}
    ev_acc = np.mean([classify(rows[i], SOFT, HARD) == truth_map[rows[i]["label"]] for i in ev_i])
    per = {}
    for lab in truth_map:
        rs = [rows[i] for i in ev_i if rows[i]["label"] == lab]
        per[lab] = {"recall": float(np.mean([classify(r, SOFT, HARD) == truth_map[lab] for r in rs]))}
    out = {
        "experiment": "exp5b POST-HOC per-dim z + jev ternary classifier",
        "post_hoc": True,
        "thresholds_fit_on": "half (45), evaluated on held-out half (45)",
        "chosen": {"SOFT": SOFT, "HARD": HARD, "fit_acc": best[0]},
        "heldout_3way_acc": float(ev_acc),
        "heldout_per_class_recall": per,
        "rows": rows,
        "verdict": "POST-HOC-PASS" if (ev_acc >= 0.70 and per["unlikely"]["recall"] >= 0.60) else "POST-HOC-FAIL",
    }
    with open(os.path.join(HERE, "exp5b_out.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
