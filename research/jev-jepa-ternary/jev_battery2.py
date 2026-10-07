#!/usr/bin/env python3
"""Battery 2 — JEV judges routing appropriateness + bucket validity at the
OPERATING thresholds (route_optimal from sweep.py).

Per item one call, 2 noul questions:
  q_route  is routing this prediction's signature (a,b,c) to path X appropriate
           given the actual outcome?
  q_filter within its bucket, is this prediction valid enough to act on?

Incremental cache jev-battery2.jsonl.
"""
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from jev_client import jev_call

CACHE = "jev-battery2.jsonl"
LOCK = threading.Lock()
AXES = ["v_star", "kappa", "coh"]
AXNAME = {"v_star": "value level", "kappa": "trend", "coh": "coherence change"}


def tern(x, c, w):
    if x > c + w:
        return 1
    if x < c - w:
        return -1
    return 0


def bucket_of(sc, cfg):
    return (tern(sc["v_star"], *cfg["v_star"]),
            tern(sc["kappa"], *cfg["kappa"]),
            tern(sc["coh"], *cfg["coh"]))


def path_of(sig):
    if sig == (1, 0, 1):
        return "strong_positive_transition"
    if sig == (0, 0, 0):
        return "stable_no_change"
    if sig == (-1, -1, -1):
        return "complete_reversal"
    return "mixed_uncertain"


def fmt(xs):
    return " ".join(f"{x:+.3f}" for x in xs)


def main():
    items = json.load(open("predictions.json"))["items"]
    cfg = json.load(open("operating-config.json"))["thresholds"]
    cfg = {ax: (cfg[ax]["center"], cfg[ax]["width"]) for ax in AXES}

    done = {}
    try:
        with open(CACHE) as f:
            for line in f:
                r = json.loads(line)
                done[r["id"]] = r
    except FileNotFoundError:
        pass
    todo = [it for it in items if it["id"] not in done]
    print(f"{len(done)} cached, {len(todo)} to judge", flush=True)

    t0 = time.time()
    n_err = 0

    def work(it):
        sig = bucket_of(it["sc_pred"], cfg)
        path = path_of(sig)
        state = (
            "A predictive model's ternary routing layer bucketed a prediction "
            "into a 3-trit signature and assigned it a routing path.\n"
            f"PREDICTED: {fmt(it['pred'])}\n"
            f"ACTUAL:    {fmt(it['actual'])}\n"
            "Signature axes: (value level, trend, coherence change), each "
            "scored +1 / 0 / -1 against the layer's thresholds.\n"
            f"This prediction's signature: ({sig[0]:+d}, {sig[1]:+d}, {sig[2]:+d}).\n"
            f"Assigned path: {path}.\n"
            "Path meanings: strong_positive_transition = value clearly above "
            "threshold with rising coherence; stable_no_change = everything "
            "inside its dead-zone; complete_reversal = value below threshold, "
            "falling trend, falling coherence; mixed_uncertain = anything else."
        )
        questions = {
            "q_route": {
                "type": "noul",
                "question": f"Routing: is assigning this prediction to the path '{path}' appropriate given the actual outcome?",
                "instructions": (
                    "Judge whether the assigned path matches what the ACTUAL row justifies. "
                    "Answer true (high) only if the actual outcome supports that path's reading "
                    "(same directional picture, or genuinely indeterminate for mixed_uncertain); "
                    "false if the actual clearly supports a different path."
                ),
            },
            "q_filter": {
                "type": "noul",
                "question": "Filter: within its bucket, is this prediction valid enough to act on (does its implied reading match the actual outcome)?",
                "instructions": (
                    "A prediction is valid if acting on its directional reading would match "
                    "acting on the actual outcome (level up/flat/down, trend up/flat/down). "
                    "Answer true (high) only if the prediction's reading and the actual's "
                    "reading agree closely enough to act on; false if they diverge."
                ),
            },
        }
        last = None
        for attempt in range(3):
            try:
                ans = jev_call(state, questions)
                return {"id": it["id"], "sig": list(sig), "path": path,
                        **{k: round(v, 4) for k, v in ans.items()}}
            except Exception as e:  # noqa: BLE001
                last = e
                time.sleep(1.5 * (attempt + 1))
        return {"id": it["id"], "error": repr(last)[:200]}

    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(work, it): it["id"] for it in todo}
        for n, fut in enumerate(as_completed(futs), 1):
            r = fut.result()
            if "error" in r:
                n_err += 1
            with LOCK, open(CACHE, "a") as f:
                f.write(json.dumps(r) + "\n")
            if n % 50 == 0:
                print(f"  {n}/{len(todo)} ({time.time()-t0:.0f}s, {n_err} err)", flush=True)

    print(f"done in {time.time()-t0:.0f}s, errors={n_err}", flush=True)


if __name__ == "__main__":
    main()
