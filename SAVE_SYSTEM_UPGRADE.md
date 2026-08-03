# SLACKWATER — SAVE SYSTEM UPGRADE

*Production readiness audit and upgrade plan for the SaveSystem.*

> **Audited:** 2026-08-03
> **Source:** `ServerScriptService/SaveSystem/init.lua` (877 lines)
> **Backend:** `lucineer-memory` worker (D1 + planned R2)
> **Related:** `SAVE_SYSTEM.md` (original design doc), `UNIFIED_INTEGRATION_PLAN.md`

---

## 1. CURRENT STATE — What SaveSystem Does Now

### Implemented and Working (in isolation)

| Feature | Status | Notes |
|---------|--------|-------|
| Build serialization | ✅ Complete | Captures position, size, material, color, transparency, shape, anchored, rotation, lights |
| Build deserialization | ✅ Complete | Reconstructs parts directly (bypasses CommandExecutor for instant restore) |
| Legacy builds (ghost) | ✅ Complete | Scores builds, clones top-N as semi-transparent non-collidable ghosts |
| In-memory cache | ✅ Complete | `playerSaveState` dict with inventory, eraData, bondLevel, lastBuildSave |
| Auto-save loop | ✅ Complete | Heartbeat accumulator, 60s interval, saves all connected players |
| Player lifecycle hooks | ✅ Complete | PlayerAdded → loadPlayer, PlayerRemoving → savePlayer + createLegacyBuild |
| Save debouncing | ✅ Complete | 5s debounce on `saveBuilds()` fast path |
| D1 abstraction layer | ✅ Written | `saveToD1()` / `loadFromD1()` with JSON encode/decode |
| R2 abstraction layer | ✅ Written | `saveToR2()` / `loadFromR2()` with JSON encode/decode |
| Graceful degradation | ✅ Complete | All save failures are non-fatal; game remains playable |
| Precision rounding | ✅ Complete | Positions/sizes rounded to 2 decimal places for compact JSON |
| Double-JSON-decode fallback | ✅ Present | Handles worker returning double-encoded data |

### Architecture Summary

```
SaveSystem.init()
  ├── PlayerAdded → loadPlayer (async)
  │     ├── loadFromD1 (inventory, era, bond)
  │     └── loadFromR2 (build snapshot) → deserializeBuilds
  ├── PlayerRemoving → savePlayer + createLegacyBuild
  │     ├── serializeBuilds → saveToR2
  │     └── saveToD1 (inventory, era, bond, lastSave)
  └── Heartbeat → autosaveAccumulator → saveAll (every 60s)
```

The serialization format is solid — compact JSON with versioned snapshots, metadata, and light attachment support. The deserialization is defensive with pcall guards on every part. The legacy build scoring algorithm (part count × 10 + material diversity × 5 + footprint × 0.1) is reasonable.

---

## 2. WHAT'S NEEDED FOR PRODUCTION

### Must-Have (Blocking)

| # | Requirement | Why | Severity |
|---|------------|-----|----------|
| P0-1 | **Worker endpoints exist** | The memory worker has zero `/api/save/r2/*` or `/api/save/d1/*` endpoints. Every save/load call hits a 404. | 🔴 Critical |
| P0-2 | **R2 bucket binding** | `wrangler.jsonc` has no R2 bucket. Build snapshots have nowhere to go even if endpoints existed. | 🔴 Critical |
| P0-3 | **Fix double-URL concatenation** | `Http.post(path)` prepends `_workerUrl`, but SaveSystem passes full URLs (`MEMORY_URL .. path`). Result: requests go to `WORKER_URLhttps://lucineer-memory...`. | 🔴 Critical |
| P0-4 | **Auth headers on all save calls** | SaveSystem uses `Http.post`/`Http.get` which include `X-Lucineer-Key` headers — but only if the URL is correct. Currently broken by P0-3. | 🔴 Critical |
| P0-4b | **BondSystem missing auth headers** | BondSystem bypasses `Http.post()` and calls `HttpService:RequestAsync` directly — no `X-Lucineer-Key` header. Worker rejects with 401. | 🔴 Critical |
| P0-5 | **Race condition: concurrent save during load** | `loadPlayer` spawns async R2 load in a `task.spawn`. If auto-save fires before the load completes, `serializeBuilds()` runs on a partially-loaded workspace and overwrites the R2 snapshot with incomplete data. | 🔴 Critical |
| P0-6 | **No player build ownership tracking** | `serializeBuilds()` scans the entire `LucineerBuilds` folder — it doesn't filter by player. If two players are in a server, Player A's save includes Player B's builds. | 🔴 Critical |

### Should-Have (Important for Launch)

| # | Requirement | Why |
|---|------------|-----|
| P1-1 | **Terrain modification persistence** | Design doc specifies R2 terrain snapshots. No serialization code exists for terrain at all. |
| P1-2 | **Legacy build reload on server restart** | Legacy builds are persisted to R2 (`legacy.json`) but never loaded back on server start. Ghosts vanish on restart. |
| P1-3 | **Build history logging** | The worker has a `/api/memory/build` endpoint and `build_history` table, but SaveSystem never calls it. |
| P1-4 | **World state persistence** | `world_state` table exists but SaveSystem doesn't save the global world state (era progression, constructed landmarks). |
| P1-5 | **Concurrent player builds** | The `LucineerBuilds` folder is shared. No per-player sub-folders or ownership attributes. Multiplayer is broken without this. |
| P1-6 | **Session-scoped vs. global builds** | Current design saves all builds per-player, but the design doc mentions world-level constructs that should persist globally (era unlocks change the world for everyone). |

### Nice-to-Have (Post-Launch)

| # | Requirement |
|---|------------|
| P2-1 | Save compression (gzip) for large build snapshots in R2 |
| P2-2 | Delta saves (only save changed parts, not full snapshots) |
| P2-3 | Save versioning and migration path (version 1 → 2 upgrade logic) |
| P2-4 | Offline progression sync (bond level increment on return after >24h) |
| P2-5 | Legacy build decay system (7-day inactivity cleanup) |

---

## 3. THE GAP — Specific Missing Functionality

### Gap 1: Backend Endpoints Don't Exist (P0-1, P0-2)

**The memory worker (`lucineer-memory/src/index.ts`) has no save endpoints.** The worker handles player profiles, build history, skills, conversations, world state, and achievements — but none of the `/api/save/r2/*` or `/api/save/d1/*` routes that SaveSystem calls exist in the router.

The `wrangler.jsonc` configuration has:
- ✅ D1 binding (`DB: lucineer-memory`)
- ❌ No R2 bucket binding (no `r2_buckets` in config)
- ❌ No `player_saves` table access code (table exists in `schema-saves.sql` but no worker code reads/writes it)

**Impact:** Every save and load operation silently fails. The game functions during a session (in-memory state works), but nothing persists across sessions.

### Gap 2: URL Concatenation Bug (P0-3)

```lua
-- SaveSystem does this:
Http.post(MEMORY_URL .. "/api/save/r2/" .. key, {...})

-- Http.post() internally does:
Http.request(_workerUrl .. path, "POST", body)

-- _workerUrl is set by LucineerServer.init() via Http.configure(ServerConfig.WORKER_URL, ...)
-- So the actual URL becomes:
-- ServerConfig.WORKER_URL .. "https://lucineer-memory.../api/save/r2/key"
-- → "https://relay.worker.devhttps://lucineer-memory.../api/save/r2/key"
```

**Note:** `MEMORY_URL` and `ServerConfig.WORKER_URL` may or may not be the same URL. Either way, the double concatenation is broken. The Http module expects *paths*, not full URLs.

**EraSystem has the same bug** — it calls `Http.post(MEMORY_URL .. "/api/era/load", ...)`.

**BondSystem avoids the bug** by using `HttpService:RequestAsync` directly with full URLs, but then **missing auth headers** (P0-4b) causes 401 rejection.

### Gap 3: Race Condition — Save During Load (P0-5)

```lua
function loadPlayer(playerName)
    -- ... D1 loads (synchronous) ...
    playerSaveState[playerName] = state  -- state marked loaded

    -- R2 load is async:
    task.spawn(function()
        local buildSnapshot = loadFromR2("saves/" .. playerName .. "/builds.json")
        if buildSnapshot then
            deserializeBuilds(buildSnapshot)  -- ← parts appearing over time
        end
    end)
end
```

Meanwhile, the auto-save heartbeat can fire before deserialization completes:

```lua
-- Heartbeat fires every 60s. If loadPlayer was called at t=55s:
-- t=55: loadPlayer starts, D1 loads, R2 load spawned
-- t=60: auto-save fires → savePlayer → serializeBuilds → captures EMPTY workspace
-- t=62: R2 response arrives → deserializeBuilds → parts appear (but too late, save already clobbered)
```

**Fix:** Add a `state.loading = true` flag. Check it in `savePlayer()` and skip if still loading. Clear it when the R2 load finishes.

### Gap 4: No Build Ownership (P0-6, P1-5)

```lua
local function serializeBuilds()
    local folder = ensureBuildsFolder()
    for _, descendant in ipairs(folder:GetDescendants()) do
        if descendant:IsA("BasePart") then
            -- Collects ALL parts regardless of who built them
        end
    end
end
```

There is no per-player attribution. The `LucineerBuilds` folder is a flat container. In a multiplayer server:
- Player A builds a castle
- Player B joins and builds a boat
- Auto-save fires → Player A's R2 snapshot includes Player B's boat
- Player A leaves → `createLegacyBuild` ghosts Player B's boat as Player A's

**Fix:** Use per-player sub-folders (`LucineerBuilds/{playerName}/`) or ownership attributes (`part:SetAttribute("Owner", playerName)`).

### Gap 5: EraSystem Persistence Endpoints Don't Exist

EraSystem calls `Http.post(MEMORY_URL .. "/api/era/save", ...)` and `Http.post(MEMORY_URL .. "/api/era/load", ...)` — but the memory worker has no `/api/era/*` routes. The `player_eras` table exists in `schema-eras.sql` but is inaccessible.

### Gap 6: Dual Bond Persistence Paths

BondSystem writes bond level to `player_profiles.bond_level` (via `/api/memory/player`). SaveSystem writes bond level to `player_saves` with key `"bond"` (via `/api/save/d1/.../bond`). These are **two different tables** with **two different write paths**. Bond level can diverge between them.

**Fix:** Pick one source of truth. Recommendation: use `player_profiles.bond_level` (already working via the existing worker endpoint) and remove the duplicate bond save from SaveSystem. SaveSystem can read it from BondSystem's in-memory state instead.

### Gap 7: No Terrain Persistence

The design doc specifies terrain snapshots in R2. No serialization code exists. `CommandExecutor` can call `setTerrain` but SaveSystem doesn't capture terrain state. This means terrain modifications (water filling, ground leveling) are lost on session end.

### Gap 8: No World State Save

The `world_state` table and `/api/memory/world-state` endpoint exist in the worker, and `LucineerServer.syncState()` sends snapshots every 10s. But this is session-scoped (keyed by `session_id`), not persistent across sessions. When a server restarts, the world state starts fresh.

### Gap 9: Missing `GET /api/save/d1/{player}/all` Endpoint

The design doc specifies a batch-load endpoint. The SaveSystem currently does 3 separate D1 requests (inventory, era, bond) on player join. A batch endpoint would reduce latency.

### Gap 10: No Error Recovery / Retry for Save Operations

If `saveToR2` fails, the next auto-save tick tries again — but if the R2 endpoint is consistently down (because it doesn't exist), the system spams failed requests every 60s per player. No circuit breaker, no exponential backoff on the save level (only on the HTTP level, which retries 3 times per call).

---

## 4. BUGS FOUND

### BUG-1: Double-URL Concatenation (Critical)

**Location:** `SaveSystem/init.lua` lines 174, 193, 226, 247; `EraSystem/init.lua` lines 274, 313
**Description:** `Http.post(fullUrl)` concatenates `_workerUrl .. fullUrl`, producing an invalid URL.
**Impact:** 100% of save/load HTTP requests fail. Nothing persists.
**Fix:** Change SaveSystem to pass paths only: `Http.post("/api/save/r2/" .. key)` and `Http.post("/api/save/d1/" .. playerName .. "/" .. key)`. The Http module will prepend `_workerUrl`. Remove `MEMORY_URL` from SaveSystem entirely — it should use the configured worker URL.

```lua
-- BEFORE (broken):
local MEMORY_URL = "https://lucineer-memory.casey-digennaro.workers.dev"
Http.post(MEMORY_URL .. "/api/save/r2/" .. key, {...})

-- AFTER (fixed):
Http.post("/api/save/r2/" .. key, {...})
```

**Same fix for EraSystem.**

### BUG-2: BondSystem Missing Auth Headers (Critical)

**Location:** `BondSystem/init.lua` lines 346, 376
**Description:** Uses `HttpService:RequestAsync` directly without `X-Lucineer-Key` header.
**Impact:** Worker's `requireAuth()` rejects all BondSystem requests with 401.
**Fix:** Either use `Http.post()` / `Http.get()` (which include auth headers), or add the header manually:

```lua
Headers = {
    ["Content-Type"] = "application/json",
    ["X-Lucineer-Key"] = ServerConfig.AUTH_KEY,  -- add this
}
```

Better: replace direct `HttpService:RequestAsync` calls with `Http.post()` / `Http.get()`.

### BUG-3: Race Condition — Concurrent Save/Load (High)

**Location:** `SaveSystem/init.lua` `loadPlayer()` line ~370 (async R2 load via `task.spawn`)
**Description:** `loadPlayer` sets `playerSaveState[playerName].loaded = true` immediately, but build deserialization is async. If auto-save fires in the gap, `serializeBuilds()` captures a partially-loaded workspace and overwrites the R2 snapshot with incomplete data.
**Impact:** Intermittent data loss — builds disappear from R2 snapshots.
**Fix:**

```lua
local function loadPlayer(playerName)
    local state = {
        loaded = false,        -- ← not loaded until R2 completes
        loading = true,        -- ← flag for savePlayer to check
        lastBuildSave = 0,
        -- ...
    }
    playerSaveState[playerName] = state

    -- ... D1 loads ...

    task.spawn(function()
        local buildSnapshot = loadFromR2("saves/" .. playerName .. "/builds.json")
        if buildSnapshot and buildSnapshot.parts then
            deserializeBuilds(buildSnapshot)
        end
        state.loading = false
        state.loaded = true
    end)
end

-- In savePlayer:
local function savePlayer(playerName)
    local state = playerSaveState[playerName]
    if not state or state.loading then return false end  -- ← skip if loading
    -- ... proceed with save ...
end
```

### BUG-4: serializeBuilds() Has No Player Filter (Critical)

**Location:** `SaveSystem/init.lua` `serializeBuilds()` 
**Description:** Scans entire `LucineerBuilds` folder with no player attribution. In multiplayer, saves Player B's builds into Player A's snapshot.
**Impact:** Cross-contamination of build data in multiplayer servers.
**Fix:** Add player parameter and use per-player folders or attributes:

```lua
local function serializeBuilds(playerName)
    local folder = ensureBuildsFolder()
    local playerFolder = folder:FindFirstChild(playerName)
    if not playerFolder then return { version = SAVE_VERSION, timestamp = os.time(), parts = {}, lights = {}, metadata = { partCount = 0, lightCount = 0 } } end
    -- ... scan playerFolder instead of folder ...
end
```

### BUG-5: deserializeBuilds() Doesn't Clear Existing Builds First

**Location:** `SaveSystem/init.lua` `deserializeBuilds()`
**Description:** When loading builds, parts are added to `LucineerBuilds` without clearing existing content. If a player has builds from the current session (e.g., rejoin without server restart), duplicate parts appear.
**Impact:** Overlapping/duplicate parts on rejoin.
**Fix:** Clear the player's build folder before deserializing:

```lua
local function deserializeBuilds(data, playerName)
    local folder = ensureBuildsFolder()
    local playerFolder = folder:FindFirstChild(playerName)
    if playerFolder then playerFolder:Destroy() end
    playerFolder = Instance.new("Folder")
    playerFolder.Name = playerName
    playerFolder.Parent = folder
    -- ... create parts in playerFolder ...
end
```

### BUG-6: Legacy Build Survives Player Return (Medium)

**Location:** `SaveSystem/init.lua` — no cleanup on PlayerAdded
**Description:** When a player returns, their legacy ghost should dissolve (per design doc §6). But `loadPlayer` never checks for or removes existing legacy builds.
**Impact:** Ghost builds persist alongside real builds when a player returns.
**Fix:** In `loadPlayer`, scan `LegacyBuilds` for ghosts with `LegacyOwner == playerName` and destroy them.

### BUG-7: HTTP Timeout on Load Blocks Player (Medium)

**Location:** `SaveSystem/init.lua` `loadPlayer()` — D1 loads are synchronous
**Description:** `loadFromD1` calls `Http.get()` which uses `HttpService:RequestAsync` (synchronous). Three sequential D1 loads on player join means ~3 HTTP round-trips blocking the load. With retry+backoff, worst case is 3 × (3 retries × up to 4s backoff) = 36s.
**Impact:** Players wait up to 36s on join if the worker is slow.
**Fix:** Run D1 loads in parallel via `task.spawn`, or implement a batch endpoint.

### BUG-8: `RunService.Heartbeat` Fires Every Frame (Low)

**Location:** `SaveSystem/init.lua` auto-save loop
**Description:** The Heartbeat connection fires every frame (~60fps). The accumulator check is correct, but creating a new closure every frame for the lifetime of the server is unnecessary overhead. Not a bug per se, but `task.spawn(function() while true do task.wait(AUTOSAVE_INTERVAL); saveAll() end end)` is lighter weight.
**Impact:** Minor performance overhead.
**Fix:** Use a `while true do task.wait()` loop instead of Heartbeat accumulator.

### BUG-9: createLegacyBuild Uses to.string(part.Material) Instead of part.Material.Name (Very Low)

**Location:** `SaveSystem/init.lua` `scoreBuild()`
**Description:** `tostring(part.Material)` returns `"Enum.Material.SmoothPlastic"` in Luau, not `"SmoothPlastic"`. The material set keys will all have the `Enum.Material.` prefix, which is harmless (it's just used for diversity counting) but inconsistent with the serialization format.
**Impact:** None functional — just cosmetic string inconsistency.
**Fix:** Use `part.Material.Name` directly.

---

## 5. INTEGRATION PLAN — Memory Worker (D1) Connection

### Phase 1: Worker Endpoints (must be done first)

Add these routes to `lucineer-memory/src/index.ts`:

```typescript
// ─── Save System: D1 Key-Value ──────────────────────

// POST /api/save/d1/:playerName/:key — write a save value
if (path.startsWith("/api/save/d1/") && method === "POST") {
  const parts = path.split("/api/save/d1/")[1].split("/");
  const playerName = decodeURIComponent(parts[0]);
  const saveKey = parts[1];
  if (!playerName || !saveKey) return error("playerName and key are required");

  const body = await parseBody(request);
  const saveData = String(body.save_data || body.data || "");
  if (!saveData) return error("save_data is required");

  await env.DB.prepare(
    `INSERT INTO player_saves (player_name, save_key, save_data, updated_at)
     VALUES (?, ?, ?, ?)
     ON CONFLICT(player_name, save_key) DO UPDATE SET
       save_data = excluded.save_data,
       updated_at = excluded.updated_at`
  ).bind(playerName, saveKey, saveData, Math.floor(Date.now() / 1000)).run();

  return json({ success: true });
}

// GET /api/save/d1/:playerName/:key — read a save value
if (path.startsWith("/api/save/d1/") && method === "GET") {
  const parts = path.split("/api/save/d1/")[1].split("/");
  const playerName = decodeURIComponent(parts[0]);
  const saveKey = parts[1];
  if (!playerName || !saveKey) return error("playerName and key are required");

  const result = await env.DB.prepare(
    `SELECT save_data FROM player_saves WHERE player_name = ? AND save_key = ?`
  ).bind(playerName, saveKey).first();

  if (!result) return error("not found", 404);
  return json({ save_data: result.save_data });
}

// GET /api/save/d1/:playerName/all — batch load all saves for a player
if (path.match(/^\/api\/save\/d1\/[^/]+\/all$/) && method === "GET") {
  const playerName = decodeURIComponent(path.split("/api/save/d1/")[1].replace("/all", ""));
  const results = await env.DB.prepare(
    `SELECT save_key, save_data FROM player_saves WHERE player_name = ?`
  ).bind(playerName).all();

  return json({ saves: results.results });
}
```

### Phase 2: R2 Bucket Binding

Add to `wrangler.jsonc`:

```jsonc
{
  "r2_buckets": [
    {
      "binding": "SAVES",
      "bucket_name": "lucineer-saves",
      "preview_bucket_name": "lucineer-saves-preview"
    }
  ]
}
```

Then add R2 endpoints to the worker:

```typescript
// Update Env interface:
export interface Env {
  DB: D1Database;
  SAVES: R2Bucket;
  LUCINEER_SHARED_SECRET: string;
}

// POST /api/save/r2/* — write to R2
if (path.startsWith("/api/save/r2/") && method === "POST") {
  const key = path.split("/api/save/r2/")[1];
  if (!key) return error("R2 key is required");

  const body = await parseBody(request);
  const data = String(body.data || "");
  if (!data) return error("data is required");

  await env.SAVES.put(key, data);
  return json({ success: true, key });
}

// GET /api/save/r2/* — read from R2
if (path.startsWith("/api/save/r2/") && method === "GET") {
  const key = path.split("/api/save/r2/")[1];
  if (!key) return error("R2 key is required");

  const object = await env.SAVES.get(key);
  if (!object) return error("not found", 404);
  const text = await object.text();
  return json({ data: text });
}
```

### Phase 3: Fix Roblox Client (SaveSystem)

1. Remove `MEMORY_URL` constant from SaveSystem
2. Change all `Http.post(MEMORY_URL .. path)` → `Http.post(path)`
3. Same for EraSystem
4. Fix BondSystem to use `Http.post()` / `Http.get()` instead of raw `HttpService:RequestAsync`
5. Add race condition guard (`state.loading` flag)
6. Add per-player build folders
7. Clear legacy builds on player return

### Phase 4: Schema Migration

Ensure `schema-saves.sql` has been applied to the D1 database:

```bash
npx wrangler d1 execute lucineer-memory --remote --file=schema-saves.sql
```

Verify the `player_saves` table exists:

```sql
SELECT name FROM sqlite_master WHERE type='table' AND name='player_saves';
```

### Phase 5: Era Persistence Endpoints

Add `/api/era/save` and `/api/era/load` to the worker, or refactor EraSystem to use the generic `/api/save/d1/` endpoints with key `"era"`.

**Recommendation:** Use the generic save endpoints. EraSystem already calls `saveToD1`/`loadFromD1` pattern. Just route it through the generic D1 save API instead of custom endpoints.

---

## 6. DATA SCHEMA — What Gets Saved Where

### D1 Table: `player_saves` (Small Data)

| save_key | save_data format | Example | Size |
|----------|-----------------|---------|------|
| `inventory` | JSON: `{item: count}` | `{"wood": 12, "stone": 5, "wire": 30}` | < 4 KB |
| `era` | JSON: `{currentEra, unlockedEras, eraXP}` | `{"currentEra": 2, "unlockedEras": [0,1,2], "eraXP": {"0": 5, "1": 3, "2": 1}}` | < 2 KB |
| `lastSave` | JSON: `{buildSnapshotR2, terrainR2, timestamp}` | `{"buildSnapshotR2": "saves/Player1/builds.json", "timestamp": 1700000000}` | < 0.5 KB |

### D1 Table: `player_profiles` (Existing — Bond Level)

| Column | Format | Example |
|--------|--------|---------|
| `player_name` | TEXT (PK) | `"Player1"` |
| `bond_level` | INTEGER | `3` |
| `preferences` | TEXT (JSON) | `{"theme": "dark"}` |
| `first_seen` | TEXT | `"2026-08-01T12:00:00Z"` |
| `last_seen` | TEXT | `"2026-08-03T14:30:00Z"` |

> **Note:** Bond level should use `player_profiles` as the single source of truth (already wired via BondSystem). Do NOT duplicate it in `player_saves`.

### D1 Table: `build_history` (Existing — Build Log)

| Column | Format | Example |
|--------|--------|---------|
| `session_id` | TEXT | `"123456-Studio"` |
| `player_name` | TEXT | `"Player1"` |
| `description` | TEXT | `"Built a castle with 47 parts"` |
| `command_count` | INTEGER | `47` |
| `location` | TEXT (JSON) | `{"center": [125, 12, -40], "radius": 50}` |
| `created_at` | TEXT | `"2026-08-03T14:30:00Z"` |

### R2 Bucket: `lucineer-saves` (Large Data)

| Key Pattern | Content | Size Range |
|-------------|---------|------------|
| `saves/{player}/builds.json` | Full build snapshot (all parts, lights, metadata) | 5–500 KB |
| `saves/{player}/terrain.json` | Terrain modification snapshot | 2–100 KB |
| `saves/{player}/legacy.json` | Legacy build metadata (part count, score, timestamp) | < 1 KB |

### Build Snapshot Format (R2)

```json
{
  "version": 1,
  "playerName": "Player1",
  "timestamp": 1700000000,
  "parts": [
    {
      "name": "CastleWall_North",
      "className": "Part",
      "position": { "x": 125.50, "y": 12.00, "z": -40.30 },
      "size": { "x": 16.00, "y": 8.00, "z": 2.00 },
      "material": "Stone",
      "color": "#8B7355",
      "transparency": 0,
      "shape": "Block",
      "anchored": true,
      "rotation": { "x": 0.00, "y": 90.00, "z": 0.00 }
    }
  ],
  "lights": [
    {
      "name": "TorchLight",
      "lightType": "PointLight",
      "parent": "CastleWall_North",
      "range": 16,
      "brightness": 2,
      "color": "#FF8800"
    }
  ],
  "metadata": {
    "partCount": 47,
    "lightCount": 3
  }
}
```

### In-Memory Only (Never Persisted)

| Data | Why |
|------|-----|
| NPC positions | NPCs respawn at anchors each session |
| Ambient particles | Cosmetic, regenerated from era config |
| Weather state | Temporal, starts from era default |
| Active build animations | Transient, only during construction |
| Active sound instances | Recreated on load from era config |
| Conversational context | Session-scoped (journal observations persist separately via `/api/memory/conversation`) |

---

## 7. IMPLEMENTATION PRIORITY

### Sprint 1: Make Saves Actually Work (Day 1–2)

1. **Add R2 binding to `wrangler.jsonc`** and deploy
2. **Add save endpoints to memory worker** (D1 + R2 routes from Phase 1 & 2 above)
3. **Apply `schema-saves.sql` to D1**
4. **Fix double-URL bug** in SaveSystem and EraSystem (remove `MEMORY_URL`, use paths)
5. **Fix BondSystem auth headers** (switch to `Http.post()`/`Http.get()`)
6. **Test end-to-end**: build → save → leave → rejoin → builds restored

### Sprint 2: Multiplayer Safety (Day 3–4)

7. **Add per-player build folders** (`LucineerBuilds/{playerName}/`)
8. **Add player filter to `serializeBuilds(playerName)`**
9. **Fix race condition** (`state.loading` guard)
10. **Clear existing builds before deserialization**
11. **Remove legacy ghosts on player return**

### Sprint 3: Completeness (Day 5–7)

12. **Add terrain serialization** (`serializeTerrain()` / `deserializeTerrain()`)
13. **Add legacy build reload on server start** (scan R2 for all `legacy.json` keys)
14. **Wire build history logging** (call `/api/memory/build` after each build batch)
15. **Add batch D1 load endpoint** (`/api/save/d1/{player}/all`)
16. **Add circuit breaker for save failures** (skip saves after N consecutive failures)

### Sprint 4: Polish (Post-Launch)

17. Delta saves (only changed parts)
18. Save compression (gzip in R2)
19. Save versioning and migration
20. Legacy build decay system (7-day cleanup cron)

---

## 8. SUMMARY

The SaveSystem's serialization/deserialization logic is well-designed and production-quality. The legacy build system is creative and functional. The auto-save loop with debouncing is solid.

**The critical problem is infrastructure:** the backend endpoints don't exist, the R2 bucket isn't bound, and URL concatenation is broken. These are straightforward fixes — the game logic is ready, the plumbing just needs to be connected.

| Area | Rating | Notes |
|------|--------|-------|
| Serialization | ★★★★★ | Compact, complete, handles lights and rotation |
| Deserialization | ★★★★☆ | Solid, missing clear-before-restore |
| Legacy builds | ★★★★☆ | Creative, missing reload-on-restart and dissolve-on-return |
| Auto-save loop | ★★★★☆ | Good debouncing, Heartbeat is wasteful |
| Backend integration | ★☆☆☆☆ | Endpoints don't exist, URLs broken, R2 not bound |
| Multiplayer safety | ★☆☆☆☆ | No ownership tracking, race conditions |
| Error resilience | ★★★☆☆ | Good fail-soft design, no circuit breaker |

**Bottom line:** Fix Sprint 1 items and the save system goes from 0% functional to fully working. The game logic was built correctly — it just can't talk to its backend.

---

*End of Save System Upgrade Audit.*
