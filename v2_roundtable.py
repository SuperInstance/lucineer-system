#!/usr/bin/env python3
"""
DeepInfra + MMX Wide Parallel Roundtable for SLACKWATER v2
Each model gets a different strategic angle on the expanded vision.
"""
import json, os, sys, subprocess, time, urllib.request
from pathlib import Path

KEY = "zYuVMGC4JySULP2waqKW35jI42TjaPkl"
MMX = os.path.expanduser("~/.npm-global/bin/mmx")
OUT = Path("/home/eileen/projects/lucineer-system/v2_roundtable")
OUT.mkdir(exist_ok=True)
BRIEF = Path("/home/eileen/projects/lucineer-system/MASTER_ARCHITECTURE_v2.md").read_text()

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

def mmx(system, user, max_tokens=4096, temp=0.8):
    r = subprocess.run([MMX, "text", "chat", "--system", system,
        "--message", user, "--max-tokens", str(max_tokens),
        "--temperature", str(temp), "--output", "text"],
        capture_output=True, text=True, timeout=120)
    return r.stdout.strip()

def save(name, model, content, elapsed):
    path = OUT / f"{name}.md"
    path.write_text(f"# {name.replace('_',' ').title()} — {model}\n\n*Generated in {elapsed:.1f}s*\n\n{content}")
    print(f"  ✅ Saved to {path.name}")

# ─── 1. Nemotron-Ultra-550B: Multi-Agent Architecture ─────────────────────
print("=== Nemotron-3-Ultra-550B: Multi-Agent Coordination ===")
t0 = time.time()
try:
    result = di("nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B",
        """You are a distributed systems architect specializing in multi-agent coordination.
        Design how 5-20 AI agents can simultaneously operate in a Roblox world without
        stepping on each other, freezing the game, or burning through API credits.""",
        BRIEF + "\n\nDesign the complete multi-agent coordination architecture:\n"
        "1. Agent message bus protocol (how agents communicate)\n"
        "2. Task partitioning algorithm (how they divide work automatically)\n"
        "3. Conflict resolution (two agents want the same resource/position)\n"
        "4. API budget management (how to run 20 agents without going broke)\n"
        "5. The perception pipeline (how agents 'see' the world — screenshot frequency, world state queries)\n"
        "6. Fleet management UI design\n"
        "Be specific with data structures and pseudocode.",
        max_tokens=4096, temp=0.5)
    save("multi_agent_architecture", "Nemotron-Ultra-550B", result, time.time()-t0)
except Exception as e:
    print(f"  ❌ Nemotron failed: {e}")

# ─── 2. Gemini-3.1-Pro: Vibe-Coding Interface ─────────────────────────────
print("\n=== Gemini-3.1-Pro: Vibe-Coding Interface ===")
t0 = time.time()
try:
    result = di("google/gemini-3.1-pro",
        """You are a UX designer and programming educator. Design the vibe-coding system
        for Slackwater — where players describe what they want in natural language and
        a coder agent generates working gamified code.""",
        BRIEF + "\n\nDesign the complete vibe-coding experience:\n"
        "1. The Coder agent's interface — how does the player interact? (chat window? tablet device in-game? voice?)\n"
        "2. How does 'approximated code that just works' actually function technically?\n"
        "3. Design 10 example vibe-code interactions (player says X → system generates Y)\n"
        "4. The deep-dive pathway — how does a curious player learn the REAL code behind the approximation?\n"
        "5. How does the vibe-coder handle errors gracefully (in-character)?\n"
        "6. Connection to real Arduino/ESP32 firmware export (like Scrapcraft)\n"
        "Be specific. Include UI mockup descriptions and example dialogues.",
        max_tokens=4096, temp=0.7)
    save("vibe_coding", "Gemini-3.1-Pro", result, time.time()-t0)
except Exception as e:
    print(f"  ❌ Gemini failed: {e}")

# ─── 3. Seed-2.0-Pro: Procedural World Economy ────────────────────────────
print("\n=== Seed-2.0-Pro: World Economy & Balance ===")
t0 = time.time()
try:
    result = di("ByteDance/Seed-2.0-pro",
        """You are a game economy designer. Design the resource economy for a 7-era
        technology progression game where scarcity drives exploration and the tide
        delivers procedural loot twice per cycle.""",
        BRIEF + "\n\nDesign the complete economic system:\n"
        "1. Resource scarcity curves per era (what's rare in each era?)\n"
        "2. Tide loot tables (what washes in? probability weights?)\n"
        "3. Crafting cost progression (how costs scale with era)\n"
        "4. Agent labor economy (what does it 'cost' to deploy an agent?)\n"
        "5. Trade system between players in multiplayer\n"
        "6. The scarcity-forces-exploration loop (when does player need to go further?)\n"
        "Include actual numbers and probability tables.",
        max_tokens=4096, temp=0.4)
    save("world_economy", "Seed-2.0-Pro", result, time.time()-t0)
except Exception as e:
    print(f"  ❌ Seed failed: {e}")

# ─── 4. Qwen3-Coder-480B: Perception Agent Implementation ─────────────────
print("\n=== Qwen3-Coder-480B: Perception Agent ===")
t0 = time.time()
try:
    result = di("Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo",
        """You are a senior Roblox developer and AI integration expert. Write production code
        for the perception agent system — AI agents that can 'see' the Roblox game world
        and react to what's happening.""",
        BRIEF + "\n\nWrite the complete perception system:\n\n"
        "1. /home/eileen/projects/lucineer-roblox/src/ServerScriptService/PerceptionSystem/init.lua\n"
        "   - Captures the game state as a structured snapshot (player positions, nearby parts, power flow, active agents)\n"
        "   - Serializes to compact JSON for model consumption\n"
        "   - Runs on a configurable interval (default: every 5 seconds for active agents, 30s for idle)\n\n"
        "2. A Python perception processor at /home/eileen/projects/lucineer-system/perception_agent.py\n"
        "   - Receives world state snapshots\n"
        "   - Uses DeepInfra Qwen3-VL-235B to analyze screenshots if provided\n"
        "   - Uses Seed-2.0-mini for fast state assessment\n"
        "   - Generates proactive observations and suggestions\n"
        "   - Routes observations to the appropriate agent's dialogue queue\n\n"
        "3. Design the screenshot pipeline:\n"
        "   - How to capture Roblox viewport server-side (or client-side relay)\n"
        "   - Image compression for API transmission\n"
        "   - When to trigger visual analysis vs. pure state analysis\n\n"
        "Write actual complete code. Lua + Python.",
        max_tokens=8192, temp=0.3)
    save("perception_system", "Qwen3-Coder-480B", result, time.time()-t0)
except Exception as e:
    print(f"  ❌ Qwen failed: {e}")

# ─── 5. Hermes-405B: Agent Dialogue Trees ─────────────────────────────────
print("\n=== Hermes-3-Llama-405B: Agent Dialogue ===")
t0 = time.time()
try:
    result = di("NousResearch/Hermes-3-Llama-3.1-405B",
        """You are a creative writer and game designer. Write the dialogue system for
        Slackwater's AI agents. Each agent needs a rich dialogue tree that covers
        teaching, arguing, storytelling, and idle chatter.""",
        BRIEF + "\n\nWrite complete dialogue content:\n\n"
        "1. For EACH of the 7 eras, write 10 lines that a Teacher agent would say when\n"
        "   introducing the core concept of that era. Make them vivid and memorable.\n\n"
        "2. Write 15 overheard conversations between agents (agent-to-agent chatter\n"
        "   that players overhear). These should reveal personality and world lore.\n"
        "   Format: [Agent A] ... [Agent B] ...\n\n"
        "3. Write 10 recruitment dialogues — one for each agent a player can recruit.\n"
        "   Each is a 4-6 line exchange that makes the player WANT this agent.\n\n"
        "4. Write 5 'deep dive' conversations — long-form (10+ lines each) where a\n"
        "   player asks an agent to explain a technology in depth. One per era (0-4).\n\n"
        "Make every line feel like it comes from a specific person with history.",
        max_tokens=4096, temp=0.85)
    save("agent_dialogue", "Hermes-405B", result, time.time()-t0)
except Exception as e:
    print(f"  ❌ Hermes failed: {e}")

# ─── 6. MMX/MiniMax-M3: Viral Mechanics & Social Design ───────────────────
print("\n=== MMX/MiniMax-M3: Viral Mechanics ===")
t0 = time.time()
try:
    result = mmx(
        "You are a social game design expert and viral mechanic specialist. You understand what makes players share, invite, and keep coming back.",
        BRIEF + "\n\nDesign the complete social and viral system:\n\n"
        "1. Design 5 viral mechanics that feel ORGANIC (not forced share buttons)\n"
        "2. The cooperative building experience — how does a novice + expert player work together?\n"
        "3. Design the 'agent showcase' — how do players show off their customized agents?\n"
        "4. The clip-worthy moment generator — what systems create shareable moments?\n"
        "5. The 7-day retention loop — what brings players back on day 2, 3, 7?\n"
        "6. Design 3 social spaces where players naturally gather\n\n"
        "Be specific. Think TikTok, YouTube Shorts, Discord clips.",
        max_tokens=4096, temp=0.9)
    save("viral_mechanics", "MiniMax-M3", result, time.time()-t0)
except Exception as e:
    print(f"  ❌ MMX failed: {e}")

# ─── 7. DeepSeek-V3: Autonomous Agent Loop ────────────────────────────────
print("\n=== DeepSeek-V3: Autonomous Agent Loop ===")
t0 = time.time()
try:
    result = di("deepseek-ai/DeepSeek-V3",
        """You are an AI agent researcher. Design the autonomous agent loop for Slackwater's
        deep research agents — agents that can independently explore, build, and learn
        without player instruction (inspired by Voyager and Steve for Minecraft).""",
        BRIEF + "\n\nDesign the complete autonomous agent system:\n\n"
        "1. The PERCEIVE-THINK-ACT-COMMUNICATE-LEARN loop — pseudocode for each stage\n"
        "2. How autonomous agents discover and learn new skills (Voyager-style skill library)\n"
        "3. How autonomous agents coordinate (Steve-style multi-agent task partitioning)\n"
        "4. Safety guardrails — what stops autonomous agents from griefing or destroying the world\n"
        "5. The player's control interface — pause, redirect, set goals for autonomous agents\n"
        "6. How autonomous mode changes the game feel (player as director vs. operator)\n\n"
        "Include pseudocode and specific model routing for each stage.",
        max_tokens=4096, temp=0.5)
    save("autonomous_agents", "DeepSeek-V3", result, time.time()-t0)
except Exception as e:
    print(f"  ❌ DeepSeek failed: {e}")

print("\n=== ROUNDTABLE v2 COMPLETE ===")
