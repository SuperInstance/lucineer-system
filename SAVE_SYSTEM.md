# SLACKWATER — SAVE SYSTEM DESIGN

*How world state and player builds persist across sessions.*

> **Gap #9 (Unified Integration Plan §5):** "Save System is mentioned (R2 for player saves) but not specified. How does world state persist? What happens to builds when a player logs off? How do Legacy Builds work with the DO model?" — This document answers those questions.

---

## 1. WHAT PERSISTS

### Persistent Data (survives logout)

| Category | Storage | Example |
|----------|---------|---------|
| **Player Builds** | R2 (JSON snapshot) | Part names, positions, sizes, materials, colors, transparency, shape, anchored state |
| **Player Inventory** | D1 (`player_saves`) | Items, resources, quantities as JSON |
| **Era Progression** | D1 (`player_saves`) | Current era, unlocked eras, era XP |
| **Bond Level** | D1 (`player_saves`) | Numeric bond stage (0–5) |
| **Achievement Progress** | D1 (`achievements` table, existing) | Unlocked achievement IDs + timestamps |
| **World Terrain Modifications** | R2 (JSON snapshot) | Terrain regions filled/cleared by the player |

### Non-Persistent Data (reset on session end)

| Category | Reason |
|----------|--------|
| **NPC Positions** | NPCs respawn at their home anchors each session |
| **Ambient Particles** | Cosmetic; regenerated from era world-changes |
| **Weather State** | Weather is temporal; always starts from a default per era |
| **Active Build Animations** | Transient; only matter during construction |
| **Active Sound Instances** | Recreated on load from era config |
| **Conversational Context** | Session-scoped; only journal observations persist |

---

## 2. STORAGE ARCHITECTURE

### Two-Tier Storage

```
┌─────────────────────────────────────────────────────┐
│                  CLOUDFLARE R2                       │
│                                                      │
│  Bucket: lucineer-saves                              │
│                                                      │
│  Key format:                                         │
│    saves/{playerName}/builds.json    (~50–500 KB)    │
│    saves/{playerName}/terrain.json   (~10–100 KB)    │
│                                                      │
│  These are large JSON blobs — too big for D1 rows.   │
│  Fetched on player join, cached in memory.           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                  CLOUDFLARE D1                       │
│           (lucineer-memory database)                 │
│                                                      │
│  Table: player_saves                                 │
│                                                      │
│  player_name | save_key    | save_data | updated_at  │
│  ──────────────────────────────────────────────────  │
│  Player1     | inventory   | {...}     | 1700000000  │
│  Player1     | era         | {...}     | 1700000000  │
│  Player1     | bond        | 3         | 1700000000  │
│  Player2     | inventory   | {...}     | 1700000000  │
│                                                      │
│  Small, frequently-read values that the AI pipeline  │
│  and game systems need fast access to.               │
└─────────────────────────────────────────────────────┘
```

### Why Two Tiers?

- **R2** handles large blobs (build snapshots can be hundreds of KB for complex creations). R2 has no row size limits and is cheap for storage-heavy data.
- **D1** handles small structured data (inventory counts, era numbers, bond levels). D1 is fast for indexed lookups and integrates with the existing memory worker API that the AI pipeline already queries.
- The **memory worker** (`lucineer-memory`) acts as the intermediary for D1. For R2, we add new endpoints to the same worker.

### R2 Access Pattern

The Roblox server cannot talk to R2 directly. Instead:

1. Roblox server → HTTP POST to memory worker (`/api/save/r2/{key}`)
2. Memory worker → R2 `put()` or `get()`
3. Memory worker → JSON response back to Roblox

This keeps all cloud access behind the authenticated worker endpoint.

---

## 3. WHEN SAVES HAPPEN

### Save Triggers

| Trigger | Scope | Timing |
|---------|-------|--------|
| **Build completion** | Builds only | After CommandExecutor finishes a batch |
| **Era unlock** | Era + inventory | Immediately on `EraSystem.unlockEra()` |
| **Player logout** | Full save | On `PlayerRemoving` event |
| **Auto-save heartbeat** | Full save | Every 60 seconds for all connected players |
| **Achievement unlock** | Achievements | Already handled by AchievementManager (D1) |

### Auto-Save Loop

The server's Heartbeat accumulates time. Every 60 seconds, `SaveSystem.saveAll()` iterates connected players and calls `SaveSystem.savePlayer()` for each. This is a safety net — even if a player disconnects uncleanly (crash, network drop), they lose at most 60 seconds of progress.

### Debouncing

Build-completion saves are debounced: if multiple batches complete within 5 seconds (e.g., a player rapid-firing commands), only the last one triggers a build save. The auto-save loop catches the rest.

---

## 4. LOAD FLOW

### Player Join Sequence

```
Player joins
    │
    ▼
┌──────────────────────────┐
│ 1. Fetch D1 profile      │  GET /api/memory/player/{name}
│    (bond, preferences)   │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ 2. Fetch D1 saves        │  GET /api/save/d1/{name}/all
│    (era, inventory, bond)│
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ 3. Fetch R2 build snap   │  GET /api/save/r2/saves/{name}/builds.json
│    (all parts as JSON)   │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ 4. Deserialize builds    │  SaveSystem.deserializeBuilds(data)
│    into LucineerBuilds   │  → creates Parts via CommandExecutor
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ 5. Apply terrain mods    │  SaveSystem.applyTerrain(data)
│    from R2 snapshot      │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ 6. Player ready          │  World state reconstructed
└──────────────────────────┘
```

### Load Failure Handling

If any step fails (network error, no saved data, corrupt JSON):
- **D1 failure** → default to era 0, empty inventory, bond 0
- **R2 failure** → start with empty world (no builds reconstructed)
- **Deserialize failure** → log the error, skip the offending part, continue with the rest
- Never block player entry on save loading — loads happen async, player can play immediately

---

## 5. BUILD SERIALIZATION FORMAT

### Serialized Part (JSON)

```json
{
  "name": "CastleWall_North",
  "className": "Part",
  "position": { "x": 125.5, "y": 12.0, "z": -40.3 },
  "size": { "x": 16, "y": 8, "z": 2 },
  "material": "Stone",
  "color": "#8B7355",
  "transparency": 0,
  "shape": "Block",
  "anchored": true
}
```

### Full Build Snapshot (R2)

```json
{
  "version": 1,
  "playerName": "Player1",
  "timestamp": 1700000000,
  "parts": [
    { "name": "...", "position": {...}, ... },
    ...
  ],
  "lights": [
    { "name": "...", "type": "Point", "position": {...}, ... },
    ...
  ],
  "metadata": {
    "partCount": 47,
    "buildCount": 3
  }
}
```

### Terrain Snapshot (R2)

```json
{
  "version": 1,
  "playerName": "Player1",
  "timestamp": 1700000000,
  "modifications": [
    {
      "action": "fill",
      "position": { "x": 0, "y": 0, "z": 0 },
      "size": { "x": 16, "y": 1, "z": 16 },
      "material": "Water"
    }
  ]
}
```

---

## 6. LEGACY BUILDS

### Concept

When a player logs off, their most impressive build stays in the world as a **ghost** — semi-transparent, non-collidable, visible to other players but not modifiable. This creates a sense of persistent presence and history in the world, connecting to the viral mechanics design (UNIFIED_INTEGRATION_PLAN §4, Phase 4: "Legacy Builds — persistent presence").

### Selection Criteria

The "most impressive" build is determined by:
1. **Part count** — more parts = more impressive (weighted)
2. **Recency** — the latest build session's work is preferred
3. **Material diversity** — using varied materials scores higher
4. **Size** — larger footprint builds are more visible

In practice, the implementation selects the largest contiguous group of parts from the player's most recent build session.

### Ghost Effect

| Property | Living Build | Ghost Build |
|----------|-------------|-------------|
| Transparency | 0 (original) | 0.7 |
| CanCollide | true (original) | false |
| Parent | `LucineerBuilds` | `LegacyBuilds` folder |
| Attributes | normal | `LegacyOwner = playerName`, `LegacyTime = timestamp` |
| Interactable | yes | view-only (hover shows creator name) |

### Lifecycle

1. **Player logout** → `SaveSystem.createLegacyBuild(playerName)` called
2. Parts cloned from `LucineerBuilds`, ghost properties applied
3. Placed in `Workspace.LegacyBuilds` folder
4. Persisted in R2 under `saves/{playerName}/legacy.json`
5. On server restart, legacy builds are reloaded from all known players
6. Legacy builds decay after **7 days** of player inactivity (configurable)
7. When the original player returns, their legacy build dissolves and their real builds are loaded from the normal save

### Limits

- Maximum **3 legacy builds** per server at a time (most recent replace oldest)
- Maximum **50 parts** per legacy build (beyond that, the bounding region is sampled)
- Legacy builds do not include terrain modifications

---

## 7. D1 SCHEMA

```sql
CREATE TABLE IF NOT EXISTS player_saves (
  player_name TEXT NOT NULL,
  save_key TEXT NOT NULL,
  save_data TEXT NOT NULL,
  updated_at INTEGER NOT NULL,
  PRIMARY KEY (player_name, save_key)
);
```

### Keys in Use

| save_key | save_data format | Example |
|----------|-----------------|---------|
| `inventory` | JSON: `{item: count}` | `{"wood": 12, "stone": 5}` |
| `era` | JSON: `{currentEra, unlockedEras, eraXP}` | `{"currentEra": 2, "unlockedEras": [0,1,2], "eraXP": {"0": 5, "1": 3, "2": 1}}` |
| `bond` | JSON: `{level, stageTriggers}` | `{"level": 3, "triggers": ["argued_and_won"]}` |
| `lastSave` | JSON: `{buildSnapshotR2, terrainR2, timestamp}` | `{"buildSnapshotR2": "saves/Player1/builds.json", "terrainR2": "saves/Player1/terrain.json", "timestamp": 1700000000}` |

---

## 8. MEMORY WORKER ENDPOINTS (to be added)

The memory worker (`lucineer-memory`) needs new endpoints for save/load:

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/save/d1/{playerName}/{key}` | Write a D1 save value |
| GET | `/api/save/d1/{playerName}/{key}` | Read a D1 save value |
| GET | `/api/save/d1/{playerName}/all` | Read all D1 saves for a player |
| POST | `/api/save/r2/{key}` | Write data to R2 bucket |
| GET | `/api/save/r2/{key}` | Read data from R2 bucket |

These are in addition to the existing `/api/memory/*` endpoints.

---

## 9. INTEGRATION POINTS

### With CommandExecutor
- `SaveSystem.serializeBuilds()` scans `LucineerBuilds` folder (where CommandExecutor parents all created parts)
- `SaveSystem.deserializeBuilds()` recreates parts by calling `CommandExecutor.createPart()` for each saved part, bypassing batch animation for instant restore

### With EraSystem
- Era state is saved/loaded through `SaveSystem.saveToD1()` / `SaveSystem.loadFromD1()`
- EraSystem's existing `savePlayer`/`loadPlayer` methods can delegate to SaveSystem for D1 persistence

### With BondSystem
- Bond level stored in D1 via SaveSystem
- SaveSystem does not interpret bond logic — it just stores the number

### With LucineerServer (init.lua)
- `SaveSystem.init()` called during server bootstrap
- Auto-save loop integrated into the Heartbeat connection
- `PlayerRemoving` calls `SaveSystem.savePlayer()` + `SaveSystem.createLegacyBuild()`
- `PlayerAdded` calls `SaveSystem.loadPlayer()` (async)

---

## 10. FAILURE MODES AND RESILIENCE

| Failure | Behavior |
|---------|----------|
| R2 write fails | Log warning; D1 still saves small data; retry on next auto-save tick |
| R2 read fails | Player starts with empty world; builds are lost but game is playable |
| D1 write fails | Log warning; in-memory state still valid; retry on next tick |
| D1 read fails | Default to era 0, empty inventory; player can still build |
| JSON parse error | Skip the corrupt entry; log with player name for debugging |
| Server crash | Auto-save ensures max 60s data loss; R2 snapshots are write-once |

**Principle:** Save failures are always non-fatal. The game must remain playable even if the save system is completely down.

---

*End of Save System Design. Implementation: `ServerScriptService/SaveSystem/init.lua`.*
