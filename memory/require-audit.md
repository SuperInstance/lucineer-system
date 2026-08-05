# Require() Audit — lucineer-roblox

**Date:** 2026-08-04
**Scope:** All 80 Lua files under `src/`
**Auditor:** Subagent (GLM-5.2)

---

## Executive Summary

The codebase has **two Rojo project files** with fundamentally different structures:
- `default.project.json` — partial mapping, flattens folder hierarchies into siblings
- `build.project.json` — fully maps all files but also flattens, using underscore-prefixed names

**Neither project file preserves the folder hierarchy** that the code's `script.Parent` / `script:WaitForChild()` patterns expect. This is the single largest class of bugs.

### Totals
- 🔴 **17 broken requires** (module won't resolve at runtime)
- 🟡 **4 entire systems not mapped** in `default.project.json` (VesselSystem, FishingSystem, EconomySystem, CrewSystem)
- 🟡 **7 RS/Lucineer audio modules** not mapped in `default.project.json`
- 🟡 **3 client modules** not mapped in `default.project.json`
- ⚪ **0 circular dependencies** (all cross-system deps use lazy require with guards)
- ⚪ **1 empty directory** (MissionSystem — no files)

---

## 1. BROKEN REQUIRES — Module Won't Resolve

### 1a. ServerConfig is sibling, not child, of LucineerServer

**default.project.json maps:**
```
SSS.LucineerServer → init.lua
SSS.ServerConfig   → ServerConfig.lua   ← flat sibling!
```

| File | Line | Require Expression | Expected Path | Actual Result |
|------|------|--------------------|---------------|---------------|
| `LucineerServer/init.lua` | 76 | `require(script:WaitForChild("ServerConfig"))` | child of LucineerServer | **FAILS** — ServerConfig is sibling in SSS |
| `BondSystem/init.lua` | 59 | `require(script.Parent:WaitForChild("LucineerServer"):WaitForChild("ServerConfig"))` | SSS.LucineerServer.ServerConfig | **FAILS** — ServerConfig is SSS.ServerConfig |

### 1b. WorldGenerator children are siblings

**default.project.json maps:**
```
SSS.WorldGenerator → init.lua
SSS.WorldConfig    → Config.lua       ← flat sibling!
SSS.Resources      → Resources.lua    ← flat sibling!
SSS.TideSystem     → TideSystem.lua   ← flat sibling!
```

| File | Line | Require Expression | Expected Path | Actual Result |
|------|------|--------------------|---------------|---------------|
| `WorldGenerator/init.lua` | 37 | `require(script.Config)` | child of WorldGenerator | **FAILS** — named "WorldConfig" in SSS |
| `WorldGenerator/init.lua` | 38 | `require(script.Resources)` | child of WorldGenerator | **FAILS** — flat in SSS |
| `WorldGenerator/init.lua` | 39 | `require(script.TideSystem)` | child of WorldGenerator | **FAILS** — flat in SSS |
| `WorldGenerator/Config.lua` | 10 | `require(script.Parent.Config)` | sibling of Config | **FAILS** — script.Parent is SSS, Config named "WorldConfig" |
| `WorldGenerator/Resources.lua` | 75,101,349 | `require(script.Parent.Config)` | sibling | **FAILS** — same issue |
| `WorldGenerator/TideSystem.lua` | 385 | `require(script.Parent.Config)` | sibling | **FAILS** — same issue |
| `VesselPhysics.lua` | 132 | `require(game.ServerScriptService.WorldGenerator.TideSystem)` | child of WorldGenerator | **FAILS** — TideSystem is SSS.TideSystem |

### 1c. EraSystem children are siblings

**default.project.json maps:**
```
SSS.EraSystem      → init.lua
SSS.CraftingSystem → CraftingSystem.lua  ← flat sibling!
SSS.Recipes        → Recipes.lua         ← flat sibling!
```

| File | Line | Require Expression | Expected Result |
|------|------|--------------------|-----------------|
| `EraSystem/init.lua` | 49 | `require(script:WaitForChild("Recipes"))` | **FAILS** — Recipes is sibling in SSS |
| `EraSystem/CraftingSystem.lua` | 30 | `require(script.Parent)` | OK — returns EraSystem module |
| `EraSystem/CraftingSystem.lua` | 31 | `require(script.Parent:WaitForChild("Recipes"))` | **FAILS** — Recipes is sibling of EraSystem, not child |
| `OnboardingSystem/init.lua` | 108 | `require(sss.EraSystem:FindFirstChild("CraftingSystem"))` | **FAILS** — CraftingSystem is SSS.CraftingSystem, not SSS.EraSystem.CraftingSystem |
| `TutorialSystem/init.lua` | 94 | `require(sss.EraSystem:FindFirstChild("CraftingSystem"))` | **FAILS** — same issue |

### 1d. WeatherSystem child is sibling with wrong name

**default.project.json maps:**
```
SSS.WeatherSystem  → init.lua
SSS.WeatherEffects → Effects.lua       ← flat sibling, renamed!
```

| File | Line | Require Expression | Expected Result |
|------|------|--------------------|-----------------|
| `WeatherSystem/init.lua` | 66 | `require(script:WaitForChild("Effects"))` | **FAILS** — module is named "WeatherEffects" in SSS, not "Effects" under WeatherSystem |

### 1e. PowerGrid children are siblings with wrong names

**default.project.json maps:**
```
SSS.PowerGrid         → init.lua
SSS.PowerVisualization → Visualization.lua  ← flat sibling, renamed!
SSS.PowerMechanical    → Mechanical.lua     ← flat sibling, renamed!
```

| File | Line | Require Expression | Expected Result |
|------|------|--------------------|-----------------|
| `PowerGrid/init.lua` | 51 | `require(vizModule)` from `script:WaitForChild("Visualization")` | **FAILS** — named "PowerVisualization" in SSS, not "Visualization" under PowerGrid |
| `PowerGrid/init.lua` | 60 | `require(mechModule)` from `script:WaitForChild("Mechanical")` | **FAILS** — named "PowerMechanical" in SSS |

*(Note: PowerGrid wraps these in pcall, so it won't crash — but Visualization and Mechanical will silently never load.)*

### 1f. VesselIntegration not mapped at all

| File | Line | Require Expression | Expected Result |
|------|------|--------------------|-----------------|
| `LucineerServer/init.lua` | 117 | `safeRequire(script:FindFirstChild("VesselIntegration"))` | **FAILS** — VesselIntegration.lua not mapped in default.project.json |

*(safeRequire prevents crash, but vessel ecosystem integration never loads.)*

---

## 2. ENTIRE SYSTEMS MISSING FROM default.project.json

Four major systems exist in `src/` but are **not mapped** in `default.project.json`:

| System | Files | Referenced By | Impact |
|--------|-------|---------------|--------|
| **VesselSystem** | 6 files (init, VesselTypes, VesselPhysics, VesselDamage, HelmController, VesselSpawner) | `LucineerServer/init.lua:113` via safeRequire | Ships, physics, helm, spawning — all dead |
| **FishingSystem** | 7 files (init, FishStocks, GearSystem, FishSpawner, CatchMechanics, MarketSystem) | `LucineerServer/init.lua:114` via safeRequire | Fishing gameplay — all dead |
| **EconomySystem** | 6 files (init, Currency, VesselUpgrades, BuildCosts, MissionBoard, EraGates) | `LucineerServer/init.lua:115` via safeRequire | Currency, missions, upgrades — all dead |
| **CrewSystem** | 5 files (init, CrewSystem, DialogueSystem, HarborLife, NPCAI) | `LucineerServer/init.lua:116` via safeRequire | Crew, dialogue, harbor NPCs — all dead |

All four are loaded via `safeRequire()` in LucineerServer, so **the game won't crash**, but these systems **silently fail to load**. The game would boot without vessels, fishing, economy, or crew.

---

## 3. CLIENT MODULES MISSING FROM default.project.json

| Module | Files | Impact |
|--------|-------|--------|
| **VesselClient** | 7 files (init, UICanvas, HelmUI, FishingUI, ChartUI, CargoUI, VesselStateUI) | All vessel-related client UI missing |
| **VisionController** | 1 file (client.lua) | Vision system client controller missing |
| **EnvironmentController** | 1 file (client.lua) | Environment client controller missing |

Only `LucineerClient/init.lua` is mapped in `default.project.json` under StarterPlayerScripts.

---

## 4. RS/LUCINEER AUDIO MODULES MISSING FROM default.project.json

Seven audio modules exist in `src/ReplicatedStorage/Lucineer/` but are **not mapped** in `default.project.json`:

| Module | Status |
|--------|--------|
| EnvironmentAudio.lua | Not mapped, not currently required by any file |
| InstrumentPanel.lua | Not mapped, not currently required by any file |
| MusicDirector.lua | Not mapped, not currently required by any file |
| SceneDirector.lua | Not mapped, not currently required by any file |
| UIAudio.lua | Not mapped, not currently required by any file |
| VesselAudio.lua | Not mapped, not currently required by any file |
| WildlifeAudio.lua | Not mapped, not currently required by any file |

**Impact:** None currently (no file requires these yet), but they are dead code that cannot be loaded if needed.

---

## 5. CIRCULAR DEPENDENCIES

**None found.** All cross-system dependencies use one of these safe patterns:
- **Lazy require** inside function body (deferred execution)
- **pcall / safeRequire wrapper** (graceful failure)
- **FindFirstChild guard** (nil check before require)

Example of correct lazy pattern:
```lua
-- VesselDamage.lua (inside function, not module top-level)
local function getWeather()
    return require(game.ServerScriptService.WeatherSystem)
end
```

---

## 6. ADDITIONAL ISSUES

### 6a. EconomySystem MissionBoard — script.Parent.Parent chain breaks in flat layout

| File | Line | Expression | Issue |
|------|------|------------|-------|
| `MissionBoard.lua` | 310, 320, 676 | `require(script.Parent.Parent:WaitForChild("EraSystem"))` | In folder layout: MissionBoard → EconomySystem → SSS ✓. In flat layout: script.Parent = SSS, script.Parent.Parent = game ✗ |
| `VesselUpgrades.lua` | 285, 413 | `require(script.Parent.Parent:WaitForChild("EraSystem"))` | Same issue |

### 6b. VesselPhysics cross-service path

| File | Line | Expression | Issue |
|------|------|------------|-------|
| `VesselPhysics.lua` | 132 | `require(game.ServerScriptService.WorldGenerator.TideSystem)` | TideSystem is SSS.TideSystem (flat), not SSS.WorldGenerator.TideSystem |

### 6c. WorldGenerator self-reference in doc comment

`WorldGenerator/init.lua` line 11 contains `require(script.ServerScriptService.WorldGenerator)` inside the opening `--[[ ]]` block comment. This is **not executable code** (it's a usage example) — no action needed.

### 6d. MissionSystem directory is empty

`src/ServerScriptService/MissionSystem/` exists but contains no files. Not referenced by any code.

### 6e. test.lua — orphan

`src/test.lua` contains only `print("hello")`. Not mapped in either project file. Not referenced.

---

## 7. SUMMARY OF REQUIRED FIXES

### Fix A: Restructure default.project.json (RECOMMENDED)

Replace flat mappings with proper folder hierarchies so `script.Parent` / `script:WaitForChild()` patterns work:

```json
"ServerScriptService": {
  "LucineerServer": {
    "$className": "Script",
    "init": { "$path": ".../LucineerServer/init.lua" },
    "ServerConfig": { "$path": ".../LucineerServer/ServerConfig.lua" },
    "VesselIntegration": { "$path": ".../LucineerServer/VesselIntegration.lua" }
  },
  "EraSystem": {
    "$className": "ModuleScript",
    "init": { "$path": ".../EraSystem/init.lua" },
    "CraftingSystem": { "$path": ".../EraSystem/CraftingSystem.lua" },
    "Recipes": { "$path": ".../EraSystem/Recipes.lua" }
  },
  "WeatherSystem": {
    "init": { "$path": ".../WeatherSystem/init.lua" },
    "Effects": { "$path": ".../WeatherSystem/Effects.lua" }
  },
  "PowerGrid": {
    "init": { "$path": ".../PowerGrid/init.lua" },
    "Visualization": { "$path": ".../PowerGrid/Visualization.lua" },
    "Mechanical": { "$path": ".../PowerGrid/Mechanical.lua" }
  },
  "WorldGenerator": {
    "init": { "$path": ".../WorldGenerator/init.lua" },
    "Config": { "$path": ".../WorldGenerator/Config.lua" },
    "Resources": { "$path": ".../WorldGenerator/Resources.lua" },
    "TideSystem": { "$path": ".../WorldGenerator/TideSystem.lua" }
  },
  // ...add VesselSystem, FishingSystem, EconomySystem, CrewSystem as folders
  // ...add VesselClient, VisionController, EnvironmentController to StarterPlayerScripts
}
```

### Fix B: Add missing systems to project mapping

Add these to `default.project.json`:
- VesselSystem (folder with 6 children)
- FishingSystem (folder with 7 children)
- EconomySystem (folder with 6 children)
- CrewSystem (folder with 5 children)
- VesselClient (folder with 7 children)
- VisionController (single file)
- EnvironmentController (single file)
- VesselIntegration (child of LucineerServer)
- 7 audio modules (children of Lucineer folder)

### Fix C: Fix EconomySystem script.Parent.Parent patterns

In `MissionBoard.lua` and `VesselUpgrades.lua`, replace:
```lua
require(script.Parent.Parent:WaitForChild("EraSystem"))
```
with:
```lua
require(game:GetService("ServerScriptService"):WaitForChild("EraSystem"))
```

### Fix D: Fix VesselPhysics TideSystem path

Replace:
```lua
require(game.ServerScriptService.WorldGenerator.TideSystem)
```
with the correct path after fixing the project structure.

---

## VERDICT

The code itself is well-written with proper lazy-loading and pcall guards. The root cause of all issues is that **`default.project.json` does not preserve the folder hierarchy** — it flattens parent-child relationships into siblings with renamed keys. Fix the project file structure (Fix A) and most issues resolve automatically.
