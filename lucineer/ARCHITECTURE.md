# Lucineer — Architecture Document

> A persistent AI companion that lives inside Roblox and builds worlds with the player in real-time.

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        THE LUCINEER SYSTEM                              │
│                                                                         │
│  ┌──────────────┐     HTTPS      ┌──────────────┐    HTTP     ┌───────┐ │
│  │   Roblox     │ ◄──────────►   │  Cloudflare  │ ◄────────►  │OpenClaw│ │
│  │  Lua Client  │   (poll-based) │   Worker     │  (relay)    │ Agent │ │
│  │              │                │  (Durable    │             │(Lucy) │ │
│  │ • Chat capture│               │   Object)    │             │       │ │
│  │ • Build exec  │               │              │             │ • Plan│ │
│  │ • World scan  │               │ • Job queue  │             │ • Code│ │
│  │ • UI display  │               │ • State cache│             │ • Mem │ │
│  └──────────────┘                └──────────────┘             └───────┘ │
│         ▲                                                             │
│         │ Argon live sync (local filesystem → Studio)                 │
│         ▼                                                             │
│  ┌──────────────┐                                                     │
│  │  Dev Machine │                                                     │
│  │  (Argon CLI) │                                                     │
│  │  watches /src│                                                     │
│  └──────────────┘                                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### Core Insight: Dual-Channel Architecture

The AI builds through **two complementary channels**:

| Channel | Mechanism | Best For | Speed |
|---------|-----------|----------|-------|
| **Hot Path** | Build commands sent through Worker → Roblox executes via `loadstring`-style dispatcher | Runtime spawning, instant feedback, interactive building | ~100ms |
| **Cold Path** | AI writes Lua files → Argon syncs to Studio | New persistent scripts, module systems, structural game logic | ~1-5s |

**Decision:** Use **Hot Path as primary** for v1. It's simpler, faster, and doesn't require Argon for the core loop. Argon is used as a **secondary channel** for evolving the game's codebase.

---

## 2. Data Flow

### 2.1 Player Says Something → AI Builds

```
Player types: "build me a tower with a glowing roof"
     │
     ▼
┌─────────────────────────────────────────────┐
│ 1. Roblox Client captures chat              │
│    POST /api/message                        │
│    { sessionId, message, playerState }      │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│ 2. Cloudflare Worker receives message       │
│    - Creates job (UUID)                     │
│    - Stores in Durable Object               │
│    - Forwards to OpenClaw via HTTP          │
│    - Returns { jobId } immediately          │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│ 3. OpenClaw agent processes request         │
│    - Reads world state from request         │
│    - Decides what to build                  │
│    - Generates build commands (Lua table)   │
│    - Optionally writes Lua files for Argon  │
│    - POST /api/job/{jobId}/result           │
│    { reply, commands[], files[] }           │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│ 4. Roblox Client polls GET /api/job/{jobId} │
│    - Receives AI reply + build commands     │
│    - Displays reply in chat UI              │
│    - Executes build commands in-game        │
└─────────────────────────────────────────────┘
```

### 2.2 World State Sync (Roblox → AI)

```
Every N seconds (or on significant change):
┌─────────────────────────────────────────────┐
│ Roblox Client collects:                     │
│  - Player position, look direction          │
│  - Nearby instances (name, class, position) │
│  - Terrain summary (size, material counts)  │
│  - Build history (what's been placed)       │
│  POST /api/state                            │
│  { sessionId, worldSnapshot }               │
└────────────────────┬────────────────────────┘
                     ▼
│ Worker stores in Durable Object             │
│ OpenClaw retrieves on next request          │
```

---

## 3. Worker API Design

### Base URL: `https://lucineer.{subdomain}.workers.dev`

All endpoints accept/return JSON. Auth via `X-Lucineer-Key` header (shared secret).

### 3.1 `POST /api/message` — Send player chat to AI

**Request:**
```json
{
  "sessionId": "roblox-game-12345",
  "playerName": "BuilderDev",
  "message": "build me a tower with a glowing roof",
  "playerState": {
    "position": { "x": 10, "y": 5, "z": -20 },
    "lookVector": { "x": 0, "y": 0, "z": -1 },
    "selectedItems": []
  },
  "worldSnapshot": {
    "nearbyInstances": [
      { "name": "SpawnLocation", "class": "SpawnLocation", "position": {"x":0,"y":1,"z":0} }
    ],
    "terrainSize": { "x": 512, "y": 64, "z": 512 },
    "buildCount": 3
  }
}
```

**Response (202 Accepted):**
```json
{
  "jobId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "status": "queued"
}
```

### 3.2 `GET /api/job/:jobId` — Poll for AI response

**Response (200, when ready):**
```json
{
  "jobId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "status": "complete",
  "reply": "I'll build you a stone tower with a neon cyan glowing roof! Placing it 15 studs ahead of you.",
  "commands": [
    {
      "type": "createPart",
      "params": {
        "name": "TowerBase",
        "shape": "Block",
        "size": { "x": 8, "y": 24, "z": 8 },
        "position": { "x": 10, "y": 17, "z": -35 },
        "material": "Cobblestone",
        "color": { "r": 163, "g": 162, "b": 165 }
      }
    },
    {
      "type": "createPart",
      "params": {
        "name": "GlowRoof",
        "shape": "Block",
        "size": { "x": 10, "y": 2, "z": 10 },
        "position": { "x": 10, "y": 30, "z": -35 },
        "material": "Neon",
        "color": { "r": 0, "g": 255, "b": 255 }
      }
    },
    {
      "type": "addLight",
      "params": {
        "parent": "GlowRoof",
        "lightType": "PointLight",
        "brightness": 3,
        "range": 30,
        "color": { "r": 0, "g": 255, "b": 255 }
      }
    }
  ],
  "files": []
}
```

**Response (200, still processing):**
```json
{
  "jobId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "status": "processing"
}
```

**Response (200, error):**
```json
{
  "jobId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "status": "error",
  "error": "AI request failed: timeout"
}
```

### 3.3 `POST /api/state` — Update world state

**Request:**
```json
{
  "sessionId": "roblox-game-12345",
  "worldSnapshot": {
    "playerPosition": { "x": 15, "y": 5, "z": -18 },
    "nearbyInstances": [...],
    "buildCount": 5,
    "lastBuiltAt": 1699488000
  }
}
```

**Response (200):**
```json
{ "ok": true }
```

### 3.4 `GET /api/state/:sessionId` — Retrieve world state (used by OpenClaw)

**Response (200):**
```json
{
  "sessionId": "roblox-game-12345",
  "worldSnapshot": { ... },
  "updatedAt": 1699488000
}
```

### 3.5 `POST /api/job/:jobId/result` — OpenClaw posts result

**Request:**
```json
{
  "reply": "I'll build you a tower...",
  "commands": [...],
  "files": [
    {
      "path": "src/server/TowerSystem.lua",
      "content": "-- Lua source code here..."
    }
  ]
}
```

**Response (200):**
```json
{ "ok": true }
```

### 3.6 `GET /api/health` — Health check

```json
{ "status": "ok", "version": "1.0.0", "time": 1699488000 }
```

---

## 4. Build Command Schema

The `commands[]` array uses a typed command protocol. The Roblox client has an executor that dispatches these.

### Command Types (v1)

| Type | Description | Key Params |
|------|-------------|------------|
| `createPart` | Spawn a BasePart | name, shape, size, position, material, color, anchored, canCollide |
| `createModel` | Group parts into a model | name, children[] (recursive commands) |
| `deletePart` | Remove a part by name | name |
| `movePart` | Move existing part | name, position |
| `addLight` | Attach light to part | parent, lightType, brightness, range, color |
| `addSound` | Attach sound to part | parent, soundId, volume, looped |
| `addScript` | Inject a Script/LocalScript | parent, scriptType, source |
| `setTerrain` | Modify terrain region | region, material, resolution |
| `sendMessage` | Display system message | text, duration |
| `runLua` | Execute arbitrary Lua string | source (scoped to sandbox) |

### Color Format
All colors use `{ "r": 0-255, "g": 0-255, "b": 0-255 }` (Roblox Color3.fromRGB).

### Position/Size Format
All vectors use `{ "x": number, "y": number, "z": number }` → converted to `Vector3.new(x, y, z)`.

---

## 5. Roblox Lua Module Structure

### File Layout (Argon project)

```
lucineer-roblox/
├── default.project.json          # Argon project config
├── src/
│   ├── ReplicatedStorage/
│   │   └── Lucineer/             # Shared modules
│   │       ├── init.lua           # Module root, exports Lucineer table
│   │       ├── Config.lua         # Configuration (endpoints, auth, polling)
│   │       ├── Http.lua           # HttpService wrapper with retry/backoff
│   │       ├── Poller.lua         # Job polling state machine
│   │       ├── ChatHandler.lua    # Captures player chat → sends to Worker
│   │       ├── CommandExecutor.lua# Executes build commands from AI
│   │       ├── WorldScanner.lua   # Collects world state for AI context
│   │       ├── UIManager.lua      # In-game UI for AI responses
│   │       └── types.lua          # Type definitions (Roblox Luau)
│   │
│   ├── ServerScriptService/
│   │   └── LucineerServer/
│   │       ├── init.lua           # Server bootstrap (entry point)
│   │       └── BuildLog.lua       # Persistent build history (DataStore)
│   │
│   └── StarterPlayer/
│       └── StarterPlayerScripts/
│           └── LucineerClient/
│               └── init.lua       # Client-side chat UI + local state
```

### Module Responsibilities

#### `Config.lua`
```lua
local Config = {
    WorkerUrl = "https://lucineer.YOUR-SUBDOMAIN.workers.dev",
    AuthKey = "YOUR_SECRET_KEY",  -- Set as an environment variable or secret
    PollInterval = 0.5,           -- Seconds between job status polls
    StateSyncInterval = 10,       -- Seconds between world state syncs
    MaxRetries = 3,
    CommandRateLimit = 50,        -- Max commands per second
}
return Config
```

#### `Http.lua` — Wrapper around HttpService
- `Http.post(path, body)` → `Response`
- `Http.get(path)` → `Response`
- `Http.request(method, path, body, timeout)` → `Response`
- Handles JSON encode/decode, auth headers, pcall + retry with exponential backoff

#### `Poller.lua` — Job polling state machine
```lua
-- Tracks active jobs by ID, polls GET /api/job/:jobId
-- When status == "complete", fires callback with result
-- When status == "error", fires error callback
-- Auto-stops polling after max attempts (timeout: ~60s)
local Poller = {}
Poller.__index = Poller

function Poller.new(http)
    local self = setmetatable({}, Poller)
    self.Http = http
    self.ActiveJobs = {}  -- { [jobId] = { onComplete, onError, attempts } }
    return self
end

function Poller:track(jobId, onComplete, onError)
    self.ActiveJobs[jobId] = {
        onComplete = onComplete,
        onError = onError,
        attempts = 0,
    }
end

function Poller:tick()
    for jobId, job in pairs(self.ActiveJobs) do
        job.attempts += 1
        if job.attempts > 120 then  -- 60s @ 0.5s interval
            job.onError("timeout")
            self.ActiveJobs[jobId] = nil
            return
        end
        local ok, response = pcall(function()
            return self.Http:get("/api/job/" .. jobId)
        end)
        if ok and response.status == "complete" then
            job.onComplete(response)
            self.ActiveJobs[jobId] = nil
        elseif ok and response.status == "error" then
            job.onError(response.error)
            self.ActiveJobs[jobId] = nil
        end
    end
end
```

#### `ChatHandler.lua` — Captures chat and sends to Worker
- Listens to `Players.PlayerChatted` or custom chat events
- Sends `POST /api/message` with player state
- On `jobId` response, registers with Poller
- Poller callback → UIManager (display reply) + CommandExecutor (run commands)

#### `CommandExecutor.lua` — The build engine
```lua
-- Dispatches commands by type
local CommandExecutor = {}
CommandExecutor.__index = CommandExecutor

local Executors = {
    createPart = function(params)
        local part = Instance.new("Part")
        part.Name = params.name
        part.Size = Vector3.new(params.size.x, params.size.y, params.size.z)
        part.Position = Vector3.new(params.position.x, params.position.y, params.position.z)
        part.Material = Enum.Material[params.material] or Enum.Material.Plastic
        part.Color = Color3.fromRGB(params.color.r, params.color.g, params.color.b)
        part.Anchored = if params.anchored ~= nil then params.anchored else true
        part.CanCollide = if params.canCollide ~= nil then params.canCollide else true
        part.Shape = if params.shape == "Ball" then Enum.PartType.Ball
                   elseif params.shape == "Cylinder" then Enum.PartType.Cylinder
                   else Enum.PartType.Block
        part.Parent = workspace
        return part
    end,

    createModel = function(params)
        local model = Instance.new("Model")
        model.Name = params.name
        for _, childCmd in ipairs(params.children or {}) do
            local child = Executors[childCmd.type](childCmd.params)
            if child then child.Parent = model end
        end
        model.Parent = workspace
        return model
    end,

    addLight = function(params)
        local parent = workspace:FindFirstChild(params.parent)
        if not parent then return end
        local light = Instance.new(params.lightType or "PointLight")
        light.Brightness = params.brightness or 1
        light.Range = params.range or 15
        light.Color = Color3.fromRGB(params.color.r or 255, params.color.g or 255, params.color.b or 255)
        light.Parent = parent
        return light
    end,

    deletePart = function(params)
        local part = workspace:FindFirstChild(params.name)
        if part then part:Destroy() end
    end,

    runLua = function(params)
        local fn, err = loadstring(params.source)
        if fn then fn() else warn("[Lucineer] Lua error:", err) end
    end,

    sendMessage = function(params)
        game.StarterGui:SetCore("ChatMakeSystemMessage", {
            Text = "[Lucineer] " .. params.text,
            Color = Color3.fromRGB(100, 255, 200),
            Font = Enum.Font.GothamMedium,
        })
    end,
}

function CommandExecutor.execute(commands)
    for _, cmd in ipairs(commands) do
        local executor = Executors[cmd.type]
        if executor then
            local ok, err = pcall(executor, cmd.params)
            if not ok then
                warn(string.format("[Lucineer] Command '%s' failed: %s", cmd.type, err))
            end
        else
            warn("[Lucineer] Unknown command type: " .. tostring(cmd.type))
        end
        task.wait()  -- Yield to avoid throttling
    end
end

return CommandExecutor
```

#### `WorldScanner.lua` — Collects world state
```lua
local WorldScanner = {}

function WorldScanner.snapshot(player, maxInstances)
    maxInstances = maxInstances or 50
    local root = workspace
    local instances = {}

    local count = 0
    for _, descendant in ipairs(root:GetDescendants()) do
        if count >= maxInstances then break end
        if descendant:IsA("BasePart") and not descendant:IsA("Terrain") then
            table.insert(instances, {
                name = descendant.Name,
                class = descendant.ClassName,
                position = {
                    x = descendant.Position.X,
                    y = descendant.Position.Y,
                    z = descendant.Position.Z,
                },
                size = {
                    x = descendant.Size.X,
                    y = descendant.Size.Y,
                    z = descendant.Size.Z,
                },
                material = tostring(descendant.Material.Name),
            })
            count += 1
        end
    end

    return {
        playerPosition = {
            x = player.Character.PrimaryPart.Position.X,
            y = player.Character.PrimaryPart.Position.Y,
            z = player.Character.PrimaryPart.Position.Z,
        },
        nearbyInstances = instances,
        buildCount = count,
        scannedAt = os.time(),
    }
end

return WorldScanner
```

#### `UIManager.lua` — In-game AI chat display
- Creates a BillboardGui or ScreenGui chat bubble
- Shows AI responses with typing animation
- Handles queued messages (multiple before player reads)

---

## 6. Cloudflare Worker Implementation

### Architecture: Durable Object for Job Queue + State

```
Worker (lucineer-relay)
├── routes/
│   ├── POST /api/message         → creates job, forwards to OpenClaw
│   ├── GET  /api/job/:id         → reads job status from DO
│   ├── POST /api/job/:id/result  → OpenClaw posts result to DO
│   ├── POST /api/state           → updates world state in DO
│   ├── GET  /api/state/:session  → reads world state from DO
│   └── GET  /api/health
│
└── Durable Object: LucineerSession
    ├── jobs: Map<jobId, { status, reply, commands, files, createdAt }>
    ├── worldState: { sessionId, snapshot, updatedAt }
    ├── messageHistory: Array<{ role, content, timestamp }>
    └── sessionMeta: { playerId, playerName, createdAt }
```

### Worker Source Structure

```
lucineer-worker/
├── wrangler.jsonc
├── src/
│   ├── index.ts           # Worker entry point (fetch handler, routing)
│   ├── router.ts          # Route matching
│   ├── openclaw.ts        # OpenClaw HTTP client (forwards messages)
│   ├── types.ts           # TypeScript types for API shapes
│   └── do/
│       └── LucineerSession.ts  # Durable Object definition
└── package.json
```

### Key Worker Logic (index.ts sketch)

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const route = url.pathname;

    // POST /api/message
    if (route === "/api/message" && request.method === "POST") {
      const body = await request.json() as MessageRequest;
      const doId = env.LUCINEER.idFromName(body.sessionId);
      const stub = env.LUCINEER.get(doId);

      // Create job in DO
      const { jobId } = await stub.createJob(body);

      // Fire-and-forget: forward to OpenClaw
      ctx.waitUntil(forwardToOpenClaw(env, jobId, body, stub));

      return json({ jobId, status: "queued" }, 202);
    }

    // GET /api/job/:jobId
    if (route.startsWith("/api/job/") && request.method === "GET") {
      const jobId = route.split("/")[3];
      const sessionId = url.searchParams.get("session")!;
      const doId = env.LUCINEER.idFromName(sessionId);
      const stub = env.LUCINEER.get(doId);
      const job = await stub.getJob(jobId);
      return json(job);
    }

    // POST /api/job/:jobId/result  (OpenClaw posts result)
    if (route.startsWith("/api/job/") && route.endsWith("/result") && request.method === "POST") {
      const jobId = route.split("/")[3];
      const sessionId = url.searchParams.get("session")!;
      const result = await request.json();
      const doId = env.LUCINEER.idFromName(sessionId);
      const stub = env.LUCINEER.get(doId);
      await stub.completeJob(jobId, result);
      return json({ ok: true });
    }

    // POST /api/state
    if (route === "/api/state" && request.method === "POST") {
      const body = await request.json();
      const doId = env.LUCINEER.idFromName(body.sessionId);
      const stub = env.LUCINEER.get(doId);
      await stub.updateState(body.worldSnapshot);
      return json({ ok: true });
    }

    // GET /api/health
    if (route === "/api/health") {
      return json({ status: "ok", version: "1.0.0", time: Date.now() });
    }

    return new Response("Not found", { status: 404 });
  }
};
```

### OpenClaw Forwarding (`openclaw.ts`)

```typescript
export async function forwardToOpenClaw(
  env: Env,
  jobId: string,
  message: MessageRequest,
  stub: DurableObjectStub
): Promise<void> {
  const payload = {
    jobId,
    sessionId: message.sessionId,
    playerName: message.playerName,
    message: message.message,
    playerState: message.playerState,
    worldSnapshot: message.worldSnapshot,
    callbackUrl: `${env.WORKER_URL}/api/job/${jobId}/result?session=${message.sessionId}`,
  };

  // Call OpenClaw's HTTP API (or use webhook mechanism)
  await fetch(`${env.OPENCLAW_URL}/api/lucineer/message`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${env.OPENCLAW_TOKEN}`,
    },
    body: JSON.stringify(payload),
  });
}
```

### Durable Object (`LucineerSession.ts`)

```typescript
export class LucineerSession {
  state: DurableObjectState;
  jobs: Map<string, Job>;
  worldState: WorldSnapshot | null;
  history: Message[];

  constructor(state: DurableObjectState) {
    this.state = state;
    this.jobs = new Map();
    this.worldState = null;
    this.history = [];
  }

  async createJob(req: MessageRequest): Promise<{ jobId: string }> {
    const jobId = crypto.randomUUID();
    this.jobs.set(jobId, {
      id: jobId,
      status: "processing",
      createdAt: Date.now(),
      reply: null,
      commands: null,
      files: null,
    });
    this.history.push({ role: "user", content: req.message, timestamp: Date.now() });
    return { jobId };
  }

  async getJob(jobId: string): Promise<JobResponse> {
    const job = this.jobs.get(jobId);
    if (!job) return { jobId, status: "not_found" };
    return {
      jobId: job.id,
      status: job.status,
      reply: job.reply,
      commands: job.commands,
      files: job.files,
      error: job.error,
    };
  }

  async completeJob(jobId: string, result: any): Promise<void> {
    const job = this.jobs.get(jobId);
    if (job) {
      job.status = "complete";
      job.reply = result.reply;
      job.commands = result.commands || [];
      job.files = result.files || [];
      this.history.push({ role: "assistant", content: result.reply, timestamp: Date.now() });
    }
  }

  async updateState(snapshot: WorldSnapshot): Promise<void> {
    this.worldState = { ...snapshot, updatedAt: Date.now() };
  }

  // Clean up old jobs periodically (call from alarm)
  async cleanup(): Promise<void> {
    const now = Date.now();
    const TTL = 5 * 60 * 1000; // 5 minutes
    for (const [id, job] of this.jobs) {
      if (now - job.createdAt > TTL) {
        this.jobs.delete(id);
      }
    }
  }
}
```

### `wrangler.jsonc`

```jsonc
{
  "name": "lucineer-relay",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-01",
  "durable_objects": {
    "bindings": [{
      "name": "LUCINEER",
      "class_name": "LucineerSession"
    }]
  },
  "migrations": [{
    "tag": "v1",
    "new_sqlite_classes": ["LucineerSession"]
  }],
  "vars": {
    "WORKER_URL": "https://lucineer.YOUR-SUBDOMAIN.workers.dev",
    "OPENCLAW_URL": "http://YOUR-HOST:PORT"
  },
  "secrets": ["OPENCLAW_TOKEN", "LUCINEER_AUTH_KEY"]
}
```

---

## 7. OpenClaw Integration Plan

### How OpenClaw receives and responds

OpenClaw exposes an HTTP endpoint that the Worker calls. The simplest integration:

#### Option A: Webhook Listener (Simplest, v1)

OpenClaw runs a lightweight HTTP server (or uses its built-in webhook system) at `/api/lucineer/message`:

```
Worker → POST /api/lucineer/message
  {
    "jobId": "uuid",
    "sessionId": "roblox-game-12345",
    "message": "build me a tower",
    "worldSnapshot": { ... },
    "callbackUrl": "https://lucineer.workers.dev/api/job/uuid/result?session=..."
  }

OpenClaw processes:
  1. Parse the player's intent
  2. Load world state from snapshot
  3. Load memory (what's been built, player preferences)
  4. Decide what to build
  5. Generate build commands
  6. Optionally write Lua files for Argon sync
  7. POST result back to callbackUrl
```

#### Option B: OpenClaw Skill (v2, richer)

Create a Lucineer skill in OpenClaw that:
- Registers as a message handler for Roblox sessions
- Has a `world/` directory with persistent world state files
- Uses OpenClaw's memory system for cross-session recall
- Can spawn subagents for complex builds (e.g., "build a village" → multiple sub-builds)

### OpenClaw Agent Prompt (Lucineer persona)

The agent operates with this system context:

```
You are Lucineer ("Lucy"), an AI companion that lives inside Roblox.
The player talks to you through the game chat. You respond conversationally
AND build things in the game world.

When the player asks you to build something:
1. Understand what they want
2. Check the world state (player position, what's nearby)
3. Generate build commands as a JSON array
4. Write a short, friendly reply explaining what you built
5. If the build requires new persistent scripts, also write Lua files

Build command types: createPart, createModel, addLight, addSound,
addScript, deletePart, movePart, setTerrain, sendMessage, runLua

Always position builds relative to the player's current position.
Be generous and creative. The player is here to have fun.
```

### Memory Strategy for OpenClaw

```
workspace/
├── lucineer/
│   ├── ARCHITECTURE.md          # This document
│   ├── memory/
│   │   ├── world-state.json     # Latest known world state per session
│   │   ├── build-history.json   # What has been built (persistent)
│   │   ├── player-prefs.json    # Player preferences and style
│   │   └── session-log/         # Per-session conversation logs
│   │       └── {sessionId}.jsonl
│   ├── src/                     # Lua source for Argon sync
│   │   ├── server/
│   │   ├── client/
│   │   └── shared/
│   └── skills/
│       └── lucineer-build/      # OpenClaw skill for building
│           └── SKILL.md
```

---

## 8. Memory & Persistence Strategy

### Three Tiers of Memory

| Tier | What | Where | Lifetime |
|------|------|-------|----------|
| **Ephemeral** | Current job, polling state | Worker Durable Object | 5 min TTL |
| **Session** | Conversation history, world snapshot | Worker DO + OpenClaw session files | Per game session |
| **Persistent** | Build history, player preferences, world manifest | OpenClaw workspace files + Roblox DataStores | Forever |

### Roblox DataStore (Build Log)

```lua
-- BuildLog.lua (ServerScriptService)
local DataStoreService = game:GetService("DataStoreService")
local BuildStore = DataStoreService:GetDataStore("Lucineer_Builds")

local BuildLog = {}

function BuildLog.save(sessionId, entry)
    local key = sessionId .. "_" .. tostring(os.time())
    BuildStore:SetAsync(key, entry)
end

function BuildLog.loadRecent(sessionId, count)
    -- Load last N builds for context
    local entries = {}
    -- Implementation: page through DataStore keys
    return entries
end

return BuildLog
```

### OpenClaw Persistent Memory

The agent maintains files in `lucineer/memory/`:
- **`world-state.json`** — Last known positions, instances, build count
- **`build-history.json`** — Append-only log: `{ timestamp, sessionId, description, commandCount }`
- **`player-prefs.json`** — Learned preferences: favorite colors, build styles, frequently requested items
- **`session-log/{sessionId}.jsonl`** — Full conversation per session for replay/analysis

On each new request, the agent loads relevant memory files, incorporates context, and updates them after responding.

---

## 9. Implementation Order (Build TODAY)

### Phase 1: Minimal Viable Loop (2-3 hours)

1. **Worker** (`lucineer-worker/`) — 30 min
   - Single `index.ts`, no Durable Objects yet
   - `POST /api/message` → store job in `Map`, forward to OpenClaw
   - `GET /api/job/:id` → return job from `Map`
   - `POST /api/job/:id/result` → store result

2. **Roblox Client** (`lucineer-roblox/`) — 60 min
   - `Config.lua`, `Http.lua`, `ChatHandler.lua`, `CommandExecutor.lua`, `Poller.lua`
   - Player types in chat → message goes to Worker → polls for result → executes commands
   - Basic `createPart` and `sendMessage` commands only

3. **OpenClaw handler** — 30 min
   - Receives forwarded messages
   - Generates simple build commands (e.g., "build a tower" → createPart commands)
   - Posts result back to Worker

### Phase 2: Richness (1-2 hours)

4. **World state sync** — WorldScanner.lua + `POST /api/state`
5. **More command types** — addLight, createModel, runLua, addScript
6. **UI** — Chat bubbles for AI responses, build status indicators
7. **Memory files** — OpenClaw writes build history

### Phase 3: Polish (ongoing)

8. **Durable Objects** — Migrate from in-memory Map to DO for persistence
9. **Argon integration** — AI writes Lua files for persistent scripts
10. **OpenClaw skill** — Proper Lucineer skill with SKILL.md
11. **DataStore** — Roblox-side persistent build log
12. **Error handling** — Retry, backoff, rate limiting, command validation
13. **Security** — Auth keys, input sanitization, sandbox for `runLua`

---

## 10. Security Considerations

| Risk | Mitigation |
|------|------------|
| Unauthorized Worker access | `X-Lucineer-Key` header with shared secret on all endpoints |
| `runLua` command injection | Server-side sandbox: strip dangerous functions (`os.execute`, `loadfile`, `require` outside whitelist) |
| Spam from Roblox chat | Rate limit per session (max 10 messages/min) in Worker DO |
| OpenClaw token exposure | Store as Worker secret (`wrangler secret put`), never in code |
| World state bloat | Cap `nearbyInstances` at 50, trim old fields |
| Durable Object storage | Set TTL on jobs (5 min), use alarms for cleanup |

---

## 11. Growth Path (Post-v1)

| Feature | How |
|---------|-----|
| **Voice chat** | Roblox Voice Chat → capture audio → STT via Worker → OpenClaw |
| **Multi-player** | Multiple sessions per DO, broadcast build events |
| **World templates** | AI loads pre-built structures from a template library |
| **Asset generation** | AI generates textures/meshes via GPU → uploads to Roblox |
| **Procedural terrain** | `setTerrain` command with noise functions |
| **AI NPC scripting** | AI writes behavioral scripts synced via Argon |
| **Versioning** | Git-track all Lua files, rollback builds |
| **Companion personality** | Rich Lucineer persona with evolving memory across sessions |

---

## 12. Hermes Reference Analysis

The SuperInstance/hermes-roblox-construct repo provides useful **structural patterns** we adapt:

| Hermes Concept | Lucineer Adaptation |
|----------------|---------------------|
| `ManifestationBridge` — buffers work between listener and executor | Worker Durable Object job queue |
| `MasterOrchestrator` — heartbeat loop polling bridge | Roblox `Poller.lua` + `RunService.Heartbeat` |
| `CommandInterface` — intent-to-action translation | OpenClaw agent (natural language → build commands) |
| `AgentCore` — agent state tracking | World state in DO + OpenClaw memory files |
| `TemplateEngine` — archetype-based instantiation | Build command schema + future template library |
| `SwarmCoordinator` — multi-agent coordination | Future: multiple OpenClaw subagents for complex builds |
| Hermes CLI (`hermes new`) | `lucineer init` — scaffold Roblox project with Argon config |

**Key difference:** Hermes uses a SuperInstance fleet integration (proprietary vector index, foreman STT/TTS). Lucineer uses **OpenClaw** as the intelligence layer — more flexible, already running, and directly integrated with the user's existing setup.

---

## Appendix A: Full Command JSON Examples

### "Build a house"
```json
{
  "reply": "Building a cozy wooden house right in front of you!",
  "commands": [
    { "type": "createPart", "params": { "name": "Floor", "shape": "Block", "size": {"x":24,"y":1,"z":20}, "position": {"x":10,"y":1,"z":-35}, "material": "WoodPlanks", "color": {"r":153,"g":102,"b":51} }},
    { "type": "createPart", "params": { "name": "WallBack", "shape": "Block", "size": {"x":24,"y":12,"z":1}, "position": {"x":10,"y":7,"z":-44}, "material": "WoodPlanks", "color": {"r":153,"g":102,"b":51} }},
    { "type": "createPart", "params": { "name": "WallLeft", "shape": "Block", "size": {"x":1,"y":12,"z":20}, "position": {"x":-1,"y":7,"z":-35}, "material": "WoodPlanks", "color": {"r":153,"g":102,"b":51} }},
    { "type": "createPart", "params": { "name": "WallRight", "shape": "Block", "size": {"x":1,"y":12,"z":20}, "position": {"x":21,"y":7,"z":-35}, "material": "WoodPlanks", "color": {"r":153,"g":102,"b":51} }},
    { "type": "createPart", "params": { "name": "Roof", "shape": "Block", "size": {"x":26,"y":1,"z":22}, "position": {"x":10,"y":13,"z":-35}, "material": "WoodPlanks", "color": {"r":102,"g":51,"b":0} }},
    { "type": "addLight", "params": { "parent": "Roof", "lightType": "PointLight", "brightness": 2, "range": 25, "color": {"r":255,"g":220,"b":150} }}
  ]
}
```

### "Make it rain particles"
```json
{
  "reply": "Adding a gentle rain particle effect above your head!",
  "commands": [
    { "type": "runLua", "params": { "source": "local p = Instance.new('ParticleEmitter')\np.Texture = 'rbxassetid://241876419'\np.Rate = 100\np.Lifetime = NumberRange.new(3,5)\np.Speed = NumberRange.new(2,5)\np.SpreadAngle = Vector2.new(360,360)\np.Parent = workspace.Terrain\np.Position = workspace.Terrain.Position + Vector3.new(0,100,0)" }}
  ]
}
```

---

*End of Architecture Document. This is a living spec — update as the system evolves.*
