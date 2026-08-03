# flux-lucid → DCA Integration Plan

## Phase 1: 9-Channel Intent Encoding
- Every DCA agent message tagged with a 9-channel IntentVector
- Channels: Boundary, Pattern, Process, Knowledge, Social, DeepStructure, Instrument, Paradigm, Stakes
- Intent profile determines message routing, priority, and handling
- Heuristic encoder for initial implementation, model-based encoder later

## Phase 2: Stakes-Based Resource Allocation
- Map C9 (Stakes) to precision and compute allocation:
  - Stakes > 0.75 → Full reasoning (Opus, dual-path verification)
  - Stakes 0.5-0.75 → Standard reasoning (Sonnet/Haiku)
  - Stakes 0.25-0.5 → Light reasoning (GLM-4.5-air)
  - Stakes < 0.25 → Cached/reflex response
- Automatic routing based on stakes assessment
- 50-70% compute savings vs uniform high-precision

## Phase 3: Draft-Tolerance Safety
- Before sending a task to an agent, check draft margin
- Sender draft = complexity/importance of the message
- Receiver capacity = agent's available context depth
- Only dispatch if: receiver_capacity > sender_draft
- Prevents overloading agents beyond their capacity

## Phase 4: Intent Alignment for Fleet Coordination
- When multiple agents collaborate, check intent alignment
- Cosine similarity > threshold = aligned, proceed
- Low similarity = divergence, may need synchronization
- GL(9) zero-holonomy transformation for smooth alignment
- No full consensus needed — just sufficient alignment

## Phase 5: XOR Dual-Path for Critical Decisions
- High-stakes decisions verified via two independent reasoning paths
- Path A: Direct logical analysis
- Path B: Alternative formulation (different model, different prompt)
- Both must agree before action
- Catches reasoning errors, not just computation errors

## Phase 6: Navigation Metaphors as Design Principles
- **Splines in the Ether**: DCA channels are anchor points; agent state flows between them
- **Fair Curve First**: Assess intent before measuring performance
- **Where the Rocks Aren't**: Track what's NOT working as primary improvement signal
- **Draft Determines Truth**: Context depth affects what tasks are safe for each agent
- **Speed Beats Truth**: For real-time tasks, satisfice rather than optimize

## Phase 7: Mixed-Precision Batching
- Group DCA tasks by stakes level
- High-stakes batch: full precision, dual-path verification
- Medium-stakes batch: standard precision
- Low-stakes batch: minimal precision, batch processed
- SIMD-friendly execution when possible

## Key Source Files
- `src/lib.rs` — Channel enum, IntentVector, core types
- `src/intent.rs` — intent encoding, alignment checking
- `src/beam_tolerance.rs` — physical math for precision
- `src/soa_emitter.rs` — mixed-precision batch processing
- `src/intent_compilation.rs` — precision classification
- `src/navigation.rs` — nautical metaphor implementations
- `src/spectral.rs` — spectral invariant tracking
