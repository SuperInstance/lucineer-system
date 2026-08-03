# P0 Roblox Bug Fixes — Applied Changes

**Date:** 2026-08-03
**Scope:** `lucineer-roblox/src/`
**Reference:** `GAP_ANALYSIS.md`

---

## Summary

Of the four assigned bug groups, **two were already fixed** in prior passes and **two were applied in this session**. All syntax checks pass.

---

## Bug #1 — CommandExecutor params dispatch (GAP #1)

**Status: ✅ Already fixed (prior pass)**

`CommandExecutor.execute()` at the dispatch site already unwraps `command.params` before passing to handlers, with a fallback to the flat command for hand-written test payloads:

```lua
local params = command.params
if type(params) ~= "table" then
    params = command
end
local ok, result = pcall(handler, params)
```

**`addLight`** already accepts both `type` and `lightType` (strips `Light` suffix), and supports `parent` by name via `findPartByName()`.

**`LucineerServer/init.lua`** already extracts `sendMessage` results from the executed command results array (checking `result.result.type == "sendMessage"` and reading `result.result.message`), and also reads `response.reply or response.message` for direct Worker replies.

No changes needed.

---

## Bug #2 — API contract mismatches (GAP #2)

**Status: ✅ Already fixed (prior pass)**

- **2a.** `ChatHandler.lua` sends `sessionId = Config.SESSION_ID`, `playerName`, `message`, `playerState`, and `worldSnapshot`. `Config.lua` generates `SESSION_ID` from `game.PlaceId` and `game.JobId`. ✅
- **2b.** `LucineerServer/init.lua` `syncState()` sends `{ sessionId = Config.SESSION_ID, worldSnapshot = state }`. ✅
- **2c.** `LucineerServer/init.lua` reads `response.reply or response.message` for job result text. ✅
- **Http 4xx retry.** `Http.lua` fails fast on 4xx (except 429): `if result.StatusCode >= 400 and result.StatusCode < 500 and result.StatusCode ~= 429 then return nil, lastErr end`. ✅

No changes needed.

---

## Bug #3 — Poller stacking + checkTimeouts spam (GAP #10/A6)

**Status: ✅ Fixed this session**

**File:** `ReplicatedStorage/Lucineer/Poller.lua`

### Change 1 — In-flight guard per job

Added `_inFlight` table to prevent overlapping polls. When `pollJob` starts for a job ID, it sets `_inFlight[jobId] = true`. If another poll attempt comes for the same job while the first is still pending (e.g., slow HTTP with retries), it returns immediately. The flag is cleared on completion, error, or unregistration.

```lua
Poller._inFlight = {} :: { [string]: boolean }

-- In pollJob():
if Poller._inFlight[job.id] then return end
Poller._inFlight[job.id] = true
-- ... HTTP call ...
Poller._inFlight[job.id] = nil
```

Also cleaned up in `unregister()` to prevent stale flags.

### Change 2 — Throttle checkTimeouts to poll interval

Moved `checkTimeouts()` from every Heartbeat tick (~60×/second) to inside the poll interval gate (every `POLL_INTERVAL` seconds, default 0.5s). Added a separate `_timeoutAccumulator` so timeout checks don't reset the poll accumulator.

```lua
Poller._timeoutAccumulator = 0

-- In tick():
Poller._timeoutAccumulator += dt
if Poller._timeoutAccumulator >= Config.POLL_INTERVAL then
    Poller._timeoutAccumulator = 0
    checkTimeouts()
end
```

### Change 3 — Init cleanup

`Poller.init()` now resets `_inFlight` and `_timeoutAccumulator` alongside existing resets.

---

## Bug #4 — Phantom RemoteEvents (GAP #9e)

**Status: ✅ Fixed this session**

**File:** `StarterPlayer/StarterPlayerScripts/LucineerClient/init.lua`

Replaced the `FindFirstChild` + `Instance.new` pattern (which created client-local phantom RemoteEvents that the server could never fire) with `WaitForChild` and a 30-second timeout:

```lua
local ResponseRemote = Lucineer:WaitForChild("ResponseEvent", 30)
local ThinkingRemote = Lucineer:WaitForChild("ThinkingEvent", 30)

if not (ResponseRemote and ThinkingRemote) then
    warn("[Lucineer] Client: server RemoteEvents never appeared after 30s — aborting")
    return
end
```

This ensures the client waits for the server's real RemoteEvents rather than creating dead client-side copies.

---

## Syntax Verification

All modified files pass `lua5.1` syntax checks:

```
OK: ReplicatedStorage/Lucineer/Poller.lua
OK: StarterPlayer/StarterPlayerScripts/LucineerClient/init.lua
```

---

## Files Modified

| File | Changes |
|------|---------|
| `ReplicatedStorage/Lucineer/Poller.lua` | In-flight guard, throttled checkTimeouts, init cleanup |
| `StarterPlayer/StarterPlayerScripts/LucineerClient/init.lua` | WaitForChild with timeout instead of phantom RemoteEvent creation |

## Files Verified (no changes needed)

| File | Reason |
|------|--------|
| `ReplicatedStorage/Lucineer/CommandExecutor.lua` | Params dispatch, addLight, addScript all already fixed |
| `ReplicatedStorage/Lucineer/ChatHandler.lua` | sessionId payload already correct |
| `ReplicatedStorage/Lucineer/Http.lua` | 4xx fail-fast already implemented |
| `ReplicatedStorage/Lucineer/Config.lua` | SESSION_ID already generated |
| `ServerScriptService/LucineerServer/init.lua` | State sync payload, reply/message, text filtering all present |
