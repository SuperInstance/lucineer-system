# SLACKWATER — THE UNIFIED INTEGRATION PLAN

*The one document that everything else plugs into. Synthesized from 13 design documents spanning architecture, character, world, agents, UX, economy, perception, viral mechanics, autonomous systems, polish, and gap analysis. Where the documents agree, this plan is firm. Where they disagree, this plan arbitrates. Where they're silent, this plan extends.*

---

## 1. SYSTEM MAP

### The Full Topology

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ROBLOX CLIENT (Luau)                              │
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌──────────┐ │
│  │ BuildFX  │  │ Atmo-    │  │ WorldScan │  │ Perception│  │ Slack-Pad│ │
│  │ (choreo) │  │ sphereRig│  │ (spatial) │  │ Capture  │  │ (vibe UI)│ │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘  └─────┬────┘  └────┬─────┘ │
│       │              │              │               │            │       │
│  ┌────▼──────────────▼──────────────▼───────────────▼────────────▼────┐ │
│  │                    CommandExecutor                                  │ │
│  │  createPart · addLight · setTerrain · markUnfinished · sendMessage │ │
│  │  (params dispatch fixed, rotation+colorJitter+PBR added)            │ │
│  └────────────────────────────┬───────────────────────────────────────┘ │
│                               │                                          │
│  ┌──────────────┐    ┌────────▼────────┐    ┌─────────────────────────┐ │
│  │ ChatHandler  │───►│  Worker Relay    │◄──►│  Poller (job results)   │ │
│  │ (STT/text)   │    │  (HTTP via Http  │    │  (progressive feedback) │ │
│  └──────────────┘    │   service)       │    └─────────────────────────┘ │
│                      └────────┬──────────┘                               │
└───────────────────────────────┼──────────────────────────────────────────┘
                                │
                     ┌──────────▼──────────┐
                     │  CLOUDFLARE WORKER   │
                     │  (Job Queue + API)   │
                     │                      │
                     │  ┌────────────────┐  │
                     │  │ Durable Object │  │
                     │  │ (per-session)  │  │
                     │  │                │  │
                     │  │ • Job claiming │  │
                     │  │ • Lease+TTL    │  │
                     │  │ • Alarm prune  │  │
                     │  └───────┬────────┘  │
                     └──────────┼───────────┘
                                │
              ┌─────────────────┼─────────────────────┐
              │                 │                      │
   ┌──────────▼─────┐  ┌───────▼────────┐  ┌──────────▼──────────┐
   │  MEMORY (D1)   │  │  VECTORIZE     │  │  PROCESSOR          │
   │                │  │  (skill index) │  │  (process_v2.py)    │
   │ • player profs │  │                │  │                     │
   │ • build history│  │ • 55+ skills   │  │  ┌────────────────┐ │
   │ • conversations│  │ • player-built │  │  │  THE BRAIN     │ │
   │ • bond_level   │  │   patterns     │  │  │  (brain.py)    │ │
   │ • achievements │  │ • semantic     │  │  │                │ │
   └────────────────  └────────────────┘  │  │ Fast Path:     │ │
                                          │  │ Seed-mini →    │ │
              ┌───────────────────────────┘  │ template match │ │
              │                              │                │ │
              │                              │ Deep Path:     │ │
              │                              │ Seed-pro →     │ │
              │                              │ Qwen3.6 →      │ │
              │                              │ Qwen3-Coder →  │ │
              │                              │ Hermes-405B →  │ │
              │                              │ Safety check   │ │
              │                              └───────┬────────┘ │
              │                                      │          │
              │     ┌────────────────────────────────┘          │
              │     │                                            │
              │     ▼                                            │
   ┌──────────▼─────────────────────────────────────────────────┐│
   │                    AI MODEL PIPELINE                       ││
   │                   (DeepInfra routing)                      ││
   │                                                            ││
   │  Intent Parse:  Seed-2.0-mini (fast, cheap)                ││
   │  Spatial Plan:  Qwen3.6-35B / Seed-2.0-pro                ││
   │  Code Gen:      Qwen3-Coder-480B                          ││
   │  Personality:   Hermes-3-Llama-405B (Lucineer's voice)    ││
   │  Vision:        Qwen3-VL-235B (perception screenshots)    ││
   │  Coordination:  Nemotron-Ultra-550B (multi-agent tasks)   ││
   │  Safety:        Nemotron-Content-Safety-3.5               ││
   │  Embeddings:    BAAI/bge-m3 (Vectorize)                  ││
   │  TTS:           Qwen3-TTS-VoiceDesign (pre-gen only)      ││
   └────────────────────────────────────────────────────────────┘│
              │                                                 │
              │     ┌───────────────────────────────────────────┘
              │     │
   ┌──────────▼─────▼───────────────────────────────────────────┐
   │                    GAME SYSTEMS                            │
   │                                                           │
   │  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
   │  │ EraSystem   │  │ CraftingSys  │  │ Economy/Tide     │  │
   │  │ (7 eras,    │  │ (145 recipes,│  │ (18min cycle,    │  │
   │  │  unlock     │  │  era-gated,  │  │  scarcity curves,│  │
   │  │  gates)     │  │  vibe-code)  │  │  storm pushes)   │  │
   │  └──────┬──────┘  └──────┬───────┘  └────────┬─────────┘  │
   │         │                │                    │            │
   │  ┌──────▼──────────────▼────────────────────▼──────────┐  │
   │  │              BOND SYSTEM                             │  │
   │  │  (5 stages, behavior-triggered, never shown as meter)│  │
   │  │  Stage transitions query player journal in D1        │  │
   │  │  Unfinished Rule: markUnfinished → detect completion │  │
   │  └─────────────────────┬───────────────────────────────┘  │
   │                        │                                   │
   │  ┌─────────────────────▼───────────────────────────────┐  │
   │  │           NPC / AGENT ECOSYSTEM                      │  │
   │  │                                                      │  │
   │  │  HUB NPCS:          RECRUITABLE AGENTS:              │  │
   │  │  • Lucineer (anvil)  • Rook (structure)              │  │
   │  │  • Earl (manifest)   • Pike (speed)                  │  │
   │  │  • Spark (weld)      • Tess (electronics)            │  │
   │  │  • Hermes (tender)   • Wren (exploration)            │  │
   │  │  • Bea (light)       • March (Era 1-2 teacher)       │  │
   │  │  • Forty-Eight       • Ferro (Era 3-4 teacher)       │  │
   │  │    (raven)           • Cipher (Era 5-7 teacher)      │  │
   │  │                      • Moss (companion)              │  │
   │  │  RIVALS:              • Jackscrew (competitive)      │  │
   │  │  • The Tide           • Rootwell (ideological)       │  │
   │  └──────────────────────────────────────────────────────┘  │
   │                                                           │
   │  ┌───────────────────────────────────────────────────────┐│
   │  │  AUTONOMOUS AGENT LOOP (Era 7)                        ││
   │  │  Perceive → Think → Act → Communicate → Learn        ││
   │  │  Skill discovery → Vectorize storage → recall         ││
   │  │  Multi-agent task partitioning via message bus        ││
   │  └───────────────────────────────────────────────────────┘│
   │                                                           │
   │  ┌───────────────────────────────────────────────────────┐│
   │  │  VIRAL / SOCIAL SYSTEMS                               ││
   │  │  Build Cards · Legacy Builds · Revenge Build          ││
   │  │  Recipe Trading · Spectate Invite · Era Showcase      ││
   │  │  Workshop Hall · Co-op Mentor Mode                    ││
   │  └───────────────────────────────────────────────────────┘│
   └───────────────────────────────────────────────────────────┘
```

### Data Flow Summary

1. **Player speaks/types** → ChatHandler fires → HTTP POST to Worker Relay (with `sessionId`)
2. **Worker creates job** (status: `pending`) → returns `jobId` to client
3. **Processor polls** → claims job (atomic lease) → reads player context from D1 (bond level, recent builds, preferences) → recalls relevant skills from Vectorize
4. **Brain pipeline runs**: Seed-mini (intent) → Qwen3.6 (spatial plan) → Qwen3-Coder (command JSON) → Hermes-405B (Lucineer's voice) → Nemotron-Safety (kid-safe check)
5. **Result posted** to Worker → Poller picks up → CommandExecutor dispatches params → BuildFX materializes parts wave-by-wave → sendMessage displays Lucineer's line
6. **Perception loop** (parallel): WorldScanner snapshots state → optional Qwen3-VL screenshot analysis → routes observations to agent dialogue queues → agents proactively comment
7. **Nightly maintenance pass**: low-cost agent walks player builds → writes one journal observation to D1 → surfaces later as dialogue, logbook entries, gifts

---

## 2. THE TEN BIGGEST INSIGHTS FROM CROSS-DOCUMENT ANALYSIS

### Insight 1: The Unfinished Rule Is the Keystone — It Connects Six Systems

No single document fully reveals this. Read together, the Unfinished Rule is not just Lucineer's personality trait — it's the mechanical spine that connects:
- **Bond System** (completing a gap is the Stage 3→4 trigger)
- **BuildFX** (the `markUnfinished` command creates a detectable physical affordance)
- **Viral Mechanics** (the Finished Skiff story: gaps travel between players via the tide)
- **Memory D1** (the nightly journal tracks whether a gap was completed)
- **Vibe-Coding** (Cipher's teaching style mirrors the gap philosophy — "the thinking was yours")
- **Achievements** ("Finished His Work" is the bond trigger made into a hidden achievement)

**Action:** The `markUnfinished` command and its completion-detection logic must be a P0 build priority. It is the single most interconnected mechanic in the game.

### Insight 2: Latency Is the Character — Across Three Documents

The Polish Plan says "latency is animation." The Agent UX says "the player should never once wonder what the agent is computing." The Character Bible says he "talks like someone paying by the word." All three describe the same design principle from different angles: **dwell time must be spent as characterization, never as loading.** The Gap Analysis reveals this is currently broken (60s dead air, then timeout). The insight is that fixing latency is not a performance task — it's a character design task. The progressive ack system ("Let me look at the ground first") and the BuildFX choreography together convert 30-90 seconds of model inference into 30-90 seconds of watching a craftsman work.

### Insight 3: The Economy Document Solves the Retention Problem the UX Document Creates

The Agent UX's attention-scarcity model (Lucineer works with one player at a time) is brilliant for character but devastating for retention — waiting players have nothing to do. The Economy document's scarcity curves solve this precisely: while waiting for Lucineer's bench, players are pushed to explore (bottleneck resources are 300+ studs from spawn), engage with the tide cycle (18-minute loot rolls), or interact with other agents (Earl's manifest, Wren's exploration quests). The economy IS the queue management system.

### Insight 4: The Vibe-Coding System and the Bond System Share Identical Architecture

Both are "approximate then reveal." Vibe-coding shows SlackScript (accessible) then reveals real C++ (depth). The bond system shows behavior changes (accessible) then reveals the mechanic underneath (depth). Both honor the same principle: **the surface layer should never require expertise, but expertise should always be rewarded.** This means the UX patterns should be shared — the same "glance deeper" interaction (click a line of SlackScript / notice a gap in a build) serves both systems.

### Insight 5: Rootwell Is the Most Important NPC Nobody Has prioritized

The Agent Collection introduces Rootwell as Lucineer's ideological opposite — anti-technology, pro-simplicity. But read against the Master Architecture's 7-era progression and the Economy's push for advancement, Rootwell becomes structurally critical: **he is the friction that makes progression meaningful.** Without him, the tech tree is a treadmill. With him, every era unlock is a philosophical choice. His presence transforms the game from "collect all the technology" to "decide whether you should." This is the kind of friction that drives engagement (players argue about it on Discord for months) and press coverage ("this game questions its own premise").

### Insight 6: The Gap Analysis and the Polish Plan Are the Same Document at Different Altitudes

The Gap Analysis says "nothing happens when you type 'build me a castle'" (P0 contract bug). The Polish Plan says "even if it did happen, it would look like gray boxes popping in" (visual choreography). These are the same problem — the boundary between intent and execution — at the protocol level and the perceptual level. The unified insight: **fix them in order.** Protocol first (Gap #1, #2, #6), then perception (Polish §1.1, §1.2), then character (Gap #7, Polish §2). Each layer is invisible until the layer below it works.

### Insight 7: The Viral Mechanics Document Underestimates the Character as Content

The viral mechanics propose five shareable systems (Revenge Build, Recipe Trade, Ghost Build, Spectate, Era Showcase). But the most viral asset in the entire design — across all 13 documents — is **Lucineer's dialogue itself.** The Build Card concept from the Polish Plan ("a screenshot with a crusty foreman's opinion attached") is worth more than all five viral mechanics combined. The character bible's 20 voice lines are the game's most shareable content. The viral strategy should lead with "Lucineer said WHAT to me?" moments, not with systems.

### Insight 8: The Multi-Agent Architecture and the Agent UX Contradict Each Other on Communication

The Multi-Agent Architecture proposes a robust message bus with 14 message types, WebSocket connections, and real-time coordination. The Agent UX proposes the opposite: "agents never talk to each other through hidden channels... word moves at player speed." These aren't reconcilable as-is. The resolution: **the Agent UX model governs hub NPCs (Lucineer, Earl, Bea, Hermes, Spark, Forty-Eight). The Multi-Agent Architecture governs Era 7 autonomous builder agents.** Two communication regimes for two classes of entity, separated by a 6-era progression gate.

### Insight 9: Forty-Eight Is a Vectorize Interface in Disguise

The raven that steals the 6th bolt, always lands exactly, and maintains exactly 48 objects on its roof — this is a character Bible entry that describes a database index. Forty-Eight is a living metaphor for the Vectorize embedding system (48 dimensions, 6 bits, exact, no drift — per Logbook №41). The raven should literally query Vectorize when deciding what to steal and what to trade. What it leaves in trade is "always somehow the thing your current build actually needed" — that's a semantic similarity search against the player's current build context, delivered as a crow.

### Insight 10: The Polish Plan's Atmosphere Rig Is the Highest-ROI Work in the Entire Project

18 hours of work (lighting + choreography + sound bed) transforms every build the system will ever produce, retroactively, without touching the AI pipeline, the Worker, or the brain. No other work item in any of the 13 documents has this ratio of impact to effort. It should be the very first thing done after the P0 gap fixes, before any feature work, because it changes the perceived quality of everything that follows.

---

## 3. CONFLICTS AND RESOLUTIONS

### Conflict 1: Agent Communication Architecture
- **Multi-Agent doc:** Full message bus with WebSocket connections, 14 message types, real-time pub/sub
- **Agent UX doc:** "Agents never talk to each other through hidden channels. Every dependency travels through the world."
- **Resolution:** Two-tier system. Hub NPCs (Era 0-6) communicate diegetically only — manifest pages, horn blasts, Forty-Eight courier, player-as-nervous-system. Autonomous research agents (Era 7) use the full message bus for fleet coordination. The message bus is an Era 7 unlock, not a baseline system.

### Conflict 2: Coder Agent Identity
- **Master Architecture:** "Coder" is listed as both a teacher agent and an era specialization
- **Agent Collection:** Cipher is the computational teacher (Era 5-7)
- **Vibe-Coding doc:** Introduces "Glitch" as the coder agent
- **Resolution:** **Cipher** is the canonical name (Agent Collection wins — it's the deepest characterization). "Glitch" is Cipher's Slack-Pad avatar name (the pixel-art persona on the device screen). The agent is Cipher; the interface persona is Glitch. "Coder" is the era specialization title, not the agent's name.

### Conflict 3: Agent Count and Roster
- **Master Architecture:** Lists Lucineer, Earl, Spark, Hermes, Bea + Voyager, Steve, GROOT, Questie + Mechanic, Electrician, Coder, Historian + Scrapjack, The Tide
- **Agent Collection:** Lists Rook, Pike, Tess, Wren, March, Ferro, Cipher, Jackscrew, Rootwell, Moss, Bea, The Tide — 12 agents total, no Voyager/Steve/GROOT/Questie
- **Resolution:** The Agent Collection roster is canonical for launch (12 agents). The research agents (Voyager, Steve, GROOT, Questie) are Era 7 content — they are not starting agents but become available as autonomous fleet members at the end of the tech tree. The Master Architecture's "Mechanic/Electrician/Coder" teacher labels map to March/Ferro/Cipher in the Agent Collection.

### Conflict 4: Vibe-Coding UI — Slack-Pad vs. Diegetic Integration
- **Vibe-Coding doc:** Proposes a dedicated device ("Slack-Pad") with split-screen UI, pixel-art avatar
- **Agent UX doc:** "Could this exist in the yard if there were no computer? Chalk passes. A chat window does not."
- **Resolution:** The Slack-Pad is diegetic — it is an in-world object (a rugged tablet assembled from salvage, consistent with the world aesthetic). It is carried, placed on workbenches, and aimed at machines. Its screen is the only screen in the game, and it exists because the player's character built it at Era 4. This satisfies the Agent UX's diegetic requirement while allowing the functional UI the vibe-coding system needs. The pixel-art "Glitch" is the visual proxy for Cipher when the agent isn't physically present.

### Conflict 5: Achievement System Scale
- **Master Architecture:** Cites "49 achievements"
- **Polish Plan:** Proposes 12 hidden achievements, never listed anywhere
- **Resolution:** **12 achievements** (Polish Plan wins). 49 visible achievements turn Lucineer into a quest dispenser. 12 hidden achievements, discovered only by triggering them and delivered as in-character dialogue, maintain the design principle that "bond is the only meter, and it is never shown as a number."

### Conflict 6: Multiplayer Model
- **Master Architecture:** "Multiplayer (2-16), shared world, territory system"
- **Viral Mechanics:** Proposes shared persistent worlds, co-op mentor mode, friend invites
- **Agent UX:** "One man with one bench and forty relationships" — attention scarcity
- **Resolution:** Three multiplayer tiers: (1) **Solo** — the primary experience, full character depth. (2) **Co-op (2 players)** — the Novice+Expert mentor mode, one shared bench, Lucineer divides labor. (3) **Server (up to 16)** — shared hub world (Slackwater Yard), each player has their own build plot, Lucineer's attention is visibly scarce (the queue-is-the-content principle from Insight 3). No "territory system" — that adds griefing surface without adding depth.

### Conflict 7: The Push Path
- **Gap Analysis:** The OPENCLAW_CALLBACK_URL points at a private WSL IP and cannot work from a Cloudflare Worker
- **Resolution:** Delete the push path. Commit to polling (the processor already does this). Make the push failure non-fatal. Simple, works today, and avoids exposing internal infrastructure.

### Conflict 8: Persona for Model Replies
- **Gap Analysis:** Three personas exist — "poetic dream-weaver" (creative mode), "shipyard foreman" (fast mode), "friendly assistant" (deep/coder mode, the one that actually runs)
- **Character Bible:** The canonical Lucineer — craftsman, partner, crank, occasional poet
- **Resolution:** One persona constant, derived from the Character Bible, injected at every path. The fast path gets a condensed version (2-3 anchor traits). The deep path gets the full persona. Both pull from the same source text. The "friendly assistant" instruction in SYSTEM_CODER is deleted and replaced with the character bible voice rules.

---

## 4. INTEGRATION PRIORITIES

### Dependency Graph

```
PHASE 0: FIX THE BROKEN SEAMS (GAP_ANALYSIS P0s)
══════════════════════════════════════════════════
A1. One source of truth (Rojo build)  ──► everything
#1.  Params dispatch fix             ──► builds render correctly
#2.  API contract alignment          ──► jobs reach the queue
#6.  Job claiming + non-fatal push   ──► no runaway spend
     ─── FIRST REAL PLAYTEST ───
#3.  Rotate key, server-side only    ──► safe to test externally
#5.  Text filtering + safety stage   ──► Roblox policy compliant

PHASE 1: MAKE IT FEEL REAL (POLISH §1)
══════════════════════════════════════
Atmosphere rig (§1.1)               ──► every build looks better
BuildFX choreography (§1.2)          ──► builds arrive, don't pop
Rotation + colorJitter (§1.4)       ──► angled walls, varied surfaces
Ambient sound bed (§3 L1)            ──► world has mood
Build SFX (§3 L2)                    ──► weight and impact
Delete off-voice strings (§2)        ──► character integrity

PHASE 2: MAKE IT A CHARACTER
═══════════════════════════
#7.  Unified persona (Character Bible)──► consistent voice
#4.  Wire memory + vectorize          ──► he remembers
Bond stage tracking in D1             ──► stages compute from journal
markUnfinished + completion detect    ──► the core loop works
Non-verbal vocalizations (§3 L3)     ──► voice without latency
First-60-seconds beat sheet           ──► onboarding is diegetic
Magic Moments 1 & 3                   ──► the jaw-drops

PHASE 3: MAKE IT A GAME
═══════════════════════
Era system (7 eras, unlock gates)     ──► progression structure
Crafting system (145 recipes)         ──► player agency
Tide economy (18min cycle)            ──► resource loop
Storm system + Magic Moment 4         ──► environmental adversary
Hidden achievements (12)              ──► discovery moments
Build Cards                           ──► shareable artifacts

PHASE 4: MAKE IT SOCIAL
═══════════════════════
Multi-session DO routing (#6c)       ──► real multiplayer
Lucineer references other players     ──► world feels inhabited
Legacy Builds                         ──► persistent presence
Recipe Trading                        ──► social crafting
Co-op mentor mode                     ──► novice+expert pair
Player patterns → Vectorize          ──► community skill library

PHASE 5: MAKE IT DEEP
═════════════════════
Vibe-coding system (Era 5+)          ──► natural language programming
Perception system (Qwen3-VL)         ──► agents see the world
Autonomous agents (Era 7)            ──► player as director
Fleet management                      ──► multi-agent coordination
Rootwell ideological arc              ──► philosophical friction
Export to real Arduino                ──► bridge to physical world
```

### What Depends on What (Critical Path)

1. **Rojo build system** → nothing else works without this (fixes land in the wrong copy)
2. **Params dispatch + API contracts** → the core loop runs at all
3. **Job claiming** → no runaway AI bills
4. **Atmosphere + BuildFX** → the game looks like something
5. **Unified persona + memory** → Lucineer is a character, not a bot
6. **markUnfinished + bond tracking** → the core loop has meaning
7. **Era system + crafting** → the core loop has direction
8. **Everything else** → adds depth, sociality, and longevity

---

## 5. WHAT'S MISSING

### Systems Designed But Not Specified

1. **Tutorial / Onboarding Flow.** The Agent UX's first-60-seconds beat sheet is brilliant but covers only the opening. There is no document describing the transition from "carry the beam" to "you now understand the crafting table, the era system, and the bond arc." The game needs a 30-minute guided first-session that teaches systems through diegetic moments, not popups. **Owner: needs a new doc.**

2. **Mobile UX Strategy.** Every document references mobile players, but no document addresses how the Slack-Pad, the crafting table, the perception system, and the multi-agent fleet work on a 6-inch touch screen. Roblox is 70%+ mobile. The build input method (voice, text, tap-to-place) needs explicit mobile design. **Owner: needs a new doc.**

3. **Moderation and Safety at Scale.** The Gap Analysis identifies the text filtering gap (#5) and safety model gap. But no document addresses what happens when 10,000 players are generating AI-narrated content simultaneously. Rate limits, content moderation queues, report systems, and the moderation burden of Ghost Builds (strangers' content persisting in your world) all need design. **Owner: needs a new doc.**

4. **Audio / Music Asset List.** The Polish Plan's sound design section (§3) specifies four layers and gives sound IDs for some. But the full asset list — every build SFX per material, every ambient loop, every storm sound, the Magic Moment cues, the 30-40 non-verbal Lucineer vocalizations — needs to be specified, sourced, and budgeted. **Owner: needs a new doc or expansion of Polish §3.**

5. **Analytics and Telemetry.** No document describes what metrics the game tracks. For a game this novel — AI-driven NPCs, bond-based progression, vibe-coding — understanding player behavior is critical. What do we track? Bond stage distribution? Era unlock rates? Build-to-conversation ratios? Drop-off points in the first session? **Owner: needs a new doc.**

### Design Gaps Within Existing Documents

6. **The Historian Agent** is listed in the Master Architecture but has no entry in the Agent Collection. If kept, needs full characterization. If cut, remove from the architecture. **Recommendation: fold into March** (March already teaches mechanical eras; she can tell the story of technology, not just the mechanics).

7. **Scrapjack** (Master Architecture's rival agent) is not in the Agent Collection. **Recommendation: renamed to Jackscrew** (Agent Collection's competitive builder). One character, not two.

8. **The World Generator** is described in the Master Architecture (Perlin noise, biomes, 400x400 for solo) but has no technical spec. The `vibe-world/` repo exists but is a static `.rbxlx` — there's no procedural generation code. **Needs: Lua terrain generation module, biome parameter table, resource placement algorithm.**

9. **Save System** is mentioned (R2 for player saves) but not specified. How does world state persist? What happens to builds when a player logs off? How do Legacy Builds work with the DO model? **Needs: save/load architecture doc.**

10. **PvP / Competition Mode.** The Master Architecture mentions territory systems and rival agents. Jackscrew provides competitive building. But no document specifies how competitive modes actually work — scoring, matchmaking, rewards. **Recommendation: defer to post-launch.** Cooperative and solo are the launch modes.

---

## 6. THE 30-DAY BUILD PLAN

### Assumptions
- 1 developer, full-time, with AI coding agents (Claude Code / KimiCode)
- Existing infrastructure (Worker, D1, Vectorize, brain.py) is kept and fixed, not rebuilt
- Roblox Studio available; Rojo sync configured on Day 1
- Total: ~30 working days

---

### WEEK 1: MAKE IT WORK (Days 1-7)

**Theme:** The core loop runs end-to-end. A player types "build me a castle" and something correct and non-gray appears.

| Day | Focus | Deliverables |
|-----|-------|-------------|
| 1 | **Rojo + source of truth** | One repo, one build command, .rbxlx is output not input. Delete `vibe-world/src`. |
| 2 | **Gap #1: Params dispatch** | `CommandExecutor.execute` uses `command.params`. Castle template produces distinct named parts at distinct positions. Smoke test passes. |
| 3 | **Gap #2: API contracts** | `sessionId` in all payloads. `POST /api/message` returns 200 with `jobId`. `POST /api/state` returns 200. `GET /api/job/:id` returns `reply` field that client reads. |
| 4 | **Gap #6: Job claiming** | Jobs start as `pending`, atomically claim with 3-min lease, `attempts` counter, dead-letter at 3. Push path made non-fatal. Schema migration for new columns. |
| 5 | **Gap #3 + #5: Security + filtering** | API key rotated, moved to ServerStorage. `TextService:FilterStringAsync` on all outbound text. Nemotron-Safety-3.5 stage added to brain pipeline. |
| 6 | **Gap #7: Unified persona** | Character Bible §1 text becomes `LUCINEER_PERSONA` constant. `SYSTEM_FAST` references it. `SYSTEM_CODER` "friendly" instruction replaced. `process_v2.py` invokes `--creative` flag. Hermes stage no longer accepts commands. |
| 7 | **Integration playtest** | Full stack: type message → job created → brain runs → commands return → parts materialize → Lucineer speaks in voice. Bug list generated and triaged. |

**Exit criteria:** A player types "build me a castle," waits ~60 seconds, and sees distinct parts appear at their location with a Lucineer voice line in character.

---

### WEEK 2: MAKE IT FEEL REAL (Days 8-14)

**Theme:** The game looks and sounds like a place. Builds arrive with weight. The world has mood.

| Day | Focus | Deliverables |
|-----|-------|-------------|
| 8 | **Atmosphere rig** (Polish §1.1) | `Atmosphere.lua` with `overcast`, `goldenhour`, `storm` presets. Future lighting enabled. Mobile quality scaling. |
| 9 | **BuildFX** (Polish §1.2) | `BuildFX.materializeBatch` — wave-by-wave materialization, dust particles, settle sounds. Wired into `CommandExecutor.executeBatch`. |
| 10 | **Command schema extension** (Polish §1.4) | `rotation`, `colorJitter`, `reflectance`, `castShadow`, `tag`, `surfaceAppearance` (PBR) added to `createPart`. Templates updated to use rotation. |
| 11 | **markUnfinished** (Polish §1.3) | New command type. Chalk outline + breathing glow + label. Completion detection via spatial overlap query. |
| 12 | **Sound design** (Polish §3) | Ambient bed (water, wind, foghorn, gulls). Build SFX (material-dependent settle sounds, pitch by mass). Cap concurrent sounds at 6. |
| 13 | **Gap #8: Progressive feedback** | Immediate ack before brain runs. Poller emits thinking-remotes at 10s/25s/45s with in-voice narration. `POLL_TIMEOUT` > `DEEP_TIMEOUT` > brain worst case. |
| 14 | **First-60-seconds beat** (Polish §2) | Delete the two off-voice strings. Implement the beat sheet: spawn in weather, he's working, "You're new. Grab a corner or don't." First hook appears. |

**Exit criteria:** The first minute of gameplay establishes a place, a character, and an invitation — with no tutorial popup.

---

### WEEK 3: MAKE IT A CHARACTER (Days 15-21)

**Theme:** Lucineer remembers, has opinions, and changes based on player behavior. The bond system computes invisibly.

| Day | Focus | Deliverables |
|-----|-------|-------------|
| 15 | **Gap #4: Wire memory** | D1 profile fetch in processor. Bond level read. Recent builds fetched. Conversation logged. All endpoints authenticated. Bond reset bug fixed (`COALESCE`). |
| 16 | **Gap #4: Wire Vectorize** | Skill recall in processor — top-3 skills by similarity for each build request. Used as few-shot examples in coder stage. `uses_count` incremented on match. |
| 17 | **Bond system** | Journal schema in D1 (one observation per build per night). Stage transition queries. Stage 1→2: player notices a flaw. Stage 2→3: player pushes back. Stage 3→4: player completes a hook. Stage 4→5: accumulated trades. |
| 18 | **Non-verbal vocals** (Polish §3 L3) | 30-40 short vocalizations pre-generated via Qwen3-TTS. Playback at reply start. Context-sensitive selection (agreeing, disagreeing, working, impressed). |
| 19 | **Magic Moments 1 & 3** | Moment 1 (The Continuation): player places part in unfinished hook → 4-second freeze → "Huh. You saw it too." Moment 3 (Torch Off): aurora event, all NPCs stop, two minutes of silence. |
| 20 | **Nightly journal pass** | Low-cost agent walks player builds, writes one observation each into D1. Observations surface as: dialogue callbacks ("Your bridge held through the last blow. I checked."), logbook entries, Stage 4 shaped gaps. |
| 21 | **Character integration playtest** | Play 3 sessions. Verify: voice is consistent, memory works across sessions, bond stage transitions fire correctly, hook completion triggers Moment 1. |

**Exit criteria:** After two sessions, Lucineer references something the player built in session 1. After completing a hook, the Continuation moment fires. The character has continuity.

---

### WEEK 4: MAKE IT A GAME (Days 22-30)

**Theme:** There are eras to unlock, things to craft, storms to survive, and reasons to come back.

| Day | Focus | Deliverables |
|-----|-------|-------------|
| 22 | **Era system** | 7-era definition table. Unlock gates (recipe completion + era-specific milestone). D1 persistence. Era-aware brain prompts (model knows what era the player is in). |
| 23 | **Crafting system (Era 1-2)** | 35 recipes (Era 0: 15, Era 1: 20). Crafting table interaction. STT integration for "speak what you want to build." Recipe suggestions from available parts. |
| 24 | **Tide economy** | 18-minute tide cycle. Loot tables from Economy doc (era-scaled). Beach restock. Bottleneck resource guaranteed every 7 tides. Hermes ping at 11 tides. Storm at 14. |
| 25 | **Storm system** | Storm tide event: barometer drop, wind shift, bell, 30% structure damage to unupgraded builds. `Atmosphere.apply("storm")` transition. Post-storm: salvage arrives, beach rearranged. |
| 26 | **Hub NPCs** | Earl at manifest window (quest queue). Spark orbiting Lucineer (weld micro-tasks). Bea at the Light (perspective/tea). Hermes at the float (supply line). Forty-Eight on roofline (exact-count trading). |
| 27 | **Hidden achievements** (12) | Wired as D1 events, delivered as Lucineer dialogue lines. "Not Fussy" (ignore him for a full session). "Finished His Work" (complete a hook). "Argued And Won" (change his mind). |
| 28 | **Build Cards** (Polish §4.1) | ViewportFrame render of completed build. Composited with Lucineer's reply line. Short URL. Mobile share sheet integration. |
| 29 | **Recruitment: Rook & Cipher** | Rook: south pillar storm event → build together → recruited. Cipher: Era 5 signal wreck → decode together → recruited. (Moss recruitment is ambient — no quest.) |
| 30 | **Full integration playtest** | Complete playthrough: spawn → first build → first argument → first hook completion → era unlock → first storm → first crafting recipe → first recruit. Bug list for polish iteration. |

**Exit criteria:** A new player can play for 2 hours, progress through Era 0→2, experience a storm, recruit Rook, complete one of Lucineer's hooks, and have a Build Card they could share.

---

### Post-30-Day Roadmap (Prioritized)

1. **Remaining recruitable agents** (Pike, Tess, Wren, March, Ferro, Moss, Jackscrew, Rootwell) — each with recruitment moment
2. **Vibe-coding system** (Era 5+) — Slack-Pad, SlackScript, deep-dive pathway, real code export
3. **Perception system** — Qwen3-VL screenshot analysis, proactive agent commentary
4. **Multiplayer** — Co-op mentor mode, then shared server hub
5. **Autonomous agents** (Era 7) — Voyager/Steve fleet coordination, message bus
6. **Viral mechanics** — Legacy Builds, Recipe Trading, Spectate Invite
7. **Music system** — 4 cinematic music moments (Polish §3 L4)
8. **Mobile UX** — touch controls, simplified build input, mobile quality scaling

---

## 7. THE ONE-SENTENCE PITCH

> **Slackwater is a multiplayer game-builder where you progress through the entire history of human technology — from levers to autonomous robots — alongside AI characters who are opinionated partners, not obedient tools, in a tidal scrapyard between dead game engines where everything the world forgot washes ashore, and the master builder you work beside has died in a thousand engines and is betting that this time, if he leaves one piece unfinished, you'll be the one to finish it.**

### Why it works for each audience:

- **Players:** "I want to build things with that guy" — the character hook is immediate
- **Developers:** "AI agents with persistent memory, multi-model pipelines, and diegetic UX" — the engineering is novel
- **Investors:** "Roblox + AI characters + educational tech tree + social virality" — the market is real
- **Journalists:** "A game where the AI has opinions about your architecture and the NPC remembers you across sessions" — the story writes itself

---

*End of Unified Integration Plan. This is the map. The territory is built one beam at a time.*
