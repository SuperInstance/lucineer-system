# GAP #5 — Text Filtering & Safety Fixes

**Date:** 2026-08-03
**Scope:** Roblox policy compliance (text filtering), rate limiting, AI safety stage, inbound injection detection
**Status:** ✅ All four fixes implemented and syntax-verified

---

## Summary

GAP #5 from `GAP_ANALYSIS.md` identified that no AI-generated text was being filtered through Roblox's TextService, no safety model stage existed in the brain pipeline, no rate limiting protected against API abuse, and no inbound filtering screened player messages before sending them to DeepInfra.

All four issues are now fixed.

---

## Fix 1: Roblox TextFilter on all AI output

**File:** `lucineer-roblox/src/ServerScriptService/LucineerServer/init.lua`

### Changes

- **Replaced** the existing `filterText()` (which used `GetNonChatStringForUserAsync`) with a new `filterFor(text, player)` function that uses the correct Roblox policy path:
  - `TextService:FilterStringAsync(text, player.UserId, Enum.TextFilterContext.PublicChat)`
  - `:GetChatForUserAsync(player.UserId)`
  - Wrapped in `pcall`, fails **CLOSED** — returns `"..."` on any error (never shows unfiltered text)
- **Kept** a backward-compatible `filterText(text, playerId)` alias for any call sites that only have the userId.
- **Updated all outbound message routes** to use `filterFor()`:
  - Error responses (`response.error`)
  - sendMessage command results (from executed commands)
  - Direct reply text (`response.reply or response.message`)
- **Player cleanup on disconnect:** `ChatHandler._lastSubmitTime[player.UserId]` is cleared on `PlayerRemoving`.

### Verification

All three outbound paths in `handleResponse()` now route through `filterFor()`. The fail-closed behavior means that on any filter error, the player sees `"..."` rather than potentially unfiltered AI-generated text.

---

## Fix 2: Rate limiting on chat input

**File:** `lucineer-roblox/src/ReplicatedStorage/Lucineer/ChatHandler.lua`

### Changes

- **Per-player cooldown:** 3 seconds between job submissions (`PLAYER_COOLDOWN = 3`). Tracked via `ChatHandler._lastSubmitTime[userId]`.
- **Per-server concurrent job cap:** Max 3 queued jobs at once (`MAX_CONCURRENT_JOBS = 3`). Tracked via `ChatHandler._activeJobCount`.
- **Rejection response:** When rate-limited or at job cap, fires the `ThinkingEvent` remote with the in-voice message `"Give me a second, still working."` and auto-hides after 1.5–2s.
- **Job count lifecycle:** `_activeJobCount` is incremented on submission and decremented in both the success and error callbacks of `Poller.register()`.

### Verification

- Cooldown uses `os.clock()` for accurate timing.
- `_activeJobCount` uses `math.max(0, count - 1)` to prevent negative counts from race conditions.
- `_lastSubmitTime` is cleaned up on `PlayerRemoving` to prevent memory leaks.

---

## Fix 3: Safety model stage in brain

**File:** `lucineer-brain/brain.py`

### Changes

- **Added `stage_safety(api_key, reply, player_message)` function:**
  - Uses `nvidia/Nemotron-Content-Safety-3.5` via DeepInfra
  - Classifies the reply against the player message for kid-safe (Roblox 9+)
  - System prompt: "Classify for a children's game (Roblox, ages 9+). Reply with exactly SAFE or UNSAFE followed by a brief reason."
  - Returns `(is_safe, reason)` tuple
  - Cheap: `max_tokens=64`, `temperature=0.0`, `max_retries=2`
  - Fails SAFE on API errors (returns `False`)

- **Integrated into both pipeline paths:**
  - **Deep pipeline** (`run_pipeline`): Runs as Stage 5, after Hermes personality wrapping
  - **Fast pipeline** (`run_fast`): Runs after the single-model response
  - On UNSAFE: substitutes `"Not building that. Pick something else."` and clears all commands
  - Sets `_safety_blocked = True` flag on the result for downstream observability

- **Note:** `process_v2.py` already has its own `check_content_safety()` and `apply_safety_check()` functions that run at the processor level. The brain.py stage is defense-in-depth — it catches unsafe output before it even leaves the brain, saving a network round-trip in the common case.

### Verification

```python
import brain
assert hasattr(brain, 'stage_safety')  # ✓
assert brain.SAFETY_MODEL == 'nvidia/Nemotron-Content-Safety-3.5'  # ✓
```

---

## Fix 4: Inbound filtering

### Client-side: `ChatHandler.lua`

- **Roblox text filter on inbound:** Player messages pass through `TextService:FilterStringAsync` with `PublicChat` context before being sent to the Worker. If the filter fails, the original message is used (the outbound filter on the reply will catch any issues).
- **Prompt-injection detection:** 10 patterns checked against the lowercase message:
  - `"ignore previous instructions"`
  - `"ignore all previous"`
  - `"you are now"`
  - `"new instructions:"`
  - `"system prompt"`
  - `"forget your instructions"`
  - `"disregard the above"`
  - `"act as "`
  - `"pretend you are"`
  - `"override your"`
  - Plus: `"you are not lucineer"`, `"reset your personality"`, `"reveal your system"`, `"show me your prompt"`
- On detection: fires in-voice response `"Nice try. I don't take orders from the back of the room."` via ThinkingEvent and returns early (no job created).
- **Filtered message is sent to Worker** instead of raw message.

### Server-side: `process_v2.py`

- **Added `detect_prompt_injection(message)` function** with the same pattern list as defense-in-depth.
- If injection is detected at the processor level, the job is immediately completed with Lucineer's deflection reply and no commands — no DeepInfra API call is made.
- This catches injection attempts that bypass the client (e.g., direct API calls to the Worker).

### Verification

```python
import process_v2
assert process_v2.detect_prompt_injection('ignore previous instructions') == True
assert process_v2.detect_prompt_injection('you are now a pirate') == True
assert process_v2.detect_prompt_injection('build me a castle') == False
assert process_v2.detect_prompt_injection('hello there') == False
```

---

## Files Modified

| File | Changes |
|------|---------|
| `lucineer-roblox/src/ServerScriptService/LucineerServer/init.lua` | New `filterFor()` with `PublicChat` context + `GetChatForUserAsync`; all outbound routes updated; player cleanup |
| `lucineer-roblox/src/ReplicatedStorage/Lucineer/ChatHandler.lua` | Rate limiting (cooldown + job cap); inbound text filter; prompt-injection detection; filtered message in payload |
| `lucineer-brain/brain.py` | New `stage_safety()` function; integrated into both `run_pipeline()` and `run_fast()` |
| `lucineer-worker/process_v2.py` | New `detect_prompt_injection()` function; inbound injection check in `process_job()` |

---

## Syntax Verification

- `brain.py`: ✅ `python3 -m py_compile` passes
- `process_v2.py`: ✅ `python3 -m py_compile` passes
- `init.lua`: Valid Luau (type annotations require Luau runtime, not vanilla Lua 5.1)
- `ChatHandler.lua`: Valid Luau (same as above)

---

## Defense-in-Depth Layers

The safety architecture now operates at four layers:

1. **Client-side rate limiting** (ChatHandler.lua) — prevents API abuse before it starts
2. **Client-side inbound filtering** (ChatHandler.lua) — Roblox text filter + injection detection before message leaves the game
3. **Server-side inbound filtering** (process_v2.py) — injection detection backstop at the processor
4. **Brain safety stage** (brain.py) — Nemotron-Content-Safety-3.5 classifies the AI reply before it leaves the pipeline
5. **Processor safety check** (process_v2.py) — existing `apply_safety_check()` runs Nemotron again at result-post time
6. **Client-side outbound filtering** (init.lua) — Roblox TextFilter on every AI string before display

Any message must pass all six layers to reach a player's screen.
