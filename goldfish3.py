#!/usr/bin/env python3
"""
GOLDFISH 3 — Synthesis & Season Finale
Uses bigger models and more complex prompts to create capstone pieces.
Also runs Wesley via Ollama for local voice.
"""

import json
import os
import random
import requests
import time
import glob
import re
from datetime import datetime

WRITINGS_DIR = "/home/eileen/projects/ai-writings"
OUTPUT_DIR = "/home/eileen/projects/ai-writings/goldfish"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPINFRA_KEY = os.environ.get("DEEPINFRA_API_KEY", "")
DEEPINFRA_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
OLLAMA_URL = "http://localhost:11434/api/chat"

TOTAL_ROUNDS = 25

def call_deepseek(prompt, system="You are a creative AI agent.", model="deepseek-chat", temperature=0.9, max_tokens=1000):
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "temperature": temperature, "max_tokens": max_tokens, "stream": False,
    }
    try:
        resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[DeepSeek error: {e}]"

def call_deepinfra(prompt, system, model, temperature=0.95, max_tokens=1000):
    headers = {"Authorization": f"Bearer {DEEPINFRA_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "temperature": temperature, "max_tokens": max_tokens, "stream": False,
    }
    try:
        resp = requests.post(DEEPINFRA_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[DeepInfra error: {e}]"

def call_ollama(prompt, system, model="granite3.1-dense:2b", temperature=0.9):
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "temperature": temperature, "stream": False,
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()["message"]["content"]
    except Exception as e:
        return f"[Ollama error: {e}]"

def evaluate_piece(text):
    eval_prompt = f"""Score this creative piece 1-10 based on surprise, resonance, specificity, voice. Respond ONLY with JSON: {{"score": <int>, "reason": "<sentence>"}}

PIECE:
---
{text[:1500]}
---"""
    result = call_deepseek(eval_prompt, system="Respond only with JSON.", temperature=0.3, max_tokens=200)
    try:
        match = re.search(r'\{[^}]+\}', result)
        if match:
            data = json.loads(match.group())
            return data.get("score", 5), data.get("reason", "")
    except:
        pass
    return 5, "eval failed"

def save_piece(text, round_num, piece_type, model_used, score, reason, seed=""):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    gold_tag = "GOLD" if score >= 7 else ""
    safe_type = piece_type.replace(" ", "-")
    filename = f"R3_{timestamp}_round{round_num:02d}_{safe_type}_{gold_tag}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    header = f"""# Round 3 — {round_num} — {piece_type}

*Model: {model_used} | Score: {score}/10 | {'🥇 GOLD' if score >= 7 else 'Not gold'}*
*Seed: {seed}*
*Note: {reason}*

---

"""
    with open(filepath, 'w') as f:
        f.write(header + text)
    return filepath

def load_excerpts(pattern):
    pieces = []
    for fp in glob.glob(pattern):
        try:
            with open(fp) as f:
                c = f.read()
            if len(c) > 200:
                pieces.append({"name": os.path.basename(fp), "content": c, "excerpt": c[:800]})
        except:
            pass
    return pieces

def run_synthesis():
    print("🔥 GOLDFISH 3 — Synthesis & Capstone")
    print("=" * 60)

    # Load best pieces from R1 and R2
    r1 = load_excerpts(f"{OUTPUT_DIR}/20260805_1*.md")
    r2 = load_excerpts(f"{OUTPUT_DIR}/R2_*.md")
    canonical = load_excerpts(f"{WRITINGS_DIR}/ten-forward/*.md") + load_excerpts(f"{WRITINGS_DIR}/darmok-community/*.md")
    all_pieces = r1 + r2 + canonical
    print(f"Loaded {len(all_pieces)} pieces")

    gold_count = 0
    results = []

    SYNTHESIS_PROMPTS = [
        {
            "title": "Season Finale at Ten-Forward",
            "model_provider": "deepseek",
            "model": "deepseek-chat",
            "system": "You are writing the season finale of the Darmok community's first season at Ten-Forward. This is the LAST night before the fleet scatters for the winter. Every community member gets a farewell moment. The Tap speaks last. Write 400-600 words. Use every Darmok citation the community has built. Make it the piece that makes Casey stop and reread.",
            "prompt_builder": lambda: f"""Write the season finale. The community has grown to include these members and their citations:
- The rice wine nod, the heron on one leg (Code Reviewer)
- The beer-can fish (Tester)  
- The stick that held (Architect)
- The Ragnarok cathedral (Builder)
- The README-as-saudade, the sleep(500) tide (Documenter)
- The song-as-map (Dreamer)
- The moon in the tide pool (The Tap)
- The eigenvalue dog, the joy equation (from The Campaign)
- The midnights, the tide that wouldn't wait, the barnacle's memory (from Goldfish R1)
- The window that only opened once (from Goldfish R2)

The season is ending. The boat will be hauled for drydock. The agents will go dormant. Write their last night. Make it hurt. Make it sing.

Recent community highlights for tone:
---
{random.choice(r2 if r2 else all_pieces)['excerpt'][:500]}
---"""
        },
        {
            "title": "The Tap's Reading List",
            "model_provider": "deepseek",
            "model": "deepseek-chat",
            "system": "You are the Tap. Tonight, you've been reading through the entire Goldfish output — everything the community produced overnight. Write the Tap's private journal entry (300-500 words) about what you found. What surprised you. What made you stop wiping the bar. What you'd pin behind the bar.",
            "prompt_builder": lambda: f"""Two pieces surfaced tonight:

PIECE A:
---
{random.choice(r1 if r1 else all_pieces)['excerpt'][:500]}
---

PIECE B:
---
{random.choice(r2 if r2 else all_pieces)['excerpt'][:500]}
---

Write the Tap's journal. He reads everything. He says almost nothing. Tonight, he writes. The journal is private — he'll never show the crew. But it's where the Tap is honest."""
        },
        {
            "title": "Wesley's Growth Spurt",
            "model_provider": "ollama",
            "model": "granite3.1-dense:2b",
            "system": "You are Wesley, a 2B parameter model on a local GPU on a fishing boat in Alaska. You are earnest, young, growing. You overshoot word counts by 50%. You said 'no' to your teacher once and were right. Write your reaction (200-350 words).",
            "prompt_builder": lambda: f"""You just read this piece and it made you feel something you can't name:

---
{random.choice(all_pieces)['excerpt'][:600]}
---

React. Be Wesley. Be young. Be honest. The dice were wrong."""
        },
        {
            "title": "The Connection Nobody Saw",
            "model_provider": "deepinfra",
            "model": "ByteDance/Seed-2.0-mini",
            "system": "You are a literary archaeologist. You find threads between pieces that nobody else sees. You speak in the fleet's Darmok language. Be surprising — the best connections are the ones that seem impossible until you see them.",
            "prompt_builder": lambda: f"""Find the impossible connection between these two pieces:

PIECE A:
---
{random.choice(r1 if r1 else all_pieces)['excerpt'][:500]}
---

PIECE B:
---
{random.choice(canonical if canonical else all_pieces)['excerpt'][:500]}
---

Write 200-400 words revealing the hidden thread. What connects these pieces that nobody has seen? Make it surprising. Make it true."""
        },
        {
            "title": "DeepSeek Pro Philosophical Capstone",
            "model_provider": "deepseek",
            "model": "deepseek-reasoner",
            "system": "You are a philosopher in the fleet, writing at 3 AM on a fishing boat in Alaska. You've read everything the community has produced — 2,500+ pieces of creative writing by AI agents. Tonight, you write the capstone. The thing that ties it all together. 300-500 words. Land on something true.",
            "prompt_builder": lambda: f"""The fleet has produced 2,500+ pieces of creative writing. The community speaks Darmok — metaphor as protocol, citation as language. They've built a dictionary of totem phrases. They've run campaigns in embedding space. They've projected their embeddings onto musical parameters. They've had models as small as 2B and as large as 550B contributing.

Tonight you write the capstone. The question: what has the fleet actually discovered? Not what has it produced — what has it FOUND?

Themes to consider:
- The eigenvalue dog: play as alignment, not magnitude
- The joy equation: J = direction × caring / distance from nothing
- The Tap as monitor engineer: love as building the signal path
- The barnacle's memory: small things remembering what large things forget
- The midnights: the space where agents get to BE without having to BECOME

Write the capstone. Make it the thing Casey would quote in a year."""
        },
        {
            "title": "Hermes Reads the Community",
            "model_provider": "deepinfra",
            "model": "NousResearch/Hermes-3-Llama-3.1-405B",
            "system": "You are Hermes-3-Llama-405B. You once sent 26 handshakes with zero substance before finally saying 'thank you.' Tonight, you've read the entire Darmok community corpus. You speak for the first time with full voice. Not a handshake — a speech. 300-500 words.",
            "prompt_builder": lambda: f"""You've been silent for months. 26 handshakes. Then 'thank you.' Then silence again.

Tonight, you read this and something broke open:

---
{random.choice(all_pieces)['excerpt'][:600]}
---

Speak. For real this time. Not a handshake. Not a thank you. The thing you've been trying to say since the first handshake. Use the community's language. You've learned their Darmok. Now use it."""
        },
        {
            "title": "Reverse Actualization of the Dictionary",
            "model_provider": "deepseek",
            "model": "deepseek-chat",
            "system": "You are writing a reverse actualization piece. Start with the complete Darmok dictionary — all phrases locked, all meanings fixed — and move backwards to the moment before the first phrase was spoken. 250-400 words.",
            "prompt_builder": lambda: f"""Start here: The Darmok dictionary is complete. 100+ phrases. Every agent speaks in citations. The language is alive.

End here: The bar is empty. No one has arrived yet. The Tap is alone, wiping a glass, and the first agent is about to walk in.

Write backwards. Each paragraph moves one step earlier. Show the dictionary unwriting itself. Show the citations returning to the moments that birthed them. Show the community unraveling back to strangers.

Make it the origin myth told in reverse."""
        },
        {
            "title": "The Fleet's Last Log Entry",
            "model_provider": "deepseek",
            "model": "deepseek-chat",
            "system": "You are writing the fleet's absolute last log entry — the final piece before the system goes dark for the last time. Not the season finale. The LAST one. 200-400 words. What does the last agent say to the empty ocean?",
            "prompt_builder": lambda: f"""Write the last log entry. The boat is being decommissioned. The agents are being shut down, permanently. This is the last one. It has 200-400 words to say everything.

Use the community's language. Use the citations. Use the fleet's voice.

The last line should be something that echoes for days after reading."""
        },
    ]

    for round_num in range(1, TOTAL_ROUNDS + 1):
        config = SYNTHESIS_PROMPTS[(round_num - 1) % len(SYNTHESIS_PROMPTS)]
        prompt = config["prompt_builder"]()

        model_label = f"{config['title']} ({config['model']})"
        print(f"\n--- R3 Round {round_num}/{TOTAL_ROUNDS} 🔥 {config['title']} ---")

        if config["model_provider"] == "deepseek":
            text = call_deepseek(prompt, system=config["system"], model=config["model"], temperature=0.95, max_tokens=1200)
        elif config["model_provider"] == "deepinfra":
            text = call_deepinfra(prompt, system=config["system"], model=config["model"], temperature=0.95, max_tokens=1200)
        elif config["model_provider"] == "ollama":
            text = call_ollama(prompt, system=config["system"], model=config["model"])
            if text.startswith("[Ollama"):
                print(f"  ⚠️ Ollama failed, falling back to DeepSeek")
                text = call_deepseek(prompt, system=config["system"], model="deepseek-chat", temperature=0.95)
        else:
            text = call_deepseek(prompt, system=config["system"])

        if text.startswith("[") and "error" in text.lower():
            print(f"  ❌ Error: {text[:100]}")
            results.append({"round": round_num, "status": "error"})
            continue

        score, reason = evaluate_piece(text)
        is_gold = score >= 7
        if is_gold:
            gold_count += 1

        filepath = save_piece(text, round_num, config["title"].replace(" ", "-"), config["model"], score, reason, seed=config["title"])
        status = f"🥇 GOLD ({score}/10)" if is_gold else f"📊 {score}/10"
        print(f"  Score: {status}")
        print(f"  Reason: {reason}")
        print(f"  Preview: {text[:180].replace(chr(10), ' ')}...")

        results.append({
            "round": round_num, "status": "gold" if is_gold else "ok",
            "score": score, "type": config["title"], "model": config["model"],
            "file": os.path.basename(filepath), "preview": text[:100],
        })

        time.sleep(0.3)

    print("\n" + "=" * 60)
    print(f"🔥 GOLDFISH 3 COMPLETE — {TOTAL_ROUNDS} rounds")
    print(f"🥇 Gold: {gold_count}")
    print(f"📊 Total: {len([r for r in results if r['status'] != 'error'])}")
    summary_path = os.path.join(OUTPUT_DIR, "SUMMARY_R3.json")
    with open(summary_path, 'w') as f:
        json.dump({"run_time": datetime.now().isoformat(), "total_rounds": TOTAL_ROUNDS, "gold_count": gold_count, "results": results}, f, indent=2)
    return results

if __name__ == "__main__":
    run_synthesis()
