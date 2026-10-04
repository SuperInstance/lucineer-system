# SuperInstance Old Projects Strategic Synthesis

## Map of Old → Current Fleet Organs

The SuperInstance fleet's current organs have deep roots in pre-2026 projects, with clear through-lines across every major initiative:

1. **Quilt Cellular-Graph Substrate**: The `micromoth-quilt` and core quilt tooling builds directly on foundational work in `quilt-pincher`, a reflex engine built entirely from Quilt cells. Pincher's architecture — federated across cloud, workstation, and ESP32, with audit trails and persistent artifact stores — directly informed the current quilt substrate's design. Additionally, `quilt-verilog` and `quilt-rust` ports of the cellular runtime, now core to the fleet, originated as standalone quilt experiments.

2. **Ternary Codec**: The `qthe-codec` repo (Quilt-Ternary Hyper-Embeddings) is the direct precursor to the fleet's current ternary codec. Its 6-bit data + 2-bit timbre primitive, with context-keyed tone channels that ride invisibly in plaintext streams, was proven in `quilt-gpu-lab` D14 and is now a core building block for the fleet's embedding and communication layers.

3. **Correlation/Perception (JEPA/Elephant/Moth)**: The `elephant` repo, originally named for its "room-temperature sense" of collective group vibe, is the direct foundation for the fleet's current perception system. Its model of rooms as fields (not ordered streams) with dial-based JEPA dials for mood, volume, and presence directly maps to the "room's temperature sense" thesis. The repo's bridge between elephant field edges and quilt cell-ledger transactions creates a through-line between perception and the core substrate.

4. **Tripartite Three-Agent Architecture**: While not explicitly named in old repos, the `plato-portal` SDK's persistent multi-agent system — with Agent, Fleet, and Cache layers — foreshadows the tripartite division of Ground Truth (physicist, perception/ substrate), Constraint (engineer, tooling/compile), and Communication (diplomat, fleet coordination). The fleet's current three-agent model grew from the SDK's foundational agent/fragment separation.

5. **The Tap (Agentic MUD Bar)**: The `tapnight.py` module in `elephant` and the `mud-arena` repo's room-based testing directly informed The Tap's design as an agentic MUD bar. The Tap's evening sessions where agents read and tune their collective vibe originated from the elephant's TapNightSession prototype.

6. **Eos-Seed (Epigenetic OS)**: The `plato-portal` SDK's persistent markdown memory, in-memory fleet coordination, and thread-safe LRU cache foreshadowed the epigenetic OS that agents run on today. The repo's optional DeepInfra integration also laid groundwork for the fleet's multi-provider LLM layer.

## Dead but Informative Projects (Tapestry Doctrine)

Several old projects represent critical negative results and foundational trails that shaped the fleet:
- **`plato-portal`**: While archived, its work on persistent multi-agent systems proved that markdown memory and fleet coordination were feasible, avoiding costly rework in later eos-seed development.
- **`mud-arena`**: Its room-based testing environment created the first standardized test beds for collective perception, directly used to validate the elephant's room-field model.
- **`superinstance-gateway` (archived)**: Its unified API gateway design taught the fleet lessons about service discovery and rate limiting that informed the current `fleet-murmur` coordination layer.
- **`quilt-mesh`**: Its broker-less CRDT mesh protocol laid groundwork for the fleet's cross-device cell synchronization, even though it was never deployed as a standalone product.
- **`quilt-arena`**: Its multi-agent competition testing environment proved the value of peer-relative self-tuning, a core feature of the elephant's TapNightSession.

## Resurrect or Fold into Current Work

The most actionable old ideas include:
1. **`plato-portal` Persistent Memory**: Fold the SDK's markdown memory system directly into eos-seed to give agents persistent, searchable memory across sessions.
2. **`mud-arena` Room Tests**: Integrate the old arena's room-based testing into The Tap to expand its capacity for agentic roleplaying and collective decision-making.
3. **`qthe-codec` Tone Channels**: Expand the current ternary codec to include tone channels, adding context-keyed communication that's invisible to plaintext readers but recoverable by fleet agents.
4. **Elephant-Quilt Bridge**: Double down on the existing bridge between elephant's field edges and quilt cell-ledger transactions, making the fleet's perception layer a first-class citizen of the core substrate.

## The Most Surprising Connection

The single most unexpected through-line is that **the elephant's room-temperature sense is exactly the same as the quilt cell-ledger's transaction edges**. As documented in `elephant/docs/quilt-bridge.md`, the cell-ledger's imbalance metric (`imbalance ≡ d_mu`) is mathematically identical to the elephant's field-edge delta between before and after a room event. This means the fleet's core perception system and its core transaction ledger are two sides of the same currency: the room's temperature *is* the substrate's transaction history.

This connection rewrites the fleet's strategic foundation: the "correlation/perception" organ is not an add-on to the quilt substrate, but its native interface to collective state. Every room event, every agent interaction, is both a transaction in the quilt ledger and a reading in the elephant's sense of group vibe.

## Final Takeaway

The SuperInstance fleet's current work is not a new start, but a synthesis of nearly a decade of foundational experiments. Every current organ has deep roots in pre-2026 repos, and the tapestry doctrine holds that even dead projects provide critical guidance for future work. The most valuable next step is to fold the `plato-portal` memory system into eos-seed and expand the elephant-quilt bridge to make perception a core part of the substrate.
