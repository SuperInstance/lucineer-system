#!/usr/bin/env python3
"""Generate just-so README images for sonar-vision via Cloudflare Workers AI.

Zero local compute — pure REST calls to CF Workers AI (FLUX-1-schnell).
Reads the wrangler OAuth token straight from the config file.
"""
import base64
import json
import re
import urllib.request
from pathlib import Path

CFG = Path.home() / ".config/.wrangler/config/default.toml"
ACCOUNT_ID = "049ff5e84ecf636b53b162cbb580aae6"
MODEL = "@cf/black-forest-labs/flux-1-schnell"
OUT = Path("/home/eileen/projects/sonar-vision/docs")

# Read the oauth token directly from the wrangler config
tok = None
text = CFG.read_text()
m = re.search(r'oauth_token = "([^"]+)"', text)
if m:
    tok = m.group(1)
assert tok, "no oauth_token found in wrangler config"

API = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}"

# (filename, prompt) — maritime/sonar "just-so" illustrations
IMAGES = [
    (
        "hero-sonar-sweep.png",
        "A sonar display glowing in a dark ship wheelhouse at night. A green phosphor "
        "radar sweep rotating across a circular display, a bright ping echo arc and a "
        "faint target return blip. Deep navy-blue ocean ambience, nautical instrument "
        "panel, cinematic, moody, high detail.",
    ),
    (
        "signal-waveforms.png",
        "An oscilloscope display showing sonar signal processing: a clean sine wave and "
        "a sweeping linear chirp, glowing green phosphor traces on a black screen, "
        "grid lines, a few amplitude labels. Scientific instrument aesthetic, dark, precise.",
    ),
    (
        "object-tracking.png",
        "A radar plot tracking multiple moving objects over dark water. Several glowing "
        "green target dots connected by dotted trails, each with a small velocity vector "
        "arrow pointing along its course. Range rings and bearing marks on the display. "
        "Top-down nautical chart feel, dark navy with phosphor green.",
    ),
    (
        "spatial-map.png",
        "An occupancy grid map of an underwater harbor floor built from sonar returns. "
        "A top-down grid of small cells where free space is dark navy, occupied obstacles "
        "are bright amber, unknown areas are muted grey. Sonar mapping aesthetic, "
        "clean, geometric, glowing highlights.",
    ),
]

OUT.mkdir(parents=True, exist_ok=True)

for fname, prompt in IMAGES:
    body = json.dumps({"prompt": prompt}).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": f"Bearer {tok}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"FAIL {fname}: {e}")
        continue

    if not data.get("success", True) or "result" not in data:
        print(f"FAIL {fname}: {json.dumps(data)[:300]}")
        continue

    img_b64 = data["result"].get("image")
    if not img_b64:
        print(f"FAIL {fname}: no image field in result")
        continue

    p = OUT / fname
    p.write_bytes(base64.b64decode(img_b64))
    print(f"OK {fname} -> {p} ({p.stat().st_size} bytes)")
