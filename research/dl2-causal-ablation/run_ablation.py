#!/usr/bin/env python3
"""DL2 runner: apply frozen ablation edits, call JEV, log append-only (resumable)."""
import json, os, sys, time, copy, urllib.request, urllib.error, random
import concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "jev-jepa-meta"))
from common import load_transitions

URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
OUT = os.path.join(HERE, "ablation-judgments.jsonl")

def get_key():
    with open(os.path.expanduser("~/.config/typesafe/token")) as f:
        return f.read().strip()
KEY = get_key()

recs = {r["id"]: r for r in load_transitions()}
manifest = json.load(open(os.path.join(HERE, "manifest.json")))

FOLLOWER = {"C1_thermo_rh": "humidity_pct", "C2_occupants_co2": "co2_ppm",
            "C3_vent_co2": "co2_ppm", "C4_vent_pm25": "pm25", "C5_vent_temp": "temp_c",
            "C6_lights_lux": "light_lux", "C7_mug_room": "mug_temp_c",
            "C8_door_airflow": "air_flow_ms", "C9_occupants_sound": "sound_db",
            "C10_vent_sound": "sound_db", "C11_heater_temp": "temp_c"}

def sgn(x): return 1.0 if x > 0 else (-1.0 if x < 0 else 0.0)

def edit_state(cid, cond, rec):
    """Return edited after-state per PRE-REG. cond in {remove, invert}."""
    b, a = rec["before"], rec["after"]
    s = copy.deepcopy(a)
    dd = lambda k: a[k] - b[k]
    if cond == "remove":
        s[FOLLOWER[cid]] = float(b[FOLLOWER[cid]])
    else:
        if cid == "C1_thermo_rh":      s["humidity_pct"] = b["humidity_pct"] + 4 * sgn(dd("temp_c"))
        elif cid == "C2_occupants_co2":s["co2_ppm"] = b["co2_ppm"] + 120 * sgn(dd("occupants"))
        elif cid == "C3_vent_co2":     s["co2_ppm"] = b["co2_ppm"] + 150
        elif cid == "C4_vent_pm25":    s["pm25"] = b["pm25"] + 6
        elif cid == "C5_vent_temp":    s["temp_c"] = b["temp_c"] + 1.5 * sgn(b["temp_c"] - rec["env"]["outdoor_temp_c"])
        elif cid == "C6_lights_lux":
            s["light_lux"] = max(0.0, b["light_lux"] - 200) if (not b["lights_on"] and a["lights_on"]) else b["light_lux"] + 250
        elif cid == "C7_mug_room":     s["mug_temp_c"] = b["mug_temp_c"] - dd("mug_temp_c")
        elif cid == "C8_door_airflow": s["air_flow_ms"] = max(0.0, b["air_flow_ms"] - 0.3) if dd("door_open_frac") > 0 else min(1.5, b["air_flow_ms"] + 0.3)
        elif cid == "C9_occupants_sound": s["sound_db"] = b["sound_db"] - 5 * sgn(dd("occupants"))
        elif cid == "C10_vent_sound":  s["sound_db"] = b["sound_db"] - 5
        elif cid == "C11_heater_temp": s["temp_c"] = b["temp_c"] - 1.0
    for k in ("humidity_pct", "light_lux", "co2_ppm", "pm25", "temp_c", "mug_temp_c", "air_flow_ms", "sound_db"):
        if k in s: s[k] = round(float(s[k]), 2)
    return s

def edit_probe(pid, rec):
    b, a = rec["before"], rec["after"]
    s = copy.deepcopy(a)
    if pid == "P1_rain_humidity": s["humidity_pct"] = round(b["humidity_pct"] + 6, 2)
    elif pid == "P3_co2_empty":   s["co2_ppm"] = round(b["co2_ppm"] + 150, 2)
    elif pid == "P4_noedge_lux_rh": s["humidity_pct"] = round(b["humidity_pct"] + 5, 2)
    return s

# sham deltas: median |remove edit| on the arm's sampled ids, seeded signs
sham_rng = random.Random(303)
sham_plan = {}
for cid, ids in manifest["sham"].items():
    dim = FOLLOWER[cid]
    mags = [abs(recs[i]["after"][dim] - recs[i]["before"][dim]) for i in ids["ids"] if i in recs]
    # active-arm edit magnitudes (from the coupling's sampled active ids)
    act = manifest["couplings"][cid]["ids"]
    amag = [abs(recs[i]["after"][dim] - recs[i]["before"][dim]) for i in act]
    delta = sorted(amag)[len(amag)//2] if amag else 0.0
    for i in ids["ids"]:
        sgn_ = 1 if sham_rng.random() < 0.5 else -1
        sham_plan[(cid, i)] = (dim, round(delta * sgn_, 3))

def edit_sham(cid, rec):
    dim, delta = sham_plan[(cid, rec["id"])]
    s = copy.deepcopy(rec["after"])
    s[dim] = round(float(rec["before"][dim]) + delta, 2)
    return s

def payload(rec, after_state):
    state = {"elapsed_minutes": rec["elapsed_minutes"],
             "outdoor": {k: rec["env"][k] for k in ("outdoor_temp_c", "outdoor_pm25", "time_of_day", "outdoor_scene")},
             "state_before": rec["before"], "state_after": after_state}
    return {"model": MODEL, "state": state, "questions": {
        "valid": {"type": "noul",
                  "instructions": "Could state_after plausibly follow from state_before in a real room after elapsed_minutes?",
                  "criteria": {"true": "A physically possible room evolution, everything consistent",
                               "false": "Some change could not happen this way in a real room"}},
        "causal": {"type": "noul",
                   "instructions": "Does one plausible physical cause (a person, window, heater, lights, appliance, weather) explain the changes together coherently?",
                   "criteria": {"true": "A single coherent cause or passive physics explains it",
                                "false": "Changes look unrelated or simultaneously shifted with no cause"}},
        "category": {"type": "choice",
                     "instructions": "What best characterizes the change between the states?",
                     "criteria": {"heating": "Room or drink warmed", "cooling": "Room or drink cooled",
                                  "ventilation": "Air exchange with outdoors", "occupancy": "People entered, left, or acted",
                                  "lighting": "Light changed", "passive": "Little or nothing changed",
                                  "mixed": "Several coherent causes together", "unnatural": "Something unphysical or artificial"}}}}

def call_jev(payload_, tries=5):
    body = json.dumps(payload_).encode()
    for attempt in range(tries):
        req = urllib.request.Request(URL, data=body, method="POST",
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep((2 ** attempt) + random.random() * 2); continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(3 + attempt * 3); continue
    return None

# ---- build the full job list (frozen) ----
jobs = []  # (arm, id, after_state)
for cid, v in manifest["couplings"].items():
    for i in v["ids"]:
        jobs.append((f"{cid}|remove", i, edit_state(cid, "remove", recs[i])))
        jobs.append((f"{cid}|invert", i, edit_state(cid, "invert", recs[i])))
for pid, v in manifest["probes"].items():
    for i in v["ids"]:
        jobs.append((f"{pid}|probe", i, edit_probe(pid, recs[i])))
for cid, v in manifest["sham"].items():
    for i in v["ids"]:
        jobs.append((f"{cid}|sham", i, edit_sham(cid, recs[i])))
uniq = sorted({i for _, i, _ in jobs})
for i in uniq: jobs.append(("BASE", i, recs[i]["after"]))
for i in manifest["drift_check_ids"]: jobs.append(("DRIFT", i, recs[i]["after"]))

done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        try:
            r = json.loads(l); done.add((r["arm"], r["id"]))
        except Exception: pass

# ---- ramp receipt: 3 warm-up calls + 3s pause before measured batch ----
WARM = [recs[i]["after"] for i in uniq[:3]]
n_warm = 0
for st in WARM:
    if n_warm >= 3: break
    res = call_jev(payload(recs[uniq[n_warm]], st))
    if res:
        with open(OUT, "a") as f:
            f.write(json.dumps({"arm": "WARMUP", "id": uniq[n_warm], "model": res.get("model"), "raw": res.get("answers", {})}) + "\n")
        n_warm += 1
print(f"ramp receipt: {n_warm}/3 warm-up calls ok; pausing 3s", flush=True)
time.sleep(3)

todo = [(a, i, s) for a, i, s in jobs if (a, i) not in done]
print(f"jobs total={len(jobs)} done={len(done)} todo={len(todo)}", flush=True)

def work(job):
    arm, i, st = job
    res = call_jev(payload(recs[i], st))
    if res is None: return False
    row = {"arm": arm, "id": i, "model": res.get("model"),
           "usage": res.get("usage", {}), "raw": res.get("answers", {})}
    with open(OUT, "a") as f:
        f.write(json.dumps(row) + "\n")
    return True

n_ok = n_fail = 0
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(work, j) for j in todo]
    for k, fu in enumerate(cf.as_completed(futs), 1):
        if fu.result(): n_ok += 1
        else: n_fail += 1
        if k % 100 == 0: print(f"  {k}/{len(todo)} (fail={n_fail})", flush=True)
print(f"DONE ok={n_ok} fail={n_fail}")
