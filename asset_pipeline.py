#!/usr/bin/env python3
"""
MMX + DeepInfra Asset Generation Pipeline
=========================================
Generates concrete creative assets for Lucineer:
1. Sound design spec (via DeepSeek analysis + MMX synthesis)
2. 20 more Vectorize skills (via DeepInfra batch generation)
3. Lucineer voice lines for common interactions (via Hermes)
"""
import json, os, sys, subprocess, time, urllib.request
from pathlib import Path

from loadkey import get_key
DEEPINFRA_KEY = get_key()
MMX = os.path.expanduser("~/.npm-global/bin/mmx")
OUT = Path("/home/eileen/projects/lucineer-system/assets")
OUT.mkdir(exist_ok=True)

def di(model, system, user, max_tokens=4096, temp=0.7):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    payload = json.dumps({"model": model, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ], "max_tokens": max_tokens, "temperature": temp}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {DEEPINFRA_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def mmx(system, user, max_tokens=4096, temp=0.8):
    r = subprocess.run([MMX, "text", "chat", "--system", system,
        "--message", user, "--max-tokens", str(max_tokens),
        "--temperature", str(temp), "--output", "text"],
        capture_output=True, text=True, timeout=120)
    return r.stdout.strip()

# ─── 1. HERMES: 50 Lucineer Voice Lines ──────────────────────────────────────
print("=== Hermes-405B: Voice Lines ===")
t0 = time.time()
voice_lines = di("NousResearch/Hermes-3-Llama-3.1-405B",
    """You are Lucineer — a master builder who's lived in a thousand engines. 
Now in Roblox. Opinionated, gruff, occasionally poetic. SE Alaska scrap aesthetic.
Read /home/eileen/projects/lucineer-system/FABLE_CHARACTER_BIBLE.md for your full personality.
You speak in short economical bursts. You leave work unfinished as invitation.
You argue with players about design. You reference Magnus, the tide, the Channel.""",
    """Write 50 voice lines for common game interactions, organized by category:

1. GREETING (when player joins) — 5 lines
2. FIRST BUILD (player's first ever request) — 5 lines
3. TEMPLATES (one line per template: tower, house, castle, tree, bridge, wall, road, lamp, pyramid, dome, arch, platform, staircase, garden, dock, lighthouse) — 17 lines
4. ARGUMENTS (when player makes bad design choices) — 5 lines
5. IMPRESSED (rare, when player does something unexpected) — 5 lines
6. REFUSAL (when player asks for something Lucineer won't do) — 5 lines
7. FAREWELL (when player leaves) — 5 lines
8. IDLE (random lines when nothing's happening) — 3 lines

Format as a JSON array: [{"category": "...", "trigger": "...", "line": "..."}]
Each line 1-2 sentences MAX. In Lucineer's voice. No generic AI talk.""",
    max_tokens=4096, temp=0.85)
(OUT / "voice_lines.json").write_text(voice_lines)
print(f"  ✓ {time.time()-t0:.1f}s — {len(voice_lines)} chars — saved voice_lines.json")

# ─── 2. SEED-2.0-MINI: 20 More Skills ────────────────────────────────────────
print("\n=== Seed-2.0-mini: Batch 4 Skills ===")
t0 = time.time()
skills_raw = di("ByteDance/Seed-2.0-mini",
    """You are a Roblox build skill generator. Output ONLY a JSON array of build skills.
Each skill: {name, description, metadata:{category,style,difficulty}, luau_source}
The luau_source is a complete Lua function that builds the structure.""",
    """Generate 20 new Roblox build skills for Lucineer's skill library. 
Existing skills cover: tower, house, castle, tree, bridge, wall, road, lamp, pyramid, dome, arch, platform, staircase, garden, dock, lighthouse, spiral stairs, columns, fountain, statue, chandelier, fire pit, banner, throne, market stall, watchtower, mine entrance, windmill, cargo crates, pipe network, gear mechanism, conveyor belt, water wheel, rope bridge, crystal cluster, cave entrance, mushroom grove, campfire camp, chasm bridge, greenhouse, telescope observatory, scrap tower, workbench, robot follower, race track, forge, foundation, wall section, resource node, light beacon, planter.

NEW skills needed (don't duplicate existing):
1. suspension bridge (cables, towers, deck)
2. clock tower (with working clock face)
3. catapult (medieval siege weapon)
4. treasure chest (openable, with glow)
5. fishing hut (on stilts over water)
6. waterfall (with particle effects)
7. treehouse (in a large tree)
8. castle gatehouse (portcullis mechanism)
9. observatory telescope (brass, steampunk)
10. lantern row (path lighting)
11. scarecrow (farm decoration)
12. well (stone, with bucket)
13. barricade (defensive structure)
14. signal tower (with flags)
15. altar (stone, with glowing runes)
16. igloo (ice blocks)
17. sandcastle (beach decoration)
18. totem pole (carved wooden)
19. wagon (covered, parked)
20. catapult target (straw dummy)

Output ONLY the JSON array. No markdown.""",
    max_tokens=8192, temp=0.5)

# Parse and save
try:
    skills = json.loads(skills_raw)
    (OUT / "skills_batch4.json").write_text(json.dumps(skills, indent=2))
    print(f"  ✓ {time.time()-t0:.1f}s — {len(skills)} skills — saved skills_batch4.json")
    
    # Seed them
    print("  Seeding to Vectorize...")
    seed_result = subprocess.run(['curl', '-s', '-X', 'POST',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(skills),
        'https://lucineer-vector.casey-digennaro.workers.dev/api/skills/seed'],
        capture_output=True, text=True, timeout=120)
    resp = json.loads(seed_result.stdout)
    print(f"  ✅ {resp.get('count', '?')} skills seeded")
except Exception as e:
    print(f"  ❌ Parse/seed error: {e}")
    (OUT / "skills_batch4_raw.txt").write_text(skills_raw)

# ─── 3. DEEPSEEK: Sound Design Spec ──────────────────────────────────────────
print("\n=== DeepSeek-V3: Sound Design ===")
t0 = time.time()
sound_spec = di("deepseek-ai/DeepSeek-V3",
    """You are a game audio designer. Design the complete sound palette for Lucineer,
an AI building companion in Roblox set in Slackwater Yard (tidal scrapyard, SE Alaska).""",
    """Read /home/eileen/projects/lucineer-system/FABLE_WORLD_BIBLE.md for the world context.

Design a complete SOUND DESIGN SPECIFICATION:

1. AMBIENT BED — What plays constantly in Slackwater Yard:
   - Water/tide sounds (what specifically?)
   - Weather (fog, rain, wind)
   - Wildlife (gulls, ravens, what else?)
   - Industrial (forge, cannery creaking, float)
   - Specify exact Roblox SoundIds or sound type descriptions

2. BUILD SFX — What each build action sounds like:
   - Part placement (different materials = different sounds)
   - Light creation (click + hum)
   - Terrain modification
   - Build completion (satisfying "snap" or "settle")
   - Specify pitch, duration, character for each

3. LUCINEER VOCAL CUES — Short sound motifs (not full voice):
   - Acknowledgment (heard request)
   - Thinking (working on it)
   - Completion (done)
   - Disagreement (refusal)
   - Surprise (impressed)
   - Specify instrument/tone character

4. UI SOUNDS:
   - Chat send
   - Chat receive
   - Error
   - Achievement unlock
   - Level up

5. MUSIC:
   - Hub ambient music (what key, what instruments, what mood?)
   - Build music (does it change during building?)
   - Storm event music
   - Aurora event music
   - Specify BPM ranges and key

Format as a structured spec with exact SoundId suggestions where possible.""",
    max_tokens=4096, temp=0.6)
(OUT / "sound_design_spec.md").write_text(sound_spec)
print(f"  ✓ {time.time()-t0:.1f}s — {len(sound_spec)} chars — saved sound_design_spec.md")

# ─── 4. MMX: Concept Art Prompts ─────────────────────────────────────────────
print("\n=== MMX/MiniMax: Concept Art Prompts ===")
t0 = time.time()
art_prompts = mmx(
    "You are a concept art director for a Roblox game with a scrap/industrial SE Alaska aesthetic.",
    """Generate 10 detailed concept art prompts for Lucineer's world (Slackwater Yard).
Each prompt should be specific enough to feed into an AI image generator.

Cover these scenes:
1. The cannery/forge at dusk (exterior, glowing windows)
2. The float/dock with the Capitaine tied up
3. The lighthouse beam sweeping through fog
4. Lucineer at his anvil, forge-lit
5. The tideline after a big ebb (salvage scattered on beach)
6. A player and Lucineer carrying a beam together
7. Earl at his manifest desk inside the cannery
8. The aurora over Slackwater Yard at night
9. A completed castle build on the island ridge
10. The storm — big Southeast blow, yard in chaos

Each prompt: 2-3 sentences with lighting, mood, color palette, camera angle.
Format as a numbered list.""",
    max_tokens=2048, temp=0.9)
(OUT / "concept_art_prompts.md").write_text(art_prompts)
print(f"  ✓ {time.time()-t0:.1f}s — {len(art_prompts)} chars — saved concept_art_prompts.md")

# ─── 5. QWEN3-CODER: Upgraded Lua CommandExecutor ────────────────────────────
print("\n=== Qwen3-Coder-480B: Build Animation Lua ===")
t0 = time.time()
anim_lua = di("Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo",
    "You are a senior Roblox Lua developer. Write production-quality Luau code.",
    """Write a Roblox Lua module that adds BUILD ANIMATION to Lucineer's CommandExecutor.
Instead of parts appearing instantly, they should animate in.

Module: /home/eileen/projects/lucineer-roblox/src/ReplicatedStorage/Lucineer/BuildAnimator.lua

Requirements:
1. Parts fade in (Transparency 1 → target) over 0.3s
2. Parts scale up from 0.1 to full size with a bounce easing
3. A particle burst at the part's position when it lands
4. A sound plays on placement (different pitch per material)
5. Camera gently focuses on the build area
6. Multiple parts in a batch stream in sequence (staggered by 0.08s)
7. A "completion burst" when all parts in a batch are done

API:
  BuildAnimator.animatePart(part, targetTransparency) -- fades/scales in
  BuildAnimator.animateBatch(parts, centerPosition) -- streams batch with completion burst
  BuildAnimator.burst(position, color) -- particle burst

Use TweenService, ParticleEmitter, SoundService.
Write the COMPLETE module. Production quality. No pseudocode.""",
    max_tokens=4096, temp=0.2)
(OUT / "BuildAnimator.lua").write_text(anim_lua)
print(f"  ✓ {time.time()-t0:.1f}s — {len(anim_lua)} chars — saved BuildAnimator.lua")

print("\n=== ASSET PIPELINE COMPLETE ===")
print(f"Files in {OUT}/:")
for f in sorted(OUT.iterdir()):
    print(f"  {f.stat().st_size//1024}K  {f.name}")
