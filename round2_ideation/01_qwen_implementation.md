# 01 Qwen Implementation — Qwen3.5-397B



Here is the engineering specification for the Lucineer RL Agent Pipeline. This is designed for production robustness, cost efficiency, and rapid iteration.

### 1. Training Data Pipeline Architecture
**Pattern:** Offline RL with Online Fine-Tuning (MOLT architecture).
We do not train on the game server. We train on a dedicated GPU cluster using data collected from production.

**Flow:**
1.  **Game Client (Roblox Lua):** Emits `AgentInteractionEvent` via `HttpPost` to a ingestion endpoint.
2.  **Ingestion Service (FastAPI/Go):** Validates schema, adds server-side timestamp, pushes to **Kafka** topic `raw-agent-telemetry`.
3.  **Preprocessing Worker (Python):** Consumes Kafka.
    *   Joins with `PlayerSessionTable` (for satisfaction metrics).
    *   Joins with `GameStateLog` (for recipe correctness/stability).
    *   Calculates dense rewards (see Q5).
    *   Writes **Parquet** files to S3 (`s3://lucineer-rl-data/train/{date}/{episode_id}.parquet`).
4.  **Trainer (Ray RLlib / PPO):**
    *   Loads batches from S3.
    *   Updates Policy Network (LoRA weights on top of Nemotron/Llama base).
    *   Pushes new weights to **Model Registry**.
5.  **Inference Service (vLLM):**
    *   Polls Model Registry.
    *   Hot-swaps weights for live NPCs.

### 2. Reward Signal Collection (Roblox Instrumentation)
Do not trust the client. All reward-critical logic must be validated server-side.

**Lua (Client/Server Script):**
```lua
local HttpService = game:GetService("HttpService")
local ENDPOINT = "https://api.lucineer.com/v1/telemetry"

local function logAgentEvent(agentId, playerId, eventType, metadata)
    -- Sanitize PII
    local payload = {
        agent_id = agentId,
        player_hash = hash(playerId), 
        event_type = eventType, -- "dialogue_start", "item_given", "task_complete"
        timestamp = os.time(),
        session_id = game:GetService("RunService"):IsServer() and sessionId or nil,
        metadata = metadata -- { recipe_id = 123, duration_ms = 500 }
    }
    
    -- Fire and forget, do not yield game thread
    spawn(function()
        HttpService:PostAsync(ENDPOINT, HttpService:JSONEncode(payload))
    end)
end
```

**Data Schema (Ingestion):**
```json
{
  "trace_id": "uuid-v4",
  "agent_id": "npc_blacksmith_01",
  "player_hash": "sha256(...)",
  "episode_id": "session-12345",
  "state_vector": [0.1, 0.5, ...], // Optional: encoded game state
  "action_taken": "give_item_iron_sword",
  "reward_signals": {
    "task_completion": 1.0,
    "time_delta_ms": 4500,
    "player_retention_min": 15,
    "resource_cost": 50
  }
}
```

### 3. Minimal Viable Experiment (MVE)
**Scope:** "The Quest Giver"
*   **Agent:** 1 NPC in a private server.
*   **Task:** Give the player the correct item requested in dialogue.
*   **State:** Player dialogue input + Inventory state.
*   **Action:** Select item from inventory to give.
*   **Reward:** Binary (Correct Item = +1, Wrong Item = -1) - (Time Taken * 0.01).
*   **Success Criteria:** Agent achieves >90% accuracy over 100 episodes without human hard-coding.
*   **Why:** Proves the RL loop (Data -> Reward -> Update -> Deploy) without needing complex 3D navigation or multi-agent coordination.

### 4. Infrastructure: DeepInfra vs. Self-Hosted vLLM
**Verdict:** You need **Self-Hosted vLLM** for the RL loop. DeepInfra is for fallback/chat only.

| Feature | DeepInfra API | Self-Hosted vLLM (A10G/A100) |
| :--- | :--- | :--- |
| **Use Case** | Baseline Chat, Non-RL NPCs | RL Inference & Training |
| **Latency** | High (Cold starts, queue) | Low (Persistent context) |
| **Gradients** | No (Black box) | **Yes (Required for PPO/DPO)** |
| **Cost** | ~$0.20 / 1M tokens | ~$1.50 / hr (A10G) |
| **Custom Ops** | None | Custom Reward Heads |

**Cost Estimate:**
*   **DeepInfra:** If you have 10k DAU interacting with agents, token costs will spike to **$2k-$5k/mo**.
*   **vLLM Cluster:** 2x A10G instances for inference + 1x A100 for training. Fixed cost **~$1.5k/mo**.
*   **Decision:** Host vLLM on Kubernetes (EKS/GKE). Use DeepInfra only for burst capacity or non-critical background NPCs.

### 5. Reward Function Pseudocode
This implements the 7 signals from your findings, normalized to prevent one signal from dominating.

```python
class CompositeRewardFn:
    def __init__(self):
        # Weights tuned via grid search in MVE
        self.w = {
            'stability': 0.1,    # Server FPS impact
            'correctness': 0.4,  # Recipe/Quest logic
            'satisfaction': 0.2, # Player thumbs up / session length
            'cooperation': 0.1,  # Helped other agents?
            'novelty': 0.05,     # Used unique dialogue path
            'efficiency': 0.1,   # Resource cost
            'speed': 0.05        # Task completion time
        }
    
    def compute(self, episode_data: dict) -> float:
        r_total = 0.0
        
        # 1. Correctness (Binary or F1 Score)
        r_correct = 1.0 if episode_data['item_given'] == episode_data['item_requested'] else -1.0
        
        # 2. Speed (Normalized against avg time)
        avg_time = 5000 # ms
        r_speed = np.clip(1.0 - (episode_data['duration_ms'] / (avg_time * 2)), 0, 1)
        
        # 3. Satisfaction (Proxy: Did player stay in zone?)
        r_sat = 1.0 if episode_data['player_retention_min'] > 5 else 0.0
        
        # 4. Efficiency (Resource Cost Penalty)
        r_eff = -1.0 * (episode_data['resource_cost'] / 100.0)
        
        # Weighted Sum
        r_total += (self.w['correctness'] * r_correct)
        r_total += (self.w['speed'] * r_speed)
        r_total += (self.w['satisfaction'] * r_sat)
        r_total += (self.w['efficiency'] * r_eff)
        
        # KL Penalty (Prevent drift from base Nemotron policy)
        kl_div = kl_divergence(episode_data['policy_probs'], episode_data['base_probs'])
        r_total -= (0.02 * kl_div) 
        
        return np.clip(r_total, -5.0, 5.0)
```

### 6. Preventing Reward Hacking
Agents will exploit loopholes (e.g., giving the item instantly to maximize speed, ignoring dialogue quality).

1.  **KL Regularization:** (Included in code above). Penalize the policy if it deviates too far from the pre-trained SFT (Supervised Fine-Tuning) model. This keeps the NPC sounding human.
2.  **Adversarial Critic:** Train a second model (the "Critic") specifically to detect unnatural behavior. If the Critic flags an interaction as "bot-like," apply a heavy negative reward, even if the task was completed.
3.  **Human-in-the-Loop (HITL):** Randomly sample 1% of episodes. Send replays to internal QA. If QA rejects it, add that trajectory to a "Negative Buffer" for DPO (Direct Preference Optimization).
4.  **Reward Clipping:** Cap the maximum reward per episode. Prevents an agent from finding a "farmable" action that yields infinite points.
5.  **Multi-Objective Constraints:** Do not optimize for speed if correctness < 95%. Use Constrained PPO (CPPO).

### 7. 2-Week Sprint Plan (Proof-of-Concept)

**Week 1: Instrumentation & Data Loop**
*   **Day 1-2:** Setup vLLM on a single A10G instance. Load Nemotron-4-8B (or Llama-3-8B if license issues).
*   **Day 3:** Implement Roblox `RemoteEvent` telemetry. Verify data hits S3.
*   **Day 4:** Build the `CompositeRewardFn` in Python. Run it against historical logs (if any) or mock data.
*   **Day 5:** Setup Ray RLlib environment. Define the Observation/Action space (Text -> Action ID).
*   **Day 6-7:** **Milestone:** "Data Flowing." Verify you can trigger an event in Roblox and see it in a Parquet file within 60 seconds.

**Week 2: Training & Deployment**
*   **Day 8-9:** Run Offline RL. Train on mock data first to ensure the loop doesn't crash.
*   **Day 10:** Deploy the trained policy to the vLLM instance.
*   **Day 11:** Connect Roblox NPC to the vLLM endpoint (via proxy server for auth).
*   **Day 12:** **Milestone:** "First Learning Step." NPC makes a mistake, gets negative reward, updates weights.
*   **Day 13:** Stress test. 10 concurrent players. Monitor latency (Target: <300ms TTFT).
*   **Day 14:** Demo Review. Show side-by-side of Base Model vs. RL-Tuned Model on the "Quest Giver" task.

**Risks:**
*   **Roblox HTTP Limits:** You may hit rate limits. *Mitigation:* Batch telemetry events (send every 30s, not every event).
*   **Latency:** vLLM might be too slow for real-time dialogue.