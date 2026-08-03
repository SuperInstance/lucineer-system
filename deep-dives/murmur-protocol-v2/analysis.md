# Murmur Protocol v2 — Deep Dive Analysis

## What It Does
A gossip-based vibe-sharing protocol implemented in Rust. Rooms whisper their "vibe" (a scalar value) to neighbors. The murmur spreads through the network like gossip, with each room blending what it hears with its own state. **Conservation is maintained**: the total vibe in the network never changes.

## Architecture
- **Single Rust crate** (`src/lib.rs`, ~350 lines + tests)
- **Core Data Structures**:
  - `Murmur`: Message with source_id, vibe (f64), hop_count, confidence, origin_tick
  - `MurmurConfig`: blending_factor (0.1), max_hops (3), forward_threshold (0.1), confidence_decay (0.8)
  - `MurmurRoom`: id, vibe, confidence, neighbors[], message counters
  - `MurmurNetwork`: HashMap of rooms + config + total_vibe + tick counter
  - `MurmurRound`: Propagation result stats (delivered, dropped, max_hop, conservation_error)

- **Topology Builders**: Star, Ring, Mesh — built-in network construction
- **Propagation Algorithm**: Each round, every room sends `vibe * blending_factor` to each neighbor. Messages below forward_threshold confidence are dropped. Total vibe is conserved (subtracted from source, added to target).

## Key Innovations
1. **Conservation Law**: Total vibe is invariant through propagation — provably conserved. The `conservation_error` field in each round verifies this.
2. **Confidence Decay**: Messages lose confidence per hop (exponential decay via `confidence_decay` factor). Below `forward_threshold`, they're dropped. This creates a natural finite propagation radius.
3. **Equilibrium Convergence**: Networks converge toward uniform vibe distribution. The `equilibrium_distance()` method measures how far from uniform.
4. **Topology-Aware Convergence**: Full mesh converges faster than star (leaves only talk through center). This is measured and tested.
5. **Inject/Extract**: External vibe sources can inject or extract from any room, adjusting the total.

## DCA / Slackwater Integration Points
- **Agent State Propagation**: Vibe = agent "energy" or "focus level" propagating through the fleet
- **Conservation as DCA Principle**: The conservation law maps to DCA's resource budget — total compute/attention is conserved across agents
- **Confidence-Weighted Communication**: Low-confidence information naturally dies out — perfect for rumor suppression in agent fleets
- **Network Topology for Agent Mesh**: Star (hub-spoke), Ring (pipeline), Mesh (peer-to-peer) — all relevant to DCA fleet topologies
- **Equilibrium Detection**: Knowing when a fleet has "settled" on a decision

## Code Quality
- **Excellent**: Clean Rust, full serde serialization, comprehensive test suite (17 tests)
- **Mathematically rigorous**: Conservation is tested to <1e-6 precision
- **Well-structured**: Data + behavior co-located in structs
- **Serializable**: Full JSON round-trip tested

## Patterns to Adopt
1. **Conservation-law state propagation** — total state is invariant
2. **Confidence decay for rumor bounds** — prevents infinite propagation
3. **Topology-aware convergence analysis** — know when the system has settled
4. **Blending factor for influence** — how much each neighbor affects you
5. **Inject/Extract for external I/O** — clean boundary between protocol and environment
