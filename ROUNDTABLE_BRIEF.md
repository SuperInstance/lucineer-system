# LUCINEER — WORLD-CLASS ROUNDTABLE BRIEF
# ============================================
# You are part of an elite team making Lucineer a head-turning, world-class release.
# Read the full system state below, then deliver your section.
# Be bold. Be specific. No hand-waving. Code where relevant.
# ============================================

## WHAT IS LUCINEER?

Lucineer is an AI building companion inside Roblox. A player walks into a world and talks naturally — "build me a castle on the hill" — and Lucineer builds it in real-time. Not a chat menu. Not a cheat tool. A character — a craftsman with opinions, a backstory, and a scrap/industrial aesthetic influenced by Southeast Alaska fishing culture.

The player experiences Lucineer as a GENIE companion — someone who's been building things for a thousand years across different engines, and now happens to be in this one.

## SYSTEM ARCHITECTURE (CURRENT STATE)

```
Roblox Player Chat
       ↓
  Lua Client (9 modules: ChatHandler, Http, Poller, CommandExecutor, WorldScanner, UIManager, Config, Server, Client)
       ↓
  Cloudflare Worker (lucineer-relay) — Durable Objects, SQLite job queue, 6 API endpoints
       ↓
  Python Processor v2 (hybrid: template match → brain.py deep pipeline)
       ↓
  DeepInfra 5-Model Pipeline:
    1. Seed-2.0-mini    → intent parsing (fast, cheap)
    2. Qwen3.6-35B-A3B  → spatial planning (or Seed-2.0-pro for --deep)
    3. Qwen3-Coder-480B → Luau command generation
    4. Hermes-405B      → personality/lore wrapping (--creative)
    5. (Nemotron-Content-Safety-3.5 for kid-safe verification)
       ↓
  JSON Build Commands → Worker → Roblox Lua CommandExecutor → Parts appear in world
```

### Infrastructure (all LIVE):
- **Worker relay**: Durable Objects, SQLite job queue, 6 API endpoints — deployed and healthy
- **Memory D1**: 5 tables (player_profiles, build_history, skills, conversations, world_state), 12 API endpoints
- **Vectorize**: 35 Luau skills indexed, semantic search verified (bge-small-en via Workers AI)
- **R2 buckets**: lucineer-templates, lucineer-assets, lucineer-user-data
- **17 build templates**: tower, house, castle, tree, bridge, wall, road, lamp, pyramid, dome, arch, platform, staircase, garden, dock, lighthouse + default
- **Character voice**: All templates rewritten as Lucineer — leaves work unfinished, references past builds, SE Alaska flavor, opinionated craftsman
- **rbxlx place file**: 10 Lua scripts, syntax-verified with lua5.1

### Design DNA (from Magnus's prior games):
- Industrial/scrap aesthetic — yards, forges, smelters, rust, gears
- AI companions as CHARACTERS (Earl the foreman, Spark the helper, Hermes the captain)
- Deep crafting systems (56 recipes, 3 tiers)
- Achievement-driven progression (49 achievements)
- Education hidden inside fun
- Southeast Alaska fishing industry influence (vessels, tenders, crab)
- Robot companions you build AND program

### Prior Incarnations:
- JetsonClaw1 (JC1) — Lucineer fleet agent on Jetson Orin Nano
- PLATO MUD — text-first agent environment where room = IDE
- Flux ecosystem — trust, perception, stigmergy in Rust/Go/C
- Pythagorean48 — exact 6-bit vector encoding for embeddings
- Forgemaster — constraint theory migration agent
- Capitaine — fork a repo, the agent is alive

## WHAT'S GREAT vs WHAT'S NOT READY

### Great:
- The character concept — Lucineer as opinionated craftsman, not servant
- 5-model pipeline with creative personality wrapping
- 35-skill semantic library
- Full Cloudflare infrastructure (Worker + D1 + Vectorize + R2)
- Character voice injected across all touchpoints

### Not Ready (THE GAP TO WORLD-CLASS):
1. **No live Studio playtest** — everything tested via curl, never driven from Roblox
2. **No visual polish** — parts are basic shapes (Block, Ball, Cylinder). No meshes, textures, or custom assets
3. **No progression system** — no achievements, no unlock gates, no skill tree
4. **No sound design** — no ambient audio, no build SFX, no Lucineer voice
5. **No tutorial/onboarding** — first-time player has no guidance
6. **Processor not running as daemon** — dies when terminal closes
7. **No multiplayer awareness** — doesn't handle multiple players building simultaneously
8. **No social/viral mechanics** — no sharing, no leaderboards, no community
9. **Build quality is generic** — templates are functional but not "head-turning"
10. **No brand identity** — no logo, no splash screen, no consistent visual language

## AVAILABLE MODELS ON DEEPINFRA
- nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B (deepest reasoning)
- google/gemini-3.1-pro (frontier multimodal)
- Qwen/Qwen3.5-397B-A17B (massive Qwen)
- Qwen/Qwen3.7-Max (newest Qwen flagship)
- Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo (code generation)
- ByteDance/Seed-2.0-pro (deep planning)
- NousResearch/Hermes-3-Llama-3.1-405B (creative/personality)
- stabilityai/sdxl-turbo, black-forest-labs/FLUX-2-max (images)
- Qwen/Qwen3-TTS-VoiceDesign (voice)
