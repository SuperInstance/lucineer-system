"""dl3_common.py — shared loaders/renderers/JEPA/JEV for the DL3 longitudinal lane.

All real data lives under ~/projects/elephant/data. JEV = typesafe SystemOne noul.
Key read at use-time from ~/.config/typesafe/token (never echoed, never logged).
"""
import json
import math
import os
import time
import urllib.request
from pathlib import Path

import numpy as np

ELEPH = Path.home() / "projects" / "elephant" / "data"
TSAFE = "https://api.typesafe.ai/v1/systemone"
TOKEN_FILE = os.path.expanduser("~/.config/typesafe/token")
SEED = 2718

B_DIALS = ["mood", "volume", "earnestness", "cynicism", "joke_landing",
           "panic", "presence", "model_vs_code"]           # bar-rail (8)
N_DIALS = ["mood", "volume", "earnestness", "cynicism",
           "joke_landing", "panic", "presence"]            # nights (7)
R_DIALS = ["mood", "volume", "earnestness", "cynicism", "joke_landing",
           "panic", "presence", "model_vs_code", "vision"]  # roomd (9)

_LEDGER = {"calls": 0, "input_tokens": 0, "output_tokens": 0, "retries": 0}


# ------------------------------------------------------------------ JEV --
def jev_noul(state_text, question, instructions, model="jev-latest", timeout=60):
    with open(TOKEN_FILE) as f:
        tok = f.read().strip()
    payload = {"model": model, "state": state_text,
               "questions": {"q": {"type": "noul", "question": question,
                                   "instructions": instructions}}}
    for attempt in (1, 2, 3):
        try:
            req = urllib.request.Request(
                TSAFE, json.dumps(payload).encode(),
                {"Authorization": "Bearer " + tok,
                 "Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                out = json.loads(r.read())
            _LEDGER["calls"] += 1
            u = out.get("usage", {})
            _LEDGER["input_tokens"] += u.get("input_tokens", 0)
            _LEDGER["output_tokens"] += u.get("output_tokens", 0)
            return float(out["answers"]["q"]["noul"])
        except Exception as e:
            _LEDGER["retries"] += 1
            if attempt == 3:
                raise RuntimeError("JEV failed 3x: %r" % e)
            time.sleep(2 + attempt)


def ledger():
    return dict(_LEDGER)


def dump(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
    print("wrote", path)


# ------------------------------------------------------------- warm-up --
def warmup_receipt(seconds=3.0):
    """Numeric-stack warm-up before any timed section (GPU absent; CPU receipt)."""
    t0 = time.time()
    a = np.random.default_rng(0).normal(size=(200, 200))
    while time.time() - t0 < seconds:
        a @ a
        np.linalg.svd(a[:50, :50], full_matrices=False)
    return {"warmup_s": round(time.time() - t0, 2), "device": "cpu (no GPU on host)",
            "torch_cuda": False}


# ------------------------------------------------------------- loaders --
def load_barrail():
    """bar-rail production log -> list of (iso_ts, day, dial_vec8)."""
    rows = []
    with open(ELEPH / "production-log.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            fld = d.get("field")
            if d.get("ok") and isinstance(fld, dict) and "mood" in fld:
                try:
                    vec = [float(fld[k]) for k in B_DIALS]
                except (KeyError, TypeError, ValueError):
                    continue
                rows.append({"ts": d["ts"], "day": d["ts"][:10], "vec": vec})
    return rows


def load_roomd():
    """roomd log -> {room: [(epoch_ts, vec9, n_messages)]} in file order."""
    rooms = {}
    with open(ELEPH / "roomd-field-log.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            for rn, r in d.get("rooms", {}).items():
                dd = r.get("dials", {})
                if len(dd) == 9:
                    try:
                        vec = [float(dd[k]) for k in R_DIALS]
                    except (KeyError, TypeError, ValueError):
                        continue
                    rooms.setdefault(rn, []).append(
                        (d["ts"], vec, r.get("messages", 0)))
    return rooms


def roomd_blocks(room_rows, block_s=300.0, gap_s=60.0):
    """2s stream -> 5-min block means within continuous segments."""
    blocks = []
    cur, last_ts = [], None
    for ts, vec, _m in room_rows:
        if last_ts is not None and ts - last_ts > gap_s and cur:
            blocks.append(cur)
            cur = []
        cur.append((ts, vec))
        last_ts = ts
    if cur:
        blocks.append(cur)
    out = []
    for seg in blocks:
        t0 = seg[0][0]
        bucket = {}
        for ts, vec in seg:
            bucket.setdefault(int((ts - t0) // block_s), []).append(vec)
        for k in sorted(bucket):
            out.append((t0 + k * block_s, np.mean(bucket[k], axis=0)))
    return out


def load_nights():
    """182 sessions -> [{file, roster:{name:{vibe,weights,accl,charisma}},
    field: (n,7) array of field_eff_after}]"""
    files = (sorted((ELEPH / "nights").glob("*.jsonl"))
             + sorted((ELEPH / "wave3").glob("*/*.jsonl"))
             + sorted((ELEPH / "wave4-pilots").glob("*/*.jsonl")))
    sessions = []
    for fn in files:
        so, field = None, []
        with open(fn) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("type") == "session_open":
                    so = d
                elif d.get("type") == "speak" and "field_eff_after" in d:
                    v = d["field_eff_after"]
                    if len(v) == 7:
                        field.append([float(x) for x in v])
        if so and len(field) >= 10:
            roster = {}
            for name, m in so.get("roster", {}).items():
                if isinstance(m, dict) and "vibe" in m:
                    roster[name] = {
                        "vibe": [float(x) for x in m["vibe"]],
                        "weights": [float(x) for x in m.get("dial_weights", [])],
                        "accl": float(m.get("acclimation_rate", 0)),
                        "charisma": float(m.get("charisma", 0))}
            sessions.append({"file": str(fn), "roster": roster,
                             "field": np.array(field)})
    return sessions


# ---------------------------------------------------------------- JEPA --
def fit_kernel(transitions):
    """transitions: list of (before_vec, after_vec). Linear [s,1]->s' lstsq."""
    B = np.array([np.append(b, 1.0) for b, _ in transitions])
    A = np.array([a for _, a in transitions])
    W, *_ = np.linalg.lstsq(B, A, rcond=None)
    return W


def residual(W, b, a):
    return float(np.linalg.norm(np.asarray(a) - np.append(np.asarray(b), 1.0) @ W))


def thresholds(W, transitions):
    rs = [residual(W, b, a) for b, a in transitions]
    return {"soft": float(np.quantile(rs, 0.90)),
            "hard": float(np.quantile(rs, 0.995)),
            "train_n": len(rs)}


# ---------------------------------------------------------- rendering --
def render_state(vec, names):
    return ", ".join("%s=%+.2f" % (n, v) for n, v in zip(names, vec))


def render_transition(b, a, names, horizon):
    d = np.asarray(a) - np.asarray(b)
    parts = ["%s %+.2f" % (n, dv) for n, dv in zip(names, d) if abs(dv) > 0.005]
    desc = "; ".join(parts) if parts else "no dial change"
    return ("Room dial state: %s. Proposed %s: %s."
            % (render_state(b, names), horizon, desc))


B_Q = ("Is this proposed 30-minute room-vibe transition plausible for this room?",
       "Answer true only if the magnitude and direction of every dial change "
       "could occur in 30 minutes of normal conversation dynamics in a quiet "
       "bar room.")
R_Q = ("Is this proposed 5-minute room-vibe transition plausible for this room?",
       "Answer true only if the magnitude and direction of every dial change "
       "could occur in 5 minutes of normal conversation dynamics in a live "
       "conversation room.")
N_Q = ("Is this proposed next-speak room-vibe transition plausible for this "
       "room's trajectory?",
       "Answer true only if the magnitude and direction of every dial change "
       "could occur after one more person speaks in a conversation room like "
       "this.")


# ------------------------------------------------------------- stats --
def wilson(k, n, z=1.96):
    if n == 0:
        return [float("nan")] * 3
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(p, 4), round(c - h, 4), round(c + h, 4)]


def _rank(a):
    a = np.asarray(a, float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a))
    ranks[order] = np.arange(len(a))
    vals, inv, counts = np.unique(a, return_inverse=True, return_counts=True)
    sums = np.zeros(len(vals))
    np.add.at(sums, inv, ranks)
    return (sums / counts)[inv]


def spearman(a, b):
    ra, rb = _rank(a), _rank(b)
    ra, rb = ra - ra.mean(), rb - rb.mean()
    den = math.sqrt(float(ra @ ra) * float(rb @ rb))
    return float(ra @ rb) / den if den > 1e-12 else 0.0


def perm_p_spearman(x, y, perms=2000, seed=SEED):
    """Two-sided permutation p for |spearman(x,y)|."""
    rng = np.random.default_rng(seed)
    obs = abs(spearman(x, y))
    y = np.asarray(y, float)
    hit = 0
    for _ in range(perms):
        hit += abs(spearman(x, rng.permutation(y))) >= obs - 1e-12
    return (hit + 1) / (perms + 1)
