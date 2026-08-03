# Integration Plan — SuperInstance → Lucineer

**Goal:** Extract the best ideas from SuperInstance and adapt them for Lucineer's Game/Thinker/Conductor/Journal stack without adopting the incomplete code.

---

## Phase 1: Immediate (This Week)

### 1.1 Adopt the `.bottle` Protocol

**What:** Copy `bottle_protocol.py` (180 lines, zero deps) into our codebase.

**Where:** `lucineer-system/src/communication/bottle.py`

**Why:** Replace ad-hoc JSONL event passing with typed YAML messages. Get confidence scores, reference chains, and six semantic kinds (observation, hypothesis, experiment, result, command, config).

**How:**
```python
# Conductor sends a build command to Thinker
from bottle import command, observe, result

cmd = command(
    source="conductor",
    action="generate.build",
    target="thinker",
    params={"game_type": "obby", "difficulty": "medium"}
)
cmd.save("lucineer-system/bottles/")

# Thinker posts an observation
obs = observe(
    source="thinker",
    what="obby builds with >500 parts take >30s to generate",
    data={"avg_parts": 750, "avg_time_ms": 34000},
    confidence=0.85,
    tags=["performance", "obby"]
)
obs.save("lucineer-system/bottles/")
```

**Effort:** 2 hours (copy, adapt, wire into existing components)

### 1.2 Adopt Conservation Laws as Design Constraints

**What:** Write these into our AGENTS.md as hard constraints:

1. **Token conservation:** Thinker operates within a per-build token budget. Conductor throttles if exceeded.
2. **Action conservation:** Every build action produces a journal entry. No orphan executions.
3. **Identity conservation:** Every action attributable to a session ID. No anonymous builds.
4. **Evolution conservation:** Skill library changes go through human review.

**Effort:** 30 minutes (documentation only)

---

## Phase 2: Short-Term (2-4 Weeks)

### 2.1 Three-Gate Pattern for Build Pipeline

**What:** Apply the Rust → Python → LLM cascade to Lucineer's build command validation.

**Adaptation for Roblox/Lua:**

| SuperInstance Gate | Lucineer Gate | Implementation |
|--------------------|---------------|----------------|
| Gate 1: Rust guard (~50µs) | Gate 1: Lua validator (~1ms) | Validate coordinates, materials, sizes are within bounds |
| Gate 2: Python cache (~200µs) | Gate 2: Vectorize cache (~5ms) | Check if we've built something similar (bge-m3 embedding) |
| Gate 3: LLM (~500ms) | Gate 3: Brain/DeepInfra (~2-5s) | Novel build generation via multi-model routing |

**Cache trajectory projection for Lucineer:**
- Week 1: 0% cache hit (cold)
- Week 2: 30% (common build patterns cached)
- Month 1: 60%+ (most obby/RPG/simulator patterns cached)
- Month 3: 80%+ (only novel build requests hit the LLM)

**Effort:** 1 week (implement cache layer, wire into Conductor)

### 2.2 Position-Aware Embeddings for Hot-Path Caching

**What:** Implement SuperInstance's 64-dim position-aware hash embedding as a pre-filter before Vectorize.

**Why:** 1µs latency vs 5-10ms for Vectorize. For exact-match or near-exact build requests, this saves a round-trip.

**Implementation:**
```python
def position_aware_embed(intent: str, dim: int = 64) -> np.ndarray:
    """Position-aware hash embedding. 44% top-1, 1µs, zero deps."""
    vec = np.zeros(dim, dtype=np.float32)
    for i, ch in enumerate(intent):
        for d in range(dim):
            vec[d] += ord(ch) * ((d * 31 + i * 17) % 256) / 255.0
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec
```

**Two-tier cache:**
1. Position-aware hash (1µs) → exact match check
2. Vectorize bge-m3 (5ms) → semantic similarity search
3. Brain/DeepInfra (2-5s) → novel generation

**Effort:** 3 days (implement, test, wire into pipeline)

### 2.3 CAPABILITIES.yaml for Component Discovery

**What:** Each Lucineer component declares its capabilities in a standard format.

**Example:**
```yaml
# Thinker/CAPABILITIES.yaml
agent: thinker
version: "0.3.0"
capabilities:
  - action: "generate.build"
    description: "Generate Roblox build commands from natural language"
    input_schema: "intent: string, context?: object"
    output_schema: "commands: BuildCommand[], confidence: float"
  - action: "estimate.complexity"
    description: "Estimate build complexity and token cost"
    input_schema: "intent: string"
    output_schema: "complexity: float, estimated_tokens: int"
channels:
  - type: "bottle"
    path: "lucineer-system/bottles/"
```

**Why:** Conductor reads these to know who can do what. Enables dynamic routing.

**Effort:** 1 day (define format, write for Thinker/Conductor/Journal/Creative)

---

## Phase 3: Medium-Term (1-3 Months)

### 3.1 Semantic Reflex Cache (pincherOS pattern)

**What:** Build a persistent cache of build commands indexed by intent embedding.

**Storage:** Cloudflare D1 (metadata) + Vectorize (embeddings) + R2 (full results)

**Schema:**
```sql
CREATE TABLE reflexes (
    id TEXT PRIMARY KEY,
    intent TEXT NOT NULL,
    intent_hash TEXT NOT NULL,
    build_commands JSON NOT NULL,
    embedding BLOB NOT NULL,
    confidence REAL DEFAULT 0.5,
    invoke_count INTEGER DEFAULT 0,
    last_invoked TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    game_type TEXT,
    complexity REAL
);
```

**Flow:**
1. Thinker generates build commands
2. Store in reflex cache with embedding
3. Next similar request → cache hit → skip Thinker entirely
4. Over time: 60-80% of build requests served from cache

**Effort:** 1 week

### 3.2 Observation Stream for Analytics

**What:** Log every build decision as a structured observation (JSONL).

**Format (inspired by SuperInstance's observation stream):**
```json
{
    "timestamp": "2026-08-03T12:00:00Z",
    "gate": "deep_loop",
    "intent": "build a medium difficulty obby with 10 stages",
    "matched_reflex": null,
    "generated_commands": 42,
    "exit_code": 0,
    "duration_ms": 3400,
    "tokens_used": 850,
    "cache_similarity": 0.32,
    "confidence": 0.91,
    "game_type": "obby",
    "model": "qwen3-coder-480b"
}
```

**Use:** Feed to a future "Lucineer Learns" feature — identify patterns, propose optimizations.

**Effort:** 2 days (logging) + ongoing analysis

### 3.3 The Self-Improvement Loop (metal-lathe pattern)

**What:** A periodic analysis of the observation stream that proposes optimizations.

**Design (adapted from SuperInstance ARCHITECTURE-V2.md):**

1. **OBSERVE:** "Over 1000 builds, obby generation averages 3.4s and 850 tokens. Simulator averages 1.2s and 300 tokens."
2. **QUESTION:** "Why is obby generation 3× slower?"
3. **HYPOTHESIZE:** "Obby requires spatial reasoning that triggers larger model (480B). Try routing to K3 (spatial specialist) instead."
4. **TEST:** Route 10% of obby requests to K3. Measure quality + speed.
5. **PROPOSE:** If K3 is faster with equal quality → propose routing change.
6. **REVIEW:** Human reviews proposal. Approved → update routing config.

**Anti-oscillation:** Minimum 1000 builds between config changes for the same parameter. A/B canary (10%) before full promotion.

**Effort:** 2 weeks (analysis pipeline + proposal format + review UI)

---

## Phase 4: Long-Term (3-6 Months)

### 4.1 Multi-Agent Coordination (PLATO pattern)

**What:** Multiple Thinker instances specializing in different game types.

**Design:**
- Thinker-Obby: specialized in obstacle course spatial reasoning
- Thinker-RPG: specialized in narrative + environment builds
- Thinker-Simulator: specialized in UI + economy systems
- Conductor routes build requests to the right specialist

**Coordination via rooms:** When a build spans genres (e.g., RPG with minigame), both Thinker-RPG and Thinker-Obby enter a "room" and share context via `.bottle` messages.

### 4.2 Skill Pack Evolution

**What:** Versioned, forkable skill libraries inspired by git-native agents.

**Design:**
- Each game type has a skill pack (JSONL of intent → build command mappings)
- Skill packs stored as versioned files in R2
- New patterns auto-promoted from observation stream (after human review)
- Fork a skill pack for a specific creator's style

### 4.3 Cross-Session Memory Migration

**What:** `.nail`-like portable memory files.

**Design:**
- Export a user's build history + preferences as a portable file
- Import on a different Roblox account or server
- Agent remembers your style without retraining

---

## What We're NOT Adopting

| SuperInstance Feature | Reason |
|----------------------|--------|
| lever-runner code | Shell-focused; we need Lua/build execution |
| pincherOS code | Core matching path broken; we have Vectorize |
| PLATO | Doesn't exist as working code |
| metal-lathe | Not implemented; we'll build our own analytics |
| CUDA/GPU tile stack | Overkill for our scale |
| Conservation-spectral-topology-rs | Formal verification not needed yet |
| The fork fleet (flux-*, cuda-*) | 69 single-file crates, zero users |
| Spectral isomorphism | Proven trivial by their own experiments |
| compiled-policy-c | We don't target microcontrollers |
| ZeroClaw Arena | Game learning is interesting but not our focus |

---

## Adoption Priority Matrix

| Feature | Impact | Effort | Priority |
|---------|--------|--------|----------|
| `.bottle` protocol | Medium | 2 hrs | 🔴 P0 — Immediate |
| Conservation laws as constraints | Medium | 30 min | 🔴 P0 — Immediate |
| Three-gate pattern | High | 1 week | 🟡 P1 — This month |
| Position-aware embeddings | Medium | 3 days | 🟡 P1 — This month |
| CAPABILITIES.yaml | Low | 1 day | 🟡 P1 — This month |
| Semantic reflex cache | High | 1 week | 🟢 P2 — Next quarter |
| Observation stream | Medium | 2 days | 🟢 P2 — Next quarter |
| Self-improvement loop | High | 2 weeks | 🟢 P2 — Next quarter |
| Multi-agent coordination | High | 1 month | 🔵 P3 — Future |
| Skill pack evolution | Medium | 1 month | 🔵 P3 — Future |
| Cross-session migration | Low | 2 weeks | 🔵 P3 — Future |

---

## Success Metrics

After adoption:

| Metric | Current | Target (3 months) | How |
|--------|---------|-------------------|-----|
| Build cache hit rate | 0% | 60%+ | Three-gate + reflex cache |
| Avg build generation time | 3-5s | <1s (cached), <3s (novel) | Cache layer |
| Avg tokens per build | ~800 | <300 (cached), <800 (novel) | Cache bypass |
| Build quality consistency | Variable | Measurable | Observation stream + analytics |
| Component coordination | Ad-hoc JSONL | Typed `.bottle` messages | Protocol adoption |

---

*Integration plan based on analysis of SuperInstance ecosystem (2026-08-03). See [analysis.md](analysis.md) for full details.*
