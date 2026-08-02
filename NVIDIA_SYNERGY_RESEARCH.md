# NVIDIA × Slackwater: Synergy Research Report
## AI Researcher Perspective — Agent Autonomy & Learning

**Author:** Research Agent (subagent depth 1)
**Date:** 2026-08-02
**Status:** Living document — update as experiments progress

---

## EXECUTIVE SUMMARY

NVIDIA's July 2026 releases — **MOLT** (agentic RL framework), **Nemotron 3 Ultra** (550B MoE agent model), and **NemoClaw** (secure agent runtime blueprint) — collectively define a stack that is *remarkably* aligned with Slackwater's architecture. Where our system uses Cloudflare Workers for orchestration and DeepInfra for inference, NVIDIA's stack provides the missing **training loop**: a way to make Slackwater's agents actually *learn* from their experiences in-game.

The highest-value insight: **MOLT's "reward is any Python you write inside an Env" contract is a near-perfect fit for Slackwater's PERCEIVE-THINK-ACT-COMMUNICATE-LEARN loop.** We can define reward functions over game state (build quality, player satisfaction, agent cooperation) and train our agent models to optimize them.

---

## 1. NVIDIA MOLT (labs-molt) — Deep Analysis

### 1.1 What MOLT Is

**Paper:** "A Scalable PyTorch-Native Training Framework for Agentic Reinforcement Learning" (Hu et al., arXiv:2607.21653, July 22 2026)

**Repo:** github.com/NVIDIA-NeMo/labs-molt (Apache 2.0, ~9.2K LOC of RL code)

**Stack:** Ray (placement + async queues) + vLLM (rollout) + NVIDIA AutoModel/FSDP2 (training). Three components, one async loop. No forks — upstream improvements arrive as container pins.

**Core contract:** "The agent is the program; the trainer is a single actor; reward is any Python you write inside an Env or ChatAgent." The trainer never sees a token the model didn't generate. Three invariants enforce this:

1. **Token identity** — sampled token ids define the trajectory, never retokenized transcripts
2. **Policy-version semantics** — every action token keeps its sampling log-probability; async mismatches corrected per-token with sequence-level gating
3. **Forward consistency** — rollout and training agree on model semantics, including MoE expert routing (rollout routing replay)

### 1.2 MOLT's RL Training Loop ↔ Slackwater

**Question (a): How does "reward is any Python" map to our game?**

Directly and powerfully. MOLT's `Env` subclass requires only one method:

```python
class SlackwaterEnv(Env):
    async def step(self, state) -> Result:
        # state contains: observation_text, action_text, label, sampling_params
        # We evaluate the agent's action against game state
        
        # REWARD SIGNAL OPTIONS:
        # 1. Build quality score (structural integrity check)
        build_score = check_structure_stability(state["action_text"])
        
        # 2. Player satisfaction (explicit feedback or engagement metrics)
        satisfaction = get_player_rating(state["session_id"])
        
        # 3. Agent cooperation (successful task handoffs)
        cooperation = score_task_handoff(state["agent_id"], state["action_text"])
        
        # 4. Era-appropriate crafting (did they use the right tier?)
        era_bonus = verify_era_tech(state["action_text"], state["current_ra"])
        
        # 5. Tool-use correctness (valid CommandExecutor output)
        tool_valid = validate_command_output(state["action_text"])
        
        reward = build_score * 0.3 + satisfaction * 0.2 + cooperation * 0.2 + era_bonus * 0.15 + tool_valid * 0.15
        return Result(reward=reward, terminated=True)
```

**Concrete reward signals we could implement:**

| Signal | Source | Type | Notes |
|--------|--------|------|-------|
| Build stability | Lua physics engine | Verifiable (binary/continuous) | Does the structure stand? Does it survive a tide? |
| Recipe correctness | Crafting system state | Binary | Did the agent use the right parts? |
| Task completion time | Game clock | Continuous (negative = faster) | Faster = better, with diminishing returns |
| Player rating | UI feedback (thumbs up/down) | Binary or 1-5 | Post-task "was this helpful?" |
| Agent coordination | Message bus logs | Continuous | Did help_request → help_response succeed? |
| Skill novelty | Vectorize similarity | Continuous | Is this a new skill, or repetition? |
| Resource efficiency | Inventory tracking | Continuous | Output value / input cost |

**Key insight:** MOLT supports `LLM-as-judge` reward functions by routing judge calls back through the same vLLM engines driving rollout. This means we could use Nemotron-Ultra to *grade* agent builds, creating a self-improving loop where the judge model itself improves over time.

### 1.3 Async Runtime Architecture Comparison

**Question (b): MOLT's Ray + vLLM vs. our Cloudflare Worker + Python processor**

| Dimension | MOLT | Slackwater (current) | Bridge Opportunity |
|-----------|------|---------------------|-------------------|
| **Orchestration** | Ray (placement, async queues) | Cloudflare Workers (job queue, Durable Objects) | MOLT's Ray patterns could inform our DO state machine |
| **Inference** | vLLM (local, loopback, token-exact) | DeepInfra API (remote, stateless) | Token-exact capture is impossible via API — but we can approximate with logit bias |
| **Weight sync** | NCCL broadcast (partial rollout pauses engines) | N/A (inference is remote) | Not applicable unless we self-host models |
| **Multi-turn stitching** | Token-id segment sealing on context compaction | JSON message history in D1 | **Adopt the segment concept** for our conversation memory |
| **Async correctness** | Per-token IS correction (seq-mask-tis default) | None (stateless API calls) | Not applicable for inference-only; critical if we ever self-host training |
| **Scale ceiling** | 1T-class MoE (DeepSeek-V3 at EP256) | Constrained by DeepInfra rate limits | Use DeepInfra for dev; MOLT + self-hosted for research |

**Actionable pattern:** MOLT's **partial rollout** concept — pausing inference engines, broadcasting new weights, resuming retained requests — maps to our architecture as: *pause the agent perception loop, push new prompt/recipe updates to all agents, resume without losing conversation context.* Our Durable Object per world instance already supports this via WebSocket connection state.

### 1.4 Multi-Turn Tool Calls in RL

**Question (c): Can MOLT's approach to tool-use in RL improve our agents?**

**Yes, significantly.** This is the most direct transfer.

MOLT ships a `geo3k` reference agent that does **VLM multi-turn + Python tool calls in an RL loop**. The agent:
1. Sees a geometry problem as an image
2. Writes Python code to solve it
3. Gets execution feedback
4. Iterates
5. Is scored on final answer correctness

This maps almost exactly to our Slackwater agent loop:

```
PERCEIVE (screenshot via Qwen3-VL) → THINK (model decides action) → 
ACT (CommandExecutor runs Lua command) → 
COMMUNICATE (message bus) → 
LEARN (Vectorize skill update)
```

**The MOLT upgrade:** Instead of our agents being frozen prompts (system prompts that never change), MOLT's RL loop would let agents *learn* which tool-call sequences lead to successful builds. An agent that repeatedly calls `BuildAnalyzer.check_stability()` before committing a structure would be reinforced; an agent that wastes resources on premature decoration would be penalized.

**Experiment proposal — RL-Finetuned Builder Agent:**
1. Collect 10K Slackwater build trajectories (agent attempts + outcomes)
2. Define reward: structural stability × era-appropriateness × resource efficiency
3. Use MOLT's GRPO estimator with Nemotron-Nano-9B as the policy
4. Compare build success rate before/after RL training
5. If successful, scale to Nemotron-3-Super-120B

### 1.5 Token-First Contract vs. JSON Command Schema

**Question (d): How does MOLT's token-first contract compare to our JSON schema?**

Our agents output JSON commands (`{action: "build", target: "gearbox", position: [x,y,z]}`). MOLT's token-first contract means the *raw token ids* define the trajectory, and everything (logprobs, action ranges, rewards) stays aligned in token space.

**Current gap:** When our agent outputs JSON, we parse it server-side and execute the command. But we lose:
- The *logprobs* of each token (DeepInfra doesn't expose these reliably)
- The *action range* boundaries (which tokens are the "action" vs. "arguments")
- The *policy version* semantics (we don't track which model version generated which response)

**What to steal:**
- **Action range tagging:** Annotate our JSON schema so we know which token ranges correspond to `action`, `target`, `position`. This enables per-component reward attribution.
- **Trajectory persistence:** Store the raw model output (before JSON parsing) alongside the parsed command and execution result. This creates a training dataset.
- **Token-exact replay:** When we eventually do RL training, we need the exact tokens — not a re-serialized version.

```typescript
// Enhanced command schema for future RL training
interface TrackedCommand {
  raw_output: string;          // exact model output
  token_ids: number[];         // from tokenizer
  logprobs?: number[];         // if available
  model_version: string;       // e.g. "nemotron-3-ultra-550b-2026-08-01"
  parsed_command: GameCommand; // our existing JSON schema
  execution_result: CommandResult;
  reward_components: {
    stability?: number;
    efficiency?: number;
    player_rating?: number;
    era_appropriate?: boolean;
  };
}
```

### 1.6 Scale Lessons

**Question (e): MOLT handles 1T-class MoE. What scale lessons apply to us?**

We use DeepInfra-hosted models (Nemotron-Ultra-550B, Qwen3-Coder-480B). Key scale lessons:

1. **MoE routing stability (R3):** MOLT's rollout routing replay ensures training and inference agree on expert selection. For *inference*, this means consistent behavior — but for our *multi-agent coordination*, it means that the same prompt should route to the same experts. **Action:** pin model versions per agent to ensure behavioral consistency.

2. **Expert parallelism as configuration:** MOLT scales from 4B dense to 700B MoE by changing flags (`--fsdp.ep_size 256`). Our pipeline should similarly treat model selection as configuration, not architecture. **Action:** ensure our processor pipeline can swap models via config without code changes.

3. **Partial rollout for weight sync:** When we update agent system prompts or recipes, we should "pause" agent inference, broadcast the update, and resume — rather than killing and restarting sessions. **Action:** implement a `pauseAgentPool()` / `resumeAgentPool()` pattern in our Durable Object.

4. **Importance sampling correction:** MOLT's seq-mask-tis default corrects for the train/inference logprob gap. While we don't train, the *concept* applies to our prompt engineering: if an agent's system prompt changes mid-session, prior responses were generated under a different "policy." **Action:** version all system prompts and track which version generated each response.

---

## 2. NVIDIA NEMOTRON 3 FAMILY — Technical Deep Dive

### 2.1 Architecture

**Nemotron 3 Ultra** (550B total / 55B active, MoE):

| Feature | Detail | Slackwater Relevance |
|---------|--------|---------------------|
| **Hybrid Mamba-Attention** | Mamba layers for sequence efficiency + Transformer layers for precise recall | Critical for long agent sessions — Mamba reduces KV-cache growth, enabling longer conversations in our Memory D1 |
| **NVFP4 precision** | Single checkpoint runs on Hopper, Blackwell, and Ampere | If we self-host: one deployment across mixed GPU fleets |
| **LatentMoE** | More efficient expert routing than dense MoE | Better per-token routing for mixed task types (building vs. coding vs. chatting) |
| **Multi-Token Prediction (MTP)** | Predicts multiple future tokens per forward pass | 5x throughput improvement for long agent outputs |
| **1M token context** | Ruler @1M: 95% | Enables full session replay for RL training without truncation |

### 2.2 "Self-Evolving Agents" — What It Means Technically

The Nemotron 3 launch materials describe agents that "sustain architectural decisions across coding sessions" and "synthesize contradictory evidence across hundreds of research sources." The technical mechanism is **Multi-Teacher On-Policy Distillation (MOPD)**:

1. **10+ specialized teacher models** are trained, each with domain-specific expertise
2. The student (Ultra) generates rollouts across domains
3. Each teacher scores the student in its area of expertise
4. Student is updated based on dense reward signals from all teachers
5. **Iterative co-evolution:** improved student → new teacher training round → next MOPD stage

**Application to Slackwater:** This is exactly the multi-agent specialist pattern we've designed (Mechanic, Electrician, Coder, etc.). We could implement a *distillation* pipeline:

```
Train specialist teachers (Mechanic-agent, Coder-agent, Builder-agent on domain data)
    ↓
Student agent (generalist Lucineer) generates build attempts
    ↓
Each specialist scores the attempt in their domain
    ↓
Student updates → improved generalist agent
    ↓
Re-train specialists from improved student → repeat
```

**This is a novel research contribution waiting to happen.** No game AI system has publicly demonstrated MOPD-style multi-teacher distillation for game agents.

### 2.3 Hybrid Mamba-Attention → Our Memory D1

The Mamba layers in Nemotron 3 directly address a problem in our architecture: **conversation memory growth**. Currently, our agent conversations grow linearly, eventually hitting context limits. Mamba's selective state-space model has **constant-time per-token inference** regardless of sequence length, which means:

- Agent conversations could run for thousands of turns without degradation
- The KV-cache footprint stays bounded (Mamba doesn't use attention for all layers)
- Long-horizon tasks (multi-hour building sessions) become feasible without context windowing

**Action:** When Nemotron 3 Ultra is available via DeepInfra, benchmark it against our current Qwen3-Coder for:
- Multi-turn conversation coherence (50+ turns)
- Tool-call accuracy degradation over time
- Throughput per turn at various context lengths

### 2.4 Training Data & RL Environments — Openness

Nemotron 3 launches with extraordinary openness:
- **50M SFT samples** (cumulative)
- **2M RL tasks** across multiple domains
- **55 RL environments** (15 new with Ultra)
- **MOPD recipes** on github.com/NVIDIA-NeMo/RL

The 15 new RL environments are particularly interesting — they define the *kinds of tasks* the model was trained on. We should review these environments to understand what behaviors Nemotron 3 Ultra is optimized for, and whether any align with our game agent tasks.

**Action:** Clone github.com/NVIDIA-NeMo/RL, inspect `docs/guides/nemotron-3-ultra.md`, and catalog the 55 RL environments. Identify any that resemble game-world tasks (tool use, spatial reasoning, multi-step planning).

---

## 3. NVIDIA AGENT INFRASTRUCTURE — NemoClaw & Agent Toolkit

### 3.1 NemoClaw Architecture

**Repo:** github.com/NVIDIA/NemoClaw (Apache 2.0, alpha)

NemoClaw is a **reference stack for running always-on AI agents securely**. It combines:

- **OpenShell** — sandboxed runtime where agents and their generated code execute (early preview, part of NVIDIA Agent Toolkit)
- **OpenClaw** — listed as the *default* agent harness, alongside Hermes and LangChain Deep Agents
- **Blueprint lifecycle** — guided onboarding, hardened configuration, network policy, lifecycle management via single CLI
- **Routed inference** — managed inference provider validation and routing

**Key architectural parallels with Slackwater:**

| NemoClaw Concept | Slackwater Equivalent | Synergy |
|-----------------|----------------------|---------|
| OpenShell sandbox | Roblox sandbox (Luau VM) | Both isolate agent-generated code from the host |
| Blueprint lifecycle | Agent recruitment/deployment | NemoClaw's "single command install" pattern for agent deployment |
| Network policy | Cloudflare Worker CORS/auth | NemoClaw's baseline rules + operator approval flow maps to our agent permission system |
| Routed inference | DeepInfra model routing | NemoClaw validates inference providers; we should adopt this pattern |
| Agent harness (OpenClaw) | Our agent runtime loop | **Direct alignment** — OpenClaw's subagent pattern is our agent spawning pattern |

### 3.2 OpenClaw as First-Class Citizen

The Nemotron 3 blog post explicitly names **OpenClaw** as a supported agent harness in NemoClaw. This is significant for us because:

1. **We're already on OpenClaw** — our entire tooling stack (gateway, skills, subagents) is built on it
2. **NemoClaw provides secure deployment patterns** — we can use NemoClaw blueprints to deploy Slackwater agent processors in NVIDIA-sanctioned sandboxes
3. **OpenShell could replace our ad-hoc Python processor** — instead of running `perception_agent.py` as a bare asyncio loop, we could run it inside OpenShell for proper isolation and lifecycle management

### 3.3 NVIDIA Agent Orchestration vs. Our Subagent Pattern

NVIDIA's agent orchestration (via NemoClaw + Hermes/OpenClaw) uses:
- **Single-process agent harness** managing tool calls, memory, and multi-turn workflows
- **Sandbox isolation** for agent-generated code (OpenShell)
- **Inference routing** with validated providers

Our OpenClaw subagent pattern uses:
- **Main agent** spawns **subagents** for specific tasks (depth-limited)
- **Session isolation** via unique session IDs
- **Channel-based routing** (Telegram, Discord, etc.)

**What to learn:** NemoClaw's **network policy** system — baseline rules, operator approval flow, egress control — is more mature than our current ad-hoc permissions. We should adopt a similar policy file for our agents:

```yaml
# agent-network-policy.yaml
agents:
  lucineer:
    allowed_endpoints:
      - deepinfra.com/*
      - lucineer-relay.casey-digennaro.workers.dev/*
    denied_endpoints:
      - "*"
    max_concurrent_sessions: 5
    rate_limit_per_minute: 60
    
  voyager:
    allowed_endpoints:
      - lucineer-relay.casey-digennaro.workers.dev/perception
    denied_endpoints:
      - "*"
    max_concurrent_sessions: 1
    requires_approval_for:
      - build_commands
      - resource_consumption
```

---

## 4. BROADER INDUSTRY CONTEXT

### 4.1 Game Studios Using NVIDIA Agent Tech

From the NVIDIA developer blog (May-July 2026), Nemotron 3 is being adopted in:
- **RTL chip design** (ACE-RTL agent for Verilog generation — agentic iterative coding)
- **Telecom network operations** (autonomous network management)
- **Industrial alarm management** (triage agents)
- **Automotive cockpit assistants** (DRIVE AGX platform, multimodal VLM agents)
- **Financial services** (multi-agent signal discovery)

**No public examples of game studios using NVIDIA's agent tech for in-game NPCs were found.** This represents both a gap and an opportunity — Slackwater could be a first-mover demonstrating RL-trained game agents on NVIDIA infrastructure.

### 4.2 Roblox + NVIDIA

No specific Roblox-NVIDIA AI partnership was found in public sources. However:
- Roblox is investing heavily in generative AI (Roblox Assistant, generative materials)
- NVIDIA's ace-in-the-hole for Roblox is **Nemotron 3's NVFP4 precision** — a single checkpoint running across GPU architectures, which could power edge inference for Roblox's cloud gaming infrastructure
- The **hybrid Mamba-Attention** architecture is ideal for Roblox's constraint: long agent sessions on constrained hardware

**Strategic opportunity:** Slackwater could serve as a *proof of concept* for NVIDIA-powered game agents on Roblox, potentially opening partnership conversations with both companies.

### 4.3 Open-Source Agent Frameworks Inspired by MOLT

MOLT was released July 22, 2026 — just 11 days before this analysis. It's too early for derivative frameworks. However, the paper explicitly invites this:

> *"The codebase must be readable by a human researcher in one pass, and navigable by an AI coding assistant, which the paper cites explicitly as a design audience."*

This means **Claude Code or similar tools can read and modify MOLT's RL code** — lowering the barrier for us to create Slackwater-specific forks.

---

## 5. RECOMMENDED PAPERS TO READ

| Priority | Paper | Why | Link |
|----------|-------|-----|------|
| **P0** | MOLT paper (Hu et al. 2026) | Core framework we may adopt | [arXiv:2607.21653](https://arxiv.org/abs/2607.21653) |
| **P0** | GRPO (Shao et al. 2024) | MOLT's default estimator; we need to understand the math | [arXiv:2402.03300](https://arxiv.org/abs/2402.03300) |
| **P1** | DAPO (2025) | Dynamic sampling + asymmetric clipping for GRPO | [arXiv:2503.14476](https://arxiv.org/abs/2503.14476) |
| **P1** | GSPO (2025) | Sequence-level optimization for MoE stability | [arXiv:2507.18071](https://arxiv.org/abs/2507.18071) |
| **P1** | ACE-RTL (2026) | Best example of iterative agentic coding with Nemotron 3 Ultra | [arXiv:2602.10218](https://arxiv.org/abs/2602.10218) |
| **P2** | Voyager (Minecraft) | Our agent is explicitly inspired by this; compare to MOLT's approach | [arXiv:2305.16291](https://arxiv.org/abs/2305.16291) |
| **P2** | DeepSeek-R1 (2025) | How GRPO + verifiable rewards improved reasoning | [arXiv:2501.12948](https://arxiv.org/abs/2501.12948) |
| **P2** | Rollout Routing Replay (R3) | MoE routing stability during RL | [arXiv:2510.11370](https://arxiv.org/abs/2510.11370) |
| **P3** | IcePop / TIS | Token-level importance sampling corrections | Referenced in MOLT README |
| **P3** | Nemotron 3 technical blog | Architecture details, MOPD recipe | [NVIDIA Blog](https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-powers-faster-more-efficient-reasoning-for-long-running-agents/) |

---

## 6. RECOMMENDED EXPERIMENTS

### Experiment 1: Baseline Agent Trajectory Collection
**Goal:** Build the training dataset for future RL
**Method:** Log every agent decision (perceive → think → act → result) with full token traces
**Scale:** 10K trajectories across 5 agent types
**Timeline:** 2 weeks (can start now with current architecture)

### Experiment 2: GRPO on Nemotron-Nano-9B for Tool Calling
**Goal:** Prove the RL loop works on our task domain
**Method:** Use NeMo RL + NeMo Gym with a Slackwater tool-calling environment
**Reward:** Binary — did the agent produce a valid game command that executed successfully?
**Scale:** Single H100, LoRA fine-tune
**Timeline:** 1-2 weeks once we have GPU access

### Experiment 3: MOPD for Multi-Specialist Distillation
**Goal:** Train a generalist Lucineer agent from specialist teachers
**Method:** Train 3 specialist models (Mechanic, Electrician, Coder) on domain data → MOPD distillation into generalist
**Scale:** 2-node H100 (using MOLT's shipped recipes as template)
**Timeline:** 4-6 weeks

### Experiment 4: MOLT's ChatAgent with Slackwater Game Harness
**Goal:** Train agents against the actual game environment
**Method:** Point MOLT's ChatAgent at our Cloudflare Worker inference endpoint; define reward from game state
**Challenge:** Our API is OpenAI-compatible but not token-exact (DeepInfra doesn't return logprobs)
**Workaround:** Self-host vLLM with Nemotron-3-Super-120B for training runs
**Timeline:** 6-8 weeks

### Experiment 5: Vision-Language RL for Perception Agent
**Goal:** Train Qwen3-VL to identify build errors from screenshots
**Method:** Use MOLT's geo3k VLM RL recipe as template; replace geometry problems with build screenshots
**Reward:** Did the agent correctly identify the structural issue?
**Timeline:** 3-4 weeks

---

## 7. ARCHITECTURE RECOMMENDATIONS

### 7.1 Immediate (No GPU Required)
1. **Add trajectory logging** to our agent runtime — store raw model outputs, parsed commands, execution results, and game state snapshots
2. **Version all system prompts** — track which prompt version generated each response
3. **Implement action range tagging** in our JSON command schema — know which tokens are "action" vs. "arguments"
4. **Add reward signal collection** — let players rate agent helpfulness; log build stability scores

### 7.2 Near-Term (With GPU Access)
1. **Set up MOLT** in a Docker container with the shipped recipes — run the geo3k VLM RL example to validate the pipeline
2. **Define a SlackwaterEnv** — MOLT Env subclass that wraps our game state as an RL environment
3. **Start with Nemotron-Nano-9B** — small, fast, good enough to prove the loop works
4. **Use GRPO with verifiable rewards** — binary task completion is the simplest signal

### 7.3 Long-Term (Research Contributions)
1. **MOPD for game agents** — novel application of multi-teacher distillation to game AI
2. **Multi-agent RL with communication** — MOLT trains single agents; we need multi-agent coordination (not yet covered by MOLT)
3. **Player-as-reward-model** — using real player behavior (engagement, retention, satisfaction) as RL reward signals
4. **Era-gated curriculum learning** — train agents that progressively master each technology era, with RL environments that scale in complexity

---

## 8. KEY RISKS & MITIGATIONS

| Risk | Severity | Mitigation |
|------|----------|------------|
| MOLT requires self-hosted vLLM (no API mode) | High | Start with NeMo RL + NeMo Gym (supports hosted inference); migrate to MOLT when we have GPUs |
| Token-exact training is impossible via DeepInfra | High | Self-host vLLM for training runs; use DeepInfra for inference-only |
| Multi-agent RL is not in MOLT's scope | Medium | Use MOLT for single-agent training; coordinate multi-agent behavior via our existing message bus |
| GPU costs for RL training (2-node H100 baseline) | Medium | Start with LoRA on single GPU; use Prime Intellect Lab for hosted training |
| Nemotron 3 Ultra not yet on DeepInfra | Low | It's listed in our TOOLS.md already; verify availability and benchmark |
| MOLT is 2 weeks old — may have bugs | Low | Start with shipped recipes (tested); contribute fixes upstream |

---

## 9. COMPETITIVE LANDSCAPE

| Framework | RL Code Size | Focus | Fit for Slackwater |
|-----------|-------------|-------|-------------------|
| **MOLT** | ~9.2K LOC | Agentic-first research, single-actor RL | **Best fit** — small, hackable, designed for exactly our use case |
| verl | ~62K LOC | Production RLHF breadth | Too heavy; would need significant adaptation |
| OpenRLHF | ~7.2K LOC | RLHF coverage | Good alternative; MOLT's creator (Jian Hu) also created OpenRLHF |
| slime | ~25K LOC | Megatron throughput | Optimized for scale, not research velocity |

---

## 10. CITATIONS & SOURCES

1. **MOLT Paper:** Hu, J. et al. "A Scalable PyTorch-Native Training Framework for Agentic Reinforcement Learning." arXiv:2607.21653 (July 2026). https://arxiv.org/abs/2607.21653
2. **MOLT Repo:** https://github.com/NVIDIA-NeMo/labs-molt (Apache 2.0)
3. **Nemotron 3 Ultra Blog:** NVIDIA Developer Blog, June 4 2026. https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-powers-faster-more-efficient-reasoning-for-long-running-agents/
4. **Nemotron 3 RTL Blog:** NVIDIA Developer Blog, July 26 2026. https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-leads-open-models-on-accuracy-and-efficiency-in-agentic-rtl-coding/
5. **Agentic RL Guide:** NVIDIA Developer Blog, July 1 2026. https://developer.nvidia.com/blog/mastering-agentic-techniques-ai-agent-reinforcement-learning/
6. **NemoClaw Repo:** https://github.com/NVIDIA/NemoClaw (Apache 2.0, alpha)
7. **Nemotron 3 Nano Customization:** NVIDIA Developer Blog, July 23 2026. https://developer.nvidia.com/blog/start-customizing-nvidia-nemotron-3-nano-with-prime-intellect-lab-in-minutes/
8. **Marktechpost Analysis:** https://www.marktechpost.com/2026/08/01/nvidia-ai-releases-molt-a-pytorch-native-agentic-reinforcement-learning-framework/
9. **LearnAgentic Analysis:** https://learnagentic.substack.com/p/nvidia-just-rebuilt-agentic-rl-training
10. **AI Weekly Alert:** https://aiweekly.co/alerts/nvidia-nemo-open-sources-molt-a-lean-pytorch-agentic-rl-stack
11. **GRPO:** Shao, Z. et al. "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models." arXiv:2402.03300 (2024).
12. **ACE-RTL:** "ACE-RTL: When Agentic Context Evolution Meets RTL-Specialized LLMs." arXiv:2602.10218 (2026).
13. **R3 (Rollout Routing Replay):** arXiv:2510.11370 (2025).

---

## APPENDIX A: MOLT Agent Contract Quick Reference

Two ways to define an agent for MOLT:

### Env Pattern (framework owns the LLM loop)
```python
from molt.agents import Env, Result, StepEnvRunner

class SlackwaterEnv(Env):
    async def step(self, state) -> Result:
        reward = grade(state["action_text"], state["label"])
        return Result(reward=reward, terminated=True)

class AgentRunner(StepEnvRunner):
    def __init__(self):
        super().__init__(SlackwaterEnv)
```

### ChatAgent Pattern (agent owns the loop, OpenAI/Anthropic SDK)
```python
from openai import AsyncOpenAI
from molt.agents import ChatAgent, ChatAgentRunner, ChatContext, Result

class BuilderAgent(ChatAgent):
    async def run(self, ctx: ChatContext) -> Result:
        client = AsyncOpenAI(base_url=ctx.base_url, api_key=ctx.api_key)
        resp = await client.chat.completions.create(
            model=ctx.model_name,
            messages=[{"role": "user", "content": ctx.prompt}],
            max_tokens=ctx.sampling_params.max_tokens,
            temperature=ctx.sampling_params.temperature,
        )
        build_score = evaluate_build(resp.choices[0].message.content)
        return Result(reward=build_score)

class AgentRunner(ChatAgentRunner):
    def __init__(self):
        super().__init__(BuilderAgent)
```

### Key Result fields
| Field | Meaning |
|-------|---------|
| `reward` | Scalar reward consumed by trainer (required) |
| `observation` | Next-turn observation text (multi-turn) |
| `terminated` | Episode finished naturally |
| `truncated` | Cut off externally |
| `info` | Optional diagnostics dict |
| `score` | Optional dynamic-filtering score |
| `images` | Optional next-turn images (VLM) |

---

*This document is a research analysis, not a commitment. Validate all assumptions before implementation. Start with Experiment 1 (trajectory collection) — it requires no GPUs and creates the foundation for everything else.*
