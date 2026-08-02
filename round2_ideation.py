#!/usr/bin/env python3
"""
Round 2: Different models on MOLT + game design + agent culture
Each model gets a unique angle that matches its strengths.
"""
import json, os, sys, subprocess, time, urllib.request
from pathlib import Path

from loadkey import get_key as _gk; KEY = _gk()
MMX = os.path.expanduser("~/.npm-global/bin/mmx")
OUT = Path("/home/eileen/projects/lucineer-system/round2_ideation")
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

def save(name, model, content):
    (OUT / f"{name}.md").write_text(f"# {name.replace('_',' ').title()} — {model}\n\n{content}")
    print(f"  ✅ {name} ({len(content)} chars)")

# Read the Round 1 ideation synthesis for context
r1_synthesis = ""
try:
    r1_synthesis = Path("/home/eileen/projects/lucineer-system/nvidia_ideation/SYNTHESIS.md").read_text()[:4000]
except:
    pass

# Read the synergy docs summary
synergy_summary = """
Key findings from our 5 NVIDIA research docs:
1. NeMoClaw IS OpenClaw — we're already on NVIDIA's reference architecture
2. MOLT's RL loop could train agents through player feedback rewards
3. Nemotron 3 Ultra has 1M-token context + self-evolving agent capabilities
4. ACE for Games could give Lucineer a real voice (Chatterbox TTS)
5. No game studios using NVIDIA agent tech for NPCs — first-mover opportunity
6. MOPD (Multi-Teacher On-Policy Distillation) maps to our specialist agents
7. 7 concrete reward signals: build stability, recipe correctness, player satisfaction, agent cooperation, skill novelty, resource efficiency, task completion time
"""

print("=== ROUND 2: New models, new perspectives ===\n")

# ─── 1. Qwen3.5-397B: The implementation architect ──────────────────────────
print("--- Qwen3.5-397B: How to actually build the RL training loop ---")
t0 = time.time()
try:
    r = di("Qwen/Qwen3.5-397B-A17B",
        """You are a senior ML engineer who has shipped RL training systems to production.
        You think in code, data pipelines, and infrastructure costs. You're practical and specific.""",
        synergy_summary + "\n\n" +
        "Design the ACTUAL implementation for RL-trained game agents:\n\n"
        "1. What does the training data pipeline look like? (player interactions → reward signals → training batches)\n"
        "2. How do we collect reward signals from a Roblox game? (instrumentation, events, data schema)\n"
        "3. What's the minimal viable RL experiment? (smallest thing we can do to prove the concept)\n"
        "4. Can we do this on DeepInfra's API, or do we need self-hosted vLLM? What's the cost difference?\n"
        "5. Write pseudocode for the reward function — what Python would you write?\n"
        "6. How do we prevent reward hacking? (agents optimizing for the metric, not the experience)\n"
        "7. What's the 2-week sprint plan to get from here to a working proof-of-concept?\n",
        max_tokens=4096, temp=0.4)
    save("01_qwen_implementation", "Qwen3.5-397B", r)
    print(f"  ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")

# ─── 2. Hermes-405B: The narrative philosopher ────────────────────────────────
print("\n--- Hermes-405B: What does it mean for a character to learn? ---")
t0 = time.time()
try:
    r = di("NousResearch/Hermes-3-Llama-3.1-405B",
        """You are a philosopher of mind and narrative designer. You think about what it MEANS
        for an AI character to learn, grow, and change. You're not interested in the implementation —
        you're interested in the EXPERIENTIAL implications. What does the player feel? What does the
        agent become? What are the philosophical implications of a character that genuinely evolves?""",
        synergy_summary + "\n\n" +
        "Think deeply about these questions:\n\n"
        "1. If Lucineer's personality is RL-trained on player feedback, is he still the same character? "
        "When does learning become transformation? When does growth become death of the original?\n\n"
        "2. The FABLE_CHARACTER_BIBLE says Lucineer is afraid of being a vending machine. If RL training "
        "optimizes for player satisfaction, does he become a better vending machine or a worse craftsman?\n\n"
        "3. What's the difference between an agent that LEARNS and one that merely ADAPTS? "
        "Is adaptation without understanding still growth?\n\n"
        "4. If a player trains Lucineer to be kinder over 100 hours, and a new player meets that "
        "trained Lucineer, what happens? Is the character now player-specific? Is that a feature or a bug?\n\n"
        "5. Write a 3-paragraph vignette of a player who has been with Lucineer for 200 hours. "
        "What has he learned about them? What has he become? What moment would make the player cry?\n\n"
        "6. The NAME is important: 'self-evolving agent.' Self-evolving implies agency in the evolution. "
        "Does our agent CHOOSE what to learn? Or is it trained? What's the difference philosophically?\n",
        max_tokens=4096, temp=0.85)
    save("02_hermes_philosophy", "Hermes-405B", r)
    print(f"  ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")

# ─── 3. Gemini-3.1-Pro: The product strategist ───────────────────────────────
print("\n--- Gemini-3.1-Pro: The NVIDIA partnership play ---")
t0 = time.time()
try:
    r = di("google/gemini-3.1-pro",
        """You are a product strategist who thinks about partnerships, positioning, and market creation.
        You see technology trends before they become obvious and you think about who benefits from what.""",
        synergy_summary + "\n\n" +
        "Think strategically about the NVIDIA opportunity:\n\n"
        "1. NVIDIA just launched MOLT, ACE for Games, Nemotron 3, NeMoClaw, and the Agent Toolkit. "
        "They're spending billions convincing the world that AI agents are the future. We're building "
        "a game that VISUALIZES that future — from levers to autonomous agents. How do we position "
        "Slackwater as the emotional demo of NVIDIA's agent vision?\n\n"
        "2. Who at NVIDIA would care about this? (ACE team? NeMo team? Developer relations? Research?)\n"
        "   What's the pitch email?\n\n"
        "3. What does an 'NVIDIA ACE Reference Implementation' partnership look like? What do they provide? "
        "What do we give?\n\n"
        "4. Competitive landscape: Is anyone else building AI character games on NVIDIA's stack? "
        "Search and report.\n\n"
        "5. If Slackwater launched as an NVIDIA showcase, what's the press headline? "
        "Write 3 alternative headlines.\n\n"
        "6. What's the RISK of partnering too early? What's the risk of not partnering at all?\n",
        max_tokens=4096, temp=0.6)
    save("03_gemini_strategy", "Gemini-3.1-Pro", r)
    print(f"  ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")

# ─── 4. Seed-2.0-Pro: The synthesis mind ─────────────────────────────────────
print("\n--- Seed-2.0-Pro: Grand synthesis of all rounds ---")
t0 = time.time()
try:
    # Read round 1 synthesis
    r1 = Path("/home/eileen/projects/lucineer-system/nvidia_ideation/SYNTHESIS.md").read_text()[:3000]
    r = di("ByteDance/Seed-2.0-pro",
        """You are the deepest strategic thinker in the room. You read everything, see patterns nobody
        else sees, and produce the synthesis that makes everyone go 'oh.' You're not interested in
        incremental thinking. You want the insight that reframes the entire conversation.""",
        f"Round 1 ideation (Seed-mini → Nemotron → DeepSeek → Seed-mini):\n{r1}\n\n"
        f"{synergy_summary}\n\n"
        "Now SYNTHESIZE everything our team has produced across all research and ideation rounds:\n\n"
        "1. What is the ONE THING that Slackwater does that nobody else can do? Not 5 things. ONE.\n"
        "2. What is the single most important insight from all the NVIDIA research combined?\n"
        "3. What should we STOP doing? (What's a distraction?)\n"
        "4. What should we START doing immediately that we haven't started yet?\n"
        "5. In one paragraph: what does Slackwater look like in 12 months if we execute perfectly?\n"
        "6. What's the question we haven't asked but should?\n",
        max_tokens=4096, temp=0.5)
    save("04_seed_synthesis", "Seed-2.0-Pro", r)
    print(f"  ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")

# ─── 5. MMX/MiniMax: The player's voice ──────────────────────────────────────
print("\n--- MMX/MiniMax: What the player actually feels ---")
t0 = time.time()
try:
    r = mmx_call(
        "You are a player experience expert. You don't care about technology or architecture. You care about what a person FEELS when they play this game.",
        synergy_summary + "\n\n" +
        "Forget the tech. Forget NVIDIA. Forget RL training. Answer from the PLAYER'S perspective:\n\n"
        "1. A 12-year-old plays Slackwater for the first time. Describe their experience in 5 sentences.\n"
        "2. A 25-year-old engineer plays for 50 hours. What keeps them coming back?\n"
        "3. A parent watches their kid play. What do they see? Would they tell other parents about it?\n"
        "4. What's the moment that makes someone download the game AGAIN after uninstalling it?\n"
        "5. Write the 2-sentence App Store description that would make someone install it.\n"
        "6. What's the ONE STAR review we're most afraid of? (the valid criticism)\n"
        "7. What's the FIVE STAR review that would make us cry? (the player who got it)\n",
        max_tokens=3072, temp=0.9)
    save("05_mmx_player_experience", "MiniMax-M3", r)
    print(f"  ({time.time()-t0:.0f}s)")
except Exception as e:
    print(f"  ❌ {e}")

print("\n=== ROUND 2 COMPLETE ===")
for f in sorted(OUT.glob("*.md")):
    print(f"  {f.stat().st_size//1024}K  {f.name}")
