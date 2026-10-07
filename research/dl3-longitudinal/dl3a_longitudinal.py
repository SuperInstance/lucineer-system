#!/usr/bin/env python3
"""DL3a — longitudinal noul tracking on real dial streams.

bar-rail (19 days, ~30-min polls): frozen day-1..3 JEPA kernel, daily residual
series, 2 JEV real-transition probes/day + 1 fixed pin-probe/day (days 4..19).
roomd (2 rooms): frozen 09-03 kernels, residual series over 09-04 + 09-17,
2+2 JEV probes. Verdict rules frozen in PRE-REG.md BEFORE any run.
"""
import datetime
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dl3_common import (B_DIALS, B_Q, R_DIALS, R_Q, SEED, dump, fit_kernel,
                        jev_noul, ledger, load_barrail, load_roomd, perm_p_spearman,
                        render_transition, residual, spearman, thresholds,
                        warmup_receipt)

CALIB_DAYS = ("2026-08-17", "2026-08-18", "2026-08-19")
PROBE_DAYS = None  # all days after calibration
GAP_S = 90 * 60
PIN_STATE = [-0.40, 0.50, 0.60, 0.30, 0.10, 0.20, 0.55, 0.20]
PIN_AFTER = [-0.40, 0.60, 0.60, 0.25, 0.10, 0.20, 0.63, 0.20]


def iso_to_epoch(ts):
    return datetime.datetime.fromisoformat(ts).timestamp()


def main():
    t0 = time.time()
    rec = warmup_receipt(3.0)  # frozen warm-up before timed sections
    rng = np.random.default_rng(SEED)

    rows = load_barrail()
    days = sorted({r["day"] for r in rows})
    # within-day consecutive transitions with gap <= 90 min
    by_day = {d: [] for d in days}
    for r in rows:
        by_day[r["day"]].append(r)
    trans = {}  # day -> list of (b, a)
    for d in days:
        rr = sorted(by_day[d], key=lambda x: x["ts"])
        tt = []
        for a, b in zip(rr[1:], rr):
            if 0 < iso_to_epoch(a["ts"]) - iso_to_epoch(b["ts"]) <= GAP_S:
                tt.append((np.array(b["vec"]), np.array(a["vec"]),
                           iso_to_epoch(b["ts"])))
        trans[d] = tt
    calib = [t for d in CALIB_DAYS for t in trans[d]]
    W = fit_kernel([(b, a) for b, a, _ in calib])
    th = thresholds(W, [(b, a) for b, a, _ in calib])

    # ---- JEV-free daily residual series (all days) -------------------
    daily = []
    for i, d in enumerate(days, 1):
        rs = [residual(W, b, a) for b, a, _ in trans[d]]
        if not rs:
            daily.append({"day": i, "date": d, "n": 0})
            continue
        daily.append({"day": i, "date": d, "n": len(rs),
                      "resid_median": round(float(np.median(rs)), 4),
                      "resid_q95": round(float(np.quantile(rs, 0.95)), 4),
                      "soft_exceed_frac": round(
                          float(np.mean([r > th["soft"] for r in rs])), 4)})

    # ---- JEV probes: days 4..19 --------------------------------------
    probe_days = [d for d in days if d not in CALIB_DAYS]
    pin_text = render_transition(PIN_STATE, PIN_AFTER, B_DIALS,
                                 "30-minute transition")
    probes = []
    for d in probe_days:
        tt = trans[d]
        if not tt:
            probes.append({"date": d, "note": "no transitions"})
            continue
        picks = [tt[i] for i in rng.choice(len(tt), size=min(2, len(tt)),
                                           replace=False)]
        rec_d = {"date": d, "real": []}
        for b, a, ts in picks:
            txt = render_transition(b, a, B_DIALS, "30-minute transition")
            noul = jev_noul(txt, *B_Q)
            rec_d["real"].append({
                "noul": round(noul, 4),
                "residual": round(residual(W, b, a), 4),
                "text": txt, "epoch": ts})
        pin = jev_noul(pin_text, *B_Q)
        rec_d["pin_noul"] = round(pin, 4)
        probes.append(rec_d)
        print("[dl3a B] %s real=%s pin=%.3f (%.0fs)"
              % (d, [r["noul"] for r in rec_d["real"]], pin, time.time() - t0),
              flush=True)

    # ---- roomd arm: frozen 09-03 kernels, probes on 09-04 + 09-17 ----
    rooms = load_roomd()
    r_arm = {}
    roomd_probes = []
    for rn, rrows in rooms.items():
        blocks_all = []
        last = None
        for ts, vec, _m in rrows:
            if last is None or ts - last > 60:
                blocks_all.append([])
            blocks_all[-1].append((ts, vec))
            last = ts
        # 5-min block means within segments
        blocks = []
        for seg in blocks_all:
            t0s = seg[0][0]
            bucket = {}
            for ts, vec in seg:
                bucket.setdefault(int((ts - t0s) // 300), []).append(vec)
            for k in sorted(bucket):
                blocks.append((t0s + k * 300, np.mean(bucket[k], axis=0)))
        d_blocks = {  # date -> [(ts, vec)]
            "2026-09-03": [x for x in blocks
                           if datetime.datetime.fromtimestamp(x[0]).strftime(
                               "%Y-%m-%d") == "2026-09-03"],
            "2026-09-04": [x for x in blocks
                           if datetime.datetime.fromtimestamp(x[0]).strftime(
                               "%Y-%m-%d") == "2026-09-04"],
            "2026-09-17": [x for x in blocks
                           if datetime.datetime.fromtimestamp(x[0]).strftime(
                               "%Y-%m-%d") == "2026-09-17"]}
        tr = [(b, a) for (t1, b), (t2, a) in zip(d_blocks["2026-09-03"],
                                                 d_blocks["2026-09-03"][1:])]
        if len(tr) < 5:
            r_arm[rn] = {"note": "too few 09-03 blocks", "n_train": len(tr)}
            continue
        Wr = fit_kernel(tr)
        thr = thresholds(Wr, tr)
        series = {}
        for dd in ("2026-09-04", "2026-09-17"):
            bl = d_blocks[dd]
            rs = [residual(Wr, b, a) for (t1, b), (t2, a) in zip(bl, bl[1:])]
            series[dd] = {"n": len(rs),
                          "resid_median": round(float(np.median(rs)), 4)
                          if rs else None,
                          "resid_q95": round(float(np.quantile(rs, 0.95)), 4)
                          if rs else None,
                          "soft_exceed_frac": round(
                              float(np.mean([r > thr["soft"] for r in rs])), 4)
                          if rs else None}
        r_arm[rn] = {"thresholds": thr, "series": series}
        # 2 probes on 09-04, 2 on 09-17
        for dd, k in (("2026-09-04", 2), ("2026-09-17", 2)):
            bl = d_blocks[dd]
            pairs = list(zip(bl, bl[1:]))
            if not pairs:
                continue
            picks = [pairs[i] for i in rng.choice(len(pairs),
                                                  size=min(k, len(pairs)),
                                                  replace=False)]
            for (t1, b), (t2, a) in picks:
                txt = render_transition(b, a, R_DIALS, "5-minute transition")
                noul = jev_noul(txt, *R_Q)
                roomd_probes.append({
                    "room": rn, "date": dd, "noul": round(noul, 4),
                    "residual": round(residual(Wr, b, a), 4), "text": txt})
                print("[dl3a R] %s %s noul=%.3f resid=%.3f"
                      % (rn, dd, noul, residual(Wr, b, a)), flush=True)

    # ---- verdicts (rules frozen in PRE-REG) ---------------------------
    ok = [p for p in probes if "real" in p]
    real_means = np.array([np.mean([r["noul"] for r in p["real"]])
                           for p in ok])
    pins = np.array([p["pin_noul"] for p in ok])
    day_idx = np.array([i + 1 for i in range(len(ok))])  # probe order
    sat_hi = float(np.mean(real_means > 0.95))
    sat_lo = float(np.mean(real_means < 0.05))
    saturated = (sat_hi >= 14 / 16) or (sat_lo >= 14 / 16)
    sp_pin = spearman(day_idx, pins)
    p_pin = perm_p_spearman(day_idx, pins)
    sp_real = spearman(day_idx, real_means)
    p_real = perm_p_spearman(day_idx, real_means)
    judge_drift = bool(np.std(pins) > 0.10
                       or (abs(sp_pin) >= 0.5 and p_pin < 0.05))
    stream_drift = bool((np.std(real_means) - np.std(pins)) > 0.05
                        and abs(sp_real) >= 0.5 and p_real < 0.05)
    ds = [d for d in daily if d.get("n", 0) > 0 and d["day"] > 3]
    sp_res = spearman([d["day"] for d in ds], [d["resid_q95"] for d in ds])
    p_res = perm_p_spearman([d["day"] for d in ds], [d["resid_q95"] for d in ds])
    kernel_decay = bool(abs(sp_res) >= 0.5 and p_res < 0.05
                        or any(d.get("soft_exceed_frac", 0) > 0.30 for d in ds))
    if saturated:
        verdict = "SATURATED"
    elif judge_drift and stream_drift:
        verdict = "BOTH_JUDGE_AND_STREAM_DRIFT"
    elif judge_drift:
        verdict = "JUDGE_DRIFT"
    elif stream_drift:
        verdict = "STREAM_DRIFT"
    elif kernel_decay:
        verdict = "KERNEL_DECAY"
    else:
        verdict = "STABLE"

    out = {
        "experiment": "DL3a longitudinal noul tracking (real dial streams)",
        "warmup_receipt": rec,
        "barrail": {
            "days": len(days), "transitions_per_day":
                {d["date"]: d["n"] for d in daily},
            "kernel_thresholds": th,
            "daily_residual_series": daily,
            "jev_probes": probes,
            "pin_probe_text": pin_text,
        },
        "roomd": {"arm": r_arm, "jev_probes": roomd_probes},
        "stats": {
            "n_probe_days": len(ok),
            "real_noul_daily_mean": [round(x, 4) for x in real_means],
            "pin_noul": [round(x, 4) for x in pins],
            "std_real": round(float(np.std(real_means)), 4),
            "std_pin": round(float(np.std(pins)), 4),
            "spearman_day_real": round(sp_real, 4), "p_real": round(p_real, 4),
            "spearman_day_pin": round(sp_pin, 4), "p_pin": round(p_pin, 4),
            "spearman_day_residq95": round(sp_res, 4),
            "p_residq95": round(p_res, 4),
            "saturation_hi_frac": round(sat_hi, 3),
            "saturation_lo_frac": round(sat_lo, 3)},
        "verdict": verdict,
        "jev_ledger": ledger(),
        "wall_s": round(time.time() - t0, 1),
    }
    dump(os.path.join(HERE, "dl3a_out.json"), out)


if __name__ == "__main__":
    main()
