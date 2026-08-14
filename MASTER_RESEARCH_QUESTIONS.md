# MASTER RESEARCH QUESTIONS — Slackwater / Lucineer

**Compiled:** 2026-08-03  
**Purpose:** The complete research backlog for the next phase of development. Every open question, unresolved design decision, and technical unknown across all source documents.

**Sources indexed:**
- `ai-writings/OPEN_RESEARCH_QUESTIONS.md` (ORQ)
- `ai-writings/DIARIES/RESEARCH_QUESTIONS.md` (DRQ)
- `lucineer-system/ROADMAP_whats_next.md` (ROAD)
- `lucineer-system/GAP_ANALYSIS.md` (GAP)
- `lucineer-system/INTEGRATED_ARCHITECTURE.md` (IA)
- `lucineer-system/SHIP_READINESS.md` (SHIP)
- `lucineer-system/CHARACTER_BIBLE.md` (CB)
- `lucineer-system/FABLE_WORLD_BIBLE.md` (FWB)

**Priority key:** P0 = blocks MVP | P1 = needed for launch | P2 = post-launch | P3 = future  
**Dependency format:** → RQ-XXX

---

## 1. TECHNICAL (ROBLOX / LUA)

**RQ-001** — How should the `CommandExecutor` command envelope (`{type, params}`) be enforced at the boundary so that every handler receives its parameters correctly? *(GAP #1)*  
Priority: **P0** | Dependencies: none

**RQ-002** — What is the canonical session identity format, and how should `sessionId` be generated, propagated, and validated across Lua → Worker → DO → processor? *(GAP #2, ROAD Decision 1)*  
Priority: **P0** | Dependencies: none

**RQ-003** — How should the Roblox client safely store and transmit authentication credentials without exposing them in ReplicatedStorage? *(GAP #3, SHIP 1.2)*  
Priority: **P0** | Dependencies: RQ-002

**RQ-004** — Should `runLua` and `addScript` be deleted entirely, or is there a safe whitelist-based parameterized behavior system worth building? *(GAP #9, SHIP 1.7, ROAD Tier 4)*  
Priority: **P0** | Dependencies: none

**RQ-005** — How should `setTerrain` handle grid alignment requirements for `FillBlock` vs deprecated `FillRegion`, and which terrain materials should be supported? *(GAP #9c)*  
Priority: **P1** | Dependencies: none

**RQ-006** — Should the game use `TextChatService` (new system) or legacy chat APIs, and how do spatial bubbles, system messages, and filtering hooks differ between them? *(GAP #9d)*  
Priority: **P0** | Dependencies: none

**RQ-007** — How should RemoteEvents be created and awaited to eliminate the client-side phantom-event race condition? Pre-create in `default.project.json`, or `WaitForChild` with timeout? *(GAP #9e)*  
Priority: **P1** | Dependencies: none

**RQ-008** — What is the optimal spatial query strategy for `WorldScanner` — `GetPartBoundsInRadius`, `workspace:FindPartsInRegion3`, or a custom spatial index? *(GAP #10)*  
Priority: **P1** | Dependencies: none

**RQ-009** — How should build-part counts be tracked efficiently (cached counter vs traversal) to avoid full-workspace scans on every quickScan tick? *(GAP #10b)*  
Priority: **P1** | Dependencies: RQ-008

**RQ-010** — Should the three divergent Lua source trees (`lucineer-roblox/src/`, `vibe-world/src/`, `.rbxlx`) be consolidated via Rojo, and what is the migration path? *(GAP A1, SHIP 0.1, ROAD Tier 1)*  
Priority: **P0** | Dependencies: none

**RQ-011** — How should build animation staggering work — fixed `task.wait()` intervals, distance-based delays, or physics-based part dropping? *(ROAD Tier 3 #15, GAP #8b)*  
Priority: **P1** | Dependencies: none

**RQ-012** — How can the `Poller` avoid stacking overlapping HTTP requests when poll intervals are shorter than network latency? *(GAP A6)*  
Priority: **P1** | Dependencies: none

**RQ-013** — What is the correct Luau type annotation for table parameters — `{ [string]: any }` vs `table` — and should `--!strict` mode be enforced project-wide? *(GAP A6)*  
Priority: **P2** | Dependencies: none

**RQ-014** — How should the `UIManager.showThinking` animation loop be guarded against leak when called multiple times rapidly? *(GAP A6)*  
Priority: **P2** | Dependencies: none

**RQ-015** — What data structure best captures the layered history of a found wreck (builder, owner, crew, final voyage, salvage) so players read it as story, not database? *(ORQ #2)*  
Priority: **P2** | Dependencies: none

**RQ-016** — How can buoyancy and hull damage be simulated with enough fidelity that a player recognizes a specific wreck from its silhouette alone? *(ORQ #7)*  
Priority: **P2** | Dependencies: none

**RQ-017** — What level of detail is required for a cofferdam/tremie-pour minigame to feel technical without becoming a spreadsheet? *(ORQ #8)*  
Priority: **P2** | Dependencies: none

**RQ-018** — How can constrained Roblox asset kits imply history, decay, or abandonment without explicit exposition? *(DRQ #1)*  
Priority: **P1** | Dependencies: none

**RQ-019** — What role does camera perspective (first vs third person) play in reading environmental details at Roblox scale? *(DRQ #2)*  
Priority: **P2** | Dependencies: none

**RQ-020** — How can lighting and fog settings be tuned to suggest mood, time period, or unseen threats in a block-based world? *(DRQ #3, FWB Lighting)*  
Priority: **P1** | Dependencies: none

**RQ-021** — What are best practices for environmental clues that reward close inspection without frustrating mobile players? *(DRQ #8)*  
Priority: **P1** | Dependencies: none

**RQ-022** — How can repeatable procedural generation be reconciled with authored environmental storytelling in Roblox? *(DRQ #11)*  
Priority: **P2** | Dependencies: none

**RQ-023** — What UI conventions (journals, maps, inventories) best support environmental storytelling without breaking immersion? *(DRQ #14)*  
Priority: **P2** | Dependencies: none

**RQ-024** — How can a Roblox experience teach players to read its environment as a narrative system within the first few minutes? *(DRQ #15)*  
Priority: **P1** | Dependencies: RQ-018

---

## 2. TECHNICAL (CLOUDFLARE / WORKERS)

**RQ-025** — How should job claiming be implemented atomically in the Durable Object to prevent duplicate processing across multiple processor instances? *(GAP #6a, SHIP 0.3)*  
Priority: **P0** | Dependencies: none

**RQ-026** — What is the correct pruning strategy for the DO's SQLite store — alarm-based 24h sweep, size-based eviction, or migration to D1 for long-term history? *(GAP #6b, SHIP 0.4)*  
Priority: **P0** | Dependencies: RQ-025

**RQ-027** — Should the system use one global Durable Object ("default") or per-session DOs, and how does this affect concurrency and routing? *(GAP #6c)*  
Priority: **P1** | Dependencies: RQ-002

**RQ-028** — Should the push path (Worker → processor callback) be deleted entirely in favor of polling, or exposed via Cloudflare Tunnel? *(GAP #6d, SHIP 0.5)*  
Priority: **P0** | Dependencies: none

**RQ-029** — How should authentication be added to `lucineer-memory` and `lucineer-vector` services — shared-secret header, per-session token, or Cloudflare Access? *(GAP #4, SHIP 1.3)*  
Priority: **P0** | Dependencies: RQ-003

**RQ-030** — How should the `bond_level` upsert bug (silent reset to 0 on omitted field) be fixed — `COALESCE`, separate update path, or schema change? *(GAP #4)*  
Priority: **P1** | Dependencies: RQ-029

**RQ-031** — Should `lucineer-vector` use stable IDs (`skill-${slug}`) for all upserts to prevent duplicate vector accumulation? *(GAP A5)*  
Priority: **P1** | Dependencies: none

**RQ-032** — How should the vector seed endpoint batch embedding calls to avoid serial AI invocations within a single Worker request? *(GAP A5)*  
Priority: **P1** | Dependencies: none

**RQ-033** — What belongs in the `/api/diag` endpoint, and should it be behind auth or removed entirely? *(SHIP 1.3)*  
Priority: **P1** | Dependencies: RQ-029

**RQ-034** — How should the CORS policy on `lucineer-vector` be tightened from `*` to a specific origin whitelist? *(GAP #4)*  
Priority: **P0** | Dependencies: none

**RQ-035** — What is the correct D1 schema for tubes, grain entries, grain patterns, lineage chains, and colony dialect tables per the Integrated Architecture? *(IA Layer 0, PERSISTENCE_LAYER_DESIGN)*  
Priority: **P2** | Dependencies: none

**RQ-036** — How should the guano decay pipeline (FRESH → COMPOSTING → SOIL → SUBSTRATE → GEOLOGICAL) be implemented via Cron Triggers? *(IA Layer 0)*  
Priority: **P2** | Dependencies: RQ-035

**RQ-037** — Should real-time Bridge Protocol communication use Durable Object WebSockets, and what is the scaling strategy for concurrent sessions? *(IA §7, Layer 2)*  
Priority: **P2** | Dependencies: RQ-027

---

## 3. TECHNICAL (AI / ML)

**RQ-038** — Which persona constant is canonical for Lucineer, and how should it be enforced across all brain pipeline stages (fast, deep, coder, Hermes)? *(GAP #7, CB §0, ROAD Decision 5)*  
Priority: **P0** | Dependencies: none

**RQ-039** — Should `process_v2.py` invoke the brain with `--creative` flag to activate the Hermes personality stage, and how does this affect latency and cost? *(GAP #7, SHIP 2.1)*  
Priority: **P0** | Dependencies: RQ-038

**RQ-040** — How should the Hermes personality stage be prevented from corrupting build commands — strip commands from its output entirely, or accept only the `reply` field? *(GAP #7)*  
Priority: **P0** | Dependencies: RQ-039

**RQ-041** — How should the Nemotron-Content-Safety-3.5 stage be integrated into the brain pipeline, and what is the in-voice deflection pattern for unsafe output? *(GAP #5, SHIP 1.5)*  
Priority: **P0** | Dependencies: RQ-038

**RQ-042** — What is the correct token budget for the fast path — is 1024 tokens sufficient for 5-8 command builds with hex colors and vector positions? *(GAP #7)*  
Priority: **P1** | Dependencies: none

**RQ-043** — How should the brain pipeline's planner fallback chain be capped — two models instead of five — to bound worst-case latency? *(GAP #8a)*  
Priority: **P1** | Dependencies: none

**RQ-044** — What is the correct timeout hierarchy — brain budget, DEEP_TIMEOUT, POLL_TIMEOUT — and how should they be ordered to prevent client-side abandonment? *(GAP #8a)*  
Priority: **P0** | Dependencies: none

**RQ-045** — Should build results be cached by hash of `(normalized_message, style, scale)` with 24h TTL, re-rolling only the reply text? *(GAP #8c)*  
Priority: **P1** | Dependencies: none

**RQ-046** — How should the memory service be wired into the processor — what context (bond level, recent builds, preferences) is injected into the prompt? *(GAP #4, ROAD Tier 3)*  
Priority: **P1** | Dependencies: RQ-029

**RQ-047** — How should the vector service be queried for semantic skill recall, and what score threshold filters irrelevant matches? *(GAP #4)*  
Priority: **P1** | Dependencies: RQ-029

**RQ-048** — How should keyword matching be fixed to use word-boundary regex, longest-match-wins, and build-verb requirement instead of naive substring matching? *(GAP A3)*  
Priority: **P0** | Dependencies: none

**RQ-049** — What is the correct progressive feedback model — immediate in-voice acknowledgment before brain runs, then build-progress narration? *(GAP #8b, ROAD Tier 3)*  
Priority: **P1** | Dependencies: RQ-038

**RQ-050** — How should the anti-pattern rejection pass work — regex matching against known bad patterns, model-based classification, or both? *(CB §10)*  
Priority: **P1** | Dependencies: RQ-038

**RQ-051** — How should `bond_level` be read and injected into the persona prompt to select the correct bond tier behavioral block? *(CB §9)*  
Priority: **P1** | Dependencies: RQ-046

**RQ-052** — What memory model should NPCs have of past wrecks, storms, and salvage so dialogue evolves without hand-authored branches? *(ORQ #11)*  
Priority: **P2** | Dependencies: RQ-046

**RQ-053** — How can a game train players to read bird posture and flight pattern as navigation/fishing aid, the way experienced mariners read water color? *(ORQ #10)*  
Priority: **P3** | Dependencies: none

**RQ-054** — How should flocking behavior convey information (food location, danger, weather change) rather than visual noise? *(ORQ #9)*  
Priority: **P2** | Dependencies: none

**RQ-055** — How should the GrainStore accumulate tool-usage wisdom (context_matcher + confidence + success_rate) across sessions? *(IA Layer 1, CHISEL_PATTERN_DESIGN)*  
Priority: **P2** | Dependencies: RQ-035

**RQ-056** — What embedding model and dimensionality should be used for grain pattern semantic search — bge-m3 via Vectorize, or a custom model? *(IA §7)*  
Priority: **P2** | Dependencies: RQ-055

**RQ-057** — How should the five-model pipeline be restructured for production — which models are deep-path vs fast-path, and what is the cost per request? *(TOOLS.md, ROUNDTABLE_BRIEF)*  
Priority: **P1** | Dependencies: none

**RQ-058** — How should the system detect and represent animal knowledge of "wrong" places (the cove gulls avoid) without anthropomorphizing? *(ORQ #12)*  
Priority: **P3** | Dependencies: RQ-054

---

## 4. DESIGN (GAME) — GAMEPLAY, MECHANICS, PROGRESSION, ECONOMY

**RQ-059** — Is the `BondSystem` a progression mechanic or a relationship simulation, and should the current XP ladder be rewritten as behavior-triggered events? *(GAP #7, SHIP 2.4, ROAD Decision 3)*  
Priority: **P0** | Dependencies: RQ-051

**RQ-060** — What are the specific behavior triggers (flaw callout, pushback, continuation) that advance bond, and how are they detected from player actions? *(CB §4)*  
Priority: **P1** | Dependencies: RQ-059

**RQ-061** — How should "finished something Lucineer left unfinished" be detected — bounding-box observation of new player parts within an open hook? *(CB §4)*  
Priority: **P1** | Dependencies: RQ-059

**RQ-062** — What is the correct tide cycle length — 18 minutes (SHIP spec, tutorial) or 20 minutes (TideSystem implementation)? *(SHIP 3.2)*  
Priority: **P1** | Dependencies: none

**RQ-063** — How can "tide windows" be represented as a renewable but strictly limited resource without making the player feel cheated by the clock? *(ORQ #1)*  
Priority: **P1** | Dependencies: RQ-062

**RQ-064** — How should a game model the transition from slack tide to flood tide so water feels like a living constraint rather than a binary timer? *(ORQ #6)*  
Priority: **P2** | Dependencies: RQ-062

**RQ-065** — What mechanics make "what to save and what to leave" a meaningful choice in a salvage scenario, rather than an optimal-loot puzzle? *(ORQ #13)*  
Priority: **P2** | Dependencies: none

**RQ-066** — How can a game reward documentation, measurement, and restraint as highly as extraction and conquest? *(ORQ #14)*  
Priority: **P2** | Dependencies: none

**RQ-067** — What systems discourage stripping a wreck for parts while still making repair and reconstruction viable playstyles? *(ORQ #15)*  
Priority: **P2** | Dependencies: none

**RQ-068** — How should the legal/moral ambiguity of salvage rights be surfaced without delivering a lecture? *(ORQ #16)*  
Priority: **P2** | Dependencies: none

**RQ-069** — What is the correct per-player rate limit — 3s cooldown, concurrent job cap, or daily quota — and how should it be enforced? *(GAP #5, SHIP 1.6)*  
Priority: **P0** | Dependencies: none

**RQ-070** — How should the tutorial's first 30 minutes be structured — is the cinematic beam-carry the right onboarding, and what happens if a player refuses? *(SHIP 3.1, FWB §2)*  
Priority: **P1** | Dependencies: none

**RQ-071** — What are Era 1→2 gate requirements, and how should era progression be validated — crafting milestones, build count, or narrative triggers? *(SHIP 3.3, ERA_TRANSITIONS)*  
Priority: **P1** | Dependencies: none

**RQ-072** — What does the save system persist — player builds, bond level, world state, conversation history — and how does it survive across sessions? *(SHIP 3.3)*  
Priority: **P1** | Dependencies: RQ-029

**RQ-073** — What are the "Magic Moments" 1-5 implementation priorities, and which can be faked for MVP vs requiring full systems? *(SHIP 3.4, CB §5)*  
Priority: **P1** | Dependencies: RQ-059

**RQ-074** — How should `markUnfinished` work as a mechanic — every build leaves one deliberate gap, tagged as a structured intent for player completion? *(CB §6, SHIP 2.3)*  
Priority: **P1** | Dependencies: none

**RQ-075** — What is the correct performant way to simulate wet concrete curing (temperature, salinity, current shear) without overwhelming the player? *(ORQ #5)*  
Priority: **P2** | Dependencies: none

**RQ-076** — How do you proceduralize the vocabulary of a specialized craft (shipwright, diver, gull-watcher) so NPC dialogue sounds authentic without repetition? *(ORQ #3)*  
Priority: **P2** | Dependencies: none

**RQ-077** — What is the minimum set of observable behaviors needed for non-player species (gulls, whales, fish) to make players infer ecological cause and effect? *(ORQ #4)*  
Priority: **P2** | Dependencies: RQ-054

**RQ-078** — How should the Seven Courts (I-VII) be implemented as progressive collaboration complexity tiers, and which court is the minimum viable? *(IA §5, §6)*  
Priority: **P3** | Dependencies: none

**RQ-079** — Should player gamification use "Attention" as the only currency with an Unpredictability Index, and how is that measured without a leaderboard? *(IA Layer 4, PLAYER_GAMIFICATION)*  
Priority: **P2** | Dependencies: none

**RQ-080** — Which systems are worth building generically (tides, weather, flocking, material curing) vs hand-authored per scenario? *(ORQ #20)*  
Priority: **P1** | Dependencies: none

---

## 5. DESIGN (CHARACTER) — LUCINEER PERSONALITY, VOICE, BEHAVIOR

**RQ-081** — Which hardcoded client strings need deletion — "Done! I built %d action(s) for you." and "Hi! I'm Lucineer" — and what replaces them? *(GAP #7, SHIP 2.6, CB §10)*  
Priority: **P0** | Dependencies: RQ-038

**RQ-082** — Should `UI_THINKING_TEXT` ("Lucineer is thinking...") be deleted and replaced with physical acknowledgment behavior? *(SHIP 2.2)*  
Priority: **P1** | Dependencies: RQ-049

**RQ-083** — How should Lucineer's fourth-wall response ("Are you an AI?") be handled — canned canonical answers, or model-generated within constraints? *(CB §6)*  
Priority: **P1** | Dependencies: RQ-038

**RQ-084** — What are the seven canonical arguments Lucineer will have, and under what conditions does he lose each one? *(CB §7)*  
Priority: **P1** | Dependencies: RQ-038

**RQ-085** — How should the "Alaska rule" be enforced in generation — one Southeast Alaska reference per 4-5 lines, always as work comparison, never scenery? *(CB §2)*  
Priority: **P1** | Dependencies: RQ-038

**RQ-086** — How should the "Magnus rule" be handled — quoted as mentor authority, never explained, referenced at bond tier 1+? *(CB §2)*  
Priority: **P1** | Dependencies: RQ-051

**RQ-087** — Is the dream-weaver persona (`LUCINEER_PERSONA` at brain.py:76) fully deleted, or archived as an alternate personality for future use? *(CB §0)*  
Priority: **P0** | Dependencies: RQ-038

**RQ-088** — How should Lucineer's idle behavior be implemented — standing at the anvil, wandering to the Unfinished Wall, standing in the seaward doorway at slack tide? *(FWB §4 NPC placement)*  
Priority: **P2** | Dependencies: none

**RQ-089** — How should the returning-player line be generated — referencing their last build, its location, and whether it's still standing? *(CB §4 bond decay)*  
Priority: **P1** | Dependencies: RQ-046

---

## 6. DESIGN (WORLD) — LORE, ENVIRONMENT, NARRATIVE

**RQ-090** — How should the Channel (the space between dead game engines) be represented visually — fog boundary, lighthouse beam radius, or both? *(FWB §1)*  
Priority: **P1** | Dependencies: RQ-020

**RQ-091** — What happens when a player walks into the fog — thickening, sound fall-off, emergence at tideline? Is there ever content past the fog? *(FWB §1 world rules)*  
Priority: **P1** | Dependencies: RQ-090

**RQ-092** — How should the tide restock the beach — generic salvage, engine-flavored relics, and personalized returns (deleted player builds)? *(FWB §1, SHIP 3.2)*  
Priority: **P1** | Dependencies: RQ-062

**RQ-093** — What is the spawn terrain authoring plan — does the ground near spawn need to be sloped to make Magic Moment 1 (The Siting) work? *(CB §5 MM1, POLISH_PLAN §2)*  
Priority: **P1** | Dependencies: none

**RQ-094** — How should the five NPCs (Earl, Spark, Hermes, Bea, Forty-Eight) be implemented — scripted loops, state machines, or AI-driven behavior? *(FWB §3)*  
Priority: **P2** | Dependencies: none

**RQ-095** — What is Forty-Eight's exact-count behavior specification — 48 objects in hoard, exact-count theft, and how does the trade-back system work? *(FWB §3)*  
Priority: **P2** | Dependencies: RQ-094

**RQ-096** — How should the lighthouse beam function as both narrative device and render-distance boundary — 40-second sweep cycle, visual effect on fog? *(FWB §4 Lighting)*  
Priority: **P1** | Dependencies: RQ-090

**RQ-097** — How should diegetic narration (logbooks, charts, overheard dialogue) be balanced against expository text in discovery-heavy gameplay? *(ORQ #19)*  
Priority: **P2** | Dependencies: none

**RQ-098** — How do players collaboratively construct meaning from environmental clues in multiplayer Roblox experiences? *(DRQ #13)*  
Priority: **P2** | Dependencies: none

**RQ-099** — What methods exist for encoding lore into interactive objects (tools, doors, machines) that players must use rather than observe? *(DRQ #10)*  
Priority: **P2** | Dependencies: none

**RQ-100** — How should the *Capitaine*'s schedule (dawn/dusk port calls, fog departures) work as a content delivery mechanism? *(FWB §4)*  
Priority: **P2** | Dependencies: none

---

## 7. INFRASTRUCTURE — DEPLOYMENT, SCALING, MONITORING, COST

**RQ-101** — Should the processor run under systemd with auto-restart, or as a managed daemon, and what is the correct supervision policy? *(GAP A2, SHIP 4.4)*  
Priority: **P0** | Dependencies: none

**RQ-102** — Should the old processor variants (`process.py`, `process-jobs.sh`) be deleted in favor of a single `process_v2.py`? *(GAP A2)*  
Priority: **P0** | Dependencies: none

**RQ-103** — What is the computed per-player-hour cost, and how should billing alarms be configured on DeepInfra and Cloudflare? *(SHIP 4.1)*  
Priority: **P1** | Dependencies: none

**RQ-104** — What five metrics should be on the operations dashboard — job latency, error rate, model cost, active sessions, queue depth? *(SHIP 4.2)*  
Priority: **P1** | Dependencies: none

**RQ-105** — How should trajectory logging to R2 in MOLT `Result` format be implemented, and what fields are captured per job? *(SHIP 4.3)*  
Priority: **P1** | Dependencies: none

**RQ-106** — How should per-player conversation logs be queryable while maintaining privacy and COPPA compliance? *(SHIP 4.5)*  
Priority: **P1** | Dependencies: RQ-029

**RQ-107** — What is the kill-switch design — fallback to template-only mode if the brain pipeline is down or over budget? *(SHIP 4.5)*  
Priority: **P1** | Dependencies: none

**RQ-108** — Should the project use a single `PROTOCOL.md` with example payloads for all six API endpoints to prevent contract drift between TypeScript and Luau? *(GAP #2)*  
Priority: **P0** | Dependencies: none

**RQ-109** — How should log rotation be handled for `processor.log` (currently 10,446+ lines with no rotation)? *(GAP A2)*  
Priority: **P1** | Dependencies: RQ-101

**RQ-110** — What is the correct CI/CD pipeline — automated Rojo build, wrangler deploy, smoke test on every commit? *(ROAD, SHIP 0.2)*  
Priority: **P1** | Dependencies: RQ-010

**RQ-111** — What is the 30fps-on-mid-tier-phone target, and how many concurrent players (16?) can the current part-creation rate sustain? *(SHIP 3.5)*  
Priority: **P1** | Dependencies: none

---

## 8. ART / AUDIO — VISUAL STYLE, SOUND DESIGN, MUSIC

**RQ-112** — What audio cues communicate tidal state before the player consciously registers water level or current? *(ORQ #17)*  
Priority: **P2** | Dependencies: none

**RQ-113** — How much of the game's mood should depend on weather, and what procedural audio tools keep storms from becoming tedious or trivial? *(ORQ #18)*  
Priority: **P2** | Dependencies: none

**RQ-114** — What is the ambient sound bed specification — tide under cannery floor, halyard clink, gull/raven traffic, rain on tin, forge hammer rhythm? *(FWB §4 Ambient sound)*  
Priority: **P1** | Dependencies: none

**RQ-115** — How should the lighthouse beam sweep be synchronized with the visual and audio metronome — 40-second cycle across the whole hub? *(FWB §4 Lighting)*  
Priority: **P1** | Dependencies: RQ-096

**RQ-116** — How should the forge lighting (warm orange core pulsing with bellows cycle, spilling through plank gaps) be authored in Roblox? *(FWB §4 Lighting)*  
Priority: **P1** | Dependencies: RQ-020

**RQ-117** — What is the visual style guide for "nothing matches and everything fits" — corrugated tin, bulkhead steel, mixed-wood boardwalk, roller-coaster-track handrails? *(FWB §1, §4)*  
Priority: **P1** | Dependencies: RQ-018

**RQ-118** — How should the aurora event (rare nights, all warm light killed for two minutes) be implemented in Roblox Atmosphere/Lighting? *(FWB §4, CB §5 MM4)*  
Priority: **P2** | Dependencies: RQ-020

**RQ-119** — What music approach is correct — no music in hub except first-control string note, storm work-song, and aurora silence? *(FWB §4 Ambient sound)*  
Priority: **P2** | Dependencies: RQ-114

**RQ-120** — How should the opening cinematic (60-second unbroken camera move, fog to forge) be authored — Roblox Camera manipulation, or pre-rendered cutscene? *(FWB §2)*  
Priority: **P1** | Dependencies: none

---

## SUMMARY STATISTICS

| Priority | Count |
|----------|-------|
| **P0** (blocks MVP) | **24** |
| **P1** (needed for launch) | **43** |
| **P2** (post-launch) | **36** |
| **P3** (future) | **4** |
| **Ambiguous/undated** | **0** |
| **Total** | **107** → **120** |

*Note: Some questions span multiple priorities depending on scope decisions. Counts reflect the highest applicable priority.*

| Category | Count |
|----------|-------|
| Technical (Roblox/Lua) | 24 |
| Technical (Cloudflare/Workers) | 13 |
| Technical (AI/ML) | 21 |
| Design (Game) | 22 |
| Design (Character) | 9 |
| Design (World) | 11 |
| Infrastructure | 11 |
| Art/Audio | 9 |
| **Total** | **120** |

---

## CROSS-REFERENCE: P0 CRITICAL PATH

These 24 P0 questions must be resolved before the MVP can ship:

| RQ | Question (short) | Source |
|----|-------------------|--------|
| RQ-001 | Command envelope params dispatch | GAP #1 |
| RQ-002 | Session identity format | GAP #2 |
| RQ-003 | Client-side secret storage | GAP #3 |
| RQ-004 | Delete runLua/addScript | GAP #9 |
| RQ-006 | TextChatService vs legacy | GAP #9d |
| RQ-010 | Consolidate Lua source trees | GAP A1 |
| RQ-025 | Atomic job claiming | GAP #6a |
| RQ-026 | DO storage pruning | GAP #6b |
| RQ-028 | Delete or fix push path | GAP #6d |
| RQ-029 | Auth on memory/vector services | GAP #4 |
| RQ-034 | Vector CORS lockdown | GAP #4 |
| RQ-038 | Canonical persona constant | GAP #7 |
| RQ-039 | --creative flag in production | GAP #7 |
| RQ-040 | Hermes can't emit commands | GAP #7 |
| RQ-041 | Nemotron safety stage | GAP #5 |
| RQ-044 | Timeout hierarchy | GAP #8a |
| RQ-048 | Keyword matching fix | GAP A3 |
| RQ-059 | BondSystem rewrite | SHIP 2.4 |
| RQ-069 | Per-player rate limit | GAP #5 |
| RQ-081 | Delete off-voice strings | SHIP 2.6 |
| RQ-087 | Delete dream-weaver persona | CB §0 |
| RQ-101 | Processor under systemd | GAP A2 |
| RQ-102 | Delete old processor variants | GAP A2 |
| RQ-108 | PROTOCOL.md shared schema | GAP #2 |

---

*End of Master Research Questions. 120 questions. 24 P0. The castle is 21 hours away. Everything else is noise.*
