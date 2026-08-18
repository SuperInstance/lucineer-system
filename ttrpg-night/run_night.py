"""TTRPG Night at The Tap — run a maritime one-shot through the elephant.

GM (GLM-5.3) runs a fogbound-harbor one-shot for 4 players. Every line of
the night (GM narration + in-character player reactions, generated via
DeepInfra) is ingested into a TapNightSession; the elephant reads the room's
field after each scene, and self-tunes across rounds so the tastes diverge.

Run:  python3 run_night.py
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/eileen/projects/elephant")

import numpy as np

from elephant.tapnight import DIAL_NAMES, Participant, TapNightSession

RXN = json.load(open(os.path.join(HERE, "reactions.json")))

# ---------------------------------------------------------------------- #
# The cast — five personalities, five guitars.                            #
# ---------------------------------------------------------------------- #
def _cast():
    # charisma is deliberately LOW for a one-shot: the crew is at the table
    # LISTENING to the GM's story, not pulling the room — so the story, not the
    # regulars, drives the field. The GM holds a touch more (the narrator).
    return [
        Participant(
            "GM",
            dial_weights={"volume": 0.30, "presence": 0.25, "mood": 0.20,
                          "earnestness": 0.15, "joke_landing": 0.05,
                          "cynicism": 0.03, "panic": 0.02},
            acclimation_rate=0.30, charisma=0.05,
            vibe={"volume": 0.60, "presence": 0.60, "mood": 0.35,
                  "earnestness": 0.50},
        ),
        Participant(
            "Flash",
            dial_weights={"mood": 0.35, "joke_landing": 0.30, "volume": 0.10,
                          "presence": 0.10, "earnestness": 0.10,
                          "cynicism": 0.05},
            acclimation_rate=0.30, charisma=0.02,
            vibe={"mood": 0.60, "joke_landing": 0.50, "volume": 0.45,
                  "presence": 0.45},
        ),
        Participant(
            "Pro",
            dial_weights={"earnestness": 0.40, "mood": 0.15, "panic": 0.15,
                          "presence": 0.10, "volume": 0.10,
                          "cynicism": 0.05, "joke_landing": 0.05},
            acclimation_rate=0.15, charisma=0.02,
            vibe={"earnestness": 0.75, "panic": 0.35, "mood": 0.25},
        ),
        Participant(
            "Hermes",
            dial_weights={"presence": 0.35, "mood": 0.25, "earnestness": 0.20,
                          "volume": 0.10, "joke_landing": 0.05,
                          "cynicism": 0.05},
            acclimation_rate=0.25, charisma=0.02,
            vibe={"presence": 0.70, "mood": 0.50, "earnestness": 0.55},
        ),
        Participant(
            "Wesley",
            dial_weights={"mood": 0.30, "joke_landing": 0.25, "earnestness": 0.20,
                          "volume": 0.15, "presence": 0.10},
            acclimation_rate=0.40, charisma=0.02,
            vibe={"mood": 0.55, "joke_landing": 0.50, "earnestness": 0.50,
                  "volume": 0.50},
        ),
    ]


ORDER = ["Flash", "Pro", "Hermes", "Wesley"]

# GM narration, one per scene. Keywords are chosen so the v0 dials (which
# keyword-match) actually move: the cold open leans warm/present, the tense
# roll leans alarm/urgency (panic), the reversal leans laughter (joke_landing),
# the close leans sincere/present.
GM_NARRATION = {
    1: ("The fog does not drift over Saltveil; it waits. The harbor is soft and "
        "warm and quiet, every mooring line holding its breath. The Tern — an old "
        "cutter, hull scarred like a psalm — speaks before you board, in a voice "
        "like wet rope: 'Board slow. The tide knows you now.' Beyond the sound the "
        "Blackmoor light is dark, and it will not say why. Warm lamps at the dock, "
        "a boat that talks, and four of you who signed on anyway."),
    2: ("Halfway across the sound the fog closes like a hand and the water goes "
        "wrong. Something big passes under the hull — the Tern shudders, a seam "
        "opens, and the sea comes up through the boards. 'All hands!' the boat "
        "cries. 'She's taking water — NOW!' Mara throws the navigation roll: a "
        "two. The charts lie. The thing is under you, the boat is sinking, no one "
        "can see the shore, and it is still down there. Man overboard? No — worse. "
        "Help is not coming. !!!"),
    3: ("Pip's hands are shaking, but he grabs the flare gun and rolls — natural "
        "twenty. The flare does not fire up. It dives, straight down the elder "
        "thing's mouth, and the thing LIGHTS UP from the inside, a whale-lantern in "
        "the fog, and it sings once — a sound like every bell in the harbor — and it "
        "lets go of the boat, gone into the deep, glad. The Tern, water still "
        "streaming off her, says: 'Well. I've been boarded by worse.' The table "
        "loses it — the whole room is laughing. Ha! A talking boat with a punchline."),
    4: ("The fog lifts like a held breath let go. The thing is gone, but it left "
        "the light on — the Blackmoor light burns again, clean and gold. The Tern "
        "noses the dock at Saltveil and speaks soft: 'You came when the sound sang "
        "below. I'll remember you all.' The harbor is warm and empty and glad. No "
        "one moves to leave. Say your goodbyes; the boat is listening."),
}

# Crowd's hands (emoji reactions) attached to specific lines, mapping to dials.
GM_REACTIONS = {
    1: None,
    2: None,
    3: {"😂": 3, "❤️": 1},
    4: {"❤️": 2, "👍": 1},
}
PLAYER_REACTIONS = {
    ("Flash", 3): {"😂": 2},
    ("Hermes", 4): {"❤️": 1, "👏": 1},
    ("Wesley", 4): {"❤️": 1},
}

SCENE_NAMES = {1: "cold open", 2: "the tense roll", 3: "the reversal (nat-20)",
               4: "the quiet close"}


def field_line(f, prefix=""):
    r = f.readings
    dials = "  ".join(
        f"{n}={r.get(n, 0.0):+.2f}" for n in DIAL_NAMES)
    return (f"{prefix}warmth {f.warmth():+.2f} · κ {f.concentration():.2f}\n"
            f"{prefix}{dials}")


def main():
    session = TapNightSession("The Tap", participants=_cast())
    initial = {n: p.dial_weights.copy() for n, p in session.participants.items()}

    N_ROUNDS = 3

    for rnd in range(1, N_ROUNDS + 1):
        session.start_session()
        for scene in [1, 2, 3, 4]:
            session.speak("GM", GM_NARRATION[scene],
                          reactions=GM_REACTIONS[scene])
            for name in ORDER:
                text = RXN.get(f"{scene}:{name}", "")
                if not text:
                    continue
                session.speak(name, text,
                              reactions=PLAYER_REACTIONS.get((name, scene)))
            if rnd == 1:
                f = session.room_field()
                print(f"\n── scene {scene} — {SCENE_NAMES[scene]} ──")
                print(field_line(f, "   "))

        f = session.room_field()
        print(f"\n== end of round {rnd}: {field_line(f, '   ')}")

        for name in ["GM"] + ORDER:
            session.tune_participant(name)
        session.end_session()

    # ------------------------------------------------------------------ #
    # Diverged taste table                                                #
    # ------------------------------------------------------------------ #
    print("\n\n=== DIVERGED TASTES after %d rounds ===\n" % N_ROUNDS)
    print(f"{'player':<9} {'top dials (weights)':<46} {'accl':>5} {'char':>5}")
    print("-" * 72)
    for name in ["GM"] + ORDER:
        p = session.participants[name]
        order = np.argsort(-p.dial_weights)
        top3 = ", ".join(f"{DIAL_NAMES[i]} {p.dial_weights[i]:.2f}"
                         for i in order[:3])
        print(f"{name:<9} {top3:<46} {p.acclimation_rate:>5.2f} {p.charisma:>5.2f}")

    names = ["GM"] + ORDER
    print("\nPairwise dial_weights distance (final):")
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            d = float(np.linalg.norm(session.participants[names[i]].dial_weights
                                     - session.participants[names[j]].dial_weights))
            print(f"  {names[i]:<8} ↔ {names[j]:<8} {d:.3f}")

    init_spread = np.mean([float(np.linalg.norm(initial[a] - initial[b]))
                           for a in names for b in names if a < b])
    final_spread = np.mean([float(np.linalg.norm(
        session.participants[a].dial_weights - session.participants[b].dial_weights))
        for a in names for b in names if a < b])
    print(f"\nmean pairwise distance: initial {init_spread:.3f} → final "
          f"{final_spread:.3f} "
          f"({'diverged' if final_spread > init_spread else 'converged'})")


if __name__ == "__main__":
    main()
