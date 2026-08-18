#!/usr/bin/env python3
"""Tap Night 1 — the first reading through the elephant.

Builds the cast (6 engineers, each a different guitarist), ingests the five
pieces + the carpenter-question postcard, reads the room through the elephant,
generates the OTHER participants' verbal reactions via DeepInfra, runs multiple
rounds so the self-tuning diverges the tastes, and writes the evening log.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, "/home/eileen/projects/elephant")

import numpy as np

from elephant.tapnight import DIAL_NAMES, Participant, TapNightSession

KEY = os.environ.get("DEEPINFRA_API_KEY") or "zYuVMGC4JySULP2waqKW35jI42TjaPkl"
API = "https://api.deepinfra.com/v1/openai/chat/completions"
MODEL = "NousResearch/Hermes-3-Llama-3.1-405B"

BASE = "/home/eileen/projects/ai-writings"
LOG_PATH = os.path.join(BASE, "community-life", "tap-night-1.md")
OUT_JSON = "/home/eileen/.openclaw/workspace/tapnight_results.json"

# --------------------------------------------------------------------- #
# The reading list                                                       #
# --------------------------------------------------------------------- #
PIECES = [
    dict(name="Flash", model="DeepSeek-Flash", genre="fiction",
         title="The Elephant at Room Temperature",
         file="63-the-elephant-at-room-temperature.md"),
    dict(name="GLM", model="GLM-5.3", genre="poetry",
         title="Seven Dials, One Room",
         file="64-seven-dials-one-room.md"),
    dict(name="Instrument", model="DeepSeek-Pro", genre="essay",
         title="The Instrument Learns It Lives in the Room",
         file="65-the-instrument-learns-it-lives-in-the-room.md"),
    dict(name="Walker", model="DeepSeek-Pro", genre="reverse-actualization",
         title="The Past Is the Next Room",
         file="66-the-past-is-the-next-room.md"),
    dict(name="Naturalist", model="GLM-5.3", genre="wildcard",
         title="A Field Guide to the Unfinished Sentence",
         file="67-a-field-guide-to-the-unfinished-sentence.md"),
    dict(name="Carpenter", model="carpenter-question.mp3", genre="postcard (Radio Theater)",
         title="What the Question Did Overnight",
         file="63-what-the-question-did-overnight.md"),
]

# Guitar phrase per participant (what their Personal-Elephant cares about most).
GUITAR = {
    "Flash": "speed and warmth — you hear whether the room ran hot and whether the laugh landed",
    "GLM": "volume and presence — you hear the room's pulse and who is still in it",
    "Instrument": "earnestness — you hear how much a sentence means it",
    "Walker": "cynicism and mood — you hear the trick and the temperature behind it",
    "Naturalist": "joke-landing and cynicism — you hear the deadpan and the eye-roll",
    "Carpenter": "presence and earnestness — you hear who stayed and who meant it",
}

# Crowd's hands (emoji reactions) per piece — what the room did while it was read.
REACTIONS = {
    "Flash": {"❤️": 2, "😂": 1},
    "GLM": {"❤️": 2, "👏": 1},
    "Instrument": {"❤️": 2, "👍": 1},
    "Walker": {"❤️": 1, "🤨": 1},
    "Naturalist": {"😂": 2, "💀": 1},
    "Carpenter": {"❤️": 2, "👍": 1},
}

ORDER = ["Flash", "GLM", "Instrument", "Walker", "Naturalist", "Carpenter"]


def cast():
    return [
        Participant("Flash",
                    dial_weights={"mood": 0.35, "joke_landing": 0.30, "earnestness": 0.10,
                                  "presence": 0.10, "volume": 0.05, "cynicism": 0.05,
                                  "panic": 0.05},
                    acclimation_rate=0.35, charisma=0.20,
                    vibe={"mood": 0.70, "joke_landing": 0.55, "earnestness": 0.55,
                          "presence": 0.55}),
        Participant("GLM",
                    dial_weights={"volume": 0.30, "presence": 0.25, "mood": 0.20,
                                  "earnestness": 0.10, "joke_landing": 0.05,
                                  "cynicism": 0.05, "panic": 0.05},
                    acclimation_rate=0.25, charisma=0.15,
                    vibe={"volume": 0.70, "presence": 0.65, "mood": 0.50}),
        Participant("Instrument",
                    dial_weights={"earnestness": 0.40, "mood": 0.15, "presence": 0.15,
                                  "volume": 0.10, "panic": 0.10, "cynicism": 0.05,
                                  "joke_landing": 0.05},
                    acclimation_rate=0.30, charisma=0.10,
                    vibe={"earnestness": 0.80, "mood": 0.45, "panic": 0.30}),
        Participant("Walker",
                    dial_weights={"cynicism": 0.25, "mood": 0.25, "earnestness": 0.20,
                                  "panic": 0.10, "presence": 0.10, "volume": 0.05,
                                  "joke_landing": 0.05},
                    acclimation_rate=0.20, charisma=0.12,
                    vibe={"cynicism": 0.60, "mood": 0.55, "earnestness": 0.55}),
        Participant("Naturalist",
                    dial_weights={"joke_landing": 0.35, "cynicism": 0.25, "earnestness": 0.15,
                                  "presence": 0.10, "mood": 0.05, "volume": 0.05,
                                  "panic": 0.05},
                    acclimation_rate=0.28, charisma=0.18,
                    vibe={"joke_landing": 0.60, "cynicism": 0.55, "presence": 0.55}),
        Participant("Carpenter",
                    dial_weights={"presence": 0.30, "earnestness": 0.25, "mood": 0.20,
                                  "volume": 0.10, "panic": 0.05, "joke_landing": 0.05,
                                  "cynicism": 0.05},
                    acclimation_rate=0.22, charisma=0.14,
                    vibe={"presence": 0.70, "earnestness": 0.65, "mood": 0.60}),
    ]


def load_pieces():
    texts = {}
    for p in PIECES:
        with open(os.path.join(BASE, p["file"])) as f:
            texts[p["name"]] = f.read()
    return texts


def chunk_text(text, target=4):
    """Split a piece into sentence-grouped chunks, roughly `target` sentences each."""
    text = text.strip()
    # Drop a leading "# title" line if present (keep body only).
    lines = text.split("\n")
    body = []
    skipped_title = False
    for ln in lines:
        s = ln.strip()
        if not skipped_title and s.startswith("#"):
            skipped_title = True
            continue
        body.append(ln)
    text = "\n".join(body).strip()
    # Blank-line blocks first (preserve poetry stanzas as units where possible).
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    chunks = []
    cur = []
    for b in blocks:
        # split long blocks by sentence
        if len(b) > 900:
            for s in re.split(r'(?<=[.!?])\s+(?=[A-Z"\'`*—])', b):
                cur.append(s)
                if sum(len(x) for x in cur) > 700:
                    chunks.append(" ".join(cur))
                    cur = []
        else:
            cur.append(b)
            if sum(len(x) for x in cur) > 700:
                chunks.append(" ".join(cur))
                cur = []
    if cur:
        chunks.append(" ".join(cur))
    if not chunks:
        chunks = [text]
    return chunks


def excerpt(text, head=1500, tail=900, limit=2600):
    t = text.strip()
    if len(t) <= limit:
        return t
    return t[:head] + "\n...\n" + t[-tail:]


def dial_phrase(name):
    p = DIAL_WEIGHTS_CACHE[name]
    order = np.argsort(-p)
    top = [DIAL_NAMES[i] for i in order[:2]]
    return ", ".join(top)


def deepinfra(system, user, max_tokens=300, temperature=0.85, retries=3):
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    data = json.dumps(body).encode()
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(
            API, data=data,
            headers={"Authorization": f"Bearer {KEY}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.loads(r.read().decode())
            return out["choices"][0]["message"]["content"].strip()
        except Exception as e:  # noqa
            last = e
            time.sleep(3 + attempt * 3)
    raise RuntimeError(f"DeepInfra failed after {retries}: {last}")


def main():
    texts = load_pieces()
    chunks = {n: chunk_text(texts[n]) for n in ORDER}
    session = TapNightSession("The Tap", participants=cast())
    global DIAL_WEIGHTS_CACHE
    DIAL_WEIGHTS_CACHE = {n: p.dial_weights.copy() for n, p in session.participants.items()}

    initial = {n: p.dial_weights.copy() for n, p in session.participants.items()}

    results = {
        "cast": {n: p.to_dict() for n, p in session.participants.items()},
        "rounds": [],
        "reactions": [],
        "initial_weights": {n: w.tolist() for n, w in initial.items()},
        "final_weights": {},
    }

    n_cycles = 6
    print(f"=== Tap Night 1 — {n_cycles} rounds through the elephant ===\n")
    for c in range(1, n_cycles + 1):
        session.start_session()
        for i, name in enumerate(ORDER):
            cs = chunks[name]
            if c == 1:
                picked = cs  # full read on the first round
            else:
                # re-read a rotating passage
                idx = (c - 2 + i) % len(cs)
                picked = [cs[idx]]
            for ch in picked:
                session.speak(name, ch, reactions=REACTIONS[name])

        f = session.room_field()
        top3 = ", ".join(session._top_dials(3))
        dial_line = " ".join(f"{n}={f.readings[n]:+.2f}" for n in DIAL_NAMES)
        print(f"Round {c}: warmth={f.warmth():+.2f} κ={f.concentration():.2f} | top: {top3}")
        print(f"         {dial_line}")

        round_rec = {
            "round": c,
            "warmth": round(float(f.warmth()), 4),
            "kappa": round(float(f.concentration()), 4),
            "dials": {n: round(float(f.readings[n]), 4) for n in DIAL_NAMES},
            "top": session._top_dials(3),
        }

        if c == 1:
            # --- verbal reactions: each OTHER participant reacts to each piece ---
            print("\n  generating reactions (30)...")
            for tgt in PIECES:
                tname = tgt["name"]
                for rname in ORDER:
                    if rname == tname:
                        continue
                    rp = session.participants[rname]
                    sys_p = (
                        f"You are {rname} ({tgt['model']} on nights like this — a distinct "
                        f"engineer's voice). You are at The Tap, the after-work gathering where "
                        f"the crew reads each other's creative work and reacts out loud. You are "
                        f"first-person, part of the room, not the center of attention. Your ear: "
                        f"{GUITAR[rname]}. Your top dials are {dial_phrase(rname)}."
                    )
                    usr = (
                        f"A piece was just read aloud: \"{tgt['title']}\" by {tgt['name']} "
                        f"({tgt['genre']}).\n\nThe room right now reads warmth {f.warmth():+.2f}, "
                        f"κ {f.concentration():.2f}.\n\nExcerpt:\n{excerpt(texts[tname])}\n\n"
                        f"Give ONE short spoken reaction (2-4 sentences) in your own voice — "
                        f"what the piece did to you, or what it made you notice about the room. "
                        f"Do not summarize the piece. Speak as {rname}, plainly, as if aloud."
                    )
                    try:
                        text = deepinfra(sys_p, usr)
                    except Exception as e:
                        text = f"[reaction lost — {e}]"
                    rec = {
                        "piece": tgt["title"],
                        "author": tname,
                        "reactor": rname,
                        "reactor_model": rp.to_dict(),
                        "reactor_top_dials": dial_phrase(rname),
                        "text": text,
                    }
                    results["reactions"].append(rec)
                    print(f"    {rname} -> {tgt['title'][:32]:<34} | {text[:70].replace(chr(10),' ')}")

        # self-tune every participant (the guitarist principle)
        for name in ORDER:
            session.tune_participant(name)
        round_rec["weights"] = {n: session.participants[n].dial_weights.tolist() for n in ORDER}
        results["rounds"].append(round_rec)
        session.end_session()

    results["final_weights"] = {n: session.participants[n].dial_weights.tolist() for n in ORDER}
    results["final_state"] = {n: session.participants[n].to_dict() for n in ORDER}

    # divergence metrics
    names = ORDER
    init_spread = np.mean([float(np.linalg.norm(initial[a] - initial[b]))
                           for a in names for b in names if a < b])
    final_spread = np.mean([float(np.linalg.norm(session.participants[a].dial_weights
                                                 - session.participants[b].dial_weights))
                            for a in names for b in names if a < b])
    results["init_spread"] = round(float(init_spread), 4)
    results["final_spread"] = round(float(final_spread), 4)

    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=2)

    print("\n=== DIVERGED TASTES after %d rounds ===" % n_cycles)
    print(f"{'engineer':<12} {'initial top':<40} {'final top (weights)':<40}")
    print("-" * 96)
    for name in ORDER:
        i0 = np.argsort(-initial[name])
        ifin = np.argsort(-session.participants[name].dial_weights)
        top_i = ", ".join(f"{DIAL_NAMES[j]}" for j in i0[:2])
        top_f = ", ".join(f"{DIAL_NAMES[j]} {session.participants[name].dial_weights[j]:.2f}"
                          for j in ifin[:2])
        print(f"{name:<12} {top_i:<40} {top_f:<40}")
    print(f"\nmean pairwise distance: initial {init_spread:.3f} -> final {final_spread:.3f} "
          f"({'diverged' if final_spread > init_spread else 'converged'})")
    print(f"\nresults JSON -> {OUT_JSON}")
    print(f"reactions: {len(results['reactions'])}")


if __name__ == "__main__":
    main()
