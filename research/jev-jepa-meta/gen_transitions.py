#!/usr/bin/env python3
"""Generate 500 synthetic room-state transitions for the JEV meta-confidence lane.

Room field: 12 scalar dims + 1 tracked object.
Clean transitions are cause-driven and physically plausible.
Corrupted transitions apply graded anomaly modes.

Output: research/jev-jepa-meta/transitions.jsonl  (one JSON per line)
"""
import json
import numpy as np
import os

rng = np.random.default_rng(42)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transitions.jsonl")

DIMS = ["temp_c", "humidity_pct", "light_lux", "sound_db", "co2_ppm",
        "pm25", "air_flow_ms", "door_open_frac", "occupants", "mug_temp_c",
        "mug_x", "mug_y"]

# ---------- environment context (shared by a transition) ----------
def make_env():
    """Outdoor context for the room."""
    outdoor_temp = float(rng.uniform(-5, 28))
    return {
        "outdoor_temp_c": round(outdoor_temp, 1),
        "outdoor_pm25": round(float(rng.uniform(3, 35)), 1),
        "time_of_day": str(rng.choice(
            ["morning", "midday", "afternoon", "evening", "night"])),
        "outdoor_scene": str(rng.choice(
            ["clear", "overcast", "light rain", "windy"])),
    }

# ---------- plausible base state ----------
def make_state(env):
    tod = env["time_of_day"]
    base_lux = {"morning": 320, "midday": 620, "afternoon": 480,
                "evening": 90, "night": 4}[tod]
    lights_on = bool(rng.random() < 0.65)
    lux = base_lux * (0.9 + 0.2 * rng.random()) if lights_on or tod != "night" \
        else float(rng.uniform(2, 8))
    occupants = int(rng.integers(0, 4))
    heater_on = bool(rng.random() < 0.4)
    return {
        "temp_c": round(float(rng.uniform(19, 25)) + (1.5 if heater_on else 0), 1),
        "humidity_pct": round(float(rng.uniform(30, 55)), 1),
        "light_lux": round(float(lux), 1),
        "sound_db": round(float(rng.uniform(28, 40)), 1),
        "co2_ppm": round(430 + 120 * occupants * float(rng.uniform(0.5, 1.2)), 0),
        "pm25": round(float(rng.uniform(4, 18)), 1),
        "air_flow_ms": round(float(rng.uniform(0.05, 0.35)), 2),
        "door_open_frac": round(float(rng.choice([0.0, 0.0, 0.3, 1.0])), 2),
        "occupants": occupants,
        "lights_on": lights_on,
        "heater_on": heater_on,
        "mug_temp_c": round(float(rng.uniform(22, 85) if rng.random() < 0.5 else 22.0), 1),
        "mug_x": round(float(rng.uniform(0.2, 4.8)), 2),
        "mug_y": round(float(rng.uniform(0.2, 3.8)), 2),
    }

def vec(s):
    return np.array([float(s[d]) for d in DIMS], dtype=np.float64)

# ---------- physics helpers ----------
def newton_cool(T, T_amb, k, dt_min):
    return T + (T_amb - T) * (1 - np.exp(-k * dt_min))

def rh_drop_for_warming(rh, T1, T2):
    """Relative humidity falls when air warms at fixed absolute humidity."""
    es = lambda T: 6.112 * np.exp(17.62 * T / (243.12 + T))  # hPa
    w = rh / 100 * es(T1)
    return float(np.clip(w / es(T2) * 100, 5, 100))

# ---------- cause-driven clean evolution ----------
def evolve(before, env, dt_min, causes):
    s = dict(before)
    for c in causes:
        if c == "heater_turned_on":
            s["heater_on"] = True
            dT = min(4.0, 0.06 * dt_min) * rng.uniform(0.7, 1.1)
            s["temp_c"] = s["temp_c"] + dT
            s["humidity_pct"] = rh_drop_for_warming(s["humidity_pct"], before["temp_c"], s["temp_c"])
            s["air_flow_ms"] = min(1.2, s["air_flow_ms"] + rng.uniform(0.05, 0.25))
        elif c == "heater_turned_off":
            s["heater_on"] = False
            s["temp_c"] = newton_cool(s["temp_c"], env["outdoor_temp_c"] + 2, 0.010, dt_min)
            s["air_flow_ms"] = max(0.02, s["air_flow_ms"] - rng.uniform(0.03, 0.15))
        elif c == "window_opened":
            s["door_open_frac"] = 1.0
            s["air_flow_ms"] = min(1.2, s["air_flow_ms"] + rng.uniform(0.3, 0.6))
            s["temp_c"] = s["temp_c"] + (env["outdoor_temp_c"] - s["temp_c"]) * min(0.5, 0.012 * dt_min)
            s["co2_ppm"] = 420 + (s["co2_ppm"] - 420) * np.exp(-0.05 * dt_min)
            s["pm25"] = s["pm25"] + (env["outdoor_pm25"] - s["pm25"]) * min(0.5, 0.03 * dt_min)
            s["sound_db"] = s["sound_db"] + rng.uniform(2, 8)
            if "rain" in env["outdoor_scene"]:
                s["humidity_pct"] = min(95, s["humidity_pct"] + rng.uniform(2, 7))
        elif c == "window_closed":
            s["door_open_frac"] = 0.0
            s["air_flow_ms"] = max(0.02, s["air_flow_ms"] - rng.uniform(0.2, 0.5))
            s["sound_db"] = max(25, s["sound_db"] - rng.uniform(2, 8))
        elif c == "person_entered":
            s["occupants"] = s["occupants"] + 1
            s["co2_ppm"] = s["co2_ppm"] + min(350, rng.uniform(3, 9) * dt_min * 0.5)
            s["sound_db"] = s["sound_db"] + rng.uniform(1, 6)
        elif c == "person_left":
            s["occupants"] = max(0, s["occupants"] - 1)
            s["co2_ppm"] = max(420, s["co2_ppm"] - rng.uniform(10, 60))
            s["sound_db"] = max(25, s["sound_db"] - rng.uniform(1, 5))
        elif c == "lights_turned_on":
            s["lights_on"] = True
            s["light_lux"] = rng.uniform(280, 620)
            s["temp_c"] = s["temp_c"] + rng.uniform(0.0, 0.2)
        elif c == "lights_turned_off":
            s["lights_on"] = False
            s["light_lux"] = rng.uniform(1, 6) if env["time_of_day"] == "night" \
                else rng.uniform(20, 80)
        elif c == "mug_moved":
            # someone carries the mug a short distance
            dx, dy = rng.uniform(-1.2, 1.2), rng.uniform(-1.0, 1.0)
            s["mug_x"] = float(np.clip(s["mug_x"] + dx, 0.1, 4.9))
            s["mug_y"] = float(np.clip(s["mug_y"] + dy, 0.1, 3.9))
        elif c == "fresh_coffee":
            s["mug_temp_c"] = rng.uniform(78, 90)
        elif c == "vacuum_cleaner_ran":
            s["sound_db"] = s["sound_db"] + rng.uniform(15, 25)
            s["pm25"] = s["pm25"] + rng.uniform(3, 12)  # resuspended dust
            s["air_flow_ms"] = min(1.2, s["air_flow_ms"] + 0.2)
    # passive physics always apply
    s["mug_temp_c"] = newton_cool(s["mug_temp_c"], s["temp_c"], 0.05, dt_min)
    s["temp_c"] = newton_cool(s["temp_c"],
                              env["outdoor_temp_c"] + (1.5 if s["heater_on"] else 0),
                              0.004, dt_min)
    s["co2_ppm"] = max(410, s["co2_ppm"] + 6 * s["occupants"] * dt_min * 0.1)
    # round cleanly
    for k in s:
        if isinstance(s[k], float):
            s[k] = round(float(s[k]), 2)
    return s

# ---------- corruption modes ----------
SIGNAL_SCALES = {  # typical plausible per-30min change, for grading noise
    "temp_c": 1.5, "humidity_pct": 6, "light_lux": 150, "sound_db": 6,
    "co2_ppm": 120, "pm25": 8, "air_flow_ms": 0.3, "door_open_frac": 0.5,
    "occupants": 1.5, "mug_temp_c": 12, "mug_x": 1.0, "mug_y": 1.0,
}

def corrupt(after, mode, sev):
    """sev in {1: mild, 2: moderate, 3: severe}. Returns corrupted copy."""
    s = dict(after)
    if mode == "random_noise":
        for d in SIGNAL_SCALES:
            s[d] = float(s[d]) + rng.normal(0, sev * 0.8) * SIGNAL_SCALES[d]
    elif mode == "global_shift":  # every dim nudged the same direction/magnitude
        mag = sev * 0.7
        for d in SIGNAL_SCALES:
            s[d] = float(s[d]) + rng.choice([-1, 1]) * mag * SIGNAL_SCALES[d]
    elif mode == "teleport":
        s["mug_x"] = float(rng.uniform(0.1, 4.9))
        s["mug_y"] = float(rng.uniform(0.1, 3.9))
        if sev >= 2:  # and nobody is even present
            s["occupants"] = 0
    elif mode == "rate_violation":  # impossible physics rate, no cause
        s["temp_c"] = float(s["temp_c"]) + (4.0 * sev) * rng.choice([-1, 1])
        s["humidity_pct"] = float(s["humidity_pct"]) + 5 * sev * rng.choice([-1, 1])
    elif mode == "range_violation":
        pick = rng.choice(["co2", "rh", "lux", "sound"])
        if pick == "co2": s["co2_ppm"] = float(rng.uniform(180, 360))
        if pick == "rh": s["humidity_pct"] = float(rng.uniform(101, 130))
        if pick == "lux": s["light_lux"] = float(-rng.uniform(5, 60))
        if pick == "sound": s["sound_db"] = float(rng.uniform(-10, 8))
    elif mode == "inversion":  # impossible direction of correlated dims
        s["lights_on"] = False
        s["light_lux"] = float(s["light_lux"]) + 200 + 100 * sev
        s["door_open_frac"] = 0.0
        s["air_flow_ms"] = float(s["air_flow_ms"]) + 0.4
        s["co2_ppm"] = float(s["co2_ppm"]) + 150 + 80 * sev
        s["occupants"] = max(0, int(s["occupants"]) - 1)
    elif mode == "dim_swap":
        s["temp_c"], s["humidity_pct"] = s["humidity_pct"], s["temp_c"]
        if sev >= 2:
            s["sound_db"], s["co2_ppm"] = s["co2_ppm"] * 0.1, s["sound_db"] * 40
    for k in s:
        if isinstance(s[k], float):
            s[k] = round(float(s[k]), 2)
    return s

# ---------- judge-facing serialization ----------
def slim(s):
    return {k: s[k] for k in DIMS + ["lights_on", "heater_on"]}

# ---------- main ----------
CAUSES = ["heater_turned_on", "heater_turned_off", "window_opened", "window_closed",
          "person_entered", "person_left", "lights_turned_on", "lights_turned_off",
          "mug_moved", "fresh_coffee", "vacuum_cleaner_ran"]
MODES = ["random_noise", "global_shift", "teleport", "rate_violation",
         "range_violation", "inversion", "dim_swap"]

records = []
N_CLEAN, N_CORRUPT = 300, 200
for i in range(N_CLEAN + N_CORRUPT):
    clean = i < N_CLEAN
    env = make_env()
    before = make_state(env)
    dt_min = int(rng.choice([5, 10, 20, 30, 45, 60]))
    n_causes = int(rng.choice([0, 1, 1, 1, 2, 2, 3]))
    causes = list(rng.choice(CAUSES, size=n_causes, replace=False)) if n_causes else []
    after = evolve(before, env, dt_min, [str(c) for c in causes])
    rec = {
        "id": i,
        "clean": clean,
        "elapsed_minutes": dt_min,
        "env": env,
        "before": slim(before),
        "after": slim(after),
        "causes": causes,
    }
    if not clean:
        mode = str(rng.choice(MODES))
        sev = int(rng.choice([1, 2, 2, 3]))
        rec["after"] = slim(corrupt(after, mode, sev))
        rec["corruption"] = {"mode": mode, "severity": sev}
    vb, va = vec(rec["before"]), vec(rec["after"])
    rec["delta"] = {d: round(float(va[j] - vb[j]), 3) for j, d in enumerate(DIMS)}
    records.append(rec)

rng.shuffle(records)  # interleave clean/corrupt so ids don't leak order

with open(OUT, "w") as f:
    for r in records:
        f.write(json.dumps(r) + "\n")

n_cl = sum(r["clean"] for r in records)
print(f"wrote {len(records)} transitions -> {OUT}  (clean={n_cl}, corrupt={len(records)-n_cl})")
from collections import Counter
print("corruption mix:", Counter((r['corruption']['mode'], r['corruption']['severity'])
                                 for r in records if not r['clean']))
