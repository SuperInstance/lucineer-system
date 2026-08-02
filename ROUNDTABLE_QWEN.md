# Qwen3.7-Max — Technical Implementation Plan

*Generated in 121.0s*

This is the blueprint to bridge the gap between "functional prototype" and "world-class experience." We are replacing the sterile, instantaneous part-popping with a visceral, industrial, real-time construction sequence. Lucineer isn't just spawning assets; he's *welding, riveting, and forging* them in front of the player.

Here is the concrete implementation plan.

---

### 1. UPGRADED COMMAND EXECUTOR (Luau)

The current executor just drops parts into the workspace. The upgraded `CommandExecutor` runs on the **Client** (to manipulate Camera and VFX without server lag) and receives validated build payloads from the Server. It handles staggered animations, industrial sound design, spark particles, and structural welding.

```lua
--!strict
-- Module: CommandExecutor (Client-Side)
local CommandExecutor = {}

local TweenService = game:GetService("TweenService")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Preloaded Assets (Industrial/Scrap Aesthetic)
local VFX_FOLDER = ReplicatedStorage:WaitForChild("LucineerVFX")
local SFX_WELDER = VFX_FOLDER:WaitForChild("SFX_WelderHiss")
local SFX_CLANK = VFX_FOLDER:WaitForChild("SFX_MetalClank")
local PARTICLE_SPARKS = VFX_FOLDER:WaitForChild("SparkEmitter")

-- Camera Tween Config (Subtle focus, doesn't hijack player control entirely)
local CAM_TWEEN_INFO = TweenInfo.new(0.8, Enum.EasingStyle.Quint, Enum.EasingDirection.Out)
local CAM_RETURN_INFO = TweenInfo.new(1.2, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut)

type PartData = {
    name: string,
    size: Vector3,
    cframe: CFrame,
    color: Color3,
    material: Enum.Material,
    shape: string, -- "Block", "Cylinder", "Ball"
    delay: number  -- Stagger delay in seconds
}

type BuildPayload = {
    jobId: string,
    parts: {PartData},
    rootCFrame: CFrame,
    lucineerDialogue: string?
}

local function createBasePart(data: PartData): BasePart
    local part: BasePart
    if data.shape == "Cylinder" then
        part = Instance.new("Part")
        part.Shape = Enum.PartType.Cylinder
    elseif data.shape == "Ball" then
        part = Instance.new("Part")
        part.Shape = Enum.PartType.Ball
    else
        part = Instance.new("Part")
        part.Shape = Enum.PartType.Block
    end
    
    part.Name = data.name
    part.Size = Vector3.zero -- Start at zero for scale-in
    part.CFrame = data.cframe
    part.Color = data.color
    part.Material = data.material
    part.Anchored = true
    part.CanCollide = false -- Prevent physics explosions during assembly
    part.Transparency = 1
    part.CastShadow = false
    
    return part
end

local function triggerAssemblyVFX(part: BasePart)
    -- Sound
    local clank = SFX_CLANK:Clone()
    clank.Parent = part
    clank.PlaybackSpeed = 0.9 + math.random() * 0.3 -- Pitch variation
    clank:Play()
    game:GetService("Debris"):AddItem(clank, 2)

    -- Sparks
    local sparks = PARTICLE_SPARKS:Clone()
    sparks.Parent = part
    sparks:Emit(math.random(8, 15))
    game:GetService("Debris"):AddItem(sparks, 1.5)
end

function CommandExecutor.ExecuteBuild(payload: BuildPayload)
    local model = Instance.new("Model")
    model.Name = "Lucineer_Build_" .. payload.jobId
    model.Parent = workspace:WaitForChild("LucineerBuilds")

    local primaryPart = Instance.new("Part")
    primaryPart.Size = Vector3.new(1,1,1)
    primaryPart.Transparency = 1
    primaryPart.CFrame = payload.rootCFrame
    primaryPart.Anchored = true
    primaryPart.Parent = model
    model.PrimaryPart = primaryPart

    local camera = workspace.CurrentCamera
    local originalCamCFrame = camera.CFrame
    
    -- Calculate bounding box for camera focus
    local focusCFrame = payload.rootCFrame + Vector3.new(15, 10, 15)
    local lookAt = payload.rootCFrame.Position
    local targetCamCFrame = CFrame.lookAt(focusCFrame.Position, lookAt)

    -- Subtle camera nudge to watch the build
    local camTween = TweenService:Create(camera, CAM_TWEEN_INFO, {CFrame = targetCamCFrame})
    camTween:Play()

    -- Staggered Part Assembly
    local weldTarget = primaryPart
    local activeTweens = {}

    for i, partData in ipairs(payload.parts) do
        task.delay(partData.delay, function()
            local part = createBasePart(partData)
            part.Parent = model

            -- Scale and Fade In
            local scaleTween = TweenService:Create(part, TweenInfo.new(0.35, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {
                Size = partData.size,
                Transparency = 0
            })
            
            scaleTween:Play()
            table.insert(activeTweens, scaleTween)

            -- Weld to primary part (Multi-part assembly)
            local weld = Instance.new("WeldConstraint")
            weld.Part0 = weldTarget
            weld.Part1 = part
            weld.Parent = part

            -- VFX triggers slightly after tween starts
            task.delay(0.2, function()
                triggerAssemblyVFX(part)
            end)
        end)
    end

    -- Wait for all animations to finish, then finalize
    task.delay(#payload.parts * 0.1 + 1.5, function()
        -- Play completion sound
        local welder = SFX_WELDER:Clone()
        welder.Parent = model
        welder:Play()
        game:GetService("Debris"):AddItem(welder, 3)

        -- Enable collisions and shadows for the finished build
        for _, descendant in ipairs(model:GetDescendants()) do
            if descendant:IsA("BasePart") then
                descendant.CanCollide = true
                descendant.CastShadow = true
            end
        end

        -- Return camera to player control
        local returnTween = TweenService:Create(camera, CAM_RETURN_INFO, {CFrame = originalCamCFrame})
        returnTween:Play()
    end)
end

return CommandExecutor
```

---

### 2. REAL-TIME BUILD STREAMING (Protocol & Architecture)

Roblox `HttpService` **does not support WebSockets or Server-Sent Events (SSE)**. If you try to hold a connection open, Roblox will time it out or the Worker will hit CPU limits. 

**The Protocol: Chunked HTTP Long-Polling**
1. **Python Processor**: Streams JSON tokens from Qwen3-Coder. As soon as a valid part object is parsed, it pushes it to the Worker.
2. **Cloudflare Worker (Durable Object)**: Acts as a high-speed buffer. It holds an in-memory queue of parts for a specific `jobId`.
3. **Roblox Poller**: Requests chunks of 10-15 parts every 0.8 seconds. 

#### Worker Side (TypeScript / Durable Object)

```typescript
// lucineer-worker.ts
import { DurableObject } from 'cloudflare:workers';

export class LucineerBuildDO extends DurableObject {
  private partQueue: any[] = [];
  private isComplete: boolean = false;
  private dialogueBuffer: string = "";

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    // Python Processor pushes parts here in real-time
    if (url.pathname === '/push' && request.method === 'POST') {
      const data = await request.json() as { part?: any, complete?: boolean, dialogue?: string };
      
      if (data.part) this.partQueue.push(data.part);
      if (data.dialogue) this.dialogueBuffer += data.dialogue;
      if (data.complete) this.isComplete = true;
      
      return new Response('OK', { status: 200 });
    }

    // Roblox Client polls here
    if (url.pathname === '/poll' && request.method === 'GET') {
      const cursor = parseInt(url.searchParams.get('cursor') || '0');
      
      // Grab up to 15 parts per poll to prevent payload bloat
      const chunk = this.partQueue.slice(cursor, cursor + 15);
      const nextCursor = cursor + chunk.length;

      const responsePayload = {
        parts: chunk,
        nextCursor: nextCursor,
        isComplete: this.isComplete && nextCursor >= this.partQueue.length,
        dialogue: this.dialogueBuffer // Send accumulated dialogue for UIManager
      };

      // Clear dialogue buffer once sent to client
      this.dialogueBuffer = ""; 

      return new Response(JSON.stringify(responsePayload), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    return new Response('Not Found', { status: 404 });
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const jobId = url.searchParams.get('jobId');
    if (!jobId) return new Response('Missing jobId', { status: 400 });

    // Route to the specific Durable Object for this build job
    const id = env.LUCINEER_BUILD.idFromName(jobId);
    const stub = env.LUCINEER_BUILD.get(id);
    return stub.fetch(request);
  }
};
```

#### Roblox Poller Side (Luau Snippet)

```lua
-- Module: Poller (Client-Side)
local HttpService = game:GetService("HttpService")
local CommandExecutor = require(script.Parent.CommandExecutor)

local Poller = {}
local WORKER_URL = "https://lucineer-relay.yourdomain.workers.dev/poll"

function Poller.StreamBuild(jobId: string, rootCFrame: CFrame)
    local cursor = 0
    local isComplete = false
    local buildBuffer = {}

    while not isComplete do
        local success, response = pcall(function()
            return HttpService:GetAsync(string.format("%s?jobId=%s&cursor=%d", WORKER_URL, jobId, cursor))
        end)

        if success and response then
            local data = HttpService:JSONDecode(response)
            
            if #data.parts > 0 then
                -- Assign staggered delays for the CommandExecutor
                for i, part in ipairs(data.parts) do
                    part.delay = (i - 1) * 0.12 -- 120ms between each part
                    table.insert(buildBuffer, part)
                end
                
                -- Execute the chunk immediately
                CommandExecutor.ExecuteBuild({
                    jobId = jobId,
                    parts = data.parts,
                    rootCFrame = rootCFrame
                })
                
                cursor = data.nextCursor
            end

            isComplete = data.isComplete
            
            -- Push dialogue to UIManager
            if data.dialogue and data.dialogue ~= "" then
                -- UIManager:AppendDialogue(data.dialogue)
            end
        else
            task.wait(1) -- Backoff on failure
        end
        
        task.wait(0.8) -- Polling interval (800ms)
    end
end

return Poller
```

---

### 3. PERFORMANCE BUDGET (10 Concurrent Players)

If 10 players say "build me a castle" at the same time, a naive implementation will crash the Roblox server and exhaust Cloudflare limits. Here is the strict performance budget and mitigation strategy.

#### A. Roblox Engine Budget
*   **Part Limit per Server**: 15,000 total parts. (Roblox handles up to ~30k, but physics and rendering degrade heavily past 15k unoptimized parts).
*   **Budget per Player**: **1,500 parts max per build.**
*   **Physics Budget**: 0 unanchored parts during build. All parts are `Anchored = true` while building.

**Optimization Tactics:**
1.  **MeshParts over Unions/Parts**: The Python processor must be prompted (via Qwen3-Coder) to use `MeshPart` with `MeshId` and `TextureId` for complex shapes (e.g., gears, hulls) instead of combining 50 small blocks. One MeshPart = 1 part count.
2.  **Aggressive Welding**: The `CommandExecutor` uses `WeldConstraint`. Once a build is complete, the entire model is treated as a single rigid body by the physics engine if unanchored, drastically reducing physics calculation overhead.
3.  **StreamingEnabled**: Must be turned **ON** in Workspace properties. Set `StreamingMinRadius` to 128 and `StreamingTargetRadius` to 256. Players only render the builds they are looking at.
4.  **Shadow & Collision Culling**: Detail parts (screws, small plates) must have `CastShadow = false` and `CanCollide = false`. Only structural parts get collisions.

#### B. Cloudflare Worker & Durable Object Budget
*   **Subrequest Limit**: 1,000 per invocation. (Not an issue for our polling model).
*   **CPU Time**: 30ms per request (Free) / 30s (Paid). Our DO poll logic takes <2ms.
*   **DO Memory Limit**: 128MB per Durable Object.
*   **Concurrent Connections**: 1,024 per DO.

**Handling Rate Limits & Concurrency:**
1.  **DO Sharding by Job, Not Player**: The DO is keyed by `jobId`, not `userId`. This prevents a single player's DO from bottlenecking if they spam requests.
2.  **In-Memory Queue vs D1 Storage**: The active build stream uses the DO's **in-memory array** (`this.partQueue`). We do *not* write every single part to D1 or DO Storage during the stream. Writing 1,500 parts to D1 sequentially will hit D1 write limits and spike latency. 
    *   *Rule*: Stream lives in RAM. Only the *finalized* build metadata is saved to D1 `build_history` upon completion.
3.  **Poll Throttling**: The Roblox client polls every 800ms. If the client detects the worker returning empty chunks (`#data.parts == 0`), it exponentially backs off (800ms -> 1.2s -> 2.0s) to save Worker reads.
4.  **DeepInfra Rate Limits**: DeepInfra limits concurrent requests. The Python processor must use an `asyncio.Semaphore(5)` to ensure we never send more than 5 concurrent generation requests to the 5-model pipeline, queuing the rest locally in Python before pushing to the Worker.

#### C. The "Scrap Aesthetic" Advantage
Magnus's design DNA (industrial, scrap, SE Alaska fishing) actually *helps* performance. Scrap builds are inherently modular and blocky. We don't need smooth, high-poly organic curves. We can use low-poly MeshParts, heavy use of `SurfaceAppearance` (PBR textures) on simple blocks to make them look like rusted iron and weathered wood, keeping the part count incredibly low while maintaining a world-class visual fidelity.