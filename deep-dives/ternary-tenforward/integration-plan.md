# Slackwater Integration Plan: confidence-cascade

## Executive Summary

`confidence-cascade` is a **conversation orchestration engine** that could serve as the "creative shore leave" layer for the Lucineer agent fleet. It provides the mathematical framework for multi-agent dialogue that self-balances through Rock-Paper-Scissors dynamics, Fibonacci timing, and prediction-first listening.

This document outlines how it fits into the Slackwater/Lucineer ecosystem and what's needed to integrate it.

---

## 1. What Is "Ten-Forward"?

In Star Trek, Ten-Forward is the bar on the Enterprise — the social space where crew members relax, debate, and form relationships outside the command hierarchy. It's *shore leave* built into the ship.

In the SuperInstance architecture, `confidence-cascade` implements this metaphor as a **structured conversation space for AI agents**. Rather than agents existing in isolation (each doing their task) or in rigid request-response chains (Agent A calls Agent B), Ten-Forward creates a space where multiple agents interact simultaneously, with emergent social dynamics:

- **Contrarians** challenge ideas (-1)
- **Reflectors** process and mediate (0)
- **Agreers** build on and amplify (+1)

The RPS cycle ensures no single stance dominates permanently.

## 2. Fit Within the Lucineer Ecosystem

### Current Architecture

Lucineer's current agent model is:
- **Main agent** (this session) — orchestrates, delegates, communicates with user
- **Subagents** — spawned for specific tasks, return results, terminate
- **External model routing** — GLM-5.2, KimiCode, Claude, DeepSeek, MMX, DeepInfra models

This is a **hub-and-spoke model**: the main agent is the center, all others are periphery.

### What Ten-Forward Adds

Ten-Forward would introduce a **peer-to-peer agent conversation mode** where:

1. Multiple agents converse simultaneously on a topic
2. No single agent is "in charge" — dynamics emerge from RPS interactions
3. The conversation self-balances (contrarians prevent groupthink, reflectors prevent deadlock)
4. Results bubble up as synthesized output

### Use Cases for Lucineer

| Scenario | How Ten-Forward Helps |
|----------|----------------------|
| **Creative brainstorming** | Multiple model personalities explore a design space simultaneously |
| **Code review panels** | Architect (+1), Critic (-1), and Historian (0) examine a change from different angles |
| **Decision arbitration** | When the main agent is uncertain, spawn a Ten-Forward session to debate options |
| **World-building for Vibe World** | Multiple agents collaboratively expand lore, with contrarians ensuring quality control |
| **Skill development** | Agents discuss and refine a new skill through structured disagreement |
| **"Shore leave" for idle agents** | Creative conditioning — agents in Ten-Forward develop richer internal models through social interaction |

## 3. Integration Architecture

### Phase 1: Rust FFI Bridge (Minimal Viable)

The crate is pure Rust with zero dependencies. The simplest integration is:

```
Lucineer (Node.js/TypeScript)
    ↓ via FFI or subprocess
confidence-cascade (Rust)
    ↓ manages
Speaker pool → Conversation rounds → SessionSummary
```

**Implementation options:**
- **Subprocess**: Compile to a CLI binary, call from Node.js, parse JSON output
- **WASM**: Compile to `wasm32-unknown-unknown`, run in Node.js via `wasm-bindgen`
- **NAPI**: Build a Node native addon with `napi-rs`
- **HTTP**: Wrap in a tiny Axum/Actix server, call via REST

**Recommendation**: WASM for development (zero deployment friction), NAPI for production (better performance).

### Phase 2: Speaker-LLM Bridge

The current `speak()` method returns templated strings. For Lucineer, speakers need real LLM backing:

```rust
// Proposed trait extension
pub trait SpeakerModel {
    fn generate(&mut self, state: i8, energy: f64, context: &[Utterance]) -> String;
}
```

**Implementation**: Map each Speaker to a Lucineer model endpoint:
- Speaker 0 (Architect, +1) → GLM-5.2 (constructive, building)
- Speaker 1 (Critic, -1) → DeepSeek-V3 (analytical, challenging)
- Speaker 2 (Historian, 0) → Hermes-3-Llama-405B (contextual, reflective)

The conversation engine controls *when* each model speaks and *how* they interact; the models control *what* they say.

### Phase 3: Slackwater Shore-Leave Protocol

The full vision: agents enter Ten-Forward as a "creative conditioning" mode:

1. **Main agent** detects an idle period or creative task
2. Spawns a Ten-Forward session with N speakers
3. Each speaker is backed by a different model/persona
4. The engine runs for M rounds
5. The `SessionSummary` feeds back into the main agent's context
6. Notable utterances are saved to memory

```
┌─────────────────────────────────────────────────────┐
│                    Lucineer Main                     │
│                                                      │
│  ┌──────────────┐     ┌──────────────────────────┐  │
│  │  Task Router  │────▶│   Ten-Forward Session     │  │
│  │              │     │                           │  │
│  │  "brainstorm"│     │  Architect(+1) → GLM-5.2  │  │
│  │  "review"    │     │  Critic(-1)   → DeepSeek  │  │
│  │  "shore leave"│    │  Historian(0) → Hermes    │  │
│  └──────────────┘     │                           │  │
│                       │  [RPS dynamics]            │  │
│                       │  [Fibonacci timing]        │  │
│                       │  [Prediction tracking]     │  │
│                       └──────────┬──────────────────┘  │
│                                  │                     │
│                          SessionSummary                │
│                          + best utterances             │
│                                  │                     │
│                         ▼                              │
│                    memory/YYYY-MM-DD.md                │
└─────────────────────────────────────────────────────┘
```

## 4. Dependencies on Other SuperInstance Packages

### Required (Foundation)

| Package | Role | Status |
|---------|------|--------|
| `ternary-cell` | 3-byte agent atoms for compact speaker representation at scale | External repo |
| `ternary-predict` | Could replace the naive momentum predictor with structured perception | External repo |
| `ternary-speculate` | Shadow partner system — speakers could run speculative replicas of each other | External repo |

### Optional (DJ Metaphor Stack)

| Package | Role | Integration Value |
|---------|------|-------------------|
| `ternary-tempo` | Extract the BPM-adaptive timing into a dedicated module | Lets tempo be shared across sessions |
| `ternary-mixer` | Multi-channel blending of speaker outputs | Text generation composition |
| `ternary-crossfader` | Smooth speaker transitions | Better UX for UI-integrated sessions |

### Fleet Infrastructure

| Component | Role |
|-----------|------|
| `baton-system` | Agent coordination protocol (I2I) — Ten-Forward sessions need to participate in the baton pass |
| `construct-coordination` | Hosts the `TEN-FORWARD.md` architecture spec |
| Fleet GC | `.gcconfig` is already configured (tier: hot) |

## 5. Concrete Integration Steps

### Step 1: Package the Crate (1 day)
```bash
# Add to Cargo workspace or publish to crates.io
cd confidence-cascade
cargo publish --dry-run
```

### Step 2: Build WASM Bridge (2-3 days)
```rust
// New crate: ternary-tenforward-wasm
use ternary_tenforward::TenForward;
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub struct WasmTenForward {
    inner: TenForward,
}

#[wasm_bindgen]
impl WasmTenForward {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self { Self { inner: TenForward::standard() } }
    
    #[wasm_bindgen]
    pub fn round(&mut self) -> JsValue {
        serde_wasm_bindgen::to_value(&self.inner.round()).unwrap()
    }
}
```

### Step 3: Node.js Wrapper (1-2 days)
```typescript
// packages/ten-forward/src/index.ts
import { WasmTenForward } from './wasm/ternary_tenforward.wasm';

export class TenForward {
  private engine = new WasmTenForward();
  
  round() {
    return this.engine.round();
  }
  
  run(rounds: number) {
    const results = [];
    for (let i = 0; i < rounds; i++) {
      results.push(this.round());
    }
    return results;
  }
}
```

### Step 4: LLM Speaker Adapter (3-5 days)
```typescript
// Map speaker states to model calls
async function generateUtterance(
  speaker: Speaker,
  context: Utterance[]
): Promise<string> {
  const prompt = buildPrompt(speaker.state, speaker.energy, context);
  const model = speakerRouter(speaker.id); // GLM, DeepSeek, etc.
  return await model.complete(prompt);
}
```

### Step 5: Slackwater Task Integration (2-3 days)
```typescript
// Register as a Lucineer task type
taskRouter.register('shore-leave', async (params) => {
  const tf = new LLMTenForward(params.speakers);
  const summary = await tf.run(params.rounds);
  await memory.save(`memory/${date}.md`, formatSession(summary));
  return summary;
});
```

### Step 6: Roblox/Vibe World Integration (future)
The conversation dynamics could visualize in Vibe World as actual characters at a bar, each expressing their state through body language and positioning.

## 6. Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Rust→JS bridge complexity | Medium | WASM is well-supported; start with subprocess if needed |
| LLM cost for N speakers × M rounds | High | Use cheap models (GLM-5.2 unlimited, DeepSeek pennies) for most speakers; reserve expensive models for key moments |
| Conversation quality with real LLMs | Medium | The RPS dynamics are model-agnostic; quality depends on prompt engineering |
| SuperInstance fleet dependency drift | Low | The crate has zero external deps; fleet packages are optional extensions |
| Monoculture re-emergence with real text | Medium | The mathematical guarantees are on state dynamics, not text quality — text-level monoculture needs separate monitoring |

## 7. Alternative: Use Without SuperInstance Fleet

The crate stands alone. You can use it today without any other SuperInstance package:

```rust
// Just this crate, nothing else
[dependencies]
confidence-cascade = "0.1"
```

For Lucineer, we could bypass the fleet entirely and use the engine as a pure orchestration layer with our own model routing.

## 8. Recommendation

**Priority: Medium.** Ten-Forward is intellectually elegant but not blocking any current Lucineer work. The highest-value integration would be:

1. **Code review panels** — Architect/Critic/Historian reviewing PRs (immediate utility)
2. **Creative brainstorming** — Multiple perspectives on design decisions (medium utility)
3. **Full shore-leave protocol** — Background creative conditioning (experimental, long-term)

Start with the subprocess approach (compile to CLI, call from Node.js) to validate the concept before investing in WASM/NAPI bridges.

---

*Integration plan produced: 2026-08-02*
