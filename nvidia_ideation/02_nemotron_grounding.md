---

## GROUNDED ASSESSMENT: MOLT + SLACKWATER

### REALITY CHECK FIRST

| Constraint | Impact |
|------------|--------|
| **Roblox = Luau VM** | No Python, no Ray, no vLLM, no PyTorch *inside* the game server. All NVIDIA stack runs **externally** via HTTP/gRPC. |
| **MOLT is a training framework** | It produces *checkpoints/policies*. It is not an inference server. You don't "call MOLT at runtime." You call **vLLM/TensorRT-LLM** serving a MOLT-trained model. |
| **Nemotron-Ultra-550B** | 550B params = **~8×H100 (80GB)** for FP8 inference. DeepInfra bills ~$3.50/hr per 8×H100 node. You cannot call this per-NPC per-tick. |
| **ACE for Games** | Designed for **Unreal/Unity** (C++/C# SDKs). No Roblox/Luau SDK. You get: Riva ASR/TTS (gRPC), Audio2Face (USD stream), Nemotron 3B (local). You wrap these yourself. |
| **NeMoClaw** | Runtime orchestrator for ACE microservices. Runs on Linux containers. Not on Roblox servers. |
| **MOLT Codebase** | 9.2K LOC = `molt/` (Env, ChatAgent, Trainer, RewardFn). Key files: `molt/envs/base.py`, `molt/agents/chat_agent.py`, `molt/trainers/grpo_trainer.py`. It expects **Gymnasium** envs. |

---

## 1. THREE MOST IMMEDIATELY BUILDABLE (30 DAYS)

These use **inference only** (no RL training loops), **existing Nemotron on DeepInfra**, and **ACE via gRPC** you wrap in a Python FastAPI gateway.

---

### 🥇 #1: REAL-TIME PLAYER-ADAPTIVE ERA 1 NPC TRADERS (SIMPLIFIED)

**What actually ships in 30 days:** Dynamic pricing + personalized dialogue + ACE voice. **No RL training loop.** Contextual bandit via prompt engineering + lightweight embedding store.

#### ARCHITECTURE

```
┌─────────────┐     HTTPS/JSON      ┌──────────────────┐     gRPC      ┌─────────────────┐
│  Roblox     │ ──────────────────▶ │  Python Gateway  │ ────────────▶ │  NVIDIA Riva    │
│  (Luau)     │  Player context,    │  (FastAPI)       │  TTS Request  │  TTS (ACE)      │
│  33 modules │  inventory, history │                  │               │  (NeMoClaw)     │
└─────────────┘                     │  • Nemotron      │               └────────┬────────┘
      ▲                             │    Ultra-550B    │                        │
      │  Audio bytes +              │  (DeepInfra)     │                        ▼
      │  Lip-sync JSON              │  • Embedding     │               ┌─────────────────┐
      │                             │    cache (Redis) │               │  Audio2Face     │
      └─────────────────────────────│  • Bandit policy │               │  (blendshapes)  │
                                    │    (LinUCB)      │               └────────┬────────┘
                                    └──────────────────┘                        │
                                                                                 ▼
                                                                        ┌─────────────────┐
                                                                        │  Roblox Client  │
                                                                        │  (Animation     │
                                                                        │   Controller)   │
                                                                        └─────────────────┘
```

#### DATA FLOW (PER INTERACTION)

1. **Roblox → Gateway** (`POST /npc/interact`)
   ```json
   {
     "npc_id": "dockhand_01",
     "player_id": "user_12345",
     "era": 1,
     "player_state": {
       "inventory": {"salmon": 47, "net_basic": 1, "coins": 1200},
       "recent_actions": ["fish_salmon", "sell_salmon", "repair_net"],
       "playstyle_embedding": [0.12, -0.45, ...]  // 384-dim from all-MiniLM-L6-v2
     },
     "npc_state": {
       "stock": {"net_reinforced": 3, "bait_premium": 12},
       "base_prices": {"net_reinforced": 800, "bait_premium": 45},
       "relationship": 0.3
     }
   }
   ```

2. **Gateway → Nemotron-Ultra-550B (DeepInfra)** — Single prompt, structured output:
   ```python
   # Gateway prompt template (vLLM chat template)
   SYSTEM = """You are Dockhand Elias, 52, Alaskan fisherman. 
   Adjust prices & dialogue for THIS player. Output JSON only:
   {"price_adjustments": {"item_id": multiplier}, "dialogue": "string", "relationship_delta": float}"""
   
   USER = f"""Player profile: {json.dumps(player_state)}
   Your stock: {json.dumps(npc_state['stock'])}
   Base prices: {json.dumps(npc_state['base_prices'])}
   Relationship: {npc_state['relationship']}
   Recent history: {player_state['recent_actions'][-5:]}"""
   ```

3. **Nemotron returns** (≈800ms on DeepInfra):
   ```json
   {
     "price_adjustments": {"net_reinforced": 0.78, "bait_premium": 1.0},
     "dialogue": "Ay, the salmon run's early this year. That net of yours won't last the season — take the reinforced for 624. Fair price for a worker.",
     "relationship_delta": 0.05
   }
   ```

4. **Gateway → Riva TTS** (gRPC, `SynthesizeOnline`):
   ```python
   # Riva TTS request
   tts_request = riva_tts_pb2.SynthesizeOnlineRequest(
       text=dialogue,
       voice_name="English-US-Male-1",  # Pre-trained fisherman voice
       sample_rate_hz=22050,
       language_code="en-US"
   )
   # Stream audio chunks back to Roblox
   ```

5. **Gateway → Audio2Face** (gRPC, `PushAudioStream`):
   ```python
   # Get blendshape weights for lip-sync
   a2f_request = a2f_pb2.PushAudioStreamRequest(audio_data=audio_bytes)
   blendshapes = a2f_stub.PushAudioStream(a2f_request)  # 51 blendshapes @ 60fps
   ```

6. **Gateway → Roblox** (single response):
   ```json
   {
     "prices": {"net_reinforced": 624, "bait_premium": 45},
     "dialogue": "Ay, the salmon run's early...",
     "audio_base64": "...",           // Riva TTS output (opus)
     "blendshapes": [[0.1, 0.0, ...]], // 51 floats × 60 frames
     "relationship": 0.35
   }
   ```

#### NVIDIA TOOLS USED
| Tool | How | Cost/Call |
|------|-----|-----------|
| **Nemotron-Ultra-550B (DeepInfra)** | Chat completion, JSON mode | ~$0.008/1K tokens |
| **Riva TTS** | gRPC streaming, custom voice | Free (self-hosted) or $0.0004/sec (NGC) |
| **Audio2Face** | Blendshape generation | Free (self-hosted) |
| **NeMoClaw** | Orchestrates Riva + A2F containers | Ops overhead only |

#### MOLT CONNECTION? **None at runtime.** MOLT used *offline* to train the **LinUCB bandit policy** that initializes `price_adjustments` priors. See "6-month project" below.

#### LUau INTEGRATION (Roblox)
```lua
-- ReplicatedStorage/Shared/NPCTraderClient.luau
local HttpService = game:GetService("HttpService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local AudioPlayer = require(ReplicatedStorage.Shared.AudioPlayer)
local LipSync = require(ReplicatedStorage.Shared.LipSync)

local GATEWAY_URL = "https://slackwater-ai-gateway.fly.dev/npc/interact"

function InteractWithTrader(npcId: string)
    local playerState = PlayerStateModule:GetCompressedState() -- Your existing 33 modules
    local response = HttpService:RequestAsync({
        Url = GATEWAY_URL,
        Method = "POST",
        Headers = {["Content-Type"] = "application/json"},
        Body = HttpService:JSONEncode({npc_id = npcId, player_id = Players.LocalPlayer.UserId, ...})
    })
    
    local data = HttpService:JSONDecode(response.Body)
    -- Apply prices
    TraderUI:SetPrices(data.prices)
    -- Play voice + lip-sync
    AudioPlayer.PlayStream(data.audio_base64)
    LipSync.ApplyBlendshapes(data.blendshapes, npcId)
    -- Update relationship
    RelationshipModule:Update(npcId, data.relationship)
end
```

#### WHY THIS WORKS IN 30 DAYS
- No training loop. Pure inference.
- Uses your existing `PlayerStateModule` (33 modules → compressed JSON).
- ACE stack runs in 2 containers (Riva + A2F) on Fly.io/RunPod.
- Nemotron on DeepInfra = zero GPU ops for you.
- Lip-sync blendshapes map to Roblox `FaceControls` (51 → 50 ARKit blendshapes).

---

### 🥈 #7: SERVER-DRIVEN ERA ADVANCEMENT CO-PILOTS

**What ships:** Weekly server analysis → era path recommendation → town hall speech (voice + text). **Batch job, not real-time.**

#### ARCHITECTURE

```
┌─────────────┐     HTTPS      ┌──────────────────┐     HTTPS      ┌─────────────────┐
│  Roblox     │ ─────────────▶ │  Python Gateway  │ ────────────▶ │  Nemotron-Ultra │
│  Game Server│  Server stats  │  (FastAPI +      │  Analysis +    │  550B (DeepInfra)│
│  (Luau)     │  (DataStore)   │   Celery Beat)   │  Speech Gen    │                 │
└─────────────┘                 │                  │                └────────┬────────┘
      ▲                         │  • SQLite/      │                     │
      │  Era proposal +         │    DuckDB       │                     ▼
      │  Speech audio           │  • Weekly cron  │            ┌─────────────────┐
      └─────────────────────────│    (Sunday 03:00)│            │  Riva TTS       │
                                └──────────────────┘            └────────┬────────┘
                                                                          │
                                                                          ▼
                                                                 ┌─────────────────┐
                                                                 │  Roblox Client  │
                                                                 │  Town Hall UI   │
                                                                 └─────────────────┘
```

#### DATA FLOW (WEEKLY CRON)

1. **Roblox → Gateway** (DataStore export, ~50KB/server):
   ```lua
   -- ServerScriptService/Analytics/WeeklyExport.luau
   local DataStoreService = game:GetService("DataStoreService")
   local AnalyticsStore = DataStoreService:GetDataStore("WeeklyAnalytics")
   
   function ExportWeeklyStats()
       local stats = {
           server_id = game.JobId,
           era_distribution = EraModule:GetServerDistribution(), -- {era1=45, era2=30, ...}
           recipe_usage = CraftingModule:GetRecipeFrequency(),   -- {recipe_id: count}
           energy_mix = PowerGridModule:GetEnergyMix(),          -- {solar=0.3, coal=0.7}
           player_count = #Players:GetPlayers(),
           playstyle_clusters = PlaystyleAnalyzer:GetClusters()  -- Your existing vibe-coding data
       }
       AnalyticsStore:SetAsync("weekly_" .. os.date("%Y-%m-%d"), stats)
   end
   ```

2. **Gateway (Celery task)** loads all servers → DuckDB → aggregates → **Nemotron prompt**:
   ```python
   # tasks/era_copilot.py
   @celery.task
   def generate_era_proposal():
       df = duckdb.query("SELECT * FROM weekly_analytics WHERE week = ?", [last_week]).df()
       
       # Aggregate server-wide signals
       signal = f"""
       SERVER POPULATION: {df['player_count'].sum()}
       ERA DISTRIBUTION: {df['era_distribution'].sum().to_dict()}
       TOP RECIPES: {df['recipe_usage'].sum().nlargest(10).to_dict