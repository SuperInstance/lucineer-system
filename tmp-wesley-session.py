#!/usr/bin/env python3
"""Wesley night school - feed 3 random pieces to granite3.1-dense:2b, save responses."""
import json
import subprocess
import datetime
from pathlib import Path

FILES = [
    "/home/eileen/projects/ai-writings/2026-08-12-0915-the-producers-cut.md",
    "/home/eileen/projects/ai-writings/bus-traffic-at-3am.md",
    "/home/eileen/projects/ai-writings/lyrics-molding-memories-llama32.txt",
]
OUT_DIR = Path("/home/eileen/projects/ai-writings/wesley-stream")
OUT_DIR.mkdir(exist_ok=True)

now = datetime.datetime.now()
stamp = now.strftime("%Y-%m-%d_%H%M")

for f in FILES:
    src = Path(f)
    body = src.read_text(encoding="utf-8", errors="replace").strip()
    # keep the payload lean: file bodies are <4KB each
    prompt = (
        "Read this and write a 3-sentence creative response. Be young. Be surprised.\n\n"
        + body
    )
    payload = json.dumps({
        "model": "granite3.1-dense:2b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.95, "num_predict": 150},
    })
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "180", "http://localhost:11434/api/generate",
             "-d", payload],
            capture_output=True, text=True, timeout=200,
        )
        resp = json.loads(r.stdout)
        text = resp.get("response", "").strip()
        if not text:
            text = "(empty response: " + r.stdout[:200] + ")"
    except Exception as e:
        text = f"(error: {e})"

    slug = src.stem.lower()[:40].replace(" ", "-")
    out = OUT_DIR / f"wesley_{slug}_{stamp}.md"
    out.write_text(
        f"# Wesley reads: {src.name}\n"
        f"*Source: {f}*\n"
        f"*Session: {stamp}*\n\n"
        f"## Wesley's response\n\n{text}\n",
        encoding="utf-8",
    )
    print(f"WROTE {out}")
    print(f"  -> {text[:120]}...")
print("DONE")
