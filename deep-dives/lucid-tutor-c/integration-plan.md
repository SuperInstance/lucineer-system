# lucid-tutor-c → DCA Integration Plan

## Phase 1: Edge Agent Runtime
- Compile lucid-tutor-c as a library for edge DCA agents
- Provides competence tracking on constrained devices (Pi, Jetson)
- FFI bindings for Python/TypeScript DCA orchestrators

## Phase 2: Bounded Resource Planning
- Adopt fixed-size entity limits pattern (max N agents, max M skills per agent)
- Pre-allocate memory pools for agent state
- Prevent unbounded growth in long-running fleet deployments
- Configurable limits via compile-time constants

## Phase 3: Dual-Implementation Strategy
- High-level (TypeScript) for development and rich features
- C for production deployment and edge devices
- Shared test suite to verify behavioral equivalence
- Performance comparisons between implementations

## Key Source Files
- `src/lucid_tutor.c` — C implementation
- `src/lucid_tutor.h` — public API
- `tests/test_tutor.c` — tests
