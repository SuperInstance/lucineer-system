# Integration Glue — Code Written

**Date:** 2026-08-03  
**Scope:** Wire together individual world systems (70–90% complete) into a playable loop (was 20–30% integrated).  
**Reference:** WORLD_SYSTEMS_AUDIT.md Top 5 Priorities

---

## Summary

Five integration systems were written across four Lua source files. All code follows existing conventions (CollectionService tagging, attribute-based metadata, BindableEvent broadcasting) and slots into the existing pipeline without replacing any working code.

| File | Lines Added | Integration |
|------|-------------|-------------|
| `CommandExecutor.lua` | ~60 | Structure tagging (P0 #4, P1 #11) |
| `WorldGenerator/init.lua` | ~180 | Spawn point + ProximityPrompts (P0 #2, #4) |
| `WeatherSystem/init.lua` | ~160 | Storm damage to builds + audio events (P1 #11) |
| `LucineerServer/init.lua` | ~4 | World generation on server start |

---

## 1. Structure Tagging System

**File:** `ReplicatedStorage/Lucineer/CommandExecutor.lua`

### What Changed

Every part/model created by CommandExecutor is now tagged and attributed so WeatherSystem (and future systems) can discover and interact with built structures.

**Tag: `"LucineerBuilt"`** — applied to every individual BasePart via `CollectionService:AddTag()` in `prepareBasePart()`.

**Tag: `"Structure"`** — applied to Models created by `createGroup()` and `createModel()`. This is the tag WeatherSystem's `applyWaveDamage()` already queries for storm mechanics.

### Attributes Set on Each Built Part

| Attribute | Value | Used By |
|-----------|-------|---------|
| `Era` | `params.era` or `0` | Era-gated damage immunity, visual filtering |
| `BuildMaterial` | Material name string | WeatherSystem reinforcement check |
| `BuildTimestamp` | `os.time()` | Age tracking, save/load |
| `Health` | `100` (or `params.health`) | Storm damage tracking |
| `MaxHealth` | `100` (or `params.health`) | Damage fraction calculations |
| `Reinforced` | `false` (or `params.reinforced`) | Storm damage immunity |

### How It Connects

```
CommandExecutor.createPart()
  → prepareBasePart()
    → CollectionService:AddTag(part, "LucineerBuilt")
    → part:SetAttribute("Health", 100)
    → part:SetAttribute("Era", era)
    → ...

WeatherSystem storm tick
  → applyStormStructureDamage()
    → CollectionService:GetTagged("LucineerBuilt")
    → Check Health, MaxHealth, Reinforced
    → Apply damage / visual cracks / collapse
```

---

## 2. Spawn Point Selection

**File:** `ServerScriptService/WorldGenerator/init.lua`

### What Changed

Added `findCoastlineSpawn()` and `placeSpawnPoint()` functions that scan the heightmap for the best beach position.

### Algorithm

1. Scan every heightmap cell for elevation between `waterLevel` and `waterLevel + 6` studs
2. Calculate local slope by sampling 4 neighbors
3. Score each candidate: `score = -slope*2 + -distanceFromWater + coastlineBiomeBonus`
4. Pick highest-scoring position
5. Create a `SpawnLocation` part (Sand material, 6×1×6 studs) at that position
6. Orient it facing the water (outward angle from center)
7. Tag with `"LucineerSpawnPoint"` for identification

### Fallback

If no suitable coastline is found, spawns at `(0, waterLevel+5, 0)`.

### Pipeline Integration

Called as `Step 4b` in `WorldGenerator.Generate()`, after terrain + props but before tide system start:

```
Step 1: Generate terrain
Step 2: Generate underground
Step 3: Spawn resources
Step 4: Place props
Step 4b: Place spawn point    ← NEW
Step 4c: Add resource prompts ← NEW
Step 5: Initialize tide
Step 6: Start tide
```

---

## 3. Storm Damage to Structures

**File:** `ServerScriptService/WeatherSystem/init.lua`

### What Changed

Added `applyStormStructureDamage()` function that runs alongside the existing `applyWaveDamage()` during storm wave damage ticks. This function specifically targets `"LucineerBuilt"` tagged parts.

### Three-Stage Damage Model

| Stage | Health Threshold | Effect |
|-------|-----------------|--------|
| **Cracks** | < 50% health | Color darkens to 70%, flickering SurfaceLight added (warm orange, simulating electrical damage) |
| **Displacement** | < 30% health | Part shifts 1.5 studs in random XZ direction (only once, anchored parts only, non-reinforced) |
| **Collapse** | 0 health | Part unanchored, impulse applied (falls with debris), Debris cleanup after 10s, `"LucineerBuilt"` tag removed |

### Reinforcement

- Structures with `Reinforced = true` attribute take **1/3x damage** (3x effective health)
- Reinforced structures are immune to displacement and collapse
- Material check: if `part.Material` is in `STORM_CONFIG.reinforcedMaterials` (Slate, Concrete, Brick, Metal, etc.), treated as reinforced

### Configuration

```lua
local STRUCTURE_STORM_CONFIG = {
    structureWaveDamage    = 25,   -- per tick
    crackThreshold         = 0.5,  -- 50% health
    displacementThreshold  = 0.3,  -- 30% health
    displacementAmount     = 1.5,  -- studs
    collapseThreshold      = 0.0,  -- 0% health
    reinforcedHealthMult   = 3.0,  -- 3x effective HP
}
```

### Damage Event

A `BindableEvent` named `"StormDamage"` is fired for each damaged structure, carrying `(part, damageAmount, newHealth, maxHealth)`. Other systems can listen:

```lua
WeatherSystem.WeatherAudioChange.Event:Connect(function(data) ... end)
script.StormDamage.Event:Connect(function(part, dmg, hp, maxhp) ... end)
```

### Wind Force Fix

Also fixed the audit-flagged `applyWindForce` NaN/extreme value bug: `AssemblyMass` is now clamped to `[0.1, 500]` with a NaN check before applying impulse.

---

## 4. Resource Node Harvesting

**File:** `ServerScriptService/WorldGenerator/init.lua`

### What Changed

Added `addResourcePrompts()` function that attaches a `ProximityPrompt` to every resource node model after prop placement.

### ProximityPrompt Configuration

| Property | Value |
|----------|-------|
| HoldDuration | From `resDef.harvestTime` or `1.0`s |
| MaxActivationDistance | 6 studs |
| KeyboardKeyCode | E |
| RequiresLineOfSight | false |

### Action Text by Resource Type

| Resource | Action Text |
|----------|-------------|
| wood, hardwood | "Chop" |
| stone, limestone, iron_ore | "Mine" |
| fiber, kelp | "Gather" |
| fish | "Catch" |
| salvage, scrap_metal | "Scavenge" |
| (other) | "Harvest" |

### Harvest Flow

```
Player triggers ProximityPrompt
  → Resources.Harvest(nodeId, harvestYield)
    → Returns (amount, resourceType)
  → player:SetAttribute("Resource_" .. resourceType, currentAmount + harvested)
  → Sound effect plays at node position
  → Node model removed if depleted
```

### Server-Side Wiring

The `Triggered` connection is server-side (resource models are server-created), so no RemoteEvent is needed. The harvested quantity is stored as a player attribute (`Resource_wood`, `Resource_stone`, etc.) that inventory systems can read.

---

## 5. AudioManager Integration

**File:** `ServerScriptService/WeatherSystem/init.lua`

### What Changed

Three improvements to the audio integration:

#### A. Warning on Missing AudioManager

Previously, `getAudioManager()` silently returned `nil` if AudioManager wasn't found. Now it emits a one-shot `warn()` on first failure so developers know audio is broken, without spamming logs on every weather tick.

#### B. WeatherAudioChange BindableEvent

Created a `BindableEvent` at `script.WeatherAudioChange` that fires on every weather transition with:

```lua
{
    weather     = "rain",      -- new weather type
    previous    = "clear",     -- previous weather type
    intensity   = 0.5,         -- 0.0–0.9 audio intensity
    windSpeed   = 15,          -- current wind speed
    windDirection = Vector3,   -- current wind direction
    musicMode   = "hub",       -- suggested music mode
}
```

AudioManager can listen to this event instead of polling, and third-party audio systems can subscribe without modifying WeatherSystem source:

```lua
local WeatherSystem = require(...)
WeatherSystem.WeatherAudioChange.Event:Connect(function(data)
    myAudioSystem.setAmbience(data.weather, data.intensity)
    myAudioSystem.setWind(data.windSpeed)
end)
```

#### C. StormDamage BindableEvent

Created `script.StormDamage` BindableEvent that fires for every structure damaged during storms. AudioManager (or a future SoundDesigner) can use this to play impact sounds at damaged structure positions.

#### D. Server Bootstrap Wiring

**File:** `ServerScriptService/LucineerServer/init.lua`

Added `WorldGenerator.Generate("single")` call before `WeatherSystem.init()` in the server bootstrap. This ensures:
- Terrain exists before weather starts (so WeatherSystem can read water level)
- Resource nodes with ProximityPrompts exist before players join
- Spawn point is placed before players need to spawn
- Tide system is initialized (WorldGenerator calls `TideSystem.Init` + `Start`)

---

## Syntax Validation

All four files were checked with `lua5.1 loadfile()`. The only failures are Luau-specific syntax (type annotations `: string`, compound assignment `+=`, `goto continue`) that are valid in Roblox Luau but not Lua 5.1. These patterns are already used throughout the original codebase. Structural validation (function/end balance, proper module returns) confirms no structural errors were introduced.

---

## What's NOT Done (Audit Items Deferred)

| Audit Priority | Status | Why Deferred |
|----------------|--------|-------------|
| Chunked terrain generation | Not addressed | Requires restructuring the generation loop into coroutines — significant refactor, not a glue change |
| Heightmap smoothing | Not addressed | Post-pass blur on heightmap — algorithmic change, separate from integration |
| Inventory UI | Not addressed | Client-side ScreenGui — different concern (this was server-side glue) |
| Crafting table object | Not addressed | Physical model placement — separate task |
| Basic sky/atmosphere | Not addressed | Lighting configuration — cosmetic, separate from system wiring |
| Day/night cycle | Not addressed | Continuous ClockTime drift — additive feature, not glue |
| NPC Lucineer | Not addressed | Large feature — character model, pathfinding, dialogue UI |

---

## Files Modified

```
src/ReplicatedStorage/Lucineer/CommandExecutor.lua    (+~60 lines)
src/ServerScriptService/WorldGenerator/init.lua        (+~180 lines)
src/ServerScriptService/WeatherSystem/init.lua         (+~160 lines)
src/ServerScriptService/LucineerServer/init.lua        (+~4 lines)
```

All additions slot into existing function signatures, module returns, and pipeline stages. No existing code was replaced or removed — only additions and one small fix (wind force mass clamping).

---

*End of integration glue report.*
