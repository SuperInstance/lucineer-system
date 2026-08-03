# P0 Security Fixes — GAP #3: API Key Exposure

**Date:** 2026-08-03
**Status:** ✅ Complete
**Scope:** `lucineer-roblox/src/`, `lucineer-worker/process_v2.py`

---

## Problem

`Config.lua` in `ReplicatedStorage/Lucineer/` replicated to every connected client.
It contained `WORKER_URL` and `AUTH_KEY` — giving any player with an executor full
authenticated access to all Worker endpoints. The same key was hardcoded in 4+ files
and embedded in the distributable `.rbxlx` place file.

## Changes Made

### 1. New: `ServerConfig.lua` (ServerScriptService)
- **Path:** `src/ServerScriptService/LucineerServer/ServerConfig.lua`
- Contains `WORKER_URL` and resolves `AUTH_KEY` at runtime from
  `ServerStorage:WaitForChild("LucineerSecret")` (a `StringValue` set in Studio)
- Falls back to empty key with a warning if secret is missing
- Studio-safe: prints a warning but doesn't crash in Studio mode

### 2. Updated: `Config.lua` (ReplicatedStorage)
- Removed `WORKER_URL` and `AUTH_KEY` entirely
- Now contains only client-safe presentation values: UI colors, bot name, poll
  intervals, session ID, retry/backoff config, scan parameters
- Header comment explicitly warns against putting secrets here

### 3. Updated: `Http.lua` (ReplicatedStorage)
- No longer reads `Config.WORKER_URL` or `Config.AUTH_KEY`
- New `Http.configure(workerUrl, authKey)` function — called once at server init
- Credentials stored in upvalues (not accessible from client-side code)
- All `Http.get()`/`Http.post()` calls fail safely if `configure()` was never called
- Uses `Config.HTTP_*` retry/backoff values (which are client-safe)

### 4. Updated: `LucineerServer/init.lua`
- Requires `ServerConfig` from `script:WaitForChild("ServerConfig")` before loading
  any shared modules
- Calls `Http.configure(ServerConfig.WORKER_URL, ServerConfig.AUTH_KEY)` immediately
  after requiring Http — before any HTTP traffic can occur
- Updated the startup log line to reference `ServerConfig.WORKER_URL`

### 5. Updated: `default.project.json`
- `LucineerServer` changed from a single Script to a Folder containing:
  - `init.lua` (Script — the bootstrap)
  - `ServerConfig.lua` (ModuleScript — server-only secrets)
- This ensures Rojo correctly maps both files

### 6. Updated: `process_v2.py`
- Changed from `AUTH_KEY = "AUTH_KEY_PLACEHOLDER"` (hardcoded)
  to `AUTH_KEY = os.environ.get("LUCINEER_KEY", "")` (environment variable)
- Prints a warning if `LUCINEER_KEY` is not set
- No hardcoded fallback value

### 7. New: `SECURITY.md`
- Full documentation of the fix, key rotation procedure, Studio setup instructions,
  environment variable reference, and recommended future improvements (per-server tokens)

## Verification

- **Lua syntax:** All `.lua` files pass bracket/paren balance checks. lua5.1 errors
  are expected for Luau type annotations (Roblox uses Luau, not Lua 5.1).
- **Python syntax:** `python3 -m py_compile process_v2.py` — ✅ passes
- **JSON validity:** `default.project.json` — ✅ valid JSON
- **Dependency chain:** ServerConfig → Http.configure() → ChatHandler/Poller use Http →
  all HTTP calls go through the configured credentials

## What Still Needs Doing (Out of Scope)

1. **Rotate the actual key.** The old placeholder key is in git history. Generate a new
   one, set it in Cloudflare Worker secrets, Studio ServerStorage, and the `LUCINEER_KEY`
   env var on the processor host.
2. **Squash git history** to purge the old key (use BFG Repo Cleaner or git filter-repo)
3. **Rebuild the `.rbxlx`** via `rojo build` so the old embedded key is gone
4. **Add auth to the memory and vectorize Workers** (GAP #4 notes they have zero auth)
5. **Consider per-server tokens** instead of a shared static key (documented in SECURITY.md)
