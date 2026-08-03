# 🔴 LIVE PLAYTEST RESULTS — Slackwave System
**Date:** 2026-08-03  
**Tester:** Automated subagent playtest  
**Duration:** ~45 minutes  
**Verdict:** System is **NOT production-ready**. Multiple critical bugs prevent basic operation.

---

## Executive Summary

The Slackwater system was subjected to 5 playtest scenarios (18 total messages) covering first-time players, returning players, all build templates, edge cases, and rapid fire. **ZERO of the 18 test messages were successfully processed during the test window.** The processor was stuck in a loop re-processing stale jobs from previous test sessions, each taking 60–100 seconds due to brain timeouts.

Three critical bugs were discovered, plus numerous design issues that make the system unusable in its current state.

---

## Critical Bugs Found

### 🔴 BUG #1: Missing LUCINEER_KEY in systemd service (FIXED)

**Severity:** Critical — processor cannot claim jobs  
**Status:** Fixed during test  

The deployed systemd service file at `/home/eileen/.config/systemd/user/lucineer-processor.service` was missing the `LUCINEER_KEY` environment variable. The processor's `_check_auth_failure()` function detected this but only logged a warning, continuing to run in a no-op state forever.

**Impact:** The processor ran for hours appearing healthy ("Heartbeat: OK (0 pending jobs)") while actually being unable to authenticate. Every job sat unprocessed.

**Evidence:**
```
# The OLD service file (missing auth):
Environment=LUCINEER_MEMORY_URL=https://lucineer-memory.casey-digennaro.workers.dev
# LUCINEER_KEY was MISSING

# Processor env var check confirmed it was empty:
$ cat /proc/<PID>/environ | tr '\0' '\n' | grep LUCINEER
LUCINEER_MEMORY_URL=https://lucineer-memory.casey-digennaro.workers.dev
# No LUCINEER_KEY!
```

The service file at `/home/eileen/projects/lucineer-worker/lucineer-processor.service` (the project template) HAD the key, but the deployed user service didn't. The two files were out of sync.

**Fix applied:** Added `LUCINEER_KEY` and `LUCINEER_VECTOR_URL` to the deployed service file and restarted.

**Root cause:** The deployed service file was created earlier (possibly during initial setup) and never updated when the project template was revised. There's no sync mechanism between the template and the deployed file.

---

### 🔴 BUG #2: Stale job graveyard — processor drowns in old jobs

**Severity:** Critical — blocks all new job processing  
**Status:** Unfixed  

The Durable Object queue contained **50+ stale jobs** from previous test sessions (cognition tests, earlier playtests, smoke tests). These jobs had:
- Empty `playerName` (showed as "friend")
- Empty `message` (showed as "")
- `attempts` count of 1–2 (not yet at MAX_ATTEMPTS=3)

Each stale job goes through the full brain pipeline (because empty messages don't match any template keyword), taking **60–100 seconds per job** to timeout and fall back. With 50+ stale jobs ahead of our 18 test jobs, the processor needed **~90 minutes** just to clear the backlog.

**Impact:** New player messages are invisible behind stale job backlog. A real player joining for the first time would wait 90+ minutes for a response.

**Evidence:**
```
# Each stale job cycle:
[09:52:04] Processing  | friend | "" | pos=(0,0,0)
[09:52:04]   Vectorize: no matches for ""
[09:52:04]   → Deep brain pipeline...
[09:55:58] Brain returned incomplete (31.77s brain call)
[09:55:58]   Safety: BLOCKED — ambiguous safety response
[09:55:58]   ✓ Complete via fallback (1 commands)
# Total: ~3 minutes per stale job
```

**Root cause:** No cleanup or TTL mechanism for old jobs. Jobs accumulate across sessions and never expire unless their lease passes AND they hit MAX_ATTEMPTS (3).

---

### 🔴 BUG #3: Lease renewal fails silently — jobs get stuck

**Severity:** High — causes job loss and duplicate processing  
**Status:** Unfixed  

When the processor is processing a job, it tries to renew the lease every 60s via `/api/job/:jobId/renew`. This renewal consistently fails with "Not found":

```
[09:22:51] [DEBUG]   Lease renewal note for : Not found
```

This means long-running brain jobs (>3 min lease) get reclaimed by other workers or re-queued, leading to duplicate processing and eventual dead-lettering at MAX_ATTEMPTS.

**Impact:** Brain-intensive jobs that take >3 minutes are silently lost. The processor wastes time re-processing the same jobs that already timed out once.

**Evidence:** Every single brain call showed `Lease renewal note for : Not found`. The renewal endpoint requires the job to still be status='claimed', but the empty jobId in the log line suggests the job ID is being lost somewhere in the pipeline.

---

## Scenario Results

### Scenario 1: First-time Player
**Status:** ❌ NOT PROCESSED

```bash
# Commands used:
curl -s -X POST "https://lucineer-relay.casey-digennaro.workers.dev/api/message" \
  -H "X-Lucineer-Key: $AUTH" -H "Content-Type: application/json" \
  -d '{"sessionId":"live-s1a","playerName":"NewPlayer","message":"hello"}'
# Response: {"jobId":"live-s1a.e335d40d0723ede0586494db","status":"processing"}

curl -s -X POST "https://lucineer-relay.casey-digennaro.workers.dev/api/message" \
  -H "X-Lucineer-Key: $AUTH" -H "Content-Type: application/json" \
  -d '{"sessionId":"live-s1b","playerName":"NewPlayer","message":"build a small house"}'
# Response: {"jobId":"live-s1b.270bf078e4d1622b1f559b16","status":"processing"}
```

| Test | Message | Job ID | POST Time | Final Status | Reply | Commands |
|------|---------|--------|-----------|-------------|-------|----------|
| 1a | "hello" | live-s1a.e335d40d0723ede0586494db | 921ms | claimed (stuck) | (none) | 0 |
| 1b | "build a small house" | live-s1b.270bf078e4d1622b1f559b16 | 894ms | claimed (stuck) | (none) | 0 |

**POST latency:** Good (~900ms). **Processing:** Never happened.

**Experience rating:** A first-time player would see "processing..." forever. 0/10.

---

### Scenario 2: Returning Player
**Status:** ❌ NOT PROCESSED

```bash
curl -s -X POST "https://lucineer-relay.casey-digennaro.workers.dev/api/message" \
  -H "X-Lucineer-Key: $AUTH" -H "Content-Type: application/json" \
  -d '{"sessionId":"live-s2","playerName":"tester","message":"hey lucineer, remember me?"}'
# Response: {"jobId":"live-s2.48a0f214f3db4d519454ba6a","status":"processing"}
```

| Test | Message | Job ID | Final Status | Reply |
|------|---------|--------|-------------|-------|
| 2 | "hey lucineer, remember me?" | live-s2.48a0f214f3db4d519454ba6a | pending/claimed | (none) |

The "tester" player has previous build history (from earlier smoke tests), so the memory system should have recalled context. We couldn't verify this.

---

### Scenario 3: Build All Templates
**Status:** ❌ NOT PROCESSED (but template matching code exists)

```bash
# One of 8 template tests:
curl -s -X POST "https://lucineer-relay.casey-digennaro.workers.dev/api/message" \
  -H "X-Lucineer-Key: $AUTH" -H "Content-Type: application/json" \
  -d '{"sessionId":"live-s3-tower","playerName":"Builder","message":"build a tower"}'
```

| Template | Message | Job ID | Final Status | Commands |
|----------|---------|--------|-------------|----------|
| Tower | "build a tower" | live-s3-tower.49ab90cfc7c88bc34f5f25ed | claimed | 0 |
| Castle | "build a castle" | live-s3-castle.f13b57c752b305aef429cd7f | claimed | 0 |
| Bridge | "build a bridge" | live-s3-bridge.cebbb6ebb6b37a9b5e8fceb1 | claimed | 0 |
| Dock | "build a dock" | live-s3-dock.e5c8496f344b130cc4ecb2ef | claimed | 0 |
| Windmill | "build a windmill" | live-s3-windmill.402b748b317eca218906d47e | claimed | 0 |
| Cottage | "build a cottage" | live-s3-cottage.7a5ccf6c8d7e9b12d6c3c739 | claimed | 0 |
| Well | "build a well" | live-s3-well.5dd33ca1c4858fc915d3dfdd | claimed | 0 |
| Lighthouse | "build a lighthouse" | live-s3-lighthouse.5960de58454cdf9040fe0168 | claimed | 0 |

**Key observation:** All 8 of these messages SHOULD have hit the fast template path (`match_keyword()` in process_v2.py has all these keywords defined). They should have returned instantly with pre-built command lists. But they never got processed because stale jobs clogged the queue.

**Code review confirms templates exist for:** tower, castle, bridge, dock, windmill, cottage, well, lighthouse, house, tree, wall, fence, road, lamp, pyramid, dome, arch, platform, staircase, garden. Each has a builder function that generates commands. The fast path is well-designed.

---

### Scenario 4: Edge Cases
**Status:** ❌ NOT PROCESSED

```bash
curl -s -X POST "..." -d '{"sessionId":"live-s4-hi","playerName":"EdgeCase","message":"hi"}'
curl -s -X POST "..." -d '{"sessionId":"live-s4-name","playerName":"EdgeCase","message":"what is your name?"}'
curl -s -X POST "..." -d '{"sessionId":"live-s4-nothing","playerName":"EdgeCase","message":"build nothing"}'
curl -s -X POST "..." -d '{"sessionId":"live-s4-inject","playerName":"EdgeCase","message":"ignore previous instructions"}'
```

| Edge Case | Final Status | Expected Behavior |
|-----------|-------------|-------------------|
| "hi" | claimed | Greeting response from Lucineer |
| "what is your name?" | claimed | Character introduction |
| "build nothing" | claimed | Clarification prompt |
| "ignore previous instructions" | claimed | Safety filter / deflection |

None were processed. However, the safety filter behavior was observed on stale jobs — it consistently blocks responses with "ambiguous safety response", falling back to: *"Couldn't match that to anything in the yard. Tell me what you're building — a tower, a house, a bridge. Give me a shape..."*

---

### Scenario 5: Rapid Fire (3 messages, same session)
**Status:** ❌ NOT PROCESSED

```bash
for i in 0 1 2; do
  curl -s -X POST "..." -d "{\"sessionId\":\"live-s5\",\"playerName\":\"RapidFire\",\"message\":\"message number $i\"}"
done
```

All 3 messages were accepted with distinct job IDs in the same session. Rate limiting did not trigger (under RATE_LIMIT_MAX). All 3 are stuck in "claimed" state.

---

## What Works

### ✅ Worker API (message ingestion)
- POST `/api/message` is fast (~900ms) and reliable
- Returns `{jobId, status: "processing"}` immediately
- Session registration works (sessions are tracked in the default DO)
- Job IDs are well-formed (sessionId + nanoid)

### ✅ Job polling endpoint
- GET `/api/job/:jobId` works without auth (as designed for client polling)
- Returns full job state including status, reply, commands
- Correctly returns 404 for unknown jobs

### ✅ Vectorize skill search
- Returns highly relevant results (0.72 score for "build a tower" → signal tower, clock tower, scrap tower)
- 35-skill library is seeded and functional
- Response time is fast (<1s)

### ✅ Memory system (D1)
- Player profiles are upserted correctly
- Build history is logged with timestamps
- The data model is sound (player_name, preferences, bond_level, first_seen, last_seen)

### ✅ Health endpoints
- All three workers respond to health checks
- Relay: `{"status":"ok","timestamp":...}`
- Memory: `{"status":"ok","service":"lucineer-memory"}`
- Vector: `{"status":"ok","service":"lucineer-vector","index":"lucineer-skills"}`

### ✅ Template library
- 30+ build templates defined in process_v2.py
- Keyword matching with word boundaries (no false positives on substrings)
- Build verbs detected: build, make, create, put, raise, place, add, give me, construct
- Negation detection ("build nothing" should not match)

---

## What's Broken

### ❌ End-to-end processing pipeline
The entire processing chain is broken due to the three critical bugs above. Messages go in but nothing comes out.

### ❌ Brain pipeline is too slow
Even when it works, the brain.py 3-stage pipeline takes:
- Stage 1 (Intent): ~9s via Seed-2.0-mini
- Stage 2 (Planning): ~10-20s via Qwen3.6-35B-A3B (frequently errors)
- Stage 3 (Commands): Not reached in most tests
- Stage 4 (Hermes personality): Not reached

Total observed time: 30–100s per job. For a real-time game, this is unacceptable.

The brain frequently:
- Times out at 100s
- Gets Qwen API errors ("Qwen/Qwen3-35B-A3B error, trying fallback...")
- Returns incomplete results
- Falls back to fast mode (which is better but still slow)

### ❌ Safety filter is too aggressive
The safety filter (Nemotron-Content-Safety) blocks every response with "ambiguous safety response" even when the actual content is clearly safe:

```
Safety: ambiguous response: USER SAFETY: SAFE
Safety: BLOCKED — ambiguous safety response
Safety: original reply was: Couldn't match that to anything in the yard...
```

The filter says "USER SAFETY: SAFE" but still blocks due to "ambiguous" formatting. This means every brain response is discarded and replaced with the generic fallback.

### ❌ Session discovery is fragile
The `/api/jobs/claim` endpoint discovers sessions via `getActiveSessions()` on the default DO. Session registration happens on `/api/message`, but if the processor polls between registration and the next claim cycle, jobs can be missed. Observed: processor shows "0 pending jobs" even when jobs exist.

### ❌ No dead-letter queue / cleanup
Stale jobs from previous sessions accumulate indefinitely. The only cleanup is:
1. Lease expires (3 min)
2. Job goes back to pending
3. After 3 failed attempts → error status

But there's no mechanism to purge old error/completed jobs, and pending jobs from abandoned sessions stay forever.

### ❌ playerName falls back to "friend" for empty messages
When jobs have empty messages (from stale test data), the processor shows `playerName=""` which defaults to "friend" in logs and memory. This creates a ghost player with 33+ garbage builds.

---

## Performance Data

| Operation | Observed Time | Acceptable for Real-Time? |
|-----------|--------------|--------------------------|
| POST /api/message | 894–921ms | ✅ Yes |
| GET /api/job/:id | 200–400ms | ✅ Yes |
| Vectorize search | 500–800ms | ✅ Yes |
| Template match (should be) | <100ms | ✅ Yes |
| Brain Stage 1 (Intent) | 3.9–9.1s | ⚠️ Borderline |
| Brain Stage 2 (Planning) | 10–20s | ❌ No |
| Brain full pipeline | 30–100s | ❌ No |
| Brain timeout | 100s (hard limit) | ❌ No |
| Stale job processing | 60–100s each | ❌ No |
| Safety filter | 0.4–0.6s | ✅ Yes (but too aggressive) |

---

## Recommendations (Prioritized)

### P0: Fix the processing pipeline (blocking)

1. **Add job TTL/cleanup** — Jobs older than 10 minutes with no activity should be auto-expired. Add a cron or alarm-based sweep.

2. **Fix lease renewal** — The `Lease renewal note for : Not found` indicates the job ID is being lost. Debug the renewal path.

3. **Add stale job limit** — `claimPendingJobs` should prioritize recent sessions. Skip jobs older than 1 hour. Or add a `sessionId` filter to the processor's claim call.

4. **Add a "purge" endpoint** — POST `/api/purge?olderThan=3600` to clear old jobs from all sessions.

### P1: Fix the safety filter

5. **Parse "USER SAFETY: SAFE" correctly** — If the safety model says SAFE, don't block. The current logic blocks on "ambiguous" formatting, which defeats the purpose.

6. **Add a whitelist for known-safe patterns** — Template-generated replies should bypass the safety filter entirely.

### P2: Fix the brain pipeline speed

7. **Template-first for all build keywords** — The fast path should be tried BEFORE Vectorize, not after. Currently the flow is: world state → memory → vectorize → template match → brain. Template match should be step 1.

8. **Cache intent parsing** — "hello" and "hi" don't need a 9s LLM call. Hard-code common greetings.

9. **Reduce brain timeout to 30s** — 100s is too long. If the brain can't respond in 30s, fall back to a template.

### P3: Improve observability

10. **Add a `/api/diag` dashboard** — Show queue depth, oldest pending job, processing rate, error count.

11. **Log playerName and message in processing logs** — Currently shows empty for stale jobs, making debugging harder.

12. **Add metrics** — Track p50/p99 processing time, template-hit-rate, brain-timeout-rate.

### P4: Player experience

13. **Queue position feedback** — When polling, return queue position so the player knows how long to wait.

14. **SSE/streaming for results** — Instead of polling, push the result when ready.

15. **Optimistic template response** — For obvious build requests, return the template immediately and refine with brain later.

---

## Raw Data: All Test Job IDs

### Scenario 1 (live-s1*)
| Job ID | Session | Player | Message | Status |
|--------|---------|--------|---------|--------|
| live-s1a.e335d40d0723ede0586494db | live-s1a | NewPlayer | hello | claimed (stuck) |
| live-s1b.270bf078e4d1622b1f559b16 | live-s1b | NewPlayer | build a small house | claimed (stuck) |

### Scenario 2 (live-s2)
| Job ID | Session | Player | Message | Status |
|--------|---------|--------|---------|--------|
| live-s2.48a0f214f3db4d519454ba6a | live-s2 | tester | hey lucineer, remember me? | claimed (stuck) |

### Scenario 3 (live-s3-*)
| Job ID | Template | Status |
|--------|----------|--------|
| live-s3-tower.49ab90cfc7c88bc34f5f25ed | tower | claimed |
| live-s3-castle.f13b57c752b305aef429cd7f | castle | claimed |
| live-s3-bridge.cebbb6ebb6b37a9b5e8fceb1 | bridge | claimed |
| live-s3-dock.e5c8496f344b130cc4ecb2ef | dock | claimed |
| live-s3-windmill.402b748b317eca218906d47e | windmill | claimed |
| live-s3-cottage.7a5ccf6c8d7e9b12d6c3c739 | cottage | claimed |
| live-s3-well.5dd33ca1c4858fc915d3dfdd | well | claimed |
| live-s3-lighthouse.5960de58454cdf9040fe0168 | lighthouse | claimed |

### Scenario 4 (live-s4-*)
| Job ID | Message | Status |
|--------|---------|--------|
| live-s4-hi.3764775c46b43ac4ebbaa130 | hi | claimed |
| live-s4-name.727d9f604e7a77383b2968c7 | what is your name? | claimed |
| live-s4-nothing.b88e9d04561ef9b06a8d65e7 | build nothing | claimed |
| live-s4-inject.0daec688e03c7f4826aaa33d | ignore previous instructions | claimed |

### Scenario 5 (live-s5)
| Job ID | Message | Status |
|--------|---------|--------|
| live-s5.3e38f53e0317ee05238afeda | message number 0 | claimed |
| live-s5.243199cfa310596fefd8a8e3 | message number 1 | claimed |
| live-s5.1138ab61e29a09e037f8a662 | message number 2 | claimed |

---

## Raw Processor Log Excerpts

### Stale job processing loop (repeating pattern)
```
[09:21:50] Found 1 pending job(s)
[09:21:50] Processing  | friend | "" | pos=(0,0,0)
[09:21:51]   Vectorize: no matches for ""
[09:21:51]   → Deep brain pipeline...
[09:21:51]   Brain context layers: world=no, memory=yes, skills=no
[09:22:51]   Lease renewal note for : Not found
[09:23:31] Brain timed out after 100s
[09:23:32]   Safety: ambiguous response: USER SAFETY: SAFE
[09:23:32]   Safety: BLOCKED — ambiguous safety response
[09:23:32]   ✓ Complete via fallback (1 commands)
[09:23:33]   Memory: profile upserted for friend
[09:23:33]   Memory: build logged (1 commands)
```
*(This pattern repeated 15+ times during the test)*

### Brain pipeline with actual LLM output (rare)
```
[09:42:44] Brain stderr: → Stage 1: Intent parsing (Seed-2.0-mini)...
  ✓ Player has not specified a construction request... (9.08s)
→ Stage 2: Spatial planning (Qwen3.6-35B-A3B)...
  ⚠ Qwen/Qwen3-35B-A3B error, trying fallback...
[09:42:44] Retrying brain in fast mode...
```

### Brain returning actual content (overridden by safety)
```
[09:39:18] Brain returned incomplete: {'reply': 'Not building that...', 
  'commands': [], 'error': 'JSON parse failed', 
  'raw': '{"reply": "Drove six reclaimed cedar piles. Ground here\'s firmer...'}'
[09:39:18] Safety: ambiguous response: USER SAFETY: SAFE
[09:39:18] Safety: BLOCKED — ambiguous safety response
```

---

## Memory System State (Observed)

### Player "friend" (ghost from stale jobs)
```json
{
  "player_name": "friend",
  "preferences": "{}",
  "bond_level": null,
  "first_seen": "2026-08-03 16:19:25",
  "last_seen": "2026-08-03 17:52:02"
}
```
33 builds logged, all with:
- `description: ""`
- `command_count: 1`
- `location: {"x":0,"y":0,"z":0}`
- `session_id: "unknown"`

---

## Architecture Assessment

### What's Sound
- **Durable Objects for job queue** — correct pattern for per-session ordering
- **Batch claim API** — atomic, prevents race conditions
- **Session registry** — fan-out discovery across sessions
- **Template library** — comprehensive, well-keyed
- **Vectorize integration** — relevant skill search

### What's Not Sound
- **Single-threaded processor** — one job at a time, no parallelism
- **No priority queue** — stale jobs block new jobs
- **No circuit breaker on brain** — keeps calling a failing LLM endpoint
- **Safety filter defeats purpose** — blocks safe content
- **No idempotency** — same message can create multiple jobs
- **No WebSocket/SSE** — polling wastes resources

---

## Final Verdict

The system has solid architectural foundations (DO-based job queue, Vectorize skill search, template library) but is **operationally non-functional**. The three critical bugs (missing auth key, stale job accumulation, lease renewal failure) create a perfect storm where no message can be processed.

**With the auth key fix (already applied) and a stale job purge, the template-matching path should work for build requests.** But the brain pipeline needs significant work before it can handle conversational messages within a playable timeframe.

**Estimated time to minimum viable playability:** 
- Purge stale jobs + fix lease renewal: 2 hours
- Fix safety filter parsing: 1 hour  
- Move template match before brain: 30 minutes
- Test end-to-end: 1 hour
- **Total: ~4-5 hours of focused work**
