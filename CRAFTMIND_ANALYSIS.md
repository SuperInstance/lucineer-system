# Craftmind Agents — Study & Integration Analysis

**Source:** `github.com/SuperInstance/roblox-craftmind-agents` (by Casey's son)
**Date:** 2026-08-03

---

## What Craftmind Does Well

### 1. 🧠 Self-Improving Task Loop (ADOPT)
The core loop is excellent: `fetch plan → simulate → refine → execute → feed results back to vector index`. This is the same pattern as our Chisel grain system, but **actually implemented in Lua**, not just designed in docs.

**Key difference from Slackwater:** Craftmind stores refined plans back to the vector index automatically after each execution. Our system has the Vectorize index but never writes back. We should adopt this.

### 2. 💰 Token Budget System (ADOPT)
Each agent has a `tokenBudget` and the framework auto-caps/trims steps to stay within budget. This is smart — it prevents runaway costs.

**Integration:** Add token budgeting to our brain pipeline. The processor should track cumulative tokens per session and degrade gracefully (switch from deep to fast mode when budget is low).

### 3. 🎤 Foreman STT/TTS (STUDY)
Voice-controlled agent interaction using `SpeechService`. This is a native Roblox API for speech-to-text and text-to-speech that we haven't explored.

**Caveat:** The implementation references `SpeechService:StartListeningAsync` which may not exist in current Roblox API. Needs verification. But the concept of voice-driven building is compelling for immersion.

### 4. 🎨 On-the-Fly Asset Generation (STUDY)
Calls a local GPU service to generate custom skins/sounds/meshes. The RTX 4050 integration concept maps to our plato-forge-daemon day/night training cycle.

**Caveat:** The implementation is stubbed (`rbxassetid://123456789` fallbacks). But the architecture — call GPU service, cache result in ReplicatedStorage, use across agents — is sound.

### 5. 🧪 Headless Test Harness (ADOPT)
The `docker-compose.yml` references `robloxcommunity/rbxtestserver:latest` — a headless Roblox test server. The setup script downloads Studio Mod Manager binaries for headless testing.

**This is huge for our playtest harness.** If a headless Roblox test server image exists, we can run automated playtests in Docker without Studio.

### 6. 📡 Fleet Vector Index Write-Back (ADOPT)
After each task execution, results are POSTed to `/ingest` on the vector index. This creates a growing library of refined plans that future agents can search.

**Integration:** Our Vectorize worker should have a `/api/skills/ingest` endpoint that accepts refined build plans. The processor should write back after each successful build.

---

## What Craftmind Does Poorly (Avoid)

### 1. No Real Error Handling
Every `pcall` silently swallows errors. No logging, no retry, no circuit breaker. If the GPU service is down, the agent just uses fallback assets forever with no warning.

### 2. Token Budget is Fake
The "token cost" is a number assigned to steps (`step.tokenCost or 10`). It's not connected to actual API token usage. The trimming just removes steps from the end of the list.

### 3. GPU Simulation is a Black Box
`_runPreSimulation` POSTs to a service and gets back `{successRate: 0.92}`. The simulation is never described. It's a placeholder.

### 4. Voice API May Not Exist
`SpeechService:StartListeningAsync` and `:SynthesizeTextAsync` need verification against current Roblox API. These look like aspirational APIs.

---

## Actionable Integrations for Slackwater

| # | Feature | Source | Effort | Priority |
|---|---------|--------|--------|----------|
| 1 | **Vector write-back after builds** | Craftmind `_updateVectorIndex` | 2h | P0 — closes the learning loop |
| 2 | **Token budget tracking** | Craftmind `tokenBudget` | 3h | P1 — cost control |
| 3 | **Headless Docker test server** | Craftmind `docker-compose.yml` | 4h | P1 — automated playtests |
| 4 | **Task plan caching** | Craftmind `taskCache` with TTL | 2h | P1 — performance |
| 5 | **Voice control investigation** | Craftmind STT/TTS | 2h | P2 — research |
| 6 | **GPU asset generation pipeline** | Craftmind `_generateOnTheFlyAssets` | 8h | P3 — future |

---

## Technical Notes

- The `robloxcommunity/rbxtestserver:latest` Docker image needs verification — may not be publicly available
- The Studio Mod Manager download URL (`MaximumADHD/Roblox-Studio-Mod-Manager`) is a known tool for headless Studio
- The setup script references `/home/phoenix/` — this was built on Casey's son's machine
- The Lua uses `+=` operator (Luau, not Lua 5.1) — consistent with our codebase
