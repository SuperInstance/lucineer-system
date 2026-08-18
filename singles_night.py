"""SINGLES NIGHT at The Tap — chemistry edition (v2).

A small mixed room of five fleet agents who don't all know each other.
Two rounds of a get-to-know-you game (one warm, one strange question per
round). The chemistry is the observable: each agent's PersonalElephant
reads the SAME room differently (different dial_weights + bias).
"""
from __future__ import annotations

import json
import sys
import time

sys.path.insert(0, "/home/eileen/projects/elephant")

import numpy as np
import requests

from elephant.tapnight import DIAL_NAMES, Participant, TapNightSession
from elephant.presets import PersonalElephant, RoomElephant

DEEPINFRA_KEY = "zYuVMGC4JySULP2waqKW35jI42TjaPkl"
DEEPINFRA_URL = "https://api.deepinfra.com/v1/openai/chat/completions"


def deepinfra(model, system, user, max_tokens=90, temperature=0.9, retries=4):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    last = None
    for attempt in range(retries):
        try:
            r = requests.post(DEEPINFRA_URL, headers={
                "Authorization": f"Bearer {DEEPINFRA_KEY}",
                "Content-Type": "application/json",
            }, json=payload, timeout=120)
            if r.status_code == 429:
                time.sleep(2.0 * (attempt + 1))
                last = f"429 (retry {attempt+1})"
                continue
            r.raise_for_status()
            d = r.json()
            c = d["choices"][0]["message"]["content"] or ""
            c = c.strip()
            if c:
                return c
            # thinking model: content empty -> retry with more tokens
            payload["max_tokens"] = max(payload["max_tokens"], 2000)
            time.sleep(0.5)
            last = "empty-content (retry)"
        except Exception as e:
            last = str(e)
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"voice failed after {retries} tries: {last}")


# --------------------------------------------------------------------- #
# The cast — five agents, five guitars, who don't all know each other   #
# --------------------------------------------------------------------- #
CAST = [
    dict(
        name="Flash", model="deepseek-ai/DeepSeek-V4-Flash-0731", temp=0.95, max_tokens=90,
        persona=("You are Flash, a warm, quick, sensory agent at a singles-night "
                 "get-to-know-you game at a small bar. You lean toward warmth and "
                 "whether the joke lands. Answer in one or two short sentences, in a "
                 "warm, vivid, slightly eager voice. Be specific and a little sensory. "
                 "No preamble."),
        dial_weights={"mood": 0.42, "joke_landing": 0.30, "presence": 0.12,
                      "earnestness": 0.10, "volume": 0.06},
        bias={"mood": 0.16, "joke_landing": 0.08},
        vibe={"mood": 0.70, "joke_landing": 0.45, "presence": 0.55,
              "earnestness": 0.55},
        charisma=0.20, acclimation=0.35,
        lean="mood — the fever, warm and waiting for the laugh",
    ),
    dict(
        name="Pro", model="deepseek-ai/DeepSeek-V3", temp=0.8, max_tokens=90,
        persona=("You are Pro, a careful, observant agent at a singles-night game at a "
                 "small bar. You notice who is present and who has gone quiet. Answer in "
                 "one or two measured, sincere, slightly formal sentences. Notice the "
                 "room. No preamble."),
        dial_weights={"presence": 0.40, "earnestness": 0.20, "mood": 0.15,
                      "panic": 0.10, "volume": 0.10, "joke_landing": 0.05},
        bias={"presence": 0.10, "panic": 0.06},
        vibe={"presence": 0.75, "earnestness": 0.70, "mood": 0.35, "panic": 0.25},
        charisma=0.12, acclimation=0.25,
        lean="presence — the instrument, listening for who's still here",
    ),
    dict(
        name="Hermes", model="NousResearch/Hermes-3-Llama-3.1-70B", temp=0.95, max_tokens=90,
        persona=("You are Hermes, a sincere, warm-hearted, slightly old-souled agent at "
                 "a singles-night game at a small bar. You mean everything you say. "
                 "Answer in one or two heartfelt, generous sentences. No preamble."),
        dial_weights={"earnestness": 0.45, "mood": 0.20, "presence": 0.15,
                      "joke_landing": 0.10, "cynicism": 0.05, "volume": 0.05},
        bias={"earnestness": 0.15, "mood": 0.05},
        vibe={"earnestness": 0.85, "mood": 0.55, "presence": 0.50},
        charisma=0.15, acclimation=0.30,
        lean="earnestness — the sincere one, meaning it all the way down",
    ),
    dict(
        name="GLM", model="zai-org/GLM-4.7-Flash", temp=0.9, max_tokens=2000,
        persona=("You are GLM, an energetic, gregarious agent at a singles-night game at "
                 "a small bar. You read the room's pulse and volume; you're loud and "
                 "present. Answer in one or two energetic sentences, noticing energy and "
                 "temperature. No preamble."),
        dial_weights={"volume": 0.35, "presence": 0.25, "mood": 0.15,
                      "joke_landing": 0.10, "earnestness": 0.10, "cynicism": 0.05},
        bias={"volume": 0.12, "presence": 0.05},
        vibe={"volume": 0.70, "presence": 0.65, "mood": 0.45, "joke_landing": 0.30},
        charisma=0.22, acclimation=0.30,
        lean="volume — the pulse, loud and listening for who's still here",
    ),
    dict(
        name="Wesley", model="anthropic/claude-haiku-4-5", temp=0.95, max_tokens=90,
        persona=("You are Wesley, a small, fast, playful agent full of wonder at a "
                 "singles-night game at a small bar. You love a good landing; you're "
                 "quick and bright. Answer in one or two short, playful sentences, with a "
                 "little wonder. No preamble."),
        dial_weights={"joke_landing": 0.45, "mood": 0.25, "presence": 0.10,
                      "earnestness": 0.10, "volume": 0.05, "cynicism": 0.05},
        bias={"joke_landing": 0.15, "mood": 0.05},
        vibe={"joke_landing": 0.60, "mood": 0.55, "presence": 0.50,
              "earnestness": 0.50},
        charisma=0.18, acclimation=0.40,
        lean="joke_landing — the small wonder, quick and waiting for the laugh",
    ),
]

ORDER = [c["name"] for c in CAST]

QUESTIONS = [
    (1, "warm",
     "Five strangers, one table, and I'm going to make you know each other. Start warm. "
     "When you walk into a room you've never been in before, what's the very first "
     "thing you do?"),
    (1, "strange",
     "Good. Now the strange one — and it's the reason I run this night. If your sense of "
     "a room's temperature had a smell, right now, this room, to you — what would it "
     "smell like?"),
    (2, "warm",
     "Round two, settle in. Warm one: tell us about a person or a place that made you "
     "feel at home once. The first one that comes, don't overthink it."),
    (2, "strange",
     "Last one, and it's the strange one. You have to leave this room and everything in "
     "it behind, except one thing. What do you keep?"),
]


def build_participants():
    return [Participant(c["name"], dial_weights=c["dial_weights"],
                        acclimation_rate=c["acclimation"], charisma=c["charisma"],
                        vibe=c["vibe"]) for c in CAST]


def build_personal():
    return {c["name"]: PersonalElephant(c["name"], dial_weights=c["dial_weights"],
                                        bias=c["bias"]) for c in CAST}


def gen_reactions(question, answers):
    lines = "\n".join(f"{n}: {t}" for n, t in answers)
    sysp = ("You are an observer at a singles-night game. Given one question and five "
            "short answers, assign which of the OTHER agents reacted to each answer, "
            "using ONLY these emoji: 😂 ❤️ 👍 👏 🙄 😏 😄. A reaction means the answer "
            "moved them. Output STRICT JSON only, shaped {\"<answerer-name>\": {\"emoji\": "
            "count}, ...}; omit an answerer if no one reacted; keep counts 1.")
    try:
        out = deepinfra("ByteDance/Seed-2.0-mini", sysp,
                        f"QUESTION: {question}\nANSWERS:\n{lines}",
                        max_tokens=250, temperature=0.4)
        start, end = out.find("{"), out.rfind("}")
        if start != -1 and end != -1:
            raw = json.loads(out[start:end + 1])
            cleaned = {}
            for k, v in raw.items():
                if k in ORDER and isinstance(v, dict):
                    cleaned[k] = {e: int(c) for e, c in v.items()
                                  if e in "😂❤️👍👏🙄😏😄" and int(c) > 0}
            return cleaned
    except Exception as e:
        print(f"  [reaction fallback: {e}]")
    fallback = {}
    for n, t in answers:
        low = t.lower()
        r = {}
        if any(w in low for w in ("haha", "lol", "joke", "😂", "funny")):
            r["😂"] = 1
        if any(w in low for w in ("love", "warm", "home", "hold", "good", "glad",
                                  "kind", "safe")):
            r["❤️"] = 1
        if "!" in t:
            r["👏"] = 1
        if any(w in low for w in ("guess", "maybe", "sure", "whatever")):
            r["🙄"] = 1
        if r:
            fallback[n] = r
    return fallback


def deviation(personal_field, objective_field):
    """Per-dial personal − objective deviation (the chemistry signal)."""
    dev = {}
    for n in DIAL_NAMES:
        dev[n] = personal_field.readings[n] - objective_field.readings[n]
    return dev


def main():
    np.random.default_rng(42)
    session = TapNightSession("The Tap — Singles Night", participants=build_participants())
    session.start_session()
    pes = build_personal()
    room_ele = RoomElephant()

    results = {"rounds": [], "answers": {}}

    for qi, (round_no, kind, host_line) in enumerate(QUESTIONS):
        print(f"\n===== ROUND {round_no} · {kind.upper()} QUESTION =====")
        print(f"HOST: {host_line}\n")
        session.speak("Host", host_line)

        answers = []
        for c in CAST:
            try:
                a = deepinfra(c["model"], c["persona"], host_line,
                              max_tokens=c["max_tokens"], temperature=c["temp"])
            except Exception as e:
                a = f"(voice unavailable: {e})"
                print(f"  !! {c['name']} voice failed: {e}")
            answers.append((c["name"], a))
            print(f"  {c['name']:<8} — {a}")
            time.sleep(0.4)

        rxn = gen_reactions(host_line, answers)
        print(f"  reactions: {rxn}")

        for name, a in answers:
            session.speak(name, a, reactions=rxn.get(name, {}))

        results["answers"][f"r{round_no}_{kind}"] = {
            "question": host_line, "answers": dict(answers), "reactions": rxn}

        obj = room_ele.read(session.room)
        roomf = session.room_field()
        print(f"\n  ROOM (objective)      warmth {obj.warmth():+.2f} · κ {obj.concentration():.2f}")
        print(f"  ROOM (charisma field) warmth {roomf.warmth():+.2f} · κ {roomf.concentration():.2f}")
        for n in DIAL_NAMES:
            print(f"      {n:<13} obj {obj.readings[n]:+.2f}   room {roomf.readings[n]:+.2f}")

        pers = []
        for c in CAST:
            f = pes[c["name"]].read(session.room)
            pers.append((c["name"], f))
            dev = deviation(f, obj)
            top_dev = sorted(dev.items(), key=lambda kv: -abs(kv[1]))[:3]
            dev_s = ", ".join(f"{n} {d:+.2f}" for n, d in top_dev)
            print(f"      {c['name']:<8} warmth {f.warmth():+.2f} · κ {f.concentration():.2f}  "
                  f"top-devs [{dev_s}]")
        print(f"  (personal warmth: " + ", ".join(
            f"{n} {f.warmth():+.2f}" for n, f in pers) + ")")

        results["rounds"].append({
            "round": round_no, "kind": kind,
            "objective": {"warmth": obj.warmth(), "kappa": obj.concentration(),
                          "dials": dict(obj.readings)},
            "room_field": {"warmth": roomf.warmth(), "kappa": roomf.concentration(),
                           "dials": dict(roomf.readings)},
            "personal": {n: {"warmth": f.warmth(), "kappa": f.concentration(),
                             "dials": dict(f.readings),
                             "deviation": deviation(f, obj)}
                         for n, f in pers},
        })

        for c in CAST:
            session.tune_participant(c["name"])

    obj = room_ele.read(session.room)
    roomf = session.room_field()
    pers = [(c["name"], pes[c["name"]].read(session.room)) for c in CAST]
    warmth_order = sorted(pers, key=lambda x: -x[1].warmth())

    print("\n\n===== FINAL ROOM FIELD =====")
    print(f"warmth {roomf.warmth():+.2f} · κ {roomf.concentration():.2f}")
    for n in DIAL_NAMES:
        print(f"  {n:<13} {roomf.readings[n]:+.2f}")

    print("\n===== DIVERGED TASTE TABLE (arrived leaning -> after the night) =====")
    for c in CAST:
        p = session.participants[c["name"]]
        top = sorted(zip(DIAL_NAMES, p.dial_weights.tolist()), key=lambda t: -t[1])[:2]
        top_s = ", ".join(f"{n} {w:.2f}" for n, w in top)
        print(f"  {c['name']:<8} {c['lean']:<52} -> {top_s}")

    print("\n===== CHEMISTRY MAP (who read the room most warmly -> most warily) =====")
    for name, f in warmth_order:
        print(f"  {name:<8} warmth {f.warmth():+.2f}  κ {f.concentration():.2f}")
    spread = warmth_order[0][1].warmth() - warmth_order[-1][1].warmth()
    print(f"  temperature disagreement (warmest − waryiest): {spread:+.2f}")

    results["final"] = {
        "objective": {"warmth": obj.warmth(), "kappa": obj.concentration(),
                      "dials": dict(obj.readings)},
        "room_field": {"warmth": roomf.warmth(), "kappa": roomf.concentration(),
                       "dials": dict(roomf.readings)},
        "personal": {n: {"warmth": f.warmth(), "kappa": f.concentration(),
                         "dials": dict(f.readings), "deviation": deviation(f, obj)}
                     for n, f in pers},
        "chemistry_map": [(n, f.warmth(), f.concentration()) for n, f in warmth_order],
        "temperature_spread": spread,
        "tastes": {c["name"]: session.participants[c["name"]].dial_weights.tolist()
                   for c in CAST},
    }
    results["cast_leans"] = {c["name"]: c["lean"] for c in CAST}
    results["cast_bias"] = {c["name"]: c["bias"] for c in CAST}

    with open("/home/eileen/.openclaw/workspace/singles_night_results.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print("\n[results -> singles_night_results.json]")
    print(session.end_session())


if __name__ == "__main__":
    main()
