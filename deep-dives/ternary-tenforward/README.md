# ternary-tenforward

**The conversation engine.** Multiple AI agents in cyclic dialogue, governed by Rock-Paper-Scissors dynamics and Fibonacci timing.

> *In Star Trek, Ten-Forward is the bar on the Enterprise — the social space outside the chain of command. This crate gives AI agents their own Ten-Forward: a structured space for simultaneous, self-balancing conversation.*

---

## Table of Contents

- [What This Is](#what-this-is)
- [Why It Exists](#why-it-exists)
- [The Physics Behind It](#the-physics-behind-it)
- [Installation](#installation)
- [Quick Start (60 Seconds)](#quick-start-60-seconds)
- [Core Concepts](#core-concepts)
- [Full Walkthrough](#full-walkthrough)
- [API Reference](#api-reference)
- [Recipes and Patterns](#recipes-and-patterns)
- [Troubleshooting](#troubleshooting)
- [How It Works: Deep Dive](#how-it-works-deep-dive)
- [See Also](#see-also)
- [License](#license)

---

## What This Is

`ternary-tenforward` is a Rust crate that implements a **beat-based conversation engine** for multi-agent systems. Instead of agents taking turns (A speaks → B speaks → C speaks), all agents speak simultaneously on each beat, then reconcile their predictions with reality.

The result: conversations that are dynamic, self-balancing, and never deadlock — powered by three mathematical principles:

1. **Z₃ cyclic group** — the only algebraic structure on {-1, 0, +1}
2. **Rock-Paper-Scissors dynamics** — self-balancing population waves
3. **Fibonacci timing** — the Pisano period mod 3 = 8, a natural rhythm

## Why It Exists

Standard multi-agent conversation systems have three problems:

1. **Turn-taking is unnatural.** Real conversations have people chiming in simultaneously. Forced sequential turns create artificial bottlenecks.
2. **Monoculture lock-in.** When 3 agents agree and 1 disagrees, the dissenter gets permanently crushed. Groupthink kills creative exploration.
3. **Conversation stalling.** When everyone goes quiet ("hmm"), there's no mechanism to restart the conversation.

Ten-Forward solves all three through mathematical guarantees rather than heuristics.

## The Physics Behind It

This isn't arbitrary design. These are proven mathematical properties:

### Z₃ Is the Only Group on {-1, 0, +1}

There's exactly one algebraic way to combine three values where every element has an inverse: cyclic addition mod 3. This means every ternary interaction is inherently cyclic — conversations can't converge to a permanent winner.

### RPS Dominance Creates Self-Balancing Waves

The dominance cycle (-1 beats +1, +1 beats 0, 0 beats -1) means no strategy is optimal against all opponents. In populations, this creates **limit cycles** — the distribution of states oscillates rather than converging.

| Speaker State | Value | Beats | Beaten By |
|--------------|-------|-------|-----------|
| Contrarian | -1 | Agreeing (+1) | Reflecting (0) |
| Reflecting | 0 | Contrarian (-1) | Agreeing (+1) |
| Agreeing | +1 | Reflecting (0) | Contrarian (-1) |

### Fibonacci Period 8 Is the Natural Rhythm

The ternary Fibonacci sequence is: `1, 1, -1, 0, -1, -1, 1, 0` — and then it repeats. This **period 8** (called the Pisano period for mod 3) is a mathematical escape hatch. Every 8 beats, agents stuck in reflection are forced to commit to a stance.

---

## Installation

### Prerequisites

- **Rust** (edition 2021 or later). Install via [rustup](https://rustup.rs):
  ```bash
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  ```

- Verify your installation:
  ```bash
  rustc --version  # Should show 1.56.0 or later
  cargo --version
  ```

### As a Dependency

Add to your `Cargo.toml`:

```toml
[dependencies]
ternary-tenforward = "0.1"
```

Or use cargo add:

```bash
cargo add ternary-tenforward
```

### From Source

```bash
git clone https://github.com/SuperInstance/ternary-tenforward
cd ternary-tenforward
cargo build --release
```

The compiled library will be at `target/release/libternary_tenforward.{rlib,a,so}` depending on your platform.

### Verify Installation

```bash
cargo test
```

You should see all 22 tests pass.

---

## Quick Start (60 Seconds)

```rust
use ternary_tenforward::TenForward;

fn main() {
    // Create the standard 3-agent conversation:
    // Architect (+1) — builds on ideas
    // Critic (-1) — challenges and pushes back
    // Historian (0) — reflects and contextualizes
    let mut tf = TenForward::standard();

    // Run one beat of conversation
    let round = tf.round();
    println!("Tick {}: {} utterances", round.tick, round.utterances.len());
    
    for u in &round.utterances {
        println!("  [{}] {}", u.speaker_id, u.content);
    }

    // Run a full 200-beat session
    let summary = tf.run(200);
    println!("Avg prediction accuracy: {:.2}", summary.avg_prediction_accuracy);
    println!("Dominance cycles: {}", summary.dominance_cycles);
    println!("Final BPM: {:.1}", summary.bpm_final);
}
```

Create this as `src/main.rs`, add `ternary-tenforward` to your `Cargo.toml`, and run `cargo run`.

---

## Core Concepts

### The T-Minus Cycle

Every conversation round has five phases:

```
Phase 1: T-minus  → Each agent predicts what others will say
Phase 2: T-0       → All agents produce output SIMULTANEOUSLY (like a musical chord)
Phase 3: T-plus    → Pairwise RPS interactions — who beat whom this round
Phase 4: T-plus    → Reconcile predictions with reality, update accuracy
Phase 5: Periodic  → Every 8 ticks, stuck reflectors tunnel out via Fibonacci timing
```

No agent waits for permission. No turns. No queue. Everyone speaks at once, then deals with the consequences.

### Speaker States

Every agent is in exactly one of three states at any moment:

| State | Value | Role | Behavior |
|-------|-------|------|----------|
| Contrarian | -1 | The Challenger | Disagrees, pushes back, finds flaws |
| Reflecting | 0 | The Mediator | Listening, thinking, staying neutral |
| Agreeing | +1 | The Builder | Supports, extends, confirms |

Agents move between states based on RPS outcomes, energy levels, and trust dynamics.

### Speaker Properties

| Property | Type | Range | Purpose |
|----------|------|-------|---------|
| `energy` | f64 | 0.0–1.0 | Affects assertiveness and output intensity |
| `trust` | u8 | 0–255 | How much the agent listens to others |
| `dominance` | f64 | ~0.0–1.0 | Running average of RPS win rate |
| `prediction_accuracy` | f64 | 0.0–1.0 | How well they predict other agents |

### The Fibonacci Tunnel

Every 8 ticks (the Pisano period for mod 3), agents stuck in reflection (state 0) with energy > 0.4 are forced to pick a side. This prevents conversations from stalling in eternal "hmm" mode.

### BPM Adaptation

The conversation tempo adapts to average speaker energy:

```
BPM = 60 + average_energy × 60
```

Range: 60 BPM (calm, low energy) to 120 BPM (excited, high energy).

---

## Full Walkthrough

### Step 1: Create Speakers

```rust
use ternary_tenforward::{Speaker, TenForward};

// Method A: Use the standard 3-agent preset
let mut tf = TenForward::standard();
// Creates: Architect(+1, energy=0.7), Critic(-1, energy=0.6), Historian(0, energy=0.5)

// Method B: Use the balanced N-agent preset
let mut tf = TenForward::balanced(6);
// Creates 6 speakers with cycling states: +1, -1, 0, +1, -1, 0

// Method C: Build custom speakers
let speakers = vec![
    Speaker::new(0, "Visionary").with_state(1).with_energy(0.9),
    Speaker::new(1, "Skeptic").with_state(-1).with_energy(0.7),
    Speaker::new(2, "Synthesizer").with_state(0).with_energy(0.5),
    Speaker::new(3, "Wildcard").with_state(-1).with_energy(0.3),
];
let mut tf = TenForward::new(speakers);
```

### Step 2: Run Rounds

```rust
// Single round
let round = tf.round();

// Examine what happened
println!("Tick: {}", round.tick);
println!("Energy average: {:.2}", round.energy_avg);
println!("Coherence: {:.2}", round.coherence);
println!("Dominant state: {:?}", round.rps_dominant);

for u in &round.utterances {
    println!("  Speaker {}: {} (state={}, energy={:.2})",
             u.speaker_id, u.content, u.state, u.energy);
}
```

### Step 3: Run Full Sessions

```rust
// Run 200 rounds and get summary statistics
let summary = tf.run(200);

println!("Rounds completed: {}", summary.rounds);
println!("Initial states: {:?}", summary.initial_states);
println!("Final states: {:?}", summary.final_states);
println!("Average dominance: {:.3}", summary.avg_dominance);
println!("Average prediction accuracy: {:.3}", summary.avg_prediction_accuracy);
println!("Dominance cycles detected: {}", summary.dominance_cycles);
println!("Final BPM: {:.1}", summary.bpm_final);
```

### Step 4: Inspect Round History

```rust
// Run some rounds
for _ in 0..50 {
    tf.round();
}

// Examine the history
for round in &tf.history {
    let (neg, zero, pos) = round.state_snapshot.iter()
        .fold((0, 0, 0), |(n, z, p), (_, s)| match s {
            -1 => (n + 1, z, p),
            0 => (n, z + 1, p),
            _ => (n, z, p + 1),
        });
    println!("Tick {}: -1×{}  0×{}  +1×{}  coherence={:.2}",
             round.tick, neg, zero, pos, round.coherence);
}
```

### Step 5: Census (Current State Distribution)

```rust
let (contrarians, reflectors, agreers) = tf.census();
println!("Contrarians: {}, Reflectors: {}, Agreers: {}",
         contrarians, reflectors, agreers);
```

### Step 6: Access Individual Speakers

```rust
for speaker in &tf.speakers {
    println!("{}: state={}, energy={:.2}, trust={}, dominance={:.2}, accuracy={:.2}",
             speaker.name,
             speaker.state,
             speaker.energy,
             speaker.trust,
             speaker.dominance,
             speaker.prediction_accuracy);
}
```

---

## API Reference

### `Speaker`

A single conversation participant.

#### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `usize` | required | Unique identifier (must be dense from 0) |
| `name` | `String` | required | Display name |
| `state` | `i8` | `0` | Current stance: -1, 0, or +1 |
| `energy` | `f64` | `0.5` | Assertiveness level (0.0–1.0) |
| `trust` | `u8` | `128` | Social credit (0–255) |
| `dominance` | `f64` | `0.33` | Exponential moving average of RPS wins |
| `last_output` | `Option<String>` | `None` | Most recent utterance text |
| `prediction` | `Option<Prediction>` | `None` | Current prediction of others |
| `prediction_accuracy` | `f64` | `0.5` | EWMA of prediction correctness |
| `ticks_speaking` | `u64` | `0` | Consecutive active ticks |
| `ticks_silent` | `u64` | `0` | Consecutive silent ticks |

#### Methods

```rust
// Construction
Speaker::new(id: usize, name: &str) -> Speaker
speaker.with_state(s: i8) -> Speaker        // builder pattern, clamps to [-1, 1]
speaker.with_energy(e: f64) -> Speaker       // builder pattern, clamps to [0.0, 1.0]

// Conversation actions
speaker.predict(&mut self, others: &[Speaker])           // Predict others' states
speaker.speak(&mut self) -> Utterance                     // Generate output
speaker.reconcile(&mut self, actual: &[i8]) -> f64        // Compare prediction to reality
speaker.react_to(&mut self, other: &Speaker)              // RPS interaction update
```

#### RPS Outcomes in `react_to`

| Self State | Other State | Outcome | Effect |
|-----------|-------------|---------|--------|
| -1 | +1 | **Win** | dominance ↑, energy ↑ |
| +1 | 0 | **Win** | dominance ↑, energy ↑ |
| 0 | -1 | **Win** | dominance ↑, energy ↑ |
| Same | Same | **Tie** | May shift to reflecting if trust > 100 |
| Otherwise | — | **Lose** | dominance ↓, trust ↓5, may collapse to reflecting |

---

### `Prediction`

An agent's forecast of other agents' states.

```rust
pub struct Prediction {
    pub predicted_states: Vec<i8>,  // What states others are expected to be in
    pub confidence: f64,             // Based on historical accuracy
}
```

---

### `Utterance`

One beat of output from one speaker.

```rust
pub struct Utterance {
    pub speaker_id: usize,
    pub content: String,
    pub state: i8,       // State when spoken
    pub energy: f64,     // Energy when spoken
}
```

---

### `Round`

The result of one complete conversation beat (all five phases).

```rust
pub struct Round {
    pub tick: u64,                        // Which beat (1-indexed)
    pub utterances: Vec<Utterance>,       // What everyone said
    pub state_snapshot: Vec<(usize, i8)>, // (speaker_id, state) pairs
    pub energy_avg: f64,                  // Mean energy across speakers
    pub coherence: f64,                   // 1/(1+variance) — alignment measure
    pub rps_dominant: Option<i8>,         // Which state has plurality
}
```

**Coherence** ranges from ~0.33 (maximum disagreement) to 1.0 (perfect alignment).

**`rps_dominant`** is `Some(-1)`, `Some(0)`, `Some(+1)`, or `None` (tie).

---

### `TenForward`

The conversation engine.

#### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `speakers` | `Vec<Speaker>` | — | All participants |
| `tick` | `u64` | `0` | Current beat counter |
| `history` | `Vec<Round>` | `[]` | Complete round history |
| `bpm` | `f64` | `90.0` | Current tempo (adapts to energy) |
| `rhythm_period` | `usize` | `8` | Fibonacci tunnel period |

#### Constructors

```rust
TenForward::new(speakers: Vec<Speaker>) -> TenForward           // Custom
TenForward::standard() -> TenForward                             // 3 agents (preset)
TenForward::balanced(n: usize) -> TenForward                    // N agents (cycling states)
```

#### Methods

```rust
tf.round(&mut self) -> Round              // Execute one conversation beat
tf.run(&mut self, rounds: usize) -> SessionSummary  // Execute N beats, return stats
tf.census(&self) -> (usize, usize, usize)          // (contrarians, reflectors, agreers)
```

---

### `SessionSummary`

Statistics from a completed session.

```rust
pub struct SessionSummary {
    pub rounds: u64,                      // Total beats executed
    pub initial_states: Vec<i8>,          // States at session start
    pub final_states: Vec<i8>,            // States at session end
    pub avg_dominance: f64,               // Mean dominance across speakers
    pub avg_prediction_accuracy: f64,     // Mean prediction accuracy
    pub dominance_cycles: usize,          // Count of dominant-state repetitions
    pub bpm_final: f64,                   // Ending BPM
}
```

---

## Recipes and Patterns

### Pattern 1: Standard Brainstorm (3 Agents)

```rust
let mut tf = TenForward::standard();
let summary = tf.run(100);
// Architect builds, Critic challenges, Historian reflects
// Self-balancing over ~100 rounds
```

### Pattern 2: Large Panel Discussion (8 Agents)

```rust
let mut tf = TenForward::balanced(8);
let summary = tf.run(200);
// Multiple coalitions form and dissolve
// More stable dynamics with larger populations
```

### Pattern 3: Adversarial Review (2 Agents)

```rust
let speakers = vec![
    Speaker::new(0, "Proposer").with_state(1).with_energy(0.8),
    Speaker::new(1, "Opposer").with_state(-1).with_energy(0.8),
];
let mut tf = TenForward::new(speakers);
let summary = tf.run(50);
// High-intensity back-and-forth
// RPS dynamics will naturally shift states over time
```

### Pattern 4: Monitoring Conversation Health

```rust
let mut tf = TenForward::balanced(6);

for i in 0..100 {
    let round = tf.round();
    
    // Alert if coherence is too high (groupthink) or too low (chaos)
    if round.coherence > 0.9 {
        eprintln!("Warning: coherence too high at tick {} — possible monoculture", round.tick);
    }
    if round.coherence < 0.4 {
        eprintln!("Note: low coherence at tick {} — high disagreement", round.tick);
    }
    
    // Check for state dominance
    if let Some(dominant) = round.rps_dominant {
        let label = match dominant { -1 => "contrarian", 0 => "reflecting", _ => "agreeing" };
        println!("Tick {}: {} dominant (coherence={:.2})", round.tick, label, round.coherence);
    }
}
```

### Pattern 5: Custom Rhythm Period

```rust
let mut tf = TenForward::standard();
tf.rhythm_period = 4;  // Faster tunneling (every 4 ticks instead of 8)
// Use shorter periods for fast-paced conversations
// Use longer periods for deeper reflection
```

### Pattern 6: Inspecting Prediction Quality

```rust
let mut tf = TenForward::balanced(4);
tf.run(50);

for speaker in &tf.speakers {
    println!("{}: accuracy={:.2}%, dominance={:.2}%, energy={:.2}%",
             speaker.name,
             speaker.prediction_accuracy * 100.0,
             speaker.dominance * 100.0,
             speaker.energy);
}
// High accuracy = reads the room well
// Low accuracy = surprised by others (could indicate creative unpredictability)
```

---

## Troubleshooting

### Problem: All agents end up in the same state

**Symptom:** `census()` shows all speakers in one state after many rounds.

**Cause:** This shouldn't happen with the default anti-monoculture mechanisms. Check if you've modified `rhythm_period` or energy/trust parameters.

**Fix:** Ensure `rhythm_period` is set (default 8) and that speakers start with non-zero energy (>0.4 for tunneling to work).

### Problem: Conversation produces no interesting dynamics

**Symptom:** All utterances look the same, states don't change.

**Cause:** Speakers may have very low energy (< 0.3), which prevents state transitions.

**Fix:** Initialize speakers with `with_energy(0.5)` or higher.

### Problem: Borrow checker errors during round execution

**Symptom:** "Cannot borrow `self.speakers` as mutable more than once."

**Cause:** This is a known Rust pattern challenge with N×N interactions. The crate handles it internally by snapshotting speaker states before the interaction loop.

**Fix:** If extending the engine, follow the same snapshot pattern used in `round()` — collect states into a `Vec` first, then iterate.

### Problem: Prediction accuracy stays at 0.5

**Symptom:** `prediction_accuracy` never improves.

**Cause:** The momentum predictor assumes agents keep their current state. If agents change states frequently (due to RPS interactions), predictions will be wrong.

**Understanding:** This is actually informative — low accuracy means the conversation is dynamic. High accuracy means it's predictable (possibly stagnant).

### Problem: `cargo test` fails

**Symptom:** Tests don't compile or fail.

**Fix:** Ensure you're using Rust edition 2021 or later:
```bash
rustup update stable
cargo test
```

### Problem: Performance with large speaker counts

**Symptom:** Rounds are slow with 100+ speakers.

**Cause:** The RPS interaction loop is O(n²) — every speaker interacts with every other.

**Fix:** For large populations, consider sub-sampling interactions or using the `ternary-cell` crate for compact representation.

---

## How It Works: Deep Dive

### The Five-Phase Round Cycle

#### Phase 1: T-Minus (Prediction)

Each agent looks at all other agents and predicts what state they'll be in when they speak. The current prediction model is a **momentum predictor**: assume others will stay in their current state unless they've been silent for more than 5 ticks (in which case predict reflection).

```rust
// Simplified prediction logic
if other.ticks_silent > 5 { predict 0 }
else { predict other.state }
```

#### Phase 2: T-0 (Simultaneous Output)

Every agent calls `speak()` at the same logical moment. There is no queue, no moderator, no permission system. Each agent produces an `Utterance` based purely on their own state and energy.

The output text is currently templated based on state and energy level:

```
State -1, Energy > 0.7: "Wait, that's not right. Disagree."
State -1, Energy > 0.3: "I see it differently. Disagree."
State -1, Energy ≤ 0.3: "Maybe, but consider this. Disagree."

State  0, Energy > 0.7: "Hmm. Let me think about that... interesting"
State  0, Energy > 0.3: "Hmm. There's something there"
State  0, Energy ≤ 0.3: "Hmm. I need a moment on this one"

State +1, Energy > 0.7: "YES. Exactly that. Right."
State +1, Energy > 0.3: "That tracks. Right."
State +1, Energy ≤ 0.3: "Fair point. Right."
```

In production, you'd replace `speak()` with LLM-backed generation.

#### Phase 3: T-Plus (RPS Interactions)

Every pair of agents (i, j) where i ≠ j interacts through `react_to()`. The RPS rules determine who wins:

- Winner: `dominance = dominance × 0.9 + 0.1` (exponential moving average, recent-heavy)
- Winner: `energy = min(energy + 0.05, 1.0)` (small energy boost)
- Loser: `dominance = dominance × 0.9` (decay)
- Loser: `trust = trust.saturating_sub(5)` (trust erosion)
- Loser with energy < 0.3: state collapses to 0 (reflection)
- Tie with trust > 100: state shifts to 0 (reflection)

This phase is O(n²) in the number of speakers.

#### Phase 4: T-Plus (Reconciliation)

Each agent compares their Phase 1 prediction against the actual states from Phase 2/3:

```rust
accuracy = correct_predictions / total_predictions
prediction_accuracy = old_accuracy × 0.8 + accuracy × 0.2  // EWMA
```

This creates evolutionary pressure: agents who read the room well gain confidence (higher prediction accuracy influences future predictions).

#### Phase 5: Fibonacci Tunnel

Every `rhythm_period` ticks (default 8):

```rust
if speaker.state == 0 && speaker.energy > 0.4 {
    speaker.state = if tick % 2 == 0 { +1 } else { -1 };
}
```

This breaks stuck reflections. The period 8 is not arbitrary — it's the Pisano period for mod 3, making it the natural rhythm of ternary systems.

### Metrics Computation

After all phases:

- **Energy average:** mean of all speakers' energy
- **Coherence:** `1.0 / (1.0 + variance_of_states)` — higher variance = lower coherence
- **RPS dominant:** the state with plurality (can be None if tied)
- **BPM:** `60.0 + energy_avg × 60.0` — adapts to conversation intensity

### The Anti-Monoculture Guarantee

Without intervention, experiments showed that 4-agent conversations lock into permanent monoculture by tick 35 (e.g., three +1 agents permanently dominating one -1 agent).

The three anti-monoculture mechanisms are:
1. **Mutation (via Fibonacci tunnel):** Forces committed stances every 8 ticks
2. **Energy decay:** Winners get small energy boosts (+0.05) but losers' energy drops lead to state collapse, creating turnover
3. **Trust realignment:** Losing agents lose trust, and low-trust agents in ties shift to reflection, which restarts the cycle

---

## See Also

### SuperInstance Fleet Crates

- **[ternary-cell](https://github.com/SuperInstance/ternary-cell)** — 3-byte agent atoms for million-instance scale
- **[ternary-predict](https://github.com/SuperInstance/ternary-predict)** — Prediction-first perception (the shoe protocol)
- **[ternary-speculate](https://github.com/SuperInstance/ternary-speculate)** — Speculative sync and shadow partners
- **[ternary-motion](https://github.com/SuperInstance/ternary-motion)** — Tracking where speakers are heading
- **[ternary-tempo](https://github.com/SuperInstance/ternary-tempo)** — BPM adapts to conversation energy
- **[ternary-mixer](https://github.com/SuperInstance/ternary-mixer)** — Multi-channel blend of speakers
- **[ternary-crossfader](https://github.com/SuperInstance/ternary-crossfader)** — Smooth transitions between dominant speakers

### Related Crates

- **[ternary-oracle](https://github.com/SuperInstance/ternary-oracle)** — Related
- **[ternary-attention](https://github.com/SuperInstance/ternary-attention)** — Related
- **[ternary-planning](https://github.com/SuperInstance/ternary-planning)** — Related

### Architecture Documents

- `TEN-FORWARD.md` in `construct-coordination` — Full architecture doc
- `SPIRAL-6-FINDINGS.md` — Monoculture experiment results
- `NEGATIVE-SPACE-EMERGENCE-PAPER.md` — Formal science paper including ten-forward dynamics

---

## License

MIT — see [LICENSE](LICENSE).

By contributing, you agree your work is dual-licensed under MIT OR Apache-2.0.

---

*Tutorial written: 2026-08-02 · Crate version: 0.1.0*
