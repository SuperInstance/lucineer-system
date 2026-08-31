#!/usr/bin/env python3
"""Mood-board batch generator: quilt-scratch concepts via Cloudflare Workers AI (flux-1-schnell).

Reads the wrangler OAuth token, generates 12 images with a consistent style block,
decodes to assets/concepts/. Subprocess list-form only (house law).
"""
import base64
import json
import os
import subprocess
import sys
import time

REPO = "/home/eileen/projects/quilt-scratch"
OUT = os.path.join(REPO, "assets", "concepts")
ACCOUNT = "049ff5e84ecf636b53b162cbb580aae6"
MODEL = "@cf/black-forest-labs/flux-1-schnell"

STYLE = (
    "1990s children's edutainment software illustration, flat chunky cartoon style, "
    "thick dark outlines, bright saturated primary colors (red, yellow, cyan, grass green), "
    "simple rounded geometric shapes, plain pale background, wholesome goofy energy, "
    "like a ridiculous Rube Goldberg machine from a 1994 kids game, no text, no words, "
    "no letters, no watermark"
)

CONCEPTS = [
    ("01-springboot-mouse", "a wind-up toy mouse wearing giant red spring boots bouncing down a hallway between oversized cartoon gears and springs, motion lines, delighted expression"),
    ("02-balloon-crane", "a huge red party balloon lifting a treasure chest on a rope over a kid's treehouse, a tiny cartoon fan blowing air at the balloon"),
    ("03-cannon-elevator", "a friendly brass cannon mounted on a tower firing a happy kid in a padded capsule upward toward a platform, puffs of smoke shaped like stars"),
    ("04-monkey-generator-belt", "a cheerful monkey pedaling a stationary bicycle connected by a spinning rubber belt to a generator lightbulb, bowling balls riding a conveyor belt beside it"),
    ("05-teeter-totter-launch", "a giant red teeter-totter catapult: a bowling ball drops on one end and launches a giggling kid in a helmet toward a big yellow trampoline"),
    ("06-scissors-balloon-bucket", "a giant cartoon safety scissors on a wooden stand about to pop an enormous yellow balloon that is lifting a bucket of water, a mouse watching expectantly"),
    ("07-corkscrew-marble-run", "a colorful marble run with a corkscrew spiral tube, round pinball bumpers that light up, and a shiny red marble zooming through"),
    ("08-builder-staircase", "a chain of tiny helmeted builders in blue overalls passing bricks and building a staircase across a gap over a canyon, teamwork, hard hats"),
    ("09-antigravity-pad", "a glowing purple anti-gravity pad on the floor flipping wooden crates upward so they float to the ceiling of a cartoon warehouse, arrows pointing up"),
    ("10-flooz-pipes", "glowing green liquid flowing through a maze of colorful pipe segments on a square grid board, pipes curving and crossing, gushing from a faucet"),
    ("11-three-specialists", "three cartoon vikings standing on a wheeled machine platform: one big with a round shield, one small and fast, one with a bow, teamwork puzzle vibes"),
    ("12-key-gate-machine", "a giant golden key floating toward an ornate mechanical gate lock with gears and tumblers, glowing bit-lights showing unlocked, confetti sparks"),
]

TOKEN = None
with open(os.path.expanduser("~/.wrangler/config/default.toml")) as f:
    for line in f:
        if "oauth_token" in line and '"' in line:
            TOKEN = line.split('"')[1]
if not TOKEN:
    sys.exit("no wrangler oauth token found")

os.makedirs(OUT, exist_ok=True)
ok, fail = 0, 0
for name, subject in CONCEPTS:
    dest = os.path.join(OUT, f"{name}.jpg")
    if os.path.exists(dest):
        print(f"[skip] {name} exists")
        ok += 1
        continue
    payload = json.dumps({"prompt": f"{STYLE}: {subject}", "steps": 4})
    body = json.dumps(payload).encode()  # curl --data-binary @-
    cmd = [
        "curl", "-sS", "-X", "POST",
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/{MODEL}",
        "-H", f"Authorization: Bearer {TOKEN}",
        "-H", "Content-Type: application/json",
        "-d", payload,
        "-o", "/tmp/qs-flux-one.json",
        "-w", "%{http_code}",
    ]
    code = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    try:
        with open("/tmp/qs-flux-one.json") as f:
            d = json.load(f)
        b64 = d["result"]["image"]
        data = base64.b64decode(b64)
        with open(dest, "wb") as f:
            f.write(data)
        print(f"[ok] {name}: {code}, {len(data)//1024} KB")
        ok += 1
    except Exception as e:  # noqa: BLE001
        print(f"[FAIL] {name}: http={code} err={e}")
        fail += 1
    time.sleep(1.5)

print(f"done: {ok} ok, {fail} failed of {len(CONCEPTS)}")
