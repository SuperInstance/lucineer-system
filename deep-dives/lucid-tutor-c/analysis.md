# lucid-tutor-c — Deep Dive Analysis

## What It Does
A **C port of the lucid-tutor engine** — the same vibration-based learning system, implemented close to the metal. Provides the same core types (Vibration, Tutor, LearningGroup, TeachingMoment) with deterministic memory layout and zero-allocation operation.

## Architecture
- **Pure C** (`lucid_tutor.c` + `lucid_tutor.h`)
- **Fixed-size arrays** instead of HashMaps:
  - Vibration: max 32 topics, each with 64-char name
  - Tutor: max 16 learners, 256 teaching history entries
  - LearningGroup: max 8 members
- **Exponential moving average** for topic level (α=0.3) — different from Rust version
- **Cosine similarity** for resonance calculation
- **Build**: `mkdir build && cd build && cmake .. && make && ctest`

## Key Differences from Rust Version
1. **EMA instead of weighted blend**: C uses α=0.3 EMA for level updates. Rust uses conditional logic (breakthrough boost, progress fraction).
2. **Delta-based outcome classification**: C classifies by delta (level change), Rust by absolute thresholds + iteration history.
3. **Fixed limits**: C has hard limits (32 topics, 16 learners). Rust uses dynamic HashMap.
4. **Simpler stuck detection**: C uses `fabs(delta) <= 0.02` for stuck. Rust uses `result < 0.3 && iterations > 3`.
5. **No adaptive style**: C doesn't implement Adaptive tutor style switching.

## Code Quality
- **Clean C**: Well-structured, proper header file, helper functions
- **Practical**: Fixed sizes appropriate for embedded/edge use
- **Tested**: `tests/test_tutor.c` validates core functionality
- **Portable**: Pure C with only `math.h` dependency

## DCA / Slackwater Integration Points
- **Edge Deployment**: C version can run on constrained devices alongside DCA agents
- **Deterministic Memory**: Fixed-size structs enable pre-allocation and memory planning
- **FFI Bridge**: Can be called from higher-level languages via FFI

## Patterns to Adopt
1. **Fixed-size entity limits** — prevents unbounded memory growth in long-running agents
2. **EMA for smooth level tracking** — less noisy than raw result values
3. **Delta-based classification** — simpler than multi-factor thresholds
4. **Dual-language implementation** — high-level for dev, C for production/edge
