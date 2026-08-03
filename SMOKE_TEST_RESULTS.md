# Lucineer Smoke Test Results

**Date:** 2026-08-03 06:18 AKDT  
**Verdict:** ✅ **ALL PASS — 17/17 assertions**

---

## Summary

| Metric | Value |
|--------|-------|
| Total assertions | 17 |
| Passed | 17 |
| Failed | 0 |
| Warnings | 0 |
| Round-trip time | 114.1s (job submission → completion) |

The core loop works **end-to-end**: message → Worker → Durable Object → Processor → brain/templates → result → memory → vector search.

---

## What Passed

### Phase 0: Service Health (3/3 ✅)
- ✅ Worker relay reachable (`/api/health` → 200, status=ok)
- ✅ Memory D1 Worker reachable (`/health` → 200, status=ok, service=lucineer-memory)
- ✅ Vector Worker reachable (`/api/health` → 200, status=ok, service=lucineer-vector)

### Phase 1: Message Submission (2/2 ✅)
- ✅ POST `/api/message` returns `jobId` (HTTP 200, status=processing)
- ✅ Job ID is non-empty string (`ae805cc60a0df6e83a6f307b0669e07c`)

### Phase 2: Job Polling (1/1 ✅)
- ✅ Job reached terminal status `complete` in 112.4s
  - Transition: `submitted → pending (0.2s) → complete (112.4s)`

### Phase 3: Build Result Validation (7/7 ✅)
- ✅ Job status is `complete`
- ✅ Result contains non-empty commands array (4 commands)
- ✅ At least one `createPart` command (3 createPart + 1 addLight)
- ✅ Parts have non-default names — **not the gray box regression**
  - Part names: `TowerBase`, `TowerBattlement`, `TowerLantern`
- ✅ Reply text exists (132 chars): *"Threw up a tower — stone shaft, battlements, beacon on top. Lantern's lit but I left the top floor open..."*
- ✅ Build commands use envelope structure (`type` + `params`) — 4/4 correct
- ✅ At least one anchored part (3/3 anchored)

### Phase 4: Memory Integration (2/2 ✅)
- ✅ Player profile exists with `bond_level` (bond_level=0, last_seen=2026-08-03)
- ✅ Build history has entries (3 builds recorded)

### Phase 5: Vector Integration (2/2 ✅)
- ✅ Vector skill search responds (HTTP 200, 3 matches)
- ✅ Top match: "Build a signal tower" (score=0.674)

---

## What Failed

Nothing. All 17 assertions passed on the final run.

---

## What Was Fixed

### 1. Python urllib blocked by Cloudflare (critical)
**Problem:** The smoke test used Python's `urllib` for HTTP requests, but Cloudflare returns 403 Forbidden for urllib's user-agent on all three Workers. The processor (`process_v2.py`) already worked around this by using `curl` via subprocess.

**Fix:** Replaced the `http_request()` function in `smoke_test.py` to use `curl` via `subprocess.run()` instead of `urllib.request.urlopen()`. This matches the pattern already used by `process_v2.py`.

**File:** `/home/eileen/projects/lucineer-worker/smoke_test.py` — replaced `http_request()` implementation and removed unused `urllib` imports.

### 2. Memory Worker health endpoint mismatch
**Problem:** The smoke test checked `/api/health` on all services, but the Memory Worker exposes its health endpoint at `/health` (without the `/api` prefix), returning 404 for `/api/health`.

**Fix:** Updated `phase_health_check()` to try both `/api/health` and `/health` paths, using whichever returns 200.

**File:** `/home/eileen/projects/lucineer-worker/smoke_test.py` — updated `phase_health_check()`.

### 3. LUCINEER_KEY not set in environment
**Problem:** The `LUCINEER_KEY` environment variable is not set in the shell or in any `.env` file. The processor daemon also runs without it (it logs a warning but continues, since `/api/message` is a public endpoint).

**Status:** Not a blocker. The smoke test was run with `LUCINEER_KEY="smoke-test-dummy"` — the Worker accepts any value for public endpoints (POST `/api/message`, GET `/api/job/:jobId`). The Memory and Vector Workers also accept any value for reads. The key is only needed for internal processor endpoints (claim/result posting), which the running processor handles via its own environment.

**Recommendation:** Set `LUCINEER_KEY` in `~/.bashrc` or a `.env` file sourced by the processor service for consistency, even though it's not currently required.

---

## What's Still Broken / Known Issues

1. **Job processing time: 112 seconds.** This is close to the client-side 120s timeout. For a simple "build a tower" (which hits the fast template path, not the deep brain), this should be much faster. The bottleneck is likely in the processor's memory/vector API calls per job or DO latency.

2. **LUCINEER_KEY not configured.** Not blocking, but should be set for security — especially if the Workers ever enable auth on public endpoints.

3. **No systemd service file for the smoke test.** The processor runs as a systemd service (`lucineer-processor.service`), but the smoke test is manual-only. Consider adding a cron or heartbeat hook.

---

## Does the Core Loop Work End-to-End?

**Yes.** The full pipeline works:

```
Roblox Client → POST /api/message → Worker (DO) → Job queued
                                                    ↓
                                            Processor polls
                                                    ↓
                                         Memory recall (D1)
                                         Skill search (Vectorize)
                                         Template match → fast path
                                                    ↓
                                         POST /api/job/:id/result
                                                    ↓
                                         Memory write-back (D1)
                                            ↓
Roblox Client ← GET /api/job/:jobId ← Worker (DO) ← Result stored
```

The build output is correct: named parts (`TowerBase`, `TowerBattlement`, `TowerLantern`), proper envelope structure, anchored, with a personality-rich reply. The gray box regression is **not present**.
