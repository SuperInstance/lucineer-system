# PRODUCTION READINESS CHECKLIST

**Audited:** `process_v2.py` (1811 lines) + `src/index.ts` (344 lines) + `src/do/LucineerSession.ts` (570 lines)
**Date:** 2026-08-03
**Scope:** Job claiming, memory wiring, keyword matching

---

## 1. JOB CLAIMING — `POST /api/job/:id/claim` and `POST /api/jobs/claim`

### 1a. Worker-side API (exists, correct)

| Check | Result | Detail |
|-------|--------|--------|
| `POST /api/job/:jobId/claim` exists? | **PASS** | `src/index.ts:186-199`. Single-job atomic claim. Uses `WHERE id = ? AND status = 'pending' AND claimed_at IS NULL`. |
| `POST /api/jobs/claim` exists? | **PASS** | `src/index.ts:205-237`. Batch atomic claim with `?workerId=&limit=`. |
| `claimJob()` DO method atomic? | **PASS** | `LucineerSession.ts:371-406`. Checks `Math.abs(job.claimedAt - now) < 1000` to verify we claimed it. |
| `claimPendingJobs()` DO method atomic? | **PASS** | `LucineerSession.ts:291-365`. Selects pending jobs, then atomically updates to claimed in one transaction. |
| Lease expiry handled? | **PASS** | 3-minute lease (`LEASE_MS = 3 * 60 * 1000`). Stale leases reclaimed by `cleanupStaleJobs()` called from `alarm()` and `getPendingJobs()`. |
| Max attempts enforced? | **PASS** | `MAX_ATTEMPTS = 3`. Exceeded → job permanently errored (dead-letter). |
| Auth required? | **PASS** | All `/api/job/*` internal endpoints are behind `isAuthorized()` at line 134. |

### 1b. Processor-side wiring (MISSING)

| Check | Result | Detail |
|-------|--------|--------|
| Processor calls `/api/job/:id/claim` before processing? | **FAIL** | `process_v2.py` never calls any claim endpoint. |
| Processor calls `/api/jobs/claim` (batch)? | **FAIL** | The processor only calls `GET /api/jobs/pending` (line 1398 in `run_once()`). |
| `api_post()` function exists for POST? | **PASS** | `api_post()` at line 95-111 handles any path + data. Ready to use. |
| Processor passes a `workerId`? | **FAIL** | No worker identity; claim endpoint accepts `?workerId=` but processor never calls it. |
| Processor handles `409 Conflict` on claim? | **FAIL** | N/A — never claims, so never sees the race condition. |

### 1c. Cross-DO polling architecture issue

| Check | Result | Detail |
|-------|--------|--------|
| Jobs visible from `GET /api/jobs/pending`? | **FAIL** | `src/index.ts:279` queries only `sessionStub(env, "default")`. Jobs are created on _session-specific_ DOs (line 95: `sessionStub(env, body.sessionId)`). Jobs in non-default session DOs are invisible. |
| `POST /api/jobs/claim` with no `?sessionId=`? | **FAIL** | Falls back to `["default"]` only (line 220). Same visibility gap as above. |
| Can processor enumerate sessions? | **FAIL** | No mechanism to discover active session DOs. Durable Objects don't support listing. |
| Recommended fix? | — | Move ALL jobs into a single "default" DO (remove session-scoped DOs) OR add a separate "job-queue" DO that all sessions write to. The Worker alreadly encodes the session ID in the job ID (`sessionId.randomHex`) so routing `getJob()` and `setJobResult()` still works — those look up by job ID which contains the session prefix. Only the polling/claiming needs the global view. |

**Job Claiming Verdict: FAIL (3 blocking issues)**

---

## 2. MEMORY WIRING — `get_player_context`, `recall_skills`, `record_build`

### 2a. `get_player_context` (D1 profile + builds + conversations + cache)

| Check | Result | Detail |
|-------|--------|--------|
| Fetches player profile from D1? | **PASS** | `get_player_profile()` at line 184, called from `get_player_context()` at line 493. |
| Fetches recent builds from D1? | **PASS** | `get_recent_builds()` at line 209, called at line 494. Default limit=5. |
| Fetches recent conversations from D1? | **PASS** | `get_recent_conversations()` at line 230, called at line 497. Uses `CONVERSATION_RECALL_LIMIT=5`. |
| Includes session cache context? | **PASS** | `_session_cache.get_player_context()` at line 521. Tracks last 10 turns in-memory. |
| Includes conversation references? | **PASS** | `build_conversation_references()` at line 526. Extracts preferences, desires, etc. |
| Builds context string? | **PASS** | Line 533: concatenates profile → builds → cache → refs → conversations into single string. |
| Called from `process_job()`? | **PASS** | Line 1591 (real session), line 1598 (mock fallback). Passes `current_message=message`. |
| Context injected into brain call? | **PASS** | `memory_ctx` passed to `call_brain()` at line 1624. |
| Bond level extracted from profile? | **PASS** | Line 503: `int(profile.get("bond_level", 0))`. |
| Preferences parsed from profile? | **PASS** | Line 508-514: JSON-decoded preferences included if present. |

### 2b. `recall_skills` / `search_skills` (Vectorize semantic search)

| Check | Result | Detail |
|-------|--------|--------|
| Sends query to Vectorize Worker? | **PASS** | `vector_post("/api/skills/query")` at line 549. |
| Filters by score threshold? | **PASS** | `SKILL_SCORE_THRESHOLD = 0.6` at line 568. |
| Returns structured matches? | **PASS** | Returns list of `{name, description, score, metadata}`. |
| Formats as brain context? | **PASS** | `format_skill_context()` at line 581 converts matches to prompt string. |
| Called from `process_job()`? | **PASS** | Line 1602: `search_skills(message, top_k=3)`. |
| Result passed to `call_brain()`? | **PASS** | `skill_ctx` passed at line 1625. |
| Logs results? | **PASS** | Lines 557, 569, 577: log on no match, above threshold, below threshold. |

### 2c. `record_build` / `save_to_memory` (persistence)

| Check | Result | Detail |
|-------|--------|--------|
| Upserts player profile before build? | **PASS** | Line 1674: `upsert_player_profile()` called FIRST (FK constraint). |
| Logs build to D1? | **PASS** | `log_build()` at line 1677. Includes description, command count, position. |
| Logs assistant reply to D1? | **PASS** | Line 1691: `log_conversation()` for assistant role. |
| Logs player message to D1? | **PASS** | Line 1581: `log_conversation()` for player role — called at start of `process_job()`. |
| Feeds session cache? | **PASS** | Line 1693: `_session_cache.add(player_name, message, reply)`. |
| Called after every job? | **PASS** | Line 1652-1661: `save_to_memory()` called unconditionally in `process_job()`. |
| Handles mock sessions? | **PASS** | `save_to_memory()` runs for mock (line 1694 forces session_id check for conversations only; cache is always fed). Profile/build logged regardless. |
| Vibe-code jobs feed cache? | **PASS** | Line 1531: `_session_cache.add()` called directly in `_process_vibe_code_job()`. |
| Error handling? | **PASS** | Each memory function logs warnings on failure (e.g. `log("Memory: build log note: ...", "WARN")`) but doesn't crash the pipeline. |

### 2d. Memory API connectivity

| Check | Result | Detail |
|-------|--------|--------|
| Memory Worker URL configured? | **PASS** | `MEMORY_URL` env var or hardcoded default (line 39). |
| Auth key sent? | **PASS** | `X-Lucineer-Key` header in `memory_get()` and `memory_post()`. |
| Vectorize Worker URL configured? | **PASS** | `VECTOR_URL` env var or default (line 41). |
| Fallback on D1 failure? | **PASS** | Memory functions return `{}` or `[]` on error (non-blocking). |

**Memory Wiring Verdict: PASS (no issues found)**

---

## 3. KEYWORD MATCHING — Word Boundaries

### 3a. Keyword match function

| Check | Result | Detail |
|-------|--------|--------|
| Uses regex word boundaries? | **PASS** | Line 1030: `_re.search(rf'\b{_re.escape(keyword)}\b', msg_lower)`. |
| Keywords escaped before regex? | **PASS** | `_re.escape(keyword)` prevents injection. |
| Longest match wins? | **PASS** | Lines 1025-1033: `best_len` tracked, longer keyword replaces shorter. "lighthouse" (11) beats "light" would beat "tower" (5) etc. |
| Build-verb guard? | **PASS** | Line 1018: `_BUILD_VERBS.search(msg_lower)` must match. Prevents keyword matching on conversational uses ("I like castles"). |
| Negation guard? | **PASS** | Line 1022: `_NEGATIONS.search(msg_lower)` returns `None`. "Don't build a tower" → no match. |
| Case-insensitive? | **PASS** | `msg_lower = message.lower()` at line 1015. `_re.IGNORECASE` flag on verb/negation regex. |

### 3b. Template function integrity

| Check | Result | Detail |
|-------|--------|--------|
| All KEYWORDS map to valid builder functions? | **PASS** | 18 canonical template functions from `b_tower` through `b_dock`. All defined. |
| Templates return (reply, commands) tuple? | **PASS** | Every builder function returns `(str, list[dict])`. |
| New templates wired? | **PASS** | `b_lookout` (line 634), `b_windmill` (line 847), `b_fence` (line 764) properly added to KEYWORDS and defined. |
| Default fallback exists? | **PASS** | `b_default()` at line 970. Used when template and brain both fail (line 1634). |

### 3c. Build verbs regex

| Check | Result | Detail |
|-------|--------|--------|
| Uses `\b` boundaries? | **PASS** | Line 1002: `\b(build|make|...)\b`. |
| Covers common verbs? | **PASS** | build, make, create, put, raise, place, add, construct, throw up, put up. |
| `add` as a build verb? | **NOTE** | "add" is very generic ("add a lamp" works, but "add it to the list" would false-positive). Mitigated by requiring a keyword match too. Low risk. |
| Multi-word phrases functional? | **NOTE** | `give me`, `raise me`, `throw up`, `put up` are in the alternation but the single-word variants (`give`, `raise`, `throw`, `put`) match first due to regex alternation left-to-right greediness. Harmless — the single-word variants are sufficient to detect build intent. |

**Keyword Matching Verdict: PASS (1 minor note about `add` verb)**

---

## 4. ADDITIONAL ISSUES FOUND DURING AUDIT

### 4a. `commandType` field propagation

| Check | Result | Detail |
|-------|--------|--------|
| `IncomingMessage` has `commandType`? | **FAIL** | `src/types.ts:19-25`: `IncomingMessage` only has `sessionId`, `playerName`, `message`, `playerState`, `worldSnapshot`. No `commandType`. |
| Worker stores `commandType` in SQLite? | **FAIL** | `createJob()` only inserts standard columns. No `commandType` column exists. |
| Processor checks `commandType`? | **PASS** (code) | Line 1575: `command_type = job.get('commandType', '')`. |
| Vibe-code routing works? | **FAIL** | `commandType` will always be `''` because it's never set. `_process_vibe_code_job()` is unreachable via the relay. |

### 4b. `GET /api/jobs/pending` only queries default DO

| Check | Result | Detail |
|-------|--------|--------|
| `createJob` writes to session DO? | **PASS** | `src/index.ts:95`: `sessionStub(env, body.sessionId).createJob(body)`. Correct. |
| `getPendingJobs` reads from default DO? | **PASS** (code) | `src/index.ts:279`: `sessionStub(env, "default").getPendingJobs()`. |
| Do these DOs share SQLite? | **FAIL** | No. Each Durable Object has its own isolated SQLite database. Jobs created in a session DO (`abc123`) are invisible from the "default" DO. |
| **Impact:** | **CRITICAL** | All jobs land in session DOs and never appear in `GET /api/jobs/pending`. The processor will ALWAYS receive an empty jobs array. The system is non-functional for non-default sessions. |

### 4c. `playerState` extraction

| Check | Result | Detail |
|-------|--------|--------|
| Processor reads `playerState` from job? | **PASS** (code) | Line 1557: `ps = job.get('playerState') or {}`. |
| Worker stores `playerState` in jobs table? | **FAIL** | `createJob()` only stores `id, session_id, player_name, message, status, created_at, attempts`. `playerState` is not persisted. |
| **Impact:** | **MEDIUM** | Player position might be `(0,0,0)` for all jobs, causing structures to overlap. The Worker needs to store `playerState` (or at least position) in the jobs table. |

### 4d. `worldSnapshot` storage

| Check | Result | Detail |
|-------|--------|--------|
| `worldSnapshot` included in `IncomingMessage`? | **PASS** (types) | `src/types.ts:24`: `worldSnapshot?: WorldSnapshot`. |
| Worker stores snapshot? | **PASS** | Line 217-224: inserted/updated in `world_state` table when provided with `createJob()`. |
| Processor reads world state? | **PASS** (code) | `get_world_context()` at line 593 calls `GET /api/state/{sessionId}`. |
| World state endpoint works? | **PASS** | `src/index.ts:264-273` reads from session-specific DO (`getWorldState`). |

---

## 5. SUMMARY

| Category | Verdict | Critical Items |
|----------|---------|----------------|
| **Job Claiming** | **FAIL** | 1. Processor never calls claim endpoint. 2. Cross-DO polling gap (jobs invisible to processor). 3. `playerState` not stored. |
| **Memory Wiring** | **PASS** | All three functions (`get_player_context`, `recall_skills`, `record_build`) properly implemented and wired into `process_job()`. |
| **Keyword Matching** | **PASS** | Word boundaries correct. Longest-match scoring. Negation filter. Build-verb guard. |
| **Additional Issues** | — | `commandType` unreachable. `playerState` not persisted. `GET /api/jobs/pending` broken for session DOs. |

### Required Fixes

**Immediate (blocking production):**
1. Fix `process_v2.py` `run_once()` to call `POST /api/jobs/claim?workerId=processor-1&limit=5` instead of `GET /api/jobs/pending`.
2. Fix the cross-DO job visibility: either route all jobs to "default" DO, or add a job-queue DO.
3. Store `playerState` (position, at minimum) in the jobs SQLite table.

**Important (before players):**
4. Add `commandType` to `IncomingMessage` type and persist it in the jobs table.
5. Verify `playerState` is being sent from the Roblox client (may be a client-side issue too).
