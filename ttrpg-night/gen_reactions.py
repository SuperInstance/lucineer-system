"""Generate in-character player reactions for TTRPG Night via DeepInfra.

The cast (4 players, routed through DeepInfra with distinct models):
- Flash  -> deepseek-ai/DeepSeek-V4-Flash          (Kel, the bosun — quick & jokey)
- Pro    -> deepseek-ai/DeepSeek-V4-Pro            (Mara, the navigator — earnest, afraid)
- Hermes -> NousResearch/Hermes-3-Llama-3.1-405B   (Auld, the old hand — grave & tender)
- Wesley -> anthropic/claude-haiku-4-5             (Pip, the cabin boy — small, fast, wonder)

Writes reactions.json. Cached: re-run skips already-generated lines.
"""
import json
import os
import time
import urllib.request
import urllib.error

KEY = "zYuVMGC4JySULP2waqKW35jI42TjaPkl"
URL = "https://api.deepinfra.com/v1/openai/chat/completions"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reactions.json")

PERSONAS = {
    "Flash": {
        "model": "deepseek-ai/DeepSeek-V4-Flash",
        "system": (
            "You are KEL, the bosun of the cutter Tern, in a maritime TTRPG one-shot. "
            "Your voice: quick, warm, jokey, the first to crack a smile and the first to grab a rope. "
            "You improvise and you care loudly. Speak in one or two short sentences, in character, "
            "no narration, no quotes, no stage directions."
        ),
    },
    "Pro": {
        "model": "deepseek-ai/DeepSeek-V4-Pro",
        "system": (
            "You are MARA, the navigator of the cutter Tern, in a maritime TTRPG one-shot. "
            "Your voice: earnest, careful, precise, a little afraid — you mean every word. "
            "You keep the chart and you notice what is wrong first. Speak in one or two short "
            "sentences, in character, no narration, no quotes, no stage directions."
        ),
    },
    "Hermes": {
        "model": "NousResearch/Hermes-3-Llama-3.1-405B",
        "system": (
            "You are AULD, the old hand of the cutter Tern, in a maritime TTRPG one-shot. "
            "Your voice: grave, tender, slow — you know the old names the sea keeps. "
            "You speak in complete, quiet sentences and you are the one the others look to when "
            "the fog closes. Speak in one or two short sentences, in character, no narration, "
            "no quotes, no stage directions."
        ),
    },
    "Wesley": {
        "model": "anthropic/claude-haiku-4-5",
        "system": (
            "You are PIP, the cabin boy of the cutter Tern, in a maritime TTRPG one-shot. "
            "Your voice: small, fast, full of wonder — you shout with delight and you see the "
            "magic in everything. Speak in one or two short sentences, in character, no narration, "
            "no quotes, no stage directions."
        ),
    },
}

SCENES = {
    1: (
        "Cold open. The GM narrated: you have all boarded the talking boat Tern at the fogbound "
        "harbor Saltveil, hired to cross the sound to the Blackmoor light, which went dark and will "
        "not say why. The boat spoke: 'Board slow. The tide knows you now.' Introduce yourself to "
        "the boat, in character."
    ),
    2: (
        "Tense roll. The GM narrated: halfway across the sound the fog closed like a hand, something "
        "huge passed under the hull, a seam opened, water came up through the boards, the boat cried "
        "'All hands! She's taking water, now!', and Mara threw the navigation roll and it came up a "
        "two. The charts are wrong, the thing is under you, the boat is sinking, no one can see the "
        "shore. React in character — you are afraid."
    ),
    3: (
        "Reversal, natural twenty. The GM narrated: Pip grabbed the flare gun and rolled a natural "
        "twenty. The flare dived straight down the elder thing's mouth and lit it up from inside, "
        "a whale-lantern in the fog, and it sang once and let go of the boat. The boat said: 'Well. "
        "I've been boarded by worse.' The whole table is laughing. React in character — giddy, "
        "relieved, the absurd success worked."
    ),
    4: (
        "Quiet close. The GM narrated: the fog lifted, the thing was gone but it left the Blackmoor "
        "light burning again, clean and gold. The boat nosed the dock and spoke soft: 'You came when "
        "the sound sang below. I'll remember you all.' The harbor is warm and empty and glad. Say a "
        "quiet, sincere goodbye to the boat and to each other, in character."
    ),
}


def call(model, system, user, temperature=0.9, max_tokens=90, retries=4):
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode()
    last_err = "[ERR]"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                URL, data=body,
                headers={
                    "Authorization": f"Bearer {KEY}",
                    "Content-Type": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=90) as r:
                data = json.load(r)
            return data["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            last_err = f"[ERR HTTP {e.code}]"
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(5 * (attempt + 1))
                continue
            return last_err
        except Exception as e:  # noqa: BLE001
            last_err = f"[ERR {type(e).__name__}]"
            time.sleep(3 * (attempt + 1))
    return last_err


def main():
    cache = {}
    if os.path.exists(OUT):
        with open(OUT) as fh:
            cache = json.load(fh)

    changed = False
    for scene in sorted(SCENES):
        for name, persona in PERSONAS.items():
            key = f"{scene}:{name}"
            if key in cache and not cache[key].startswith("[ERR"):
                continue
            print(f"gen {key} -> {persona['model']}", flush=True)
            cache[key] = call(
                persona["model"], persona["system"], SCENES[scene],
            )
            changed = True
            time.sleep(0.3)

    with open(OUT, "w") as fh:
        json.dump(cache, fh, indent=2)
    print(f"wrote {OUT} ({len(cache)} entries, changed={changed})")


if __name__ == "__main__":
    main()
