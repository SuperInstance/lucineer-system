#!/usr/bin/env python3
"""Judge every transition with JEV (typesafe.ai systemone, model jev-latest).

Questions per transition:
  valid    (noul)   : probability the after-state plausibly follows the before-state
  physical (noul)   : every individual change physically possible
  causal   (noul)   : one plausible physical cause explains all changes together
  category (choice) : heating/cooling/ventilation/occupancy/lighting/mechanical/mixed

Output: judgments.jsonl  (append-only, resumable by id+question set)
"""
import json, os, time, urllib.request, urllib.error, random
import concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "transitions.jsonl")
OUT = os.path.join(HERE, "judgments.jsonl")
URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"

def get_key():
    with open("/mnt/c/Users/casey/key.txt") as f:
        for line in f:
            if line.startswith("TYPESAFE_AI_KEY="):
                return line.strip().split("=", 1)[1]
    raise SystemExit("key not found")

KEY = get_key()

def call_jev(payload, tries=5):
    body = json.dumps(payload).encode()
    for attempt in range(tries):
        req = urllib.request.Request(
            URL, data=body, method="POST",
            headers={"Authorization": f"Bearer {KEY}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                wait = (2 ** attempt) + random.random() * 2
                time.sleep(wait)
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(3 + attempt * 3)
            continue
    return None

def payload_for(rec):
    state = {
        "elapsed_minutes": rec["elapsed_minutes"],
        "outdoor": {k: rec["env"][k] for k in
                    ("outdoor_temp_c", "outdoor_pm25", "time_of_day", "outdoor_scene")},
        "state_before": rec["before"],
        "state_after": rec["after"],
    }
    return {
        "model": MODEL,
        "state": state,
        "questions": {
            "valid": {
                "type": "noul",
                "instructions": ("Could state_after plausibly follow from "
                                 "state_before in a real room after elapsed_minutes?"),
                "criteria": {
                    "true": "A physically possible room evolution, everything consistent",
                    "false": "Some change could not happen this way in a real room",
                },
            },
            "physical": {
                "type": "noul",
                "instructions": ("Is every individual quantity in state_after "
                                 "physically possible given state_before "
                                 "(ranges, rates, directions)?"),
                "criteria": {
                    "true": "Each change is within physical possibility",
                    "false": "At least one change violates physics (range, rate, or coupling)",
                },
            },
            "causal": {
                "type": "noul",
                "instructions": ("Does one plausible physical cause (a person, window, "
                                 "heater, lights, appliance, weather) explain the changes "
                                 "together coherently?"),
                "criteria": {
                    "true": "A single coherent cause or passive physics explains it",
                    "false": "Changes look unrelated or simultaneously shifted with no cause",
                },
            },
            "category": {
                "type": "choice",
                "instructions": "What best characterizes the change between the states?",
                "criteria": {
                    "heating": "Room or drink warmed",
                    "cooling": "Room or drink cooled",
                    "ventilation": "Air exchange with outdoors",
                    "occupancy": "People entered, left, or acted",
                    "lighting": "Light changed",
                    "passive": "Little or nothing changed",
                    "mixed": "Several coherent causes together",
                    "unnatural": "Something unphysical or artificial",
                },
            },
        },
    }

def main():
    recs = [json.loads(l) for l in open(SRC)]
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            try:
                done.add(json.loads(l)["id"])
            except Exception:
                pass
    todo = [r for r in recs if r["id"] not in done]
    print(f"{len(done)} judged, {len(todo)} to go")

    lock_write = []
    def work(rec):
        res = call_jev(payload_for(rec))
        if res is None:
            return None
        ans = res.get("answers", {})
        row = {"id": rec["id"], "model": res.get("model"),
               "usage": res.get("usage", {}),
               "raw": ans}
        with open(OUT, "a") as f:
            f.write(json.dumps(row) + "\n")
        return row

    n_ok = n_fail = 0
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = [ex.submit(work, r) for r in todo]
        for i, fu in enumerate(cf.as_completed(futs), 1):
            if fu.result() is None:
                n_fail += 1
            else:
                n_ok += 1
            if i % 50 == 0:
                print(f"  {i}/{len(todo)} done (fail={n_fail})")
    print(f"finished: ok={n_ok} fail={n_fail}")

if __name__ == "__main__":
    main()
