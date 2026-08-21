# Architecture Analysis: confidence-cascade

## Repository Metadata

| Field | Value |
|-------|-------|
| **Repo** | `SuperInstance/confidence-cascade` |
| **Language** | Rust (edition 2021) |
| **Version** | 0.1.0 |
| **License** | MIT |
| **Dependencies** | Zero external crates |
| **LOC (source)** | ~280 lines (`src/lib.rs`) |
| **Tests** | 22 unit tests, all passing |
| **CI** | GitHub Actions: check, test, clippy (deny warnings), fmt |
| **GC Tier** | Hot (actively maintained) |

---

## 1. Purpose and Scope

`confidence-cascade` is a **conversation engine for multi-agent systems**. It models dialogue not as sequential turn-taking (Agent A → Agent B → Agent C) but as **simultaneous beat-based interaction**, where all agents speak at once and then reconcile.

The crate answers a specific question: *How do you structure conversation between N autonomous agents so that it stays dynamic, self-balancing, and never deadlocks into monoculture?*

The answer combines three mathematical foundations:
1. **Z₃ cyclic group theory** — the only algebraic structure on {-1, 0, +1}
2. **Rock-Paper-Scissors (RPS) dominance dynamics** — self-balancing population waves
3. **Fibonacci timing (Pisano period mod 3 = 8)** — natural rhythm that prevents stalling

## 2. Architecture Overview

The entire crate is a single file (`src/lib.rs`) with zero external dependencies. This is intentional — it's a foundational primitive that other crates build upon.

### Module Structure

```
confidence-cascade/
├── src/
│   └── lib.rs          # All types, logic, and tests (single-file crate)
├── Cargo.toml          # Package manifest (no dependencies)
├── Cargo.lock          # Lock file (empty deps)
├── .github/workflows/
│   └── ci.yml          # 4 CI jobs: check, test, clippy, fmt
├── .gcconfig           # Fleet garbage collection config (tier: hot)
├── AGENTS.md           # SuperInstance fleet coordination metadata
├── CONTRIBUTING.md     # Contribution guidelines
└── README.md           # User-facing documentation
```

### Key Types

The crate exports **four primary types** and **one module-level engine**:

#### `Speaker` — The Agent Atom

```rust
pub struct Speaker {
    pub id: usize,
    pub name: String,
    pub state: i8,                // -1=contrarian, 0=reflecting, +1=agreeing
    pub energy: f64,              // 0.0-1.0, affects tempo and assertiveness
    pub trust: u8,                // 0-255, affects how much they listen
    pub dominance: f64,           // Running average of RPS win rate
    pub last_output: Option<String>,
    pub prediction: Option<Prediction>,
    pub prediction_accuracy: f64, // Exponential moving average
    pub ticks_speaking: u64,
    pub ticks_silent: u64,
}
```

A Speaker is a stateful agent with:
- **Ternary state** (-1, 0, +1) — their current stance
- **Energy** — a resource that depletes and replenishes, affecting assertiveness
- **Trust** — social credit that erodes when they lose RPS exchanges
- **Dominance** — exponential moving average of how often they "win"
- **Prediction tracking** — they simulate what others will say, then measure accuracy

Key methods:
- `predict(&mut self, others: &[Speaker])` — forecast other agents' states
- `speak(&mut self) -> Utterance` — produce output based on state + energy
- `react_to(&mut self, other: &Speaker)` — RPS interaction update
- `reconcile(&mut self, actual: &[i8]) -> f64` — compare prediction to reality

#### `TenForward` — The Conversation Engine

```rust
pub struct TenForward {
    pub speakers: Vec<Speaker>,
    pub tick: u64,
    pub history: Vec<Round>,
    pub bpm: f64,               // Adapts to energy (60-120)
    pub rhythm_period: usize,   // Default 8 (Pisano period mod 3)
}
```

The engine runs **five-phase rounds**:

```
Phase 1: T-minus — Each agent predicts what others will say
Phase 2: T-0     — All agents speak SIMULTANEOUSLY (no queue)
Phase 3: T-plus  — Pairwise RPS interactions (who beat whom)
Phase 4: T-plus  — Reconcile predictions vs reality
Phase 5: Periodic — Fibonacci tunnel: every 8 ticks, reflectors commit
```

#### `Round` — One Beat of Conversation

```rust
pub struct Round {
    pub tick: u64,
    pub utterances: Vec<Utterance>,
    pub state_snapshot: Vec<(usize, i8)>,
    pub energy_avg: f64,
    pub coherence: f64,            // 1/(1+variance) — alignment measure
    pub rps_dominant: Option<i8>,  // Which state is "winning"
}
```

#### `SessionSummary` — Run-Level Statistics

```rust
pub struct SessionSummary {
    pub rounds: u64,
    pub initial_states: Vec<i8>,
    pub final_states: Vec<i8>,
    pub avg_dominance: f64,
    pub avg_prediction_accuracy: f64,
    pub dominance_cycles: usize,
    pub bpm_final: f64,
}
```

## 3. Design Patterns

### Pattern 1: Speculation-First Perception
Every agent predicts what others will say *before* they speak. This mirrors speculative execution in CPUs — you commit to a prediction and roll back if wrong. The `prediction_accuracy` field creates an evolutionary pressure: agents that read the room well become more confident.

### Pattern 2: Rock-Paper-Scissors Self-Balancing
Instead of a moderator or queue, social dynamics emerge from pairwise RPS interactions:
- Contrarian (-1) beats Agreeing (+1) — challenges break consensus
- Agreeing (+1) beats Reflecting (0) — support draws out the hesitant
- Reflecting (0) beats Contrarian (-1) — patience disarms aggression

This creates **limit cycle dynamics** — populations oscillate rather than converge to a fixed point.

### Pattern 3: Fibonacci Tunneling
Agents stuck in reflection (state 0) with sufficient energy get force-committed every 8 ticks. The number 8 comes from the **Pisano period for mod 3**: the ternary Fibonacci sequence `1, 1, -1, 0, -1, -1, 1, 0` has period exactly 8. This is a mathematical escape hatch — it's not arbitrary, it's the natural rhythm of ternary systems.

### Pattern 4: Energy Economics
- **Winning** an RPS exchange costs nothing (gains +0.05 energy)
- **Losing** costs trust (−5 per loss) and potentially forces state collapse
- **Dominance** is exponentially smoothed (factor 0.9) — recent exchanges matter more
- **BPM adapts to average energy**: `bpm = 60 + energy_avg × 60`, giving a 60–120 range

### Pattern 5: Anti-Monoculture Pressure
The README documents experiments showing that without active countermeasures, 4-agent conversations lock into monoculture by tick 35. The engine prevents this through:
- Energy decay (dominant speakers become less assertive)
- Trust realignment (low-trust agents reset to reflection)
- The Fibonacci tunnel (periodic forced commitment breaks stalemates)

### Pattern 6: Zero-Dependency Crate
The `Cargo.toml` has no `[dependencies]` section. This is a pure-logic crate — no serde, no tokio, no nothing. It's designed to be a foundational primitive that higher-level crates compose.

## 4. The RPS Interaction Matrix

The entire social dynamic emerges from this 3×3 table:

| Speaker \ Other | -1 (Contrarian) | 0 (Reflecting) | +1 (Agreeing) |
|-----------------|:---:|:---:|:---:|
| **-1 (Contrarian)** | Tie → reflect | **Lose** | **Win** |
| **0 (Reflecting)** | **Win** | Tie → reflect | **Lose** |
| **+1 (Agreeing)** | **Lose** | **Win** | Tie → reflect |

Key observations:
- **Ties** push agents toward reflection (state 0) — agreement is boring
- **No dominant strategy exists** — this is the fundamental theorem of RPS
- **Periodic waves** emerge in large populations — documented as ~50-tick cycles

## 5. Prediction Model

The current prediction model is deliberately simple:

```rust
// Assume others stay in current state, unless they've been silent >5 ticks
if o.ticks_silent > 5 { 0 } else { o.state }
```

This is a **momentum predictor** — it assumes agents will continue doing what they're doing. The elegance is in the accuracy tracking: `prediction_accuracy = old × 0.8 + new × 0.2`, creating an exponentially-weighted moving average that rewards consistent reading of the room.

The prediction model is the obvious extension point for more sophisticated agents.

## 6. Output Generation

The `speak()` method generates output purely from state and energy:

| State | Energy > 0.7 | Energy 0.3–0.7 | Energy < 0.3 |
|-------|-------------|----------------|--------------|
| -1 | "Wait, that's not right. Disagree." | "I see it differently. Disagree." | "Maybe, but consider this. Disagree." |
| 0 | "Hmm. Let me think about that... interesting" | "Hmm. There's something there" | "Hmm. I need a moment on this one" |
| +1 | "YES. Exactly that. Right." | "That tracks. Right." | "Fair point. Right." |

This is clearly placeholder output — in a real integration, `speak()` would be overridden or extended to call an LLM.

## 7. Dependencies and Integrations

### Internal Fleet Dependencies (SuperInstance Ecosystem)

The crate sits in the middle of a layered architecture:

**Foundation layer (below):**
- `ternary-cell` — 3-byte agent atoms for million-instance scale
- `ternary-predict` — prediction-first perception (the "shoe protocol")
- `ternary-speculate` — speculative sync and shadow partners
- `ternary-motion` — tracking where speakers are heading

**DJ metaphor layer (above):**
- `ternary-tempo` — BPM that adapts to conversation energy
- `ternary-mixer` — multi-channel blend of speakers
- `ternary-crossfader` — smooth transitions between dominant speakers

**Referenced documents:**
- `TEN-FORWARD.md` in `construct-coordination` — full architecture doc
- `SPIRAL-6-FINDINGS.md` — monoculture experiment results
- `NEGATIVE-SPACE-EMERGENCE-PAPER.md` — formal science paper

### External Dependencies
**None.** Zero crates in `Cargo.toml`. This is pure Rust with no I/O, no async runtime, no serialization.

## 8. Build and Test

The CI pipeline is strict:
- **cargo check** — compilation verification
- **cargo test** — all 22 tests must pass
- **cargo clippy** — with `-D warnings` (warnings are errors)
- **cargo fmt** — `--check` mode (formatting enforced)

The test suite covers:
- Speaker construction and builder methods (4 tests)
- Prediction and reconciliation (3 tests)
- RPS win/lose/tie dynamics (3 tests)
- TenForward construction variants (3 tests)
- Round execution and metrics (5 tests)
- Multi-speaker scenarios (2 tests)
- Fibonacci tunneling (1 test)
- BPM adaptation (1 test)

## 9. What Problems It Solves

### Problem 1: Turn-Taking Is Unnatural
Standard multi-agent chat is ping-pong. Ten-Forward models conversation as **simultaneous expression with post-hoc reconciliation** — closer to how real group conversations work.

### Problem 2: Monoculture Lock-In
When 3 agents agree and 1 disagrees, the dissenter gets crushed permanently. The anti-monoculture mechanisms (energy decay, trust realignment, mutation via the Fibonacci tunnel) keep conversations alive indefinitely.

### Problem 3: Conversation Stalling
When all agents enter reflection (state 0), the conversation dies. The Fibonacci tunnel (period 8) mathematically guarantees that stuck reflectors will be force-committed.

### Problem 4: No Natural Rhythm
Without a timing model, conversations have no cadence. The BPM-adaptive system ties conversation tempo to energy levels — excited conversations run at 120 BPM, calm ones at 60.

## 10. Limitations and Extension Points

### Output Is Placeholder
The `speak()` method returns templated strings. Real integration requires either:
- Trait-based extension (inject an LLM-backed speaker)
- Callback architecture (emit state, receive generated text)
- Composition with a `ternary-mixer` crate that handles actual text generation

### Prediction Is Naive
The momentum predictor (`assume current state continues`) is the simplest possible model. Richer prediction could use:
- Markov chains over state history
- Neural state prediction
- Theory-of-mind modeling

### No Persistence
Sessions are entirely in-memory. There's no save/load, no replay, no streaming. History grows unboundedly in `Vec<Round>`.

### Single-Threaded
All interactions are synchronous. For real-time use, you'd need to wrap the engine in an async runtime.

### No I/O
The crate has no networking, no IPC, no file I/O. It's a pure compute engine that must be embedded in a host application.

## 11. Code Quality Assessment

**Strengths:**
- `#![forbid(unsafe_code)]` — memory safety guaranteed by the type system
- Zero dependencies — minimal attack surface, fast compile, easy to audit
- Comprehensive doc comments at module and type level
- 22 tests covering all public API surface
- Clean separation of concerns: Speaker logic, engine orchestration, and metrics

**Observations:**
- The `react_to` method constructs a throwaway `Speaker` for each pairwise interaction during round execution (Phase 3) to satisfy the borrow checker — this is a known pattern when doing N×N interactions on a single `Vec<Speaker>`. The workaround is correct but creates unnecessary allocations.
- The `reconcile` method uses `speaker.id` to filter self from the actual states list, which assumes IDs are dense and unique starting from 0. The `balanced()` constructor satisfies this, but custom speaker vectors might not.
- The coherence metric (`1/(1+variance)`) is mathematically sound but creates a value that's always ≥ 0.5 for ternary states (since variance of {-1,0,1} values is at most ~1.0). The range is effectively [0.5, 1.0] rather than [0.0, 1.0].

---

*Analysis produced: 2026-08-02*
*Repository version: 0.1.0 (commit 7c49400)*
