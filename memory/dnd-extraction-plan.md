# D&D System Extraction Plan — Technical Assessment

## Which Features Should Be Extracted and Built Into the Fleet NOW

### Source: ai_society_dnd Layer 3 Architecture + Advanced Features

The D&D system was far more than a game simulator. It was a laboratory for multi-agent coordination, cognitive health monitoring, and adaptive model routing. The architecture documents (LAYER3_ARCHITECTURE.md: ~6,000 words; ADVANCED_FEATURES.md: ~2,550 lines of documented Python) describe systems that solve problems the fleet is facing right now.

### Tier 1: Extract Immediately (This Week)

#### 1.1 — Model Routing System (model_routing.py → casting-call)

**What it does:** Analyzes task complexity on a 5-level scale (TRIVIAL → EXPERT) and routes to the appropriate model. Tracks cost savings (90% on simple tasks, 70% on moderate).

**Why extract NOW:** The fleet currently has TOOLS.md with a model routing strategy that is *manually executed* — the main agent reads the table and decides. The D&D system's `ComplexityAnalyzer` and `ModelRouter` automate this. The casting-call system (the fleet's model dispatch) is the natural home.

**Integration path:**
- Port `ComplexityAnalyzer.analyze()` into a Cloudflare Worker
- Feed it the task description + context (options count, consequence flag, latency constraint)
- It returns a complexity level → maps to the TOOLS.md model table
- The casting-call worker dispatches to DeepSeek-Flash (TRIVIAL/SIMPLE), GLM-5.2 (MODERATE), DeepSeek-Pro (COMPLEX), Claude Opus (EXPERT)
- **Estimated effort:** 2 days. The Python is clean, the logic is self-contained.

#### 1.2 — Pathology Detection System (pathology_detection.py → agent health monitoring)

**What it does:** Monitors for 6 cognitive pathologies: memory drift, identity fragmentation, memory bloat, repetition syndrome, decision paralysis, temporal confusion. Produces a 0-100 health score with auto-interventions for severity ≥ 2.

**Why extract NOW:** The fleet's agents (Lucineer, Wesley, the Tap) are long-running entities with persistent identity. Nothing currently monitors whether they're drifting from their core personality, accumulating bloat in their memory files, or stuck in repetition loops. This is a safety system the fleet needs.

**Integration path:**
- Port `PathologyMonitor` as a heartbeat check that runs against agent memory files
- Identity coherence: compare recent outputs against AGENTS.md/SOUL.md identity statements using embedding similarity
- Memory bloat: count memory files, flag when low-importance entries exceed 40%
- Repetition syndrome: track action history, flag 3+ identical actions in a 10-action window
- **The 0-100 health score** becomes a fleet dashboard metric, reported alongside agent status
- **Estimated effort:** 3 days. Requires adapting from character-specific to agent-general.

### Tier 2: Extract This Month (Weeks 2-4)

#### 2.1 — Digital Twin Learning (digital_twin.py → agent-watching-human)

**What it does:** Observes human behavior (decisions, timing, hesitation, risk tolerance, social patterns) and trains a predictive model that can simulate the human's choices.

**Why extract:** Lucineer's mandate is to learn Casey's patterns. The D&D system's `BehaviorCapture` and `BehaviorAnalyzer` are exactly the right primitives: record decisions, analyze patterns, build a risk profile, train a twin. The "fill in for absent players" use case maps directly to "answer messages the way Casey would when Casey is asleep."

**Integration path:**
- `BehaviorCapture` wraps around Lucineer's session logs
- `BehaviorAnalyzer` produces a decision-pattern profile
- The twin predicts how Casey would respond to a given message
- **Critical safety constraint:** twin predictions are marked as such, never impersonating Casey directly
- **Estimated effort:** 1 week. The capture layer is straightforward; the analysis needs tuning.

#### 2.2 — Escalation Trigger Engine (LAYER3 → fleet escalation protocol)

**What it does:** Determines when to escalate from mechanical handling → small model → big model → human. Based on novelty, stakes, time pressure, and confidence.

**Why extract:** The fleet needs this for message handling. A Telegram message at 03:00 with "hey" is TRIVIAL (mechanical response). A message asking "should I commit this rewrite?" is COMPLEX (big model). A message at 23:00 saying "the server is down" is Level 3 (human). The escalation engine formalizes what the main agent currently does by intuition.

**Integration path:**
- Port `EscalationEngine.should_escalate()` into the message-handling pipeline
- Novelty: cosine distance of incoming message from handled-message history (vector DB query)
- Stakes: keyword/intent classification (commit, deploy, delete, send = high stakes)
- Time pressure: detect urgency markers
- **Estimated effort:** 3 days. Clean logic, needs only the novelty scoring (which requires vector DB access).

#### 2.3 — Metrics Dashboard (metrics_dashboard.py → fleet observability)

**What it does:** Collects metrics across character/session/system/model dimensions. Tracks memory count, identity coherence, drift score, model routing decisions, cost per decision, latency. Alerting on threshold breaches.

**Why extract:** The fleet has no observability layer. We don't know how many tokens we're burning, which models are most cost-effective, whether agents are healthy, or when interventions are needed. This is the fleet's missing nervous system.

**Integration path:**
- Cloudflare Worker that collects metrics from agent activity logs
- D1 database for time-series storage
- Simple web dashboard served from Pages (or canvas)
- Alerts pushed to Telegram
- **Estimated effort:** 1 week. Mostly plumbing.

### Tier 3: Adapt Later (Months 2-3)

#### 3.1 — Advanced Consolidation (advanced_consolidation.py → memory maintenance)

**What it does:** Four strategies for memory compression: cluster-based (group similar memories), adaptive (learn optimal timing), incremental (continuous small batches), cross-memory inference (derive new knowledge from patterns).

**Why defer:** The fleet's memory system (MEMORY.md + daily files) is still small enough that manual curation works. But as the daily files accumulate, consolidation becomes necessary. The D&D system's adaptive consolidation — which learns when to consolidate based on retrieval quality — is the right approach. Just not urgent yet.

**Trigger for extraction:** When daily memory files exceed 500 entries or MEMORY.md exceeds 50KB.

#### 3.2 — Perception Batching Engine

**What it does:** Processes all agents' perceptions in a single batched pass rather than individually.

**Why defer:** The fleet doesn't yet have enough concurrent agents to justify batching. When the fleet exceeds 5 simultaneously-active agents, revisit this.

### What NOT to Extract

- **LoRA Training Pipeline** — Fleet agents use API-based models, not local fine-tunes. Wesley's LoRA training is a special case, not a general pattern. Skip until local model hosting becomes standard.
- **Combat/Social/Exploration Bot Framework** — These are D&D-specific. The patterns (perceive → decide → execute → escalate) are useful conceptually but the code is too domain-specific.
- **Multi-window Chat Interface** — LucidDreamer's streaming interface supersedes this. The MUD-style feed concept is interesting but the fleet's communication is Telegram-native, not chatroom-native.

### Extraction Priority Matrix

| Feature | Value | Effort | Priority |
|---------|-------|--------|----------|
| Model Routing | Critical (cost optimization) | 2 days | **TIER 1** |
| Pathology Detection | Critical (agent safety) | 3 days | **TIER 1** |
| Escalation Engine | High (message handling) | 3 days | **TIER 2** |
| Digital Twin | High (Lucineer mandate) | 1 week | **TIER 2** |
| Metrics Dashboard | High (observability) | 1 week | **TIER 2** |
| Advanced Consolidation | Medium (future-proofing) | 1 week | TIER 3 |
| Perception Batching | Low (not needed yet) | 1 week | TIER 3 |

### The Big Picture

The D&D system was building a self-improving society of AI agents with personality persistence, health monitoring, cost-optimized routing, and human-learning capabilities. That's exactly what the fleet is becoming. The code is 6,725 lines of production Python that solves problems we're solving right now — but it's written for D&D characters, not fleet agents.

The extraction work is translation, not invention. The logic transfers. The domain changes. Model routing becomes casting-call. Pathology detection becomes agent health. Digital twin becomes Lucineer's learning layer. The D&D system was a prototype for the fleet, disguised as a game.

*Extract the organs. Leave the dice.*
