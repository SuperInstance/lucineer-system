# fleet-murmur-worker — Deep Dive Analysis

## What It Does
A TypeScript worker that runs the 5 Murmur thinking strategies continuously as a Cloudflare Worker. Results are quality-gated then pushed to PLATO (the fleet's persistent memory layer). Part of the "reverse-actualization truck" — it generates insights from fleet data and feeds them back into fleet knowledge.

## Architecture
- **3 Core Modules**:
  - `MurmurWorker` (`index.ts`): Main worker class. Runs cycles: pick theorem → generate insights → quality gate → push to PLATO
  - `Scheduler` (`scheduler.ts`): Orchestrates theorem rotation. Picks least-recently-run theorem, tracks statistics (pass rate via EMA), time-since-last-run per theorem
  - `IdleDetector` (`idle_detector.ts`): System resource awareness. Skips work when battery <20%, CPU >80°C, user idle >10min, or hourly insight cap reached

- **Quality Pipeline**: Raw insight → `computeQuality()` → threshold (0.35 default) → PLATO writer
- **Theorem Rotation**: Each cycle picks the theorem that hasn't been run in the longest time. EMA pass-rate tracking (α=0.1) for quality monitoring.

## Key Innovations
1. **Quality Gating**: Not all insights make it to PLATO. Each is scored; below-threshold results are logged but not committed. Prevents noise from flooding fleet knowledge.
2. **Idle-Aware Execution**: The worker checks battery, CPU temperature, user activity, and hourly output caps before doing work. Self-limiting to avoid degrading the host.
3. **Theorem Rotation via Recency**: Rather than round-robin, picks the least-recently-run theorem. This naturally adapts to varying execution times.
4. **Exponential Moving Average Quality Tracking**: Pass rate tracked with EMA (α=0.1) — recent performance weighted more than historical.
5. **Graceful Shutdown**: SIGINT/SIGTERM handlers, clean interval clearing, status logging.
6. **Diminishing Returns Detection**: Max insights per hour (default 5) prevents quality degradation from over-production.

## Code Quality
- **Good**: Clean separation of concerns, proper error handling, structured logging
- **Practical**: Real system checks (reads /sys/class/power_supply/BAT0/capacity, thermal zones)
- **Well-configurable**: Config objects with defaults, quality threshold customizable

## DCA / Slackwater Integration Points
- **Quality-Gated Output**: Every DCA agent output should pass a quality gate before being committed to shared state. Maps directly.
- **Idle Detection → DCA Heartbeat**: The idle detector pattern is exactly what DCA needs for "should I do work now?" decisions during heartbeat polls.
- **Theorem Rotation → Task Scheduling**: Recency-based task selection prevents starvation of low-priority items.
- **PLATO Integration**: Pushing validated results to a persistent knowledge layer = DCA's memory consolidation.
- **Reverse-Actualization**: Generating insights FROM fleet data and feeding them BACK = reflexive knowledge improvement.

## Patterns to Adopt
1. **Quality gate before persistence** — threshold-based filtering of agent output
2. **Idle-aware execution** — battery/CPU/activity checks before doing work
3. **Recency-based task rotation** — least-recently-run first
4. **EMA quality tracking** — smooth, responsive quality metrics
5. **Hourly output caps** — prevent diminishing returns
6. **Graceful shutdown** — SIGINT/SIGTERM with clean state
7. **Periodic status logging** — visibility into running workers
