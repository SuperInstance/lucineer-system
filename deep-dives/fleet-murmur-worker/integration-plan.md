# fleet-murmur-worker → DCA Integration Plan

## Phase 1: Quality-Gated Agent Output
- Every DCA agent output passes through a quality scorer before being committed
- Quality threshold configurable per agent role (0.35 default, 0.7 for critical decisions)
- Below-threshold outputs logged but not persisted to shared memory
- Quality metrics feed back into agent self-improvement

## Phase 2: Idle-Aware Heartbeat
- Port IdleDetector to DCA's heartbeat system
- Check battery (Linux /sys/class/power_supply), CPU temp (thermal zones), user activity
- Skip non-urgent work when host is constrained
- Track insights-per-hour to prevent diminishing returns
- Integrate with DCA's existing heartbeat state file

## Phase 3: Recency-Based Task Selection
- Replace simple round-robin with least-recently-run task selection
- Track last-run timestamp per task
- Natural priority adjustment based on neglect
- Prevents starvation of infrequent-but-important tasks

## Phase 4: EMA-Based Quality Monitoring
- Track per-agent quality via exponential moving average (α=0.1)
- Detect quality degradation early
- Auto-adjust thresholds based on historical performance
- Fleet-wide quality dashboard

## Phase 5: PLATO-Like Memory Consolidation
- Periodic background process that:
  1. Picks underexplored topics (least recently examined)
  2. Runs thinking strategies against fleet data
  3. Quality-gates results
  4. Pushes validated insights to persistent memory
  5. Logs everything for audit

## Key Source Files
- `src/index.ts` — worker pattern (runCycle, start/stop, status)
- `src/scheduler.ts` — recency-based rotation, EMA tracking
- `src/idle_detector.ts` — system resource checks (battery, CPU temp, idle time)
