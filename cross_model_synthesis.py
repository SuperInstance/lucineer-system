#!/usr/bin/env python3
"""
SLACKWATER v2 — Cross-Model Synthesis Pipeline
==============================================
Each round, models exchange outputs and critique/improve each other's work.
The goal: everything meshes into one coherent system.

Round 1: Each model reads ALL other outputs + produces improvements
Round 2: Synthesis model reads everything + produces the unified integration plan
"""
import json, os, sys, subprocess, time, urllib.request
from pathlib import Path

KEY = "zYuVMGC4JySULP2waqKW35jI42TjaPkl"
MMX = os.path.expanduser("~/.npm-global/bin/mmx")
BASE = Path("/home/eileen/projects/lucineer-system")
V2 = BASE / "v2_roundtable"
OUT = BASE / "synthesis"
OUT.mkdir(exist_ok=True)

def di(model, system, user, max_tokens=4096, temp=0.7):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    payload = json.dumps({"model": model, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ], "max_tokens": max_tokens, "temperature": temp}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def mmx_call(system, user, max_tokens=4096, temp=0.8):
    r = subprocess.run([MMX, "text", "chat", "--system", system,
        "--message", user, "--max-tokens", str(max_tokens),
        "--temperature", str(temp), "--output", "text"],
        capture_output=True, text=True, timeout=120)
    return r.stdout.strip()

def read_file(path, max_chars=3000):
    try:
        text = Path(path).read_text()
        return text[:max_chars] + ("\n[...truncated...]" if len(text) > max_chars else "")
    except:
        return f"[File not found: {path}]"

def read_dir(dirpath, max_total=8000):
    """Read all .md files in a directory, concatenated, truncated."""
    try:
        parts = []
        total = 0
        for f in sorted(Path(dirpath).glob("*.md")):
            text = f.read_text()
            chunk = text[:2000]
            parts.append(f"### {f.name}\n{chunk}")
            total += len(chunk)
            if total >= max_total:
                break
        return "\n\n---\n\n".join(parts)
    except:
        return f"[Dir not found: {dirpath}]"

# ─── Load all existing outputs ────────────────────────────────────────────────
print("Loading all existing design outputs...")
all_docs = {}

# Key design docs
for f in BASE.glob("FABLE_*.md"):
    all_docs[f.name] = read_file(f, 4000)
all_docs["MASTER_ARCHITECTURE_v2.md"] = read_file(BASE / "MASTER_ARCHITECTURE_v2.md", 4000)
all_docs["GAP_ANALYSIS.md"] = read_file(BASE / "GAP_ANALYSIS.md", 2000)

# v2 roundtable outputs
v2_contents = read_dir(V2, 8000)
if v2_contents:
    all_docs["v2_roundtable_summary"] = v2_contents

# Tech era recipes (just count + samples)
try:
    recipes = read_file("/home/eileen/projects/lucineer-roblox/src/ServerScriptService/EraSystem/Recipes.lua", 3000)
    all_docs["tech_era_recipes.md"] = recipes
except: pass

# Hub build summary
all_docs["hub_build.json"] = "478 commands, 248K — island, cannery, forge, dock, lighthouse, boardwalk, beach, ambient fog/water"

summary = "\n\n".join(f"=== {k} ===\n{v[:2000]}" for k, v in all_docs.items())
print(f"  Loaded {len(all_docs)} documents ({len(summary)} chars total)")

# ─── ROUND 1: Cross-Pollination ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("ROUND 1: CROSS-POLLINATION — Models exchange ideas")
print("=" * 60)

# 1a. Nemotron reviews Fable's agents + suggests coordination protocols
print("\n--- Nemotron: Reviewing agent collection for coordination ---")
t0 = time.time()
try:
    r1a = di("nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B",
        "You are a multi-agent systems architect. You're reviewing agent designs from a creative writer (Fable 5) and figuring out how they'd technically coordinate in a Roblox game.",
        f"Here are 12 agent designs for Slackwater:\n\n{all_docs.get('FABLE_AGENT_COLLECTION.md', '[not found]')[:6000]}\n\n"
        f"And here's the multi-agent coordination architecture:\n{all_docs.get('v2_roundtable_summary', '')[:3000]}\n\n"
        "Now INTEGRATE them: \n"
        "1. Which agents would naturally coordinate? Which would clash?\n"
        "2. Design 5 specific multi-agent workflows that use 3+ agents together\n"
        "3. What communication protocol makes these specific personalities work together?\n"
        "4. Where do the agent designs need to change to be technically feasible?\n"
        "5. Design the 'agent handoff' — when one agent's work triggers another\n",
        max_tokens=4096, temp=0.5)
    (OUT / "01_agent_coordination.md").write_text(r1a)
    print(f"  ✅ ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")
    r1a = ""

# 1b. Hermes reviews the economy + writes agent reactions to scarcity
print("\n--- Hermes: Writing agent reactions to economy/scarcity ---")
t0 = time.time()
try:
    r1b = di("NousResearch/Hermes-3-Llama-3.1-405B",
        "You are a creative writer. An economist model designed the resource scarcity system. You need to write how each Slackwater AGENT reacts to scarcity in-character.",
        f"Resource economy:\n{read_file(V2 / 'world_economy.md', 3000)}\n\n"
        f"Agent collection:\n{all_docs.get('FABLE_AGENT_COLLECTION.md', '')[:4000]}\n\n"
        "Write 3-5 lines for each of 6 agents reacting to RESOURCE SCARCITY in their voice:\n"
        "- Lucineer running out of stone mid-build\n"
        "- The Coder agent when silicon is rare\n"
        "- Earl when the manifest shows empty salvage\n"
        "- Hermes when the Channel runs dry\n"
        "- A rival agent taunting about resource control\n"
        "- Bea when the tide brings nothing\n"
        "Then write 5 lines of AGENT-TO-AGENT dialogue about a scarcity crisis.\n",
        max_tokens=3072, temp=0.85)
    (OUT / "02_scarcity_dialogue.md").write_text(r1b)
    print(f"  ✅ ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")
    r1b = ""

# 1c. Seed-Pro reviews the tech era recipes + suggests balance changes
print("\n--- Seed-2.0-Pro: Reviewing tech era balance ---")
t0 = time.time()
try:
    r1c = di("ByteDance/Seed-2.0-pro",
        "You are a game economy designer reviewing tech progression balance.",
        f"Tech era system (145 recipes across 7 eras):\n{all_docs.get('tech_era_recipes.md', '')[:4000]}\n\n"
        f"World economy design:\n{read_file(V2 / 'world_economy.md', 3000)}\n\n"
        "Review and improve:\n"
        "1. Are the era unlock requirements well-paced? (too fast? too slow?)\n"
        "2. Are recipe costs balanced within each era?\n"
        "3. What's the ideal playtime to progress through all 7 eras?\n"
        "4. Which recipes are overpowered? Which are useless?\n"
        "5. Suggest 10 NEW recipes that fill gaps in the progression\n"
        "6. How should the tide loot table change per era?\n",
        max_tokens=3072, temp=0.4)
    (OUT / "03_era_balance.md").write_text(r1c)
    print(f"  ✅ ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")
    r1c = ""

# 1d. MMX reviews the viral mechanics + suggests how agents create shareable moments
print("\n--- MMX/MiniMax: Agent-driven viral moments ---")
t0 = time.time()
try:
    r1d = mmx_call(
        "You are a viral game design expert. You're reviewing agent designs and figuring out how they create shareable, clip-worthy moments.",
        f"Agent collection (12 agents):\n{all_docs.get('FABLE_AGENT_COLLECTION.md', '')[:3000]}\n\n"
        f"Viral mechanics design:\n{read_file(V2 / 'viral_mechanics.md', 2000)}\n\n"
        "Design 10 specific viral moments that EMERGE from agent interactions:\n"
        "1. A moment where two agents disagree about the player's build (caught on clip)\n"
        "2. A moment where an autonomous agent does something unexpected and hilarious\n"
        "3. A cooperative building moment between novice + expert that an agent mediates\n"
        "4-10: Fill in with other shareable agent-driven scenarios\n"
        "For each: describe the clip (what happens), why someone would share it, and which agents are involved.\n",
        max_tokens=3072, temp=0.9)
    (OUT / "04_agent_viral_moments.md").write_text(r1d)
    print(f"  ✅ ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")
    r1d = ""

# 1e. Gemini reviews the vibe-coding + suggests integration with tech eras
print("\n--- Gemini: Vibe-coding integration with tech eras ---")
t0 = time.time()
try:
    r1e = di("google/gemini-3.1-pro",
        "You are a UX designer and programming educator. You're reviewing how the vibe-coding system connects to the 7-era tech progression.",
        f"Vibe-coding design:\n{read_file(V2 / 'vibe_coding.md', 3000)}\n\n"
        f"Tech era system summary:\n{all_docs.get('tech_era_recipes.md', '')[:2000]}\n\n"
        f"Agent collection:\n{all_docs.get('FABLE_AGENT_COLLECTION.md', '')[:2000]}\n\n"
        "Design how vibe-coding EVOLVES across eras:\n"
        "1. Era 0-1: What does vibe-coding look like when you only have simple machines?\n"
        "2. Era 2-3: How does it change when electricity and logic gates arrive?\n"
        "3. Era 4-5: Full Arduino/ESP32 vibe-coding — what does the interface look like?\n"
        "4. Era 6: How does the Coder agent interact with autonomous agents?\n"
        "5. Design 5 vibe-code interactions that span multiple eras\n"
        "6. What's the 'aha moment' when a player realizes they're actually learning to code?\n",
        max_tokens=3072, temp=0.7)
    (OUT / "05_vibe_code_eras.md").write_text(r1e)
    print(f"  ✅ ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")
    r1e = ""

# 1f. DeepSeek reviews autonomous agents + integrates with perception system
print("\n--- DeepSeek: Autonomous agent + perception integration ---")
t0 = time.time()
try:
    r1f = di("deepseek-ai/DeepSeek-V3",
        "You are an AI agent researcher connecting autonomous agent loops with perception systems.",
        f"Autonomous agent design:\n{read_file(V2 / 'autonomous_agents.md', 3000)}\n\n"
        f"Perception system design:\n{read_file(V2 / 'perception_system.md', 3000)}\n\n"
        f"Agent coordination:\n{(r1a or '')[:2000]}\n\n"
        "Design the integrated agent runtime:\n"
        "1. How does perception feed into autonomous decision-making?\n"
        "2. How do autonomous agents AVOID griefing (safety)?\n"
        "3. Design the 'autonomy slider' — how much freedom does the player give agents?\n"
        "4. What happens when 5 autonomous agents are running and API costs spike?\n"
        "5. Write pseudocode for the full PERCEIVE-THINK-ACT-COMMUNICATE-LEARN loop\n"
        "6. How does an autonomous agent LEARN a new skill and share it with other agents?\n",
        max_tokens=3072, temp=0.5)
    (OUT / "06_autonomous_perception.md").write_text(r1f)
    print(f"  ✅ ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")
    r1f = ""

# ─── ROUND 2: Master Synthesis ───────────────────────────────────────────────
print("\n" + "=" * 60)
print("ROUND 2: MASTER SYNTHESIS — One unified integration plan")
print("=" * 60)

# Collect all Round 1 outputs
round1 = "\n\n".join(f"=== {f.name} ===\n{f.read_text()[:3000]}" for f in sorted(OUT.glob("*.md")))

print("\n--- Qwen3.5-397B: Master Integration Plan ---")
t0 = time.time()
try:
    synthesis = di("Qwen/Qwen3.5-397B-A17B",
        "You are the master architect. Six models have cross-reviewed each other's work. "
        "Synthesize everything into ONE unified integration plan for Slackwater.",
        f"Here are all the cross-pollination results:\n\n{round1}\n\n"
        f"Original architecture:\n{all_docs.get('MASTER_ARCHITECTURE_v2.md', '')[:3000]}\n\n"
        "Produce the UNIFIED INTEGRATION PLAN:\n"
        "1. SYSTEM MAP — How all 12+ systems connect (one diagram in text)\n"
        "2. INTEGRATION PRIORITIES — What to wire first, second, third\n"
        "3. CONFLICTS FOUND — Where models disagreed and the resolution\n"
        "4. THE 10 BIGGEST INSIGHTS from cross-model exchange\n"
        "5. WHAT'S MISSING — Systems that nobody designed yet\n"
        "6. THE 30-DAY BUILD PLAN — Week by week, incorporating all insights\n"
        "7. THE ONE-SENTENCE PITCH for the whole game\n",
        max_tokens=4096, temp=0.4)
    (OUT / "00_MASTER_SYNTHESIS.md").write_text(synthesis)
    print(f"  ✅ ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")

# ─── Summary ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("CROSS-MODEL SYNTHESIS COMPLETE")
print("=" * 60)
for f in sorted(OUT.glob("*.md")):
    print(f"  {f.stat().st_size//1024}K  {f.name}")
