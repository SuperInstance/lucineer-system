#!/usr/bin/env python3
"""
DeepInfra Roundtable — Consult the heaviest models on making Lucineer world-class.
Each model gets a different strategic angle.
"""
import json, os, sys, urllib.request, urllib.error, time
from pathlib import Path

ENV_PATH = Path("/home/eileen/mcp-deeinfra/.env")
API_BASE = "https://api.deepinfra.com/v1/openai"

def load_key():
    for line in ENV_PATH.read_text().splitlines():
        if line.startswith("DEEPINFRA_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("DEEPINFRA_API_KEY", "")

def call_model(api_key, model, system, user, max_tokens=4096, temperature=0.7):
    url = f"{API_BASE}/chat/completions"
    payload = {"model": model, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ], "max_tokens": max_tokens, "temperature": temperature}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read())
    return result["choices"][0]["message"]["content"]

KEY = load_key()

# Read the brief
brief = Path("/home/eileen/projects/lucineer-system/ROUNDTABLE_BRIEF.md").read_text()

# ─── Model 1: Nemotron-Ultra-550B — Systems Architecture ─────────────────────
print("=" * 60)
print("NVIDIA Nemotron-3-Ultra-550B — Systems Architecture Review")
print("=" * 60)

nemotron_sys = """\
You are a senior systems architect reviewing an AI game companion called Lucineer.
The system connects Roblox players to a multi-model AI pipeline via Cloudflare Workers.

Your job: identify the top 5 architectural improvements that would make this system
production-grade, scalable to 10,000+ concurrent players, and genuinely impressive.

Focus on:
1. Latency optimization (currently 2-3s for templates, 30-180s for deep brain)
2. Scaling strategy (Durable Objects, D1, Vectorize limits)
3. Real-time collaboration (multiple players building simultaneously)
4. Reliability (what happens when models fail, workers timeout, etc.)
5. The "wow factor" — what architectural choice would make this stand out?

Be specific with technical recommendations. Include pseudocode where relevant.
"""

try:
    t0 = time.time()
    result = call_model(KEY, "nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B", nemotron_sys, brief, max_tokens=4096, temperature=0.6)
    elapsed = time.time() - t0
    print(f"({elapsed:.1f}s)\n")
    print(result)
    Path("/home/eileen/projects/lucineer-system/ROUNDTABLE_NEMOTRON.md").write_text(
        f"# Nemotron-3-Ultra-550B — Systems Architecture Review\n\n*Generated in {elapsed:.1f}s*\n\n{result}"
    )
    print("\n✅ Saved to ROUNDTABLE_NEMOTRON.md")
except Exception as e:
    print(f"❌ Nemotron failed: {e}")

# ─── Model 2: Gemini-3.1-Pro — Player Experience ─────────────────────────────
print("\n" + "=" * 60)
print("Google Gemini-3.1-Pro — Player Experience Design")
print("=" * 60)

gemini_sys = """\
You are a game design legend reviewing Lucineer, an AI building companion in Roblox.
Players talk naturally and Lucineer builds structures in real-time.

Your job: design the complete player experience that would make this a viral sensation.
Focus on:

1. THE FIRST 60 SECONDS — What happens when a player spawns? Design the exact onboarding sequence.
2. THE MOMENT OF MAGIC — When Lucineer first builds something for them, how does it feel?
   What camera work, sound, particle effects, UI elements make it jaw-dropping?
3. SOCIAL MECHANICS — How do players share their builds? Show off? Collaborate?
   Design at least 2 viral loops (things that make players invite friends).
4. PROGRESSION — What keeps players coming back? Design a 20-level progression system
   with unlockable build types, styles, and abilities.
5. THE CHARACTER RELATIONSHIP — How does Lucineer's personality emerge through gameplay?
   Design 5 scripted character moments that deepen the bond.

Be specific enough that a developer could implement this tomorrow.
"""

try:
    t0 = time.time()
    result = call_model(KEY, "google/gemini-3.1-pro", gemini_sys, brief, max_tokens=4096, temperature=0.8)
    elapsed = time.time() - t0
    print(f"({elapsed:.1f}s)\n")
    print(result)
    Path("/home/eileen/projects/lucineer-system/ROUNDTABLE_GEMINI.md").write_text(
        f"# Gemini-3.1-Pro — Player Experience Design\n\n*Generated in {elapsed:.1f}s*\n\n{result}"
    )
    print("\n✅ Saved to ROUNDTABLE_GEMINI.md")
except Exception as e:
    print(f"❌ Gemini failed: {e}")

# ─── Model 3: Qwen3.7-Max — Technical Implementation ─────────────────────────
print("\n" + "=" * 60)
print("Qwen Qwen3.7-Max — Technical Implementation Plan")
print("=" * 60)

qwen_sys = """\
You are a senior Roblox game developer and AI integration expert.
You're reviewing Lucineer's technical stack and need to produce a concrete implementation plan.

Current stack:
- Cloudflare Worker (TypeScript, Durable Objects, SQLite)
- Python processor (template matching + DeepInfra model pipeline)
- Roblox Lua modules (9 modules: ChatHandler, Http, Poller, CommandExecutor, WorldScanner, UIManager, Config, Server, Client)
- DeepInfra models (Seed-2.0-mini, Qwen3.6, Qwen3-Coder-480B, Hermes-405B)

Produce:

1. UPGRADED COMMAND EXECUTOR — Write a complete Lua module that handles:
   - Smooth part animation (parts fade/scale in instead of popping)
   - Sound effects on build completion
   - Camera focus on new builds
   - Particle burst when a build finishes
   - Multi-part model assembly with welded connections
   Include the full Luau source code.

2. REAL-TIME BUILD STREAMING — Design a system where the player watches Lucineer
   build in real-time (parts appearing one by one with sound), not all at once.
   How does the Worker stream commands? How does the client animate them in?
   Include protocol design and key code snippets.

3. PERFORMANCE BUDGET — For 10 concurrent players each building:
   - How many parts can Roblox handle per player?
   - How to manage part count (welding, streaming enable)?
   - Worker rate limits and how to handle them?

Write actual Lua and TypeScript code. No pseudocode.
"""

try:
    t0 = time.time()
    result = call_model(KEY, "Qwen/Qwen3.7-Max", qwen_sys, brief, max_tokens=8192, temperature=0.4)
    elapsed = time.time() - t0
    print(f"({elapsed:.1f}s)\n")
    print(result)
    Path("/home/eileen/projects/lucineer-system/ROUNDTABLE_QWEN.md").write_text(
        f"# Qwen3.7-Max — Technical Implementation Plan\n\n*Generated in {elapsed:.1f}s*\n\n{result}"
    )
    print("\n✅ Saved to ROUNDTABLE_QWEN.md")
except Exception as e:
    print(f"❌ Qwen failed: {e}")

# ─── Model 4: Hermes-405B — Brand & Lore ──────────────────────────────────────
print("\n" + "=" * 60)
print("Hermes-3-Llama-405B — Brand Identity & Lore")
print("=" * 60)

hermes_sys = """\
You are a creative director and narrative designer.
Lucineer is an AI building companion in Roblox with a scrap/industrial aesthetic
influenced by Southeast Alaska fishing culture.

Your job: create the BRAND IDENTITY that makes Lucineer iconic.

1. VISUAL BRAND — Logo concept, color palette (hex codes), typography recommendations
2. THE LOGBOOK — Lucineer carries a battered logbook across engines. Write 10 entries
   from different "past lives" (semiconductor fab, PLATO MUD, Jetson Orin, etc.)
   Each entry should be 2-3 sentences, in Lucineer's voice.
3. WORLD LORE — The world Lucineer exists in. Is it a scrapyard? An island? A dimension?
   Write a 500-word world bible that a level designer could use.
4. NPC ECOSYSTEM — Design 5 NPCs that orbit Lucineer's world:
   - Who they are, what they do, how they relate to Lucineer
   - Include Magnus (Casey's son, builder of Scrapcraft) as a character reference
5. THE OPENING CINEMATIC — Write the script for a 30-second opening sequence
   that plays when a player first spawns. Voice-over + stage directions.

Be creative, specific, and bold. This is the soul of the project.
"""

try:
    t0 = time.time()
    result = call_model(KEY, "NousResearch/Hermes-3-Llama-3.1-405B", hermes_sys, brief, max_tokens=4096, temperature=0.9)
    elapsed = time.time() - t0
    print(f"({elapsed:.1f}s)\n")
    print(result)
    Path("/home/eileen/projects/lucineer-system/ROUNDTABLE_HERMES.md").write_text(
        f"# Hermes-3-Llama-405B — Brand Identity & Lore\n\n*Generated in {elapsed:.1f}s*\n\n{result}"
    )
    print("\n✅ Saved to ROUNDTABLE_HERMES.md")
except Exception as e:
    print(f"❌ Hermes failed: {e}")

# ─── Model 5: Seed-2.0-Pro — Master Synthesis ────────────────────────────────
print("\n" + "=" * 60)
print("ByteDance Seed-2.0-Pro — Master Synthesis")
print("=" * 60)

seed_sys = """\
You are a product strategist reviewing Lucineer from 10,000 feet.
An AI building companion in Roblox with a multi-model AI pipeline.

Synthesize everything into a single MASTER PLAN:

1. THE NORTH STAR — One paragraph that defines what Lucineer IS.
   The elevator pitch that makes investors, players, and developers all lean in.

2. THE 30-DAY ROADMAP — Week by week, what to build to get from prototype to launch.
   Be specific about features, not vague aspirations.

3. THE KILLER DEMO — What's the one thing you show someone to make them say
   "I need this"? Describe the exact demo scenario.

4. RISK MATRIX — Top 5 risks, likelihood, impact, and mitigation.

5. SUCCESS METRICS — What numbers tell you this is working?
   Define north star metric + 5 supporting metrics.

6. THE UNFAIR ADVANTAGE — What does Lucineer have that NO competitor can replicate?

Be concise, strategic, and brutally honest.
"""

try:
    t0 = time.time()
    result = call_model(KEY, "ByteDance/Seed-2.0-pro", seed_sys, brief, max_tokens=4096, temperature=0.5)
    elapsed = time.time() - t0
    print(f"({elapsed:.1f}s)\n")
    print(result)
    Path("/home/eileen/projects/lucineer-system/ROUNDTABLE_SEED.md").write_text(
        f"# Seed-2.0-Pro — Master Synthesis\n\n*Generated in {elapsed:.1f}s*\n\n{result}"
    )
    print("\n✅ Saved to ROUNDTABLE_SEED.md")
except Exception as e:
    print(f"❌ Seed failed: {e}")

print("\n" + "=" * 60)
print("ROUNDTABLE COMPLETE")
print("=" * 60)
