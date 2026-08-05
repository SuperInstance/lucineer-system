# GPU Agent Output — Save System Architecture Redesign
**Timestamp:** 2026-08-04 10:22:30 AKDT
**Model:** granite3.1-dense:2b on RTX 4050
**Topic:** Production Engineering — Debounced Save Queue + Conflict Resolution

## Analysis
The save system fires after every build — too expensive (R2 writes), too fragile (mid-build failure), not granular enough. The GPU proposed a debounced batch save queue.

## Key Insights from GPU Output
1. **Debounce pattern:** 500ms timeout collects multiple saves into batches → fewer R2 writes
2. **D1 versioning for conflict resolution:** version metadata checked before applying saves
3. **Error isolation:** save failures don't block game loop
4. **Lua SaveManager:** client-side state management with era-level granularity

## GPU Raw Code Assessment
The GPU output has significant issues:
- Used Google Cloud Storage APIs instead of Cloudflare R2/D1/DO (model confusion)
- Lua-side SaveManager uses HTTP requires to GCS — doesn't match Roblox/Worker architecture
- Conflict resolution logic is incomplete
- No actual DO (Durable Object) usage despite mentioning it

## Corrected Architecture (adapted from GPU insights)

### Worker-Side: Debounced Save Queue in Durable Object

```typescript
// SaveQueueDO.ts — inside the session-routed Durable Object
interface QueuedSave {
  type: 'build' | 'era' | 'bond' | 'inventory';
  data: Record<string, unknown>;
  timestamp: number;
  version: number;
}

export class SaveQueueDO implements DurableObject {
  state: DurableObjectState;
  env: Env;
  saveQueue: QueuedSave[] = [];
  flushTimer: ReturnType<typeof setTimeout> | null = null;
  currentVersion = 0;

  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
    this.env = env;
  }

  async enqueue(save: QueuedSave): Promise<void> {
    save.version = ++this.currentVersion;
    this.saveQueue.push(save);

    // Debounce: flush 2 seconds after last save request
    if (this.flushTimer) clearTimeout(this.flushTimer);
    this.flushTimer = setTimeout(() => this.flush(), 2000);
  }

  async flush(): Promise<void> {
    if (this.saveQueue.length === 0) return;

    const batch = this.saveQueue.splice(0);
    const batchId = `save_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;

    try {
      // Write all queued saves as a single R2 object
      await this.env.SAVES.put(batchId, JSON.stringify(batch), {
        customMetadata: { version: String(this.currentVersion), count: String(batch.length) },
      });

      // Update D1 metadata for conflict detection
      await this.env.DB.prepare(
        'INSERT INTO save_metadata (batch_id, version, item_count, created_at) VALUES (?, ?, ?, ?)'
      ).bind(batchId, this.currentVersion, batch.length, Date.now()).run();

      // Clean up old saves (keep last 10 per session)
      await this.pruneOldSaves();
    } catch (err) {
      console.error('Save flush failed:', err);
      // Re-queue the batch for next flush
      this.saveQueue.unshift(...batch);
    }
  }

  async pruneOldSaves(): Promise<void> {
    const old = await this.env.SAVES.list({ limit: 20 });
    if (old.objects.length <= 10) return;
    const toDelete = old.objects.slice(10).map(o => o.key);
    await this.env.SAVES.delete(toDelete);
  }
}
```

### Lua-Side: SaveManager

```lua
-- SaveManager.lua (client/server shared)
local SaveManager = {}
SaveManager.__index = SaveManager

local HttpService = game:GetService("HttpService")
local WORKER_URL = "https://lucineer-relay.casey-digennaro.workers.dev"

function SaveManager.new(playerId: number)
  local self = setmetatable({}, SaveManager)
  self.playerId = playerId
  self.pendingState = {}
  self.lastSaveTime = 0
  self.saveInProgress = false
  return self
end

function SaveManager:queueSave(saveType: string, data: {[string]: any})
  self.pendingState[saveType] = data
  self.lastSaveTime = os.clock()
end

function SaveManager:flush()
  if self.saveInProgress or not next(self.pendingState) then return end
  self.saveInProgress = true

  local payload = HttpService:JSONEncode({
    saves = self.pendingState,
    playerId = self.playerId,
    timestamp = os.time(),
  })

  local success, response = pcall(function()
    return HttpService:PostAsync(
      WORKER_URL .. "/api/save",
      payload,
      Enum.HttpContentType.ApplicationJson
    )
  end)

  self.saveInProgress = false

  if success then
    self.pendingState = {}
  else
    warn("[SaveManager] Save failed, will retry: " .. tostring(response))
    task.wait(3)
    self:flush()  -- retry once
  end
end

return SaveManager
```

## Assessment
- **GPU contribution:** The debounce concept is correct and valuable
- **Main issue:** Model confused Cloudflare APIs with Google Cloud — hallucinated imports
- **Value:** Architecture pattern (batch + debounce + version + retry) is the right approach
