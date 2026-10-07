#!/usr/bin/env python3
"""JEPA<->JEV bilateral dialogue experiments (Lane 1).

Simulated JEPA predictor (numpy room-state dynamics) judged by JEV
(api.typesafe.ai System One, noul-graded gates). Key read at runtime from
env TYPESAFE_AI_KEY (never stored).

Experiments:
  1. Predict -> Judge baseline (10 diverse transitions)
  2. Judge -> Predict reversed (JEV range gates constrain next prediction)
  3. Iterative calibration (3-round conversation, 3 trajectories)
  4. Calibration drift (50 trials, known ground truth, ROC/threshold)
"""
import json, os, sys, time
import numpy as np
import requests

API = "https://api.typesafe.ai/v1/systemone"
KEY = os.environ["TYPESAFE_AI_KEY"]
MODEL = "jev-latest"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogue-results.json")

DIMS = ["coherence", "v_star_projection", "kappa", "energy", "entropy", "symmetry", "momentum"]
BOUNDS = {"coherence": (0.3, 0.9), "v_star_projection": (-0.5, 0.8), "kappa": (1.0, 5.0),
          "energy": (0.0, 1.0), "entropy": (0.0, 1.0), "symmetry": (0.0, 1.0), "momentum": (-1.0, 1.0)}

LEGEND = ("Room state is a 7D latent: coherence [0.3,0.9] = internal consistency of the room; "
          "v_star_projection [-0.5,0.8] = projection onto the target manifold direction v*; "
          "kappa [1,5] = curvature/stiffness of the state manifold; energy [0,1]; entropy [0,1]; "
          "symmetry [0,1]; momentum [-1,1] = velocity along v*.")

VALIDITY_INSTR = ("A valid one-step room evolution requires: (1) smooth, small changes in every "
                  "dimension (no abrupt jumps), (2) v_star_projection evolving consistently with "
                  "coherence (they are correlated: higher coherence pulls v* up), (3) kappa changing "
                  "slowly (stiffness does not teleport), (4) deltas consistent with continuous "
                  "dynamics rather than independent resampling of each dimension. Answer true only "
                  "if the predicted next state is a plausible one-step evolution of the current state.")

_usage = {"calls": 0, "input_tokens": 0, "output_tokens": 0}

def call_jev(state, questions, retries=4):
    payload = {"model": MODEL, "state": state, "questions": questions}
    last = None
    for i in range(retries):
        try:
            r = requests.post(API, headers={"Authorization": f"Bearer {KEY}",
                                            "Content-Type": "application/json"},
                              json=payload, timeout=90)
            if r.status_code == 200:
                j = r.json()
                u = j.get("usage", {})
                _usage["calls"] += 1
                _usage["input_tokens"] += u.get("input_tokens", 0)
                _usage["output_tokens"] += u.get("output_tokens", 0)
                time.sleep(0.3)
                return j
            last = f"HTTP {r.status_code}: {r.text[:200]}"
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(3 * (i + 1)); continue
            raise RuntimeError(last)
        except requests.RequestException as e:
            last = str(e); time.sleep(3 * (i + 1))
    raise RuntimeError(f"JEV call failed after {retries} retries: {last}")

def noul_answer(j, name):
    a = j["answers"][name]
    return {"noul": a.get("noul"), "confidence": a.get("confidence"),
            "probabilities": a.get("probabilities"), "model": j.get("model")}

def clip(v, lo, hi): return float(np.clip(v, lo, hi))

# ---------------------------------------------------------------- room dynamics
def base_state(rng):
    c = rng.uniform(0.45, 0.85)
    return {
        "coherence": clip(c, 0.3, 0.9),
        "v_star_projection": clip(0.6 * c - 0.15 + rng.normal(0, 0.08), -0.5, 0.8),
        "kappa": clip(rng.uniform(2.0, 3.4), 1, 5),
        "energy": clip(rng.uniform(0.3, 0.7), 0, 1),
        "entropy": clip(1.1 - c + rng.normal(0, 0.05), 0, 1),
        "symmetry": clip(0.5 * c + rng.normal(0, 0.06), 0, 1),
        "momentum": clip(rng.normal(0.05, 0.15), -1, 1),
    }

def step_plausible(s, rng, lam=1.0, rho=1.0):
    """Smooth AR(1) mean-reverting correlated dynamics. lam=noise scale, rho=correlation weight."""
    n = {}
    c_next = clip(s["coherence"] + 0.15 * (0.62 - s["coherence"]) * rho + rng.normal(0, 0.035 * lam), 0.3, 0.9)
    n["coherence"] = c_next
    n["v_star_projection"] = clip((0.72 + 0.28 * rho) * s["v_star_projection"]
                                  + 0.38 * rho * (c_next - s["coherence"]) + 0.05 * (c_next - 0.5)
                                  + rng.normal(0, 0.045 * lam), -0.5, 0.8)
    n["kappa"] = clip(s["kappa"] + 0.12 * (2.6 - s["kappa"]) * rho + rng.normal(0, 0.14 * lam), 1, 5)
    n["energy"] = clip(s["energy"] + rng.normal(0, 0.035 * lam), 0, 1)
    n["entropy"] = clip(0.88 * s["entropy"] + 0.12 * (1.05 - c_next) + rng.normal(0, 0.035 * lam), 0, 1)
    n["symmetry"] = clip(s["symmetry"] + 0.12 * (0.52 * c_next - s["symmetry"]) * rho + rng.normal(0, 0.035 * lam), 0, 1)
    n["momentum"] = clip(0.85 * s["momentum"] + 0.3 * (n["v_star_projection"] - s["v_star_projection"])
                         + rng.normal(0, 0.035 * lam), -1, 1)
    return n

def step_implausible(s, rng, mag=1.0):
    """Decorrelated jumps: each dim moves independently by a large amount / resamples."""
    n = dict(s)
    n["coherence"] = clip(s["coherence"] + rng.choice([-1, 1]) * rng.uniform(0.18, 0.4) * mag, 0.3, 0.9)
    n["v_star_projection"] = clip(rng.uniform(-0.5, 0.8), -0.5, 0.8)  # full resample, ignores coherence
    n["kappa"] = clip(s["kappa"] + rng.choice([-1, 1]) * rng.uniform(0.9, 2.2) * mag, 1, 5)
    n["energy"] = clip(s["energy"] + rng.choice([-1, 1]) * rng.uniform(0.25, 0.5) * mag, 0, 1)
    n["entropy"] = clip(s["entropy"] + rng.choice([-1, 1]) * rng.uniform(0.25, 0.5) * mag, 0, 1)
    n["symmetry"] = clip(rng.uniform(0.0, 1.0), 0, 1)
    n["momentum"] = clip(-s["momentum"] + rng.choice([-1, 1]) * rng.uniform(0.2, 0.6) * mag, -1, 1)
    return n

def deltas(cur, nxt):
    return {k: round(nxt[k] - cur[k], 4) for k in DIMS}

def round4(s): return {k: round(v, 4) for k, v in s.items()}

def transition_state(cur, nxt, extra=None):
    st = {"context": ("Simulated JEPA predictor (latent dynamics model) proposes the next room state. "
                      + LEGEND),
          "current_room_state": round4(cur),
          "predicted_next_state": round4(nxt),
          "transition_delta": deltas(cur, nxt)}
    if extra: st.update(extra)
    return st

VALIDITY_Q = {"type": "noul",
              "question": "Does this predicted state transition represent a valid room evolution?",
              "instructions": VALIDITY_INSTR}

def judge_transition(cur, nxt, extra=None):
    st = transition_state(cur, nxt, extra)
    j = call_jev(st, {"validity": VALIDITY_Q})
    return noul_answer(j, "validity")

# ================================================================ EXP 1
def exp1():
    rng = np.random.default_rng(6611)
    trials = []
    # 5 plausible (varied noise) + 5 implausible (varied magnitude), shuffled order
    specs = [("plausible", {"lam": 0.4}), ("plausible", {"lam": 1.0}), ("plausible", {"lam": 1.6}),
             ("plausible", {"lam": 0.7}), ("plausible", {"lam": 2.2}),
             ("implausible", {"mag": 0.5}), ("implausible", {"mag": 0.8}), ("implausible", {"mag": 1.0}),
             ("implausible", {"mag": 1.3}), ("implausible", {"mag": 1.6})]
    order = rng.permutation(len(specs))
    for idx in order:
        kind, kw = specs[idx]
        cur = base_state(rng)
        nxt = step_plausible(cur, rng, **kw) if kind == "plausible" else step_implausible(cur, rng, **kw)
        ans = judge_transition(cur, nxt)
        trials.append({"ground_truth": kind, "perturbation": kw, "current": round4(cur),
                       "predicted": round4(nxt), "judgment": ans})
        print(f"[exp1] {kind:12s} {kw} -> noul={ans['noul']} conf={ans.get('confidence')}", flush=True)
    p = [t["judgment"]["noul"] for t in trials if t["ground_truth"] == "plausible"]
    i = [t["judgment"]["noul"] for t in trials if t["ground_truth"] == "implausible"]
    return {"trials": trials,
            "summary": {"plausible_mean_noul": round(float(np.mean(p)), 4),
                        "implausible_mean_noul": round(float(np.mean(i)), 4),
                        "separation": round(float(np.mean(p) - np.mean(i)), 4)}}

# ================================================================ EXP 2
def exp2():
    cur = {"coherence": 0.70, "v_star_projection": 0.30, "kappa": 3.0, "energy": 0.50,
           "entropy": 0.40, "symmetry": 0.36, "momentum": 0.05}
    v_ranges = [(-0.5, -0.2), (-0.2, 0.1), (0.1, 0.4), (0.4, 0.7), (0.7, 0.8)]
    k_ranges = [(1.0, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 5.0)]
    questions = {}
    for j, (lo, hi) in enumerate(v_ranges):
        questions[f"v_range_{j}"] = {
            "type": "noul",
            "question": f"Given current coherence=0.70 and v* projection=0.30, is v* projection in [{lo:+.1f}, {hi:+.1f}] a valid range for the NEXT state?",
            "instructions": ("Judge range validity for a one-step evolution: v* moves smoothly (small "
                             "delta, typically |delta| < 0.15) and stays consistent with coherence 0.70. "
                             "Answer true only if the whole range is reachable in one plausible step.")}
    for j, (lo, hi) in enumerate(k_ranges):
        questions[f"k_range_{j}"] = {
            "type": "noul",
            "question": f"Given current kappa=3.0, is kappa in [{lo:.1f}, {hi:.1f}] a valid range for the NEXT state?",
            "instructions": ("Judge range validity for a one-step evolution: kappa is manifold stiffness, "
                             "it evolves slowly (one-step |delta| < 0.5). Answer true only if the whole "
                             "range is reachable in one plausible step.")}
    st = {"context": ("Constraint-elicitation round: before the predictor (JEPA) emits its next "
                      "prediction, the judge (you) states which next-state ranges are valid. " + LEGEND),
          "current_room_state": round4(cur)}
    j = call_jev(st, questions)
    gates = {}
    for name in questions:
        gates[name] = noul_answer(j, name)
        print(f"[exp2] {name}: noul={gates[name]['noul']}", flush=True)
    # accepted ranges -> constraints for the JEPA prediction
    acc_v = [v_ranges[i] for i in range(len(v_ranges)) if (gates[f"v_range_{i}"]["noul"] or 0) >= 0.5]
    acc_k = [k_ranges[i] for i in range(len(k_ranges)) if (gates[f"k_range_{i}"]["noul"] or 0) >= 0.5]
    rng = np.random.default_rng(6612)
    nxt = step_plausible(cur, rng, lam=0.6)
    constrained = bool(acc_v and acc_k)
    if constrained:
        vlo, vhi = acc_v[0]; klo, khi = acc_k[len(acc_k) // 2]
        nxt["v_star_projection"] = clip(rng.uniform(vlo, vhi), -0.5, 0.8)
        nxt["kappa"] = clip(rng.uniform(klo, khi), 1, 5)
    # judge the constrained prediction, and an unconstrained (implausible) contrast
    ans_con = judge_transition(cur, nxt, extra={"constraint_round": {
        "accepted_v_ranges": [list(r) for r in acc_v], "accepted_k_ranges": [list(r) for r in acc_k],
        "note": "JEPA sampled its prediction inside the judge-accepted ranges."}})
    nxt_bad = step_implausible(cur, rng, mag=1.0)
    ans_bad = judge_transition(cur, nxt_bad, extra={"constraint_round": {
        "accepted_v_ranges": [list(r) for r in acc_v], "accepted_k_ranges": [list(r) for r in acc_k],
        "note": "Contrast: prediction IGNORES the judge-accepted ranges."}})
    print(f"[exp2] constrained -> noul={ans_con['noul']} | unconstrained contrast -> noul={ans_bad['noul']}", flush=True)
    return {"current": round4(cur), "gates": gates,
            "accepted_v_ranges": [list(r) for r in acc_v], "accepted_k_ranges": [list(r) for r in acc_k],
            "constrained_prediction": round4(nxt), "judgment_constrained": ans_con,
            "unconstrained_contrast_prediction": round4(nxt_bad), "judgment_unconstrained": ans_bad}

# ================================================================ EXP 3
def exp3():
    """3-round conversation x 3 trajectories. JEPA absorbs judgment via (lam, rho) knobs."""
    trajectories = []
    starts = [
        ("A_wild", {"lam": 2.6, "rho": 0.2}),   # starts loud/decorrelated -> likely judged invalid
        ("B_borderline", {"lam": 1.4, "rho": 0.6}),
        ("C_calm", {"lam": 0.5, "rho": 1.0}),   # starts near-valid
    ]
    for name, knobs in starts:
        rng = np.random.default_rng(hash(name) % (2**32))
        cur = base_state(rng)
        lam, rho = knobs["lam"], knobs["rho"]
        rounds = []
        for rnd in range(1, 4):
            # JEPA predicts: blend of correlated dynamics (rho) and decorrelated noise (1-rho)
            good = step_plausible(cur, rng, lam=lam, rho=rho)
            wild = step_implausible(cur, rng, mag=lam / 2.2)
            nxt = {k: round(clip(rho * good[k] + (1 - rho) * wild[k], *BOUNDS[k]), 4) for k in DIMS}
            extra = None
            if rounds:
                extra = {"prior_rounds": [{"round": r["round"], "noul": r["judgment"]["noul"],
                                           "verdict": "valid" if r["judgment"]["noul"] >= 0.5 else "invalid",
                                           "jepa_knobs": r["knobs_after"]} for r in rounds],
                         "note": "JEPA has seen these prior judgments and adjusted its noise scale (lam) "
                                 "and correlation weight (rho) accordingly before emitting this prediction."}
            ans = judge_transition(cur, nxt, extra=extra)
            noul = ans["noul"]
            # absorption rule: invalid -> tame (raise rho, cut lam); valid -> mild exploration
            if noul < 0.5:
                lam = max(0.3, lam * max(0.35, (0.6 - noul)))
                rho = min(1.0, rho + 0.25 * (0.6 - noul))
            else:
                lam = min(2.8, lam * 1.12)
                rho = max(0.1, rho - 0.05)
            rounds.append({"round": rnd, "knobs_before": knobs if rnd == 1 else rounds[-1]["knobs_after"],
                           "prediction": nxt, "judgment": ans,
                           "knobs_after": {"lam": round(lam, 3), "rho": round(rho, 3)}})
            print(f"[exp3:{name}] round {rnd} noul={noul} -> knobs lam={lam:.2f} rho={rho:.2f}", flush=True)
        trajectories.append({"trajectory": name, "start_knobs": knobs, "rounds": rounds,
                             "noul_trajectory": [r["judgment"]["noul"] for r in rounds]})
    return {"trajectories": trajectories}

# ================================================================ EXP 4
def exp4():
    rng = np.random.default_rng(6613)
    cur = {"coherence": 0.62, "v_star_projection": 0.24, "kappa": 2.7, "energy": 0.55,
           "entropy": 0.44, "symmetry": 0.33, "momentum": 0.04}
    trials = []
    labels, nouls, mags = [], [], []
    for t in range(50):
        if t < 25:
            lam = rng.uniform(0.5, 2.0)  # spans borderline
            nxt = step_plausible(cur, rng, lam=lam)
            kind, mag = "plausible", lam
        else:
            mag = rng.uniform(0.5, 1.5)
            nxt = step_implausible(cur, rng, mag=mag)
            kind, mag = "implausible", mag
        ans = judge_transition(cur, nxt)
        trials.append({"trial": t, "ground_truth": kind, "perturbation_scale": round(float(mag), 3),
                       "predicted": round4(nxt), "judgment": ans})
        labels.append(1 if kind == "plausible" else 0); nouls.append(ans["noul"]); mags.append(mag)
        if (t + 1) % 10 == 0: print(f"[exp4] {t+1}/50 done", flush=True)
    nouls = np.array(nouls, dtype=float); labels = np.array(labels)
    # rank-based AUC (plausible should score HIGHER)
    order = np.argsort(nouls); ranks = np.empty(len(nouls)); ranks[order] = np.arange(1, len(nouls) + 1)
    n1, n0 = labels.sum(), (1 - labels).sum()
    auc = (ranks[labels == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    # Youden threshold
    cand = np.unique(nouls)
    best_j, best_thr = -1, None
    for thr in np.concatenate([[cand[0] - 0.01], (cand[:-1] + cand[1:]) / 2, [cand[-1] + 0.01]]):
        pred = nouls >= thr
        tpr = (pred & (labels == 1)).sum() / n1
        fpr = (pred & (labels == 0)).sum() / n0
        jd = tpr - fpr
        if jd > best_j: best_j, best_thr = jd, thr
    p, i = nouls[labels == 1], nouls[labels == 0]
    hist, edges = np.histogram(nouls, bins=10, range=(0, 1))
    return {"initial_state": round4(cur), "trials": trials,
            "stats": {"auc": round(float(auc), 4), "youden_threshold": round(float(best_thr), 4),
                      "youden_j": round(float(best_j), 4),
                      "plausible": {"mean": round(float(p.mean()), 4), "std": round(float(p.std(ddof=1)), 4),
                                    "min": round(float(p.min()), 4), "max": round(float(p.max()), 4)},
                      "implausible": {"mean": round(float(i.mean()), 4), "std": round(float(i.std(ddof=1)), 4),
                                      "min": round(float(i.min()), 4), "max": round(float(i.max()), 4)},
                      "histogram_counts": hist.tolist(), "histogram_edges": [round(float(e), 2) for e in edges]}}

# ================================================================ main
def main():
    t0 = time.time()
    results = {"meta": {"started": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "model_requested": MODEL,
                        "api": API, "note": "JEPA simulated via numpy latent room dynamics; JEV = typesafe System One."},
               "exp1_predict_to_judge": exp1(),
               "exp2_judge_to_predict": exp2(),
               "exp3_iterative_calibration": exp3(),
               "exp4_calibration_drift": exp4(),
               "usage": _usage, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f: json.dump(results, f, indent=1)
    print(f"DONE {results['elapsed_s']}s, {_usage['calls']} calls -> {OUT}", flush=True)

if __name__ == "__main__":
    main()
