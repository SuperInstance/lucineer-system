#!/usr/bin/env python3
"""Shared helpers: feature building, data loading for the JEV meta lane."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DIMS = ["temp_c", "humidity_pct", "light_lux", "sound_db", "co2_ppm",
        "pm25", "air_flow_ms", "door_open_frac", "occupants", "mug_temp_c",
        "mug_x", "mug_y"]
TOD = ["morning", "midday", "afternoon", "evening", "night"]
SCENE = ["clear", "overcast", "light rain", "windy"]

# typical plausible change magnitude per dimension (for scaling)
SIG = np.array([1.5, 6, 150, 6, 120, 8, 0.3, 0.5, 1.5, 12, 1.0, 1.0])
# typical plausible value scale per dimension (for normalizing states)
VAL = np.array([3.0, 15, 300, 12, 400, 12, 0.3, 0.5, 2.5, 30, 1.5, 1.2])

def load_transitions():
    return [json.loads(l) for l in open(os.path.join(HERE, "transitions.jsonl"))]

def load_judgments():
    out = {}
    for l in open(os.path.join(HERE, "judgments.jsonl")):
        r = json.loads(l)
        out[r["id"]] = r
    return out

def svec(s):
    return np.array([float(s[d]) for d in DIMS])

def env_feats(rec):
    e = rec["env"]
    tod = [1.0 if e["time_of_day"] == t else 0.0 for t in TOD]
    sc = [1.0 if e["outdoor_scene"] == s else 0.0 for s in SCENE]
    return np.array([e["outdoor_temp_c"] / 30.0, e["outdoor_pm25"] / 25.0,
                     rec["elapsed_minutes"] / 60.0] + tod + sc)

def features(rec, after_state=None):
    """Feature vector for (before, after, env). after_state overrides rec['after']."""
    vb = svec(rec["before"])
    va = svec(rec["after"] if after_state is None else after_state)
    d = (va - vb) / SIG                      # scaled delta
    b = (vb - np.array([22.0, 42, 300, 35, 700, 10, 0.3, 0.4, 1.5, 50, 2.5, 2.0])) / VAL
    a = (va - np.array([22.0, 42, 300, 35, 700, 10, 0.3, 0.4, 1.5, 50, 2.5, 2.0])) / VAL
    l2 = np.array([np.linalg.norm(d)])
    l1 = np.array([np.sum(np.abs(d))])
    nshift = np.array([np.sum(np.abs(d) > 1.0)])
    return np.concatenate([b, a, d, l2, l1, nshift, env_feats(rec)])

N_FEATS = features(load_transitions()[0]).shape[0]

def state_from_vec(v, template):
    """Rebuild a state dict from a 12-vector using template for extra keys."""
    s = {d: round(float(v[i]), 3) for i, d in enumerate(DIMS)}
    s["lights_on"] = template["lights_on"]
    s["heater_on"] = template["heater_on"]
    return s
