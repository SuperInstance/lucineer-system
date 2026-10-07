#!/usr/bin/env python3
"""Shared edit functions — verbatim logic from run_ablation.py (coupling edits, probes, sham)."""
import copy, json, os, random

_HERE = os.path.dirname(os.path.abspath(__file__))
manifest = json.load(open(os.path.join(_HERE, "manifest.json")))
recs_src = None
def set_records(r): 
    global recs_src; recs_src = r

FOLLOWER = {"C1_thermo_rh": "humidity_pct", "C2_occupants_co2": "co2_ppm",
            "C3_vent_co2": "co2_ppm", "C4_vent_pm25": "pm25", "C5_vent_temp": "temp_c",
            "C6_lights_lux": "light_lux", "C7_mug_room": "mug_temp_c",
            "C8_door_airflow": "air_flow_ms", "C9_occupants_sound": "sound_db",
            "C10_vent_sound": "sound_db", "C11_heater_temp": "temp_c"}

def sgn(x): return 1.0 if x > 0 else (-1.0 if x < 0 else 0.0)

def edit_state(cid, cond, rec):
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

sham_rng = random.Random(303)
sham_plan = {}
def _build_sham_plan():
    if sham_plan: return
    for cid, ids in manifest["sham"].items():
        dim = FOLLOWER[cid]
        act = manifest["couplings"][cid]["ids"]
        amag = [abs(recs_src[i]["after"][dim] - recs_src[i]["before"][dim]) for i in act]
        delta = sorted(amag)[len(amag)//2] if amag else 0.0
        for i in ids["ids"]:
            sgn_ = 1 if sham_rng.random() < 0.5 else -1
            sham_plan[(cid, i)] = (dim, round(delta * sgn_, 3))

def edit_sham(cid, rec):
    _build_sham_plan()
    dim, delta = sham_plan[(cid, rec["id"])]
    s = copy.deepcopy(rec["after"])
    s[dim] = round(float(rec["before"][dim]) + delta, 2)
    return s
