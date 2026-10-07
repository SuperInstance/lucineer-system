#!/usr/bin/env python3
"""Exp 3 — Ternary-structured JEPA: transition prediction on the ternary lattice.

Flat JEPA: continuous TransitionPredictor (field_before + ternary corr) ->
ternarize the output. Lattice JEPA: per-dim conditional count table
P(after_trit | before_trit, corr_trit) over 3x3x3 states -> argmax decode.
Question: does predicting ON the lattice keep the accuracy while collapsing
the representation to log2(3^9) ~ 14.3 bits (vs 9 x float32 = 288 bits)?
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/eileen/projects/quilt-gpu-lab")
from tools.transition_kernel import (Markov1, TransitionPredictor,
                                     make_tripartite_transitions, SEED)

D = 9
NOISES = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0, 1.5, 2.0]


def ternarize(x, thr=0.0):
    return np.where(x > thr, 1, np.where(x < -thr, -1, 0))


class LatticeJepa:
    """Per-dim ternary transition table P(after|before,corr), argmax decode."""

    def fit(self, b_tri, c_tri, a_tri):
        # b,c,a: (N,D) int in {-1,0,1}; tab[b+1, c+1, a+1, j] = counts
        self.tab = np.zeros((3, 3, 3, D))
        idx = lambda v: (v + 1).astype(int)
        for j in range(D):
            np.add.at(self.tab[:, :, :, j],
                      (idx(b_tri[:, j]), idx(c_tri[:, j]), idx(a_tri[:, j])), 1)
        return self

    def predict(self, b_tri, c_tri):
        idx = lambda v: (v + 1).astype(int)
        out = np.zeros_like(b_tri)
        for j in range(D):
            counts = self.tab[idx(b_tri[:, j]), idx(c_tri[:, j]), :, j]  # (N,3)
            out[:, j] = counts.argmax(axis=1) - 1
        return out


def run(noise, seed):
    fb, corr, diff_n, fa, _ = make_tripartite_transitions(
        n_agents=8, field_dim=D, n_steps=4000, push=0.5, noise=noise, seed=seed)
    split = int(0.8 * len(fb))
    tr, te = slice(0, split), slice(split, None)

    # ternarize fields with the codec's honest deadband: |x|<=0.15 -> 0
    tb, ta = ternarize(fb, 0.15), ternarize(fa, 0.15)

    # flat JEPA (D19 kernel, continuous), then ternarize its output
    flat = TransitionPredictor().fit(fb[tr], corr[tr].astype(np.float32), fa[tr])
    flat_pred_t = ternarize(flat.predict(fb[te], corr[te].astype(np.float32)), 0.15)

    # markov1 floor, ternarized output
    mk = Markov1().fit(fb[tr], fa[tr])
    mk_pred_t = ternarize(mk.predict(fb[te]), 0.15)

    # lattice JEPA: predict ternary directly from (before_trit, corr_trit)
    lat = LatticeJepa().fit(tb[tr], corr[tr], ta[tr])
    lat_pred = lat.predict(tb[te], corr[te])

    truth = ta[te]
    res = {}
    for name, pred in (("flat_tern", flat_pred_t), ("markov1_tern", mk_pred_t),
                       ("lattice", lat_pred)):
        res[name] = {
            "trit_acc": float((pred == truth).mean()),
            "exact_match": float((pred == truth).all(axis=1).mean()),
        }
    # decoded MSE against continuous field_after (lattice decoded as trits)
    res["lattice"]["decoded_mse"] = float(((lat_pred.astype(np.float32) - fa[te]) ** 2).mean())
    res["flat_tern"]["decoded_mse"] = float(((flat_pred_t.astype(np.float32) - fa[te]) ** 2).mean())
    res["markov1_tern"]["decoded_mse"] = float(((mk_pred_t.astype(np.float32) - fa[te]) ** 2).mean())
    return res


def main():
    runs = []
    for noise in NOISES:
        for seed in [SEED + i for i in range(10)]:
            r = run(noise, seed)
            runs.append({"noise": noise, "seed": seed, **r})
            print("noise=%.2f seed=%d lattice_acc=%.3f flat_acc=%.3f mk1_acc=%.3f"
                  % (noise, seed, r["lattice"]["trit_acc"],
                     r["flat_tern"]["trit_acc"], r["markov1_tern"]["trit_acc"]),
                  flush=True)

    def at(noise, key="trit_acc"):
        rs = [r for r in runs if r["noise"] == noise]
        return float(np.mean([r["lattice"][key] for r in rs])), \
               float(np.mean([r["flat_tern"][key] for r in rs])), \
               float(np.mean([r["markov1_tern"][key] for r in rs]))

    lat_lo, flat_lo, mk_lo = at(0.1)
    lat_all = float(np.mean([r["lattice"]["trit_acc"] for r in runs]))
    flat_all = float(np.mean([r["flat_tern"]["trit_acc"] for r in runs]))
    # G1 across ALL noises: mean lattice within 0.02 of flat
    g1 = lat_all >= flat_all - 0.02
    g2 = True  # definitional: 14.3 bits vs 288 bits (booked)
    g3 = lat_lo >= mk_lo + 0.10
    out = {
        "experiment": "exp3 ternary-structured JEPA (lattice transitions)",
        "n_runs": len(runs), "d": D,
        "bits": {"lattice": np.log2(3 ** D), "flat_float32": 32 * D},
        "gates": {"G1_lattice_within_2pts_flat_all_noises": {"value": [lat_all, flat_all], "pass": g1},
                  "G2_bits_le_5pct": {"value": [np.log2(3 ** D), 32 * D], "pass": g2},
                  "G3_lattice_beats_markov1_by_10pts_at_sigma0.1": {"value": [lat_lo, mk_lo], "pass": g3}},
        "mean_by_noise": {str(n): dict(zip(("lattice", "flat", "markov1"), at(n))) for n in NOISES},
        "runs": runs,
        "verdict": "LATTICE-PASS" if (g1 and g3) else "LATTICE-FAIL",
    }
    with open(os.path.join(HERE, "exp3_out.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote exp3_out.json — verdict:", out["verdict"])


if __name__ == "__main__":
    main()
