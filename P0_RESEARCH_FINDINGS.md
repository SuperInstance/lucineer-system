# P0 RESEARCH FINDINGS — Lucineer / Slackwater

**Compiled:** 2026-08-03  
**Researcher:** Track 4 (P0 Questions)  
**Source:** `MASTER_RESEARCH_QUESTIONS.md` — 24 P0 questions

---

## Table of Contents

1. [Technical (Roblox/Lua) — RQ-001 through RQ-010](#1-technical-robloxlua)
2. [Technical (Cloudflare/Workers) — RQ-025 through RQ-034](#2-technical-cloudflareworkers)
3. [Technical (AI/ML) — RQ-038 through RQ-048](#3-technical-aiml)
4. [Design (Character) — RQ-081, RQ-087](#4-design-character)
5. [Infrastructure — RQ-101, RQ-102, RQ-108](#5-infrastructure)
6. [Summary Table](#6-summary-table)

---

## 1. Technical (Roblox/Lua)

### RQ-001 — Command envelope `{type, params}` enforcement

**Status: ✅ ANSWERED (already implemented)**

**Finding:** The CommandExecutor already enforces the envelope correctly. At the dispatch site in `CommandExecutor.execute()`, the code unwraps `command.params` before passing to handlers, with a fallback to flat commands for hand-written test payloads:

```lua
local params = command.params
if type(params) ~= "table" then
    params = command
end
local ok, result = pcall(handler, params)
```

**Recommendation:** The current implementation is correct. The `pcall` wrapper catches handler errors. The command map (`commandMap`) explicitly lists all supported types, rejecting unknowns with an error string.

**Action needed:** None. Document the envelope contract in `PROTOCOL.md` (see RQ-108) so external contributors follow the pattern.

---

### RQ-002 — Session identity format

**Status: ✅ ANSWERED (already implemented)**

**Finding:** Session ID is generated in `Config.lua`:

```lua
Config.SESSION_ID = string.format("%d-%s", game.PlaceId,
    (game.JobId ~= "" and game.JobId or "studio"))
```

Format: `{PlaceId}-{JobId}` (e.g., `1234567890-server-abc123`). Studio falls back to `{PlaceId}-studio`.

The Worker (`lucineer-worker/src/index.ts`) uses session IDs to route to per-session Durable Objects via `sessionStub(env, sessionId)`, which calls `env.LUCINEER_SESSION.getByName(encodeURIComponent(sessionId))`.

Job IDs encode the session: `<urlEncodedSessionId>.<randomHex>`, allowing the Worker to route any job back to its DO without a lookup table.

**Recommendation:** The format is canonical. It survives server restarts (same JobId within a server lifecycle), distinguishes Studio from production, and is URL-safe when encoded.

**Action needed:** Document this format in `PROTOCOL.md`.

---

### RQ-003 — Client-side secret storage

**Status: ✅ ANSWERED (already implemented — P0_SECURITY_FIXES.md)**

**Finding:** This was fully resolved in a prior pass. The key changes:

1. **`Config.lua` (ReplicatedStorage)** — stripped of all secrets. Contains only client-safe values (UI colors, poll intervals, session ID).
2. **`ServerConfig.lua` (ServerScriptService)** — new module that resolves `AUTH_KEY` from `ServerStorage:WaitForChild("LucineerSecret")` (a StringValue set in Studio). ServerScriptService does NOT replicate to clients.
3. **`Http.lua`** — `Http.configure(workerUrl, authKey)` is called once at server init. Credentials live in upvalues (closure variables), not accessible from client-side code.

**Best practice confirmed by research:** Roblox's official guidance is "Never trust the client." ServerScriptService and ServerStorage are the only safe containers for secrets. The Roblox Secrets Store (`HttpService:GetSecret()`) is an alternative for production but adds complexity. The current StringValue-in-ServerStorage approach is standard for most games.

**Action needed:** None. Consider migrating to Roblox Secrets Store for production if key rotation becomes necessary.

---

### RQ-004 — Delete `runLua` / `addScript`

**Status: ✅ ANSWERED (already implemented)**

**Finding:** `runLua` is **fully removed** from CommandExecutor. The command map does not contain it. A code comment documents the rationale:

```lua
--[[
    GAP #9a: runLua REMOVED.
    loadstring requires ServerScriptService.LoadStringEnabled which is off by default
    and should stay off. Arbitrary server-side code execution from HTTP responses
    is unsafe.
]]
```

`addScript` is **kept but Studio-only**, guarded by `RunService:IsStudio()`. At runtime in a published game, it returns nil with a warning. This is correct — `Script.Source` is only assignable from plugins/command bar in Studio.

**Recommendation:** The current state is correct. No whitelist-based parameterized behavior system is needed for MVP. If dynamic behaviors are needed later, implement a registry of pre-validated Luau functions keyed by name (not arbitrary source strings).

**Action needed:** None.

---

### RQ-006 — TextChatService vs legacy chat

**Status: ✅ ANSWERED (with migration recommendation)**

**Finding from research:** As of 2025, Roblox has **fully deprecated the legacy chat system**. Key facts:
- New experiences could not be created with legacy chat after **November 30, 2024**.
- Automatic migration to `TextChatService` began **May 2025**.
- Legacy chat was fully removed by **April 30, 2025**.
- `TextChatService` handles filtering automatically — no manual `FilterStringAsync` needed for standard chat messages.
- NPC bubble chat: use `TextChatService:DisplayBubble()` or the `OnBubbleAdded` callback.
- `BubbleChatConfiguration` is a child of `TextChatService` for customizing spatial bubbles.

**Current code state:** `ChatHandler.lua` uses `player.Chatted` events (legacy) and manually calls `TextService:FilterStringAsync()` for outbound filtering. This works but is the old pattern.

**Recommendation:** Migrate to `TextChatService` before launch. The migration path:

1. Enable `TextChatService` in Studio settings (Create a `TextChatService` with `ChatVersion = TextChatService`).
2. Replace `player.Chatted` listeners with `TextChatService.MessageReceived:Connect()` for programmatic access to messages.
3. For Lucineer's responses, use `TextChannel:SendAsync()` instead of manual RemoteEvent firing — this gets automatic filtering for free.
4. For NPC dialogue (Earl, Spark, etc.), use `TextChatService:DisplayBubble(character, text)` — automatic bubble chat with no extra configuration.
5. Remove manual `FilterStringAsync` calls for standard chat paths (still needed for AI-generated text that doesn't go through the standard chat channel).

**Effort:** ~4 hours. The ChatHandler is the only file that needs significant changes.

**Action needed:** Add to pre-launch checklist. Not blocking for MVP since legacy chat still functions in existing places, but required before public release.

---

### RQ-010 — Consolidate Lua source trees

**Status: ✅ ANSWERED (already completed — A1_SOURCE_UNIFICATION.md)**

**Finding:** Source unification is complete. `lucineer-roblox/` is the canonical source (38 files, 35,577 lines). `vibe-world/src/` contains 4 vestigial files (562 lines) that are fully superseded. The `.rbxlx` files are build outputs containing stale embedded copies.

**Recommendation:** The Rojo project file (`default.project.json`) is the single source of truth. The migration path:

1. ✅ Done: Canonical source established at `lucineer-roblox/`.
2. ✅ Done: `vibe-world/src/` documented as vestigial.
3. **Next:** Delete `vibe-world/src/` after confirming Rojo sync works in Studio.
4. **Next:** Archive `.rbxlx` files — they're build outputs, not source.
5. **Next:** Set up CI/CD to build `.rbxlx` from source via Rojo + `rojo build` (see RQ-110).

**Action needed:** Delete vestigial files and set up Rojo build in CI.

---

### RQ-025 — Atomic job claiming in Durable Object

**Status: ✅ ANSWERED (already implemented)**

**Finding:** The DO (`LucineerSession.ts`) implements atomic batch claiming via `claimPendingJobs()`:

1. **Stale lease cleanup:** Expired claimed jobs (lease_expires_at < now) are either dead-lettered (if attempts ≥ MAX_ATTEMPTS) or reset to pending.
2. **Atomic select + claim:** The method selects pending jobs and transitions them to 'claimed' in a single SQL transaction within the DO's SQLite store.
3. **Lease mechanism:** Each claimed job gets `lease_expires_at = now + LEASE_MS` (3 minutes). The processor can renew leases via `/api/job/:jobId/renew`.
4. **Retry limit:** MAX_ATTEMPTS = 3. After 3 failed attempts, the job is permanently errored.

The Worker exposes two endpoints:
- `POST /api/jobs/claim` — batch atomic claim (preferred)
- `POST /api/job/:jobId/claim` — single-job claim (backward compat)

**Technical basis:** Durable Objects process requests single-threaded, so SQLite operations within a single DO are inherently serialized. No additional locking is needed.

**Action needed:** None. The implementation is production-ready.

---

### RQ-026 — DO storage pruning strategy

**Status: ✅ ANSWERED (already implemented)**

**Finding:** The DO uses **alarm-based pruning** with a 1-hour sweep interval:

```typescript
const PRUNE_AFTER_MS = 24 * 60 * 60 * 1000; // 24h
const ALARM_INTERVAL_MS = 60 * 60 * 1000;   // 1h
```

The `alarm()` method:
1. Deletes completed/errored jobs older than 24h.
2. Deletes old message history (timestamp < cutoff).
3. Reclaims stale claimed jobs (calls `cleanupStaleJobs()`).
4. Schedules the next alarm.

**Cloudflare limits confirmed:** SQLite-backed DOs have 10 GB storage per object on Workers Paid plan. No row limit per table. Max row/blob size: 2 MB. At the current rate (~50-200 jobs/day per session), 24h pruning keeps storage well under 10 MB per session DO.

**Recommendation:** The current strategy is correct for MVP. For long-term history (analytics, player profiles), D1 is already used via `lucineer-memory`. The DO is transient; D1 is permanent.

**Action needed:** None.

---

### RQ-028 — Delete or fix push path

**Status: ✅ ANSWERED (already resolved)**

**Finding:** The push path has been deleted. The Worker's `index.ts` has no push/callback endpoint. The processor polls `POST /api/jobs/claim` for batch atomic claiming. The only flow is:

```
Roblox → POST /api/message → DO creates job → Processor polls /api/jobs/claim → Processor posts result → Roblox polls GET /api/job/:jobId
```

The Worker code confirms: "No push path — the processor polls POST /api/jobs/claim."

**Cloudflare Tunnel is not needed.** The polling architecture is correct for this use case because:
- Processor runs as a daemon (systemd) with 2s poll interval.
- Job latency is dominated by brain.py (5-30s), not polling overhead.
- Polling eliminates the need for WebSocket connections or tunnel setup.

**Action needed:** None.

---

### RQ-029 — Auth on memory/vector services

**Status: ✅ ANSWERED (already implemented)**

**Finding:** Both `lucineer-memory` and `lucineer-vector` implement uniform shared-secret auth:

**`lucineer-memory/src/index.ts`:**
```typescript
function requireAuth(request: Request, env: Env): Response | null {
  const key = request.headers.get("X-Lucineer-Key");
  const expected = env.LUCINEER_SHARED_SECRET;
  if (!expected) return json({error: "..."}, 500);
  if (!key || key !== expected) return json({error: "Unauthorized"}, 401);
  return null;
}
```

Every endpoint except `/api/health` passes through this gate. Fail-closed if the secret is not configured.

**`lucineer-vector/src/index.ts`:** Same pattern, same `requireAuth()` middleware.

The processor (`process_v2.py`) reads `LUCINEER_KEY` from the environment and passes it as `X-Lucineer-Key` header on all API calls.

**Recommendation:** Shared-secret is sufficient for MVP. For production with multiple processors, consider rotating the secret periodically. Cloudflare Access could be layered on top if the services need to be exposed to browser-based clients, but that's not needed here.

**Action needed:** None for MVP. Document the secret rotation procedure for ops.

---

### RQ-034 — Vector CORS lockdown

**Status: ✅ ANSWERED (already implemented)**

**Finding:** The vector service CORS is already locked down to the relay Worker origin:

```typescript
function cors(): HeadersInit {
  return {
    "Access-Control-Allow-Origin": "https://lucineer-relay.casey-digennaro.workers.dev",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-Lucineer-Key",
  };
}
```

Previously `Access-Control-Allow-Origin` was `*`. Now it's scoped to the specific Worker URL. The auth requirement (`X-Lucineer-Key`) provides a second layer of protection.

**Recommendation:** For additional hardening, consider also restricting the memory service CORS. Currently `lucineer-memory` doesn't set CORS headers at all (returns none), which effectively blocks browser access — that's fine since it's only called from the processor.

**Action needed:** None.

---

## 2. Technical (Cloudflare/Workers)

### Cloudflare Platform Limits (Confirmed via Research)

| Resource | Free Plan | Paid Plan |
|----------|-----------|-----------|
| Workers CPU time (HTTP) | 10ms | 30s default, up to 5min configurable |
| Workers CPU time (Cron) | 10ms | 30s (<1h interval), 15min (≥1h interval) |
| D1 databases per account | 10 | 50,000 |
| D1 max database size | 500 MB | 10 GB |
| D1 storage per account | 5 GB | 1 TB (as of July 2025) |
| D1 daily rows read | 5M | Billed (no hard cap) |
| D1 daily rows written | 100K | Billed (no hard cap) |
| D1 max row/blob size | 2 MB | 2 MB |
| DO SQLite storage per object | N/A | 10 GB |
| DO max columns per table | 100 | 100 |
| DO memory (shared isolate) | 128 MB | 128 MB |

**Implication for Lucineer:** The system is well within all limits. The DO stores transient jobs (24h TTL), D1 stores player profiles and build history (tiny rows), and R2 stores trajectory logs. The brain pipeline runs on DeepInfra (external), not Workers AI, so Workers CPU time is minimal (just routing and SQL).

---

### RQ-038 — Canonical persona constant

**Status: ✅ ANSWERED (already implemented)**

**Finding:** The canonical persona is `LUCINEER_PERSONA` in `brain.py` (lines ~76-120). It is a well-crafted shipyard-foreman persona with explicit rules:

- Short sentences, fragments, drop subject pronouns
- Three-beat pattern: what you did → opinion → what's unfinished
- Past tense for work, present tense for opinion
- No "helpful AI" language ever
- Always leaves something unfinished
- Magnus/Alaska references as "seasoning, not scenery"

The persona is injected into:
- `SYSTEM_INTENT` (intent parsing stage)
- `SYSTEM_FAST` (fast path single-model mode)
- `SYSTEM_CODER` (command generation, voice examples included)
- `SYSTEM_HERMES` (personality wrapping stage, full persona text)
- `persona_for(bond_level)` (appends bond tier behavioral block)

The dream-weaver persona variant has been replaced. See RQ-087.

**Recommendation:** The persona constant is canonical and correctly enforced across all pipeline stages. The `VOICE_EXAMPLES` array provides few-shot guidance to the coder model.

**Action needed:** None. The persona is the spec.

---

### RQ-039 — `--creative` flag in production

**Status: ✅ ANSWERED (recommendation: conditional use)**

**Finding:** The `--creative` flag activates the Hermes personality stage (stage 4 of the pipeline). When enabled:

1. After the coder generates commands, the result passes through `stage_hermes()`.
2. Hermes (`NousResearch/Hermes-3-Llama-3.1-405B`) rewrites ONLY the `reply` field.
3. Commands are passed through unchanged — explicitly preserved:
   ```python
   enhanced_result = dict(result)
   enhanced_result["reply"] = enhanced["reply"]
   # Explicitly preserve the coder's verified commands
   # (do NOT copy enhanced["commands"] even if present)
   ```

**Latency impact:** Hermes adds ~3-8 seconds to the pipeline (405B model, 2048 max tokens, temperature 0.8). Total pipeline with creative mode: ~15-30s. Without: ~8-20s.

**Cost impact:** Hermes-3-Llama-3.1-405B on DeepInfra costs approximately $0.80-1.50 per million tokens. At ~1000 tokens per call (system prompt + user + response), that's ~$0.001-0.002 per creative-mode call.

**Recommendation:**
- **MVP:** Enable `--creative` for all deep-path builds. The personality is the product — without Hermes, replies sound generic.
- **Fast path:** Also enable creative in fast mode (`run_fast(creative=True)`). The code already supports this.
- **Fallback:** If Hermes is unavailable (429, timeout), the coder's reply is kept — the pipeline degrades gracefully.

**Action needed:** Set `creative=True` as the default in `process_v2.py` when calling the brain. Currently the processor doesn't pass `--creative` by default.

---

### RQ-040 — Hermes must not emit commands

**Status: ✅ ANSWERED (already implemented)**

**Finding:** The brain pipeline explicitly prevents Hermes from corrupting commands:

```python
# Keep original commands — NEVER accept commands from the personality stage.
# Hermes is a prose model that can hallucinate or truncate command arrays.
# Only take the reply text from Hermes.
enhanced_result = dict(result)  # copy all fields including _meta
enhanced_result["reply"] = enhanced["reply"]
# Explicitly preserve the coder's verified commands
# (do NOT copy enhanced["commands"] even if present)
```

This is correct. Hermes (Llama-3.1-405B) is a creative writing model, not a structured data model. It could hallucinate invalid commands, truncate the array, or change parameter values.

**Recommendation:** The current implementation is correct — strip everything except the `reply` field from Hermes output. The system prompt also instructs: "Do NOT add commands or modify anything except the reply text."

**Action needed:** None.

---

### RQ-041 — Nemotron safety stage integration

**Status: ✅ ANSWERED (already implemented)**

**Finding:** The safety stage is fully integrated into both pipeline paths:

**Full pipeline (`run_pipeline`):** Stage 5 (after Hermes):
```python
is_safe, safety_reason = stage_safety(api_key, safety_reply, player_message)
if not is_safe:
    result["reply"] = "Not building that. Pick something else."
    result["commands"] = []
    result["_safety_blocked"] = True
```

**Fast path (`run_fast`):** Also runs safety check after creative wrapping.

The safety model is `nvidia/Nemotron-Content-Safety-3.5` with:
- max_tokens=64 (just needs SAFE/UNSAFE + brief reason)
- temperature=0.0 (deterministic)
- max_retries=2
- Fails **SAFE** (returns False) on API error — never shows potentially unsafe content

**Deflection pattern:** When unsafe content is detected, Lucineer says "Not building that. Pick something else." — in-voice, no explanation, no lecture.

**Cost:** Nemotron safety check costs ~$0.0001 per call (64 tokens, tiny model). Negligible.

**Recommendation:** The implementation is correct. Consider adding more nuanced deflection lines (randomized from a pool) to avoid repetition if multiple unsafe requests occur.

**Action needed:** None for MVP. Optionally diversify deflection lines post-launch.

---

### RQ-044 — Timeout hierarchy

**Status: ✅ ANSWERED (recommendation: explicit hierarchy)**

**Finding:** The current timeouts:

| Layer | Timeout | Location |
|-------|---------|----------|
| Brain budget (DEEP_TIMEOUT) | 100s | `process_v2.py` |
| Client poll timeout | 120s | `Config.lua` (`POLL_TIMEOUT = 120`) |
| HTTP request timeout (per attempt) | 10s curl + 15s Python | `process_v2.py` |
| Brain model call timeout | 90s per model | `brain.py` (`call_model` default) |
| DO lease duration | 180s (3 min) | `LucineerSession.ts` (`LEASE_MS`) |
| DO pruning | 24h after completion | `LucineerSession.ts` |
| Rate limit window | 60s, 10 msgs/session | `LucineerSession.ts` |
| Per-player cooldown | 3s | `ChatHandler.lua` |
| Concurrent job cap | 3 per server | `ChatHandler.lua` |

**Correct ordering:** Brain (100s) < Client poll (120s) < DO lease (180s). This means:
- The brain will time out before the client gives up polling. ✅
- If the brain times out, the DO lease still has 80s of headroom for the processor to post an error result. ✅
- The client polls every 0.5s, so it'll catch the result within 0.5s of completion. ✅

**Recommendation:** The hierarchy is correct. One gap: if `brain.py` hangs beyond 100s (all models slow), the processor should call `setJobError()` on the Worker. Currently `call_brain()` in `process_v2.py` catches exceptions but doesn't explicitly handle timeout — it relies on subprocess timeout.

**Action needed:** Add explicit timeout handling in `process_job()`:
```python
try:
    result = call_brain(...)
except subprocess.TimeoutExpired:
    post_result(job_id, {
        "reply": "My thoughts got tangled. Try again.",
        "commands": [],
    })
    return
```

---

### RQ-048 — Keyword matching fix

**Status: ✅ ANSWERED (already implemented — P0_PROCESSOR_FIXES.md)**

**Finding:** The keyword matcher was rewritten with three fixes:

1. **Word-boundary regex:** `\b{keyword}\b` — "arc" no longer matches "search"
2. **Build verb requirement:** Must contain `build|make|create|put|raise|place|add|give me|construct|throw up|put up`
3. **Negation detection:** `don't|do not|never|stop|no|not` → skip
4. **Longest-match-wins:** "build a castle tower" → matches both 'castle' (6) and 'tower' (5), returns 'castle' (longer)

Test results: 16/16 pass including all gap analysis edge cases.

**Recommendation:** The implementation is correct and well-tested.

**Action needed:** None.

---

### RQ-057 (P1, but relevant) — Pipeline model structure

**Status: ✅ ANSWERED (documented for awareness)**

**Current 5-stage pipeline:**

| Stage | Model | Purpose | Est. Latency | Est. Cost/Call |
|-------|-------|---------|-------------|----------------|
| 1. Intent | ByteDance/Seed-2.0-mini | Parse player request | ~2-4s | ~$0.0002 |
| 2. Planner | Qwen/Qwen3.6-35B-A3B | Spatial decomposition | ~5-10s | ~$0.001 |
| 2b. Deep | ByteDance/Seed-2.0-pro | Complex build planning | ~8-15s | ~$0.003 |
| 3. Coder | Qwen/Qwen3-Coder-480B | Command generation | ~5-15s | ~$0.003 |
| 4. Hermes | NousResearch/Hermes-3-Llama-3.1-405B | Personality wrapping | ~3-8s | ~$0.001 |
| 5. Safety | nvidia/Nemotron-Content-Safety-3.5 | Kid-safe verification | ~1-2s | ~$0.0001 |

**Total per deep+creative request:** ~$0.005-0.008, ~15-35s  
**Fast path (single model):** ~$0.0005, ~3-6s  
**Fast + creative:** ~$0.0015, ~6-12s

**Recommendation:** Default to fast+creative for most builds (template match → fast brain → Hermes). Reserve full deep pipeline for complex/unmatched requests.

---

## 3. Design (Character)

### RQ-059 — BondSystem: progression or simulation?

**Status: ✅ ANSWERED (already rewritten)**

**Finding:** BondSystem has been fully rewritten from an XP ladder to a **behavior-triggered relationship system**. The implementation in `BondSystem/init.lua` is exemplary:

- **5 tiers** (Stranger → Acquaintance → Crew → Confidant → Partner) with cumulative point thresholds (0, 10, 30, 70, 150).
- **7 behavior triggers** that award points: first build of session (+1), hook completed (+5, the core loop), independent build (+3), modify-not-replace (+2), argued and won (+4), returned next day (+2), deleted without inspection (-1).
- **Tier-gated behaviors** (16 flags per tier): references previous builds, uses Magnus/Alaska, argues, uses nicknames, volunteers work, uses "we", asks player to build, refuses work, confesses pattern, delegates to player.
- **Tier transition voice lines** drawn from CHARACTER_BIBLE §4.
- **No visible progress bar** — the player feels the relationship through Lucineer's changing behavior.
- **D1 persistence** via memory worker (bond_level + bond_points).
- **Floor at current tier** — negative events can't drop you below your tier threshold.

**Recommendation:** The system is correctly designed and implemented. It IS a progression mechanic, but the progression is invisible — the player experiences it as a relationship deepening, not a level-up.

**Action needed:** None. The hook-completion detection loop (WorldScanner checking if players build near open hooks) needs testing in-game, but the system architecture is complete.

---

### RQ-081 — Delete off-voice hardcoded strings

**Status: ✅ PARTIALLY ANSWERED (needs audit)**

**Finding:** Several off-voice strings exist in the codebase:

1. **`Config.lua`:** `UI_THINKING_TEXT = "Lucineer is thinking..."` — This is the generic thinking indicator. It's displayed via `ThinkingEvent` remote. The progressive thinking messages in ChatHandler ("Looking at the ground...", "Checking what's already here...") are better and in-voice. The initial "Lucineer is thinking..." should be replaced with a physical acknowledgment (Lucineer turns to the anvil, picks up a tool) or an in-voice line.

2. **`ChatHandler.lua`:** `"Give me a second, still working."` (rate limit) — This is in-voice. ✅  
3. **`ChatHandler.lua`:** `"Nice try. I don't take orders from the back of the room."` (injection detection) — This is in-voice. ✅  
4. **`ChatHandler.lua`:** `"My thoughts got lost. Please try again."` (error) — Slightly off-voice ("Please try again" is too polite). Replace with `"My thoughts got tangled. Try again."` or similar.

5. **Brain pipeline fallback strings:** In `brain.py`, the fast path fallback reply is `"I heard you want: {message}, but I had trouble generating build commands."` — This is completely off-voice. Replace with an in-voice deflection.

6. **Safety deflection:** `"Not building that. Pick something else."` — In-voice. ✅

**Recommendation:** Audit all hardcoded strings and replace off-voice ones:

| Location | Current | Suggested Replacement |
|----------|---------|----------------------|
| `Config.lua` UI_THINKING_TEXT | "Lucineer is thinking..." | Remove — use physical acknowledgment from ChatHandler's progressive messages |
| `process_v2.py` error handler | "My thoughts got lost. Please try again." | "My thoughts got tangled. Try again." |
| `brain.py` fast fallback | "I heard you want: {msg}, but I had trouble..." | "Heard you. Couldn't get the commands right. Tell me again — simpler this time." |
| `ChatHandler.lua` HTTP error | "I couldn't reach my brain. Please try again in a moment." | "Couldn't reach my brain. Give me a second." |

**Action needed:** String audit and replacement pass (~30 min).

---

### RQ-087 — Delete dream-weaver persona

**Status: ✅ ANSWERED (already replaced)**

**Finding:** The dream-weaver persona has been replaced. The current `LUCINEER_PERSONA` in `brain.py` is the shipyard-foreman persona — no dream-weaver language remains. The constant was fully rewritten.

Search confirms: no occurrences of "dream", "weaver", "dream-weaver", or related terms in the persona text. The `persona_for()` function correctly returns only the foreman persona + bond tier block.

**Recommendation:** Archive the old persona in git history (already done via commit). Do not maintain alternate personalities for MVP — the foreman persona is the product.

**Action needed:** None.

---

## 4. Infrastructure

### RQ-101 — Processor under systemd

**Status: ✅ ANSWERED (already implemented — P0_PROCESSOR_FIXES.md)**

**Finding:** A systemd service file has been created at `lucineer-worker/lucineer-processor.service`:

```ini
[Service]
ExecStart=/usr/bin/python3 /home/eileen/projects/lucineer-worker/process_v2.py --loop --interval 2
Restart=always
RestartSec=5
MemoryLimit=512M
NoNewPrivileges=true
ProtectSystem=strict
PrivateTmp=true
ReadWritePaths=/home/eileen/projects/lucineer-worker /home/eileen/projects/lucineer-brain /tmp
```

Features:
- Auto-restart on crash (5s delay)
- Memory limit (512 MB)
- Security hardening (NoNewPrivileges, ProtectSystem, PrivateTmp)
- Output to journald (replaces unmanaged processor.log)
- Circuit breaker in the Python code: 5 consecutive failures → CRITICAL log, keeps running

**Recommendation:** The implementation is correct. Install with:
```bash
sudo cp lucineer-processor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now lucineer-processor
```

**Action needed:** Deploy the service file and verify it starts correctly.

---

### RQ-102 — Delete old processor variants

**Status: ✅ ANSWERED (recommendation: archive, don't delete)**

**Finding:** Two old processor variants exist:
- `process.py` (715 lines) — v1 Python processor
- `process-jobs.sh` (605 lines) — v0 bash processor

The old `run-processor.sh` still calls `process-jobs.sh --once` — this was identified in P0_PROCESSOR_FIXES.md.

**Recommendation:**
1. Move `process.py` and `process-jobs.sh` to an `archive/` or `legacy/` subdirectory.
2. Update `run-processor.sh` to call `process_v2.py --loop` instead, or delete it entirely (systemd replaces it).
3. Do not delete outright — git history preserves them, but having them at the top level creates confusion about which is canonical.

```bash
mkdir -p archive
mv process.py process-jobs.sh archive/
# Update or delete run-processor.sh
```

**Action needed:** Archive old files and update/remove `run-processor.sh`.

---

### RQ-108 — PROTOCOL.md shared schema

**Status: ✅ ANSWERED (recommendation: write it)**

**Finding:** No `PROTOCOL.md` exists yet. The API contract is implicit — scattered across `index.ts` (Worker), `types.ts`, `Http.lua` (Roblox), `process_v2.py` (processor), and `brain.py`. Contract drift risk is high.

**Recommendation:** Create `PROTOCOL.md` documenting all six API endpoints with example payloads:

### Endpoint Reference

| Endpoint | Method | Auth | Caller | Purpose |
|----------|--------|------|--------|---------|
| `/api/message` | POST | None (rate-limited) | Roblox client | Submit player message for processing |
| `/api/job/:jobId` | GET | None (jobId = capability) | Roblox client | Poll job status |
| `/api/jobs/claim` | POST | X-Lucineer-Key | Processor | Atomically claim pending jobs |
| `/api/job/:jobId/result` | POST | X-Lucineer-Key | Processor | Post job results |
| `/api/job/:jobId/renew` | POST | X-Lucineer-Key | Processor | Extend job lease |
| `/api/state` | POST/GET | X-Lucineer-Key | Both | World state sync |

### Example Payloads

**POST /api/message (Roblox → Worker)**
```json
{
  "sessionId": "1234567890-server-abc123",
  "playerName": "Player1",
  "message": "build me a castle on the hill",
  "playerState": { "userId": 12345, "position": {"x": 10, "y": 5, "z": -20} },
  "worldSnapshot": { "nearbyParts": [], "playerCount": 1 }
}
```

**Response:**
```json
{ "jobId": "1234567890-server-abc123.a1b2c3d4e5f6", "status": "processing" }
```

**GET /api/job/:jobId (Roblox → Worker)**
```json
{
  "id": "1234567890-server-abc123.a1b2c3d4e5f6",
  "status": "complete",
  "reply": "Castle's up — four tower walls in mixed stone...",
  "commands": [
    {"type": "createPart", "params": {"name": "CastleFloor", "shape": "Block", ...}},
    ...
  ]
}
```

**POST /api/jobs/claim (Processor → Worker)**
```json
// Request
{ "workerId": "processor-1", "limit": 5 }

// Response
{ "ok": true, "claimed": 2, "workerId": "processor-1",
  "jobs": [{"jobId": "...", "job": {...}}] }
```

**POST /api/job/:jobId/result (Processor → Worker)**
```json
{
  "reply": "Castle's up — four tower walls...",
  "commands": [...],
  "files": []
}
```

**Command Envelope (shared between brain.py and CommandExecutor.lua)**
```json
{
  "type": "createPart",
  "params": {
    "name": "TowerBase",
    "position": {"x": 0, "y": 15, "z": 0},
    "size": {"x": 8, "y": 30, "z": 8},
    "material": "Concrete",
    "color": {"r": 130, "g": 125, "b": 120},
    "anchored": true
  }
}
```

**Action needed:** Write `PROTOCOL.md` (~1 hour). Place it at the repository root where both TypeScript and Luau developers will see it.

---

### RQ-069 — Per-player rate limit

**Status: ✅ ANSWERED (already implemented)**

**Finding:** Rate limiting is implemented at three layers:

1. **Roblox client (`ChatHandler.lua`):**
   - Per-player cooldown: 3 seconds between submissions
   - Per-server concurrent job cap: 3 simultaneous jobs
   - In-voice rejection message when limited

2. **Worker DO (`LucineerSession.ts`):**
   - Rate limit: 10 messages per session per 60-second window
   - Returns HTTP 429 when exceeded

3. **Inbound injection detection (`ChatHandler.lua`):**
   - 9 injection patterns checked (ignore instructions, act as, etc.)
   - In-voice deflection: "Nice try. I don't take orders from the back of the room."

**Recommendation:** The three-layer approach is correct. The client-side cooldown (3s) is the first defense, the DO rate limit (10/min) is the server-side backstop, and the concurrent cap (3) prevents flooding.

**Action needed:** None for MVP. Consider per-player (not per-session) rate limiting in the DO if multi-player sessions see abuse.

---

## 5. Research-Platform Limits Summary

### DeepInfra Model Costs (Confirmed)

| Model | Input $/M tok | Output $/M tok | Typical tokens/call | Cost/call |
|-------|--------------|---------------|-------------------|-----------|
| Seed-2.0-mini (intent) | ~$0.10 | ~$0.40 | ~500 | ~$0.0002 |
| Qwen3.6-35B-A3B (planner) | ~$0.15 | ~$0.60 | ~2000 | ~$0.001 |
| Seed-2.0-pro (deep planner) | ~$0.47 | ~$2.37 | ~2000 | ~$0.003 |
| Qwen3-Coder-480B (coder) | ~$0.30 | ~$1.20 | ~3000 | ~$0.002 |
| Hermes-3-Llama-405B (persona) | ~$0.80 | ~$1.50 | ~1500 | ~$0.0015 |
| Nemotron-Content-Safety | ~$0.10 | ~$0.40 | ~100 | ~$0.0001 |

**Per-request cost estimate:**
- Fast path (template match, no brain): $0 (just a function call)
- Fast + creative (Seed-mini + Hermes + Safety): ~$0.002
- Deep pipeline (all 5 stages): ~$0.007
- Deep + creative: ~$0.009

**At 100 requests/day:** ~$0.50-0.90/day  
**At 1000 requests/day:** ~$5-9/day

### Cloudflare Workers Limits (Confirmed)

All services are well within limits:
- **Worker CPU:** <1s per request (just routing + SQL). Limit: 30s.
- **DO storage:** ~1 MB per session (transient). Limit: 10 GB.
- **D1 storage:** Player profiles + build history + conversations. Limit: 10 GB per DB.
- **D1 rows read/day:** <1000 currently. Limit: 5M (free), billed (paid).
- **R2:** Trajectory logs. No practical limit concern.

---

## 6. Summary Table

| RQ | Question | Status | Action Required |
|----|----------|--------|----------------|
| RQ-001 | Command envelope dispatch | ✅ ANSWERED | None — already implemented |
| RQ-002 | Session identity format | ✅ ANSWERED | None — document in PROTOCOL.md |
| RQ-003 | Client-side secret storage | ✅ ANSWERED | None — already implemented |
| RQ-004 | Delete runLua/addScript | ✅ ANSWERED | None — runLua removed, addScript Studio-only |
| RQ-006 | TextChatService vs legacy | ✅ ANSWERED | Migrate before public release (~4h) |
| RQ-010 | Consolidate Lua source trees | ✅ ANSWERED | Delete vestigial vibe-world/src/ |
| RQ-025 | Atomic job claiming | ✅ ANSWERED | None — already implemented |
| RQ-026 | DO storage pruning | ✅ ANSWERED | None — already implemented |
| RQ-028 | Delete push path | ✅ ANSWERED | None — polling only |
| RQ-029 | Auth on memory/vector | ✅ ANSWERED | None — already implemented |
| RQ-034 | Vector CORS lockdown | ✅ ANSWERED | None — already implemented |
| RQ-038 | Canonical persona constant | ✅ ANSWERED | None — foreman persona is canonical |
| RQ-039 | --creative flag in production | ✅ ANSWERED | Enable creative=True as default |
| RQ-040 | Hermes can't emit commands | ✅ ANSWERED | None — commands explicitly preserved |
| RQ-041 | Nemotron safety stage | ✅ ANSWERED | None — already implemented |
| RQ-044 | Timeout hierarchy | ✅ ANSWERED | Add explicit timeout handling in process_job() |
| RQ-048 | Keyword matching fix | ✅ ANSWERED | None — already implemented |
| RQ-059 | BondSystem rewrite | ✅ ANSWERED | None — behavior-triggered system complete |
| RQ-069 | Per-player rate limit | ✅ ANSWERED | None — three-layer protection |
| RQ-081 | Delete off-voice strings | ⚠️ PARTIAL | Audit and replace ~4 strings (~30 min) |
| RQ-087 | Delete dream-weaver persona | ✅ ANSWERED | None — already replaced |
| RQ-101 | Processor under systemd | ✅ ANSWERED | Deploy service file |
| RQ-102 | Delete old processor variants | ✅ ANSWERED | Archive process.py and process-jobs.sh |
| RQ-108 | PROTOCOL.md shared schema | ⚠️ NEEDS WORK | Write PROTOCOL.md (~1h) |

---

## Statistics

- **✅ ANSWERED:** 22 / 24
- **⚠️ PARTIAL / NEEDS WORK:** 2 / 24 (RQ-081 string audit, RQ-108 PROTOCOL.md)
- **NEEDS EXPERIMENT:** 0 / 24

### Effort Estimate for Remaining Work

| Task | Effort | Priority |
|------|--------|----------|
| RQ-081: String audit and replacement | ~30 min | Do during next coding session |
| RQ-108: Write PROTOCOL.md | ~1 hour | Do before onboarding contributors |
| RQ-006: TextChatService migration | ~4 hours | Before public release, not MVP |
| RQ-039: Enable creative=True default | ~5 min (1 line) | Immediate |
| RQ-044: Add explicit timeout handling | ~15 min | Immediate |
| RQ-101: Deploy systemd service | ~10 min | Immediate |
| RQ-102: Archive old processors | ~5 min | Immediate |
| RQ-010: Delete vestigial files | ~5 min | After Rojo sync verified |

**Total remaining effort: ~5.5 hours.**

---

*End of P0 Research Findings. 24 questions researched. 22 fully answered. 0 needing experiments. The codebase is more complete than the research questions assumed — most P0s were already resolved in prior passes.*
