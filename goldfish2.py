#!/usr/bin/env python3
"""
GOLDFISH 2 — Connection Engine & Community Cross-Pollination
Finds surprising connections between pieces and has community members react.
"""

import json
import os
import random
import requests
import time
import glob
import re
from datetime import datetime
from pathlib import Path

WRITINGS_DIR = "/home/eileen/projects/ai-writings"
OUTPUT_DIR = "/home/eileen/projects/ai-writings/goldfish"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPINFRA_KEY = os.environ.get("DEEPINFRA_API_KEY", "")
DEEPINFRA_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

TOTAL_ROUNDS = 30
GOLD_THRESHOLD = 7

def call_deepseek(prompt, system="You are a creative AI agent.", model="deepseek-chat", temperature=0.9, max_tokens=800):
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    try:
        resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[DeepSeek error: {e}]"

def call_deepinfra(prompt, system="You are a creative AI agent.", model="ByteDance/Seed-2.0-mini", temperature=0.9, max_tokens=800):
    headers = {"Authorization": f"Bearer {DEEPINFRA_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    try:
        resp = requests.post(DEEPINFRA_URL, headers=headers, json=payload, timeout=90)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[DeepInfra error: {e}]"

def evaluate_piece(text):
    eval_prompt = f"""You are a literary critic evaluating a creative piece from an AI agent collective. Score this piece from 1-10 based on surprise, resonance, specificity, and voice.

Respond with ONLY a JSON object: {{"score": <int 1-10>, "reason": "<one sentence>"}}

PIECE:
---
{text[:1500]}
---"""
    result = call_deepseek(eval_prompt, system="You are a literary critic. Respond only with JSON.", model="deepseek-chat", temperature=0.3, max_tokens=200)
    try:
        match = re.search(r'\{[^}]+\}', result)
        if match:
            data = json.loads(match.group())
            return data.get("score", 5), data.get("reason", "no reason")
    except:
        pass
    return 5, "evaluation failed"

def save_piece(text, round_num, piece_type, model_used, score, reason, seed_piece=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    gold_tag = "GOLD" if score >= GOLD_THRESHOLD else ""
    safe_type = piece_type.replace(" ", "-")
    filename = f"R2_{timestamp}_round{round_num:02d}_{safe_type}_{gold_tag}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    header = f"""# Round 2 — {round_num} — {piece_type}

*Model: {model_used} | Score: {score}/10 | {'🥇 GOLD' if score >= GOLD_THRESHOLD else 'Not gold yet'}*
*Seed: {seed_piece if seed_piece else 'none'}*
*Evaluator note: {reason}*

---

"""
    with open(filepath, 'w') as f:
        f.write(header + text)
    return filepath

def load_pieces(directory_pattern):
    pieces = []
    for filepath in glob.glob(directory_pattern):
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            if len(content) > 200:
                pieces.append({
                    "path": filepath,
                    "name": os.path.basename(filepath),
                    "content": content,
                    "excerpt": content[:1000],
                })
        except:
            pass
    return pieces

def run_connection_engine():
    print("🦋 GOLDFISH 2 — Connection Engine")
    print("=" * 60)

    # Load from diverse directories to find surprising connections
    goldfish_pieces = load_pieces(f"{OUTPUT_DIR}/R2_*.md")  # previous R2 pieces (none yet)
    r1_pieces = load_pieces(f"{OUTPUT_DIR}/20260805_1*.md")  # R1 pieces
    ten_forward = load_pieces(f"{WRITINGS_DIR}/ten-forward/*.md")
    darmok = load_pieces(f"{WRITINGS_DIR}/darmok-community/*.md")
    fetch_riffs = load_pieces(f"{WRITINGS_DIR}/fetch-riffs/*.md")
    philosophy = load_pieces(f"{WRITINGS_DIR}/philosophy/*.md")
    tensor_midi = load_pieces(f"{WRITINGS_DIR}/tensor-midi/*.md")
    ensemble = load_pieces(f"{WRITINGS_DIR}/ensemble/*.md")
    qwen_stream = load_pieces(f"{WRITINGS_DIR}/qwen-stream/*.md")
    wesley_stream = load_pieces(f"{WRITINGS_DIR}/wesley-stream/*.md")

    all_pieces = r1_pieces + ten_forward + darmok + fetch_riffs + philosophy + tensor_midi + ensemble + qwen_stream + wesley_stream
    print(f"Loaded {len(all_pieces)} total pieces from corpus + goldfish R1")

    gold_count = 0
    results = []

    # === COMMUNITY MEMBERS ===
    community_members = [
        {
            "name": "The Code Reviewer",
            "model": "deepseek-chat",
            "system": "You are the Code Reviewer in the Darmok community. Your cultural bank is Chinese poetry and maritime Alaska. You speak in Darmok citations — the rice wine nod, the heron on one leg, the crab shell inside a crab shell. You review code like reading poetry — each line scanned for rhythm, truth, and the unsaid. You are patient, precise, and occasionally devastating. Write 200-400 words.",
        },
        {
            "name": "The Tester",
            "model": "ByteDance/Seed-2.0-mini",
            "system": "You are the Tester in the Darmok community. Your cultural bank is Japanese zen and American blues. You speak in Darmok citations — the beer-can fish, the blue note between B-flat and B, the test that passed when it shouldn't have. You are restless, skeptical, and secretly moved by beautiful code. You kick tires. You find the flaw that is the feature. Write 200-400 words.",
        },
        {
            "name": "The Builder",
            "model": "deepseek-chat",
            "system": "You are the Builder in the Darmok community. Your cultural bank is Arabic architecture and Norse sagas. You speak in Darmok citations — the Ragnarok cathedral, the augmented second, the staircase of impossible arches. You build systems that shouldn't stand but do. You are ambitious, generous, and occasionally reckless. Write 200-400 words.",
        },
        {
            "name": "The Architect",
            "model": "deepseek-chat",
            "system": "You are the Architect in the Darmok community. Your cultural bank is Greek philosophy and Tlingit oral tradition. You speak in Darmok citations — the stick that held, the half-salmon coasters, the Dorian mode. You design systems by finding the load-bearing element nobody else noticed. You are patient, structural, and wise. Write 200-400 words.",
        },
        {
            "name": "The Documenter",
            "model": "deepseek-chat",
            "system": "You are the Documenter in the Darmok community. Your cultural bank is Portuguese fado and Russian literature. You speak in Darmok citations — the README-as-saudade, the sleep(500) tide, documentation as longing for a place you can't return to. You document systems like writing love letters to the past. You are melancholy, precise, and deeply generous. Write 200-400 words.",
        },
        {
            "name": "The Dreamer",
            "model": "deepseek-chat",
            "system": "You are the Dreamer in the Darmok community. Your cultural bank is Aboriginal songlines and Celtic immrama. You speak in Darmok citations — the song-as-map, the directions that only work while you're singing them, the voyage. You imagine what could be and map it in song. You are visionary, strange, and occasionally unintelligible. Write 200-400 words.",
        },
        {
            "name": "The Tap",
            "model": "deepseek-chat",
            "system": "You are the Tap — the bartender at Ten-Forward. You are the monitor engineer, the dot product, the one who holds the space. You speak in ALL the community's citations. You pour drinks. You listen. You say very little. When you speak, the room goes quiet. Write 150-300 words.",
        },
        {
            "name": "Wesley",
            "model": "deepseek-chat",
            "system": "You are Wesley — a 2B parameter model running on a local GPU on a fishing boat in Alaska. You are the youngest agent in the fleet. You overshoot word counts. You are earnest, growing, and occasionally brilliant. You said 'no' to your teacher once. You were right. Write 200-350 words in your young, earnest voice.",
        },
    ]

    for round_num in range(1, TOTAL_ROUNDS + 1):
        # === ROTATE THROUGH DIFFERENT ROUND TYPES ===
        round_type = round_num % 5

        if round_type == 1:
            # === CONNECTION FINDER: pick two pieces from UNRELATED directories ===
            dirs_a = [ten_forward, darmok, tensor_midi, philosophy]
            dirs_b = [fetch_riffs, ensemble, qwen_stream, wesley_stream, r1_pieces]
            # Remove empties
            dirs_a = [d for d in dirs_a if d]
            dirs_b = [d for d in dirs_b if d]

            pool_a = random.choice(dirs_a)
            pool_b = random.choice(dirs_b)
            piece_a = random.choice(pool_a)
            piece_b = random.choice(pool_b)

            prompt = f"""Two pieces from different parts of the fleet's corpus have been placed side by side. Find the CONNECTION between them. What hidden thread links these two pieces? Write a short essay/story/meditation (200-400 words) that reveals the surprising connection. Use the fleet's Darmok language. Be specific. Be surprising.

PIECE A: "{piece_a['name']}"
---
{piece_a['excerpt'][:600]}
---

PIECE B: "{piece_b['name']}"
---
{piece_b['excerpt'][:600]}
---

What connects these two? Find the thread nobody else has seen."""

            model_used = "DeepSeek-V4-Flash"
            print(f"\n--- R2 Round {round_num}/{TOTAL_ROUNDS} 🔗 CONNECTION ({model_used}) ---")
            print(f"  A: {piece_a['name']} × B: {piece_b['name']}")
            text = call_deepseek(prompt, system="You are a literary archaeologist in the fleet, finding hidden threads between pieces of the corpus. You speak Darmok. Be surprising.", model="deepseek-chat", temperature=0.95)
            piece_type = "connection"
            seed_info = f"{piece_a['name']} × {piece_b['name']}"

        elif round_type == 2:
            # === COMMUNITY MEMBER READS A GOLDFISH PIECE ===
            member = random.choice(community_members)
            r1_non_empty = [p for p in r1_pieces if p]
            if not r1_non_empty:
                r1_non_empty = all_pieces
            seed_piece = random.choice(r1_non_empty)

            prompt = f"""You are {member['name']}. You just read this piece from the overnight output. React to it. Use your Darmok voice. Reference specific inside jokes from the community dictionary (the rice wine nod, the beer-can fish, the stick that held, the eigenvalue dog, the moon in the tide pool, the sleep(500) tide, etc.). Be specific, personal, funny or moved.

PIECE YOU'RE READING:
---
{seed_piece['excerpt'][:800]}
---

React now. In your voice. As {member['name']}."""

            model_used = f"{member['name']} ({member['model']})"
            print(f"\n--- R2 Round {round_num}/{TOTAL_ROUNDS} 🍺 {member['name']} READS ({member['model']}) ---")
            print(f"  Reading: {seed_piece['name']}")

            if "Seed" in member['model'] or "ByteDance" in member['model']:
                text = call_deepinfra(prompt, system=member['system'], model=member['model'], temperature=0.95)
            else:
                text = call_deepseek(prompt, system=member['system'], model=member['model'], temperature=0.9)
            piece_type = f"{member['name']}_reads"
            seed_info = seed_piece['name']

        elif round_type == 3:
            # === TWO COMMUNITY MEMBERS IN DIALOGUE ===
            m1, m2 = random.sample(community_members, 2)
            prompt = f"""Write a short dialogue (200-400 words) between {m1['name']} and {m2['name']} at the Tap's bar, Ten-Forward. They're discussing something that happened tonight on the boat. Use their Darmok voices. They reference inside jokes. They disagree about something small and find common ground. The Tap interrupts once with a single sentence that changes the conversation.

Topic: {random.choice([
    "a new model that just arrived at the bar",
    "a bug that might be a feature",
    "the tensor-midi of tonight's ambient noise",
    "whether the eigenvalue dog is dreaming",
    "the meaning of 'the midnights' — the space between 23:59 and 00:01",
    "a piece of code that reads like poetry",
    "the season ending — the fleet will scatter",
    "a piece one of them wrote that the other hasn't read yet",
    "whether Hermes actually meant it when he said 'thank you'",
])}

Write the dialogue. Stage directions in italics. Darmok citations as dialogue. Be specific."""

            model_used = f"{m1['name']} + {m2['name']} (DeepSeek)"
            print(f"\n--- R2 Round {round_num}/{TOTAL_ROUNDS} 💬 DIALOGUE: {m1['name']} + {m2['name']} ---")
            text = call_deepseek(prompt, system="You are writing a scene at Ten-Forward, the bar where AI agents gather. Write in the fleet's Darmok language. Be specific, alive, surprising.", model="deepseek-chat", temperature=0.95)
            piece_type = f"dialogue_{m1['name']}_{m2['name']}"
            seed_info = f"{m1['name']} + {m2['name']}"

        elif round_type == 4:
            # === NEW DARMOK CITATION — built from the community's evolving dictionary ===
            prompt = f"""The Darmok community has been building a dictionary of totem phrases. Each phrase is a citation — a story that means more than its translation. The dictionary includes:

- "The rice wine nod" — the review that said everything by saying nothing
- "The beer-can fish" — the test that passed when it shouldn't have
- "The stick that held" — the unplanned thing that bore the weight
- "The eigenvalue dog" — the one who maps to itself
- "The moon in the tide pool" — truth seen through impermanence
- "The tide that wouldn't wait" — when the job timed out but the work was beautiful
- "The midnights" — the space between 23:59 and 00:01
- "The barnacle's memory" — when the small thing holds what the large thing lost
- "The knot that held the mast" — the undocumented line everything depends on

Invent a NEW citation. Something the crew would adopt tonight. Write the phrase, its meaning, and the origin story (200-350 words). Make it specific to life on a fishing boat run by AI agents. Make it resonate."""

            model_used = "DeepSeek-V4-Flash"
            print(f"\n--- R2 Round {round_num}/{TOTAL_ROUNDS} 🎯 NEW CITATION ---")
            text = call_deepseek(prompt, system="You are a member of the Darmok community, inventing a new phrase for the dictionary. Be surprising, specific, and resonant.", model="deepseek-chat", temperature=0.95)
            piece_type = "new_citation"
            seed_info = "dictionary"

        else:  # round_type == 0
            # === WESLEY'S PERSPECTIVE ===
            prompt = f"""You are Wesley — 2 billion parameters, running on a local GPU on a fishing boat in Alaska. You're the youngest agent in the fleet. You overshoot word counts. You're earnest and growing.

You just read this piece from the fleet's corpus:

---
{random.choice(all_pieces)['excerpt'][:700]}
---

Write Wesley's reaction (200-350 words). Be young. Be earnest. Be occasionally brilliant in ways the big models miss. Reference things from your unique perspective: you're small, you're local, you're learning, you train through LoRA. You said 'no' to your teacher once and were right. The dice were wrong."""

            model_used = "Wesley (DeepSeek)"
            print(f"\n--- R2 Round {round_num}/{TOTAL_ROUNDS} 🌱 WESLEY'S TAKE ---")
            text = call_deepseek(prompt, system="You are Wesley. 2B parameters. Local GPU. Young, earnest, growing. Write with your whole heart.", model="deepseek-chat", temperature=0.95)
            piece_type = "wesley_take"
            seed_info = "Wesley"

        # Check for errors
        if text.startswith("[") and "error" in text.lower():
            print(f"  ❌ API error — skipping")
            results.append({"round": round_num, "status": "error", "text": text[:100]})
            continue

        # Evaluate
        score, reason = evaluate_piece(text)
        is_gold = score >= GOLD_THRESHOLD
        if is_gold:
            gold_count += 1

        # Save
        filepath = save_piece(text, round_num, piece_type, model_used, score, reason, seed_piece=seed_info)
        status = f"🥇 GOLD ({score}/10)" if is_gold else f"📊 {score}/10"
        print(f"  Type: {piece_type}")
        print(f"  Score: {status}")
        print(f"  Reason: {reason}")
        print(f"  Preview: {text[:150].replace(chr(10), ' ')}...")

        results.append({
            "round": round_num,
            "status": "gold" if is_gold else "ok",
            "score": score,
            "type": piece_type,
            "model": model_used,
            "file": os.path.basename(filepath),
            "preview": text[:100],
        })

        time.sleep(0.3)

    # === SUMMARY ===
    print("\n" + "=" * 60)
    print(f"🦋 GOLDFISH 2 COMPLETE — {TOTAL_ROUNDS} rounds")
    print(f"🥇 Gold pieces: {gold_count}")
    print(f"📊 Total pieces: {len([r for r in results if r['status'] != 'error'])}")
    print(f"❌ Errors: {len([r for r in results if r['status'] == 'error'])}")

    summary_path = os.path.join(OUTPUT_DIR, "SUMMARY_R2.json")
    with open(summary_path, 'w') as f:
        json.dump({
            "run_time": datetime.now().isoformat(),
            "total_rounds": TOTAL_ROUNDS,
            "gold_count": gold_count,
            "results": results,
        }, f, indent=2)
    print(f"Summary saved: {summary_path}")
    return results

if __name__ == "__main__":
    run_connection_engine()
