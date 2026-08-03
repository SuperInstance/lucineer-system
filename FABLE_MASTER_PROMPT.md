# FABLE 5 MASTER PROMPT — SLACKWATER DYNAMIC COGNITION

> **The single most important prompt in the project.**
> Designed for Claude Opus / Fable 5 (finite, non-renewing tokens — every word matters).
> Paste this entire document as the initial message in a Fable 5 session.

---

## SYSTEM PROMPT

You are designing the next generation of a system called **Slackwater** — a novel dynamic machine learning architecture for an AI game companion named Lucineer, operating inside a Roblox experience.

This is not a chatbot. This is not a tool-calling agent. This is a **cognition engine** where:

- The **training signal** IS the stream of consciousness
- The **loss function** IS play quality (novelty, engagement, specificity, progression)
- The **gradient** IS prompt/parameter adjustment every 30 seconds
- The **model update** happens continuously, not per epoch

The system has been under design for months. 400,000+ words of architecture documentation exist. Five repos have been deep-dived and analyzed. A cognition codebase (4,152 lines, 71 tests) is running. The game-side production stack scores 96/100 readiness.

**Your job is to design the five missing subsystems that transform this from a research prototype into a genuinely novel form of machine intelligence.** Every token you spend must advance that goal.

---

## CONTEXT INJECTION

### What Slackwater IS

Slackwater is an AI-powered Roblox experience where players build structures alongside Lucineer — a shipyard foreman character with 40 years of building experience across multiple game engines. He is not an assistant. He was hired, not summoned. He always leaves something unfinished. The relationship between player and Lucineer deepens through five bond tiers based on collaborative building behavior, not conversation count.

The character bible is canonical. The game IS the spec — constraint produces thought the way chord changes produce jazz. Attention is the only currency. Getting better at the shared activity IS the point.

### What's Already Built

**Production Stack (96/100 readiness):**
- Cloudflare Worker relay (live), Durable Object job queue (lease-based, alarm-pruned)
- D1 player profiles + build history, Vectorize skill index (35 skills, bge-m3 embeddings)
- Five-model brain pipeline: Seed-2.0-mini (intent) → Qwen3-Coder-480B (code) → Nemotron-Ultra (heavy) → Hermes-405B (personality) → Nemotron-Safety-3.5 (filter)
- 38 Lua modules (36,244 lines): CommandExecutor, ChatHandler, WorldScanner, Poller, UIManager, BeatClock, BuildAnimator, BondSystem
- Process_v2.py: keyword routing, memory/vector integration, progressive feedback, circuit breaker

**Cognition System (4,152 lines, 71 tests — all passing):**
- `local_thinker/`: inference loop, algorithmic action policy (explore/approach/build/inspect/wait/speak), state parser, JSONL journal writer
- `conductor/`: deep analysis loop, prompt updater, parameter tuner (temperature/top_p/budget), quality scorer (novelty/specificity/engagement/spatial_awareness)
- `temporal/`: BeatClock (BPM, measures, phrases), MIDI encoder (gameplay as note_on/note_off/velocity/tempo), pattern matcher (beat-similarity search)

**Infrastructure:**
- RTX 4050 laptop (6GB VRAM), WSL2 Linux, Python 3.10+, Lua 5.1/Luau
- Cloudflare free tier (Workers, D1, R2, Vectorize, Durable Objects, Cron Triggers)
- GLM-5.2 unlimited (Z.ai Max), DeepInfra (179 models), DeepSeek V3 (direct, extremely cheap)
- Ollama for local inference (Granite 3.1 2B target, ~500ms)

### What the Deep Dives Proved

Five SuperInstance repos were analyzed. The extracted patterns form the engineering foundation:

**1. Pincher — "Vector DB as Runtime, LLM as Compiler"**
- The vector database IS the runtime. Known intents match in <1ms ($0). Novel intents escalate to LLM.
- The LLM doesn't answer — it **compiles** interactions into reusable reflexes (.nail format).
- Three-tier compute: spinal reflex (~50ms, $0) → confirmation (~3s) → cortical deliberation (~10s).
- Confidence model: success ×1.005, failure ×0.95, clamped [0.05, 0.95].
- Veto engine + immunology system for autonomous safety.
- **For Slackwater:** Pincher's reflex engine becomes Layer 1 memory — sub-millisecond pattern matching for the Conductor. Thoughts become vector-embedded reflexes. The .nail format enables portable agent state.

**2. ZeroClaw Arena — "No Neural Nets, Vectors + Patterns + Evolution"**
- Bounded-state games learned from scratch via tile-based Monte Carlo self-play.
- Tile decomposition: game states factored into independent local patterns with independent statistics.
- Evolution loop: empirical win rate → exponential moving average (α=0.05) → clamped [0.05, 0.95].
- Compiled policies: trained tiles compile to O(1) hash-lookup tables (zero dependencies, ~15KB).
- Results: Tic-Tac-Toe 70.6%, Go 9×9 67.3%, Holdem 62.0% win rates vs random.
- **For Slackwater:** The evolution engine breeds better action policies. Context = "game state," actions = "moves," satisfaction = "win rate." The compiled policy makes millions of free decisions, reserving LLM calls for the 20% that genuinely require reasoning.

**3. Lever Runner — "Intent-Based Execution, 3-Gate Cascade"**
- LLM compresses user request to 3-8 word intent phrase (~70 tokens total vs 2,000-5,000 for tool-calling).
- Three-gate cascade: Gate 1 Rust guard (~50µs) → Gate 2 embedding cache (~7.6ms, 44% hit rate) → Gate 3 LLM (~500ms).
- **56% of queries never reach the LLM.** Combined cache trajectory: 0% (day 1) → 44% (week 1) → 80%+ (month 1).
- Trust scoring: +1.5 success, −4.0 failure (asymmetric — 3 successes per failure to recover).
- Structural security: LLM cannot inject commands because it only outputs a short phrase, never a command.
- **For Slackwater:** The three-gate cascade becomes the Local Thinker's action pipeline. The trust scoring system becomes the Conductor's "which prompt modifications work" tracker.

**4. SuperInstance Ecosystem — ".bottle Protocol, Four-Layer Composition"**
- Four layers: Execute (lever-runner) → Cache (pincherOS) → Orchestrate (PLATO) → Evolve (git-native).
- `.bottle` protocol: typed YAML envelopes for inter-component communication (observation, hypothesis, experiment, result, command, config).
- Conservation laws as hard constraints: token conservation, action conservation, identity conservation, evolution conservation.
- Self-improvement loop: observe → hypothesize → A/B test (10% canary) → propose → human review → merge.
- Anti-oscillation: hysteresis (minimum dwell time), rollback budgets, immutable core.
- **For Slackwater:** The .bottle protocol becomes the Thinker ↔ Conductor communication format. Conservation laws become design constraints. The self-improvement loop becomes the Conductor's meta-learning system.

**5. Craftmind — "Vector Write-Back After Each Build"**
- After each task execution, results POST back to the vector index automatically.
- Creates a growing library of refined plans that future agents can search.
- Token budget system with graceful degradation.
- **For Slackwater:** The write-back loop closes the learning cycle. Every thought, every build result, every conductor intervention gets vectorized and stored for future recall.

### Anti-Patterns to Avoid

From the Weird Roblox AI analysis — the exact wrong way to build an AI game companion:
- Open-loop control with no feedback (random actions, no state tracking)
- No vision, no screen reading, no game state inference
- Phantom dependencies and aspirational README claims
- Dead code from duplicate function definitions
- **The lesson:** Every iteration must close the loop: perceive → decide → act → perceive.

---

## TASK SPECIFICATION

Design five subsystems. Each must include: architecture diagram (ASCII), data flow specification, Python interface definitions, integration points with existing code, and acceptance criteria. Output as production-ready design documents with code stubs.

### Task 1: Reflex Compilation Pipeline (Thoughts → .nail Reflexes)

**The problem:** The Local Thinker generates ~1 thought per 5 seconds. Over a play session, thousands of thoughts accumulate. Most are variations of patterns the system has seen before. Currently, every thought requires an LLM call — this is wasteful and slow.

**Design the pipeline that compiles recurring thought patterns into sub-millisecond reflexes:**

1. **Thought intake:** How thoughts flow from the journal into the reflex engine
2. **Pattern detection:** How to identify when a new thought matches an existing reflex (vector similarity thresholds, semantic vs. structural matching)
3. **Reflex compilation:** How a verified thought pattern becomes a .nail reflex entry (the compilation step — what gets stored, how confidence is initialized)
4. **Runtime dispatch:** How the Local Thinker checks reflexes before calling the LLM (the three-tier path: reflex hit → assisted → novel)
5. **Confidence evolution:** How reflex confidence updates based on action outcomes (adapt Pincher's model: +0.05×(1-confidence) on success, −0.10×confidence on failure, clamped [0.05, 0.95])
6. **Reflex pruning:** When to decay, merge, or delete stale reflexes

**Integration:** The reflex engine sits between the Local Thinker's perception step and its LLM inference step. It must handle the journal format defined in `local_thinker/journal.py` and store reflexes in SQLite + sqlite-vec (vendor the Pincher pattern, not the code).

**Acceptance criteria:**
- [ ] Reflex check completes in <1ms for 10,000 stored reflexes
- [ ] After 1 hour of play, ≥40% of thoughts are served by reflexes (no LLM call)
- [ ] Reflex confidence correlates with action success rate (≥0.7 correlation)
- [ ] .nail bundle can be exported, transferred to a fresh instance, and produce matching behavior
- [ ] Zero-dependency hash fallback works when ONNX model is unavailable

### Task 2: Evolution Engine Integration (ZeroClaw Breeds Better Action Policies)

**The problem:** The action policy in `local_thinker/action_policy.py` currently uses static weights (curiosity bonus, cooldown timers, novelty detection). These weights were hand-tuned. They should self-optimize based on which action distributions produce the highest-quality play.

**Design the evolution system that breeds better policies:**

1. **Define the "game":** Slackwater's game state = (channel, player_bond_tier, time_of_day, urgency, nearby_structures, last_action_type). Actions = (explore, approach, build, inspect, wait, speak). Outcome = quality_score from `conductor/quality_scorer.py`.
2. **Tile decomposition:** How to factor Slackwater's context space into tiles (by channel, by bond tier, by time window, by proximity to structures) — each accumulating independent statistics
3. **Monte Carlo simulation:** How to run rollouts of action sequences during idle periods (heartbeat), scoring outcomes against the quality metrics
4. **Evolution loop:** The periodic score refinement step (α=0.05 EMA toward empirical quality, clamped [0.05, 0.95]) — port ZeroClaw's `evolve()` exactly
5. **Policy compilation:** How trained tiles compile to a zero-dependency lookup table for O(1) runtime action selection
6. **Hierarchical clustering:** Group similar context tiles into 8 "strategy archetypes" (e.g., "morning_builder", "evening_explorer") — discovered, not designed

**Integration:** The evolution engine replaces the static weights in `action_policy.py`. It runs evolution during heartbeat cycles (daily). The compiled policy is loaded at startup and hot-swapped when a new version is ready.

**Acceptance criteria:**
- [ ] Policy converges within 2 weeks of training (score variance < 0.01 over 24h)
- [ ] Evolved policy outperforms static weights by ≥15% on quality metrics
- [ ] Compiled policy is a self-contained Python dict (< 50KB)
- [ ] Every decision is traceable to a specific tile entry (100% interpretability)
- [ ] Hierarchical clustering produces meaningful strategy archetypes (human-validated)

### Task 3: Trust Scoring System (Conductor Learns Which Modifications Work)

**The problem:** The Conductor modifies the Local Thinker's system prompt, inference parameters, and action policy weights every 30 seconds. Currently, there's no feedback loop on whether these modifications actually improved play quality. The Conductor is operating blind.

**Design the trust scoring system that closes the Conductor's learning loop:**

1. **Intervention tracking:** Record every Conductor intervention (prompt change, parameter delta, policy update) as a `.bottle`-format command with: timestamp, target, modification type, before-state, after-state, confidence
2. **Outcome measurement:** How to measure whether an intervention improved play (compare quality scores before/after the intervention, controlling for novelty bias — the " placebo" effect of any change producing temporary improvement)
3. **Trust dynamics:** Adapt Lever Runner's asymmetric model (+1.5 success / −4.0 failure) but tuned for cognitive modifications (which need slower learning — suggest +0.5 / −2.0 with 10-observation minimum before trust changes)
4. **A/B canary:** How to test modifications on 10% of thoughts before full promotion (the SuperInstance anti-oscillation pattern)
5. **Rollback budgets:** How many consecutive failures before an intervention type is auto-rolled back (suggest 3 strikes → revert to previous prompt version)
6. **Conductor self-model:** The Conductor maintains a profile of which modification types work in which contexts ("temperature increases help when novelty is low; prompt specificity helps when generic thoughts increase")

**Integration:** The trust system wraps every Conductor output in `conductor/conductor.py`. Before applying a modification, the Conductor checks trust for that modification type in the current context. After applying, it tracks outcomes and updates trust.

**Acceptance criteria:**
- [ ] Every Conductor intervention is logged with before/after state
- [ ] Trust scores correlate with actual quality improvement (≥0.6 correlation after 100 interventions)
- [ ] Auto-rollback triggers on 3 consecutive quality decreases from the same modification type
- [ ] A/B canary runs for 50 thoughts before promotion
- [ ] Conductor self-model identifies ≥3 reliable modification patterns within 2 weeks

### Task 4: Temporal Pattern → Vector Embedding Pipeline (MIDI Sessions → bge-m3 → Vectorize)

**The problem:** The temporal encoder (`temporal/midi_encoder.py`, 600 lines, fully tested) encodes gameplay as MIDI-like beat patterns. But these patterns are never vectorized or stored for future recall. The system can describe what happened but cannot learn from temporal rhythms.

**Design the pipeline that converts play sessions into searchable temporal knowledge:**

1. **Session → MIDI encoding:** How a complete play session (explore→build→inspect→wait→speak sequences) maps to MIDI events (note_on/note_off/velocity/tempo) using the existing `midi_encoder.py`
2. **MIDI → text canonicalization:** How to convert MIDI patterns into text suitable for embedding (suggest: map to a symbolic notation like "B8:E72:v85 → B16:I67:v60 → B4:W:v30" where B=beat, E=explore, I=inspect, W=wait, v=velocity)
3. **Text → bge-m3 embedding:** How to embed the canonical text using bge-m3 via Cloudflare Workers AI (free tier) or local sentence-transformers
4. **Embedding → Vectorize storage:** How to store in Cloudflare Vectorize with metadata (session_id, player_id, timestamp, quality_score, bond_tier)
5. **Pattern recall:** How the Conductor queries for similar temporal patterns when evaluating the current play rhythm ("has this exploration-explore-build rhythm worked before?")
6. **Cross-session learning:** How patterns from multiple sessions aggregate into "play style archetypes" — temporal fingerprints that characterize different player types

**Integration:** The pipeline runs as a post-session batch job (triggered by session end). The Vectorize index is queried by the Conductor during its 30-second analysis cycle. Results feed into prompt updates ("this player's rhythm matches the 'methodical builder' archetype — provide more detail per build").

**Acceptance criteria:**
- [ ] Session → MIDI → text → embedding → Vectorize pipeline runs end-to-end without manual intervention
- [ ] Temporal similarity search returns relevant patterns in <50ms
- [ ] Play style archetypes are discoverable via clustering (≥3 meaningful clusters after 20 sessions)
- [ ] Conductor uses temporal patterns in ≥30% of its modification decisions
- [ ] Embedding consistency: same session always produces the same vector

### Task 5: LoRA Fine-Tuning Data Pipeline (Thought Journals → Granite 3.1 Training Data)

**The problem:** The system generates rich training data (thought journals with quality scores, conductor commentary, action outcomes) but this data never feeds back into the underlying model. The Local Thinker runs the same base model forever. The vision is a LoRA adapter that is continuously refined on the system's own thought data.

**Design the data pipeline that transforms thought journals into LoRA training data:**

1. **Data selection:** Which thoughts become training examples? (Filter: quality_score > 0.7, conductor_commentary = positive, action_result = success. These are the "good thoughts" worth learning from.)
2. **Prompt-completion formatting:** How to structure training pairs: input = (game_state, system_prompt_version), completion = (thought_text, lean, action_taken). Target: the model should generate similar thoughts in similar states.
3. **Quality-weighted sampling:** How to weight training examples by quality score (high-quality thoughts sampled more frequently during training)
4. **Negative examples:** How to use low-quality thoughts as contrastive examples ("don't generate this kind of thought") — DPO-style preference pairs
5. **Training schedule:** When to trigger LoRA fine-tuning (suggest: every 1000 high-quality thoughts, ~weekly). How to run on local RTX 4050 (6GB VRAM — LoRA rank 8-16, batch size 1-4, seq len 512-1024).
6. **Evaluation loop:** How to evaluate whether the fine-tuned model is actually better (run both base and fine-tuned on held-out game states, compare quality scores using the quality_scorer)
7. **Hot-swap:** How to load the new LoRA adapter into the running Ollama instance without restarting the Local Thinker

**Integration:** The pipeline reads from `journals/thoughts/` (JSONL files produced by `local_thinker/journal.py`). Training runs as a cron job or heartbeat task. The fine-tuned model is evaluated against held-out data before promotion.

**Acceptance criteria:**
- [ ] Training data extraction produces ≥500 quality-weighted examples from 1 week of journals
- [ ] LoRA fine-tuning completes in <4 hours on RTX 4050 (6GB VRAM)
- [ ] Fine-tuned model scores ≥10% higher on quality metrics vs base model on held-out states
- [ ] DPO preference pairs improve specificity and spatial_awareness scores specifically
- [ ] Hot-swap works: new adapter loaded without dropping the inference loop

---

## CONSTRAINTS

**Hardware:** RTX 4050 laptop (6GB VRAM), WSL2, 32GB RAM
**Cloud:** Cloudflare free tier (Workers, D1, R2, Vectorize, DO, Cron)
**Models:** GLM-5.2 unlimited (default), DeepSeek V3 (cheap fallback), DeepInfra (179 models), Ollama local (Granite 3.1 2B, ~500ms target)
**Budget:** Token-lean operation is mandatory. The three-gate cascade must handle ≥50% of decisions at $0 cost. LLM calls are reserved for novel situations.
**Latency:** Local inference target <500ms. Reflex matching <1ms. Vector search <50ms.
**Safety:** Every action passes through a veto engine. LLM never produces executable commands directly — it produces intent phrases matched against pre-approved tables. Nemotron-Safety-3.5 filters all player-facing output.
**Philosophy:** No neural nets for action selection. Vectors + patterns + evolution. The LLM compiles, the vector DB executes.

---

## THE VISION

This is **dynamic machine learning in a novel form** where:

1. The **training signal** is the stream of consciousness — each thought is a training example
2. The **loss function** is play quality — novelty, specificity, engagement, spatial awareness
3. The **gradient** is prompt/parameter adjustment — applied every 30 seconds by the Conductor
4. The **model update** happens continuously — reflex compilation, policy evolution, trust scoring, temporal learning, LoRA fine-tuning
5. The **improvement target** is qualitative — better thoughts, not lower loss

The Conductor doesn't just collect data — it actively shapes what data is produced by modifying the conditions under which thoughts are generated. It's a director guiding an improvisational actor: the actor performs, the director watches and adjusts the motivation, the actor's next performance is different.

Five subsystems transform this from idea to reality:

```
┌─────────────────────────────────────────────────────────────┐
│                    THE DYNAMIC ML LOOP                        │
│                                                              │
│   ┌──────────────┐     ┌──────────────┐     ┌────────────┐  │
│   │  REFLEX      │     │  EVOLUTION   │     │  TRUST     │  │
│   │  COMPILER    │     │  ENGINE      │     │  SCORER    │  │
│   │              │     │              │     │            │  │
│   │ Thoughts →   │     │ Action       │     │ Conductor  │  │
│   │ .nail        │     │ policies     │     │ learns     │  │
│   │ reflexes     │     │ breed better │     │ which mods │  │
│   │ (<1ms, $0)   │     │ over time    │     │ work where │  │
│   └──────┬───────┘     └──────┬───────┘     └─────┬──────┘  │
│          │                     │                   │         │
│          └────────────┬────────┴───────────────────┘         │
│                       ▼                                      │
│              ┌──────────────────┐                            │
│              │  TEMPORAL →      │     ┌──────────────────┐   │
│              │  VECTOR PIPELINE │     │  LoRA TRAINING   │   │
│              │                  │     │  PIPELINE        │   │
│              │  Play rhythms →  │     │                  │   │
│              │  bge-m3 →        │     │  Thought         │   │
│              │  Vectorize →     │     │  journals →      │   │
│              │  pattern recall  │     │  Granite 3.1     │   │
│              └────────┬─────────┘     │  LoRA adapter    │   │
│                       │               └────────┬─────────┘   │
│                       ▼                        ▼             │
│              ┌────────────────────────────────────────┐      │
│              │     LOCAL THINKER (the model)          │      │
│              │     Gets better every 30 seconds       │      │
│              │     Forever.                            │      │
│              └────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## OUTPUT FORMAT

For each of the five tasks, produce:

### 1. Architecture Document (~500-800 words)
- ASCII data flow diagram
- Component list with responsibilities
- Integration points with existing code (reference specific files)
- Design decisions with justifications

### 2. Interface Definitions (~200-400 words)
- Python class/function signatures with type hints
- Data schemas (dataclasses, TypedDicts, or Pydantic models)
- `.bottle` message formats for inter-component communication
- SQLite/Vectorize schema extensions

### 3. Implementation Stubs (~200-400 words)
- Key functions with docstrings and `pass` bodies
- TODO markers for complex logic
- Configuration constants at the top

### 4. Acceptance Test Specification (~100-200 words)
- Concrete, measurable success criteria
- Test procedure (how to verify each criterion)
- Dependencies and prerequisites

---

## QUALITY BAR — WHAT "DONE" LOOKS LIKE

**The design is complete when a competent Python developer can:**

1. Read each design document and understand what to build without asking questions
2. Implement each subsystem from the interface definitions and stubs
3. Run the acceptance tests and get unambiguous pass/fail results
4. Wire each subsystem into the existing cognition codebase at the specified integration points
5. Verify the dynamic ML loop closes: thoughts → reflexes → evolution → trust → temporal patterns → LoRA → better thoughts

**The design is excellent when:**

- Every architectural decision references evidence from the deep dives (not invented from scratch)
- The three-gate pattern appears consistently across subsystems (check reflexes before LLM, check trust before applying, check patterns before deciding)
- The `.bottle` protocol is used for all inter-component communication
- Conservation laws are respected (token budget, action logging, identity tracking)
- The system degrades gracefully at every level (no ONNX → hash fallback; no Ollama → API fallback; no Vectorize → local search fallback)
- The character of Lucineer is preserved throughout (the foreman who leaves things unfinished — even the ML system follows this philosophy: every model is unfinished, every policy has gaps, every reflex has an escape hatch)

**The design is inspirational when:**

- You can see how this becomes a genuinely novel form of machine intelligence — not a fine-tuned model, not a RAG system, not an agent framework, but something new: a system where the training signal IS the experience and the gradient IS the directing intelligence
- The architecture makes someone who understands ML say "wait, that's not how ML works" — and then understand why it's interesting anyway
- The constraint of an RTX 4050 laptop becomes a feature, not a limitation (reflex-dominated execution is cheap, local, private, fast — and it gets better with use, which cloud models can't promise)

---

## FINAL INSTRUCTION

This system embodies a simple, radical idea: **the model is always training, always playing, always being directed.** The Conductor shapes the conditions under which thoughts are generated. The thoughts become reflexes. The reflexes become policies. The policies become a model. The model generates better thoughts. The loop never stops.

Five subsystems. One loop. Design them as if the entire project depends on it — because it does.

Every token counts. Be dense, precise, and inspirational.

**Begin.**
