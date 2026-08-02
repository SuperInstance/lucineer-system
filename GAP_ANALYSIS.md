# LUCINEER — GAP ANALYSIS

**Date:** 2026-08-02
**Scope:** `lucineer-worker/`, `lucineer-roblox/src/`, `lucineer-brain/`,
`lucineer-memory/src/`, `lucineer-vector/src/`, plus `vibe-world/lucineer-ready.rbxlx`
**Method:** full read of every source file in scope; cross-service grep for call sites.

---

## EXECUTIVE SUMMARY

The infrastructure is real and well-built. The Worker, the Durable Object, the D1 schema,
the Vectorize index, and the five-model brain are all competent, deployed, and healthy in
isolation.

**They are not connected to each other.**

The system has been validated component-by-component via `curl`, and every component
passes. It has never been validated end-to-end from Roblox, and the seams between
components do not line up. There are three separate contract mismatches between the
Roblox client and the Worker, one dispatch bug in the command executor that would flatten
every build to an identical gray box, and two entire services (`lucineer-memory`,
`lucineer-vector`) with **zero call sites anywhere in the codebase.**

This is not a polish problem. The honest status is:

> **A player who joins the game today, types "build me a castle," and waits, will see
> nothing happen at all.** The HTTP request 400s before a job is ever created.

The good news is that this is the *cheap* kind of broken. Every issue below is a
well-scoped fix in a file that already exists. There is no architecture to redo. Gaps
#1, #2, and #6 are roughly a day of work together and they take the system from
"nothing happens" to "the core loop runs."

**Counts:** 6 × P0 (blocks release), 4 × P1 (should fix), 6 × P2 (in the appendix).

### The critical path

```
#1 params dispatch  ──┐
#2 API contracts    ──┼──► core loop works at all
#6 job claiming     ──┘
                          │
#3 secret handling  ──────┼──► safe to make public
#5 text filtering   ──────┘
                          │
#4 memory wiring    ──────────► the character has continuity
#7 persona conflict ──────────► the character has a voice
```

---

## P0 — BLOCKS RELEASE

---

### #1 — `CommandExecutor` never receives its parameters. Every build is the same gray box.

**Severity: P0. This is the single highest-impact bug in the system.**

**What's broken**

`CommandExecutor.lua:393` dispatches the *entire command envelope* to the handler:

```lua
local ok, result = pcall(handler, command)
```

But every handler reads the fields directly off its argument. `CommandExecutor.lua:95`:

```lua
function CommandExecutor.createPart(params: table): Instance
    part.Name = params.name or "LucineerPart"
    part.Position = parseVector3(params.position or { x = 0, y = 5, z = 0 })
    part.Size = parseVector3(params.size or { x = 4, y = 1, z = 4 })
```

Both the templates (`process_v2.py:118`) and the brain (`brain.py:374`) emit the
documented envelope shape:

```json
{"type": "createPart", "params": {"name": "TowerBase", "size": {...}, ...}}
```

So `command.name` is `nil`, `command.position` is `nil`, `command.size` is `nil`.

**Every fallback fires.** Every single part created by this system — from every template,
from every brain response — is:

- named `LucineerPart`
- at position `(0, 5, 0)`
- sized `4 × 1 × 4`
- `SmoothPlastic`, color `(180,180,180)`

A 20-command castle produces **twenty identical gray slabs occupying the same cubic
volume at the world origin.**

The same bug hits `sendMessage`: `LucineerServer/init.lua:80` reads `cmd.message`, but
the message is at `cmd.params.message`. Every Lucineer line is dropped.

**Why it survived:** the shape is only wrong at the *boundary*. Unit-testing
`CommandExecutor.createPart({name="X"})` directly passes. Testing the Python side with
`curl` produces correct-looking JSON. Only running both together exposes it — and that
has never happened (see #2, which prevents it from happening).

**Fix** — `CommandExecutor.lua:378`, and make the boundary explicit so it can't drift again:

```lua
function CommandExecutor.execute(command: { [string]: any }): (any, string?)
    if type(command) ~= "table" then
        return nil, "Command must be a table"
    end

    local cmdType = command.type
    if not cmdType then
        return nil, "Command missing 'type' field"
    end

    local handler = commandMap[cmdType]
    if not handler then
        return nil, string.format("Unknown command type: '%s'", cmdType)
    end

    -- Commands are envelopes: { type = "createPart", params = { ... } }.
    -- Accept a flat command as a fallback so hand-written test payloads still work.
    local params = command.params
    if type(params) ~= "table" then
        params = command
    end

    local ok, result = pcall(handler, params)
    if not ok then
        local err = tostring(result)
        warn(string.format("[Lucineer] CommandExecutor: '%s' failed: %s", cmdType, err))
        return nil, err
    end

    return result, nil
end
```

And `LucineerServer/init.lua:76`:

```lua
for _, cmd in ipairs(commands) do
    if cmd.type == "sendMessage" then
        local p = cmd.params or cmd
        ResponseRemote:FireClient(player, { type = "message", message = p.message })
    end
end
```

**Also fix the `addLight` contract while you're here.** The templates emit
`{"parent": "TowerLantern", "lightType": "PointLight", ...}` (`process_v2.py:121`) but
`CommandExecutor.addLight` (`:172`) reads `params.type` and `params.position` and has no
concept of `parent`. Even after the params fix, every light detaches from its lantern,
lands in the folder root, and takes the default range of 16. Add:

```lua
function CommandExecutor.addLight(params: table): Instance
    local folder = ensureFolder()
    -- Accept both "type" and "lightType" from generators
    local lightType = params.type or params.lightType or "Point"
    lightType = lightType:gsub("Light$", "")  -- "PointLight" -> "Point"

    local parent: Instance
    if params.parent then
        parent = findPartByName(params.parent) or folder
    elseif params.position then
        parent = -- ...existing carrier-part logic...
    else
        parent = folder
    end
    -- ...
```

**Verification:** in Studio, run one template and confirm distinct named parts at
distinct positions. This is the smoke test that should gate every future change.

---

### #2 — The Roblox client and the Worker do not speak the same protocol. Nothing reaches the queue.

**Severity: P0.**

Three independent contract mismatches. Any one of them breaks the loop; all three are live.

#### 2a. `POST /api/message` — 400 on every request

`ChatHandler.lua:44` sends:

```lua
local payload = {
    playerId   = player.UserId,
    playerName = player.Name,
    message    = message,
    worldState = worldState,
    placeId    = game.PlaceId,
}
```

`worker/src/index.ts:32` requires:

```ts
if (!body.sessionId || !body.playerName || !body.message) {
  return Response.json({ error: "Missing required fields: sessionId, playerName, message" },
                       { status: 400 });
}
```

**The string `sessionId` does not appear anywhere in `lucineer-roblox/src/`.** Verified
by grep. Every chat message returns 400. No job is ever created. The Poller is never
given a job ID. The player sees nothing.

`Http.request` treats a 400 as retryable (`Http.lua:88` only accepts `result.Success`),
so each chat message becomes **4 HTTP requests over ~7.5 seconds of exponential backoff**
before giving up.

#### 2b. `POST /api/state` — 400 every 10 seconds, per player

`LucineerServer/init.lua:111` sends `{playerId, playerName, state}`. `index.ts:129`
requires `{sessionId, worldSnapshot}`. Same 400, same 4× retry, fired on a timer for
every player forever. `syncState()` also runs two full workspace traversals per player
per tick (see #10) to build a payload that is then rejected.

#### 2c. Job results use `reply`; the server reads `message`

`types.ts:40` defines `JobResult.reply`. `LucineerSession.ts:131` stores it in the
`reply` column. `getJob` returns `reply`. But `LucineerServer/init.lua:87`:

```lua
if response.message then
    ResponseRemote:FireClient(player, { type = "message", message = response.message })
end
```

`response.message` is always `nil`. **Even if 2a were fixed, Lucineer's dialogue would
never reach the player** — the only text a player could ever see is the generic
client-side summary at `LucineerClient/init.lua:85` ("Done! I built 8 action(s) for
you."), which is itself a voice violation (see #7).

**Fix** — introduce a real session identity and align all three payloads.

`Config.lua`, add:

```lua
-- Session identity. JobId is unique per server instance; PlaceId scopes it.
Config.SESSION_ID = string.format("%d-%s", game.PlaceId,
    (game.JobId ~= "" and game.JobId or "studio"))
```

`ChatHandler.lua:44`:

```lua
local payload = {
    sessionId  = Config.SESSION_ID,
    playerName = player.Name,
    message    = message,
    playerState = {
        userId   = player.UserId,
        position = worldState.player and worldState.player.position or nil,
    },
    worldSnapshot = worldState,
}
```

`LucineerServer/init.lua:111`:

```lua
local _, err = Http.post("/api/state", {
    sessionId     = Config.SESSION_ID,
    worldSnapshot = state,
})
```

`LucineerServer/init.lua:86`, accept both keys during the transition:

```lua
local text = response.reply or response.message
if text then
    ResponseRemote:FireClient(player, { type = "message", message = text })
end
```

**Also:** `Http.request` should not retry 4xx. Client errors are not transient — retrying
a 400 four times just multiplies the damage. `Http.lua:95`:

```lua
else
    lastErr = string.format("HTTP %d: %s", result.StatusCode, result.Body or "")
    -- 4xx is a contract error, not a transient failure. Fail fast.
    if result.StatusCode >= 400 and result.StatusCode < 500 and result.StatusCode ~= 429 then
        return nil, lastErr
    end
end
```

**Root cause worth naming:** there is no shared schema between the TypeScript and Luau
sides. `types.ts` is the de facto contract and the Lua has never been checked against it.
A single `PROTOCOL.md` with example payloads for all six endpoints — and one Studio smoke
test that exercises each — prevents this whole class of failure.

---

### #3 — The API key ships to every player, in plaintext, in four files.

**Severity: P0. Security.**

`Config.lua:13`:

```lua
Config.AUTH_KEY = "feba836ba409a7e959d957c7c4051fa6243a3436367073e52c567f979f49c9a7"
```

`Config.lua` lives at `ReplicatedStorage/Lucineer/Config` (`default.project.json:9`).
**ReplicatedStorage is replicated to every connected client.** Any player with a standard
executor can read that string in one line and then has full authenticated access to every
Worker endpoint: inject jobs, read other sessions' world state, and burn DeepInfra credit
without limit.

The same key is committed in four places:

```
lucineer-roblox/src/ReplicatedStorage/Lucineer/Config.lua:13
lucineer-worker/process.py:11
lucineer-worker/process-jobs.sh:21
lucineer-worker/process_v2.py:29
```

…and is embedded a fifth time in the shipping place file,
`vibe-world/lucineer-ready.rbxlx`.

**Fix**

1. **Rotate the key immediately.** It is in git history across two repositories and in a
   distributable `.rbxlx`. Treat it as public.

2. **Split the config.** `HttpService` is server-only, so nothing client-side ever needs
   the key or the URL. Move both to a server-only module:

   `src/ServerScriptService/LucineerServer/ServerConfig.lua`:
   ```lua
   local ServerConfig = {}
   ServerConfig.WORKER_URL = "https://lucineer-relay.casey-digennaro.workers.dev"
   -- Never hardcoded. Set via Studio: Game Settings > Security, or a private
   -- ModuleScript excluded from source control.
   ServerConfig.AUTH_KEY = game:GetService("ServerStorage")
       :WaitForChild("LucineerSecret").Value
   return ServerConfig
   ```

   Leave only presentation values (`UI_COLOR`, `BOT_NAME`, `POLL_INTERVAL`) in the
   replicated `Config`. Update `default.project.json` accordingly.

3. **Python side:** read from the environment, not a literal.
   ```python
   AUTH_KEY = os.environ["LUCINEER_KEY"]  # fail loudly if unset
   ```

4. **Prefer a per-server token over a shared static key.** A single global secret means
   one leak compromises everything with no revocation path. The Worker should mint a
   short-lived token scoped to `sessionId`, and the Roblox server should exchange a
   place-level credential for it at startup. That's a follow-up, but the shared-key
   design is what makes the leak catastrophic rather than annoying.

---

### #4 — `lucineer-memory` and `lucineer-vector` have zero call sites. `bond_level` is a dead column.

**Severity: P0 for the product, even though nothing is "broken."**

Both services are deployed, healthy, and — verified by grep across
`lucineer-worker/`, `lucineer-roblox/`, `lucineer-brain/` — **called by nothing.**

```
$ grep -rniE "api/memory|lucineer-memory" lucineer-worker lucineer-roblox lucineer-brain
(no results)

$ grep -rniE "api/skills|lucineer-vector" lucineer-worker lucineer-roblox lucineer-brain
(only auto-generated type definitions in worker-configuration.d.ts)
```

Consequences:

- **`player_profiles.bond_level`** (`schema.sql:8`) is written by exactly one endpoint
  that nothing calls, and read by nothing. The entire relationship arc in
  `CHARACTER_BIBLE.md` §4 has no substrate.
- **`build_history`** is empty. Lucineer cannot reference a previous build, which is the
  most-cited trait in his voice spec and the mechanism behind Magic Moment 2.
- **`conversations`** is empty. He has no memory within a session, let alone across
  sessions. Every message is turn one.
- **`skills.uses_count`** is never incremented; the ranking in
  `memory/src/index.ts:159` (`ORDER BY uses_count DESC`) is always a no-op.
- **The 35-skill Vectorize index is never queried.** `brain.py` writes Luau command JSON
  from scratch every time, with a semantic library of verified patterns sitting unused.
  That library is the highest-leverage quality lever in the system and it is switched off.

**Additionally, the memory Worker has no authentication whatsoever.** `memory/src/index.ts:36`
routes straight from `fetch` to the D1 queries with no key check. Every player profile,
conversation log, and skill is publicly readable and writable by anyone who finds the
hostname. `lucineer-vector` is the same, and additionally sets
`Access-Control-Allow-Origin: *` (`vector/src/index.ts:194`), so the skill index can be
poisoned from a browser tab and Workers AI quota can be burned by anyone.

**And a data-loss bug:** `memory/src/index.ts:61` — the player upsert always writes
`bond_level = Number(body.bond_level ?? 0)`. Any profile write that omits `bond_level`
**silently resets the player's bond to zero.** Fix before the column carries meaning:

```sql
INSERT INTO player_profiles (player_name, preferences, bond_level, first_seen, last_seen)
VALUES (?, ?, ?, datetime('now'), datetime('now'))
ON CONFLICT(player_name) DO UPDATE SET
  preferences = excluded.preferences,
  bond_level  = COALESCE(?, player_profiles.bond_level),  -- null = leave it alone
  last_seen   = datetime('now')
```

with `bond_level` bound as `body.bond_level === undefined ? null : Number(body.bond_level)`.

**Fix — wire memory into the processor.** In `process_v2.py`, around `process_job`:

```python
MEMORY_URL = os.environ.get("LUCINEER_MEMORY_URL",
                            "https://lucineer-memory.casey-digennaro.workers.dev")
VECTOR_URL = os.environ.get("LUCINEER_VECTOR_URL",
                            "https://lucineer-vector.casey-digennaro.workers.dev")

def get_player_context(player_name):
    """Fetch bond level, preferences, and recent builds for prompt injection."""
    profile = api_get_json(f"{MEMORY_URL}/api/memory/player/{player_name}") or {}
    builds  = api_get_json(f"{MEMORY_URL}/api/memory/builds/{player_name}?limit=5") or {}
    return {
        "bond_level":  int(profile.get("bond_level", 0)),
        "preferences": json.loads(profile.get("preferences") or "{}"),
        "recent_builds": [b.get("description", "") for b in builds.get("builds", [])],
    }

def recall_skills(message, top_k=3):
    """Semantic lookup against the 35-skill Vectorize library."""
    res = api_post_json(f"{VECTOR_URL}/api/skills/query",
                        {"query": message, "top_k": top_k, "return_metadata": True})
    return [m["metadata"] for m in (res or {}).get("matches", []) if m.get("score", 0) > 0.6]

def record_build(job, reply, commands, ctx):
    api_post_json(f"{MEMORY_URL}/api/memory/build", {
        "session_id":    job.get("sessionId", ""),
        "player_name":   job.get("playerName", ""),
        "description":   job.get("message", ""),
        "command_count": len(commands),
        "location":      {"x": ctx["px"], "y": ctx["py"], "z": ctx["pz"]},
    })
    api_post_json(f"{MEMORY_URL}/api/memory/conversation", {
        "session_id":  job.get("sessionId", ""),
        "player_name": job.get("playerName", ""),
        "role": "assistant", "content": reply,
    })
```

Then pass `bond_level` into `persona_for()` (`CHARACTER_BIBLE.md` §9), the recent builds
into the prompt as callback material, and the recalled skills into the coder stage as
few-shot examples.

**Sequencing note:** add auth to both Workers *before* wiring them in. Adding a key
afterwards means a second round of client changes.

---

### #5 — No text filtering on AI-generated output. This is a Roblox policy problem, not a taste problem.

**Severity: P0 for a public release.**

Grep for `FilterStringAsync`, `TextService`, or `TextChatService` across
`lucineer-roblox/src/` returns **nothing.**

Lucineer's replies are model-generated from player-supplied input and displayed to every
player in the server. That is user-influenced text being broadcast, and Roblox requires
it to pass through the text filter before display. Ignoring this risks moderation action
against the experience — the kind of thing that ends a launch rather than delaying it.

There is also no filtering of **inbound** player messages before they're sent off-platform
to DeepInfra, and no safety pass on the model output. `ROUNDTABLE_BRIEF.md` lists
`Nemotron-Content-Safety-3.5` in the pipeline; it appears in **no code path** in
`brain.py` or `process_v2.py`.

**Fix — filter on the way out**, in `LucineerServer/init.lua`:

```lua
local TextService = game:GetService("TextService")

--[[ Filter AI text for a specific recipient. Roblox requires this for any
     user-influenced text shown to players. ]]
local function filterFor(text: string, player: Player): string
    local ok, result = pcall(function()
        local filtered = TextService:FilterStringAsync(
            text, player.UserId, Enum.TextFilterContext.PublicChat)
        return filtered:GetChatForUserAsync(player.UserId)
    end)
    if ok and result then
        return result
    end
    warn("[Lucineer] filter failed; suppressing message")
    return "..."   -- fail closed. Never show unfiltered text.
end
```

Route every outbound line through it:

```lua
local text = response.reply or response.message
if text then
    ResponseRemote:FireClient(player, { type = "message", message = filterFor(text, player) })
end
```

**Fail closed, not open.** If the filter errors, show nothing. Showing unfiltered text
on filter failure is exactly the case moderation catches.

**Add the safety stage to the brain.** It's listed in the architecture and absent from
the code:

```python
SAFETY_MODEL = "nvidia/Nemotron-Content-Safety-3.5"

def stage_safety(api_key, reply, player_message):
    """Kid-safe verification. Returns (is_safe, reason)."""
    verdict = call_model(api_key, SAFETY_MODEL, messages=[
        {"role": "system", "content":
            "Classify for a children's game (Roblox, ages 9+). Reply with exactly "
            "SAFE or UNSAFE followed by a brief reason."},
        {"role": "user", "content": f"Player said: {player_message}\nReply: {reply}"},
    ], max_tokens=64, temperature=0.0)
    return verdict.strip().upper().startswith("SAFE"), verdict
```

Run it on the final reply. On UNSAFE, substitute an in-voice deflection rather than an
error — the character should never visibly hit a guardrail:

```python
if not is_safe:
    reply = "Not building that. Pick something else."
    commands = []
```

**Also add a rate limit.** `ChatHandler.lua:109` fires a job on *every* chat message with
no throttle. One player holding down enter is unbounded DeepInfra spend. Per-player
cooldown of ~3 seconds plus a per-server concurrent-job cap belongs in `ChatHandler.init`.

---

### #6 — The job queue has no claiming, no TTL, and one Durable Object for the entire game.

**Severity: P0.**

#### 6a. No claiming → duplicate work and an infinite reprocessing loop

`LucineerSession.ts:178`:

```ts
async getPendingJobs(): Promise<Job[]> {
  const cursor = this.ctx.storage.sql.exec(
    `SELECT * FROM jobs WHERE status = 'processing' ORDER BY created_at ASC LIMIT 10`);
```

Jobs are created with `status = 'processing'` (`LucineerSession.ts:70`) and only leave
that status when a result is posted. `getPendingJobs` is a **read with no state
transition.**

Therefore:

- Two processor instances both see the same job and both process it. Both call DeepInfra.
  Both post results. The player gets whichever lands last, having paid twice.
- If a job's result post fails for any reason, the job stays `processing` **forever** and
  is returned by every subsequent poll. `process_v2.py` polls every 2 seconds. That is a
  permanent, self-sustaining loop through the 480B coder model. A single failed callback
  becomes an unbounded bill.

There is no `attempts` counter and no dead-letter path.

**Fix** — atomic claim with a lease:

```ts
async claimPendingJobs(workerId: string, limit = 5): Promise<Job[]> {
  const now = Date.now();
  const LEASE_MS = 180_000;   // 3 min — longer than DEEP_TIMEOUT
  const MAX_ATTEMPTS = 3;

  // Reclaim expired leases and retire jobs that have burned their attempts.
  this.ctx.storage.sql.exec(
    `UPDATE jobs SET status = 'error', error = 'max attempts exceeded', completed_at = ?
     WHERE status = 'claimed' AND lease_expires_at < ? AND attempts >= ?`,
    now, now, MAX_ATTEMPTS);

  this.ctx.storage.sql.exec(
    `UPDATE jobs SET status = 'pending' WHERE status = 'claimed' AND lease_expires_at < ?`,
    now);

  const rows = this.ctx.storage.sql.exec<{ id: string }>(
    `SELECT id FROM jobs WHERE status = 'pending' ORDER BY created_at ASC LIMIT ?`,
    limit).toArray();

  if (rows.length === 0) return [];

  const placeholders = rows.map(() => "?").join(",");
  this.ctx.storage.sql.exec(
    `UPDATE jobs SET status = 'claimed', claimed_by = ?, lease_expires_at = ?,
            attempts = attempts + 1
     WHERE id IN (${placeholders})`,
    workerId, now + LEASE_MS, ...rows.map(r => r.id));

  return rows.map(r => this.rowToJob(r.id));
}
```

Schema additions (`LucineerSession.ts:20`): `attempts INTEGER NOT NULL DEFAULT 0`,
`claimed_by TEXT`, `lease_expires_at INTEGER`. Change the initial insert to
`status = 'pending'`. The `Poller`'s `pending`/`processing`/`queued` handling
(`Poller.lua:98`) already tolerates both names.

#### 6b. Jobs and history grow without bound

`jobs` and `message_history` are never pruned. A Durable Object's SQLite store has a
finite size limit; a busy game reaches it and then **every write fails**, which manifests
as the whole system dying with no obvious cause.

Add an alarm-based sweep:

```ts
async alarm() {
  const cutoff = Date.now() - 24 * 60 * 60 * 1000;
  this.ctx.storage.sql.exec(
    `DELETE FROM jobs WHERE completed_at IS NOT NULL AND completed_at < ?`, cutoff);
  this.ctx.storage.sql.exec(
    `DELETE FROM message_history WHERE timestamp < ?`, cutoff);
  await this.ctx.storage.setAlarm(Date.now() + 60 * 60 * 1000);
}
```

Long-term history belongs in D1 (`conversations`), which is built for it and already
exists — see #4.

#### 6c. One Durable Object for the entire game

Every route in `worker/src/index.ts` calls `env.LUCINEER_SESSION.getByName("default")` —
lines 40, 87, 110, 137, 147, and 156. The comment at `:39` acknowledges it
("Jobs live in the default DO; world state is session-scoped") but the code does not
implement it.

A Durable Object is single-threaded. **Every request from every player in every server
serializes through one object.** This is a hard concurrency ceiling and it is also why
`getJob` has to guess (`:86`: *"We don't know which session this belongs to"*).

**Fix** — encode the session into the job ID so it can be routed without a lookup:

```ts
// LucineerSession.generateJobId()
private generateJobId(sessionId: string): string {
  const bytes = new Uint8Array(12);
  crypto.getRandomValues(bytes);
  const rand = Array.from(bytes).map(b => b.toString(16).padStart(2, "0")).join("");
  return `${encodeURIComponent(sessionId)}.${rand}`;
}

// index.ts — route by session, not to "default"
function sessionStub(env: Env, sessionId: string) {
  return env.LUCINEER_SESSION.getByName(sessionId);
}

const jobMatch = path.match(/^\/api\/job\/([^/]+)$/);
if (jobMatch && method === "GET") {
  const jobId = decodeURIComponent(jobMatch[1]);
  const sessionId = decodeURIComponent(jobId.split(".")[0]);
  const job = await sessionStub(env, sessionId).getJob(jobId);
  // ...
}
```

Note this also requires relaxing the job-ID regex — `/^\/api\/job\/([\da-f]+)$/`
(`index.ts:83`) only matches lowercase hex and will 404 on any ID containing a session
prefix.

`/api/jobs/pending` then needs to fan out across active sessions, or — better — the
processor should be pushed to rather than polling. Which brings us to:

#### 6d. The push path points at a private IP and cannot work

`index.ts:58` and `wrangler.jsonc:30`:

```
"OPENCLAW_CALLBACK_URL": "http://172.22.219.126:18789/api/lucineer/message"
```

`172.22.x.x` is RFC 1918 private address space — a WSL interface. **A Cloudflare Worker
cannot route to it.** Every `POST /api/message` therefore hits the `catch` at `index.ts:67`,
marks the job as an error, and returns **502** — before the polling processor ever sees
it.

So the current live behavior is: request 400s on missing `sessionId` (#2a); *if* that were
fixed, it would 502 here instead.

**Fix:** either delete the push path and commit to polling (simplest, works today), or
expose the processor via a Cloudflare Tunnel and make the callback a real hostname. Do not
leave a broken push path in the request path — at minimum, make the forward failure
non-fatal so the polling path still works:

```ts
// Don't fail the request if push is unavailable — the processor also polls.
ctx.waitUntil(
  fetch(callbackBase, { /* ... */ }).catch(err =>
    console.warn("push to processor failed; falling back to poll", err))
);
return Response.json({ jobId, status: "processing" });
```

---

## P1 — SHOULD FIX BEFORE RELEASE

---

### #7 — Two contradictory personas, and the personality model never runs.

**Severity: P1 — it doesn't crash, it just means the character isn't in the product.**

Covered in depth in `CHARACTER_BIBLE.md` §0. In summary:

| File | Character | Runs? |
|---|---|---|
| `brain.py:76` `LUCINEER_PERSONA` | Poetic dream-weaver | Only in `--creative` |
| `brain.py:750` `SYSTEM_FAST` | Shipyard foreman | Only in `--fast` |
| `brain.py:349` `SYSTEM_CODER` | *"friendly one or two sentence message"* | **The deep path** |

`process_v2.py:317` invokes:

```python
['python3', BRAIN_SCRIPT, '--verbose', enhanced]
```

Not `--creative`. **The Hermes-405B personality stage is dead code in production.** Every
reply on the deep path is written by Qwen3-Coder under an instruction to be "friendly" —
generic assistant voice.

And when `--creative` *is* passed manually, it applies the dream-weaver persona, which is
the wrong character per the brief.

**Fixes:**

1. Replace `LUCINEER_PERSONA` with the canonical text in `CHARACTER_BIBLE.md` §9.
2. Make `SYSTEM_FAST` reference the same constant rather than duplicating persona text —
   two hand-maintained copies is how they drifted in the first place.
3. Rewrite the reply instruction in `SYSTEM_CODER` (`brain.py:373`):
   ```
   "reply": "Lucineer's line. 1-3 sentences, foreman voice, always names one thing
             left deliberately unfinished. Never 'friendly', never assistant-toned."
   ```
4. `process_v2.py:317` → `['python3', BRAIN_SCRIPT, '--creative', '--verbose', enhanced]`

**Related bug — `stage_hermes` can corrupt the build.** `brain.py:636`:

```python
if "commands" in enhanced and enhanced["commands"]:
    enhanced_result["commands"] = enhanced["commands"]
```

Hermes is a *prose* model given a 2048-token budget (`MAX_TOKENS["hermes"]`) and told to
rewrite one string. If it echoes a truncated or hallucinated command array, that array
silently replaces the coder's verified output. **Never accept commands from the
personality stage.** Delete those three lines and take only `reply`.

**Also:** `run_fast` (`brain.py:794`) requests full build JSON with
`max_tokens=MAX_TOKENS["intent"]` = **1024**. A 5–8 command build with hex colors and
vector positions will frequently exceed that, truncating mid-JSON and falling through to
the parse-failure stub at `:808`. Give the fast path its own budget (~2048).

---

### #8 — Sixty seconds of dead air, then a timeout the player can't distinguish from a crash.

**Severity: P1 — this is the difference between "magical" and "broken."**

**8a. The timeouts are inverted.** `Config.lua:17` sets `POLL_TIMEOUT = 60`.
`process_v2.py:32` sets `DEEP_TIMEOUT = 120`. The brain is allowed twice as long as the
client is willing to wait. **Every deep build that takes 60–120 seconds is abandoned
client-side while the processor is still working** — the result posts to a job nobody is
watching, and the player is told "My thoughts got lost" (`ChatHandler.lua:88`).

Worse, the brain's own budget is far larger than either: `call_model` defaults to
`timeout=300` with `max_retries=3`, and `stage_plan` walks a **five-model fallback chain**
(`brain.py:481`). Worst case is well over ten minutes.

Fix: `POLL_TIMEOUT` must exceed `DEEP_TIMEOUT` must exceed the brain's realistic worst
case. Concretely — brain budget 90s, `DEEP_TIMEOUT` 100s, `POLL_TIMEOUT` 120s. Cap the
planner fallback chain at two models, not five.

**8b. There is no progressive feedback.** The player types, sees "Lucineer is thinking...",
and waits. `ThinkingRemote` is fired exactly twice per job
(`LucineerServer/init.lua:62` and `:100`). For a 40-second deep build that is 40 seconds
of an unchanging pulsing dot.

**Lucineer is a character who narrates while working, and the architecture gives him
nothing to narrate with.**

Fix — emit an immediate acknowledgement before the brain runs, then build progressively:

```python
# process_v2.py — post a fast in-voice ack the moment the job is claimed,
# before the expensive pipeline starts.
ACKS = [
    "Alright. Let me look at the ground first.",
    "Give me a minute. Walking the site.",
    "Heard you. Checking what's already here.",
]
api_post(f"/api/job/{job_id}/progress", {"text": random.choice(ACKS)})
```

And in `CommandExecutor.executeBatch`, **stagger placement instead of materializing
everything in one frame**:

```lua
function CommandExecutor.executeBatch(commands: { table }, onProgress): { table }
    local results = {}
    for i, command in ipairs(commands) do
        local result, err = CommandExecutor.execute(command)
        table.insert(results, { index = i, type = command.type,
                                success = err == nil, result = result, error = err })
        if onProgress then onProgress(i, #commands, result) end
        -- Parts landing one at a time reads as *building*.
        -- All at once reads as a texture pop-in.
        if i % 3 == 0 then task.wait(0.08) end
    end
    return results
end
```

This is a small change with an outsized effect on how the product *feels*. See
`POLISH_PLAN.md` §1.

**8c. No caching.** Identical requests re-run the full five-model pipeline. "build a
house" from ten players is ten full pipelines. Hash `(normalized_message, style, scale)`
and cache commands for 24h in D1 or KV; re-roll only the `reply` text so it still feels
personal.

---

### #9 — The Roblox API layer uses APIs that are disabled, deprecated, or will throw.

**Severity: P1.**

**9a. `runLua` cannot work and shouldn't exist.** `CommandExecutor.lua:339` calls
`loadstring(source)`. `loadstring` requires `ServerScriptService.LoadStringEnabled`, which
is **off by default** and should stay off. The comment at `:326` says *"SECURITY: This
should be gated behind auth"* — it isn't, and `LucineerServer/init.lua:96` calls it with
`response.lua` straight off the network:

```lua
if response.lua then
    CommandExecutor.runLua({ source = response.lua })
end
```

That is arbitrary server-side code execution sourced from an HTTP response, on a shared
key that every client can read (#3). Even non-functional, it should not ship. **Delete
`runLua`, its `commandMap` entry, and the `response.lua` branch.** If dynamic behavior is
needed later, do it with a whitelist of parameterized behaviors, never with source strings.

**9b. `addScript` will throw at runtime.** `CommandExecutor.lua:265` assigns
`scriptInstance.Source`. `Script.Source` is not assignable from a running script — it's
writable only from plugins and the command bar. This raises, gets swallowed by the `pcall`
at `:393`, and silently reports failure. Remove it or restrict it to a Studio-only path.

**9c. `setTerrain` will throw on most inputs.** `CommandExecutor.lua:291`:

```lua
local region = Region3.new(regionStart, regionEnd)
Terrain:FillRegion(region, resolution, material)
```

`FillRegion` requires the region to be aligned to a 4-stud grid; an arbitrary player
position will not be. It also requires a *terrain* material — passing `WoodPlanks` or
`Cobblestone` (both of which `parseMaterial` will happily return) throws. And `FillRegion`
is deprecated in favor of `FillBlock`.

```lua
local TERRAIN_MATERIALS = {
    Grass = true, Rock = true, Sand = true, Water = true, Snow = true,
    Mud = true, Slate = true, Ice = true, Ground = true, Asphalt = true,
}

function CommandExecutor.setTerrain(params: table): boolean
    local size   = parseVector3(params.size or { x = 16, y = 4, z = 16 })
    local center = parseVector3(params.position or { x = 0, y = 0, z = 0 })

    local matName = params.material or "Grass"
    if not TERRAIN_MATERIALS[matName] then
        warn(string.format("[Lucineer] setTerrain: '%s' is not a terrain material", matName))
        matName = "Grass"
    end

    local material = (params.action == "clear")
        and Enum.Material.Air or parseMaterial(matName)

    -- FillBlock takes a CFrame and needs no grid alignment.
    Terrain:FillBlock(CFrame.new(center), size, material)
    return true
end
```

**9d. Legacy chat APIs.** `UIManager.lua:168` uses
`StarterGui:SetCore("ChatMakeSystemMessage")` and `:194` uses `Chat:Chat()`. Both belong
to the legacy chat system; new experiences default to `TextChatService`, where these are
deprecated. `ChatHandler.lua:109` uses `player.Chatted`, which still fires but bypasses
`TextChatService`'s filtering and callbacks — the exact hooks needed for #5.

```lua
-- UIManager: system message
local TextChatService = game:GetService("TextChatService")
function UIManager.displayChatResponse(message: string)
    local channel = TextChatService:FindFirstChild("TextChannels")
        and TextChatService.TextChannels:FindFirstChild("RBXGeneral")
    if channel then
        channel:DisplaySystemMessage(
            string.format('<font color="#00FFAA">[%s]</font> %s', Config.BOT_NAME, message))
        return
    end
    -- legacy fallback
    pcall(function() StarterGui:SetCore("ChatMakeSystemMessage", { --[[...]] }) end)
end

-- UIManager: spatial bubble
function UIManager.showChatBubble(text: string, adornee: Instance)
    TextChatService:DisplayBubble(adornee, text)
end
```

**9e. The client fabricates phantom RemoteEvents.** `LucineerClient/init.lua:21`:

```lua
local ResponseRemote = Lucineer:FindFirstChild("ResponseEvent")
if not ResponseRemote then
    ResponseRemote = Instance.new("RemoteEvent")   -- client-side only!
    ResponseRemote.Parent = Lucineer
end
```

`FindFirstChild` doesn't wait. If the client loads before the server creates the remotes
(`LucineerServer/init.lua:32`), this creates a **client-local** RemoteEvent that the server
can never fire, and then the server's real one replicates in alongside it — two children
with the same name. The client listens to the dead one forever.

```lua
local ResponseRemote = Lucineer:WaitForChild("ResponseEvent", 30)
local ThinkingRemote = Lucineer:WaitForChild("ThinkingEvent", 30)
if not (ResponseRemote and ThinkingRemote) then
    warn("[Lucineer] Client: server remotes never appeared")
    return
end
```

Better still: create the remotes in `default.project.json` so they exist before any script
runs, and remove the race entirely.

---

### #10 — `WorldScanner` walks the entire workspace twice per message, and caps the wrong things.

**Severity: P1 — performance and correctness.**

**10a. Two full traversals per scan.** `WorldScanner.lua:112` iterates
`Workspace:GetDescendants()`, and `countBuilds()` at `:143` iterates it **again**.
`WorldScanner.scan` is called on every chat message (`ChatHandler.lua:41`), and
`quickScan` — which also calls `countBuilds()` — runs for every player every 10 seconds
(`LucineerServer/init.lua:108`).

In a world Lucineer has been building in, `GetDescendants()` is tens of thousands of
instances. Two full traversals on the main thread is a visible frame hitch, and it happens
on a timer whether or not anyone is talking.

**10b. The instance cap discards the wrong instances.** `WorldScanner.lua:113`:

```lua
for _, descendant in ipairs(Workspace:GetDescendants()) do
    if count >= Config.SCAN_MAX_INSTANCES then break end
    -- ...distance check, then insert...
end
table.sort(instances, function(a, b) return a.distance < b.distance end)  -- :168
```

The break happens in **traversal order**, and the sort by distance happens *after*. So the
50 instances kept are the first 50 encountered in the tree, not the 50 nearest. The
structure the player is standing next to can be excluded in favor of something 199 studs
away, purely because of child ordering. Lucineer's spatial context is effectively random.

**10c. `isRelevant` can throw.** `WorldScanner.lua:29`:

```lua
if instance:IsDescendantOf(workspace:FindFirstChildOfClass("Camera")) then
```

If there's no Camera in Workspace, `FindFirstChildOfClass` returns `nil` and
`IsDescendantOf(nil)` raises. The check is also meaningless — the player-character check
immediately below at `:34` is the one doing real work, and it walks the full ancestor
chain for every candidate, which is the expensive way to ask the question.

**Fix** — use a spatial query and keep the nearest, not the first:

```lua
local RELEVANT_CLASSES = {
    Part = true, MeshPart = true, UnionOperation = true, Model = true,
}

local function collectNearby(playerPosition: Vector3): { table }
    -- Spatial query instead of a full-tree walk.
    local params = OverlapParams.new()
    params.FilterType = Enum.RaycastFilterType.Exclude
    params.FilterDescendantsInstances = getCharacterModels()
    params.MaxParts = Config.SCAN_MAX_INSTANCES * 4  -- overshoot, then rank

    local parts = workspace:GetPartBoundsInRadius(
        playerPosition, Config.SCAN_RADIUS, params)

    local candidates = {}
    for _, part in ipairs(parts) do
        if RELEVANT_CLASSES[part.ClassName] then
            local serialized = serializeInstance(part)
            if serialized then
                serialized.distance = (part.Position - playerPosition).Magnitude
                table.insert(candidates, serialized)
            end
        end
    end

    -- Sort BEFORE capping, so we keep the nearest N rather than the first N.
    table.sort(candidates, function(a, b) return a.distance < b.distance end)
    while #candidates > Config.SCAN_MAX_INSTANCES do
        table.remove(candidates)
    end
    return candidates
end
```

And cache the build count rather than recomputing it — maintain a counter that
`CommandExecutor` increments as it creates parts, and have `quickScan` read it:

```lua
-- CommandExecutor
CommandExecutor._partsCreated = 0
-- in createPart, after part.Parent = folder:
CommandExecutor._partsCreated += 1
```

`quickScan` then costs approximately nothing, which matters because it runs on a timer
forever.

---

## APPENDIX — ADDITIONAL FINDINGS (P2)

---

### A1 — Three divergent copies of the Roblox source, and no build step

The Lua exists in three places:

```
lucineer-roblox/src/...                   ← 1,688 lines, the apparent source of truth
vibe-world/src/...                        ← separate repo, separate copy
vibe-world/lucineer-ready.rbxlx           ← 25 KB, the file that actually ships
```

The `.rbxlx` is the artifact that gets opened in Studio, it embeds its own copy of every
module (including the API key), and **nothing syncs it from `lucineer-roblox/src/`.** At
25 KB for nine modules totaling 1,688 lines, the embedded copies are near-certainly
older, smaller versions.

Any fix in this document applied to `lucineer-roblox/src/` **will not reach the game.**

Fix: pick one source of truth (`lucineer-roblox/src/`), delete the others, and use Rojo to
build the place file. `default.project.json` already exists; the missing piece is
`rojo build default.project.json -o lucineer.rbxlx` in a script, plus removing
`vibe-world/src` and treating the `.rbxlx` as a build output rather than a source file.

**Do this before applying any other fix in this document,** or the fixes will be applied
to the wrong copy.

### A2 — The daemon runs the wrong processor

`run-processor.sh:5` invokes `./process-jobs.sh --once` — the **v1 bash template
processor**, not `process_v2.py`. The hybrid brain that `ROUNDTABLE_BRIEF.md` describes as
the production pipeline is not what the running loop executes.

The loop also has no supervision: `while true; sleep 3` in a terminal dies with the
terminal, has no restart policy, no log rotation (`processor.log` is already 10,446 lines),
and no health signal. Move to `systemd`:

```ini
# /etc/systemd/system/lucineer-processor.service
[Unit]
Description=Lucineer Job Processor
After=network-online.target

[Service]
Type=simple
User=eileen
WorkingDirectory=/home/eileen/projects/lucineer-worker
Environment=LUCINEER_KEY=...
ExecStart=/usr/bin/python3 process_v2.py --loop --interval 2
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Then delete `process.py` and `process-jobs.sh` so there's one processor, not three.

### A3 — Keyword matching fires on substrings, in dictionary order

`process_v2.py:299`:

```python
def match_keyword(message):
    msg_lower = message.lower()
    for keyword, builder in KEYWORDS.items():
        if keyword in msg_lower:
            return builder
```

Substring containment, first match wins, insertion order. Real failures:

| Player says | Builds | Why |
|---|---|---|
| "keep it small" | a **castle** | `'keep'` → `b_castle` |
| "take me home" | a **house** | `'home'` → `b_house` |
| "what's the architecture here" | an **arch** | `'arc'` is a substring of "architecture" |
| "search for something" | an **arch** | `'arc'` in "search" |
| "build a castle tower" | a **tower** | `'tower'` precedes `'castle'` in the dict |
| "don't build a wall" | a **wall** | no negation handling |

Fix — match on word boundaries, score all candidates, prefer the longest match, and
require a build verb:

```python
import re

BUILD_VERBS = re.compile(r'\b(build|make|create|put|raise|place|add|give me|construct)\b')
NEGATIONS   = re.compile(r"\b(don'?t|do not|never|stop|no)\b")

def match_keyword(message: str):
    msg = message.lower()
    if NEGATIONS.search(msg) or not BUILD_VERBS.search(msg):
        return None  # let the brain handle conversation and refusals

    best, best_len = None, 0
    for keyword, builder in KEYWORDS.items():
        if re.search(rf'\b{re.escape(keyword)}\b', msg) and len(keyword) > best_len:
            best, best_len = builder, len(keyword)
    return best
```

This also correctly routes "what do you think of my castle?" to the brain instead of
silently constructing a castle.

### A4 — Every build lands at the origin

`process_v2.py:360` reads the player position from `job['playerState']['position']`.
The Roblox client never sends `playerState` (#2a), so `px, py, pz` are always `(0, 0, 0)`
and every template builds at the world origin, on top of the last one. Fixed by #2, but
worth an explicit assertion — a build at exactly `(0,0,0)` should log a warning, since it
almost certainly means position data was lost.

### A5 — `lucineer-vector` creates duplicate vectors on re-upsert

`vector/src/index.ts:96` generates `skill-${slug(name)}-${Date.now()}` for single upserts,
while `:153` (batch seed) uses the stable `skill-${slug(name)}`. Upserting the same skill
twice through `/api/skills/upsert` therefore produces **two vectors** rather than
overwriting one — the index accumulates stale duplicates that compete in search results.
Use the stable ID in both paths.

Also, `/api/skills/seed` (`:148`) awaits one embedding per skill sequentially inside a
single request. For a batch of 35 that's 35 serial AI calls in one Worker invocation,
which risks the subrequest limit and the CPU-time limit. Batch the embedding call, or
chunk the seed into smaller requests.

### A6 — Minor correctness and hygiene

- **`UIManager.showThinking` leaks animation loops** (`UIManager.lua:122`). Each call
  spawns a new `while` loop keyed on `Visible`; two rapid calls leave two loops fighting
  over the same `Dot`. Guard with a token that the loop checks.
- **`UIManager.showThinking` dereferences `_thinkingLabel` without a nil check** (`:109`)
  while checking `_thinkingBar` on the line above.
- **`Poller.tick` calls `checkTimeouts()` every Heartbeat** (`Poller.lua:127`) — 60× per
  second to scan a table that changes seconds apart. Move it inside the interval gate.
- **`Poller` can stack overlapping polls.** `pollJob` runs inside `task.spawn` and can
  block for up to ~7.5 s of `Http` retries, while `tick` spawns a fresh poll every 0.5 s.
  A slow endpoint produces ~15 concurrent in-flight requests per job. Add an in-flight
  flag per job.
- **`parseBody` errors return 500, not 400** (`memory/src/index.ts:25`) — it throws a
  plain `Error`, caught by the outer handler at `:259`, which returns 500 for what is a
  client error.
- **`b_pyramid` says "Seven tiers"** and builds six (`process_v2.py:194`).
- **`table` is not a Luau type.** Used as an annotation in ~20 places, including under
  `--!strict` in `LucineerServer/init.lua:44`. It runs, but every one is an analysis
  error, which means the type checker is effectively off. Use `{ [string]: any }`.
- **Type drift in `types.ts`:** `MessageHistoryEntry` (`:75`) declares `jobId` and no
  `sessionId`, but `getMessageHistory` (`LucineerSession.ts:203`) selects `job_id` and
  `session_id`. The cast is unchecked, so the returned objects don't match the type.

---

## RECOMMENDED ORDER OF WORK

**Do A1 first.** Everything else is wasted effort if it lands in a copy of the source that
doesn't ship.

| # | Gap | Est. | Unblocks |
|---|---|---|---|
| 0 | A1 — one source of truth + Rojo build | 2h | everything |
| 1 | #1 — params dispatch | 1h | builds look like builds |
| 2 | #2 — API contracts + sessionId | 3h | anything happens at all |
| 3 | #6a/#6d — job claiming, non-fatal push | 3h | no runaway spend |
| 4 | **First real Studio playtest** | 2h | *validates 1–3 and will find more* |
| 5 | #3 — rotate key, move server-side | 2h | safe to go public |
| 6 | #5 — text filtering + safety stage | 3h | safe to go public |
| 7 | #7 — one persona, wire `--creative` | 2h | the character exists |
| 8 | #8 — timeouts + progressive build | 4h | it feels magical |
| 9 | #4 — wire memory + vectorize | 6h | the character remembers |
| 10 | #9, #10, #6b/#6c | 6h | it holds up under load |

**Step 4 is the important one.** Every P0 in this document is a boundary failure that a
single ten-minute session in Studio would have caught. The most valuable thing to build
after the fixes is not a feature — it's a repeatable smoke test that drives one message
through the entire stack and asserts a named part exists at an expected position.
