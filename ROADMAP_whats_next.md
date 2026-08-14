# ROADMAP: What's Next

## Slackwater/Lucineer — From Architecture to Game

**Date:** 2026-08-03
**Audience:** Casey + build agents
**Method:** Full source scan of all implementations + cross-reference with every design doc

---

## 1. CURRENT STATE ASSESSMENT

### What Actually Exists and Works

**The brutal summary:** The project has 400,000+ words of design documentation, 36,000 lines of Lua (38 modules), a working Cloudflare Worker relay, a Durable Object with a correct lease-based job queue, a deployed D1 database, a 35-skill Vectorize index, a five-model brain pipeline, and seven Rust crates implementing the Slackwater mathematical substrate. It has processed four real jobs in its lifetime. Zero have reached a player.

**What works end-to-end:** Nothing. The loop from "player types message" → "AI processes" → "build appears in game" → "character replies" has never completed. The GAP_ANALYSIS and SHIP_READINESS docs document why: contract mismatches at every boundary, zero integration tests, and a build tree that historically shipped 9% of the code.

**What has been fixed since the audits:** The `default.project.json` now includes all 38 modules (not just 9). The `Config.AUTH_KEY` issue was addressed by removing auth from the inbound endpoint. The `runLua` command was removed. `ServerConfig.lua` exists. `FilterGate.lua` has been written (113 lines). These are real improvements.

**What remains broken:** The core loop still doesn't close. Memory and vector services are still unwired. The persona is still "friendly assistant" not Lucineer. `BondSystem` is still an XP ladder. `markUnfinished` still doesn't exist. The text filter (`FilterGate`) exists as a module but the server doesn't route through it. The processor still doesn't claim jobs. There is still no smoke test.

### Component Health Matrix

| Component | Lines | Deployed | Wired In | Actually Works |
|-----------|-------|----------|----------|----------------|
| **Worker relay** (`index.ts`) | 344 | ✅ Live | Partial | Creates jobs; auth gutted; push path broken |
| **Durable Object** (`LucineerSession.ts`) | 570 | ✅ Live | Partial | Claim endpoint exists but unused; no alarm sweep |
| **Brain pipeline** (`brain.py`) | 1,207 | Local | ❌ Not wired | `--creative` flag never used in production; persona is wrong |
| **Processor** (`process_v2.py`) | 1,487 | Running as daemon | Partial | Polls and processes but doesn't claim; keyword matching is broken |
| **Memory service** (`index.ts`) | 360 | ✅ Live | ❌ Zero call sites | Deployed, healthy, open to the internet, called by nothing |
| **Vector service** (`index.ts`) | 232 | ✅ Live | ❌ Zero call sites | 35 skills indexed, never queried |
| **Roblox client** (38 modules) | 36,244 | In project file | Partial | All modules now in build; most never loaded by a running game |
| **Rust substrate** (7 crates) | 3,786 + stubs | Libraries only | ❌ Not integrated | `flux-core`, `harmony-core`, `lattice-core` are real; 4 are stub files |
| **Templates** (`build_templates_v2.py`) | 495 | Embedded in processor | Partial | 17 templates exist; params dispatch bug may persist |

---

## 2. DESIGN → IMPLEMENTATION GAP MATRIX

| Design Document | Implementation Status | % Done | What's Missing |
|-----------------|----------------------|--------|----------------|
| **INTEGRATED_ARCHITECTURE.md** (master wiring) | ~15% | 15% | Most layers exist as code but are not connected. The "wiring diagram" is on paper, not in code. No data flow path has been verified end-to-end. |
| **GAP_ANALYSIS.md** (6 P0 bugs) | ~50% fixed | 50% | Project file fixed (#A1). Params dispatch may persist (#1). API contracts partially addressed (#2). Key handling partial (#3). Memory still unwired (#4). No text filter in path (#5). Job claiming still not called (#6). |
| **FABLE_GRAND_PLAN.md** (12-layer stack) | Phase 1 partially started | 10% | Layers 1-2 (FLUX/SWMIDI) exist in Rust but aren't integrated. Layer 3 (Tempo) is a stub. Layers 4-7 (Lattice/T-Minus/Harmony/Perception) are stubs or nonexistent in the running system. Layer 9 (pipeline) exists but with wrong persona. The 90-day plan is day 2 of a 90-day sprint. |
| **BUILD_SEQUENCE.md** (team assignments) | Obsolete | 0% | Assigns work to coding agents (KimiCode, OpenCode, etc.) that aren't being used this way. The layer ordering is still valid but the team model doesn't match reality. |
| **SHIP_READINESS.md** (29 checklist items) | 1 DONE, ~8 IN PROGRESS | 10% | Of 29 items, 1 is done (no key in client), ~8 are in progress, ~20 are blocked. Gates 0-4 are all blocked. |
| **CHISEL_PATTERN_DESIGN.md** (tool wisdom) | Not started | 0% | Zero grain store tables. Zero chisel wrappers. The design is thorough and the API is specified, but nothing is built. Not needed for MVP. |
| **BRIDGE_PROTOCOL_DESIGN.md** (agent comms) | Not started | 0% | No Bridge sessions, no seven-note contributions, no Dance Floor. The TypeScript interfaces are specified but unimplemented. Not needed for MVP. |
| **PERSISTENCE_LAYER_DESIGN.md** (memory hierarchy) | ~5% | 5% | D1 tables for tubes/grain/lineage don't exist. The guano decay pipeline isn't built. Memory and vector services exist but have no callers. The design for session memory exists conceptually. |
| **SWARM_INTELLIGENCE_ARCHITECTURE.md** (multi-agent) | Not started | 0% | No puffin calls, no hex lattice routing, no jam protocol. This is a post-MVP system. The design is thorough. |
| **PLAYER_GAMIFICATION.md** (attention economy) | ~5% | 5% | BondSystem exists but implements the *opposite* of the design (XP ladder vs. attention economy). No unpredictability index. No resonance profile. No Skipper quests. |
| **AGENT_GAMIFICATION.md** (five measures) | Not started | 0% | No grain audits, no bridge scores, no flow streaks, no lineage trees, no mastery profiles. Post-MVP. |

### The Honest Percentage

If you weight by "what's needed to ship a playable MVP":
- **Infrastructure needed for MVP:** ~40% complete (Worker, DO, D1, brain, processor, Lua modules all exist in some form)
- **Integration of that infrastructure:** ~5% complete (almost nothing is wired together correctly)
- **Design completeness for MVP scope:** ~300% over-specced (the design docs cover systems that won't be built for a year)

**Effective project completion toward a playable game: ~10%.**

---

## 3. THE CRITICAL PATH TO PLAYABLE

### What "Playable" Means

A player joins, types "build me a castle," and within 60 seconds sees a castle appear, part by part, while a character named Lucineer says something in voice. That's it. Everything else is decoration on this moment.

### The Minimum Viable Loop

```
1. Player types message → it reaches the Worker (not 400/401)
2. Worker creates job → processor claims it (not double-processing)
3. Brain runs → produces build commands + a voice line (not "friendly assistant")
4. Commands return to client → parts appear at player's location (not at origin)
5. Voice line displays → filtered through Roblox text filter (not raw AI output)
6. Build animates → parts land with stagger and sound (not all at once)
```

### What It Takes to Get There

| Step | What's Needed | Est. Hours | Status |
|------|---------------|------------|--------|
| 1 | Fix API contract: `sessionId` in payload, align field names | 3h | **Partially done** — ServerConfig exists, need to verify alignment |
| 2 | Wire processor to call `claimJob` before processing | 2h | Endpoint exists, one HTTP call needed |
| 3 | Fix params dispatch in CommandExecutor (if still broken) | 1h | May still be the `command.params` vs `command` bug |
| 4 | Route brain through `--creative` flag with correct persona | 2h | Constant exists in brain.py, flag not in process_v2.py invocation |
| 5 | Delete "Done! I built %d action(s)" and use brain reply | 1h | Client-side string replacement |
| 6 | Route all AI text through FilterGate before display | 2h | Module exists (113 lines), not called from server |
| 7 | Stagger build animation (even simple `task.wait(0.08)`) | 1h | One loop modification |
| 8 | First Studio smoke test: type message → see build → see reply | 2h | This is verification, not building |
| 9 | Fix what the smoke test breaks | 4h | Budget for reality |
| 10 | Add Nemotron safety stage to brain pipeline | 2h | Specified in design, zero code |
| 11 | Per-player rate limit in ChatHandler | 1h | Currently no throttle at all |

**Total critical path: ~21 hours of focused work.**

That's three days at a sane pace. Not three weeks. Not three months. The infrastructure exists. The seams are wrong. Fixing seams is cheap.

---

## 4. RANKED BUILD QUEUE

Top 20 tasks, ranked by **impact ÷ effort** ratio (highest first).

### Tier 1: The Core Loop (do these first or nothing else matters)

| # | Task | Design Doc | Effort | Unblocks | Depends On |
|---|------|-----------|--------|----------|------------|
| 1 | **Fix API contracts** — align `sessionId`, field names between Lua and TypeScript | GAP #2 | 3h | Anything reaching the Worker | — |
| 2 | **Wire job claiming** — add `POST /api/job/:id/claim` call in `process_v2.py` | GAP #6a | 2h | No duplicate processing, no infinite loops | #1 |
| 3 | **Fix params dispatch** — verify `command.params` flows through to handlers | GAP #1 | 1h | Builds look like builds, not gray boxes | — |
| 4 | **Route through correct persona** — `--creative` flag, one persona constant, delete "friendly" | GAP #7 | 2h | The character exists | — |
| 5 | **Delete off-voice strings** — remove "Done! I built %d action(s)", use brain reply | SHIP_READINESS 2.6 | 1h | Character speaks in voice | #4 |
| 6 | **Route through FilterGate** — all AI text passes `FilterStringAsync`, fail-closed | GAP #5 | 2h | Safe to show AI text to players | — |
| 7 | **Studio smoke test** — script that drives one message through the full stack | FABLE §4 | 2h | Truth about what works | #1-6 |
| 8 | **Delete push path** — remove the broken `await fetch(callback)` from Worker | GAP #6d | 0.5h | No more 502s on job creation | — |

### Tier 2: Safety and Sound (required before any player)

| # | Task | Design Doc | Effort | Unblocks | Depends On |
|---|------|-----------|--------|----------|------------|
| 9 | **Nemotron safety stage** — model check on final reply, in-voice deflection | GAP #5 | 2h | Kid-safe output | #4 |
| 10 | **Per-player rate limit** — 3s cooldown in ChatHandler + server job cap | GAP #5 | 1h | Can't burn unlimited DeepInfra credit | #1 |
| 11 | **Auth on memory + vector services** — shared-secret header | GAP #4 | 1h | Safe to wire memory | — |
| 12 | **Fix timeout inversion** — `POLL_TIMEOUT` > `DEEP_TIMEOUT` > brain budget | GAP #8a | 0.5h | Player doesn't give up before brain finishes | — |

### Tier 3: Depth That Matters

| # | Task | Design Doc | Effort | Unblocks | Depends On |
|---|------|-----------|--------|----------|------------|
| 13 | **Wire memory service** — player profiles, build history, conversation log into processor | GAP #4 | 6h | Character remembers; Day-2 callbacks | #11 |
| 14 | **Wire vector service** — semantic skill recall in brain pipeline | GAP #4 | 3h | Better build quality; pattern reuse | #11 |
| 15 | **Stagger build animation** — parts land progressively, not all at once | FABLE §2 | 1h | Feels like building, not texture pop-in | #3 |
| 16 | **Add `markUnfinished`** — every build leaves one deliberate gap | CHARACTER_BIBLE §6 | 3h | The thesis mechanic exists | #4 |
| 17 | **Rewrite BondSystem** — XP ladder → behavior triggers; keep voice lines | SHIP_READINESS 2.4 | 4h | Character relationship is alive, not instrumented | #4 |
| 18 | **Progressive feedback** — immediate in-voice ack before brain runs | GAP #8b | 2h | No dead air during 40s builds | #4 |

### Tier 4: Polish That Elevates

| # | Task | Design Doc | Effort | Unblocks | Depends On |
|---|------|-----------|--------|----------|------------|
| 19 | **Delete `addScript`** — remove the runtime-injectable script command | GAP #9b | 0.5h | No arbitrary code execution path | — |
| 20 | **Fix keyword matching** — word boundaries, longest match, negation detection | GAP A3 | 1h | "take me home" doesn't build a house | — |

---

## 5. QUICK WINS (<2 hours each, visible improvement)

### 1. Delete the push path (30 min)
The `await fetch(OPENCLAW_CALLBACK_URL)` at `index.ts:96-125` points at a private WSL IP and cannot work. Every message creates a 502 before the poll path saves it. Deleting those lines and returning the job response immediately removes a source of errors that masks real bugs. **Impact:** eliminates phantom 502s; simplifies debugging.

### 2. Fix the timeout inversion (30 min)
`Config.lua:17`: `POLL_TIMEOUT = 60`. `process_v2.py:32`: `DEEP_TIMEOUT = 120`. The client gives up before the brain finishes. Flip the numbers: brain budget 90s, processor 100s, client 120s. **Impact:** deep builds that currently succeed server-side but appear as failures to the player will start appearing as successes.

### 3. Delete "Done! I built %d action(s) for you." (15 min)
`LucineerClient/init.lua:85`. Replace with: use the brain's reply text (the `reply` field from the job result). This is the single line most directly responsible for making the product feel like a generic assistant instead of a character. **Impact:** the character speaks.

### 4. Delete `addScript` and its dispatch entry (30 min)
`CommandExecutor.lua:313` and its `commandMap` entry at line 404. `Script.Source` can't be assigned at runtime; it always fails silently. Removing it eliminates a code injection vector and a class of silent failures. **Impact:** cleaner command surface; one fewer silent failure path.

### 5. Fix keyword substring matching (1h)
`process_v2.py:299`: "keep it small" → builds a castle (`'keep'` matches). Word-boundary regex matching with longest-match-wins eliminates the most absurd misroutes. **Impact:** player messages that aren't build requests stop accidentally triggering builds.

---

## 6. ARCHITECTURE DECISIONS NEEDED

These are not technical questions. They are product and direction decisions that Casey must make before more building happens. Each one has a technical implication, but the decision itself is human.

### Decision 1: What ships first — single-agent or multi-agent?

**The design envisions a world with multiple AI agents (Earl, Spark, Bea, Hermes, Forty-Eight) collaborating through Bridge Protocol.** The architecture for this is beautiful, thoroughly documented, and 0% implemented. Building it is a 3-6 month effort.

**The alternative:** Ship with one agent (Lucineer) who does everything. The brain pipeline already produces builds. The character bible already defines the voice. The BondSystem (once rewritten) defines the relationship arc. This is shippable in weeks, not months.

**My recommendation:** Ship single-agent. The Bridge Protocol, Swarm Intelligence, puffin calls, seven-note jams, and courts IV-VII are the most exciting parts of this design — and they are also the parts most likely to kill the project if attempted before the core loop works. Build the chapel with the organist. Add the choir later.

**What this means concretely:** Stop designing multi-agent systems. The CHISEL_PATTERN_DESIGN, BRIDGE_PROTOCOL_DESIGN, SWARM_INTELLIGENCE_ARCHITECTURE, and AGENT_GAMIFICATION docs should be filed as "Phase 2 design references" and not consulted again until the single-agent game works end-to-end and has real players.

### Decision 2: How much of the Slackwater substrate is needed for MVP?

The Grand Plan specifies 12 layers. Three Rust crates (`flux-core`, `harmony-core`, `lattice-core`) are real implementations of layers 1, 2, and 6. Four more crates (`perception-core`, `swmidi`, `tempo-core`, `tminus-core`) are stubs. The tempo system is on PyPI.

**The question:** Does the MVP need Eisenstein lattice placement, SWMIDI event packing, the Harmony Governor's Φ computation, and the T-Minus prediction engine? Or can the MVP use regular Vector3 positions, JSON commands, a simple "is the player frustrated?" heuristic, and HTTP polling?

**My recommendation:** The MVP does not need any of the Rust substrate. The substrate is beautiful engineering. It is also the most sophisticated solution to problems the game does not yet have. A player typing "build me a castle" does not benefit from hex-lattice coordinate snapping. They benefit from a castle appearing at their location, with a character who says something interesting.

**What this means concretely:** The Rust crates should be maintained as a research track but not integrated into the shipping product until the shipping product works without them. The JSON command envelope is fine. Regular Vector3 positions are fine. Polling is fine. The substrate can replace these incrementally once the game is live and the substrate's value can be measured rather than assumed.

### Decision 3: Is the BondSystem a progression mechanic or a relationship simulation?

The design says bond is measured by behavior triggers (flaw callout, pushback, continuation) and never shown as a number. The current implementation is an XP ladder with level-up lines. The SHIP_READINESS correctly identifies this as the largest piece of *wrong* work — it's not missing, it's mistaken.

**The question:** Rewrite it now, or ship the XP ladder and rewrite later?

**My recommendation:** Rewrite now, but simply. The behavior-triggered version is actually *less* code than the XP ladder: a few event handlers (onFlawCallout, onPushback, onContinuation) that adjust a hidden bond value and trigger voice lines at thresholds. The XP ladder is 626 lines. The replacement should be ~200. Ship the simpler version.

### Decision 4: How much gameplay before the first external playtest?

The SHIP_READINESS says Gate 3 (It's a Game) requires: first 30 minutes completable, tide restocks, era gates, save system, magic moments, 30fps on mid-phone, 16 players, Roblox compliance.

**The question:** Is all of that needed before *anyone* outside the team plays? Or can you get value from putting the core loop in front of a friend with none of the progression systems?

**My recommendation:** Two playtest tiers:
- **Week 1-2:** "Core loop playtest" — friends type build requests, see things appear, hear Lucineer talk. No tutorial, no tide, no era gates, no save. This tests whether the magic moment works. It's the most important test in the project.
- **Week 3-4:** "First 10 minutes playtest" — add tutorial, tide, and basic crafting. This tests whether the game has legs beyond the initial trick.

Do not wait for Gate 3 completeness to do the first playtest. The design docs are detailed enough to create the illusion that the game exists. Only a real player destroys that illusion.

### Decision 5: The persona problem — which Lucineer ships?

The Character Bible defines Lucineer as a gruff foreman who always leaves something unfinished. The brain pipeline's `SYSTEM_FAST` says "friendly one or two sentence message." `SYSTEM_CODER` says the same. The Hermes persona (`LUCINEER_PERSONA`) describes a poetic dream-weaver. `process_v2.py` invokes without `--creative`, so the Hermes persona never runs.

**The question:** Which voice is canonical?

**My recommendation:** The Character Bible is canonical — that's why it's called the Bible. The gruff foreman who leaves things unfinished is the character. "Friendly" is the enemy. The poetic dream-weaver is a different character entirely. Pick the foreman, write him into the brain pipeline as the only persona constant, and make every model stage reference it. This is a 2-hour fix that changes the entire feel of the product.

---

## CLOSING ASSESSMENT

### The Good News

The infrastructure is real. The Worker is deployed. The D1 database is provisioned. The Vectorize index has 35 skills. The brain pipeline has five models. The Lua codebase has 36,000 lines across 38 modules, all now in the build tree. The Rust substrate has three working crates. The design documentation is extraordinary — genuinely the best game design writing I've seen in a repository.

### The Bad News

The project is dramatically over-designed relative to what it needs to ship. There are seven design documents specifying systems (Chisel, Bridge, Swarm, Persistence, Gamification x2, Courts) that are collectively 0% implemented and are not needed for the MVP. The GAP_ANALYSIS identified 6 P0 bugs; roughly half are fixed. The SHIP_READINESS identified 29 checklist items; 1 is done. The project has been alive for two days and has produced 400,000 words of design and processed 4 real jobs.

### The Real Problem

The real problem is not technical. It is **integration discipline**. Every component works in isolation. No component has been verified against its neighbors. The project keeps generating new design documents and new modules instead of connecting the ones that exist. This is the exact pattern the SHIP_READINESS identified, and it is still happening.

### What To Do Tomorrow Morning

1. Open Roblox Studio.
2. Press Play.
3. Type "build a castle."
4. Watch nothing happen.
5. Fix the first thing that prevents the castle from appearing.
6. Repeat step 3.
7. Do not write any new design documents until the castle appears.

The castle is 21 hours away. Everything else is noise.

---

*"Stop generating and start integrating. One person, or one agent with continuity, opens Roblox Studio, presses play, and does not stop until a part appears in the world because a player typed a sentence."*

— SHIP_READINESS, which is still the best advice in this repository.

---

*End of Roadmap. 20 tasks. 5 decisions. 1 castle. Build it.*
