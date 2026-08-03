# SaveSystem — Critical Bug Fixes

> **Fixed:** 2026-08-03
> **Source:** `ServerScriptService/SaveSystem/init.lua`, `ServerScriptService/BondSystem/init.lua`
> **Audit:** `SAVE_SYSTEM_UPGRADE.md` (BUG-1 through BUG-4)

---

## Bug 1: Double-URL Concatenation (CRITICAL) ✅

**Problem:** `Http.post(MEMORY_URL .. path)` produced invalid URLs because `Http.post()` internally prepends the configured `_workerUrl`. Result: every request went to `WORKER_URLhttps://lucineer-memory...`.

**Fix:** Removed the `MEMORY_URL` constant entirely from SaveSystem. All `Http.post()` and `Http.get()` calls now pass **paths only** (e.g. `"/api/save/r2/" .. key`). The Http module prepends the configured worker URL automatically.

**Files changed:** `SaveSystem/init.lua` — 4 call sites fixed (`saveToR2`, `loadFromR2`, `saveToD1`, `loadFromD1`).

---

## Bug 2: BondSystem Missing Auth Headers (CRITICAL) ✅

**Problem:** BondSystem bypassed the `Http` module and called `HttpService:RequestAsync` directly with only `Content-Type` header — no `X-Lucineer-Key`. The worker's `requireAuth()` middleware rejected all BondSystem requests with 401.

**Fix:** Added `ServerConfig` require at the top of BondSystem. Both `persistBond()` (POST) and `loadBond()` (GET) now include:
```lua
["X-Lucineer-Key"] = ServerConfig.AUTH_KEY
```

**Files changed:** `BondSystem/init.lua` — `persistBond()` (line ~364), `loadBond()` (line ~392).

---

## Bug 3: Race Condition — Save During Async Load (CRITICAL) ✅

**Problem:** `loadPlayer()` set `state.loaded = true` immediately, but build deserialization ran async via `task.spawn`. If auto-save fired in the gap, `serializeBuilds()` captured an empty workspace and overwrote the R2 snapshot.

**Fix:** Added `state.loading = true` flag set at state creation. Both `savePlayer()` and `saveBuilds()` now check `if state.loading then return false end` before proceeding. The flag is cleared (`state.loading = false; state.loaded = true`) only after `deserializeBuilds()` completes inside the `task.spawn`.

**Files changed:** `SaveSystem/init.lua` — `loadPlayer()`, `savePlayer()`, `saveBuilds()`.

---

## Bug 4: No Build Ownership Filter (CRITICAL) ✅

**Problem:** `serializeBuilds()` scanned the entire shared `LucineerBuilds` folder. In multiplayer, Player A's save included Player B's builds. `deserializeBuilds()` also wrote to the shared folder with no player attribution.

**Fix:**
1. Added `ensurePlayerBuildFolder(playerName)` helper that creates per-player sub-folders (`LucineerBuilds/{playerName}/`).
2. `serializeBuilds(playerName)` now accepts a player parameter and scans only that player's folder.
3. `deserializeBuilds(data, playerName)` creates/clears the player's sub-folder, parents restored parts there, and sets `part:SetAttribute("ownerId", playerName)` on each part.
4. `createLegacyBuild(playerName)` only scans the leaving player's folder.
5. All internal call sites (`savePlayer`, `saveBuilds`) pass `playerName` through.

**Files changed:** `SaveSystem/init.lua` — `serializeBuilds()`, `deserializeBuilds()`, `createLegacyBuild()`, `savePlayer()`, `saveBuilds()`.

---

## Syntax Verification

```
lua5.1 loadfile check:
  SaveSystem/init.lua → OK ✓
  BondSystem/init.lua → uses Luau type annotations (--!strict, : type) — fails lua5.1 parser
                         but valid in Roblox Luau. No new non-Luau syntax introduced.
```

---

## API Changes

| Function | Before | After |
|----------|--------|-------|
| `SaveSystem.serializeBuilds()` | No params, scans all builds | `serializeBuilds(playerName)` — per-player |
| `SaveSystem.deserializeBuilds(data)` | No player param | `deserializeBuilds(data, playerName)` — per-player folder + ownerId |
| `SaveSystem.savePlayer(playerName)` | No loading guard | Skips if `state.loading == true` |
| `SaveSystem.saveBuilds(playerName)` | No loading guard | Skips if `state.loading == true` |

**Note for CommandExecutor integration:** When creating new parts via CommandExecutor, set `part:SetAttribute("ownerId", playerName)` and parent to `LucineerBuilds/{playerName}/` folder. This is the other half of Bug 4 — SaveSystem now expects ownership attribution on parts.

---

*End of bug fix summary.*
