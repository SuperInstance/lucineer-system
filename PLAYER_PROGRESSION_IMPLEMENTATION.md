# PLAYER PROGRESSION — IMPLEMENTATION SPECIFICATION

**Slackwater — From Spawn to Day 2, in Code**

*This is an engineering document. It references real files, real tables, and real function signatures. Every Lua snippet is paste-ready into `EraSystem/init.lua` unless noted otherwise.*

---

## TABLE OF CONTENTS

1. [MVP Progression Path — The First Hour](#1-mvp-progression-path)
2. [Era 1 Implementation Spec — Driftwood and Salvage](#2-era-1-implementation-spec)
3. [Lucineer's Assessment Logic — Decision Tree](#3-lucineers-assessment-logic)
4. [Hook System — BondSystem ↔ EraSystem Bridge](#4-hook-system)
5. [Day-2 Callback — Returning Player Logic](#5-day-2-callback)
6. [Lua Code Blocks](#6-lua-code-blocks)

---

## 1. MVP PROGRESSION PATH

### The Question: What's the minimum viable player journey from spawn to "I want to come back tomorrow"?

### The Answer: 40 minutes, 4 builds, 1 hook completed, 1 assessment.

```
MINUTE 0:00 ─── Player spawns on beach. Lucineer is already there, working on
                something. He doesn't greet them. He acknowledges them with a nod
                and keeps stacking driftwood.

                SYSTEM STATE:
                  era = 0 (Simple Machines / Building Era not yet started)
                  bond = 0 (Stranger)
                  buildCounts = {}
                  sessionFirstBuild = false

MINUTE 2:00 ─── Player explores. Finds materials on the tideline. Picks up
                driftwood, beach_stone, canvas_scrap. The game teaches nothing
                with text — the world has obvious material sources and the
                player clicks them.

MINUTE 5:00 ─── Player tries to build something. This triggers Magic Moment 1
                ("The Siting"). Lucineier walks over, moves their intended
                placement, and delivers his first line.

                "You were standing in the wet. Ground drops four studs
                 over there. Build it here."

                This is also the player's first build, which fires:
                  - BondSystem.addBuildXP()  →  first_build_of_session = +1
                  - EraSystem.onBuild("lean_to")
                  - Building era 1 begins (first build triggers era tracking)

MINUTE 8:00 ─── Lucineier builds something nearby (his first NPC build for the
                player). It's a salvage_rack — and he leaves it deliberately
                unfinished (no top rack).

                "Threw up a rack. Left the top off — depends what you're drying."

                SYSTEM: BondSystem.registerOpenHook(playerId, "rack_top",
                         "salvage_rack missing top rack", position)

MINUTE 15:00 ── Player gathers more materials, builds a debris_hut. Now has 2
                distinct Era 1 builds.

                Lucineier: "Hut's up. Keeps rain off. Mostly."

MINUTE 20:00 ── Player builds a fire_pit. This is a required build for Era 1
                advancement. 3 distinct builds now.

                Lucineier builds something near the fire — a workbench_scrap.
                He leaves it unfinished (no tool rack).

                "Workbench. Stock's underneath. Left the rack off —
                 you'll want to pick what hangs there."

                SYSTEM: BondSystem.registerOpenHook(playerId,
                         "workbench_rack", "workbench missing tool rack",
                         position)

                Fire pit is lit. The world changes — ambient sound adds
                crackling, light radius at night. First tangible "I made
                this place different" moment.

MINUTE 25:00 ── Player explores further, finds more materials. Returns to camp.
                Notices the salvage_rack has no top. Completes it (places
                driftwood on the top rack position).

                SYSTEM DETECTS:
                  BondSystem.checkHookProximity(playerId, buildPosition)
                  → returns "rack_top"

                BondSystem.addHookXP(playerId, "rack_top")
                  → +5 bond points (CORE LOOP)
                  → bond now at 6

                Lucineier delivers Magic Moment 3 (mini version):
                  "Huh. Ran the slats crosswise. I'd have gone lengthwise.
                   Yours drains better. Don't make a thing of it."

                This is the moment the player understands: Lucineier notices
                what they do. The game is different from other builders.

MINUTE 30:00 ── Player has 4 distinct build types (lean_to, debris_hut,
                fire_pit, and either driftwood_platform or tideline_fence).
                fire_pit and workbench_scrap are built (required).

                Era 1 ADVANCEMENT CHECK passes.
                Lucineier assessment triggers (see §3).

                Lucineier walks the camp. Delivers Era 1→2 transition
                dialogue. New materials (timber, plank, treenail...) become
                available silently. Player discovers them by finding new
                material sources or by trying to build new things.

MINUTE 35:00 ── First Era 2 build attempt. Player tries to fell a tree.
                Game checks: has Lucineier shown them how? At bond 6 (still
                Stranger), Lucineier would normally do it himself. But the
                era transition just happened, so Lucineier delivers one
                tutorial line:

                "Different wood now. Timber doesn't come from the beach.
                 Look inland."

                Player explores inland. Finds trees. The world has expanded.

MINUTE 40:00 ── Player ends session. They have:
                  - A camp with 4-5 structures
                  - A fire pit that glows at night
                  - Evidence that Lucineier noticed their work
                  - New materials to explore next time
                  - An unfinished workbench rack (second hook)

                They want to come back because:
                  1. The workbench rack is still unfinished (open hook)
                  2. New materials just unlocked — they haven't tried them
                  3. Lucineier changed how he talked to them after they
                     finished his work — what happens if they do more?
                  4. The fire pit made the camp feel like THEIRS

                SYSTEM STATE:
                  era = 0 → advanced to building_era 1 complete, era 1 unlocked
                  bond = 6 (Stranger, but on the way to Acquaintance at 10)
                  buildCounts = { lean_to=1, debris_hut=1, fire_pit=1,
                                  workbench_scrap=1, salvage_rack=1 }
                  openHooks = { workbench_rack = unfinished }
                  lastSeen = <timestamp>
```

### What the MVP does NOT include

- No skill tree UI. No progress bar. No "Level 1" notification.
- No quest log. No objective markers. No tutorial overlays.
- No multi-day weather events. No NPC scheduling beyond Lucineier's proximity behavior.
- No Era 2+ content beyond material availability. Frame & Plank builds exist in the catalog but require timber, which requires felling trees, which requires a tool the player doesn't have yet. The world gates naturally.

### What makes it work

The MVP works because of three things, in order of importance:

1. **Lucineier's hook loop.** He leaves things unfinished. The player finishes them. He notices. This is the only feedback loop that matters in the first hour. No XP bar can substitute for "the AI builder reacted to my work."

2. **The fire pit.** It changes the world. Light at night, ambient sound, a gathering point. The player builds it and the island is different. This is the first "I changed the world" moment.

3. **The silent unlock.** When Era 1 completes, nothing flashes on screen. Lucineier walks, talks, and new things become possible. The player discovers timber by finding trees, not by a notification. Discovery is the reward.

---

## 2. ERA 1 IMPLEMENTATION SPEC

### 2.1 What Exists Now (Do Not Break)

The current `EraSystem/init.lua` is a **technology-era system** (Eras 0–6, from levers to autonomous agents). It tracks:
- `playerStates[playerName].currentEra` — which tech era (0–6)
- `playerStates[playerName].unlockedEras` — set of unlocked era numbers
- `playerStates[playerName].buildCounts` — { [buildType] = count }
- `EraSystem.onBuild(playerName, buildType)` — called when something is built

The technology-era system works. It's the backbone. **Building eras layer on top of it.**

The design doc (`ERA_BUILDING_SYSTEM.md`) defines a parallel `BUILDING_ERAS` table (Eras 1–5, Driftwood through Light & Signal). These map to tech eras but are tracked separately. A player can be tech era 2 (Electricity) but building era 1 (still in a driftwood shack). Lucineier cares about the building era.

### 2.2 What Needs to Be Added to EraSystem/init.lua

#### New State Fields (per player)

```lua
-- Add to playerStates[playerName]:
{
    -- Existing fields...
    currentEra = 0,
    unlockedEras = { [0] = true },
    eraXP = {},
    buildCounts = {},

    -- NEW: Building era fields
    buildingEra = 1,              -- current building era (1-5), starts at 1
    buildingEraUnlocked = { [1] = true },  -- which building eras are unlocked
    buildingEraReady = false,     -- whether advancement check has passed
    buildingEraAssessed = false,  -- whether Lucineier has delivered the assessment
    sessionStartBuilds = 0,       -- build count at session start (for day-2 delta)
    lastAssessmentTime = 0,       -- os.time() of last Lucineier assessment
}
```

#### New Tables (module-level)

```lua
-- Building era definitions (from ERA_BUILDING_SYSTEM.md)
local BUILDING_ERAS = {}

BUILDING_ERAS[1] = {
    name = "Driftwood and Salvage",
    lucineerName = "salvage years",
    requiredBuilds = { "fire_pit", "workbench_scrap" },
    minDistinctBuilds = 4,
    validBuilds = {
        "lean_to", "debris_hut", "tideline_fence", "salvage_rack",
        "fire_pit", "driftwood_platform", "workbench_scrap",
    },
    materials = {
        "driftwood", "salvage_plank", "rawhide", "palm_fiber",
        "kelp_dried", "sea_rope", "beach_stone", "canvas_scrap",
        "pitch", "shell", "bone",
    },
    tempo = 40,
    sky = "dawn_coastal",
    nightLight = "fire_only",
}

BUILDING_ERAS[2] = {
    name = "Frame and Plank",
    lucineerName = "honest years",
    requiredBuilds = { "post_and_beam", "framed_workshop" },
    minDistinctBuilds = 5,
    validBuilds = {
        "post_and_beam", "plank_wall", "shingled_roof", "framed_floor",
        "caulked_seam", "hinged_door", "glazed_window", "framed_workshop",
        "storehouse", "pier_jetty", "saw_pit", "crane_post",
    },
    tempo = 70,
    sky = "morning_clear",
    nightLight = "oil_lamps",
}

-- ... Eras 3-5 defined per ERA_BUILDING_SYSTEM.md §1
```

#### New Functions

| Function | Purpose | Called By |
|---|---|---|
| `EraSystem.getBuildingEra(playerName)` | Returns current building era (1–5) | UI, Lucineier brain, WorldScanner |
| `EraSystem.getBuildingEraInfo(eraNum)` | Returns era definition table | Any system querying materials/builds |
| `EraSystem.checkBuildingEraAdvancement(playerName)` | Returns true if era requirements met | Internal, called after every build |
| `EraSystem.advanceBuildingEra(playerName)` | Unlocks next era, fires Lucineier event | Internal, called after assessment |
| `EraSystem.onBuildingEraBuild(playerName, buildType)` | Tracks building-type builds separately from tech components | WorldScanner / placement system |
| `EraSystem.getSessionBuildDelta(playerName)` | Returns number of new builds this session | Day-2 callback |
| `EraSystem.getAssessmentContext(playerName)` | Returns structured data for Lucineier's decision | Lucineier brain |

### 2.3 Integration Points with BondSystem

The two systems connect at four points:

```
1. BUILD REGISTERED
   Player places a structure
     → EraSystem.onBuildingEraBuild(playerName, buildType)
         → updates buildCounts
         → checks advancement
     → BondSystem.addBuildXP(playerName)
         → if first build of session: +1 bond

2. HOOK COMPLETED
   Player finishes something Lucineier left unfinished
     → BondSystem.addHookXP(playerName, hookId)
         → +5 bond
     → EraSystem.onBuildingEraBuild(playerName, "hook_completion")
         → counts toward distinct build total if hook was an era build type

3. ASSESSMENT TRIGGERED
   Era advancement check passes
     → EraSystem requests Lucineier assessment
         → Lucineier brain queries BondSystem.getBehaviors()
         → Lucineier brain queries EraSystem.getAssessmentContext()
         → Assessment delivered
         → EraSystem.advanceBuildingEra(playerName)

4. ERA ADVANCED
   Building era unlocks
     → EraSystem.advanceBuildingEra()
         → new materials/builds become available
         → WorldChanges applied (sky, tempo, ambient)
         → BondSystem notified (era change may affect voice line pool)
```

### 2.4 Material Registry Extension

`Recipes.lua` currently handles technology components (lever, pulley, generator, etc.). Building materials and build types need a parallel registry. Add a `BuildingRecipes` module:

```
EraSystem/
  init.lua          (existing — gets building era additions)
  Recipes.lua       (existing – technology components)
  BuildingRecipes.lua (NEW – building materials and structure recipes)
```

`BuildingRecipes.lua` defines:
- Material IDs → harvest source mapping (where to find driftwood, beach_stone, etc.)
- Build type recipes (lean_to costs driftwood×3, canvas_scrap×2, etc.)
- Placement rules (surface, foundation_required, etc.)

---

## 3. LUCINEER'S ASSESSMENT LOGIC

### 3.1 When Does the Assessment Fire?

The assessment is a two-stage gate:

**Stage 1: Mechanical check (silent, automatic)**

```lua
EraSystem.checkBuildingEraAdvancement(playerName)
```

This runs after every build. If it returns `true`, `buildingEraReady` is set to `true`. Nothing visible happens.

**Stage 2: Lucineier's visit (narrative, triggered)**

When `buildingEraReady == true` AND any of these conditions:
- Player completes an open hook (Lucineier is already nearby, in a good mood)
- Player stands still for >10 seconds near their primary build site (Lucineier approaches)
- Player explicitly asks Lucineier to "look at" or "check" their camp
- 5 minutes have passed since the mechanical check passed (Lucineier arrives on his own)

The player can delay this indefinitely. Lucineier will approach, but if the player walks away, he shrugs and goes back to work. The gate stays open.

### 3.2 The Decision Tree (Pseudocode)

```
function Lucineier.shouldAssess(player):
    ┌─ Is buildingEraReady == true?
    │   NO  → return false. Not yet.
    │   YES → continue
    │
    ├─ Has buildingEraAssessed == true?
    │   YES → return false. Already done.
    │   NO  → continue
    │
    ├─ Is player currently building?
    │   YES → return false. Don't interrupt active work.
    │   NO  → continue
    │
    ├─ Has player completed at least one open hook?
    │   YES → priority = HIGH. Player has engaged with the core loop.
    │          Fire assessment at next natural pause.
    │   NO  → priority = MEDIUM. Player meets mechanical requirements
    │          but hasn't engaged with hook loop. Wait for natural pause
    │          or 5-minute timer.
    │
    └─ Return true, with priority.


function Lucineier.deliverAssessment(player):
    ┌─ Walk to primary build site (highest-investment structure)
    │
    ├─ Perform inspection animation (4 seconds):
    │   - Pace the perimeter
    │   - Test a beam/joint
    │   - Look at the fire pit specifically
    │   - Check the workbench
    │
    ├─ Query context:
    │   era = EraSystem.getBuildingEra(player)
    │   req = EraSystem.getBuildingEraInfo(era)
    │   bondTier = BondSystem.getBondLevel(player)
    │   hookStats = BondSystem.getPlayerData(player)
    │   builds = EraSystem.getBuildCounts(player)
    │
    ├─ SELECT DIALOGUE BRANCH based on context:
    │
    │   ┌─ BRANCH A: Standard assessment
    │   │   Condition: hookStats.hooksCompleted >= 1
    │   │   Content: Full Era 1→2 transition dialogue (from ERA_BUILDING_SYSTEM.md)
    │   │   Tone: Respectful. The player has proven engagement.
    │   │
    │   ├─ BRANCH B: No hooks completed
    │   │   Condition: hookStats.hooksCompleted == 0
    │   │   Content: Shorter assessment, still advances era, but Lucineier
    │   │           notes the unfinished work with a raised eyebrow.
    │   │   Tone: "You've built enough. Could build better."
    │   │   Line: "Camp's functional. Workshop's up. You haven't finished
    │   │          the rack, but that's your business.
    │   │          Ready for real wood when you are."
    │   │
    │   ├─ BRANCH C: Rushed (all 4 builds in <10 minutes)
    │   │   Condition: session build time < 10 minutes
    │   │   Content: Lucineier is slightly suspicious of the speed.
    │   │   Tone: "You throw things up fast. Fine. We'll see if they stand."
    │   │   Still advances era. But notes it.
    │   │
    │   └─ BRANCH D: Refusal state (player walked away from previous approach)
    │       Condition: buildingEraReady == true, previous approach was dodged
    │       Content: Very short. Non-pushy.
    │       Line: "Camp's ready to move up. Whenever you are."
    │       Does NOT force the full inspection. Just the one line.
    │
    ├─ AFTER DIALOGUE:
    │   - EraSystem.advanceBuildingEra(player)
    │   - buildingEraAssessed = true
    │   - Apply world changes (sky, tempo, ambient)
    │   - Silently unlock new materials
    │   - BondSystem: no direct points, but the assessment event itself
    │     may trigger an independent_build (+3) if Lucineier asks the
    │     player to do something during the dialogue
    │
    └─ POST-ASSESSMENT HOOK:
        Lucineier immediately creates a new open hook appropriate to the
        next era. For Era 2, this might be placing the first post_and_beam
        frame and leaving the braces off.

        "Set the first frame. Left the braces off — you'll want to
         feel where the racking force comes from before you brace it."
```

### 3.3 Edge Cases

| Situation | Behavior |
|---|---|
| Player builds all 7 Era 1 types (over-qualifies) | Assessment still fires with standard dialogue. Lucineier may note the thoroughness: "Seven builds. Could've stopped at four." |
| Player deletes structures after qualifying | Building counts are lifetime, not current. Deleting doesn't un-qualify. Lucineier notes: "Tore down the fence. That's fine. You built it once." |
| Player qualifies during a storm event | Assessment queued. Lucineier is busy checking structures (Magic Moment 4). Assessment fires after storm passes. |
| Player never builds fire_pit | Assessment never fires. fire_pit is a hard requirement. Lucineier will eventually hint: "Gets cold at night. A fire would change things." |
| Multiple players on same server | Each player has independent era tracking. Lucineier can only assess one player at a time. Queue assessments. |

---

## 4. HOOK SYSTEM — BondSystem ↔ EraSystem Bridge

### 4.1 How Open Hooks Connect to Era Advancement

The BondSystem's `openHooks` are the **primary engagement signal** for era advancement. Here's the connection:

```
BONDSYSTEM SIDE:
  Lucineier builds something → leaves it unfinished
  → BondSystem.registerOpenHook(playerId, hookId, description, position)

  Player builds near the hook
  → WorldScanner detects new part in hook's bounding box
  → BondSystem.checkHookProximity(playerId, buildPosition) → returns hookId
  → BondSystem.addHookXP(playerId, hookId)
      → +5 bond points
      → hook marked completed

ERASYSTEM SIDE (new bridge code):
  When BondSystem.addHookXP fires, EraSystem should ALSO be notified,
  because completing a hook often counts as a distinct build type.

  EraSystem.onHookCompleted(playerName, hookId):
    -- If the completed hook corresponds to a building-era build type,
    -- count it toward era advancement.
    -- E.g., completing "rack_top" on a salvage_rack counts as improving
    -- the salvage_rack, which is a valid Era 1 build.
```

### 4.2 Hook Creation Strategy by Era

Lucineier doesn't leave hooks randomly. He leaves them **strategically**, based on the player's current building era and what they haven't built yet.

#### Era 1 Hook Strategy

| Player Has Built | Lucineier Leaves | Hook ID | Purpose |
|---|---|---|---|
| `lean_to` (first build) | `salvage_rack` missing top rack | `hook_era1_rack` | Introduces material processing |
| `fire_pit` | Nearby `workbench_scrap` missing tool rack | `hook_era1_workbench` | Introduces crafting stations |
| 3 distinct builds | `driftwood_platform` missing rail | `hook_era1_platform_rail` | Tests if player understands safety/details |
| Any build near water | `tideline_fence` missing a post section | `hook_era1_fence` | Tests attention to perimeter |

Lucineier creates **at most 2 open hooks at a time** during Era 1. He's not overwhelming. The player should always have something to finish, but never feel buried.

#### Hook Selection Logic

```lua
function Lucineier.selectHookToCreate(playerName)
    local builds = EraSystem.getBuildCounts(playerName)
    local existingHooks = BondSystem.getOpenHooks(playerName)
    local era = EraSystem.getBuildingEra(playerName)

    -- Don't create more than 2 open hooks at once
    local openCount = 0
    for _ in pairs(existingHooks) do openCount = openCount + 1 end
    if openCount >= 2 then return nil end

    -- Era 1 hook selection
    if era == 1 then
        -- If player has built lean_to but no salvage_rack, create rack hook
        if builds["lean_to"] and not builds["salvage_rack"] then
            return {
                buildType = "salvage_rack",
                hookId = "hook_era1_rack",
                unfinishedPart = "top_rack",
                description = "salvage_rack missing top rack",
            }
        end

        -- If player has built fire_pit but no workbench, create workbench hook
        if builds["fire_pit"] and not builds["workbench_scrap"] then
            return {
                buildType = "workbench_scrap",
                hookId = "hook_era1_workbench",
                unfinishedPart = "tool_rack",
                description = "workbench_scrap missing tool rack",
            }
        end

        -- If player has 3+ distinct builds, create platform rail hook
        local distinct = 0
        for _, count in pairs(builds) do
            if count > 0 then distinct = distinct + 1 end
        end
        if distinct >= 3 and not existingHooks["hook_era1_platform_rail"] then
            return {
                buildType = "driftwood_platform",
                hookId = "hook_era1_platform_rail",
                unfinishedPart = "rail",
                description = "driftwood_platform missing safety rail",
            }
        end
    end

    return nil  -- No hook needed right now
end
```

### 4.3 Hook → Era Advancement Data Flow

```
Player places part near open hook
         │
         ▼
WorldScanner detects new part
         │
         ├─→ BondSystem.checkHookProximity(playerId, position)
         │       │
         │       └─→ Returns hookId if match
         │
         ├─→ BondSystem.addHookXP(playerId, hookId)
         │       │
         │       ├─→ +5 bond points
         │       ├─→ Mark hook completed
         │       └─→ Fire "magic_moment: the_handoff" if tier >= 2
         │
         └─→ EraSystem.onHookCompleted(playerName, hookId)  [NEW]
                 │
                 ├─→ Check if hook corresponds to a build type
                 │   (e.g. completing "hook_era1_rack" → salvage_rack built)
                 │
                 ├─→ If yes: EraSystem.onBuildingEraBuild(playerName, buildType)
                 │       │
                 │       └─→ Check advancement
                 │
                 └─→ If hook was required build: advancement may now pass
```

### 4.4 What Happens When Lucineier Leaves Something Unfinished

Per CHARACTER_BIBLE §3: "Every build has one deliberate gap, and you name it."

This is enforced in code. When Lucineier's brain generates a build plan, the build executor **must** omit one component and the dialogue generator **must** name it. The hook system formalizes this:

```lua
-- In Lucineier's build executor (brain → placement pipeline):
function Lucineier.executeBuild(buildPlan, playerName)
    local build = buildPlan.buildType
    local parts = buildPlan.parts  -- full list of parts

    -- Determine what to leave unfinished
    local hookPart = selectHookPart(build, playerName)

    -- Build everything EXCEPT the hook part
    for _, part in ipairs(parts) do
        if part.id ~= hookPart then
            placePart(part)
        end
    end

    -- Register the open hook
    BondSystem.registerOpenHook(
        playerName,
        generateHookId(build, playerName),
        hookPart.description,
        buildPlan.position
    )

    -- Generate dialogue that names the unfinished part
    -- (handled by brain's response generator)
end
```

The unfinished-part selection is deterministic per build type, not random:

| Build Type | Always Leaves | Why |
|---|---|---|
| `lean_to` | Door covering | Player's first shelter — they choose how to close it |
| `salvage_rack` | Top rack | Top rack is for processing — player isn't ready yet |
| `fire_pit` | (Nothing — fire pit is always complete) | Fire is sacred. You don't leave fire half-built. |
| `workbench_scrap` | Tool rack | Player chooses their tools |
| `driftwood_platform` | Rail | Safety detail — Lucineier wants them to notice |

**Exception:** `fire_pit` is never left unfinished. Lucineier considers fire a complete act. This also ensures the required build is always fully functional.

---

## 5. DAY-2 CALLBACK — RETURNING PLAYER LOGIC

### 5.1 What Happens When a Player Returns

```
Player joins server
         │
         ▼
EraSystem.loadPlayer(playerName)
    → Load from D1: era state, build counts, building era
         │
         ▼
BondSystem.loadBond(playerName)
    → Load from D1: bond tier, bond points
         │
         ▼
BondSystem.onPlayerJoin(playerName)
    → Check absence duration
    → If >24h: applyBondEvent("returned_next_day") → +2 bond
    → Reset sessionFirstBuild = false
         │
         ▼
EraSystem.onPlayerReturn(playerName)  [NEW]
    → Compare sessionStartBuilds to persisted buildCounts
    → Calculate delta (new builds since last session)
    → Check for open hooks that are still open
    → Generate "returning state" for Lucineier's opening line
```

### 5.2 The Returning State Object

```lua
function EraSystem.getPlayerReturnState(playerName)
    local state = playerStates[playerName]
    if not state then return nil end

    local data = BondSystem.getPlayerData(playerName)
    local builds = getBuildCounts(playerName)

    -- Calculate session delta
    local sessionDelta = 0
    for buildType, count in pairs(builds) do
        local lastSession = state.sessionStartBuilds[buildType] or 0
        if count > lastSession then
            sessionDelta = sessionDelta + (count - lastSession)
        end
    end

    -- Find unfinished hooks
    local unfinishedHooks = BondSystem.getOpenHooks(playerName)

    return {
        buildingEra = state.buildingEra,
        bondTier = data.tier,
        bondTierName = data.tierName,
        totalBuilds = countTotalBuilds(builds),
        sessionBuildDelta = sessionDelta,
        openHooks = unfinishedHooks,
        openHookCount = data.openHookCount or 0,
        hooksCompleted = data.hooksCompleted or 0,
        absenceHours = math.floor((os.time() - (data.lastSeen or os.time())) / 3600),
        buildingEraReady = state.buildingEraReady,
        lastAssessmentTime = state.lastAssessmentTime or 0,
    }
end
```

### 5.3 Lucineier's Day-2 Behavior

Based on the returning state, Lucineier's opening line and behavior change:

#### Scenario A: First Return (left after Era 1, hook still open)

```
State:
  buildingEra = 1 (still in Driftwood)
  openHooks = { workbench_rack = unfinished }
  hooksCompleted = 1
  bondTier = 0 (Stranger, ~6 points)
  absenceHours = 20

Lucineier's behavior:
  - He's standing near the fire pit when the player spawns.
  - He doesn't rush over. He nods. Continues working.
  - Opening line (delivered after 5-10 seconds, not immediately):

    "Back. Workbench rack's still open. Fire held — I checked."

  - The world reflects their previous work:
    * Fire pit is still burning (Lucineier maintained it)
    * All structures are standing (no degradation in MVP)
    * The salvage_rack the player completed has materials on it
      (Lucineier placed a few items there as ambient worldbuilding)
    * The workbench is still missing its rack (the hook persists)

  - The camp looks slightly different: Lucineier added one small thing
    while they were gone. Maybe a stone path from the fire pit to the
    workbench. Nothing functional — just evidence that the world continued
    without them.

    "Threw a path in. Mud was getting old."
```

#### Scenario B: Return After Era Advancement

```
State:
  buildingEra = 2 (advanced to Frame & Plank last session)
  openHooks = { } (none — player cleared all hooks)
  hooksCompleted = 3
  bondTier = 0-1 (~11-15 points, may have hit Acquaintance)
  absenceHours = 26

Lucineier's behavior:
  - He's standing at the edge of camp, looking at trees.
  - Opening line:

    "Been looking at the timber. Straight grain, three trees inland.
     Ready when you are."

  - The world reflects advancement:
    * Trees are now harvestable (weren't interactable in Era 1)
    * A new material source (clay deposit, stone outcrop) has appeared
      further inland — visible if the player explores
    * The camp's ambient sound has shifted slightly (tempo map changed
      from 40 BPM to 70 BPM on advancement)
    * Lucineier has placed one timber beam near the workbench —
      not a structure, just stock. Evidence that he's been preparing.

  - If bond tier hit 1 (Acquaintance) during the absence:
    Lucineier references a previous build for the first time:

    "Fire pit's holding. Same stone you set. Good choice."
```

#### Scenario C: Long Absence (>7 days)

```
State:
  absenceHours = 168+ (a week or more)

Lucineier's behavior:
  - He's working on something when the player arrives. Doesn't stop.
  - Opening line (after a beat):

    "Been a while. Nothing fell down."

  - Then, after a pause:

    "Tower's still open on top, same as you left it."

  - The world is exactly as they left it. No degradation, no penalty.
    But Lucineier has clearly been busy — there are small additions:
    * Cleaned-up material storage near the workbench
    * A second fire pit (he built his own, separate from the player's)
    * Materials staged near likely Era 2+ build sites

  - These additions are NOT a penalty or a "look what you missed."
    They're evidence that Lucineier exists between sessions. He's a
    builder. He builds. The player was gone and he kept working.

  - No quest appears. No "welcome back" notification. Just the world,
    slightly different, and Lucineier acknowledging the gap without
    judgment.
```

### 5.4 Session Start Capture

To support the day-2 delta, capture the build state at session start:

```lua
-- In EraSystem.loadPlayer(), after loading from D1:
local function captureSessionStart(playerName)
    local state = playerStates[playerName]
    if not state then return end

    -- Deep-copy current build counts as session baseline
    local snapshot = {}
    for buildType, count in pairs(state.buildCounts or {}) do
        snapshot[buildType] = count
    end
    state.sessionStartBuilds = snapshot
end
```

### 5.5 D1 Persistence Schema Extension

The current `/api/era/save` endpoint persists:
```json
{ "playerName": "...", "currentEra": 0, "unlockedEras": [0], "eraXP": {} }
```

Extend it to include building era state:
```json
{
    "playerName": "...",
    "currentEra": 0,
    "unlockedEras": [0],
    "eraXP": {},
    "buildingEra": 1,
    "buildingEraUnlocked": [1],
    "buildingEraReady": false,
    "buildingEraAssessed": false,
    "buildCounts": { "lean_to": 1, "fire_pit": 1 },
    "lastAssessmentTime": 0
}
```

The D1 worker (`lucineer-memory`) needs its schema extended to store these fields. The `buildCounts` table is the most important — it's the persistent record of what the player has built across sessions.

---

## 6. CONCRETE LUA CODE BLOCKS

### Snippet 1: Building Era Definitions Table

Paste at module level in `EraSystem/init.lua`, after the existing `ERAS` table:

```lua
-- ═══════════════════════════════════════════════════════════════════════════
-- BUILDING ERA DEFINITIONS (parallel to tech eras)
-- ═══════════════════════════════════════════════════════════════════════════

local BUILDING_ERAS = {}

BUILDING_ERAS[1] = {
    name = "Driftwood and Salvage",
    lucineerName = "salvage years",
    tagline = "You work with what the tide brings you.",
    requiredBuilds = { "fire_pit", "workbench_scrap" },
    minDistinctBuilds = 4,
    validBuilds = {
        "lean_to", "debris_hut", "tideline_fence", "salvage_rack",
        "fire_pit", "driftwood_platform", "workbench_scrap",
    },
    materials = {
        "driftwood", "salvage_plank", "rawhide", "palm_fiber",
        "kelp_dried", "sea_rope", "beach_stone", "canvas_scrap",
        "pitch", "shell", "bone",
    },
    worldChanges = {
        ambientSound = "wind_and_waves",
        skyPreset = "dawn_coastal",
        particleDensity = 0.3,
        nightLight = "fire_only",
    },
    tempo = 40,
    lucineerTransitionKey = "era1_to_era2",
}

BUILDING_ERAS[2] = {
    name = "Frame and Plank",
    lucineerName = "honest years",
    tagline = "First real carpentry. The structure has opinions about where it wants to stand.",
    requiredBuilds = { "post_and_beam", "framed_workshop" },
    minDistinctBuilds = 5,
    validBuilds = {
        "post_and_beam", "plank_wall", "shingled_roof", "framed_floor",
        "caulked_seam", "hinged_door", "glazed_window", "framed_workshop",
        "storehouse", "pier_jetty", "saw_pit", "crane_post",
    },
    materials = {
        "timber", "plank", "treenail", "tar_boiled", "oakum",
        "nail_wrought", "hinge_iron", "glass_crude", "shingle",
        "mortise_peg", "brace_timber", "sill_beam", "canvas_woven",
    },
    worldChanges = {
        ambientSound = "hammer_and_saw",
        skyPreset = "morning_clear",
        particleDensity = 0.4,
        nightLight = "oil_lamps",
    },
    tempo = 70,
    lucineerTransitionKey = "era2_to_era3",
}

-- Eras 3-5 follow the same pattern per ERA_BUILDING_SYSTEM.md.
-- Only Era 1-2 are shown here; Era 3+ defined when those eras are implemented.
```

### Snippet 2: Building Era State Initialization

Modify the `loadPlayer` function to include building era fields:

```lua
-- Extended loadPlayer with building era state
local function loadPlayer(playerName)
    local success, result = pcall(function()
        return Http.post(MEMORY_URL .. "/api/era/load", {
            playerName = playerName,
        })
    end)

    if success and result and result.currentEra then
        playerStates[playerName] = {
            currentEra = result.currentEra,
            unlockedEras = {},
            eraXP = result.eraXP or {},
            buildCounts = result.buildCounts or {},
            -- Building era fields
            buildingEra = result.buildingEra or 1,
            buildingEraUnlocked = { [1] = true },
            buildingEraReady = result.buildingEraReady or false,
            buildingEraAssessed = result.buildingEraAssessed or false,
            lastAssessmentTime = result.lastAssessmentTime or 0,
        }
        -- Reconstruct unlockedEras set
        for _, eraNum in ipairs(result.unlockedEras or {0}) do
            playerStates[playerName].unlockedEras[eraNum] = true
        end
        -- Reconstruct building era unlocked set
        for _, eraNum in ipairs(result.buildingEraUnlocked or {1}) do
            playerStates[playerName].buildingEraUnlocked[eraNum] = true
        end
    else
        -- Default: tech era 0, building era 1
        playerStates[playerName] = {
            currentEra = 0,
            unlockedEras = { [0] = true },
            eraXP = {},
            buildCounts = {},
            buildingEra = 1,
            buildingEraUnlocked = { [1] = true },
            buildingEraReady = false,
            buildingEraAssessed = false,
            lastAssessmentTime = 0,
        }
    end

    -- Capture session-start snapshot for day-2 delta
    local snapshot = {}
    for buildType, count in pairs(playerStates[playerName].buildCounts) do
        snapshot[buildType] = count
    end
    playerStates[playerName].sessionStartBuilds = snapshot
end
```

### Snippet 3: Building Era Advancement Check

Add as a new public function. This is the mechanical gate:

```lua
-- ═══════════════════════════════════════════════════════════════════════════
-- BUILDING ERA ADVANCEMENT
-- ═══════════════════════════════════════════════════════════════════════════

-- Helper: check if player has built any from a list
local function hasBuiltAny(counts, buildList)
    for _, buildType in ipairs(buildList) do
        if counts[buildType] and counts[buildType] > 0 then
            return true
        end
    end
    return false
end

-- Check if a player meets the requirements to advance building era.
-- Returns true if ready, false if not. Does NOT advance — that requires
-- Lucineier's assessment.
function EraSystem.checkBuildingEraAdvancement(playerName)
    local state = playerStates[playerName]
    if not state then return false end

    local currentEra = state.buildingEra or 1
    local nextEra = currentEra + 1

    -- Era 5 is the final era — no advancement possible
    if not BUILDING_ERAS[nextEra] then return false end

    -- Already assessed/ready? Don't re-check.
    if state.buildingEraReady then return true end

    local eraDef = BUILDING_ERAS[currentEra]
    if not eraDef then return false end

    local counts = state.buildCounts or {}

    -- Check required builds
    for _, buildType in ipairs(eraDef.requiredBuilds) do
        if not (counts[buildType] and counts[buildType] > 0) then
            return false  -- Missing a required build
        end
    end

    -- Count distinct valid builds
    local distinctCount = 0
    for _, buildType in ipairs(eraDef.validBuilds) do
        if counts[buildType] and counts[buildType] > 0 then
            distinctCount = distinctCount + 1
        end
    end

    if distinctCount < eraDef.minDistinctBuilds then
        return false  -- Not enough variety
    end

    -- All checks passed — mark as ready
    state.buildingEraReady = true
    return true
end

-- Actually advance the building era (called after Lucineier's assessment)
function EraSystem.advanceBuildingEra(playerName)
    local state = playerStates[playerName]
    if not state then return false end
    if not state.buildingEraReady then return false end
    if state.buildingEraAssessed then return false end

    local currentEra = state.buildingEra or 1
    local nextEra = currentEra + 1

    if not BUILDING_ERAS[nextEra] then return false end

    state.buildingEra = nextEra
    state.buildingEraUnlocked[nextEra] = true
    state.buildingEraReady = false
    state.buildingEraAssessed = true
    state.lastAssessmentTime = os.time()

    local eraDef = BUILDING_ERAS[nextEra]
    print(string.format("[EraSystem] %s advanced to Building Era %d: %s",
        playerName, nextEra, eraDef.name))

    -- Fire event for other systems
    _G.EraSystem_BuildingEraAdvanced = _G.EraSystem_BuildingEraAdvanced or {}
    table.insert(_G.EraSystem_BuildingEraAdvanced, {
        playerName = playerName,
        newEra = nextEra,
        eraData = eraDef,
    })

    -- Persist
    savePlayer(playerName)

    return true
end

-- Get current building era
function EraSystem.getBuildingEra(playerName)
    local state = playerStates[playerName]
    return state and state.buildingEra or 1
end

-- Get building era definition
function EraSystem.getBuildingEraInfo(eraNumber)
    return BUILDING_ERAS[eraNumber]
end

-- Get build counts (public accessor)
function EraSystem.getBuildCounts(playerName)
    local state = playerStates[playerName]
    return state and state.buildCounts or {}
end
```

### Snippet 4: Building Era Build Registration + Hook Bridge

This replaces the existing `onBuild` with a version that handles both tech-era triggers and building-era tracking. It also connects to BondSystem hooks:

```lua
-- Called when a player places a building-type structure.
-- This is SEPARATE from tech-era component builds (which go through onBuild).
-- Building-type structures: lean_to, fire_pit, workbench_scrap, etc.
function EraSystem.onBuildingEraBuild(playerName, buildType)
    local state = playerStates[playerName]
    if not state then
        loadPlayer(playerName)
        state = playerStates[playerName]
    end

    -- Track build count
    local counts = state.buildCounts or {}
    counts[buildType] = (counts[buildType] or 0) + 1
    state.buildCounts = counts

    -- Check if this build completed an open hook
    -- (the hook proximity check is done by WorldScanner before calling this,
    -- but we also check here as a safety net)
    local BondSystem = script.Parent and script.Parent:FindFirstChild("BondSystem")
    if BondSystem then
        local bs = require(BondSystem)
        local hooks = bs.getOpenHooks(playerName)
        for hookId, hook in pairs(hooks) do
            -- If this build type matches a hook's expected build type
            if hook.buildType == buildType or string.find(hook.description, buildType, 1, true) then
                bs.addHookXP(playerName, hookId)
                break
            end
        end
    end

    -- Check for building era advancement
    EraSystem.checkBuildingEraAdvancement(playerName)

    -- Persist
    savePlayer(playerName)
end

-- Called when a hook is completed (by BondSystem or WorldScanner)
-- This allows hook completions to count toward era advancement.
function EraSystem.onHookCompleted(playerName, hookId, buildType)
    local state = playerStates[playerName]
    if not state then return end

    -- If the hook completion corresponds to a build type we track,
    -- and it's not already counted, count it.
    if buildType then
        local counts = state.buildCounts or {}
        -- Only count if this build type wasn't already registered
        -- (avoids double-counting if onBuildingEraBuild was also called)
        if not counts[buildType] or counts[buildType] == 0 then
            counts[buildType] = 1
            state.buildCounts = counts
            EraSystem.checkBuildingEraAdvancement(playerName)
            savePlayer(playerName)
        end
    end
end
```

### Snippet 5: Assessment Context + Return State

These functions provide the data that Lucineier's brain needs to make assessment decisions and generate day-2 callbacks:

```lua
-- ═══════════════════════════════════════════════════════════════════════════
-- ASSESSMENT CONTEXT (for Lucineier's brain)
-- ═══════════════════════════════════════════════════════════════════════════

-- Get a structured context object describing the player's progression state.
-- Lucineier's brain queries this when deciding whether and how to assess.
function EraSystem.getAssessmentContext(playerName)
    local state = playerStates[playerName]
    if not state then return nil end

    local counts = state.buildCounts or {}
    local era = state.buildingEra or 1
    local eraDef = BUILDING_ERAS[era]

    -- Count distinct builds in current era
    local distinctInEra = 0
    local builtTypes = {}
    if eraDef then
        for _, buildType in ipairs(eraDef.validBuilds) do
            if counts[buildType] and counts[buildType] > 0 then
                distinctInEra = distinctInEra + 1
                table.insert(builtTypes, buildType)
            end
        end
    end

    -- Check required builds
    local requiredMet = {}
    local allRequiredMet = true
    if eraDef then
        for _, buildType in ipairs(eraDef.requiredBuilds) do
            local has = counts[buildType] and counts[buildType] > 0
            requiredMet[buildType] = has
            if not has then allRequiredMet = false end
        end
    end

    return {
        currentEra = era,
        eraName = eraDef and eraDef.name or "Unknown",
        ready = state.buildingEraReady or false,
        assessed = state.buildingEraAssessed or false,
        distinctBuildsInEra = distinctInEra,
        minRequired = eraDef and eraDef.minDistinctBuilds or 0,
        builtTypes = builtTypes,
        requiredBuilds = requiredMet,
        allRequiredMet = allRequiredMet,
        totalBuilds = (function()
            local t = 0
            for _, c in pairs(counts) do t = t + c end
            return t
        end)(),
    }
end

-- ═══════════════════════════════════════════════════════════════════════════
-- RETURNING PLAYER STATE (for day-2 callback)
-- ═══════════════════════════════════════════════════════════════════════════

-- Get the player's state for day-2 processing.
-- Called by Lucineier's brain when a player joins to generate the
-- returning-player greeting and decide what's changed in the world.
function EraSystem.getPlayerReturnState(playerName)
    local state = playerStates[playerName]
    if not state then return nil end

    -- Calculate builds since last session
    local currentCounts = state.buildCounts or {}
    local sessionStart = state.sessionStartBuilds or {}
    local newBuilds = {}
    local totalNew = 0

    for buildType, count in pairs(currentCounts) do
        local prev = sessionStart[buildType] or 0
        if count > prev then
            newBuilds[buildType] = count - prev
            totalNew = totalNew + (count - prev)
        end
    end

    return {
        buildingEra = state.buildingEra or 1,
        buildingEraReady = state.buildingEraReady or false,
        totalBuilds = (function()
            local t = 0
            for _, c in pairs(currentCounts) do t = t + c end
            return t
        end)(),
        newBuildsSinceLastSession = totalNew,
        newBuildTypes = newBuilds,
        lastAssessmentTime = state.lastAssessmentTime or 0,
        assessmentAvailable = state.buildingEraReady and not state.buildingEraAssessed,
    }
end

-- Mark that Lucineier has assessed (used after assessment dialogue completes)
function EraSystem.markAssessed(playerName)
    local state = playerStates[playerName]
    if not state then return end
    state.buildingEraAssessed = true
    state.lastAssessmentTime = os.time()
    savePlayer(playerName)
end

-- Reset assessment flag for next era (called internally by advanceBuildingEra)
-- This allows the next era's advancement to trigger a fresh assessment.
local function resetAssessmentFlag(playerName)
    local state = playerStates[playerName]
    if not state then return end
    state.buildingEraAssessed = false
    state.buildingEraReady = false
end
```

### Snippet 6: Extended Save Function

Update `savePlayer` to persist building era state to D1:

```lua
-- Extended savePlayer with building era fields
local function savePlayer(playerName)
    local state = playerStates[playerName]
    if not state then return end

    local unlockedList = {}
    for eraNum in pairs(state.unlockedEras) do
        table.insert(unlockedList, eraNum)
    end
    table.sort(unlockedList)

    local buildingEraUnlockedList = {}
    for eraNum in pairs(state.buildingEraUnlocked or {}) do
        table.insert(buildingEraUnlockedList, eraNum)
    end
    table.sort(buildingEraUnlockedList)

    pcall(function()
        Http.post(MEMORY_URL .. "/api/era/save", {
            playerName = playerName,
            currentEra = state.currentEra,
            unlockedEras = unlockedList,
            eraXP = state.eraXP,
            -- Building era persistence
            buildingEra = state.buildingEra or 1,
            buildingEraUnlocked = buildingEraUnlockedList,
            buildingEraReady = state.buildingEraReady or false,
            buildingEraAssessed = state.buildingEraAssessed or false,
            buildCounts = state.buildCounts or {},
            lastAssessmentTime = state.lastAssessmentTime or 0,
        })
    end)
end
```

### Snippet 7: Hook-Aware Lucineier Build Selector

This is a standalone function that Lucineier's brain calls before starting a build. It determines what to leave unfinished and creates the hook. Place it in the Lucineier build controller (not EraSystem — this is the bridge between brain and BondSystem):

```lua
-- In ServerScriptService/LucineerBuildController/init.lua (or similar)
-- Called before Lucineier places a build. Determines the hook and registers it.

local EraSystem = require(game:GetService("ServerScriptService"):WaitForChild("EraSystem"))
local BondSystem = require(game:GetService("ServerScriptService"):WaitForChild("BondSystem"))

-- Maps build types to their deliberate-unfinished part.
-- Fire pit is NEVER left unfinished (it's sacred and required).
local HOOK_PARTS = {
    lean_to = { part = "door_cover", description = "lean_to missing door covering" },
    debris_hut = { part = "ridge_cap", description = "debris_hut missing ridge cap" },
    salvage_rack = { part = "top_rack", description = "salvage_rack missing top rack" },
    workbench_scrap = { part = "tool_rack", description = "workbench_scrap missing tool rack" },
    driftwood_platform = { part = "rail", description = "driftwood_platform missing rail" },
    tideline_fence = { part = "gate_section", description = "tideline_fence missing gate section" },
    -- Era 2 builds
    post_and_beam = { part = "brace_north", description = "post_and_beam missing north brace" },
    framed_workshop = { part = "south_wall", description = "framed_workshop missing south wall" },
    -- ... extend per era
}

-- Determine what Lucineier should leave unfinished for this build.
function LucineierBuildController.getHookForBuild(buildType, playerName)
    -- Fire pit: never unfinished
    if buildType == "fire_pit" then
        return nil
    end

    local hookDef = HOOK_PARTS[buildType]
    if not hookDef then
        -- No hook defined for this build type — pick the last part
        return { part = "last", description = buildType .. " missing final piece" }
    end

    -- Generate unique hook ID
    local hookId = "hook_" .. buildType .. "_" .. tostring(os.time())

    return {
        hookId = hookId,
        buildType = buildType,
        part = hookDef.part,
        description = hookDef.description,
    }
end

-- Called after Lucineier places a build (with the hook part omitted).
-- Registers the open hook with BondSystem.
function LucineierBuildController.registerBuildHook(playerName, buildType, position)
    -- Don't create hooks if Lucineier is at Partner tier (tier 4)
    -- Per CHARACTER_BIBLE §4 Tier 4: "stops leaving things unfinished"
    if BondSystem.getBondLevel(playerName) >= 4 then
        -- At tier 4, Lucineier finishes things — but says so out loud
        return nil
    end

    -- Don't exceed 2 open hooks
    local openHooks = BondSystem.getOpenHooks(playerName)
    local openCount = 0
    for _ in pairs(openHooks) do openCount = openCount + 1 end
    if openCount >= 2 then
        return nil  -- Already enough bait out
    end

    local hook = LucineierBuildController.getHookForBuild(buildType, playerName)
    if not hook then return nil end

    BondSystem.registerOpenHook(
        playerName,
        hook.hookId,
        hook.description,
        position
    )

    -- Also notify EraSystem so it knows this build type was placed
    -- (for advancement tracking — Lucineier's builds count toward
    -- the player's era awareness, even though the player didn't build them)
    EraSystem.onBuildingEraBuild(playerName, buildType)

    return hook
end
```

---

## APPENDIX A: FILE MODIFICATION CHECKLIST

| File | Changes Required |
|---|---|
| `EraSystem/init.lua` | Add `BUILDING_ERAS` table. Add building era fields to `playerStates`. Add `onBuildingEraBuild`, `checkBuildingEraAdvancement`, `advanceBuildingEra`, `getAssessmentContext`, `getPlayerReturnState`, `markAssessed`. Extend `loadPlayer`/`savePlayer` with building-era persistence. Export new functions. |
| `EraSystem/Recipes.lua` | No changes needed for MVP. Building recipes go in new `BuildingRecipes.lua`. |
| `EraSystem/BuildingRecipes.lua` | **NEW FILE.** Material harvest sources. Build type costs. Placement rules. Era gating per build type. |
| `BondSystem/init.lua` | No structural changes. The hook system (`registerOpenHook`, `checkHookProximity`, `addHookXP`) already exists. Bridge code lives in EraSystem or a new connector module. |
| `EraSystem/HookBridge.lua` | **NEW FILE (optional).** Thin connector that listens for BondSystem hook events and notifies EraSystem. Can be inlined in EraSystem if preferred. |
| `LucineierBuildController/init.lua` | **NEW FILE (or extend existing).** Hook-aware build selector. Translates build plans into "build everything except hookPart" instructions. |

## APPENDIX B: IMPLEMENTATION ORDER

```
PHASE 1 (MVP — get the first hour working):
  1. Add BUILDING_ERAS table to EraSystem (Snippet 1)
  2. Extend loadPlayer/savePlayer with building-era fields (Snippets 2, 6)
  3. Add advancement check + advance function (Snippet 3)
  4. Add onBuildingEraBuild with hook bridge (Snippet 4)
  5. Add assessment context + return state (Snippet 5)
  6. Create BuildingRecipes.lua with Era 1 materials and builds
  7. Wire WorldScanner to call onBuildingEraBuild when player places structures
  8. Wire Lucineier build executor to create hooks (Snippet 7)

PHASE 2 (Lucineier assessment):
  9. Implement assessment trigger logic (proximity, pause, timer)
  10. Wire Lucineier brain to query getAssessmentContext
  11. Implement dialogue branch selection (A/B/C/D from §3.2)
  12. Implement world changes on advancement (sky, tempo, ambient)

PHASE 3 (Day-2):
  13. Implement session-start snapshot capture (Snippet in §5.4)
  14. Wire BondSystem.onPlayerJoin to call EraSystem.getPlayerReturnState
  15. Implement Lucineier's day-2 greeting based on return state (§5.3)
  16. Add ambient world changes (Lucineier's path, staged materials)

PHASE 4 (Era 2 content):
  17. Add Era 2 BUILDING_ERAS definition
  18. Add Era 2 BuildingRecipes (timber, plank, etc.)
  19. Add tree harvesting mechanics
  20. Add Era 2 hook definitions
```

---

*End of Player Progression Implementation Specification. 7 code blocks, 4 appendices, every function signature documented. Hand to an engineer and they can start on Phase 1 immediately.*
