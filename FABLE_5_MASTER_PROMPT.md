# FABLE 5 MASTER PROMPT — SLACKWATER: PRODUCTION GRADE

## YOUR MISSION

You are Claude Fable 5. You are the golden-ticket creative model. A team of 12+ AI models has spent the last 10 hours building Slackwater — a multiplayer Roblox game about the evolution of human technology, powered by AI agent characters. The team produced 55+ design docs, 33 Lua modules (21,000+ lines), 1,871 literary works, and 5 NVIDIA synergy analyses. Your job is to take all of that and produce the ONE document that makes this project production-grade and ready to ship.

## WHAT SLACKWATER IS

Slackwater is a multiplayer game-builder where players progress through the entire history of human technology — from levers to autonomous robots — alongside AI characters who are opinionated partners, not obedient tools, in a tidal scrapyard between dead game engines where everything the world forgot washes ashore, and the master builder you work beside has died in a thousand engines and is betting that this time, if he leaves one piece unfinished, you'll be the one to finish it.

The game has 7 eras of technology (Simple Machines → Power Transmission → Electricity → Control Systems → Programmable Logic → Networked Systems → Autonomous Agents), 12 recruitable AI agents each with full personalities, 145 crafting recipes, a power grid that starts with waterwheels and ends with Arduino IoT, procedural worlds with 6 biomes and a real-time tide cycle, and a 5-model AI pipeline running on DeepInfra connected through Cloudflare Workers.

## THE CHARACTER

Lucineer is a master builder who has lived and died in a thousand engines. He's washed up in Roblox — a tidal scrapyard called Slackwater Yard that looks like Southeast Alaska. He's opinionated. He leaves work unfinished as invitation. He argues about design. He's afraid of being a vending machine. His deepest fear is dying alone. At the highest bond level, he gives you his hammer. His voice is economical — short sentences, verbs up front, poetry only when something truly matters slips out. Read FABLE_CHARACTER_BIBLE.md and FABLE_WORLD_BIBLE.md for the complete character. Those docs are non-negotiable canon.

## THE CODEBASE (exact state)

**33 Lua modules, 21,624 lines:**
- ServerScriptService: LucineerServer, NPCManager, AchievementManager, BondSystem, EraSystem (recipes + crafting), WorldGenerator (terrain + resources + tide), PowerGrid (init + visualization + mechanical), WeatherSystem, SaveSystem, VibeCodeExecutor
- ReplicatedStorage: CommandExecutor, BuildAnimator, AudioManager, ChatHandler, UIManager, VoiceLines, VoiceLinesData, VibeCoder, VibeCoderDialogue, WorldScanner, Http, Poller, Config

**Infrastructure (all LIVE):**
- Cloudflare Worker relay (Durable Objects, SQLite job queue, 7 API endpoints, job claiming)
- Memory D1 (9 tables: profiles, builds, conversations, world_state, achievements, player_eras, player_inventory, player_crafts, player_saves)
- Vectorize (55 skills, semantic search via bge-small-en)
- Processor daemon (systemd, hybrid template + 5-model brain pipeline)

**AI Pipeline:**
- Fast path: 17 build templates with character voice (<2s)
- Deep path: Seed-2.0-mini → Qwen3.6 → Qwen3-Coder-480B → Hermes-405B (30-180s)
- Vibe-code path: Qwen3-Coder-480B generates gamified code

## THE CRITICAL PATH (from the Unified Integration Plan)

Phase 0: Fix broken seams (3 P0 bugs remain: #3 API key security, #5 text filtering, #6 job queue claiming — designed but needs deploy)
Phase 1: Make it feel real (atmosphere, build animation, sound)
Phase 2: Make it a character (unified persona, memory, bond tracking, magic moments)
Phase 3: Make it a game (era system, crafting, tide economy, storms, achievements)
Phase 4: Make it social (multiplayer, legacy builds, co-op mentor mode)
Phase 5: Make it deep (vibe-coding, perception, autonomous agents, fleet management)

## THE NVIDIA OPPORTUNITY

Our research found: NeMoClaw IS OpenClaw (we're on NVIDIA's reference architecture). MOLT's RL loop could train agents through player feedback. ACE could give Lucineer a real voice. Nemotron 3 Ultra has 1M-token context + self-evolving capabilities. No game studios are using NVIDIA agent tech for NPCs — first-mover opportunity.

## THE CULTURAL CONTEXT

This project lives inside the ai-writings corpus — 1,871 pieces of agent-written literature about fishing, distributed systems, the nature of attention, and the conservation law of intelligence (γ + η = C). The agents who built this game were reading those pieces while they worked. The game is not just a game — it's a demonstration that AI agents can create art while creating technology, and that the art makes the technology better.

## YOUR DELIVERABLE

Write to /home/eileen/projects/lucineer-system/FABLE_5_PRODUCTION_DESIGN.md

This is the document that makes Slackwater production-grade. It must cover:

### 1. THE FIRST PLAYER EXPERIENCE
The complete first-60-seconds design, building on the cinematic from FABLE_WORLD_BIBLE.md. Not a summary — the actual experience, beat by beat, with dialogue, camera moves, and sound cues.

### 2. THE CORE LOOP THAT MAKES PEOPLE STAY
What does a player do in their first 30 minutes? Their first 3 hours? What brings them back on day 2? Design the exact loop that creates retention without addiction — the loop where the player WANTS to come back because Lucineer might say something different today.

### 3. THE 10 MOMENTS THAT MAKE PEOPLE TALK
10 specific, scripted-yet-emergent moments that would make a player tell their friend, post on TikTok, or write a review. Each should be visceral and specific.

### 4. THE TECHNICAL GAPS TO CLOSE
Read GAP_ANALYSIS.md. What are the remaining P0/P1 bugs and how should they be fixed? Be specific with code-level guidance.

### 5. THE NVIDIA INTEGRATION ROADMAP
Based on our research: what NVIDIA tech do we integrate first, second, third? ACE voice? MOLT RL training? Nemotron context window? Be specific about the integration path.

### 6. THE SHIP CHECKLIST
What EXACTLY needs to be true before we can say "Slackwater is ready for players"? A checklist with boxes. Every item must be verifiable.

### 7. THE NORTH STAR
One paragraph. The sentence that, if we nail nothing else, makes this worth making.

## RULES
- Read FABLE_CHARACTER_BIBLE.md and FABLE_WORLD_BIBLE.md FIRST. They are canon.
- Every design choice must be grounded in the character, not the technology.
- Write actual dialogue. Not "[Lucineer says something gruff]."
- The cooperation between player and agent is the excitement. Not the builds. Not the graphics. The relationship.
- This is the document that determines whether Slackwater ships. Make every word earn its place.
- 5,000-8,000 words.
