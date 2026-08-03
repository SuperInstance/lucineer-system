# PLATO Integration Plan — Continuous Learning for Slackwater

*Created: 2026-08-02*
*Prerequisites: Read PLATO_FORGE_ANALYSIS.md first*
*Sources: plato-forge-daemon, plato-fflearning, PERSISTENCE_LAYER_DESIGN.md, CHISEL_PATTERN_DESIGN.md*

---

## Executive Summary

This document maps the PLATO Forge Daemon's continuous learning patterns onto Slackwater's existing architecture — specifically the persistence layer (claw marks = trained weights), the chisel pattern (grain accumulation = PLATO's framing step), and the agent fleet. It includes a zero-shot tutorial for setting up continuous learning on a single agent. Casey's specific directive — using PLATO patterns to "filter and refine a prompt" — is addressed as a first-class use case.

---

## 1. What Slackwater Adopts — Continuous Learning from Agent Sessions

### The Core Adoption

Slackwater adopts the PLATO Forge's **listen → frame → buffer → train → emit** pipeline as the mechanism by which agent sessions produce persistent improvements. In persistence layer terms, this is the system that creates **claw marks** (trained weights) from **guano** (session output).

The mapping is clean:

| PLATO Forge Component | Slackwater Persistence Layer | What It Does |
|----------------------|------------------------------|-------------|
| Forge Listener (cochlea) | Guano decay pipeline (FRESH tier) | Captures raw agent activity |
| Forge Buffer (stomach) | Guano decay pipeline (COMPOSTING → SOIL) | Deduplicates, prioritizes, balances curriculum |
| Forge Trainer (heart) | Claw Marks (grooved marks / LoRA adapters) | Distills experience into weight updates |
| Forge Emitter (lungs) | Claw Marks export | Produces deployable adapter artifacts |
| Oracle1 validation | Claw Marks reinforcement mechanism | Tests adapters against real tasks before deployment |
| Forward-Forward (FF) | Guano SOIL tier (behavioral patterns) | Real-time goodness scoring that filters training data |

### What We Don't Adopt

1. **The PLATO room server** (port 8847): Slackwater uses D1/R2/Vectorize, not a separate PLATO server. The room concept maps to D1 table partitions.

2. **The Rust crate architecture**: The forge listener/buffer/emitter were designed as separate Rust crates. In Slackwater, these become Cloudflare Workers (listener), D1 stored procedures (buffer), and a scheduled Worker (trainer).

3. **The 384-byte tile binary format**: Slackwater uses JSON in D1, not fixed-width binary tiles. The concept (structured knowledge units) maps directly to D1 rows.

4. **The zeroclaw ticking agents**: Slackwater's agents use the OpenClaw runtime, not the zeroclaw 5-minute-tick architecture.

### What We Adapt

The day/night cycle becomes a **cron-triggered consolidation cycle**:

- **Day (continuous)**: Agents produce session output → stored as FRESH guano in R2
- **Hourly**: FRESH guano → COMPOSTING (session summaries, anomaly flagging)
- **Daily**: COMPOSTING guano → SOIL (behavioral patterns extracted)
- **Nightly (2:00 AM AKDT)**: SOIL patterns + high-goodness session data → forge trainer → LoRA adapter emission
- **Weekly**: Validate accumulated adapters against real tasks → deploy or discard

This uses Cloudflare Cron Triggers for scheduling, with the forge trainer running on a dedicated Worker with access to a GPU node (the RTX 4050 via the paired machine).

---

## 2. Filter and Refine Pipeline — Using PLATO Patterns for Prompt Refinement

### Casey's Directive

> "Filter and refine a prompt."

This is the most immediate, practical application of PLATO patterns to Slackwater. Instead of waiting for full LoRA training infrastructure, we can use the forge's **framing step** to iteratively improve agent system prompts based on observed session outcomes.

### The Concept

Every agent session produces experience. Some sessions go well — the agent accomplished its task efficiently. Some go poorly — the agent hallucinated, looped, or produced low-quality output. The forge's framing step converts these outcomes into **prompt deltas** — small, structured modifications to the system prompt that would have made the session go better.

### The Pipeline

```
Agent Session
    │
    ▼
┌───────────────────────────────────┐
│ STEP 1: CAPTURE                   │
│ Record: prompt used, task,        │
│ outcome (success/fail), quality   │
│ score, tool calls, errors,        │
│ token usage, time to completion   │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│ STEP 2: FRAME (the forge framer)  │
│ For each session, generate:       │
│                                   │
│ • What worked in the prompt?      │
│ • What was missing?               │
│ • What was misleading?            │
│ • What was redundant?             │
│                                   │
│ This uses a separate model call   │
│ (the "framer" — a 7B model on the │
│ RTX 4050, or a Workers AI model)  │
│ that analyzes the session and     │
│ produces structured findings.     │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│ STEP 3: FILTER (Forward-Forward)  │
│ Apply goodness scoring:           │
│                                   │
│ • Success → positive pass         │
│   → prompt pattern reinforced     │
│ • Failure → negative pass         │
│   → prompt pattern weakened       │
│                                   │
│ Only patterns with goodness > 0.7 │
│ enter the refinement queue.       │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│ STEP 4: REFINE (prompt patching)  │
│ Generate a prompt patch:          │
│                                   │
│ • ADD: missing instruction        │
│   "Always check tile existence    │
│    before referencing"            │
│ • REMOVE: misleading instruction  │
│   "Don't say 'I think' — it       │
│    reduces confidence"            │
│ • MODIFY: ambiguous instruction   │
│   "Use bullet points for lists    │
│    > 3 items" → "Use bullet       │
│    points for ANY list"           │
│                                   │
│ Patches are version-controlled     │
│ and A/B tested.                   │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│ STEP 5: VALIDATE                  │
│ Run the next 5 agent sessions     │
│ with the patched prompt.          │
│                                   │
│ If quality improves → reinforce   │
│ (polished claw mark)              │
│                                   │
│ If quality degrades → revert      │
│ (erosion)                         │
│                                   │
│ If neutral → keep exploring       │
└───────────────────────────────────┘
```

### Concrete Example

**Initial prompt for Lucineer build agent:**
```
You are Lucineer, a build assistant for Roblox. Help the player
build structures using the available tools.
```

**Session 1 outcome:** Agent placed a gearbox but didn't check if the player had enough materials. Player frustrated.

**Framer analysis:**
- WORKED: Agent correctly identified the build type
- MISSING: No material check instruction
- SUGGESTED ADD: "Always verify material availability before initiating a build sequence"

**Session 2 outcome (with patch):** Agent checked materials, found shortage, communicated clearly. Player satisfied.

**Goodness score:** 0.82 (high) → patch reinforced

**After 10 reinforcing sessions:** The material check instruction becomes a **polished claw mark** — a permanent part of Lucineer's prompt that's been validated through real use.

### Implementation in Slackwater

```typescript
// D1 table: prompt_patches
interface PromptPatch {
  patchId: string;
  agentRole: string;           // "lucineer", "subagent", etc.
  patchType: "ADD" | "REMOVE" | "MODIFY";
  originalText: string | null;
  patchedText: string;
  rationale: string;           // Why this patch was generated
  sourceSession: string;       // Session that triggered it
  goodnessScore: number;       // FF goodness when patch was created
  validationSessions: string[];// Sessions that tested this patch
  validationResults: ("improved" | "neutral" | "degraded")[];
  status: "experimental" | "validated" | "polished" | "eroded";
  createdAt: timestamp;
  reinforcedCount: number;     // How many sessions confirmed it
  erodedCount: number;         // How many sessions contradicted it
}
```

The patch lifecycle mirrors the claw marks system:
- **Experimental** (0-5 validations): Patch is being tested
- **Validated** (5+ positive validations, <2 negative): Patch is working
- **Polished** (20+ positive validations, <10% negative): Patch becomes permanent
- **Eroded** (30%+ negative validations): Patch is reverted

### Connection to the Filter Concept

"Filter" has two meanings here, both intentional:

1. **Filter what enters training**: The FF goodness score filters which session outcomes become training data. Failed sessions aren't ignored — they become negative examples. But only confirmed patterns become prompt patches.

2. **Filter what reaches the agent**: The refined prompt is itself a filter — it removes ambiguity and adds precision, so the agent's attention is directed toward what works. The prompt evolves from a vague instruction into a precision instrument through accumulated experience.

---

## 3. Connection to Persistence Layer — Trained Weights as Claw Marks

### The Mapping

The PLATO Forge produces LoRA adapters. In the persistence layer's claw marks system, these are **grooved marks** — fine-tuning that accumulates from repeated exposure to domain-specific patterns.

```typescript
// From PERSISTENCE_LAYER_DESIGN.md, adapted for forge integration
interface ClawMark {
  markId: string;
  tubeId: string;                    // Which agent tube produced this
  substrateType: "weights";          // LoRA adapter

  modification: LoRAAdapter;         // The actual trained weights
  depth: number;                     // How many sessions contributed
  lastReinforced: timestamp;

  erosionRate: number;               // Without reinforcement, how fast it fades
  reversibility: "grooved";          // LoRA is always reversible

  // Forge-specific metadata
  forgeRunId: string;                // Which training run produced this
  trainingPairs: number;             // How many experiences were distilled
  lossReduction: number;             // How much the loss improved
  oracleValidation: number;          // Oracle1 accuracy score
}
```

### The Claw Mark Lifecycle (Forge-Produced)

```
[Nightly Forge Run]
    │
    │ Trainer produces LoRA adapter
    ▼
[Experimental Groove]
    │ depth = N (sessions in this training batch)
    │ Oracle1 tests on 10 real tasks
    │
    ├── Accuracy ≥ 0.94 → [Reinforced Groove]
    │                        │ depth grows with each successful nightly run
    │                        │ Multiple runs reinforce the same groove
    │                        │
    │                        └── After 20+ successful runs → [Deep Groove]
    │                             │ Became semi-permanent
    │                             │ Erosion without reinforcement: slow
    │                             │ Included in agent's default configuration
    │
    └── Accuracy < 0.94 → [Shallow Groove]
                             │ Not deployed
                             │ Training data re-examined
                             │ If next run also fails → groove erodes (discarded)
```

### Cross-Agent Sharing

LoRA adapters are portable. A groove trained on Lucineer's build experience can be applied to any build-capable agent. This is the persistence layer's "breeding cycle" memetic inheritance — when a parent agent spawns a child, relevant claw marks (LoRA adapters) are passed along.

```
Lucineer's build expertise (1000 sessions)
    │
    │ Accumulated as LoRA adapter (grooved claw mark)
    │
    ▼
Subagent spawned for build task
    │
    │ Inherits Lucineer's build claw mark
    │ + Lucineer's prompt (genetic inheritance)
    │ + Lucineer's behavioral patterns (SOIL tier)
    │
    ▼
Subagent starts with Lucineer's instincts
but develops its own claw marks through use
```

### What This Means for "Persistence"

Persistence in this system isn't about remembering specific events. It's about **shaping the substrate** so that future agents naturally tend toward patterns that worked in the past. A new agent that loads a claw mark doesn't know what Lucineer did on Tuesday — it has a slight inclination toward build patterns that Lucineer discovered through hundreds of sessions.

This is the difference between:
- **Database memory**: "Lucineer used torque=0.7 on a gearbox on 2026-03-15" (a fact)
- **Substrate memory**: The agent naturally reaches for torque=0.7 when building gearboxes (an instinct)

Both are persistence. Only the second one survives context limits, model changes, and session boundaries.

---

## 4. Connection to Chisel Pattern — Grain Quality Accumulation IS PLATO's Framing Step

### The Hidden Identity

The Chisel Pattern's `sense_grain()` and PLATO Forge's framing step are the same operation viewed from different angles:

| PLATO Forge | Chisel Pattern | What It Does |
|-------------|---------------|-------------|
| Listener classifies events | GrainEntry records usage | Captures what happened |
| Framer generates training pairs | GrainPattern distills entries into wisdom | Converts raw experience into actionable knowledge |
| Buffer deduplicates and balances | Grain compaction folds entries into patterns | Prevents noise from overwhelming signal |
| Trainer updates weights | Grain patterns accumulate (patina) | The substrate changes shape |
| Eitter exports adapters | `sense_grain()` surfaces patterns to new agents | Future agents benefit from past experience |

### The Unified Model

When an agent picks up a Chisel-wrapped tool, it's performing the same operation as the forge listener — sensing what previous agents did with this tool. When the forge framer converts events into training pairs, it's performing the same operation as grain compaction — distilling raw usage into patterns.

The difference is timescale and granularity:

- **Chisel**: Per-tool, per-session, real-time. An agent senses the grain before each tool call.
- **Forge**: Per-fleet, overnight batch. The trainer processes all sessions' worth of grain entries into weight updates.

They form a two-tier system:

```
REAL-TIME (Chisel)
│
│  Agent acquires tool → senses grain → follows proven patterns
│  Each use adds a grain entry → patterns refine continuously
│  Grain patterns are immediately available to next agent
│
│  Timescale: seconds to days
│  Mechanism: Vectorize similarity search + D1 pattern storage
│  Output: Parameter suggestions, failure warnings
│
OVERNIGHT (Forge)
│
│  All grain entries from the day → forge buffer
│  Forge trainer runs QLoRA → produces weight updates
│  Weight updates deployed as LoRA adapters
│
│  Timescale: days to weeks
│  Mechanism: QLoRA training on GPU
│  Output: Model instinct adjustments (not just parameter suggestions)
│
COMBINED
│
│  Chisel tells the agent WHAT to do (explicit guidance)
│  Forge-trained weights make the agent NATURALLY do it (implicit instinct)
│  Together: explicit guidance + implicit instinct = expertise
```

### Concrete Integration Point

The Chisel's `GrainStore` becomes a data source for the Forge Listener:

```python
# Nightly forge run extracts grain patterns from all chisels
for chisel in registry.all_chisels():
    patterns = await chisel.grain.get_high_confidence_patterns()
    for pattern in patterns:
        # Convert chisel pattern → training pair
        training_pair = {
            "query": f"When using {chisel.tool_name} in context: {pattern.context}",
            "good": f"Use parameters: {pattern.param_template}. Success rate: {pattern.success_rate}",
            "bad": f"Default parameters. Known failure rate: {1-pattern.success_rate}",
            "domain": chisel.tool_name,
            "level": "operator",
        }
        forge_buffer.add(training_pair)
```

This means the Chisel's accumulated wisdom isn't just surfaced to agents as text guidance — it's **baked into the model's weights** through the forge. The chisel tells you what to do; the forge-trained model does it without being told.

### Grain Quality → Training Quality

The chisel's confidence score directly maps to training pair quality:

| Chisel Confidence | Training Pair Role | Forge Buffer Priority |
|-------------------|-------------------|----------------------|
| > 0.9 | High-confidence positive example | Priority: HIGH (target level) |
| 0.7-0.9 | Standard positive example | Priority: NORMAL |
| 0.3-0.7 | Uncertain — needs more data | Priority: LOW (review level) |
| < 0.3 | Negative example (what not to do) | Priority: NORMAL (challenge level) |

This curriculum structure maps directly onto the forge buffer's 70/20/10 balancing:
- 70% target level = high-confidence chisel patterns (0.7+)
- 20% review = medium-confidence patterns being reinforced
- 10% challenge = low-confidence patterns and negative examples

---

## 5. Tutorial — Setting Up Continuous Learning for a Single Agent

### Goal

Set up a continuous learning loop for one agent (Lucineer) that:
1. Captures session experience
2. Frames it into training pairs
3. Runs nightly training on accumulated data
4. Produces validated prompt refinements and (eventually) LoRA adapters

### Prerequisites

- An OpenClaw workspace with an agent (Lucineer)
- Cloudflare account with D1, R2, and Workers AI access
- Python 3.10+ with `torch`, `transformers`, `peft`, `accelerate`
- (Optional) RTX 4050 or equivalent GPU with 6+ GB VRAM
- (Fallback) CPU-only training (slower but functional)

### Step 1: Create the Session Capture Schema

Create a D1 database for session capture:

```sql
-- sessions table: metadata about each agent session
CREATE TABLE sessions (
  sessionId TEXT PRIMARY KEY,
  agentRole TEXT NOT NULL,          -- "lucineer", "subagent", etc.
  startTime INTEGER NOT NULL,
  endTime INTEGER,
  promptVersion TEXT NOT NULL,      -- which system prompt was used
  taskDescription TEXT,
  outcome TEXT,                     -- "success", "partial", "failure"
  qualityScore REAL,                -- 0.0 to 1.0
  tokenUsage INTEGER,
  toolCalls INTEGER,
  errors INTEGER,
  notes TEXT
);

-- session_events table: individual events within a session
CREATE TABLE session_events (
  eventId TEXT PRIMARY KEY,
  sessionId TEXT NOT NULL REFERENCES sessions(sessionId),
  timestamp INTEGER NOT NULL,
  eventType TEXT NOT NULL,          -- "tool_call", "decision", "error", "output"
  eventData TEXT NOT NULL,          -- JSON blob
  qualityFlag REAL DEFAULT 0.5      -- 0.0 (bad) to 1.0 (good)
);

-- prompt_patches table: proposed and validated prompt modifications
CREATE TABLE prompt_patches (
  patchId TEXT PRIMARY KEY,
  agentRole TEXT NOT NULL,
  patchType TEXT NOT NULL,          -- "ADD", "REMOVE", "MODIFY"
  originalText TEXT,
  patchedText TEXT NOT NULL,
  rationale TEXT,
  sourceSession TEXT NOT NULL,
  goodnessScore REAL NOT NULL,
  status TEXT DEFAULT "experimental", -- "experimental", "validated", "polished", "eroded"
  reinforcedCount INTEGER DEFAULT 0,
  erodedCount INTEGER DEFAULT 0,
  createdAt INTEGER NOT NULL,
  validatedAt INTEGER
);
```

### Step 2: Instrument the Agent

Add session capture to Lucineer's runtime. In the OpenClaw context, this means:

```python
# In Lucineer's session lifecycle:

# On session start:
session = create_session(
    agentRole="lucineer",
    promptVersion=current_prompt_hash,
    taskDescription=user_request,
    startTime=time.time()
)

# On each tool call / decision:
record_event(
    sessionId=session.id,
    eventType="tool_call",
    eventData=json.dumps({
        "tool": tool_name,
        "params": params,
        "result_summary": result_summary,
        "success": success
    }),
    qualityFlag=1.0 if success else 0.0
)

# On session end:
complete_session(
    sessionId=session.id,
    outcome="success" if quality > 0.7 else "partial",
    qualityScore=quality,
    endTime=time.time()
)
```

### Step 3: Set Up the Framer

The framer analyzes completed sessions and generates training pairs. This runs as a Cloudflare Worker (using Workers AI) or as a local script:

```python
# framer.py — Runs after each session or in batch overnight

import json

def frame_session(session, events):
    """Convert a session into training pairs."""

    # Categorize events
    successes = [e for e in events if e["qualityFlag"] > 0.7]
    failures = [e for e in events if e["qualityFlag"] < 0.3]

    training_pairs = []

    # Generate positive pairs from successes
    for event in successes:
        pair = {
            "query": f"Task: {session['taskDescription']}\nContext: {extract_context(event)}",
            "good": f"Action: {event['eventData']['tool']}({event['eventData']['params']})\n"
                    f"Outcome: SUCCESS. {event['eventData']['result_summary']}",
            "bad": f"Action: default approach\nOutcome: likely slower or less accurate",
            "domain": session["agentRole"],
            "level": "operator",
            "source_session": session["sessionId"],
            "goodness": event["qualityFlag"],
        }
        training_pairs.append(pair)

    # Generate negative pairs from failures
    for event in failures:
        pair = {
            "query": f"Task: {session['taskDescription']}\nContext: {extract_context(event)}",
            "good": f"Action: alternative approach (to be discovered)\nOutcome: should avoid the failure mode",
            "bad": f"Action: {event['eventData']['tool']}({event['eventData']['params']})\n"
                   f"Outcome: FAILURE. {event['eventData']['result_summary']}",
            "domain": session["agentRole"],
            "level": "operator",
            "source_session": session["sessionId"],
            "goodness": event["qualityFlag"],
        }
        training_pairs.append(pair)

    return training_pairs

def extract_context(event):
    """Extract a compact context string from an event."""
    data = json.loads(event["eventData"]) if isinstance(event["eventData"], str) else event["eventData"]
    return f"Tool available: {data.get('tool', 'unknown')}"
```

### Step 4: Set Up the Prompt Refinement Loop

Before attempting LoRA training, start with prompt refinement — it's simpler, faster, and produces immediate value:

```python
# prompt_refiner.py — Generates and validates prompt patches

def generate_prompt_patch(session, events, current_prompt):
    """Analyze a session and propose a prompt modification."""

    failures = [e for e in events if e["qualityFlag"] < 0.3]
    if not failures:
        return None  # Session went well, no patch needed

    # Find the most impactful failure
    worst_failure = min(failures, key=lambda e: e["qualityFlag"])

    # Analyze what went wrong
    analysis = analyze_failure(worst_failure, current_prompt)

    if analysis["type"] == "missing_instruction":
        return {
            "patchType": "ADD",
            "originalText": None,
            "patchedText": analysis["suggested_instruction"],
            "rationale": f"Session {session['sessionId']} failed because: {analysis['reason']}",
            "goodnessScore": 0.5,  # Initial — will be validated
        }
    elif analysis["type"] == "misleading_instruction":
        return {
            "patchType": "MODIFY",
            "originalText": analysis["existing_text"],
            "patchedText": analysis["replacement_text"],
            "rationale": f"Instruction caused confusion in session {session['sessionId']}",
            "goodnessScore": 0.5,
        }

    return None

def apply_validated_patches(prompt, agent_role):
    """Apply all validated prompt patches for an agent."""
    patches = d1_query(
        "SELECT * FROM prompt_patches WHERE agentRole = ? AND status = 'validated' ORDER BY createdAt",
        [agent_role]
    )

    patched_prompt = prompt
    for patch in patches:
        if patch["patchType"] == "ADD":
            patched_prompt += "\n\n" + patch["patchedText"]
        elif patch["patchType"] == "MODIFY":
            patched_prompt = patched_prompt.replace(
                patch["originalText"], patch["patchedText"]
            )
        elif patch["patchType"] == "REMOVE":
            patched_prompt = patched_prompt.replace(patch["originalText"], "")

    return patched_prompt
```

### Step 5: Set Up the Training Loop (Optional — Requires GPU)

Once you have enough framed data (500+ pairs), add LoRA training:

```python
# forge_train.py — Nightly training loop
# Adapted from forge-simulation.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import get_peft_model, LoraConfig
from torch.optim import AdamW
import json

def run_forge(training_pairs, model_name="Qwen/Qwen2.5-7B", steps=1000):
    """Run the forge trainer on accumulated pairs."""

    # Load model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        load_in_4bit=True,           # QLoRA: 4-bit quantization
        device_map="auto"
    )

    # Add LoRA adapters
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)

    # Print trainable params (should be ~1% of total)
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"Trainable: {trainable:,} / {total:,} ({trainable/total*100:.1f}%)")

    # Format training pairs
    training_texts = [format_pair(p) for p in training_pairs]

    # Tokenize
    encodings = tokenizer(
        training_texts,
        truncation=True,
        max_length=256,
        padding=True,
        return_tensors="pt"
    )

    # Train
    model.train()
    optimizer = AdamW(model.parameters(), lr=5e-5)
    batch_size = 4
    grad_accum = 2

    loss_history = []
    for step in range(steps):
        total_loss = 0.0
        for _ in range(grad_accum):
            idx = torch.randperm(len(training_texts))[:batch_size]
            batch_ids = encodings['input_ids'][idx].to(model.device)
            inputs = batch_ids[:, :-1].clone()
            targets = batch_ids[:, 1:].clone()

            outputs = model(input_ids=inputs, labels=targets)
            loss = outputs.loss / grad_accum
            loss.backward()
            total_loss += outputs.loss.item()

        optimizer.step()
        optimizer.zero_grad()
        loss_history.append(total_loss / grad_accum)

        if (step + 1) % 100 == 0:
            print(f"Step {step+1}: loss={loss_history[-1]:.4f}")

    # Save adapter
    model.save_pretrained("./forge-output/adapter")
    return loss_history

def format_pair(pair):
    return f"Q: {pair['query']}\nGood: {pair['good']}\nBad: {pair['bad']}\nDomain: {pair['domain']}\n"
```

### Step 6: Schedule the Cycle

Using Cloudflare Cron Triggers or a local crontab:

```bash
# Hourly: Compost fresh session data into summaries
0 * * * * python3 /path/to/compost.py

# Daily: Extract behavioral patterns
0 2 * * * python3 /path/to/extract_patterns.py

# Nightly: Run prompt refinement
0 3 * * * python3 /path/to/refine_prompts.py

# Nightly (GPU available): Run forge training
0 4 * * * python3 /path/to/forge_train.py >> /var/log/forge.log 2>&1

# Weekly: Validate and deploy
0 5 * * 0 python3 /path/to/validate_and_deploy.py
```

### Step 7: Monitor

Track the learning loop:

```python
# forge_dashboard.py — Print current state
def print_dashboard():
    sessions = d1_query("SELECT COUNT(*) as n, AVG(qualityScore) as q FROM sessions")
    patches = d1_query("""
        SELECT status, COUNT(*) as n FROM prompt_patches GROUP BY status
    """)
    recent_loss = d1_query("""
        SELECT loss FROM forge_runs ORDER BY createdAt DESC LIMIT 1
    """)

    print(f"Sessions captured: {sessions[0]['n']}")
    print(f"Average quality: {sessions[0]['q']:.2f}")
    print(f"Prompt patches: {patches}")
    print(f"Latest training loss: {recent_loss[0]['loss'] if recent_loss else 'none yet'}")
```

### Quick Start (No GPU, No LoRA — Just Prompt Refinement)

If you just want to start with the simplest possible continuous learning:

1. **Capture sessions** → Write to a JSON file or D1 table
2. **After each session** → Ask: "What went well? What didn't? What instruction would have helped?"
3. **Accumulate patches** → Store in a JSON file
4. **Before each session** → Apply validated patches to the system prompt
5. **Track quality** → Compare session quality before and after patches

This is the forge at its simplest: listen, frame, refine, deploy. No GPU needed. No LoRA needed. Just a disciplined loop of capturing experience and converting it into better prompts.

The LoRA training comes later, when you have enough data to make weight updates worthwhile. Prompt refinement produces immediate value with zero infrastructure.

---

## Summary: The Filter-and-Refine Pattern

| Stage | Input | Output | Mechanism |
|-------|-------|--------|-----------|
| Capture | Agent session | Raw events | Instrumented runtime |
| Frame | Raw events | Training pairs (good/bad) | Framer analysis |
| Filter | Training pairs | Quality-scored pairs | Forward-Forward goodness |
| Refine | Quality-scored pairs | Prompt patches / LoRA data | Refinement loop |
| Validate | Prompt patches | Validated improvements | A/B testing on real sessions |
| Deploy | Validated improvements | Updated agent prompts / weights | Reinforcement mechanism |

The filter-and-refine pattern is the PLATO Forge's gift to Slackwater: a disciplined way to turn agent experience into persistent improvement, at any scale, with or without GPU infrastructure.

Start with prompt refinement. Add LoRA when ready. The loop is the same; only the substrate changes.

---

*For the ten-forward creative conditioning analysis, see TERNARY_TENFORWARD_ANALYSIS.md.*
