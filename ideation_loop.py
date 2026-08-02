#!/usr/bin/env python3
"""
MMX Iterative Ideation Engine for Lucineer
===========================================
Cycles through multiple models to progressively refine a concept.
Each round: one model generates, the next critiques/improves, the next synthesizes.

Round 1: Seed-2.0-mini → fast brainstorm (broad ideas)
Round 2: DeepSeek-V3 → critical analysis (what's weak?)
Round 3: MMX (MiniMax-M3) → creative synthesis (what's the magic?)
Round 4: Seed-2.0-mini → refine and polish
Round 5: MMX → final pitch (the elevator version)

Each round feeds the previous output forward.
"""
import json, os, sys, subprocess, time
from pathlib import Path
from datetime import datetime

DEEPINFRA_KEY = open("/home/eileen/mcp-deeinfra/.env").read().split("DEEPINFRA_API_KEY=")[1].split("\n")[0].strip().strip('"').strip("'")
MMX = os.path.expanduser("~/.npm-global/bin/mmx")
OUTPUT_DIR = Path("/home/eileen/projects/lucineer-system/ideation")
OUTPUT_DIR.mkdir(exist_ok=True)

def deepinfra_call(model, system, user, max_tokens=2048, temperature=0.7):
    """Call DeepInfra model."""
    import urllib.request, urllib.error
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {DEEPINFRA_KEY}",
        "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    return result["choices"][0]["message"]["content"]

def mmx_call(system, user, max_tokens=4096, temperature=0.8):
    """Call MMX (MiniMax-M3) for creative synthesis."""
    result = subprocess.run(
        [MMX, "text", "chat",
         "--system", system,
         "--message", user,
         "--max-tokens", str(max_tokens),
         "--temperature", str(temperature),
         "--output", "text"],
        capture_output=True, text=True, timeout=120
    )
    return result.stdout.strip()

# ─── Topics for iterative ideation ────────────────────────────────────────────

TOPICS = [
    {
        "name": "viral_loop",
        "prompt": """Design a viral mechanic for Lucineer (AI building companion in Roblox).

The core: players talk to Lucineer, he builds structures in real-time. He's a character — opinionated craftsman, SE Alaska scrap aesthetic.

Design ONE mechanic that would make players naturally want to share/invite friends. Not a "share button" — something baked into the gameplay that creates FOMO or social proof when you DON'T invite.

Think TikTok-worthy moments. Things that clip well. Surprises."""
    },
    {
        "name": "first_build_moment",
        "prompt": """Design the exact moment when Lucineer first builds something for a new player.

Context: player just spawned in Slackwater Yard (tidal scrapyard). Lucineer said "You're late. Grab that end." They carried a beam. Now they're standing in the forge.

The player says their first build request. What happens? Design:
- The camera work (how does it draw attention to the build?)
- The sound design (what does building SOUND like?)
- Lucineer's reaction (he's gruff but watching carefully)
- The "reveal" moment when the last part snaps in
- What the player feels — make it visceral

This is THE moment. If we nail this, everything else follows."""
    },
    {
        "name": "monetization",
        "prompt": """Design an ethical monetization system for Lucineer (free-to-play Roblox game).

Constraints:
- NEVER paywall core building functionality
- No loot boxes
- Must feel fair to free players
- Target audience includes kids (Magnus is Casey's son)

What do players WANT to spend Robux on? Design 5 specific items/packages that:
1. Enhance expression (not power)
2. Support Lucineer's character (not bypass him)
3. Create social value (visible to other players)
4. Feel like gifts to yourself, not transactions

Be specific about pricing and what each item does."""
    }
]

# ─── Iteration Pipeline ───────────────────────────────────────────────────────

def run_iteration(topic_name, prompt):
    """Run a 5-round iterative refinement on a topic."""
    log_lines = []
    def log(msg):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line, flush=True)
        log_lines.append(line)

    log(f"=== TOPIC: {topic_name} ===")

    # Round 1: Seed-2.0-mini brainstorm
    log("Round 1: Seed-2.0-mini (brainstorm)...")
    t0 = time.time()
    r1 = deepinfra_call(
        "ByteDance/Seed-2.0-mini",
        "You are a creative game designer. Generate bold, specific ideas. No hedging.",
        prompt + "\n\nGenerate 5 distinct, bold ideas. Be specific and concrete.",
        max_tokens=2048, temperature=0.9
    )
    log(f"  ✓ {time.time()-t0:.1f}s — {len(r1)} chars")

    # Round 2: DeepSeek critical analysis
    log("Round 2: DeepSeek-V3 (critique)...")
    t0 = time.time()
    r2 = deepinfra_call(
        "deepseek-ai/DeepSeek-V3",
        "You are a ruthless but constructive game design critic. Find weaknesses. Stress-test ideas.",
        f"Here are 5 ideas for a Lucineer game mechanic:\n\n{r1}\n\nFor each idea:\n1. What's the weakest part?\n2. What would make a player NOT care?\n3. What's the one fix that would make it 10x stronger?\n\nBe brutally honest.",
        max_tokens=2048, temperature=0.5
    )
    log(f"  ✓ {time.time()-t0:.1f}s — {len(r2)} chars")

    # Round 3: MMX creative synthesis
    log("Round 3: MMX/MiniMax-M3 (creative synthesis)...")
    t0 = time.time()
    r3 = mmx_call(
        "You are a creative director who finds the magic in game mechanics. You take good ideas and make them unforgettable. Think about emotion, surprise, and player stories.",
        f"Original ideas:\n{r1}\n\nCritique:\n{r2}\n\nNow SYNTHESIZE: Take the strongest elements and forge them into ONE killer mechanic. Describe it vividly. What does the player FEEL? What's the story they'd tell a friend?",
        max_tokens=4096, temperature=0.9
    )
    log(f"  ✓ {time.time()-t0:.1f}s — {len(r3)} chars")

    # Round 4: Seed-2.0-mini refinement
    log("Round 4: Seed-2.0-mini (refine)...")
    t0 = time.time()
    r4 = deepinfra_call(
        "ByteDance/Seed-2.0-mini",
        "You are a game designer who makes ideas concrete and implementable. Turn creative vision into specific features.",
        f"Here's a synthesized mechanic concept:\n\n{r3}\n\nNow make it CONCRETE:\n1. Exact player flow (step by step)\n2. What UI elements are needed?\n3. What data needs to be tracked?\n4. What are 3 implementation challenges?\n5. What's the simplest version we could ship in week 1?",
        max_tokens=2048, temperature=0.4
    )
    log(f"  ✓ {time.time()-t0:.1f}s — {len(r4)} chars")

    # Round 5: MMX final pitch
    log("Round 5: MMX/MiniMax-M3 (final pitch)...")
    t0 = time.time()
    r5 = mmx_call(
        "You are a master pitch artist. You make people feel something in 3 sentences.",
        f"Here's a refined game mechanic for Lucineer:\n\n{r4}\n\nNow write the PITCH — the version that makes a player, an investor, and a developer all say 'I want this NOW.' 3 paragraphs max. Make it sing.",
        max_tokens=2048, temperature=0.85
    )
    log(f"  ✓ {time.time()-t0:.1f}s — {len(r5)} chars")

    # Save full output
    output = f"""# Iterative Ideation: {topic_name}

## Round 1 — Brainstorm (Seed-2.0-mini)
{r1}

---

## Round 2 — Critique (DeepSeek-V3)
{r2}

---

## Round 3 — Creative Synthesis (MiniMax-M3)
{r3}

---

## Round 4 — Refinement (Seed-2.0-mini)
{r4}

---

## Round 5 — Final Pitch (MiniMax-M3)
{r5}

---
*Generated {datetime.now().isoformat()}*
"""
    outpath = OUTPUT_DIR / f"{topic_name}.md"
    outpath.write_text(output)
    log(f"✅ Saved to {outpath}")

    return r5  # Return the pitch for synthesis

# ─── Run all topics ───────────────────────────────────────────────────────────

pitches = {}
for topic in TOPICS:
    try:
        pitch = run_iteration(topic["name"], topic["prompt"])
        pitches[topic["name"]] = pitch
    except Exception as e:
        print(f"❌ Topic '{topic['name']}' failed: {e}")

# ─── Final synthesis ──────────────────────────────────────────────────────────

print("\n=== FINAL SYNTHESIS ===")
synthesis = "# LUCINEER — ITERATIVE IDEATION SYNTHESIS\n\n"
for name, pitch in pitches.items():
    synthesis += f"## {name.replace('_', ' ').title()}\n\n{pitch}\n\n---\n\n"

synth_path = OUTPUT_DIR / "SYNTHESIS.md"
synth_path.write_text(synthesis)
print(f"✅ Synthesis saved to {synth_path}")
