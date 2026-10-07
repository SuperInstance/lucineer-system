#!/usr/bin/env python3
"""Shared JEV client for the ternary lane. Reads TYPESAFE_AI_KEY at use-time
from /mnt/c/Users/casey/key.txt (never printed, never persisted)."""
import json
import tempfile
import os
import shutil
import subprocess

KEYFILE = "/mnt/c/Users/casey/key.txt"
URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"


def read_key(name="TYPESAFE_AI_KEY"):
    with open(KEYFILE, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith(name):
                v = line.split("=", 1)[1].strip().strip('"').strip("'")
                if v:
                    return v
    raise RuntimeError(f"{name} not found")


def jev_call(state, questions, timeout_s=60.0, model=MODEL):
    """One System One call. questions: {name: {"type": "noul", "question": ...,
    "instructions": ...}}. Returns {name: noul_float} or raises."""
    key = read_key()
    body = json.dumps({"model": model, "state": state, "questions": questions})
    curl = shutil.which("curl") or "/usr/bin/curl"
    fd, cfg = tempfile.mkstemp(prefix="jev_tern_", suffix=".cfg")
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write('header = "Authorization: Bearer %s"\n' % key)
    try:
        p = subprocess.run(
            [curl, "-sS", "-m", str(int(timeout_s)), "-K", cfg,
             "-H", "Content-Type: application/json", "-X", "POST",
             "-d", body, URL],
            capture_output=True, text=True, timeout=timeout_s + 15)
        if p.returncode != 0:
            raise RuntimeError(f"curl rc={p.returncode}: {p.stderr[:300]}")
        obj = json.loads(p.stdout)
        if "error" in obj:
            raise RuntimeError(f"api error: {obj['error']}")
        out = {}
        for name in questions:
            noul = obj["answers"][name]["noul"]
            out[name] = float(noul)
        return out
    finally:
        try:
            os.unlink(cfg)
        except OSError:
            pass


if __name__ == "__main__":
    r = jev_call(
        "Smoke test state: a scalar trajectory predicted as "
        "0.11 0.14 0.18 0.23 0.27 0.32 0.36 0.41 0.45 0.50; "
        "actual outcome was 0.10 0.13 0.17 0.22 0.26 0.31 0.35 0.40 0.44 0.49.",
        {"q": {"type": "noul",
               "question": "Does the prediction track the actual outcome closely?",
               "instructions": "Answer true (high) only if the predicted values stay within a small tolerance of the actual values at every step."}})
    print("SMOKE_OK", r)
