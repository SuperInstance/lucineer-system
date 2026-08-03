# P0 — Memory & Vector Wiring (GAP #4) — Complete

**Date:** 2026-08-03
**Scope:** `lucineer-worker/process_v2.py`, `lucineer-memory/src/index.ts`, `lucineer-vector/src/index.ts`, both `wrangler.jsonc` files

---

## Status: ✅ FULLY WIRED

All five consequences listed in GAP_ANALYSIS.md #4 are addressed in code:

| Issue | Status | Where |
|-------|--------|-------|
| `bond_level` is a dead column | ✅ Fixed | Memory worker COALESCE fix preserves bond_level on upsert; `get_player_context()` reads it; `upsert_player_profile()` writes without clobbering |
| `build_history` is empty | ✅ Fixed | `save_to_memory()` → `log_build()` called after every job completion in `process_job()` |
| `conversations` is empty | ✅ Fixed | Player message logged at start of `process_job()`; Lucineer reply logged in `save_to_memory()` |
| 35-skill Vectorize index never queried | ✅ Fixed | `search_skills()` queries Vectorize before brain runs; results filtered at 0.6 score threshold |
| No auth on memory/vector workers | ✅ Fixed | `requireAuth()` middleware on all non-health routes in both workers; `X-Lucineer-Key` header sent on all calls from `process_v2.py` |

---

## What's Wired

### process_v2.py — Integration Points

The memory/vector integration is woven through `process_job()` in the correct order:

```
1. Log player message → memory_post("/api/memory/conversation", role="player")
2. Get world context  → api_get("/api/state/{session_id}")
3. Recall memory       → get_player_context(player_name, session_id)
   ├── GET /api/memory/player/{name}       (profile, bond_level, preferences)
   ├── GET /api/memory/builds/{name}       (recent builds, limit=5)
   └── GET /api/memory/conversations/{sid}  (recent turns, limit=5)
4. Search skills       → search_skills(message, top_k=3)
   └── POST /api/skills/query              (Vectorize semantic search)
5. Try template match   → keyword-based fast path
6. Deep brain           → call_brain(message, world_ctx, memory_ctx, skill_ctx)
7. Safety check         → Nemotron-Content-Safety-3.5
8. Post result          → api_post("/api/job/{id}/result")
9. Save to memory       → save_to_memory()
   ├── upsert_player_profile()
   ├── log_build()
   └── log_conversation(role="assistant")
```

### Environment Variables

| Variable | Used By | Purpose |
|----------|---------|---------|
| `LUCINEER_MEMORY_URL` | process_v2.py | Memory worker base URL |
| `LUCINEER_VECTOR_URL` | process_v2.py | Vector worker base URL |
| `LUCINEER_KEY` | process_v2.py | Shared secret sent as `X-Lucineer-Key` header |
| `LUCINEER_SHARED_SECRET` | memory/vector wrangler.jsonc | Expected shared secret (vars binding) |

### Auth Implementation

**Memory worker (`src/index.ts`):**
- `requireAuth()` function checks `X-Lucineer-Key` header against `env.LUCINEER_SHARED_SECRET`
- Applied to ALL routes except `/api/health`, `/`, `/health`
- Fails closed: returns 500 if secret not configured, 401 if mismatched

**Vector worker (`src/index.ts`):**
- Same `requireAuth()` pattern
- Applied to all routes except health check
- CORS locked to `lucineer-relay.casey-digennaro.workers.dev` (not `*`)
- `X-Lucineer-Key` added to CORS allowed headers

**Processor (`process_v2.py`):**
- All `memory_get()`, `memory_post()`, `vector_post()` functions send `X-Lucineer-Key: {AUTH_KEY}` header
- `AUTH_KEY` read from `LUCINEER_KEY` env var with warning if missing

### Data Flow Diagram

```
Roblox Client
    │
    ▼
Worker (Relay) ──► Durable Object (job queue)
    │
    │  poll /api/jobs/pending
    ▼
process_v2.py
    │
    ├──► GET memory/player/{name}        ──► D1 player_profiles
    ├──► GET memory/builds/{name}         ──► D1 build_history
    ├──► GET memory/conversations/{sid}   ──► D1 conversations
    ├──► POST vector/skills/query         ──► Vectorize index (35 skills)
    │
    ├──► (template match OR brain.py with injected context)
    │
    ├──► POST memory/build                ──► D1 build_history
    ├──► POST memory/conversation         ──► D1 conversations
    └──► POST memory/player               ──► D1 player_profiles (upsert)
```

### bond_level COALESCE Fix

The memory worker's player upsert uses:
```sql
INSERT INTO player_profiles (player_name, preferences, bond_level, first_seen, last_seen)
VALUES (?, ?, ?, datetime('now'), datetime('now'))
ON CONFLICT(player_name) DO UPDATE SET
  preferences = excluded.preferences,
  bond_level  = COALESCE(?, player_profiles.bond_level),  -- null = preserve
  last_seen   = datetime('now')
```

Bond level is bound as `null` when omitted from the request body, so routine profile upserts (which don't include bond_level) preserve the existing value instead of resetting to 0.

---

## Changes Made This Session

1. **`process_v2.py`** — `SKILL_SCORE_THRESHOLD` raised from `0.5` to `0.6` per GAP_ANALYSIS spec
2. **`lucineer-memory/wrangler.jsonc`** — Added `LUCINEER_SHARED_SECRET` var binding
3. **`lucineer-vector/wrangler.jsonc`** — Added `LUCINEER_SHARED_SECRET` var binding

All other wiring was already in place from prior agent work. Verified by:
- `python3 -m py_compile process_v2.py` — ✅ COMPILE OK
- Full trace of `process_job()` flow confirming memory calls before brain, save after
- Auth middleware confirmed on both worker codebases

---

## Deployment Notes

Before deploying, the actual shared secret must be set via:

```bash
# Memory worker
cd lucineer-memory
npx wrangler secret put LUCINEER_SHARED_SECRET
# (enter the real secret when prompted)

# Vector worker
cd lucineer-vector
npx wrangler secret put LUCINEER_SHARED_SECRET
```

Or set it as a plaintext var in wrangler.jsonc for development (current state — placeholder value).

The processor must have the matching key:
```bash
export LUCINEER_KEY="same-secret-value"
```

---

## Remaining Items (Not GAP #4)

- **Bond level increment logic** — currently bond_level is preserved but never incremented. A "relationship arc" implementation (incrementing based on interaction quality/count) is a product feature, not infrastructure wiring.
- **Skill uses_count increment** — the D1 `skills.uses_count` column exists for ranking but is never incremented. Would need a new endpoint or inline UPDATE in the query path.
- **Wrangler deploy** — both workers need `npx wrangler deploy` with the secret configured to go live.
