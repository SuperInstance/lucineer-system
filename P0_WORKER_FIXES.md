# P0 Worker Fixes — Implementation Summary

**Date:** 2026-08-03  
**Engineer:** Subagent (P0-worker-bugfixes)  
**Status:** ✅ All fixes applied, TypeScript compiles clean

---

## Files Modified

| File | Changes |
|------|---------|
| `lucineer-worker/src/types.ts` | Added `claimed_by`, `lease_expires_at` to Job; added `"claimed"` to JobStatus; added `claimPendingJobs` to RPC interface; fixed MessageHistoryEntry to include `sessionId` |
| `lucineer-worker/src/do/LucineerSession.ts` | Full rewrite: added `claimPendingJobs()`, alarm-based pruning, session-encoded job IDs, `claimed_by`/`lease_expires_at` columns, migration logic |
| `lucineer-worker/src/index.ts` | Session-routed DOs (no more `getByName("default")`), relaxed job ID regex to accept session-prefixed IDs, added `POST /api/jobs/claim` batch endpoint, removed push path |
| `lucineer-worker/wrangler.jsonc` | Removed `OPENCLAW_CALLBACK_URL` var (pointed at unreachable WSL private IP) |
| `lucineer-memory/src/index.ts` | Fixed `bond_level` COALESCE bug (omitting it no longer resets to 0); fixed `parseBody` errors to return 400 instead of 500 |
| `lucineer-vector/src/index.ts` | Fixed duplicate vector ID on single upsert (now uses stable `skill-{slug}` instead of `skill-{slug}-{timestamp}`) |

---

## Bug #1 — Atomic Job Claiming (GAP #6a) ✅

**Problem:** Jobs created with `status='processing'`, no atomic claim, duplicate processing, infinite loops on failure.

**Fix:**
- **New schema columns:** `claimed_by TEXT`, `lease_expires_at INTEGER` (in addition to existing `claimed_at`, `attempts`)
- **Migration:** `migrateSchema()` adds columns idempotently to existing tables; migrates old `'processing'` status to `'pending'`
- **Jobs inserted as `'pending'`** (was already done in prior pass, confirmed)
- **New `claimPendingJobs(workerId, limit)` method:**
  1. Retires jobs with `attempts >= MAX_ATTEMPTS (3)` → `status='error'`
  2. Resets expired leases (`lease_expires_at < now`, within retry limit) → `status='pending'`
  3. Selects pending jobs (`status='pending' AND claimed_at IS NULL`)
  4. Atomically transitions all selected → `status='claimed'` with `claimed_by`, `lease_expires_at`, `attempts++`
  5. Returns full Job objects with updated state
- **Lease duration:** 3 minutes (covers `DEEP_TIMEOUT=120s` plus margin)
- **New endpoint:** `POST /api/jobs/claim?workerId=<id>&limit=<n>` — preferred over the old getPendingJobs + claimJob two-step
- **Backward compat:** `getPendingJobs()` and `claimJob(jobId)` still work for existing processor code

---

## Bug #2 — Push Path to Private IP (GAP #6d) ✅

**Problem:** Worker tried to POST to `http://172.22.219.126:18789/...` (WSL private IP), which Cloudflare can't reach. Push failure caused job to error before polling could work.

**Fix:**
- Push path was already removed in a prior code pass (confirmed by reading `index.ts`)
- **Removed the `OPENCLAW_CALLBACK_URL` var** from `wrangler.jsonc` — it's dead config
- The `/api/message` handler now just returns `{ jobId, status: "processing" }` — the processor polls

---

## Bug #3 — One Durable Object for Everything (GAP #6c) ✅

**Problem:** All routes used `getByName("default")`, serializing every player through one single-threaded object.

**Fix:**
- **Session-encoded job IDs:** `generateJobId(sessionId)` produces `<urlEncodedSessionId>.<randomHex>` (e.g., `studio-1234.a1b2c3d4e5f6`)
- **`sessionIdFromJobId(jobId)`** extracts the session prefix to route `getJob`, `setJobResult`, etc. to the correct DO
- **`sessionStub(env, sessionId)`** replaces all `getByName("default")` calls — routes by session
- **Relaxed regex:** Job result/claim routes now match `^/api/job/(.+)/result$` (any chars) instead of `^/api/job/([\da-f]+)$/result$` (hex only)
- **GET /api/job/:jobId** also routes by session extracted from the job ID
- Fallback: if no session prefix in job ID, routes to `"default"` DO

---

## Bug #4 — Jobs/History Never Pruned (GAP #6b) ✅

**Problem:** `jobs` and `message_history` tables grow without bound, eventually exceeding DO SQLite storage limits.

**Fix:**
- **Alarm-based cleanup** scheduled every 1 hour in the DO constructor
- **`alarm()` method:**
  - Deletes completed/errored jobs older than 24h (`completed_at < cutoff`)
  - Deletes message history older than 24h
  - Calls `cleanupStaleJobs()` to reclaim expired leases
  - Re-schedules next alarm

---

## Bug #5 — Memory/Vector Worker Auth (GAP #4) ✅

**Problem (from gap analysis):** Memory and vector Workers had no authentication.

**Finding:** Auth was **already implemented** in both Workers in a prior code pass:
- `lucineer-memory/src/index.ts` — `requireAuth()` middleware checks `X-Lucineer-Key` against `LUCINEER_SHARED_SECRET`; all routes except `/api/health` require auth
- `lucineer-vector/src/index.ts` — same `requireAuth()` pattern
- Both fail-closed if `LUCINEER_SHARED_SECRET` is not configured

**Additional fixes applied:**
- **Memory: bond_level COALESCE fix** — `INSERT ... ON CONFLICT DO UPDATE SET bond_level = COALESCE(?, player_profiles.bond_level)` — omitting `bond_level` from a profile write now preserves the existing value instead of resetting to 0
- **Memory: parseBody 400 fix** — invalid JSON returns 400 (client error) instead of 500 (server error)
- **Vector: stable upsert ID** — single skill upsert now uses `skill-{slug(name)}` (matching the batch seed path) instead of `skill-{slug(name)}-{Date.now()}`, preventing duplicate vectors on re-upsert
- **Vector: CORS** — already restricted to relay worker URL (not `*`)

---

## TypeScript Compilation

```
$ npx tsc --noEmit
(no output — zero errors)
```

---

## What the Processor Needs to Change

The Python processor (`process_v2.py`) should be updated to use the new batch claim endpoint:

```python
# Old (race-prone):
jobs = api_get("/api/jobs/pending")["jobs"]
for job in jobs:
    claimed = api_post(f"/api/job/{job['id']}/claim", {})

# New (atomic):
result = api_post("/api/jobs/claim?workerId=lucineer-proc-1&limit=5", {})
for entry in result["jobs"]:
    job = entry["job"]
    # process job...
```

The old endpoints still work for backward compatibility.

---

## Deployment Notes

1. **Deploy Workers:** `cd lucineer-worker && npx wrangler deploy` (run from project root)
2. **Redeploy memory + vector Workers** with `LUCINEER_SHARED_SECRET` set as a secret
3. **DO migration:** The `migrateSchema()` method handles adding `claimed_by` and `lease_expires_at` columns automatically — no manual migration needed
4. **Wrangler migration tag:** A new migration tag may be needed if the DO class signature changed (the constructor now accepts `Env` type parameter). Add to `wrangler.jsonc`:
   ```jsonc
   {"tag": "v2", "new_sqlite_classes": ["LucineerSession"]}
   ```
