# Automated Playtesting Research — Lucineer System

**Date:** 2026-08-03  
**Author:** Research Engineering Subagent  
**Purpose:** Evaluate all viable approaches for AI-driven automated playtesting of Roblox games with experience journaling for ML training data.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Landscape Analysis](#landscape-analysis)
   - [1. Roblox Automated Testing Frameworks](#1-roblox-automated-testing-frameworks)
   - [2. AI Playtesting in the Industry](#2-ai-playtesting-in-the-industry)
   - [3. Headless Roblox](#3-headless-roblox)
   - [4. Roblox HTTP APIs](#4-roblox-http-apis)
   - [5. Browser Automation](#5-browser-automation)
   - [6. Bot Frameworks](#6-bot-frameworks)
   - [7. Journaling & Training Data](#7-journaling--training-data)
   - [8. Multi-Agent Simulation](#8-multi-agent-simulation)
3. [Ranked Recommendations](#ranked-recommendations)
4. [Architecture Sketches (Top 3)](#architecture-sketches-top-3)
5. [Code Snippets for Recommended Approach](#code-snippets-for-recommended-approach)
6. [Build TODAY vs Needs More Research](#build-today-vs-needs-more-research)

---

## Executive Summary

**The winning architecture is a three-layer stack:**

1. **In-game Luau journaling agent** — a script injected into the Roblox place that captures game state, player actions, and "train-of-thought" snapshots, posting them via HttpService to our Worker API.
2. **Studio CLI test runner** — Roblox Studio launched headlessly via `--task RunScript --quitAfterExecution` to orchestrate automated playtest sessions on a schedule.
3. **Worker API journal aggregator** — our existing Cloudflare Worker receives telemetry streams, structures them into training episodes, and stores in R2/KV for later ML use.

This approach wins because it's **free**, uses **official Roblox APIs**, produces **high-quality structured data**, and integrates with our existing Worker infrastructure with minimal effort.

---

## Landscape Analysis

### 1. Roblox Automated Testing Frameworks

#### TestService (Legacy)
- Built-in Roblox service for running automated tests
- Can emulate multiple players (`Players:setSimulatePlayersCount(n)`)
- Limited developer-facing API; primarily used internally by Roblox
- Works but feels dated and restricted

#### StudioTestService (Dec 2025) — ⭐ KEY FINDING
- **New official framework** for programmatic test automation
- Launches tests, executes play/run modes asynchronously
- Retrieves test arguments and concludes test sessions programmatically
- Supports multiplayer testing with up to **8 simulated clients**
- Can add players mid-session and trigger client disconnects
- This is Roblox's answer to CI-driven automated playtesting

#### Studio Testing APIs (May 2026) — ⭐ CRITICAL
- **`StudioDeviceSimulatorService`** — scriptable device simulation (resolution, DPI, orientation, custom devices)
- **`VirtualInput`** — simulates mouse, keyboard, and pointer events identical to real hardware input
- **`GuiButton:Activate()`** — programmatic UI button clicks for automated UI flows
- Combined, these let you script complete playtest sequences with no human input

#### TestEZ
- BDD-style testing framework, used by Roblox internally
- Good for unit/integration tests of game logic modules
- Not designed for full playthrough simulation

#### Lunit / Specium
- Newer frameworks (2026) for roblox-ts / Luau
- Lunit supports running tests via **Lune** (standalone Luau runtime) for CI
- Specium is dependency-free, lightweight
- Both are unit-test focused, not playtest focused

#### Rojo + CI/CD
- File sync tool enabling external editors + git workflows
- Can build `.rbxlx` place files in CI pipelines
- Pairs with TestEZ for headless unit testing
- Complex setup but mature ecosystem

#### Studio CLI — ⭐ KEY DISCOVERY
Roblox Studio supports command-line arguments that enable **fully scriptable test execution**:

```bash
# Run a script in a specific game and exit when done
RobloxStudio.exe --task RunScript \
  --placeId 74265016723074 \
  --universeId 7127583708 \
  --runScriptFile smokeTest.luau \
  --outputFile out.log \
  --quitAfterExecution
```

This is the closest thing to headless Roblox test execution. Studio opens, loads the place, runs your script (which can use StudioTestService + VirtualInput), writes output, and exits.

**Evaluation:**
| Metric | Score |
|--------|-------|
| Feasibility | ✅ Fully feasible — official API |
| Cost | Free |
| Quality | High — real Roblox engine, real physics |
| Integration effort | Low — our Luau scripts + HttpService → Worker |
| Journaling | Excellent — full game state access via script |

---

### 2. AI Playtesting in the Industry

#### EA / SEED — Most Mature
EA's SEED research group has the most published work on ML-based game testing:

- **Reinforcement Learning (RL) agents** for Battlefield V and Dead Space (2023)
- **Imitation Learning (IL)** — trains agents from human gameplay recordings; 20 min training vs 5 hours for RL
- **CCPT (Curiosity-Conditioned Proximal Trajectories)** — explores near demonstrated paths to find bugs
- **MultiGAIL** — trains agents with multiple "personas" (careful, reckless, etc.) in a single model
- Battlefield V case study: 601 features → ~500K manual testing hours (~300 work years)
- SEED's key lesson: **IL beats RL for practical game testing** — faster training, easier for devs, no ML expertise needed

#### Ubisoft
- **"Teammates"** — generative AI companions responding to voice commands (R&D prototype)
- **"Client Bots"** for The Division — AI that mimicked human input for mission playthroughs
- Focus on bug reproduction + performance data collection

#### Academic Research
- Agent-based approaches using intelligent agents that reason about game environments
- Computer vision methods interpreting visual feedback from game frames
- Hybrid workflows combining automated detection with human validation
- Key paper: [arxiv.org/abs/2202.12777](https://arxiv.org/abs/2202.12777) — automated game testing using agent-based approaches

#### Google Research
- Published on "quickly training game-playing agents with ML"
- Game telemetry as ML training data is well-established
- Google's approach: use telemetry data directly as training input

**Key Insight for Lucineer:** EA's IL approach is the most applicable — we record human playtest sessions (via our in-game journaling), then train imitation learning models on that data.

---

### 3. Headless Roblox

#### Official Headless Server: Does Not Exist
Roblox does not offer a headless server binary. The game engine requires a client (GUI) to run.

#### Workarounds:

| Approach | How It Works | Pros | Cons |
|----------|-------------|------|------|
| **Studio CLI `--task RunScript`** | Opens Studio, runs script, exits | Official, scriptable, real engine | Still opens a window (not truly headless); requires Windows/macOS |
| **rbxsilent** (GitHub) | Patches Roblox client to disable rendering | Low resource usage, real networking | Uses exploits/patches — TOS risk; Windows only; unstable |
| **Cloud GPU** (now.gg style) | Remote desktop with full Roblox client | No local resources needed | Expensive, high latency, not scriptable |
| **VIP Private Server** | Roblox-hosted private game instance | Free/cheap, official | No programmatic control; still need a client to interact |

**Best Option:** Studio CLI with `--quitAfterExecution` on a cheap Windows VPS or local machine. It's official, scriptable, and produces real engine output. Not truly headless, but can run minimized.

---

### 4. Roblox HTTP APIs

#### Open Cloud Messaging Service API — ⭐ CRITICAL
REST API for publishing messages to live game servers from external services:

```bash
curl -L -X POST \
  'https://apis.roblox.com/cloud/v2/universes/{universe}:publishMessage' \
  -H 'x-api-key: {api-key}' \
  -H 'Content-Type: application/json' \
  --data '{"topic": "autoplay-command", "message": "{\"action\":\"move\",\"x\":10,\"y\":5}"}'
```

**Rate Limits:**
- 600 + 240 × (players per server) messages sent/min per server
- 1,024 bytes max per message
- 80-char topic names

#### HttpService (In-Game → External)
- Game servers can POST to external endpoints (our Worker API)
- Must be enabled in Experience Settings
- 500 HTTP requests/min per server (+ 2500 Open Cloud requests/min separately)
- Supports HTTPS only
- Can call Open Cloud endpoints from within the game

**Bi-directional Architecture:**
```
Worker API ──→ Open Cloud Messaging ──→ Game Server (receives commands)
Game Server ──→ HttpService:PostAsync() ──→ Worker API (sends telemetry)
```

This is our integration backbone. We can command bots from outside AND receive journal data.

---

### 5. Browser Automation

#### Can Playwright/Selenium Drive Roblox?

**No, not the game client.** Roblox is a native desktop app, not a web app.

**What browser automation CAN do:**
- Automate Roblox website interactions (login, navigate, click "Play")
- Launch the Roblox client from the web page
- Cannot control the game once launched

**What browser automation CANNOT do:**
- Control in-game character movement
- Read game state
- Click in-game UI elements
- Capture game telemetry

**Verdict:** Browser automation is only useful for automating the *launch* of Roblox, not for playtesting. Skip this approach for game-level automation.

---

### 6. Bot Frameworks

#### pyrobloxbot (GitHub: Mews/pyrobloxbot) — ⭐ NOTABLE
- Python library for creating Roblox bots via keyboard input simulation
- Movement, chatting, UI navigation through keyboard only
- Multi-account support
- Windows only (uses Windows keyboard APIs)
- Simple API: `bot.walk_forward(5)`, `bot.chat("Hello")`, `bot.reset_player()`

**Pros:** Dead simple, real game client, real networking  
**Cons:** Windows only, keyboard-based (no mouse), no game state reading, no journaling

#### BloxBot
- AI agent that connects to Roblox Studio
- For building games, not playtesting them
- Not useful for our use case

#### Roblox Native AI Assistant (July 2026)
- Roblox's own AI that can bug-test games and explain analytics
- Uses the new Studio Testing APIs
- Still in early rollout; not externally scriptable yet
- **Watch this space** — could be the long-term solution

#### Custom Luau Bot Scripts
- Most flexible approach: write Luau scripts that control NPCs/players in-game
- Full access to game state, physics, raycasting, pathfinding
- Can journal anything to HttpService
- This is what we should build

---

### 7. Journaling & Training Data Collection

#### What to Capture

For ML training data, we need structured episodes:

```json
{
  "session_id": "uuid",
  "timestamp": "2026-08-03T08:10:00Z",
  "tick": 12345,
  "player_state": {
    "position": [x, y, z],
    "health": 100,
    "inventory": [...],
    "current_objective": "reach_the_castle"
  },
  "world_state": {
    "npcs_visible": [...],
    "nearby_interactables": [...],
    "environment": "day",
    "era": "medieval"
  },
  "action_taken": {
    "type": "move",
    "params": {"direction": "north", "duration": 2.5}
  },
  "perception": {
    "screen_description": "A stone path leads north toward castle gates...",
    "notable_objects": ["gate", "guard_npc", "sign_post"]
  },
  "reasoning": "The player sees the castle gate ahead. Moving north to progress objective.",
  "emotion": "curious"
}
```

#### How to Capture It

**In-Game Luau Journaling Script:**
- Runs on the game server every N ticks
- Captures player position, game state, nearby objects
- Posts structured data to our Worker API via HttpService
- Can include AI-generated "train-of-thought" by calling an LLM endpoint

**Telemetry → Training Pipeline:**
1. Game posts state snapshots to Worker (every 1-5 seconds)
2. Worker structures as episodes, stores in R2
3. Batch process converts episodes to training format (JSONL)
4. Feed to imitation learning model

**Industry Precedent:** EA's IL approach records human playtest sessions, then trains agents on the recordings. Our in-game journaling is the Roblox equivalent — but richer because we have full game state, not just pixels.

---

### 8. Multi-Agent Simulation

#### Roblox Native Multiplayer Testing
- **StudioTestService** supports up to **8 simulated clients** in one session
- Can simulate player joins/leaves (stress testing)
- Can trigger client disconnects (reconnection testing)
- Each client is a real Roblox client simulation with full engine

#### Approaches for Multi-Agent:

| Approach | Agent Count | Complexity | Journal Quality |
|----------|-------------|------------|-----------------|
| StudioTestService | Up to 8 | Low — built-in | Excellent — full state per client |
| Multiple Studio instances | Unlimited (scale with hardware) | Medium — orchestration needed | Excellent per instance |
| VIP Server + pyrobloxbot | 1 per Windows machine | High — need many machines | Basic — keyboard only |
| Open Cloud + MessagingService | Unlimited (virtual) | High — need AI decision engine | Custom — whatever you log |

**Best Multi-Agent Approach:** StudioTestService with 8 clients for development, scale with multiple Studio instances on a farm for production data collection.

#### Industry Multi-Agent
- **GPTeam** — open-source multi-agent simulation with unique personalities
- **nunu.ai** — multimodal AI agents powered by Gemini for game testing
- **γ-World (NVIDIA)** — generative multi-agent world model, scales 2→4 players
- **Tencent** — cloud-based testing across thousands of device configs

---

## Ranked Recommendations

### 🥇 Rank 1: In-Game Luau Journaling + Studio CLI + Worker API
**The Hybrid Three-Layer Stack**

| Criterion | Rating |
|-----------|--------|
| Feasibility | ⭐⭐⭐⭐⭐ — all official APIs |
| Cost | Free |
| Quality | ⭐⭐⭐⭐⭐ — full game state, real physics, real engine |
| Integration | ⭐⭐⭐⭐ — straightforward, we control both sides |
| Journaling | ⭐⭐⭐⭐⭐ — arbitrary data capture, train-of-thought via LLM |
| Multi-agent | ⭐⭐⭐⭐ — up to 8 via StudioTestService |

**Why #1:** Uses only official Roblox APIs. Produces the richest training data. Integrates with our existing Worker. Zero licensing cost. We can start building today.

---

### 🥈 Rank 2: Open Cloud API + AI Decision Engine + HttpService Telemetry
**External Bot Commander**

| Criterion | Rating |
|-----------|--------|
| Feasibility | ⭐⭐⭐⭐ — needs AI decision engine |
| Cost | Free (API) + LLM costs for decision-making |
| Quality | ⭐⭐⭐⭐ — real game server, real players see the bot |
| Integration | ⭐⭐⭐ — need to build AI decision logic |
| Journaling | ⭐⭐⭐⭐ — via HttpService callbacks |
| Multi-agent | ⭐⭐⭐⭐⭐ — unlimited virtual agents |

**Why #2:** Can drive bots on live production servers (not just Studio). Unlimited agent count. But requires a sophisticated external AI decision engine to choose actions.

---

### 🥉 Rank 3: pyrobloxbot + Screen Capture + Vision Model
**Keyboard Simulation + Vision**

| Criterion | Rating |
|-----------|--------|
| Feasibility | ⭐⭐⭐ — Windows only, fragile |
| Cost | Free + vision model costs |
| Quality | ⭐⭐⭐ — limited by keyboard input and vision quality |
| Integration | ⭐⭐ — need screen capture pipeline + vision model |
| Journaling | ⭐⭐⭐ — via vision model interpretation |
| Multi-agent | ⭐⭐ — one bot per Windows instance |

**Why #3:** Most similar to how EA/Ubisoft do it (input simulation + vision). But fragile, Windows-only, and produces lower-quality data than direct game state access.

---

### Rank 4: rbxsilent (Headless Client Patch)
**Renderless Real Client**

| Criterion | Rating |
|-----------|--------|
| Feasibility | ⭐⭐ — TOS risk, unstable |
| Cost | Free |
| Quality | ⭐⭐⭐⭐ — real client with networking |
| Integration | ⭐⭐ — needs exploit scripts |
| Journaling | ⭐⭐ — requires exploit-based data exfiltration |

**Why not top 3:** TOS violation risk. Could get accounts banned. Unstable against Roblox updates. Not worth the risk when official APIs exist.

---

### Rank 5: Browser Automation
**Playwright for Roblox Web**

| Criterion | Rating |
|-----------|--------|
| Feasibility | ⭐ — cannot control game |
| Cost | Free |
| Quality | ⭐ — no game data |
| Integration | N/A |
| Journaling | ⭐ — website only |

**Why last:** Simply cannot do what we need. Browser automation cannot interact with the Roblox game client.

---

## Architecture Sketches (Top 3)

### Architecture 1: Hybrid Three-Layer Stack (Recommended)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │ Cron/Worker  │  │ Studio CLI   │  │ Episode Storage    │    │
│  │ Scheduler    │──│ Launcher     │  │ (R2 Buckets)       │    │
│  └──────────────┘  └──────┬───────┘  └────────────────────┘    │
│                           │                                      │
│                    launches Studio                               │
│                    with test script                             │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                    ┌───────▼───────┐
                    │  ROBLOX STUDIO │
                    │  (--task RunScript)│
                    │                │
                    │  ┌──────────┐  │
                    │  │Journaling│  │  ┌──────────────────┐
                    │  │  Agent   │──┼──│ HttpService:     │
                    │  │ (Luau)   │  │  │ PostAsync()      │
                    │  └──────────┘  │  └────────┬─────────┘
                    │       │        │           │
                    │  ┌──────────┐  │           │
                    │  │StudioTest│  │    POST telemetry
                    │  │ Service  │  │           │
                    │  │(8 clients│  │           ▼
                    │  └──────────┘  │  ┌──────────────────┐
                    │  ┌──────────┐  │  │ Worker API        │
                    │  │Virtual   │  │  │ /api/journal      │
                    │  │Input     │  │  │                   │
                    │  └──────────┘  │  │ Structures data   │
                    └────────────────┘  │ into episodes     │
                                        │                   │
                            ┌───────────│ R2: raw captures  │
                            │           │ KV: session index │
                            ▼           │ D1: query layer   │
                    ┌──────────────┐    └──────────────────┘
                    │ LLM Endpoint │           │
                    │ (GLM-5.2)    │           ▼
                    │              │    ┌──────────────────┐
                    │ Generates    │    │ Training Data    │
                    │ train-of-    │────│ Pipeline         │
                    │ thought for  │    │ JSONL export     │
                    │ each tick    │    │ for IL training  │
                    └──────────────┘    └──────────────────┘
```

**Data Flow:**
1. Worker Scheduler triggers a playtest session (cron)
2. Studio CLI launches with the place + test script
3. StudioTestService spins up N simulated clients
4. Journaling Agent captures game state every tick
5. HttpService POSTs state snapshots to Worker API
6. Worker optionally calls LLM for train-of-thought annotations
7. Worker stores structured episodes in R2
8. Batch pipeline exports JSONL for imitation learning

---

### Architecture 2: External Bot Commander (Open Cloud)

```
┌──────────────────────────────────────────────────────────┐
│                  EXTERNAL COMMAND CENTER                  │
│                                                          │
│  ┌────────────┐   ┌──────────────┐   ┌───────────────┐  │
│  │ AI Decision│   │ Open Cloud   │   │ Episode       │  │
│  │ Engine     │──►│ Messaging    │──►│ Storage (R2)  │  │
│  │ (LLM-based)│   │ API          │   │               │  │
│  └────────────┘   └──────┬───────┘   └───────────────┘  │
│                          │                               │
│              publishMessage to topic                     │
└──────────────────────────┼───────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   LIVE ROBLOX SERVER    │
              │                        │
              │  MessagingService:     │
              │  SubscribeAsync()      │
              │       │                │
              │       ▼                │
              │  ┌──────────────┐      │
              │  │ Bot Handler  │      │
              │  │ (Luau)       │      │
              │  │              │      │
              │  │ Executes     │      │
              │  │ commands,    │      │
              │  │ captures     │      │
              │  │ state        │      │
              │  └──────┬───────┘      │
              │         │              │
              │  HttpService:          │
              │  PostAsync() ──────────┼──► Worker API
              │                        │
              └────────────────────────┘
```

**Key Difference:** Bots run on a *live production server* (or private server), not in Studio. External AI decides actions and sends them via Open Cloud Messaging. The in-game bot handler executes and reports back.

**Pros over Architecture 1:** Real server, real player interactions, unlimited scale.  
**Cons:** Need external AI decision engine; harder to coordinate; messaging rate limits.

---

### Architecture 3: pyrobloxbot + Vision Journaling

```
┌──────────────────────────────────────────────────────┐
│                  WINDOWS VPS (or local)               │
│                                                      │
│  ┌──────────────┐    ┌──────────────────────────┐   │
│  │ pyrobloxbot  │    │ Screen Capture            │   │
│  │              │    │ (mss / d3dshot)           │   │
│  │ keyboard ────┼────┼─► Roblox Client Window    │   │
│  │ simulation   │    │                           │   │
│  └──────┬───────┘    └──────────┬───────────────┘   │
│         │                       │                    │
│         │ action log            │ screenshots        │
│         │                       │                    │
│         ▼                       ▼                    │
│  ┌──────────────────────────────────────────────┐   │
│  │ Vision Model (Qwen3-VL / FLUX)               │   │
│  │                                              │   │
│  │ Analyzes screenshots + action log            │   │
│  │ Generates structured journal entries         │   │
│  │ "I see a bridge ahead. I'm choosing to       │   │
│  │  cross it because the objective marker       │   │
│  │  is on the other side."                      │   │
│  └──────────────────────┬───────────────────────┘   │
│                         │                            │
└─────────────────────────┼────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ Worker API            │
              │ /api/journal          │
              │                       │
              │ Stores episodes in R2 │
              └───────────────────────┘
```

**Key Difference:** Bot is controlled by keyboard simulation. State is captured by screenshotting and running a vision model. No HttpService needed (bot is external).

**Pros:** Works on ANY game (no script injection needed).  
**Cons:** Lower quality data (pixels vs game state), expensive vision model calls, Windows-only, fragile.

---

## Code Snippets for Recommended Approach

### Layer 1: In-Game Journaling Agent (Luau)

```lua
--!strict
-- JournalAgent.lua
-- Injected into the Roblox place, captures game state and posts to Worker API

local HttpService = game:GetService("HttpService")
local RunService = game:GetService("RunService")
local Players = game:GetService("Players")

local WORKER_URL = "https://lucineer-relay.casey-digennaro.workers.dev/api/journal"
local SESSION_ID = HttpService:GenerateGUID(false)
local TICK_INTERVAL = 1.0  -- capture state every second
local lastTick = 0

-- Configuration
local JOURNAL_CONFIG = {
    capturePlayers = true,
    captureNPCs = true,
    captureEnvironment = true,
    captureInteractables = true,
    maxRaycastDistance = 100,
}

-- Capture player state
local function capturePlayerState(player: Player)
    local character = player.Character
    if not character then return nil end
    
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    local rootPart = character:FindFirstChild("HumanoidRootPart")
    if not humanoid or not rootPart then return nil end
    
    return {
        name = player.Name,
        position = {rootPart.Position.X, rootPart.Position.Y, rootPart.Position.Z},
        health = humanoid.Health,
        maxHealth = humanoid.MaxHealth,
        walkSpeed = humanoid.WalkSpeed,
        jumpPower = humanoid.JumpPower,
        state = humanoid:GetState().Name,
    }
end

-- Capture nearby objects via workspace traversal
local function captureNearbyObjects(position: CFrame, radius: number)
    local nearby = {}
    for _, descendant in ipairs(workspace:GetDescendants()) do
        if descendant:IsA("BasePart") and descendant.CanCollide then
            local distance = (descendant.Position - position.Position).Magnitude
            if distance < radius then
                table.insert(nearby, {
                    name = descendant.Name,
                    className = descendant.ClassName,
                    position = {descendant.Position.X, descendant.Position.Y, descendant.Position.Z},
                    distance = distance,
                })
            end
        end
    end
    -- Limit to nearest 20 for payload size
    table.sort(nearby, function(a, b) return a.distance < b.distance end)
    while #nearby > 20 do table.remove(nearby) end
    return nearby
end

-- Main journaling loop
RunService.Heartbeat:Connect(function(dt)
    lastTick += dt
    if lastTick < TICK_INTERVAL then return end
    lastTick = 0
    
    local players = {}
    for _, player in ipairs(Players:GetPlayers()) do
        local state = capturePlayerState(player)
        if state then table.insert(players, state) end
    end
    
    local primaryPlayer = Players:GetPlayers()[1]
    local nearbyObjects = {}
    if primaryPlayer and primaryPlayer.Character then
        local root = primaryPlayer.Character:FindFirstChild("HumanoidRootPart")
        if root then
            nearbyObjects = captureNearbyObjects(root.CFrame, JOURNAL_CONFIG.maxRaycastDistance)
        end
    end
    
    local entry = {
        sessionId = SESSION_ID,
        timestamp = os.time(),
        tick = os.clock(),
        players = players,
        nearbyObjects = nearbyObjects,
        lighting = {
            timeOfDay = game.Lighting.ClockTime,
            brightness = game.Lighting.Brightness,
            atmosphere = game.Lighting:FindFirstChildOfClass("Atmosphere") ~= nil,
        },
    }
    
    -- Post to Worker API
    local success, err = pcall(function()
        HttpService:PostAsync(WORKER_URL, HttpService:JSONEncode(entry))
    end)
    
    if not success then
        warn("[JournalAgent] Failed to post entry: " .. tostring(err))
    end
end)

-- Also subscribe to Open Cloud commands (Architecture 2 hybrid)
local MessagingService = game:GetService("MessagingService")
MessagingService:SubscribeAsync("autoplay-command", function(message)
    local command = HttpService:JSONDecode(message.Data)
    -- Execute bot commands here
    print("[JournalAgent] Received command:", command.action)
end)

print("[JournalAgent] Started session:", SESSION_ID)
```

### Layer 2: Studio CLI Test Runner

```bash
#!/bin/bash
# run_playtest.sh
# Launches a headless Studio playtest session

STUDIO_PATH="/mnt/c/Users/eileen/AppData/Local/Roblox/Versions/version-3e9f4a7e1b81/RobloxStudioBeta.exe"
PLACE_ID="74265016723074"
UNIVERSE_ID="7127583708"
SCRIPT_PATH="/home/eileen/projects/lucineer-system/scripts/playtest_runner.luau"
OUTPUT_LOG="/home/eileen/projects/lucineer-system/logs/playtest_$(date +%s).log"

# Launch Studio with test script, exit when done
"$STUDIO_PATH" \
  --task RunScript \
  --placeId "$PLACE_ID" \
  --universeId "$UNIVERSE_ID" \
  --runScriptFile "$SCRIPT_PATH" \
  --outputFile "$OUTPUT_LOG" \
  --quitAfterExecution &

echo "Playtest started. Output: $OUTPUT_LOG"
```

```lua
--!strict
-- playtest_runner.luau
-- Runs inside Studio via --task RunScript

local StudioTestService = game:GetService("StudioTestService")
local VirtualInput = game:GetService("VirtualInput")
local HttpService = game:GetService("HttpService")

local WORKER_URL = "https://lucineer-relay.casey-digennaro.workers.dev/api/playtest/start"

-- Start a multiplayer test session with 4 simulated clients
local session = StudioTestService:StartPlayTest({
    numClients = 4,
})

-- Wait for the game to load
task.wait(5)

-- Send session start notification to Worker
HttpService:PostAsync(WORKER_URL, HttpService:JSONEncode({
    sessionType = "multiplayer",
    clientCount = 4,
    placeId = game.PlaceId,
    startTime = os.time(),
}))

-- Run a scripted sequence of actions
local function simulateGameplay(duration)
    local startTime = os.clock()
    
    while os.clock() - startTime < duration do
        -- Simulate keyboard movement (W key = forward)
        VirtualInput:PressKey(Enum.KeyCode.W)
        task.wait(2)
        VirtualInput:ReleaseKey(Enum.KeyCode.W)
        
        -- Turn right
        VirtualInput:PressKey(Enum.KeyCode.D)
        task.wait(0.5)
        VirtualInput:ReleaseKey(Enum.KeyCode.D)
        
        -- Jump
        VirtualInput:PressKey(Enum.KeyCode.Space)
        task.wait(0.2)
        VirtualInput:ReleaseKey(Enum.KeyCode.Space)
        
        -- Wait for next action
        task.wait(1)
    end
end

-- Run 5 minutes of simulated gameplay
simulateGameplay(300)

-- End the test session
session:Stop()

print("[PlaytestRunner] Session complete")
```

### Layer 3: Worker API Journal Endpoint

```typescript
// src/api/journal.ts
// Cloudflare Worker endpoint for receiving journal entries

interface JournalEntry {
  sessionId: string;
  timestamp: number;
  tick: number;
  players: PlayerState[];
  nearbyObjects: NearbyObject[];
  lighting: LightingState;
}

interface PlaytestSession {
  sessionId: string;
  startTime: number;
  entries: JournalEntry[];
  metadata: {
    placeId: string;
    clientCount: number;
    sessionType: string;
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname === '/api/journal' && request.method === 'POST') {
      return handleJournalEntry(request, env);
    }
    
    if (url.pathname === '/api/playtest/start' && request.method === 'POST') {
      return handleSessionStart(request, env);
    }
    
    if (url.pathname === '/api/playtest/export' && request.method === 'GET') {
      return exportTrainingData(request, env);
    }
    
    return new Response('Not found', { status: 404 });
  }
};

async function handleJournalEntry(request: Request, env: Env): Promise<Response> {
  const entry: JournalEntry = await request.json() as JournalEntry;
  
  // Store raw entry in R2
  const key = `journal/${entry.sessionId}/${entry.timestamp}.json`;
  await env.JOURNAL_BUCKET.put(key, JSON.stringify(entry));
  
  // Update session index in KV
  const indexKey = `session:${entry.sessionId}`;
  const existing = await env.SESSION_KV.get(indexKey, 'json') || { entries: 0, lastTick: 0 };
  existing.entries += 1;
  existing.lastTick = entry.tick;
  await env.SESSION_KV.put(indexKey, JSON.stringify(existing));
  
  return Response.json({ ok: true, entries: existing.entries });
}

async function handleSessionStart(request: Request, env: Env): Promise<Response> {
  const body = await request.json() as any;
  const sessionId = crypto.randomUUID();
  
  // Initialize session
  await env.SESSION_KV.put(`session:${sessionId}`, JSON.stringify({
    sessionId,
    startTime: Date.now(),
    placeId: body.placeId,
    clientCount: body.clientCount,
    sessionType: body.sessionType,
    entries: 0,
    status: 'running',
  }));
  
  return Response.json({ sessionId, status: 'started' });
}

async function exportTrainingData(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  const sessionId = url.searchParams.get('session');
  
  if (!sessionId) {
    return Response.json({ error: 'Missing session param' }, { status: 400 });
  }
  
  // List all entries for this session from R2
  const list = await env.JOURNAL_BUCKET.list({ prefix: `journal/${sessionId}/` });
  
  // Build JSONL training data
  const trainingExamples: string[] = [];
  for (const item of list.objects) {
    const entry = await env.JOURNAL_BUCKET.get(item.key);
    const data = await entry!.json() as JournalEntry;
    
    // Format as training example
    const example = {
      observation: {
        players: data.players,
        nearbyObjects: data.nearbyObjects,
        lighting: data.lighting,
      },
      // Action would be derived from diff between consecutive entries
      // This is where IL training pairs are constructed
      timestamp: data.timestamp,
    };
    trainingExamples.push(JSON.stringify(example));
  }
  
  return new Response(trainingExamples.join('\n'), {
    headers: { 'Content-Type': 'application/x-ndjson' }
  });
}
```

### Bonus: Open Cloud Command Sender (for Architecture 2)

```typescript
// src/api/bot_command.ts
// Send commands to live game servers via Open Cloud

const ROBLOX_API_BASE = 'https://apis.roblox.com/cloud/v2';

interface BotCommand {
  action: 'move' | 'jump' | 'interact' | 'chat' | 'reset';
  params: Record<string, unknown>;
}

export async function sendBotCommand(
  universeId: string,
  apiKey: string,
  topic: string,
  command: BotCommand
): Promise<Response> {
  const url = `${ROBLOX_API_BASE}/universes/${universeId}:publishMessage`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'x-api-key': apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      topic: topic,
      message: JSON.stringify(command),
    }),
  });
  
  if (!response.ok) {
    throw new Error(`Open Cloud API error: ${response.status} ${response.statusText}`);
  }
  
  return response;
}

// Example: Move bot forward for 3 seconds
// sendBotCommand(UNIVERSE_ID, API_KEY, 'autoplay-command', {
//   action: 'move',
//   params: { direction: 'forward', duration: 3 }
// });
```

---

## Build TODAY vs Needs More Research

### ✅ Can Build TODAY

1. **In-Game Journaling Agent** — Write the Luau script, inject into our `.rbxlx` place. Posts game state to our Worker API every second. This is the core data collection layer.

2. **Worker API Journal Endpoint** — Add `/api/journal` and `/api/playtest/start` routes to our existing Worker. Store entries in R2, index in KV. We already have the Worker infrastructure.

3. **Studio CLI Test Runner** — Write a bash script that launches Studio with `--task RunScript --quitAfterExecution`. Run on the Windows machine (WSL can invoke the Windows Studio exe).

4. **Basic Bot Actions via VirtualInput** — Use the new `VirtualInput` API to simulate keyboard/mouse in Studio playtests. Combined with StudioTestService for multiplayer simulation.

5. **Training Data Export** — Add an `/api/playtest/export` endpoint that converts R2 journal entries to JSONL format for ML training.

6. **Open Cloud Command Channel** — Create an API key, subscribe to a topic in our game, and send commands from the Worker via REST. This gives us external control of live servers.

### 🔬 Needs More Research

1. **AI Decision Engine** — Building the external brain that decides what actions bots should take. Could use GLM-5.2, but needs a proper observation→action loop architecture. Research needed on prompt design, context windows, and real-time decision latency.

2. **Imitation Learning Model Training** — EA's SEED showed IL trains in 20 min vs 5 hours for RL. But we need to define the model architecture, training pipeline, and evaluation metrics. This is a full ML project.

3. **Multi-Studio Instance Farm** — Running multiple Studio instances in parallel for large-scale data collection. Need to figure out resource requirements, orchestration (k8s?), and session isolation.

4. **Train-of-Thought Annotation** — Having an LLM generate "reasoning" text for each game state snapshot. Need to determine the best model (GLM-5.2 for cost, Hermes-3 for creativity), prompt format, and how to keep latency low enough for real-time annotation.

5. **Roblox Assistant AI Integration** — Roblox's own AI (July 2026 rollout) can bug-test and analyze games. Monitor for API access that would let us programmatically trigger AI playtests.

6. **Cross-Game Generalization** — Whether a bot trained on Lucineer's game can generalize to other Roblox experiences. EA found their IL agents were game-specific; we'd need per-game training.

---

## Summary Comparison Matrix

| Approach | Feasibility | Cost | Quality | Integration | Journaling | Multi-Agent |
|----------|------------|------|---------|-------------|------------|-------------|
| **Luau Journal + Studio CLI** | ⭐⭐⭐⭐⭐ | Free | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Open Cloud + AI Engine** | ⭐⭐⭐⭐ | Free + LLM | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **pyrobloxbot + Vision** | ⭐⭐⭐ | Free + vision | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **rbxsilent** | ⭐⭐ | Free | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Browser Automation** | ⭐ | Free | ⭐ | N/A | ⭐ | ⭐ |

---

## Recommended Action Plan

### Phase 1: Foundation (Week 1-2)
- Write the JournalAgent.luau script
- Add journal endpoints to our Worker
- Set up R2 bucket + KV namespace for storage
- Test with a manual Studio playtest

### Phase 2: Automation (Week 3-4)
- Build the Studio CLI test runner script
- Implement VirtualInput-based bot actions
- Set up cron-triggered playtest sessions
- Add StudioTestService multiplayer (4-8 bots)

### Phase 3: Intelligence (Week 5-8)
- Build the AI decision engine (LLM-based action selection)
- Implement train-of-thought annotation
- Connect Open Cloud for live server control
- Begin collecting training episodes at scale

### Phase 4: Learning (Month 3+)
- Export episodes as JSONL training data
- Train first imitation learning model
- Compare IL bot performance vs scripted bot
- Iterate on model architecture

---

*Research complete. The path is clear: Luau journaling + Studio CLI + Worker API. All official APIs, zero cost, maximum data quality. Start with Phase 1 today.*
