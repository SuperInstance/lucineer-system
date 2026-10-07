"""common.py — shared JEV client + booking utilities for the JEV×JEPA×ternary explore."""
import json
import os
import time
import urllib.error
import urllib.request

TSAFE = "https://api.typesafe.ai/v1/systemone"
TOKEN_FILE = os.path.expanduser("~/.config/typesafe/token")
SEED = 2718

_LEDGER = {"calls": 0, "input_tokens": 0, "output_tokens": 0, "retries": 0}


def jev_noul(state_text, question, instructions, model="jev-latest", timeout=60):
    """One JEV judgment call -> graded confidence float [0,1]."""
    with open(TOKEN_FILE) as f:
        tok = f.read().strip()
    payload = {
        "model": model, "state": state_text,
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


def jev_noul_batch(state_text, questions, model="jev-latest", timeout=90):
    """Multiple noul questions in ONE call. questions: dict name->(q, instr)."""
    with open(TOKEN_FILE) as f:
        tok = f.read().strip()
    qs = {}
    for name, (q, instr) in questions.items():
        qs[name] = {"type": "noul", "question": q, "instructions": instr}
    payload = {"model": model, "state": state_text, "questions": qs}
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
            return {k: float(v["noul"]) for k, v in out["answers"].items()}
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
