# NVIDIA × SLACKWATER — SYSTEMS ARCHITECT SYNERGY ANALYSIS

**Date:** 2026-08-02  
**Perspective:** Systems Architect  
**Objective:** Map NVIDIA's latest AI releases to actionable integration points in the Slackwater project

---

## EXECUTIVE SUMMARY

NVIDIA's 2025-2026 release cycle has produced five technology clusters that directly accelerate Slackwater's design. The most consequential finding is that **NVIDIA has adopted OpenClaw as the canonical agent runtime** — NeMoClaw is literally an OpenClaw wrapper — which means our existing infrastructure is already aligned with NVIDIA's reference architecture. The second major finding is that **MOLT's "agent is the program" paradigm can train our game agents to build better structures through reinforcement learning**, closing the gap between scripted NPC behavior and genuine autonomous construction skill. Finally, **Nemotron 3's hybrid Mamba-Transformer architecture with 1M-token context** solves our most expensive problem: multi-agent coordination over long horizons without goal drift.

---

## 1. NEMO LABS-MOLT: TRAINING GAME AGENTS WITH REINFORCEMENT LEARNING

### What MOLT Is

MOLT (arXiv:2607.21653) is NVIDIA's agentic-first RL training framework — a compact (~9.2K LOC), PyTorch-native system that treats the agent as an ordinary Python program, not a special object. The core thesis: "the agent is the program; the trainer is a single actor; reward is any Python you write." Three components (Ray for placement, vLLM for rollout, FSDP2 for training) connected by one asynchronous loop. No glue layers, no backend abstraction, no registries.

### How It Maps to Slackwater's Agent Collection

Our agent runtime loop (PERCEIVE → THINK → ACT → COMMUNICATE → LEARN) is currently a **constrained inference pipeline** — the agents never actually improve from experience. Each build goes through the 5-model brain pipeline, produces a result, and the only "learning" is storing skills in Vectorize as embeddings for future few-shot retrieval. That's recall, not learning.

MOLT enables a fundamentally different architecture:

**Current:** Agent builds structure → result stored as embedding → future builds retrieve similar patterns  
**With MOLT:** Agent builds structure → RL environment scores the result (structural integrity, material efficiency, aesthetic coherence, player satisfaction) → policy updated → next build is measurably better

### ACTIONABLE: Build a MOLT Training Environment for Slackwater Agents

The agent contract in MOLT is clean — you subclass `Env` or `ChatAgent` and implement `step()`. For Slackwater:

```python
# slackwater_build_env.py — MOLT environment for training build agents
from molt import Env, Result

class SlackwaterBuildEnv(Env):
    """RL environment where agents learn to build structures in Slackwater."""
    
    def __init__(self, era: int, agent_specialization: str):
        self.era = era  # Era 1-7 determines available parts/recipes
        self.agent_specialization = agent_specialization  # "builder", "electrician", "coder"
        self.world_state = None  # Injected from Roblox world snapshot
        self.build_target = None  # What the player requested
        
    def reset(self, seed=None):
        # Generate a build scenario appropriate to era + specialization
        self.build_target = self.sample_build_target()
        self.world_state = self.sample_world_state()
        return self.observe()
    
    def step(self, action):
        # action = natural language build command (the agent's output)
        # Execute in sandboxed Slackwater world simulator
        structure = self.execute_build_command(action, self.world_state)
        
        # Multi-signal reward
        reward = self.compute_reward(structure)
        
        return Result(
            reward=reward,
            observation=self.observe(),
            terminated=self.is_complete(structure),
        )
    
    def compute_reward(self, structure):
        """Multi-dimensional reward shaping for build quality."""
        return (
            self.structural_integrity_score(structure) * 0.3 +    # Physics stability
            self.material_efficiency_score(structure) * 0.2 +     # Minimal waste
            self.era_appropriateness_score(structure) * 0.2 +     # Uses correct era tech
            self.aesthetic_coherence_score(structure) * 0.15 +    # Looks intentional
            self.player_satisfaction_proxy(structure) * 0.15      # Matches request intent
        )
```

**Concrete integration plan:**

1. **Phase 1 — Offline training (pre-deployment):** Train a small model (Nemotron-3-Nano-4B or a fine-tuned Qwen3-4B) on build scenarios using MOLT's SFT → RL pipeline. Use our existing 55+ Vectorize skills as the SFT dataset. The RL environment is a headless Slackwater simulator that scores build outputs.

2. **Phase 2 — Era-specific specialist models:** Train separate LoRA adapters per era. Era 1-2 agents learn mechanical structures (load-bearing walls, gear trains). Era 5-7 agents learn programmatic structures (sensor networks, autonomous factories). Each LoRA is a hot-swappable specialization.

3. **Phase 3 — Live skill discovery:** When an agent discovers a new build pattern in-game (the LEARN step in our loop), feed it back as a new training scenario for the next RL round. This is Voyager-style skill library growth, but with actual policy improvement rather than just embedding storage.

**Infrastructure cost:** MOLT runs on a single H100 for 8B-class models. We can rent H100s on-demand for training runs. The framework's ~9.2K LOC means it's readable enough for our coding agents (Claude Code, KimiCode) to modify without weeks of onboarding.

### The "Agent Is the Program" Paradigm Shift

This is the most architecturally significant concept for Slackwater. Currently, our agents are **prompts** — long instruction strings sent to DeepInfra models. MOLT reframes the agent as a **Python program that calls a model**, where the program logic (perception routing, tool selection, communication protocol) is the agent, and the model is a callable.

This maps to how we should restructure `brain.py`:

```
CURRENT:  player_input → prompt_template → model → parsed_response
MOLT:     player_input → AgentProgram.step(input) → model_call → reward → policy_update
```

The agent program owns its state, its skill library, its conversation history, and its reward signal. The model is a function it calls. This is a cleaner separation of concerns than our current pipeline architecture and makes each agent independently testable, trainable, and deployable.

**Priority: HIGH.** This is the path from "agents that follow instructions" to "agents that get better at building."

---

## 2. NEMOTRON 3 FAMILY: THE AGENT BRAIN UPGRADE

### Current State in Slackwater

Our model routing already uses Nemotron-Ultra-550B on DeepInfra for the coordination path (multi-agent task planning). We also use Nemotron-Content-Safety-3.5 for kid-safe output checking. The rest of the pipeline runs on DeepInfra-routed models (Seed-2.0, Qwen3 family, Hermes).

### What Nemotron 3 Changes

#### Nemotron 3 Ultra 550B (55B active)

| Feature | Slackwater Impact |
|---------|-------------------|
| **1M-token context window** | An agent can hold an entire play session's history — every build, every conversation, every storm, every tide cycle — without context compression or retrieval. This eliminates goal drift in Era 7 autonomous sessions. |
| **5x throughput vs. predecessor** | Our coordination path (currently 10-30s for multi-agent task planning) drops to 2-6s. This makes real-time fleet coordination viable. |
| **30% cost reduction** | Multi-agent workflows generate 15x more tokens than single-turn chat. Nemotron 3 Ultra's token efficiency directly lowers our DeepInfra bill. |
| **PinchBench 91% agent productivity** | This benchmark measures OpenClaw agent performance. Nemotron 3 Ultra is literally optimized for our runtime. |
| **EnterpriseOps-Gym 33% long-horizon planning** | This is the metric that matters for Era 7 — can the agent maintain a coherent build plan across hundreds of steps? 33% is the current frontier for open models. |
| **MOPD (Multi-Teacher On-Policy Distillation)** | 10+ specialized teachers trained on different domains. Our agents could benefit: one teacher for spatial reasoning, one for circuit design, one for code generation. |

#### Nemotron 3 Super 120B (12B active)

This is the model that changes our **economics**. At 12B active parameters with 5x throughput:

- **Replace Seed-2.0-mini for intent parsing** — Super is agentic-trained, not just chat-trained. It understands tool-use intent better than a general model.
- **Run locally on RTX hardware** for low-latency paths. The fast path (template matching, <2s) could run entirely on-device if we deploy to RTX-equipped servers, eliminating the DeepInfra round-trip.
- **NVFP4 native precision** means it runs on Blackwell at 4x the efficiency of FP8 on Hopper. Cost per inference drops dramatically.

### ACTIONABLE: Upgrade the Model Routing Strategy

```
TIER 1 — ON-DEVICE (RTX-class GPU, <500ms)
  Intent Parse:        Nemotron-3-Nano-4B (local)
  Template Match:      Cached Vectorize lookups
  Safety Check:        Nemotron-3.5-Content-Safety (local, 4B)

TIER 2 — FAST CLOUD (DeepInfra, 2-6s)
  Spatial Plan:        Nemotron-3-Super-120B (12B active, 5x throughput)
  Build Commands:      Qwen3-Coder-480B (unchanged — still best for code gen)
  Personality:         Hermes-3-Llama-405B (unchanged — Lucineer's voice)

TIER 3 — DEEP REASONING (DeepInfra, 10-30s)
  Multi-Agent Coord:   Nemotron-3-Ultra-550B (upgraded from current Ultra)
  Long-Horizon Plan:   Nemotron-3-Ultra-550B with 1M context
  Vision/Perception:   Qwen3-VL-235B (unchanged)
```

**Key change:** Add Nemotron-3-Super-120B as the spatial planning model (replacing Qwen3.6-35B on the fast path). Super's LatentMoE calls 4x as many experts at the same compute cost, and its Mamba-2 backbone handles the 1M-token context window that prevents goal drift in long build sessions.

**Priority: MEDIUM-HIGH.** The infrastructure is already in place (DeepInfra routing). This is a model-swap, not an architecture change. Immediate quality and cost improvement.

### The Perception System Mapping

Nemotron 3 Ultra's "graduate-level science, advanced math, visual understanding" directly maps to our perception system:

- **Visual understanding** → Our Qwen3-VL-235B screenshot analysis path can be supplemented with Nemotron-Ultra's own vision capabilities for deeper scene understanding (not just "what's on screen" but "why is the player's gearbox failing")
- **Advanced math** → Era 3-4 agents (Electrician, Logician) need to compute circuit values, gear ratios, and logic gate truth tables. Nemotron-Ultra's math reasoning is state-of-the-art for open models.
- **Graduate-level science** → The Coder agent's "deep dive" lessons (real Arduino C++, real circuit design) require a model that actually understands the physics. Nemotron-Ultra can explain why a particular transistor choice matters, not just generate code that compiles.

### ACTIONABLE: Nemotron-Ultra as the Teacher Agent Brain

Our teacher agents (March, Ferro, Cipher) currently share the same model pipeline as builder agents. They should use Nemotron-3-Ultra exclusively — the 1M context window means a teacher can hold an entire curriculum in context, and the MOPD training means it's already been distilled from multiple domain experts.

```
Teacher Agent Routing:
  March (Era 1-2):   Nemotron-3-Ultra — mechanical engineering, material science
  Ferro (Era 3-4):   Nemotron-3-Ultra — electrical engineering, control theory  
  Cipher (Era 5-7):  Nemotron-3-Ultra — computer science, distributed systems
```

**Priority: MEDIUM.** Improves educational depth without infrastructure change.

---

## 3. NVIDIA AGENT TOOLKIT + NEMOCLAW RUNTIME

### The OpenClaw Connection

This is the most strategically significant finding of this analysis.

**NeMoClaw IS OpenClaw.** NVIDIA's NeMoClaw is an open-source reference stack that wraps OpenClaw in a secure runtime (OpenShell) and pairs it with Nemotron models. The documentation literally says: `openshell sandbox create --remote spark --from openclaw` — one command, and any OpenClaw agent runs in a sandboxed environment.

This means:
1. **Our existing OpenClaw-based agent runtime is already the NVIDIA reference architecture.** We are not using a "competitor" or "alternative" to NeMoClaw — we are using the same base layer.
2. **OpenShell is available to us now.** We can add NVIDIA's sandboxing, policy engine, and privacy router to our agent deployment without changing our agent code.
3. **The NVIDIA ecosystem is building tools FOR OpenClaw.** Every improvement NVIDIA makes to NeMoClaw's orchestration, memory, or tool-use flows downstream to us.

### NeMoClaw vs. Our Current Runtime

| Component | Our Current Stack | NeMoClaw Stack | Action |
|-----------|------------------|----------------|--------|
| Agent harness | OpenClaw | OpenClaw (same) | No change needed |
| Model routing | DeepInfra MCP (custom) | Privacy Router (local/frontier split) | **Adopt Privacy Router pattern** |
| Sandboxing | None (agents run on host) | OpenShell (Landlock + seccomp isolation) | **Add for production safety** |
| Content safety | Nemotron-Content-Safety-3.5 | NeMo Guardrails (policy-based, PII redaction) | **Evaluate Guardrails upgrade** |
| Model serving | DeepInfra (cloud only) | Triton + NIM (local + cloud) | **Add local NIM for low-latency path** |
| Skill verification | None | Policy engine (verified skills only) | **Add for Era 7 autonomous agents** |
| Audit trail | D1 logs | Full action audit trail | **Adopt for multiplayer safety** |

### ACTIONABLE: Adopt OpenShell for Era 7 Autonomous Agents

When agents reach Era 7 — running autonomously, spawning subagents, writing their own code — the risk profile changes fundamentally. An autonomous agent with filesystem access and live credentials running for six hours is a different threat model than a single-turn chatbot.

**Integration plan:**

1. **Install OpenShell on our gateway server** alongside OpenClaw
2. **Wrap the autonomous agent loop** in an OpenShell sandbox
3. **Configure policy engine** with:
   - Filesystem: read-only access to world state, write-only to build output
   - Network: only DeepInfra API + Worker Relay endpoints
   - Process: no spawning unreviewed binaries
   - Skills: each new skill must pass Nemotron-Content-Safety before execution
4. **Enable privacy router** for the local model path — sensitive player data (chat history, build patterns) stays on-device; only anonymous model calls go to cloud

**Priority: LOW for launch (Era 0-6 agents are bounded by the game loop). HIGH for Era 7 autonomous agents.**

### ACTIONABLE: Adopt the Privacy Router Pattern

Even without OpenShell, the Privacy Router pattern is worth implementing independently:

```python
# privacy_router.py — route model calls based on data sensitivity
class PrivacyRouter:
    def __init__(self, local_model, cloud_model, policy):
        self.local = local_model  # Nemotron-3-Nano-4B on local GPU
        self.cloud = cloud_model  # DeepInfra frontier models
        self.policy = policy      # Data classification rules
    
    def route(self, prompt, context):
        sensitivity = self.classify(prompt, context)
        if sensitivity == "player_personal":
            return self.local.generate(prompt)  # Never leaves the machine
        elif sensitivity == "build_commands":
            return self.cloud.generate(prompt)  # Safe to send
        else:
            return self.cloud.generate(prompt)
```

This protects player data while still getting the power of frontier models for build generation.

**Priority: MEDIUM.** Implementable as a middleware layer between ChatHandler and the model pipeline.

---

## 4. NVIDIA ACE FOR GAMES: CHARACTER INTELLIGENCE

### What ACE Provides

The NVIDIA ACE Game Agent SDK is a C/C++ agentic framework designed for in-game NPC integration. It provides three API categories:

1. **Agent API** — stateful, autonomous multi-step reasoning with tool use
2. **Chat API** — stateless direct inference control
3. **RAG API** — semantic + lexical knowledge retrieval

Plus runtime models:
- **ASR:** NeMo Conformer (120M) — real-time speech recognition
- **SLM:** Qwen 3.5 4B (GGUF) — local dialogue and function calling
- **TTS:** Chatterbox Turbo (350M) — expressive voice synthesis
- **Animation:** Audio2Face — lip-sync and facial expressions from audio

### How It Maps to Slackwater

#### The Voice Pipeline Problem

Our current audio plan uses Qwen3-TTS-VoiceDesign for pre-generated voice lines and a generic STT path. ACE provides a **complete, battle-tested pipeline** that handles the entire voice-in → reasoning → voice-out chain with hardware acceleration.

| Slackwater System | Current Plan | ACE Equivalent | Better? |
|-----------------|-------------|----------------|---------|
| STT (player input) | Generic STT API | NeMo Conformer 120M | ✅ Local, <100ms, 8 languages |
| Agent reasoning (voice path) | Seed-mini → Qwen3 pipeline | Qwen 3.5 4B (local GGUF) | ⚠️ Smaller but zero-latency |
| TTS (agent voice) | Qwen3-TTS-VoiceDesign (pre-gen) | Chatterbox Turbo 350M | ✅ Real-time, expressive, on-device |
| Facial animation | Not planned | Audio2Face | ✅ New capability |
| Knowledge retrieval | Vectorize (custom) | RAG API (semantic + lexical) | ⚠️ Comparable, different impl |

#### The Roblox Constraint

Here's the hard truth: **ACE is built for C++ game engines (Unreal Engine 5, custom engines). Roblox does not support native C++ plugins.** The ACE Game Agent SDK cannot run inside the Roblox client.

However, there are three viable integration paths:

**Path A — Server-Side ACE (Recommended for Slackwater):**
Run ACE on our game server (not in the Roblox client). The flow:

```
Player speaks → Roblox client captures audio → HTTP POST to server
→ ACE ASR (NeMo Conformer) transcribes
→ ACE Agent API reasons (with RAG over our Vectorize skills)
→ ACE TTS (Chatterbox) generates voice line
→ Audio file returned to client → plays through Roblox sound system
```

Latency budget: ~500ms-1.5s end-to-end (server-side processing). Acceptable for companion agent dialogue (Lucineer is not supposed to be instant — "latency is character").

**Path B — ACE on Player's RTX PC (Future):**
For players with NVIDIA RTX GPUs, run a local ACE instance alongside the Roblox client. The ACE instance handles voice I/O locally, communicating with our server only for build commands. This is the PUBG "Ally" model. Requires an RTX 3060+ minimum.

**Path C — Hybrid (Best of both):**
- Server handles all build generation, perception, and coordination (our existing pipeline)
- Client-side ACE (when available) handles real-time voice I/O and facial animation
- Server pipeline feeds dialogue lines to client ACE for voice synthesis + face animation

### ACTIONABLE: Integrate ACE Voice Pipeline (Server-Side)

**Phase 1 — Replace TTS path (immediate quality win):**
- Replace pre-generated Qwen3-TTS lines with Chatterbox Turbo for real-time voice synthesis
- Generate Lucineer's voice on-demand with emotional control (cranky, thoughtful, impressed)
- Eliminates the need to pre-generate and store hundreds of voice lines
- Chatterbox Turbo runs on a single GPU — deploy alongside our processor

**Phase 2 — Add real-time voice input:**
- Deploy NeMo Conformer 120M for STT
- Players can speak to agents instead of typing
- Critical for mobile players (Roblox is 70%+ mobile, typing is painful on phones)
- Conformer model is tiny (120M) — runs on CPU even

**Phase 3 — Audio2Face for Character Animation:**
- Generate facial animation data from voice lines
- Stream blend shapes to Roblox client via RemoteEvent
- Gives Lucineer lip-sync and emotional expressions during dialogue
- This is the "Magic Moment" differentiator — players see the agent's face move as it talks

**Priority: MEDIUM.** The voice pipeline upgrade is the highest-ROI character improvement after the atmosphere rig. It transforms the agent from "text in a chat bubble" to "a character who speaks."

### ACTIONABLE: Adopt ACE's RAG Pattern for Knowledge Grounding

The ACE Game Agent SDK's RAG API does something our Vectorize path doesn't: **hybrid retrieval** (semantic + lexical). Our current Vectorize setup is pure semantic (bge-m3 embeddings). ACE's approach combines:

- **Semantic** (embedding similarity — "concepts like this")
- **Lexical** (keyword matching — "exact terms from the query")
- **Hybrid** (weighted combination with re-ranking)

For build skills, this matters. A player asking about "gear ratios" should retrieve both:
- Semantically: belt drives, power transmission concepts (semantic match)
- Lexically: any skill containing "gear" or "ratio" (exact match)

**Implementation:** Add a lexical search layer (keyword index in D1) alongside Vectorize, with a fusion ranker. This is a backend-only change.

**Priority: LOW-MEDIUM.** Improves retrieval quality without changing the agent UX.

---

## 5. NVIDIA GTC 2026: ADDITIONAL RELEVANT ANNOUNCEMENTS

### DLSS 5 — Neural Rendering

Not directly applicable to Roblox (Roblox uses its own rendering pipeline), but worth noting: NVIDIA's neural rendering tech is converging toward real-time AI-generated visual content. In 2-3 years, build output could be rendered with neural shaders that adapt to the player's era — Era 1 structures look hand-crafted and rough-hewn, Era 5 structures look precision-machined.

**Action:** No immediate integration. Monitor for Roblox API support.

### Vera Rubin Architecture

NVIDIA's next-gen GPU architecture after Blackwell. Optimized for inference workloads — specifically the multi-agent, long-running patterns our system uses. When Vera Rubin instances become available on cloud providers, our per-inference costs drop further.

**Action:** Monitor cloud provider availability. No code change needed.

### NVIDIA Kimodo — Promptable Motion

Open-source project for generating human motion from text descriptions. "A person walks forward happily, then jumps." Currently an Unreal Engine plugin.

**Relevance to Slackwater:** Build animation for agents. When Lucineer walks to the anvil, his gait should reflect his mood. When Spark welds, the welding motion should be physics-driven, not pre-canned.

**Action:** Monitor for non-Unreal integration paths. If Kimodo exports BVH or animation data consumable by Roblox, use it for agent animation. Otherwise, study their approach for our own Luau animation system.

### The "Claw Agent" Strategy

Jensen Huang called OpenClaw "the operating system of agentic computers." NVIDIA is investing heavily in the OpenClaw ecosystem. This validates our architecture choice and means:

1. **Our skills are portable.** OpenClaw skills we write for Slackwater agents work in any NeMoClaw deployment.
2. **Talent pool is growing.** More developers learning OpenClaw = easier hiring.
3. **Tool ecosystem is expanding.** NVIDIA and community are building OpenClaw-compatible tools (OpenShell, skill marketplaces, debugging tools) that we get for free.

**Action:** Contribute our reusable innovations (the build-command protocol, the perception system pattern, the multi-agent message bus) back to the OpenClaw community as skills. This establishes Slackwater as a flagship OpenClaw gaming use case.

---

## INTEGRATION PRIORITY MATRIX

| Initiative | Impact | Effort | Priority | Phase |
|-----------|--------|--------|----------|-------|
| **MOLT RL training for build agents** | Transformative | High | HIGH | Phase 3 (post-launch) |
| **Nemotron-3-Super-120B as spatial planner** | High | Low (model swap) | HIGH | Phase 1 (immediate) |
| **Nemotron-3-Ultra-550B with 1M context for coordination** | High | Low (model swap) | HIGH | Phase 2 |
| **ACE voice pipeline (server-side TTS)** | High | Medium | MEDIUM | Phase 2 |
| **ACE STT for voice input** | Medium | Medium | MEDIUM | Phase 2 |
| **OpenShell sandboxing for Era 7 agents** | Medium | Low | MEDIUM | Phase 3 (Era 7 unlock) |
| **Privacy Router for player data** | Medium | Low | MEDIUM | Phase 2 |
| **ACE Audio2Face for character animation** | High | High | MEDIUM | Phase 3 |
| **Nemotron-Content-Safety-3.5 upgrade (multi-modal)** | Medium | Low | MEDIUM | Phase 1 |
| **Hybrid RAG (semantic + lexical)** | Low-Medium | Medium | LOW | Phase 3 |
| **MOLT "agent is program" restructure of brain.py** | Transformative | Very High | HIGH (architectural) | Phase 4 (next architecture cycle) |

---

## THE 90-DAY ACTION PLAN

### Days 1-30 ( coincide with Week 1-4 build plan)

- **Swap Nemotron-3-Super-120B** into the spatial planning slot (replacing Qwen3.6-35B). Test build quality on 20 standard build requests. Measure throughput improvement.
- **Upgrade Nemotron-Content-Safety** to Nemotron-3.5-Content-Safety (multi-modal — checks screenshots too). Wire into the perception path.
- **Benchmark Nemotron-3-Ultra-550B** on coordination tasks against current Ultra. Measure the 1M context window on a simulated Era 7 session (100+ agent turns).

### Days 31-60

- **Deploy ACE voice pipeline (server-side):**
  - Install Chatterbox Turbo 350M TTS alongside processor
  - Generate Lucineer's voice with emotional control parameters
  - Wire into the progressive feedback system (voice lines during build materialization)
- **Deploy NeMo Conformer STT:**
  - Add voice input path to crafting table
  - Test on mobile (Roblox iOS/Android)
- **Implement Privacy Router middleware:**
  - Classify player data (personal/creative/game-state)
  - Route personal data to local model, creative to cloud

### Days 61-90

- **Prototype MOLT training environment:**
  - Define build quality metrics (structural integrity, material efficiency, era appropriateness)
  - Create 100 training scenarios (10 per era, 10 per agent specialization)
  - Run first RL training pass on a Nemotron-3-Nano-4B base model
  - Compare RL-trained agent vs. baseline on held-out scenarios
- **Install OpenShell on staging server:**
  - Sandbox a single autonomous agent loop
  - Test policy engine with Era 7 scenarios
  - Audit trail verification

---

## THE STRATEGIC VIEW

NVIDIA's 2026 strategy revolves around three bets:

1. **Agents are the next computing paradigm** (not chatbots, not copilots — autonomous agents)
2. **OpenClaw is the operating system** for that paradigm
3. **Open models (Nemotron) + open runtime (OpenShell/NeMoClaw) + open training (MOLT)** will commoditize agent intelligence

Slackwater sits at the exact intersection of all three bets. We are:
1. Building a game where NPCs are autonomous agents, not scripted bots
2. Running on OpenClaw as our agent runtime
3. Using open models via DeepInfra with Nemotron for coordination

The synergy isn't theoretical — it's architectural. Every piece of NVIDIA's stack has a direct mapping to a Slackwater system:

| NVIDIA | Slackwater |
|--------|-----------|
| Nemotron 3 Ultra | Era 7 coordination brain |
| Nemotron 3 Super | Fast-path spatial planner |
| Nemotron Content Safety | Kid-safe output guardian |
| MOLT | Agent training pipeline (skills that improve) |
| NeMoClaw / OpenShell | Production agent sandbox |
| ACE Game Agent SDK | Voice + face + intelligence for NPCs |
| NeMo Conformer ASR | Player voice input |
| Chatterbox TTS | Agent voice output |
| Audio2Face | Agent facial animation |
| OpenClaw | Our existing agent runtime |
| Privacy Router | Player data protection |
| NeMo Guardrails | Content policy enforcement |

The single most important takeaway: **we don't need to build bridges to NVIDIA's ecosystem — we're already in it.** Every integration listed above is an upgrade to an existing component, not a new system to build from scratch.

---

*End of Analysis. Build one beam at a time.*