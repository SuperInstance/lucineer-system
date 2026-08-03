# spreader-tool — Deep Dive Analysis

## What It Does
**Intelligence tiling for PLATO rooms** — watches agent rooms for "deadband" (the gap between what hardcoded rules handle and what needs real intelligence). When a room enters deadband, Spreader freezes reasoning snapshots, validates them, and locks proven-good checkpoints (Seeds) that deploy fleet-wide. A **self-improving reflex system** for agent fleets.

## Architecture
- **Python, zero dependencies** — pure dataclasses, no framework lock-in
- **12 modules**, ~2500 lines total, 241 tests

### The 8-Step Intelligence Tiling Loop (SpreaderRoom)
1. **CAPTURE STATE** — record incoming KPIs
2. **UPDATE SLIDING WINDOW** — aggregate metrics over context window (default 6 ticks)
3. **CREATE FROZEN SNAPSHOT** — snapshot KPIs when deadband first detected
4. **CHECK DEADBAND** — are we struggling?
5. **CHECK ESCALATION** — need LLM help?
6. **RUN LOCAL INFERENCE** — use locked seed if available
7. **UPDATE SEED LOCK** — validate / promote candidates
8. **SYNC** — return state for peer coordination

### Deadband Detection (`deadband.py`)
- **4 KPI Metrics** with independent thresholds and duration gates:
  - Task completion rate < 90% for 5+ minutes
  - Average wait time > 30s for 30+ seconds
  - Energy over baseline > 10% for 30+ seconds
  - Inference MAE > 10% for 3 consecutive windows
- **Hysteresis**: Exit thresholds are relaxed by `hysteresis_exit_factor` to prevent flickering
- **Severity scoring**: 0-1 based on breach count × duration factor (ramps 0.3→1.0 over 10 min)

### Frozen Context Window Lifecycle
`STAGING → FROZEN → TESTING → REFINING → LOCKED` (or `DISCARDED` at any pre-lock stage)

### Seed Lifecycle (8 states)
`UNLOCKED → CANDIDATE → VALIDATING → LOCK_PENDING → LOCKED → DEPRECATED → ARCHIVED`
- Seeds are intelligence checkpoints validated via KPI-threshold backtest
- Default validation: `task_completion_rate >= 95%` (SEED_LOCK_KPI)
- Once locked, seeds deploy fleet-wide as reflex responses

### Cost Tracking
- Intelligence cost tracked per FCW
- Refinement gradient computed for optimization
- Low-value FCWs pruned via redaction engine

### Self-Optimization
- `SelfOptimizer` monitors its own development process
- `development_patterns.py` contains 7 locked patterns:
  - test-first-development, continuous-integration, code-review-before-merge, semantic-versioning, dependency-pinning, documentation-drift-prevention, performance-regression-monitoring

### Redaction Engine
- Prunes FCWs by KPI-space distance
- Content-addressed file storage with dedup
- Target reduction percentage configurable

## Key Innovations
1. **Deadband Detection**: Identifies exactly WHERE rules end and intelligence is needed. This is the fundamental question for any AI system: when do you need to think harder?
2. **Frozen Context Windows**: Immutable snapshots of reasoning state at the moment of struggle. Copy-on-write, content-addressed. You can replay exactly what the agent was thinking when it failed.
3. **Seed Locking Pipeline**: Validated intelligence checkpoints that deploy fleet-wide. This is institutional learning — proven responses become reflexes.
4. **Hysteresis on Deadband**: Prevents rapid on/off flickering. Once in deadband, you need to recover PAST the threshold to exit. Stable, not oscillating.
5. **Sliding Window Aggregation**: KPIs averaged over N recent ticks, not just instantaneous values. Smooths noise.
6. **Self-Optimization**: The tool monitors its own development patterns. It has opinions about how it should be built. Meta-cognitive.
7. **Zero Dependencies**: Pure Python dataclasses. No framework lock-in. Runs anywhere.
8. **Development Pattern Library**: 7 proven patterns locked and ready for fleet deployment.

## Code Quality
- **Exceptional**: 241 tests in <1 second, 12 well-separated modules, clean docstrings
- **Architecture diagram** in README
- **Type-safe**: Full type hints throughout
- **State machines** properly implemented with transition guards
- **Immutable dataclasses** with copy-on-write semantics

## DCA / Slackwater Integration Points
- **Deadband Detection → DCA Capability Gaps**: Every DCA agent has deadbands — tasks too complex for rules, too frequent for full LLM. Detect and fill them.
- **Seed Locking → DCA Skill Library**: Locked seeds = validated agent responses that deploy fleet-wide. This is the DCA skill library mechanism.
- **Frozen Context Windows → DCA Debugging**: When an agent fails, freeze the context for analysis. Copy-on-write snapshots.
- **Self-Optimization → DCA Self-Improvement**: Agents monitor their own performance patterns and lock proven approaches.
- **Sliding Window KPI Aggregation → DCA Health Metrics**: Don't react to instantaneous values. Smooth metrics over windows.
- **Hysteresis → DCA State Stability**: Prevent oscillation in state transitions.

## Patterns to Adopt
1. **Deadband detection with duration gates** — sustained breach required, not instantaneous
2. **Hysteresis on state transitions** — exit threshold > entry threshold
3. **Frozen context snapshots** — immutable reasoning state for debugging
4. **Seed locking pipeline** — candidate → validate → lock → deploy
5. **8-step tick loop** — capture, aggregate, check, escalate, infer, update, sync
6. **Self-optimization harness** — monitor own development, lock patterns
7. **KPI-space distance pruning** — intelligent cleanup of low-value artifacts
8. **Development pattern library** — proven patterns as locked, deployable seeds
9. **Zero-dependency design** — pure dataclasses, portable, no framework lock-in
10. **Severity scoring** — breach_count × duration_factor for prioritization
