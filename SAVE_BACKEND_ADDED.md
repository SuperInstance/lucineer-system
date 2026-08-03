# Save Backend Endpoints — Implementation Summary

> **Completed:** 2026-08-03
> **Worker:** `lucineer-memory`
> **Files modified:** `src/index.ts`, `wrangler.jsonc`, `tsconfig.json` (new)

---

## What Was Added

### 1. R2 Bucket Binding (`wrangler.jsonc`)

Added R2 bucket binding to wrangler config:

```jsonc
"r2_buckets": [
  {
    "binding": "SAVES",
    "bucket_name": "lucineer-saves"
  }
]
```

**Action required before deploy:** Create the R2 bucket in Cloudflare:
```bash
npx wrangler r2 bucket create lucineer-saves
```

### 2. Env Interface Updated (`src/index.ts`)

Added `SAVES: R2Bucket` to the `Env` interface so the worker can read/write R2 objects.

### 3. New Endpoints (all behind AUTH_KEY check)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/save/r2/:playerName` | Save base64 build snapshot to R2 |
| GET | `/api/save/r2/:playerName` | Load build snapshot from R2 |
| POST | `/api/save/d1/:playerName/:key` | Upsert player metadata in D1 (`player_saves` table) |
| GET | `/api/save/d1/:playerName/:key` | Read a specific save value from D1 |
| GET | `/api/save/d1/:playerName/all` | Batch load all saves for a player |
| GET | `/api/era/:playerName` | Load era progression data (tries `player_eras` table, falls back to `player_saves` with key `"era"`) |
| POST | `/api/era/:playerName` | Save era progression data (same fallback strategy) |

### 4. Endpoint Details

#### R2 Save/Load
- **POST `/api/save/r2/:key`**: Accepts `{ "data": "<base64 or JSON string>" }` in the body. Stores it in R2 at the given key (e.g., `saves/Player1/builds.json`). Returns `{ success: true, key }`.
- **GET `/api/save/r2/:key`**: Fetches the object from R2. Returns `{ data: "...", key }` or 404 if not found.
- The R2 key is the full path after `/api/save/r2/` — this supports arbitrary key patterns like `saves/{player}/builds.json`, `saves/{player}/terrain.json`, `saves/{player}/legacy.json`.

#### D1 Save/Load
- Uses the existing `player_saves` table (composite PK: `player_name` + `save_key`).
- **POST**: Upserts via `INSERT ... ON CONFLICT DO UPDATE`.
- **GET single**: Returns `{ save_data, player_name, key }` or 404.
- **GET all**: Returns `{ saves: [{ save_key, save_data, updated_at }, ...] }`.

#### Era Endpoints
- Tries the dedicated `player_eras` table first (from `schema-eras.sql`).
- Falls back to `player_saves` with key `"era"` if the table doesn't exist yet.
- Returns sensible defaults (era 0, unlocked `[0]`, empty XP) if no data exists.

### 5. Auth
All new endpoints are inside the existing auth gate — the `requireAuth()` check runs before any route matching. No changes needed; all save/era endpoints inherit the same `X-Lucineer-Key` header check.

### 6. Route Ordering
- `/api/save/d1/:playerName/all` (GET) is matched **before** `/api/save/d1/:playerName/:key` (GET) via regex check, so the batch endpoint isn't shadowed.
- POST routes for D1 and era are matched by method+path, so they don't conflict with GET routes.

---

## TypeScript Compilation

```
npx tsc --noEmit → 0 errors
```

Clean compilation with `strict: true`.

---

## Remaining Steps Before Deploy

1. **Create the R2 bucket:**
   ```bash
   cd /home/eileen/projects/lucineer-memory
   npx wrangler r2 bucket create lucineer-saves
   ```

2. **Apply the save schema to D1** (if not already done):
   ```bash
   npx wrangler d1 execute lucineer-memory --remote --file=schema-saves.sql
   ```

3. **Apply the era schema to D1** (optional but recommended — era endpoints work without it via fallback):
   ```bash
   npx wrangler d1 execute lucineer-memory --remote --file=schema-eras.sql
   ```

4. **Deploy the worker:**
   ```bash
   npx wrangler deploy
   ```

5. **Set the production secret** (if not already set):
   ```bash
   npx wrangler secret put LUCINEER_SHARED_SECRET
   ```

---

## What Still Needs Fixing (Client-Side)

The endpoints now exist, but the Roblox client still has bugs that prevent them from being used. See `SAVE_SYSTEM_UPGRADE.md` §4:

- **BUG-1:** Double-URL concatenation in SaveSystem/EraSystem (must pass paths, not full URLs)
- **BUG-2:** BondSystem missing auth headers
- **BUG-3:** Race condition (concurrent save during load)
- **BUG-4:** `serializeBuilds()` has no player filter
- **BUG-5:** `deserializeBuilds()` doesn't clear existing builds first

These are Lua-side fixes — the backend is now ready.

---

*End of implementation summary.*
