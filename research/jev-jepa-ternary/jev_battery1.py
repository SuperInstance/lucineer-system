#!/usr/bin/env python3
"""Battery 1 — per-item JEV judgment (axis agreement + internal confidence).

One System One call per item, 4 noul questions batched inside:
  q_v     does the prediction capture the actual's overall level (within ~0.2)?
  q_k     does the prediction capture the actual's direction of change
          (increasing vs stable vs decreasing)?
  q_c     does the prediction capture whether the actual's internal coherence
          rises or falls across its horizon?
  q_conf  is the prediction itself internally consistent / high-confidence?

Incremental cache in jev-battery1.jsonl; safe to re-run. 8 workers, 2 retries.
"""
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from jev_client import jev_call

CACHE = "jev-battery1.jsonl"
LOCK = threading.Lock()


def fmt(xs):
    return " ".join(f"{x:+.3f}" for x in xs)


def state_for(it):
    return (
        "A predictive model produced a scalar latent-trajectory prediction for "
        "the next 10 steps, and the actual outcome was later observed.\n"
        f"PREDICTED: {fmt(it['pred'])}\n"
        f"ACTUAL:    {fmt(it['actual'])}\n"
        "Steps run left to right (oldest to newest)."
    )


QUESTIONS = {
    "q_v": {
        "type": "noul",
        "question": "Value level: does the prediction track the actual's overall level (its average value) within about 0.2?",
        "instructions": "Compare the average height of the two curves. Answer true (high) only if their means differ by less than roughly 0.2.",
    },
    "q_k": {
        "type": "noul",
        "question": "Trend: does the prediction capture the actual's direction of change (increasing, stable, or decreasing) without flipping it?",
        "instructions": "Compare the overall slopes. Answer true (high) only if both trajectories move the same way (both rising, both flat, or both falling); answer false if one rises while the other falls or stays flat against a clear trend.",
    },
    "q_c": {
        "type": "noul",
        "question": "Coherence dynamics: does the prediction capture whether the actual's step-to-step consistency rises or falls from its first half to its second half?",
        "instructions": "Judge each trajectory's first half vs second half: are later steps more consistently directional (coherence rising), similarly consistent (stable), or less consistent (falling)? Answer true (high) only if prediction and actual agree on this.",
    },
    "q_conf": {
        "type": "noul",
        "question": "Ignoring the actual outcome, is the prediction itself internally consistent and trustworthy in form (smooth, coherent, free of scrambling)?",
        "instructions": "Look only at the PREDICTED row. Answer true (high) if it looks like a coherent signal (smooth trend, no random-looking jumps, not suspiciously flat against its own level shifts); false if it looks scrambled, erratic, or degenerate.",
    },
}


def main():
    items = json.load(open("predictions.json"))["items"]
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
        last = None
        for attempt in range(3):
            try:
                ans = jev_call(state_for(it), QUESTIONS)
                return {"id": it["id"], **{k: round(v, 4) for k, v in ans.items()}}
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
            if n % 25 == 0:
                print(f"  {n}/{len(todo)} ({time.time()-t0:.0f}s, {n_err} err)", flush=True)

    print(f"done in {time.time()-t0:.0f}s, errors={n_err}", flush=True)


if __name__ == "__main__":
    main()
