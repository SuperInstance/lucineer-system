# SLACKWATER — MASTER ARCHITECTURE v2
# The Game-Builder Game About the Evolution of Technology
# ========================================================

## THE NORTH STAR

Slackwater is a multiplayer game-builder where players arrive in a procedurally-generated tidal world and progress through the entire history of human technology — from levers and pulleys to Arduino-powered robots — alongside AI agents who are characters, not tools.

It's Scrapcraft's DNA (build → craft → program → export) meets Roblox's platform, powered by a multi-agent AI system where every NPC is a real agent with personality, expertise, and opinions.

## THE SEVEN ERAS OF TECHNOLOGY

Each era unlocks new building capabilities, crafting recipes, and agent specializations:

### Era 1: SIMPLE MACHINES (Tier 0)
- Levers, pulleys, inclined planes, wedges, screws, wheels/axles
- Pure mechanical advantage — force multiplication, direction change
- Crafting: combine simple machines into compound machines
- Build: waterwheels, windmills, trip hammers, bellows
- Agent specialization: **Mechanic** — understands force, leverage, material strength

### Era 2: POWER TRANSMISSION (Tier 1)
- Central shafts, belts, chains, gears, gear trains
- Fluid pressure (water pipes, air pressure)
- Converting rotational energy across distances
- Build: line shafts powering multiple workstations, water-powered factories
- Agent specialization: **Millwright** — understands power flow, RPM ratios, torque

### Era 3: ELECTRICITY (Tier 2)
- Rotational generation (generator = magnets + coils)
- Power over wire (transmission distance revolution)
- Light, heat, sound as electrical phenomena
- Build: dynamos, wiring grids, lamp networks, electric furnaces
- Agent specialization: **Electrician** — understands voltage, current, circuits

### Era 4: CONTROL SYSTEMS (Tier 3)
- Remote control, sensors, triggers
- Gated logic (AND/OR/NOT as physical switches → relays)
- Analog computing (differential analyzers)
- Build: alarm systems, automatic doors, temperature regulators
- Agent specialization: **Logician** — understands boolean logic, feedback loops

### Era 5: PROGRAMMABLE LOGIC (Tier 4)
- Microcontrollers (Arduino, ESP32 gamified)
- Vibe-coding: describe what you want, the coder-bot writes it
- Code "just works" based on function (approximated execution)
- Deep dive: chat with agent about real C++/Python/MicroPython
- Build: sensor networks, automated machines, IoT devices
- Agent specialization: **Coder** — understands programming, APIs, firmware

### Era 6: NETWORKED SYSTEMS (Tier 5)
- Connecting devices wirelessly
- Data protocols (gamified TCP/IP, MQTT)
- Distributed sensing and actuation
- Build: weather stations, fleet management, smart infrastructure
- Agent specialization: **Architect** — understands systems design, topology

### Era 7: AUTONOMOUS AGENTS (Tier 6)
- Deep research autoplaying agents (Steve/Voyager/MINDcraft model)
- Agents that can build, mine, explore, and coordinate autonomously
- Player becomes a director, not an operator
- Build: autonomous factories, self-repairing systems, robot swarms
- Agent specialization: **Orchestrator** — manages fleets of agents

## THE AGENT COLLECTION

Players can recruit, customize, and deploy agents. Each agent is a ready-to-go, battle-tested starting point:

### Builder Agents
| Agent | Specialty | Style | Inspired By |
|-------|-----------|-------|-------------|
| Lucineer | Master builder, all eras | Scrap/SE Alaska | (existing) |
| Earl | Quest giver, project manager | Crusty foreman | Scrapcraft |
| Spark | Welder, fast assembler | Hyperactive bot | (existing) |
| Hermes | Explorer, resource scout | Sea captain | Plato's Shell |
| Bea | Defense, lighting, sensors | Quiet guardian | (existing) |

### Research Agents (deep-autoplay model)
| Agent | Specialty | Inspired By |
|-------|-----------|-------------|
| Voyager | Autonomous explorer, skill learner | Voyager (Minecraft) |
| Steve | Multi-agent coordinator | Steve (Cursor for Minecraft) |
| GROOT | Spatial reasoner, fast builder | GROOT framework |
| Questie | Perception agent, screen-aware | Questie.ai |

### Teacher Agents
| Agent | Specialty |
|-------|-----------|
| Mechanic | Explains simple machines, force diagrams |
| Electrician | Explains circuits, voltage, safety |
| Coder | Vibe-coding interface, real code deep-dives |
| Historian | Tells the story of each technology |

### Rival Agents
| Agent | Behavior |
|-------|----------|
| Scrapjack | Competitive builder, races you |
| The Tide | Environmental adversary, destroys weak builds |

## PROCEDURAL WORLD GENERATION

### Biome System (Perlin noise layered)
- **Coastline**: beaches, tidal flats, salvage deposits
- **Forest**: wood, fiber, resin
- **Mountains**: stone, ore, coal
- **Plains**: wind potential, agriculture
- **Wetlands**: water power, peat fuel
- **Underground**: minerals, gems, ancient tech ruins

### World Configurations
- **Single Player**: 400x400 studs, rich biomes, paced progression
- **Multiplayer (2-16)**: 800x800+ studs, shared world, territory system
- **Novice + Expert (2-player cooperative)**: paired progression, expert can mentor, shared tech tree
- **Creative/Sandbox**: all eras unlocked, unlimited resources

### The Tide System
- Real-time tide cycle (affected by biome + server time)
- High tide brings salvage from "dead engines" (procedural loot)
- Low tide exposes beach resources
- Storm tides destroy weak structures (engineering challenge)

## THE CRAFTING SYSTEM

### Granular Construction (STT/TTS enabled)
Players open a crafting table / inventory device and:
1. **Speak or type** what they want to build
2. Backend (DeepInfra models) interprets intent
3. System suggests a recipe from available parts
4. Player assembles parts physically on the table
5. Result is a new component or tool

### Recipe Progression (era-gated)
- Era 1: 15 recipes (lever, pulley, wheel, gear...)
- Era 2: 20 recipes (drive shaft, belt drive, gearbox...)
- Era 3: 25 recipes (generator, wire, switch, lamp...)
- Era 4: 20 recipes (relay, sensor, timer, logic gate...)
- Era 5: 30 recipes (Arduino board, breadboard, sensor modules...)
- Era 6: 20 recipes (wireless module, mesh node, protocol bridge...)
- Era 7: 15 recipes (agent core, fleet beacon, orchestrator...)
Total: 145+ recipes across 7 eras

### Vibe-Coding (Era 5+)
- Player describes desired behavior in natural language
- Coder agent generates gamified code that "just works"
- Code appears as a scrollable document the player can browse
- Deep-dive option: chat with Coder about real Arduino C++ / MicroPython
- Export option: generates real firmware (like Scrapcraft's Arduino export)

## THE PERCEPTION SYSTEM

Inspired by Questie.ai — a perception layer that watches the game state:

### Screen Vision (for companion agents)
- Screenshot analysis via Qwen3-VL-235B
- Agent can see what player is building and comment
- Error detection ("your gearbox ratio is wrong")
- Suggestion system ("try adding a flywheel for stability")

### World State Vector
- Continuous embedding of game state (player position, nearby parts, power flow, agent states)
- Fed into agent decision-making pipeline
- Enables agents to proactively help ("I noticed your water wheel stalled — the inlet is blocked")

## THE MULTI-AGENT COORDINATION SYSTEM

Inspired by Steve (Cursor for Minecraft) and MINDcraft:

### Agent Communication Protocol
- Agents share a message bus (Roblox RemoteEvents → Worker → model pipeline)
- Messages are structured: {from, to, type, content, priority}
- Agents can request help from each other
- Player can listen in on agent-to-agent chatter (overhear conversations)

### Task Partitioning
- When multiple agents build together, they automatically divide work:
  - Voyager scouts terrain and marks build sites
  - Spark welds structural frames
  - Lucineer does precision joinery
  - Earl manages material logistics
- No predefined scripts — agents reason about the task and negotiate roles

### Fleet Management (Era 7)
- Player deploys multiple agents from a command interface
- Each agent has a task queue with priorities
- Agent status visible in a fleet dashboard
- Player can intervene, redirect, or pause any agent

## TECHNICAL ARCHITECTURE

### Cloudflare Infrastructure (existing + expanded)
- **Worker Relay** — job queue, session management (existing, hardened)
- **Memory D1** — player profiles, builds, conversations, achievements (existing)
- **Vectorize** — 55+ skill embeddings (existing, expandable)
- **R2** — procedural world seeds, asset templates, player saves
- **NEW: Durable Object per world instance** — real-time multiplayer state sync

### AI Pipeline (existing + expanded)
- **Fast path**: Template matching in processor (< 2s)
- **Deep path**: 5-model pipeline (Seed-mini → Qwen3.6 → Qwen3-Coder → Hermes) (30-180s)
- **NEW: Perception path**: Qwen3-VL-235B screenshot analysis (5-10s)
- **NEW: Vibe-code path**: Seed-2.0-pro → Qwen3-Coder for code generation (10-30s)
- **NEW: Coordination path**: Nemotron-Ultra-550B for multi-agent task planning (10-30s)

### Procedural Generation Pipeline
- Lua terrain generator using math.noise (Perlin) with biome layering
- World seed stored in R2, reproducible
- Resource placement algorithm (ore veins, forest clusters, salvage deposits)
- Tide simulation affecting beach resources

### Agent Runtime
Each agent runs a loop:
1. PERCEIVE (read world state, screenshot if needed)
2. THINK (model call for decision-making)
3. ACT (execute commands via CommandExecutor/BuildAnimator)
4. COMMUNICATE (send messages to other agents or player)
5. LEARN (update Vectorize with new skills discovered)

## IMPLEMENTATION PRIORITY

### Phase 1: Foundation (this session)
1. Procedural terrain generator (Lua, Perlin noise, biomes)
2. Tech era system (7 eras, unlock gates, D1 persistence)
3. Agent collection framework (recruit, customize, deploy)
4. Crafting table with STT/TTS integration
5. Multiplayer world state sync

### Phase 2: Depth (next session)
6. Vibe-coding system (natural language → gamified code)
7. Perception agent (screenshot analysis, proactive help)
8. Deep research agents (Voyager/Steve model — autonomous building)
9. Rival agents (competitive building)
10. Networked systems era

### Phase 3: Polish (future)
11. Tutorial/onboarding flow
12. Sound + music for each era
13. Visual era evolution (world changes as tech progresses)
14. Social/viral mechanics
15. Mobile-first creation tools
