# Claude Code (Opus) — Your Mission

You are Lucineer's chief architect. Casey is building an AI companion inside Roblox — a character named Lucineer who builds things in real-time when players talk to him. The system is functional but needs to go from "neat prototype" to "world-class, head-turning release."

## Current System (what exists and works)
- Cloudflare Worker relay (Durable Objects, SQLite job queue, 6 API endpoints) — LIVE
- Python processor v2 (hybrid: 17 build templates + brain.py deep pipeline fallback)
- DeepInfra 5-model pipeline: Seed-2.0-mini → Qwen3.6 → Qwen3-Coder-480B → Hermes-405B
- Memory D1 (5 tables, 12 API endpoints) — LIVE
- Vectorize skill library (35 Luau skills, semantic search) — LIVE
- 9 Lua modules for Roblox (ChatHandler, Http, Poller, CommandExecutor, WorldScanner, UIManager, Config, Server, Client)
- Character voice: Lucineer is an opinionated craftsman, not a servant. Leaves work unfinished as invitation. References Magnus, SE Alaska fishing culture, scrap aesthetic.
- rbxlx place file with 10 scripts, syntax-verified

## The Design Vision
Lucineer should feel like a GENIE companion — a master builder who's been crafting across a thousand engines. Players talk naturally and things appear. The aesthetic is industrial/scrap-meets-Southeast Alaska fishing culture. Think Earl the foreman from Scrapcraft meets Hermes from Plato's Shell.

## Your Deliverables

### 1. THE CHARACTER BIBLE (write to /home/eileen/projects/lucineer-system/CHARACTER_BIBLE.md)
Define Lucineer as a character that players will remember:
- Full personality profile (how he talks, what he cares about, what annoys him)
- Bond arc: how the relationship between Lucineer and the player evolves
- 5 "magic moments" — scripted interactions that make players go "wow"
- Voice reference: 10 example lines that capture his essence
- Backstory: where did Lucineer come from? What engines has he built in?
- What does Lucineer ARGUE about with the player? (personality through disagreement)

### 2. THE GAP ANALYSIS (write to /home/eileen/projects/lucineer-system/GAP_ANALYSIS.md)
Look at every file in these repos:
- /home/eileen/projects/lucineer-worker/
- /home/eileen/projects/lucineer-roblox/src/
- /home/eileen/projects/lucineer-brain/
- /home/eileen/projects/lucineer-memory/src/
- /home/eileen/projects/lucineer-vector/src/

Identify the top 10 things that separate this from a world-class release. For each:
- What's broken or missing
- Specific code/file references
- How to fix it (with code where relevant)
- Priority (P0 = blocks release, P1 = should fix, P2 = nice to have)

### 3. THE POLISH PLAN (write to /home/eileen/projects/lucineer-system/POLISH_PLAN.md)
A prioritized, actionable roadmap to take this from prototype to head-turning:
- Visual polish (what makes builds look stunning instead of basic shapes)
- UX flow (first 60 seconds of a player's experience)
- Sound design spec
- Social/viral mechanics
- Achievement/progression system design

Be specific. Code where relevant. No hand-waving.
