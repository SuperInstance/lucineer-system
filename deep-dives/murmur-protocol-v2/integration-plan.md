# Murmur Protocol v2 → DCA Integration Plan

## Phase 1: Vibe Protocol for Agent State
- Port MurmurNetwork to TypeScript as a DCA fleet coordination layer
- Each agent = a MurmurRoom with a "vibe" (focus level, workload, priority)
- Neighbors = agents that should be aware of each other's state
- Propagation rounds = periodic fleet sync (every N seconds)

## Phase 2: Conservation-Based Resource Allocation
- Total fleet compute budget = conserved vibe
- Agents inject vibe (request resources) and extract vibe (release resources)
- Blending factor = how much an agent's state influences neighbors
- Equilibrium detection = fleet has reached consensus

## Phase 3: Confidence-Weighted Information Flow
- Agent findings/insights tagged with confidence scores
- Confidence decays per hop — unreliable info dies out naturally
- Forward threshold = minimum confidence to propagate (prevents rumor cascades)
- High-confidence findings propagate further

## Phase 4: Topology Configuration
- Star topology for hub-orchestrator patterns (Lucineer → sub-agents)
- Ring topology for pipeline patterns (research → plan → build → verify)
- Mesh for peer-to-peer agent collaboration
- Dynamic reconfiguration based on task requirements

## Implementation Notes
- Rust crate can be called via FFI or reimplemented in TypeScript (~300 LOC)
- The conservation law is the key insight: total fleet attention/compute is bounded
- Equilibrium distance = decision confidence metric
