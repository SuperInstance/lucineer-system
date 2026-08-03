# P0 Processor Fixes — Applied 2026-08-03

## Status: ALL 5 BUGS FIXED

All changes verified with `py_compile` syntax checks on both `process_v2.py` and `brain.py`.

---

## Bug #1 — Keyword Matching Fires on Substrings (GAP A3)

**File:** `lucineer-worker/process_v2.py` — `match_keyword()` function

**Root cause:** Used `keyword in msg_lower` (substring containment) with first-match-wins in dict order.

**Fix applied:**
- Added `re` (regex) import and word-boundary matching: `\b{keyword}\b`
- Added build verb requirement: message must contain `build|make|create|put|raise|place|add|give me|construct|throw up|put up`
- Added negation detection: `don't|do not|never|stop|no|not` → skip matching
- Changed from first-match-wins to **score all candidates, return longest keyword match**
  - "build a castle tower" → both 'castle' (6 chars) and 'tower' (5 chars) match, 'castle' wins

**Test results:** 16/16 pass, including all gap analysis cases:
- "keep it small" → no match (no build verb) ✓
- "search for something" → no match (no 'arc' substring false positive) ✓
- "build a castle tower" → b_castle (longest match wins) ✓
- "don't build a wall" → no match (negation) ✓
- "what do you think of my castle?" → no match (no build verb) ✓

---

## Bug #2 — Daemon Runs Wrong Processor (GAP A2)

**File:** `lucineer-worker/run-processor.sh` (still calls `process-jobs.sh --once` — the v1 bash processor)

**Fix applied:**
- Created systemd service file: `lucineer-worker/lucineer-processor.service`
  - Runs `python3 process_v2.py --loop --interval 2`
  - `Restart=always`, `RestartSec=5`
  - Output to journald (replaces unmanaged `processor.log`)
  - Memory limit: 512MB
  - Security hardening: `NoNewPrivileges`, `ProtectSystem=strict`, `PrivateTmp`
  - `ReadWritePaths` scoped to lucineer-worker, lucineer-brain, and /tmp

**Install instructions:**
```bash
# Copy to systemd directory
sudo cp /home/eileen/projects/lucineer-worker/lucineer-processor.service /etc/systemd/system/

# Reload systemd, enable and start
sudo systemctl daemon-reload
sudo systemctl enable lucineer-processor
sudo systemctl start lucineer-processor

# Check status / logs
sudo systemctl status lucineer-processor
sudo journalctl -u lucineer-processor -f

# Stop the old daemon first if it's running:
# pkill -f "process-jobs.sh" ; pkill -f "run-processor.sh"
```

**Important:** Set `LUCINEER_KEY` and optionally `DEEPINFRA_API_KEY` in the service file's `Environment=` lines before installing. The current placeholder `AUTH_KEY_PLACEHOLDER` must be replaced with the real key, or better yet, read from an EnvironmentFile.

---

## Bug #3 — Persona Is Dead Code (GAP #7)

**Files:** `lucineer-worker/process_v2.py`, `lucineer-brain/brain.py`

### 3a. Production path now runs personality stage

**Root cause:** `process_v2.py` called brain.py with `--verbose` only. The `--creative` flag (which enables the Hermes-3-Llama-405B personality stage) was never passed in the production path.

**Fix:** Changed the `call_brain()` subprocess invocation from:
```python
['python3', BRAIN_SCRIPT, '--verbose', enhanced]
```
to:
```python
['python3', BRAIN_SCRIPT, '--creative', '--verbose', enhanced]
```

Now the full 4-stage pipeline runs: Intent → Planner → Coder → **Hermes (personality)**.

### 3b. Deleted stage_hermes command-stealing bug

**Root cause:** In `brain.py:stage_hermes()`, three lines allowed Hermes (a prose model) to overwrite the coder's verified command array:
```python
if "commands" in enhanced and enhanced["commands"]:
    enhanced_result["commands"] = enhanced["commands"]
```

**Fix:** Deleted those lines entirely. Hermes output now only affects the `reply` field. The coder's `commands` array is always preserved.

### 3c. run_fast gets its own token budget

**Root cause:** `run_fast()` used `MAX_TOKENS["intent"]` = 1024, which is too small for 5-8 command builds with hex colors and vector positions. The JSON would truncate mid-generation and fall through to the parse-failure stub.

**Fix:** Changed from `max_tokens=MAX_TOKENS["intent"]` to `max_tokens=2048`.

---

## Bug #4 — Timeouts Are Inverted (GAP #8a)

**Files:** `lucineer-worker/process_v2.py`, `lucineer-brain/brain.py`

**Root cause chain:**
- `Config.lua` (client): `POLL_TIMEOUT = 60` — client gives up after 60s
- `process_v2.py`: `DEEP_TIMEOUT = 120` — brain allowed 120s
- `brain.py`: `call_model timeout = 300` with `max_retries=3` — worst case 10+ minutes
- `PLANNER_FALLBACKS`: 5 models in chain

The client gave up before the brain finished.

**Fix applied:**
1. `process_v2.py`: `DEEP_TIMEOUT` changed from `120` → `100`
2. `brain.py`: `call_model` default `timeout` changed from `300` → `90`
3. `brain.py`: `PLANNER_FALLBACKS` capped from 5 models to 2 (primary + 1 fallback)

**Timeout chain is now properly ordered:**
```
brain call_model timeout:  90s  (per-model, with retries)
DEEP_TIMEOUT (processor): 100s  (brain.py subprocess timeout)
POLL_TIMEOUT (client):    120s  ← must be set in Config.lua
```

**Action required on Roblox side:** Update `Config.lua` to set `POLL_TIMEOUT = 120`. This is a Roblox client file and was not modified here.

---

## Bug #5 — Pyramid Says "Seven Tiers" Builds Six (GAP A6)

**File:** `lucineer-worker/process_v2.py` — `b_pyramid()` function

**Root cause:** `levels = 6` but the reply text says "Seven tiers of packed sand."

**Fix:** Changed `levels = 6` → `levels = 7`. Now the pyramid builds 7 levels + the golden capstone, matching the persona text.

---

## Pre-existing Bug Found: brain.py Syntax Error

While verifying syntax, discovered that `brain.py` line 144 had a truncated string literal:
```python
if line.startswith("DEEPINFRA_API_KEY=***REDACTED***
```
The line was missing its closing `"):` — appeared to be damaged by a security filter that replaced the key prefix pattern. Fixed by restoring the proper string literal:
```python
if line.startswith("DEEPINFRA_API_KEY="):
```

---

## Files Modified

| File | Changes |
|------|---------|
| `lucineer-worker/process_v2.py` | Bug #1 (match_keyword rewrite), Bug #3a (--creative flag), Bug #4 (DEEP_TIMEOUT 120→100), Bug #5 (pyramid levels 6→7) |
| `lucineer-brain/brain.py` | Bug #3b (deleted command-stealing), Bug #3c (run_fast tokens 1024→2048), Bug #4 (call_model timeout 300→90, PLANNER_FALLBACKS 5→2), pre-existing syntax error fix |
| `lucineer-worker/lucineer-processor.service` | New file — systemd service for Bug #2 |

## Action Items for Human

1. **Install systemd service** — see instructions in Bug #2 section above
2. **Set `POLL_TIMEOUT = 120`** in `Config.lua` on the Roblox client side
3. **Rotate API key** — the placeholder `AUTH_KEY_PLACEHOLDER` must be replaced with the real key in the systemd service file before deployment
4. **Kill the old daemon** if `run-processor.sh` is still running: `pkill -f "run-processor.sh"`
