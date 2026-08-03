# A1 — Source Unification Complete

**Date:** 2026-08-03
**Scope:** `lucineer-roblox/`, `vibe-world/`, `lucineer-worker/`

---

## What Was Done

### 1. Single Source of Truth Established

`/home/eileen/projects/lucineer-roblox/` is now the canonical source for all Roblox Lua code.

- **38 source files** across ReplicatedStorage, ServerScriptService, and StarterPlayer (35,577 total lines)
- Mapped by `default.project.json` (Rojo project file) — well-structured, no changes needed
- All game logic lives here: NPCManager, BondSystem, EraSystem, WeatherSystem, WorldGenerator, PowerGrid, SaveSystem, TutorialSystem, AchievementManager, OnboardingSystem, VibeCodeExecutor, etc.

### 2. vibe-world/src/ — Vestigial, Documented for Removal

`vibe-world/src/` contains **4 files (562 lines)** — this is the **original prototype** from before the codebase was restructured:

| File | Lines | Purpose | Status |
|---|---|---|---|
| `Server.lua` | 136 | Old world setup, chat commands, baseplate | **Superseded** by `lucineer-roblox/src/ServerScriptService/LucineerServer/init.lua` |
| `Client.lua` | 79 | Old welcome UI, vibe console | **Superseded** by `lucineer-roblox/src/StarterPlayer/StarterPlayerScripts/LucineerClient/init.lua` |
| `Config.lua` | 24 | Old world/player config | **Superseded** by `lucineer-roblox/src/ReplicatedStorage/Lucineer/Config.lua` |
| `Commands.lua` | 323 | Old chat commands (spawn, weather, teleport) | **Superseded** by `CommandExecutor.lua` + processor templates |

**Action:** `vibe-world/src/` should be deleted once Rojo build is verified in Studio. Not deleted now because the old `.rbxlx` files still reference these scripts and Casey may want to test side-by-side.

### 3. vibe-world/*.rbxlx — Build Outputs, Not Source

Two `.rbxlx` files exist in `vibe-world/`:

| File | Purpose |
|---|---|
| `lucineer-ready.rbxlx` | The place file that was manually authored/synced. Contains **stale embedded copies** of the Lua source. |
| `lucineer-ready-v2.rbxlx` | A second variant. Same problem. |

Both are **build outputs**, not source files. They contain embedded copies of Lua scripts that diverge from `lucineer-roblox/src/`. **Any fix applied to `src/` will NOT reach the game through these files.**

**The fix:** Use `rojo build` to generate fresh `.rbxlx` from `lucineer-roblox/src/`. The `build.sh` script handles this.

### 4. Rojo Not Installed — Documented

Rojo is not currently available on the system. The `build.sh` script detects this and prints install instructions:

```
cargo install rojo --version 7.5.1
# or download from https://github.com/rojo-rbx/rojo/releases
```

Once installed, the build command is:
```bash
cd /home/eileen/projects/lucineer-roblox
./build.sh
# Output: ../vibe-world/lucineer-built.rbxlx
```

For live development:
```bash
./build.sh --serve
# Connect from Studio using the Rojo plugin (port 34872)
```

### 5. PROTOCOL.md — API Contract Documented

Created `/home/eileen/projects/lucineer-roblox/PROTOCOL.md` with:
- All 6 HTTP endpoints documented with example JSON payloads
- Build command envelope format (`createPart`, `addLight`, `addParticle`, `sendMessage`)
- Color/vector format specifications
- Session identity construction
- Error handling matrix (don't retry 4xx!)
- Auth requirements per endpoint

Sources used:
- `lucineer-worker/src/index.ts` — actual route handlers
- `lucineer-worker/src/types.ts` — TypeScript type definitions
- `lucineer-worker/src/do/LucineerSession.ts` — Durable Object implementation
- `lucineer-worker/process_v2.py` — processor templates (for build command shapes)
- `lucineer-system/GAP_ANALYSIS.md` — contract mismatch documentation

### 6. build.sh — Build Script Created

Created `/home/eileen/projects/lucineer-roblox/build.sh`:
- Checks for Rojo installation, prints install help if missing
- `rojo build default.project.json -o ../vibe-world/lucineer-built.rbxlx`
- Supports custom output path: `./build.sh /path/to/output.rbxlx`
- Supports live-sync mode: `./build.sh --serve`
- Executable (`chmod +x` applied)

---

## File Inventory

### lucineer-roblox/src/ — THE SOURCE OF TRUTH (38 files, 35,577 lines)

**ReplicatedStorage/Lucineer/ (16 modules):**
AudioManager, BeatClock, BuildAnimator, ChatHandler, CinematicController, CommandExecutor, Config, FilterGate, Http, Poller, UIManager, VibeCoder, VibeCoderDialogue, VoiceLines, VoiceLinesData, WorldScanner

**ServerScriptService/ (22 modules across 11 systems):**
LucineerServer, NPCManager, AchievementManager, BondSystem, EraSystem (+ CraftingSystem, Recipes), SaveSystem, TutorialSystem, WeatherSystem (+ Effects), PowerGrid (+ Mechanical, Visualization), WorldGenerator (+ Config, Resources, TideSystem), VibeCodeExecutor, OnboardingSystem

**StarterPlayer/StarterPlayerScripts/ (1 module):**
LucineerClient

### vibe-world/src/ — VESTIGIAL (4 files, 562 lines)

Old prototype. **Do not edit.** Delete after Rojo build is verified.

---

## Next Steps for Casey

1. **Install Rojo:**
   ```bash
   cargo install rojo --version 7.5.1
   ```
   Or download the prebuilt binary from [rojo releases](https://github.com/rojo-rbx/rojo/releases).

2. **Install the Rojo Studio plugin** (Rojo Manager in Studio's plugin marketplace).

3. **Build the place file:**
   ```bash
   cd /home/eileen/projects/lucineer-roblox
   ./build.sh
   ```

4. **Open `lucineer-built.rbxlx` in Studio** — verify all scripts are present under the correct services.

5. **Delete `vibe-world/src/`** once the Rojo build is confirmed working.

6. **Delete `vibe-world/lucineer-ready.rbxlx` and `lucineer-ready-v2.rbxlx`** — they contain stale embedded Lua and will cause confusion.

7. **Use `rojo serve` for ongoing development** — live sync means edits in your editor appear in Studio instantly. Never edit scripts directly in Studio.
