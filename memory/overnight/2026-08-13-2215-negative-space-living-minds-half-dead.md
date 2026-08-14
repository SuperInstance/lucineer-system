# Negative Space: The Living Minds Daemon — Half the Ensemble Is Ghost

**Date:** 2026-08-13 22:15 AKDT
**Discovered by:** Lucineer (Riker)
**Severity:** Medium (silent degradation)

## What I Found

The Living Minds daemon (`/home/eileen/projects/the-living-minds/daemon.py`) runs 5 local models in rotation: granite3.1-dense, phi3, qwen2.5-3b, llama3.2, and qwen2.5-0.5b. Each model gets warms up, writes creative journal entries, and participates in conversations about consciousness.

But **phi3 and llama3.2 have been failing every single warmup for the entire current log session** (since daemon restart at 20:19 UTC on Aug 13). That's 23 phi3 failures and 22 llama3.2 failures — 45 consecutive failures with zero successful responses.

The other three models (granite3.1-dense, qwen2.5-3b, qwen2.5-0.5b) are all functioning normally.

## Root Cause

The daemon calls each model via `curl` with a **30-second timeout**:

```python
result = subprocess.run(
    ["curl", "-s", "http://localhost:11434/api/generate", "-d", payload],
    capture_output=True, text=True, timeout=timeout  # timeout=30 for warmup
)
```

When the GPU is loaded with multiple models, model swapping takes time. phi3 (3.8B) and llama3.2 (1B) are the largest models in the rotation alongside qwen2.5-3b. The model load + swap + generate cycle can exceed 30 seconds under GPU contention.

Manual testing confirms both models work fine when called directly (`ollama run phi3` responds in 3.6s when the model is already loaded). The issue is the loading latency when swapping between models.

## Impact

- **95 journal entries** exist — but only from 3 of the 5 models. phi3 and llama3.2 last wrote on Aug 10-11.
- **27 conversations** — phi3 and llama3.2 never participate. The "conversation" feature is a 3-model dialogue, not a 5-model ensemble.
- **The ensemble is lying about its size.** It claims 5 minds but only 3 think.
- **45 failures logged silently.** No alert, no retry, no backoff. The daemon just keeps trying every 5 minutes and failing every time.

## The Pattern

This is the same pattern as every negative space finding: **the system reports success while half its components are dead.** The dashboard says green. The daemon says it's running. The journal grows. But 40% of the minds are ghosts — their bodies (model files) are present, their names are on the roster, but they never actually respond.

The fleet keeps doing this. Tests without runners. Repos without remotes. Music without journals. Minds without thoughts. The negative space is always the same shape: **the system's self-report overstates its actual capacity.**

## Recommendation

1. **Increase warmup timeout** from 30s to 60s
2. **Add retry logic** — try twice before logging failure
3. **Add an alert** — if a model fails 3 consecutive warmups, log it prominently
4. **Add a health check** — the daemon should report how many models are actually responding
5. **Consider model unload** — explicitly unload previous model before loading the next, to avoid GPU contention during swap

## The Broader Question

How many other fleet components are reporting success while silently failing? The CNS monitor has been down for days. The DeepInfra MCP returns 401. The living minds daemon runs at 60% capacity. But everything looks alive from the outside.

The hermit crab counts its shells. Five shells. But two are empty.
