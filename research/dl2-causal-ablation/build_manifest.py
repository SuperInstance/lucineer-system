#!/usr/bin/env python3
"""DL2: build manifest.json — freeze sample ids per arm (seed 202), retrain marginal-null RF."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "jev-jepa-meta"))
from common import load_transitions, load_judgments, features
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, "..", "jev-jepa-meta")
rng = np.random.default_rng(202)

recs = load_transitions()
clean = [r for r in recs if r["clean"]]
jd = load_judgments()

def d(r, k): return r["after"][k] - r["before"][k]

ACTIVE = {
    "C1_thermo_rh":      lambda r: abs(d(r, "temp_c")) > 0.5,
    "C2_occupants_co2":  lambda r: d(r, "occupants") != 0,
    "C3_vent_co2":       lambda r: d(r, "door_open_frac") > 0.2 or d(r, "air_flow_ms") > 0.15,
    "C4_vent_pm25":      lambda r: d(r, "door_open_frac") > 0.2 and abs(r["before"]["pm25"] - r["env"]["outdoor_pm25"]) > 4,
    "C5_vent_temp":      lambda r: d(r, "door_open_frac") > 0.2 and abs(r["before"]["temp_c"] - r["env"]["outdoor_temp_c"]) > 5,
    "C6_lights_lux":     lambda r: r["before"]["lights_on"] != r["after"]["lights_on"],
    "C7_mug_room":       lambda r: abs(r["before"]["mug_temp_c"] - r["before"]["temp_c"]) > 3 and abs(d(r, "mug_temp_c")) > 0.3,
    "C8_door_airflow":   lambda r: d(r, "door_open_frac") != 0,
    "C9_occupants_sound":lambda r: d(r, "occupants") != 0,
    "C10_vent_sound":    lambda r: d(r, "door_open_frac") > 0.2,
    "C11_heater_temp":   lambda r: (not r["before"]["heater_on"]) and r["after"]["heater_on"],
}
PROBES = {
    "P1_rain_humidity":  lambda r: r["env"]["outdoor_scene"] == "light rain" and d(r, "door_open_frac") == 0 and abs(d(r, "humidity_pct")) < 1,
    "P2_night_lux":      lambda r: r["env"]["time_of_day"] == "night" and not r["after"]["lights_on"] and r["after"]["light_lux"] > 200,
    "P3_co2_empty":      lambda r: r["before"]["occupants"] == 0 and r["after"]["occupants"] == 0,
    "P4_noedge_lux_rh":  lambda r: abs(d(r, "light_lux")) > 200 and d(r, "door_open_frac") == 0 and abs(d(r, "temp_c")) < 0.3,
}

def sample(pool, n):
    ids = [r["id"] for r in pool]
    if len(ids) <= n: return sorted(ids)
    idx = rng.choice(len(ids), size=n, replace=False)
    return sorted([ids[i] for i in idx])

manifest = {"couplings": {}, "probes": {}, "sham": {}}
for cid, fn in ACTIVE.items():
    pool = [r for r in clean if fn(r)]
    manifest["couplings"][cid] = {"n_active": len(pool), "ids": sample(pool, 20)}
for pid, fn in PROBES.items():
    pool = [r for r in clean if fn(r)]
    manifest["probes"][pid] = {"n_active": len(pool), "ids": sample(pool, 15)}
# sham: inactive-set samples, 12 each
for cid, fn in ACTIVE.items():
    pool = [r for r in clean if not fn(r)]
    manifest["sham"][cid] = {"n_active": len(pool), "ids": sample(pool, 12)}

# ---- marginal-null RF on all 500 ----
X = np.stack([features(r) for r in recs])
y = np.array([jd[r["id"]]["raw"]["valid"]["noul"] for r in recs])
cl = np.array([r["clean"] for r in recs])
tr, te = train_test_split(np.arange(len(recs)), test_size=0.2, random_state=7, stratify=cl)
rf_check = RandomForestRegressor(400, random_state=0, n_jobs=-1).fit(X[tr], y[tr])
p = rf_check.predict(X[te])
r2 = 1 - np.sum((p - y[te])**2) / np.sum((y[te] - y[te].mean())**2)
rf = RandomForestRegressor(400, random_state=0, n_jobs=-1).fit(X, y)
import pickle
with open(os.path.join(HERE, "rf_null.pkl"), "wb") as f:
    pickle.dump(rf, f)
manifest["rf_gate"] = {"heldout_r2": float(r2),
                       "heldout_spearman": float(spearmanr(p, y[te]).statistic),
                       "gate_pass": bool(0.70 <= r2 <= 0.90)}
# extra drift-check originals: 20 clean not used anywhere
used = set()
for sec in ("couplings", "probes", "sham"):
    for v in manifest[sec].values(): used.update(v["ids"])
rest = [r["id"] for r in clean if r["id"] not in used]
manifest["drift_check_ids"] = sorted(np.random.default_rng(11).choice(rest, size=20, replace=False).tolist())
with open(os.path.join(HERE, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=1)
print("RF gate:", manifest["rf_gate"])
print("arm sizes:", {k: len(v["ids"]) for k, v in manifest["couplings"].items()})
print("probes:", {k: len(v["ids"]) for k, v in manifest["probes"].items()})
uniq = set()
for sec in ("couplings", "probes"):
    for v in manifest[sec].values(): uniq.update(v["ids"])
print("unique originals to (re)judge:", len(uniq), "sham ids:", sum(len(v['ids']) for v in manifest['sham'].values()))
