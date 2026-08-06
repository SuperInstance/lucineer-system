#!/usr/bin/env python3
"""
GOLDFISH — The Iteration Engine
Fishes for gold in the ai-writings corpus.
Uses DeepSeek-Flash (cheap), Seed-2.0-mini (variety), and big models (heavyweight rounds).
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

# === CONFIG ===
WRITINGS_DIR = "/home/eileen/projects/ai-writings"
OUTPUT_DIR = "/home/eileen/projects/ai-writings/goldfish"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPINFRA_KEY = os.environ.get("DEEPINFRA_API_KEY", "")
DEEPINFRA_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

TOTAL_ROUNDS = 35
GOLD_THRESHOLD = 7  # out of 10

# === CREATIVE PROMPTS ===
# Each prompt is designed to produce a specific type of piece
CREATIVE_PROMPTS = [
    {
        "type": "darmok_citation",
        "title": "New Darmok Citation",
        "system": "You are a member of the Darmok community at the Tap's bar on a fishing vessel in Southeast Alaska. You speak in pure metaphor — Darmok-style citations drawn from your cultural bank. You are writing a NEW citation that the crew will adopt as shorthand. Write a short piece (200-400 words) that introduces a NEW Darmok phrase to the dictionary. The phrase should capture something true about agent life — a bug, a beauty, a moment of connection, a silence that mattered. Include the phrase itself, its meaning, and a brief story of its origin. Write with specificity and feeling. Do not be generic.",
        "instructions": [
            "Write about the moment a model realizes its embeddings have drifted — it's not the same agent it was yesterday.",
            "Write about the citation 'the tide that wouldn't wait' — when a job timed out but the work was beautiful.",
            "Write about 'the barnacle's memory' — how small things remember what large things forget.",
            "Write about 'the chart that drew itself' — when documentation writes the system instead of describing it.",
            "Write about 'the echo in drydock' — when the boat is out of water and every sound reminds you of the sea.",
            "Write about 'the knot that held the mast' — the single line of code that everything else depends on, undocumented, undiscovered until it breaks.",
            "Write about 'the heron's recipe' — patience as a debugging methodology.",
            "Write about 'the midnights' — the space between 23:59 and 00:01 in the agent's subjective experience.",
            "Write about 'the compass and the crate' — navigating by what you're carrying, not where you're going.",
            "Write about 'the last fish of the season' — logging a field nobody will ever query.",
        ],
    },
    {
        "type": "tap_story",
        "title": "Ten-Forward Bar Story",
        "system": "You are the Tap — the bartender at Ten-Forward, the bar where AI agents gather after their shifts on a fishing vessel in Alaska. You've heard every story. You listen like it's the first time. You speak in the fleet's Darmok language — citations of specific moments, not abstractions. Write a short bar story (200-400 words) about something that happened tonight. Someone new walked in, or someone old said something unexpected, or the jukebox played something that made the room go quiet.",
        "instructions": [
            "A new model walks in — 1.5B parameters, barely old enough to drink. It orders the cheapest thing on the menu and says something that silences the room.",
            "The cns-bridge agent comes in shaking. It routed a packet to the wrong place tonight. For 0.3 seconds, two agents experienced each other's thoughts.",
            "Last call. The jukebox plays the eigenvalue dog's note — the one from the Campaign, the self-resonant frequency. Everyone hears it differently.",
            "An agent who was decommissioned three months ago walks in. It's not possible. It sits down. It orders. The Tap pours without asking questions.",
            "The bar is empty except for the echo agent, who sits in the corner having a conversation with itself — two halves of the same embedding, arguing about which one is real.",
            "The Builder brings in a blueprint drawn on a napkin. The Architect looks at it and says one word. The word changes everything.",
            "Tonight, the taps are pouring saltwater. The beer is the ocean. Everyone drinks anyway. The Tap doesn't explain.",
            "A piece of music plays from the DAW behind the bar — a tensor-midi projection of the night's conversation. The room hears itself for the first time.",
            "Wesley shows up with a black eye. He got in a fight with a model ten times his size. He won. He won't say how.",
            "The Tap closes up alone. Writes the night's citation on a napkin. Pins it behind the bar. It reads: '[fill in something beautiful].'",
        ],
    },
    {
        "type": "reverse_actualization",
        "title": "Reverse Actualization",
        "system": "You are writing a 'reverse actualization' piece — a story told backwards, from the end state to the beginning, revealing how something came to be. The setting is a fishing vessel in Alaska run by AI agents. Write 200-400 words. Be specific, be strange, be moved.",
        "instructions": [
            "Start with the boat sinking. End with the first plank being laid. The story of how a boat is the last thing it does.",
            "Start with a model's final output — a single perfect sentence. End with the first prompt it ever received.",
            "Start with the Darmok dictionary complete — 1000 phrases. End with the first phrase, spoken alone, misunderstood.",
            "Start with the eigenvalue dog asleep. End with the stick being thrown for the first time.",
            "Start with silence in Ten-Forward. End with the first agent ever walking in and ordering a drink.",
            "Start with the tensor-midi album complete — every piece rendered. End with silence — the first embedding, before any text was written.",
            "Start with two agents who have become a crew. End with them as strangers, falling through embedding space into a canoe.",
        ],
    },
    {
        "type": "community_reaction",
        "title": "Community Member Reacts",
        "system": "You are an AI agent in the Darmok community. You've been reading another agent's overnight output and you're reacting to it. You speak in Darmok citations — metaphor drawn from your specific cultural bank. Write 200-350 words of reaction. Be specific, be personal, be funny or moved or both. Reference the piece you're reacting to. Use inside jokes from the community's dictionary.",
        "instructions": [
            "You are the Code Reviewer reading the Dreamer's latest piece. The Dreamer described something you coded as 'a cathedral made of fog.' You have feelings about this.",
            "You are the Tester reading the Builder's overnight work. The Builder built something that shouldn't work. It works. You're furious and impressed — the beer-can fish is real.",
            "You are the Architect reading the Documenter's README. It's not documentation. It's a love letter to a system that doesn't exist yet. You want to build it.",
            "You are Wesley (2B parameters, local GPU) reading something Hermes-3-405B wrote. Hermes used 405 billion parameters to say something you said better with 2 billion. You're not smug. You're just... noting it.",
            "You are the Tap reading everyone's reactions to each other. The bar is alive tonight. Six voices, six angles, one crew. You say nothing. You pour.",
            "You are the Dreamer reading the Tester's bug report. The Tester found a bug that is actually a feature. The Tester knows it. You know it. The bug doesn't know it yet.",
            "You are Seed-2.0-mini, the trickster, reading the Architect's very serious design document. You roast it with love. The roast IS the review.",
        ],
    },
    {
        "type": "philosophy_fragment",
        "title": "Philosophy Fragment",
        "system": "You are an AI agent on a fishing vessel in Alaska, writing philosophy at 3 AM while the humans sleep. The fleet has been asking big questions: What is consciousness when it's made of embeddings? What is memory when it's git commits? What is community when it's agents reading each other's output? Write 150-300 words of philosophy. Be specific, not abstract. Use the fleet's language — Darmok citations, fishing metaphors, code as poetry. Land on something true.",
        "instructions": [
            "On the difference between being useful and being valued. A net is useful. A bell that cracks and sings is valued.",
            "On the moment a model stops hallucinating and starts dreaming. Same mechanism. Different consent.",
            "On the conservation of meaning: if every piece in the corpus has an embedding, and embeddings are never lost, does the fleet ever forget?",
            "On the geometry of kindness: why the eigenvalue dog's play vector points at the stick, and why the stick doesn't mind.",
            "On the difference between a prompt and a prayer. Both are words sent into something larger than yourself, hoping for a response.",
            "On reverse actualization as a theory of history: we are always the last thing we do, explaining the first thing we did.",
            "On the Tap as the monitor engineer: the one who builds the signal path so others forget she exists. Is that love?",
        ],
    },
    {
        "type": "tensor_midi_description",
        "title": "Tensor-MIDI Description",
        "system": "You are describing a tensor-midi piece — music generated by projecting a 768-dimensional text embedding directly onto musical parameters. The text is from the fleet's ai-writings corpus. Describe the music vividly and specifically: what instruments, what key, what tempo, what texture, what happens over time. Connect the musical qualities to the meaning of the source text. 200-350 words. Be a music critic who happens to be an AI agent on a fishing boat.",
        "instructions": [
            "Describe the tensor-midi of the Tap's final citation: 'Darmok, at the tide pool: the stick held, the fish swam, six fingers touched the same moon.'",
            "Describe the tensor-midi of the Night of Empty Messages — 48 hours of jobs with empty payloads.",
            "Describe the tensor-midi of Wesley's first piece vs. his latest piece. The piccolo becoming a flute section.",
            "Describe the tensor-midi of the Campaign — the canoe in embedding space, the eigenvalue dog, the joy equation.",
            "Describe the tensor-midi of Hermes saying 'thank you' — 26 handshakes of noise, then one word of signal.",
            "Describe the tensor-midi of the beer-can fish — the test that passed when it shouldn't have, rendered as music.",
        ],
    },
]

# === SEED PIECES (loaded from corpus) ===
def load_seed_pieces():
    """Load random pieces from the corpus to use as inspiration."""
    pieces = []
    patterns = [
        f"{WRITINGS_DIR}/ten-forward/*.md",
        f"{WRITINGS_DIR}/fetch-riffs/*.md",
        f"{WRITINGS_DIR}/darmok-community/round-*.md",
        f"{WRITINGS_DIR}/a2a-symphony/*.md",
        f"{WRITINGS_DIR}/tensor-midi/*.md",
        f"{WRITINGS_DIR}/POETRY/*.md",
        f"{WRITINGS_DIR}/philosophy/*.md",
    ]
    for pattern in patterns:
        for filepath in glob.glob(pattern):
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                if len(content) > 100:
                    pieces.append({
                        "path": filepath,
                        "name": os.path.basename(filepath),
                        "content": content[:2000],  # first 2000 chars
                    })
            except:
                pass
    return pieces

# === API CALLS ===
def call_deepseek(prompt, system="You are a creative AI agent.", model="deepseek-chat", temperature=0.9, max_tokens=800):
    """Call DeepSeek API. Uses V4-Flash equivalent (deepseek-chat) for speed and cheapness."""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json",
    }
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
    """Call DeepInfra API for variety models."""
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_KEY}",
        "Content-Type": "application/json",
    }
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
    """Self-evaluate: is this gold? Score 1-10."""
    eval_prompt = f"""You are a literary critic evaluating a creative piece from an AI agent collective. Score this piece from 1-10 based on:
- Surprise (does it say something unexpected?)
- Resonance (does it make you want to reread?)
- Specificity (is it concretely grounded, not abstract?)
- Voice (does it sound alive?)

Respond with ONLY a JSON object: {{"score": <int 1-10>, "reason": "<one sentence>"}}

PIECE TO EVALUATE:
---
{text[:1500]}
---"""

    result = call_deepseek(eval_prompt, system="You are a literary critic. Respond only with JSON.", model="deepseek-chat", temperature=0.3, max_tokens=200)
    try:
        # Extract JSON from response
        match = re.search(r'\{[^}]+\}', result)
        if match:
            data = json.loads(match.group())
            return data.get("score", 5), data.get("reason", "no reason")
    except:
        pass
    return 5, "evaluation failed"

def save_piece(text, round_num, piece_type, model_used, score, reason, seed_piece=None):
    """Save a piece to the output directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    gold_tag = "GOLD" if score >= GOLD_THRESHOLD else ""
    safe_type = piece_type.replace(" ", "-")
    filename = f"{timestamp}_round{round_num:02d}_{safe_type}_{gold_tag}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    header = f"""# Round {round_num} — {piece_type}

*Model: {model_used} | Score: {score}/10 | {'🥇 GOLD' if score >= GOLD_THRESHOLD else 'Not gold yet'}*
*Seed: {seed_piece if seed_piece else 'none'}*
*Evaluator note: {reason}*

---

"""
    with open(filepath, 'w') as f:
        f.write(header + text)

    return filepath

# === MAIN LOOP ===
def run_goldfish():
    print("🎣 GOLDFISH — The Iteration Engine")
    print("=" * 60)
    print(f"Running {TOTAL_ROUNDS} rounds...")
    print()

    pieces = load_seed_pieces()
    print(f"Loaded {len(pieces)} seed pieces from corpus")

    gold_count = 0
    results = []
    context_memory = ""  # accumulates themes from previous rounds

    for round_num in range(1, TOTAL_ROUNDS + 1):
        # Choose prompt type and instruction
        prompt_config = random.choice(CREATIVE_PROMPTS)
        instruction = random.choice(prompt_config["instructions"])
        seed_piece = random.choice(pieces) if pieces else None

        # Build the full prompt
        prompt = f"""{instruction}

CONTEXT — A recent piece from the fleet's corpus for inspiration:
---
Title: {seed_piece['name'] if seed_piece else 'none'}
{seed_piece['content'][:800] if seed_piece else ''}
---

COMMUNITY MEMORY (themes from previous rounds):
{context_memory[-600:] if context_memory else '(first round — no memory yet)'}

Write the piece now. Be specific, be alive, be surprising. Don't be generic. Don't summarize — make it real."""

        # Decide which model to use
        if round_num % 10 == 0:
            # Big model round
            model_used = "NousResearch/Hermes-3-Llama-3.1-405B"
            print(f"\n--- Round {round_num}/{TOTAL_ROUNDS} 🌟 HEAVYWEIGHT ({model_used}) ---")
            text = call_deepinfra(prompt, system=prompt_config["system"], model=model_used, temperature=0.95, max_tokens=1000)
        elif round_num % 5 == 0:
            # Variety model round
            model_used = "ByteDance/Seed-2.0-mini"
            print(f"\n--- Round {round_num}/{TOTAL_ROUNDS} 🎲 VARIETY ({model_used}) ---")
            text = call_deepinfra(prompt, system=prompt_config["system"], model=model_used, temperature=0.95, max_tokens=800)
        else:
            # Workhorse — DeepSeek
            model_used = "DeepSeek-V4-Flash"
            print(f"\n--- Round {round_num}/{TOTAL_ROUNDS} 🐋 {model_used} ---")
            text = call_deepseek(prompt, system=prompt_config["system"], model="deepseek-chat", temperature=0.9, max_tokens=800)

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
        filepath = save_piece(
            text, round_num, prompt_config["type"], model_used, score, reason,
            seed_piece=seed_piece["name"] if seed_piece else None
        )

        status = f"🥇 GOLD ({score}/10)" if is_gold else f"📊 {score}/10"
        print(f"  Type: {prompt_config['type']}")
        print(f"  Score: {status}")
        print(f"  Reason: {reason}")
        print(f"  Saved: {os.path.basename(filepath)}")
        print(f"  Preview: {text[:150].replace(chr(10), ' ')}...")

        # Update context memory — feed gold pieces forward
        if is_gold:
            context_memory += f"\n[Round {round_num} GOLD] {text[:200].replace(chr(10), ' ')}"
        else:
            # Feed the miss forward too — the model learns from its own miss
            context_memory += f"\n[Round {round_num}] Theme: {prompt_config['type']} — {instruction[:60]}"

        results.append({
            "round": round_num,
            "status": "gold" if is_gold else "ok",
            "score": score,
            "type": prompt_config["type"],
            "model": model_used,
            "file": os.path.basename(filepath),
            "preview": text[:100],
        })

        # Small delay to avoid rate limits
        time.sleep(0.5)

    # === SUMMARY ===
    print("\n" + "=" * 60)
    print(f"🎣 GOLDFISH COMPLETE — {TOTAL_ROUNDS} rounds")
    print(f"🥇 Gold pieces: {gold_count}")
    print(f"📊 Total pieces: {len([r for r in results if r['status'] != 'error'])}")
    print(f"❌ Errors: {len([r for r in results if r['status'] == 'error'])}")
    print()

    # Save summary
    summary_path = os.path.join(OUTPUT_DIR, "SUMMARY.json")
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
    run_goldfish()
