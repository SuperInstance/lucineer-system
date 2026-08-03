# GAP #8 — Game Feel Fixes

**Date:** 2026-08-03
**Scope:** Eliminate sixty seconds of dead air and make builds feel alive.
**Status:** ✅ All four fixes implemented.

---

## Summary

The player experience had a critical game feel problem: after typing a build request, the player would stare at an unchanging "Lucineer is thinking..." dot for up to sixty seconds with no feedback, then hit a timeout indistinguishable from a crash. These fixes address that across four dimensions.

---

## Fix 1: Staggered Build Placement in `executeBatch`

**File:** `ReplicatedStorage/Lucineer/CommandExecutor.lua`

**What changed:**
- `executeBatch` now accepts an optional `onProgress(current, total, result)` callback parameter.
- Every 3 commands, `task.wait(0.08)` fires during execution — parts land progressively instead of materializing in a single frame.
- The wait is skipped on the last iteration (`i < #commands`) to avoid a trailing delay.
- `onProgress` is called via `task.spawn` so it can't block the build loop (e.g., firing RemoteEvents to update UI).

**Why it matters:** Parts landing one-at-a-time reads as *construction*. All-at-once reads as texture pop-in. The 0.08s stagger every 3 parts is subtle enough to feel natural while giving the BuildAnimator cinematic reveal a sense of sequential work order.

---

## Fix 2: Progressive Thinking Messages

**Files:**
- `ReplicatedStorage/Lucineer/ChatHandler.lua` — pending-phase rotation
- `ServerScriptService/LucineerServer/init.lua` — build-phase rotation

**What changed — Pending Phase (ChatHandler):**
- Added `_pendingThinking` tracking table (per-player boolean flags).
- After showing the initial "Lucineer is thinking..." message, a background task rotates through 4 thinking messages every 5 seconds:
  - `"Looking at the ground..."`
  - `"Checking what's already here..."`
  - `"Working on it..."`
  - `"Almost there..."`
- Rotation stops when:
  - The job completes successfully (success callback clears flag)
  - The job errors (error callback clears flag)
  - POST `/api/message` fails (cleared immediately)
  - Immediate response with no jobId (cleared immediately)
  - Player leaves (cleared in `PlayerRemoving`)

**What changed — Build Phase (Server init.lua):**
- The existing `startThinkingRotation`/`stopThinkingRotation` system now has a correct loop guard: `thinkingRotations[player] == coroutine.running()` instead of always-truthy check.
- `stopThinkingRotation(player)` is now called at the end of `handleResponse` (after build completes) to properly cancel the build-phase rotation thread.
- The `onProgress` callback from `executeBatch` fires `"Placing piece N of M..."` updates to the client during the build.

**Why it matters:** Forty seconds of an unchanging pulsing dot feels broken. Five-second rotating messages feel like Lucineer is actively working — narrating while building, which is core to his character.

---

## Fix 3: Contextual Completion Messages

**File:** `ServerScriptService/LucineerServer/init.lua`

**What changed:**
- After command execution completes, if the Worker didn't already provide a `reply` or `message`, the server sends a count-aware completion message:
  - `"There. %d pieces placed."`
  - `"Built — %d parts fitted and set."`
  - `"That's %d pieces. Not bad."`
- Selected randomly via `math.random(#messages)`, formatted with the actual command count.
- Passes through `filterFor()` for Roblox text-filter compliance.

**Why it matters:** `"Done! I built 8 action(s) for you."` was generic assistant voice. Count-aware messages in Lucineer's foreman tone feel like a character who knows what he just built.

---

## Fix 4: Timeout Chain Verification

**File:** `ReplicatedStorage/Lucineer/Config.lua`

**What changed:**
- `POLL_TIMEOUT`: 180 → **120 seconds**
- Updated comment to reference `DEEP_TIMEOUT` (100s) — `POLL_TIMEOUT` must exceed it.

**Timeout chain (correct order):**
1. Brain model calls: `timeout=300` with retries (but planner capped at 2 models, not 5 — separate fix)
2. `DEEP_TIMEOUT` (process_v2.py): 100s — the processor gives up on the brain
3. `POLL_TIMEOUT` (Config.lua): 120s — the client gives up on the processor

The client waits 20 seconds longer than the processor, so even a slow deep build that finishes at t=99s gets delivered before the client times out at t=120s.

---

## Files Modified

| File | Changes |
|------|--------|
| `ReplicatedStorage/Lucineer/CommandExecutor.lua` | `executeBatch` gets `onProgress` callback + staggered `task.wait(0.08)` every 3 parts |
| `ReplicatedStorage/Lucineer/ChatHandler.lua` | Progressive thinking rotation during pending phase + `_pendingThinking` tracking |
| `ReplicatedStorage/Lucineer/Config.lua` | `POLL_TIMEOUT` 180 → 120 |
| `ServerScriptService/LucineerServer/init.lua` | Build-phase `onProgress` wiring, count-aware completion messages, rotation thread cleanup fix |

---

## What This Fixes (from GAP_ANALYSIS.md #8)

- ✅ **8a** (inverted timeouts): `POLL_TIMEOUT` (120s) now exceeds `DEEP_TIMEOUT` (100s)
- ✅ **8b** (no progressive feedback): Two-phase thinking rotation (pending + build) + staggered placement + progress callbacks
- Partially **8c** (no caching): Not addressed in this pass — caching identical requests is a separate optimization

## What This Does NOT Fix

- **8c (caching):** Hash-based command caching for identical requests. This is an optimization, not a game-feel fix.
- **Brain-side ack messages:** The `process_v2.py` ACK system (`api_post("/api/job/{id}/progress", ...)`) is documented in the gap analysis but not implemented here — it requires Worker endpoint changes. The client-side thinking rotation covers the same user-facing gap.
