# plato-ship-protocol — Analysis

## What It Does

**plato-ship-protocol** defines a **6-layer network stack for vessel-to-vessel communication** in the SuperInstance ecosystem. It's the OSI model reborn as a marine protocol: each layer is a Rust trait that can be independently implemented, tested, and composed.

The layers, bottom-up:

| Layer | Name | Marine Metaphor | Real Function |
|-------|------|-----------------|---------------|
| L1 | Harbor | Direct addressing, peer discovery | Identity resolution, peer registration |
| L2 | TidePool | Async message routing, buffering | FIFO message queue with trust-weighted routing |
| L3 | Current | Cross-runtime transport | Serialization/framing for git-based inter-instance messaging |
| L4 | Channel | Simulation ↔ live bridging | Dual-mode channels (sim vs production) |
| L5 | Beacon | Event signaling, trust scoring | Observability, trust reputation (0.0–1.0) |
| L6 | Reef | Persistence, state handoff | Key-value state store with handoff to next runtime |

The `ShipStack` composes all 6 into a pipeline: `send()` routes L1→L6 (outbound), `receive()` routes L6→L1 (inbound).

## Architecture

- **Pure trait definitions** — no I/O, no async, no dependencies beyond std
- **Mock-testable** — every layer has a mock implementation in the doc tests
- **Directional stack** — send goes bottom-up, receive goes top-down
- **Stateless layers** — each layer transforms bytes independently
- **Composable** — swap any layer's implementation without touching others

### Key Innovation: Trust as Protocol Layer

Layer 5 (Beacon) embeds **trust scoring directly into the network stack**. Every node has a `[0.0, 1.0]` trust score that flows through the protocol itself. This isn't bolted-on security — it's a protocol-level concept.

### Key Innovation: State Handoff as Protocol Layer

Layer 6 (Reef) treats persistence as a network concern. The `handoff()` method enables **ghost tiles** — state that survives runtime death and can be picked up by a new instance. This is the afterlife of an agent's beliefs.

## Code Quality

- **4 files** (Cargo.toml, lib.rs, ci.yml, LICENSE)
- ~350 lines of Rust
- Zero dependencies — pure trait crate
- Excellent doc tests with runnable examples per trait
- Full test coverage of the ShipStack roundtrip
- Clean, idiomatic Rust with proper doc comments

## Relevance to Slackwater

This is the **discovery and communication protocol** for in-game agents. When two NPCs or agent-processes meet in the game world, the Plato protocol defines how they:
1. Notice each other (Harbor)
2. Queue messages (TidePool)
3. Cross runtime boundaries (Current)
4. Switch between simulation and live modes (Channel)
5. Build trust (Beacon)
6. Remember each other after restarts (Reef)
