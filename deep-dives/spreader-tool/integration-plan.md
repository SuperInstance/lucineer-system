# spreader-tool → DCA Integration Plan

## Phase 1: Deadband Detection for DCA Agents
- Port DeadbandDetector to DSA's monitoring layer
- Per-agent KPI tracking: task success rate, response time, error rate, resource usage
- Duration gates prevent over-reaction to transient failures
- Hysteresis prevents oscillation between "healthy" and "struggling" states
- Severity scoring for prioritization

## Phase 2: Seed Library (Skill Locking)
- Implement the seed lifecycle for DCA skills
- When an agent finds a validated approach, propose it as a candidate seed
- Backtest against historical performance
- Lock proven seeds → deploy fleet-wide as reflex responses
- Version seeds with major.minor versioning
- Deprecation with replacement tracking

## Phase 3: Frozen Context Windows
- When an agent fails or enters deadband, snapshot the full reasoning context
- Copy-on-write, content-addressed storage
- Enables post-mortem debugging: "what was the agent thinking when it failed?"
- Redaction engine prunes low-value snapshots over time
- KPI-space distance for intelligent pruning

## Phase 4: Self-Optimization Loop
- Each DCA agent monitors its own performance patterns
- Lock proven development patterns (test-first, CI/CD, code review)
- Generate improvement reports automatically
- Track deadband status per agent skill area

## Phase 5: 8-Step Tick Loop
- Implement the SpreaderRoom 8-step loop as DCA's core monitoring cycle:
  1. Capture agent state
  2. Aggregate over sliding window
  3. Snapshot on deadband entry
  4. Check deadband status
  5. Check escalation need
  6. Run local inference (use locked seeds)
  7. Update seed candidates
  8. Sync state to fleet

## Phase 6: Development Pattern Library
- Curate 7+ proven patterns for DCA agent development
- Lock patterns after validation
- Auto-check agents against pattern library
- Fleet-wide pattern deployment

## Key Source Files
- `spreader/spreader_room.py` — 8-step tick loop orchestrator
- `spreader/deadband.py` — deadband detection with hysteresis
- `spreader/seed_lock.py` — seed lifecycle management
- `spreader/frozen_context.py` — FCW lifecycle
- `spreader/types.py` — all dataclasses, state machines, constants
- `spreader/self_optimize.py` — self-monitoring harness
- `spreader/development_patterns.py` — 7 locked patterns
- `spreader/redaction.py` — KPI-space distance pruning
- `spreader/cost.py` — intelligence cost tracking
