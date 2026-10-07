#!/usr/bin/env python3
"""DL1-REAL-JEPA step 1: extract real dial streams, verify encoder/basis (V1/V2),
build latent trajectories (logged cumulative + computed sliding K=16).

Read-only against projects/elephant. Outputs to research/dl1-real-jepa/.
Uses ~/venvs/elephant-gpu numpy (deterministic, no GPU needed here).
"""
import json, os, sys
import numpy as np

ELE = "/home/eileen/projects/elephant"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ELE)

from elephant.field import DIAL_NAMES
from elephant.tapnight import DIAL_BOUNDS, DIAL_CENTER
from elephant.vmf import vmf_fit, zvec  # frozen encoder, verbatim

D = 7
SCALE = 2.0 / np.array([DIAL_BOUNDS[n][1] - DIAL_BOUNDS[n][0] for n in DIAL_NAMES])
CENTER = np.array([DIAL_CENTER[n] for n in DIAL_NAMES])
LO = np.array([DIAL_BOUNDS[n][0] for n in DIAL_NAMES])
HI = np.array([DIAL_BOUNDS[n][1] for n in DIAL_NAMES])

PRIMARY = ["A", "D", "D-cold", "S1", "S2", "S3", "S4a", "S4b", "S5"]
TEST_NIGHTS = ["D-cold", "S4b"]
TRAIN_NIGHTS = ["A", "D", "S1", "S2", "S3", "S4a", "S5"]
K_SLIDE = 16

def load_night(name):
    import glob
    fns = glob.glob(os.path.join(ELE, "data", "nights", f"night-{name}.jsonl"))
    rows = [json.loads(l) for l in open(fns[0]) if l.strip()]
    speaks = [r for r in rows if r["type"] == "speak"]
    return speaks

# ---------------------------------------------------------------- V2: basis
def build_basis():
    from scripts.e2_instrument import (Measurement, corpus_sd, Night,
                                       PRIMARY_NIGHTS)
    from scripts.e2_field import field_readers
    from scripts.reg1_rotation import z_cells, decompose, solve_gen
    nights_list = list(PRIMARY_NIGHTS)
    rn = field_readers()
    sd, _ = corpus_sd([Night(n) for n in nights_list])
    m = Measurement(rn, sd, include_nights=nights_list, presence="canonical")
    cells = z_cells(m)
    dec = decompose(cells, list(range(7)))
    sol = solve_gen(dec["C_room"], dec["C_pers"])
    evecs = sol["evecs"] / np.linalg.norm(sol["evecs"], axis=0, keepdims=True)
    return sol["evals"], evecs

def main():
    out = {"nights": {}}
    streams, logged = {}, {}
    v1_fail = []
    for name in PRIMARY:
        speaks = load_night(name)
        raw = np.array([r["field_raw_after"] for r in speaks], float)
        fits = [(r["seq"], r["fit"]) for r in speaks if r.get("fit")]
        streams[name] = raw
        logged[name] = fits
        # V1 consistency gate on logged fits
        prev_n = 0
        for seq, f in fits:
            mu = np.array(f["mu_hat"])
            ok = (abs(np.linalg.norm(mu) - 1.0) < 1e-6
                  and 0.0 <= f["rho"] <= 0.9995
                  and f["kappa"] > 0.0 and f["n"] >= 10
                  and f["n"] >= prev_n
                  and np.all(np.isfinite(mu)) and np.isfinite(f["kappa"]))
            if not ok:
                v1_fail.append((name, seq))
            prev_n = f["n"]
    print(f"[V1] logged-fit consistency: "
          f"{'PASS' if not v1_fail else 'FAIL ' + str(v1_fail[:5])} "
          f"({sum(len(v) for v in logged.values())} fits over {len(PRIMARY)} nights)")
    if v1_fail:
        sys.exit("V1 hard stop")

    evals, evecs = build_basis()
    filed = json.load(open(os.path.join(ELE, "data", "slope",
                                        "reg1-rotation-results.json")))
    w1 = filed["waves"]["wave1"]["primary_full7"]
    v_star_filed = np.array([w1["v_star"][d] for d in DIAL_NAMES])
    v2_filed = np.array([w1["v2"][d] for d in DIAL_NAMES])
    c1 = abs(float(evecs[:, 0] @ v_star_filed))
    c2 = abs(float(evecs[:, 1] @ v2_filed))
    print(f"[V2] basis reproduction: cos(v*, filed v*) = {c1:.6f}, "
          f"cos(v2, filed v2) = {c2:.6f} "
          f"{'PASS' if c1 > 0.999 and c2 > 0.999 else 'FAIL'}")
    if not (c1 > 0.999 and c2 > 0.999):
        sys.exit("V2 hard stop")

    B = evecs.T  # rows: v*, v2..v7 (z-space, Euclidean-normalized)
    def latent(mu_hat, kappa, rho):
        return np.array([B[0] @ mu_hat, np.log1p(kappa), rho,
                         B[1] @ mu_hat, B[2] @ mu_hat, B[3] @ mu_hat,
                         B[4] @ mu_hat])

    # channel A: logged cumulative
    latA = {}
    for name in PRIMARY:
        latA[name] = [(seq, latent(np.array(f["mu_hat"]), f["kappa"], f["rho"]))
                      for seq, f in logged[name]]
    # channel B: computed sliding K=16 on raw streams
    latB = {}
    for name in PRIMARY:
        zs = [SCALE * (v - CENTER) for v in streams[name]]
        zs = [z for z in zs if np.linalg.norm(z) > 1e-3]
        seqs = []
        lats = []
        for i in range(K_SLIDE, len(streams[name]) + 1):
            sample = zs[:i][-K_SLIDE:]
            if len(sample) < 10:
                continue
            f = vmf_fit(sample, B=2)  # tiny bootstrap (CIs unused, keeps solver path)
            if f is None:
                continue
            seqs.append(i - 1)  # index of last speak in window
            lats.append(latent(f["mu_hat"], f["kappa"], f["rho"]))
        latB[name] = (seqs, lats)

    np.savez_compressed(
        os.path.join(HERE, "real_latents.npz"),
        basis=evecs, evals=evals, scale=SCALE, center=CENTER, lo=LO, hi=HI,
        **{f"raw_{n}": streams[n] for n in PRIMARY},
        **{f"latA_{n}": np.array([l for _, l in latA[n]]) for n in PRIMARY},
        **{f"seqA_{n}": np.array([s for s, _ in latA[n]]) for n in PRIMARY},
        **{f"latB_{n}": np.array(latB[n][1]) for n in PRIMARY},
        **{f"seqB_{n}": np.array(latB[n][0]) for n in PRIMARY},
    )
    totA = sum(len(latA[n]) for n in PRIMARY)
    totB = sum(len(latB[n][1]) for n in PRIMARY)
    print(f"[DATA] speaks/night: "
          + ", ".join(f"{n}:{len(streams[n])}" for n in PRIMARY))
    print(f"[DATA] latent points: channelA(logged)={totA}, channelB(sliding16)={totB}")
    print(f"[DATA] test nights {TEST_NIGHTS}: "
          + ", ".join(f"{n}: A={len(latA[n])} B={len(latB[n][1])}"
                      for n in TEST_NIGHTS))
    json.dump({"v1": "PASS", "v2": {"cos_vstar": c1, "cos_v2": c2},
               "gen_evals": [float(x) for x in evals],
               "basis": {f"v{i+1}": {d: float(evecs[j, i]) for j, d in
                                     enumerate(DIAL_NAMES)} for i in range(7)},
               "n_latents_A": totA, "n_latents_B": totB,
               "test_nights": TEST_NIGHTS, "train_nights": TRAIN_NIGHTS},
              open(os.path.join(HERE, "extract-verify.json"), "w"), indent=1)
    print("[OK] saved real_latents.npz + extract-verify.json")

if __name__ == "__main__":
    main()
