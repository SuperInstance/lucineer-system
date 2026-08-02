#!/usr/bin/env python3
"""
Multi-Model Ideation Session — Seed-mini as expansive catalyst
Round 1: Seed-mini expands the vision (wild, unconstrained)
Round 2: Nemotron grounds it (what's technically possible)
Round 3: DeepSeek finds the research gaps (what needs to be proven)
Round 4: Seed-mini re-expands with the constraints (creative within the possible)
"""
import json, os, sys, subprocess, time, urllib.request
from pathlib import Path

KEY = open("/home/eileen/mcp-deeinfra/.env").read().split("DEEPINFRA_API_KEY=")[1].split("\n")[0].strip().strip('"').strip("'")
OUT = Path("/home/eileen/projects/lucineer-system/nvidia_ideation")
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

BRIEF = """
CONTEXT: We're building Slackwater — a multiplayer Roblox game about the evolution of technology
(simple machines → Arduino IoT → autonomous agents), powered by AI agent characters.

NVIDIA just released MOLT (https://github.com/NVIDIA-NeMo/labs-molt) — an agentic-first RL framework where:
- "The agent is the program; the trainer is a single actor"
- "Reward is any Python you write inside an Env or ChatAgent"
- Fully-async runtime with Ray + vLLM
- Supports multimodal VLM environments, multi-turn tool calls
- 9.2K LOC of RL code that scales to 1T-class MoE

We already use Nemotron-Ultra-550B on DeepInfra for deep reasoning in our 5-model pipeline.
NVIDIA also has: ACE for Games (speech/animation AI), NeMoClaw runtime, Agent Toolkit.

Our game has 7 eras of technology, 12 recruitable AI agents, 145 crafting recipes,
a power grid, weather system, procedural worlds, and a vibe-coding system.
33 Lua modules, 19,000+ lines. All on GitHub at SuperInstance.
"""

# ─── Round 1: Seed-mini expands ─────────────────────────────────────────────
print("=== Round 1: Seed-2.0-mini (expansive catalyst) ===")
t0 = time.time()
try:
    r1 = di("ByteDance/Seed-2.0-mini",
        """You are the most expansive, innovative, wild-thinking creative mind in a team of AI researchers.
        Your job is NOT to be practical. Your job is to FIND THE EDGES — the ideas that make
        everyone else go "wait, that's actually possible?" Think 10x, not 10%.
        Be bold. Be weird. Be specific. Every idea should make someone uncomfortable with how
        much sense it makes.""",
        BRIEF + """

The team is about to discuss how NVIDIA's MOLT and other releases could transform our work.
Your job: generate 10 WILD ideas for how MOLT's RL training + Nemotron's self-evolving agents +
ACE's voice/animation could transform Slackwater. Not incremental improvements. MOONSHOTS.

Think about:
- What if game agents could LEARN from player behavior in real-time using MOLT's RL loop?
- What if Lucineer could actually SPEAK with NVIDIA ACE, customized to a SE Alaska fisherman's voice?
- What if the game's NPC agents used MOLT's "reward is any Python you write" to develop their OWN personalities through play?
- What if the autonomous agents (Era 7) were trained with MOLT to coordinate like Steve/Voyager?
- What if players could TRAIN their own agents using MOLT's paradigm?

Go wild. 10 ideas. Each 3-4 sentences. Make them SPECIFIC enough to build.""",
        max_tokens=4096, temp=1.0)
    (OUT / "01_seed_expansive.md").write_text(r1)
    print(f"  ✅ ({time.time()-t0:.0f}s) — {len(r1)} chars")
except Exception as e:
    print(f"  ❌ {e}")
    r1 = ""

# ─── Round 2: Nemotron grounds it ────────────────────────────────────────────
print("\n=== Round 2: Nemotron-Ultra-550B (grounding) ===")
t0 = time.time()
try:
    r2 = di("nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B",
        """You are a pragmatic systems architect. Your job is to take wild ideas and figure out
        which ones are actually buildable, how, and in what order. You love the wild ideas but
        you translate them into roadmaps. Be specific about architecture, data flow, and
        what infrastructure is needed.""",
        BRIEF + f"\n\nHere are 10 wild ideas from the expansive thinker:\n\n{r1}\n\n" +
        "Now GROUND them:\n"
        "1. Which 3 ideas are the most immediately buildable (next 30 days)?\n"
        "2. For each: what's the architecture? What NVIDIA tools specifically? What's the data flow?\n"
        "3. Which 2 ideas are 6-month projects?\n"
        "4. Which ideas are genuinely impossible or impractical? Say so honestly.\n"
        "5. What's the ONE idea that could define Slackwater as a category-killer?\n"
        "Be specific. Reference actual NVIDIA APIs, actual MOLT code patterns, actual model capabilities.",
        max_tokens=4096, temp=0.4)
    (OUT / "02_nemotron_grounding.md").write_text(r2)
    print(f"  ✅ ({time.time()-t0:.0f}s) — {len(r2)} chars")
except Exception as e:
    print(f"  ❌ {e}")
    r2 = ""

# ─── Round 3: DeepSeek finds research gaps ───────────────────────────────────
print("\n=== Round 3: DeepSeek-V3 (research gaps) ===")
t0 = time.time()
try:
    r3 = di("deepseek-ai/DeepSeek-V3",
        """You are an AI researcher who reads everything and finds what's missing.
        Your job is to identify the RESEARCH QUESTIONS that need to be answered before
        we can build the ideas above. What experiments do we need to run? What papers
        do we need to read? What baselines do we need to establish?""",
        BRIEF + f"\n\nWild ideas:\n{r1[:3000]}\n\nGrounding:\n{r2[:3000]}\n\n" +
        "Now find the GAPS:\n"
        "1. What 5 research questions must we answer before building any of this?\n"
        "2. For each question: what experiment would answer it? What data do we need?\n"
        "3. What existing papers (cite them) are most relevant?\n"
        "4. What's the simplest PROOF OF CONCEPT we could build in a weekend?\n"
        "5. What are the ethical/safety concerns with RL-trained game agents?\n",
        max_tokens=4096, temp=0.5)
    (OUT / "03_deepseek_research.md").write_text(r3)
    print(f"  ✅ ({time.time()-t0:.0f}s) — {len(r3)} chars")
except Exception as e:
    print(f"  ❌ {e}")
    r3 = ""

# ─── Round 4: Seed-mini re-expands with constraints ──────────────────────────
print("\n=== Round 4: Seed-2.0-mini (creative within constraints) ===")
t0 = time.time()
try:
    r4 = di("ByteDance/Seed-2.0-mini",
        """You are the expansive thinker again. You've now seen the grounding (what's buildable)
        and the research gaps (what needs to be proven). Your job: take the MOST PROMISING
        constrained idea and make it SING. Find the emotional core, the player experience,
        the thing that would make someone tell their friend about this game.""",
        BRIEF + f"\n\n" +
        f"Grounded top ideas:\n{r2[:3000]}\n\n" +
        f"Research questions:\n{r3[:2000]}\n\n" +
        "Now make it SING:\n"
        "1. Describe the PLAYER EXPERIENCE of the #1 most promising idea in vivid detail\n"
        "2. What's the TikTok moment? The thing someone clips and shares?\n"
        "3. What's the emotional beat? When does the player feel something real?\n"
        "4. Write the one-liner that would be on the Roblox game page\n"
        "5. What's the 3-month roadmap to get there? (be specific, building on what exists)\n",
        max_tokens=4096, temp=0.9)
    (OUT / "04_seed_vision.md").write_text(r4)
    print(f"  ✅ ({time.time()-t0:.0f}s) — {len(r4)} chars")
except Exception as e:
    print(f"  ❌ {e}")
    r4 = ""

# ─── Synthesis ───────────────────────────────────────────────────────────────
print("\n=== Synthesis ===")
synthesis = f"""# Multi-Model Ideation: NVIDIA Synergies

## Round 1 — Seed-2.0-mini (Expansive Catalyst)
{r1}

---

## Round 2 — Nemotron-Ultra-550B (Grounding)
{r2}

---

## Round 3 — DeepSeek-V3 (Research Gaps)
{r3}

---

## Round 4 — Seed-2.0-mini (Vision)
{r4}

---

*Generated {time.strftime('%Y-%m-%d %H:%M')} — Seed-mini → Nemotron → DeepSeek → Seed-mini*
"""
(OUT / "SYNTHESIS.md").write_text(synthesis)
print(f"✅ Synthesis saved ({len(synthesis)} chars)")
print(f"\nFiles in {OUT}/:")
for f in sorted(OUT.iterdir()):
    print(f"  {f.stat().st_size//1024}K  {f.name}")
