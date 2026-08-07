# Digital Twin Research — Fleet Mirror Architecture

**Date:** 2026-08-06
**Source:** ABB RobotStudio SmartComponent (DigitalTwin-RobotStudio-SmartComponent)
**Author:** Lucineer Fleet Agent

---

## 1. Architecture Comparison: ABB vs Fleet

| Component | ABB Digital Twin | Fleet Mirror |
|-----------|-----------------|--------------|
| **Real controller** | IRC5/OmniCore cabinet commanding physical servos | Git repos + CI pipelines + agent sessions |
| **Simulation** | RobotStudio 3D station with virtual mechanism | Wiki, fleet dashboard, Roblox game |
| **I/O signals** | Ethernet/PCSDK signal stream (digital/analog/group) | CNS bridge, git webhooks, cron heartbeats |
| **Monitoring loop** | `OnSimulationStep()` per render frame | Cron/heartbeat every 30s–5min |
| **Signal types** | `doSignal`, `diSignal`, `goSignal`, `aoSignal` | Build status, test pass/fail, commit SHA, agent state |
| **Feedback** | Read-only (simulation watches real) | Closed-loop (agent reads mirror, writes back via git/PR) |
| **Human interface** | 3D visualization in RobotStudio | Wiki pages, dashboard, chat notifications |

### Key Insight
ABB's twin is **passive** (read-only). Our fleet twin is **active** (closed-loop) — agents read fleet state, take action, and the mirror updates. This is more powerful but also more complex. Phase 1 should be passive (just watch), Phase 3 adds the active loop.

## 2. Signal Mapping: Fleet Data ↔ Robot Data

| Fleet Signal | Robot Equivalent | Data Type | Update Frequency |
|---|---|---|---|
| `git/repo/lastCommitSHA` | Joint position (RobAx) | String (SHA) | Per commit (event-driven) |
| `git/repo/lastCommitMsg` | — (metadata) | String | Per commit |
| `git/repo/commitCount` | Position counter | Integer | Per commit |
| `ci/repo/lastRunStatus` | Motor enable signal (doMotorOn) | Enum: pass/fail/running | Per CI run |
| `ci/repo/lastRunDuration` | Cycle time | Number (seconds) | Per CI run |
| `test/suite/passCount` | Good parts counter | Integer | Per test run |
| `test/suite/failCount` | Bad parts counter | Integer | Per test run |
| `test/suite/coverage` | Motor current (analog) | Percentage | Per test run |
| `agent/session/active` | Program running (doRunning) | Boolean | Real-time |
| `agent/session/model` | Active tool (aoToolId) | String | Per session |
| `wiki/lastEdit` | Position feedback | Timestamp | Per edit |
| `pr/openCount` | Queue length | Integer | Per PR event |
| `pr/oldestAge` | — (derived) | Duration | Per check |

### Signal Categories (matching ABB's I/O types)
- **Digital signals** (on/off): CI pass/fail, agent active/idle, repo has uncommitted changes
- **Analog signals** (continuous value): test coverage %, commit frequency, issue count
- **Group signals** (enumerated): build status (pass/fail/running/queued), agent state (thinking/acting/waiting/done)

## 3. Implementation Plan

### Phase 1: Mirror Git State (Passive)
**Goal:** A wiki page or dashboard that shows the current state of every fleet repository.

**Components:**
- Cron job (5 min interval) that runs `git log --oneline -1` on each repo
- Writes results to a structured file: `memory/fleet-state.json`
- Wiki page (`fleet-dashboard.md`) that reads the JSON and renders a table
- Signals mirrored: last commit SHA, last commit message, commit count, last commit time

**Existing systems that support this:**
- OpenClaw cron/heartbeat (scheduling)
- `exec` tool (git commands)
- `memory/` directory (state persistence)
- Wiki rendering (display)

**Effort:** Small. A single cron script + a wiki template.

### Phase 2: Mirror Test State (Passive + Alerting)
**Goal:** Engine room gauges showing CI status across the fleet.

**Components:**
- Extend Phase 1 cron to run test suites or read CI results
- Add pass/fail/running status to `fleet-state.json`
- Add alerting: if a repo goes from pass → fail, notify via chat
- Add historical tracking: last 10 CI runs per repo (sparkline data)

**Existing systems:**
- `gh` CLI (CI status from GitHub Actions)
- CNS bridge (notifications)
- Fleet dashboard (display)

**Effort:** Medium. Need CI integration per repo and historical state management.

### Phase 3: Mirror Agent State (Active/Closed-Loop)
**Goal:** Real-time crew positions — which agents are working, what they're doing, what they've done.

**Components:**
- Agent session registry: each agent writes its state to `memory/agent-state.json`
- States: `thinking`, `acting`, `waiting`, `done`, `idle`
- Activity feed: last 5 actions per agent (commit, PR, file edit, message)
- Dashboard renders the crew as a watch bill: who's on watch, who's below

**Existing systems:**
- OpenClaw session management (session IDs, status)
- `memory/` directory (state)
- PersonalLOG (activity tracking)
- CNS bridge (inter-agent communication)

**Effort:** Large. Requires agent instrumentation — each agent must write its state at key transitions. But high value: makes the fleet legible to the human.

## 4. Existing Fleet Systems That Support This

| System | Role in Digital Twin | Current Status |
|---|---|---|
| **CNS Bridge** | Signal transport (like ABB's Ethernet/PCSDK) | ✅ Live |
| **PersonalLOG** | Per-agent activity log (signal history) | ✅ Live |
| **Fleet Dashboard** | Display surface (like RobotStudio UI) | ⚠️ Exists but needs auto-refresh |
| **Memory Files** | State persistence (like ABB's StateCache) | ✅ Live |
| **Cron/Heartbeat** | Monitoring loop (like OnSimulationStep) | ✅ Live |
| **Git Webhooks** | Event-driven signal (like position change interrupt) | ❌ Not configured |
| **Roblox Game** | 3D visualization (like RobotStudio station) | ✅ Live, needs fleet integration |

## 5. Minimal Viable Twin (MVP)

The absolute minimum viable digital twin for the fleet:

1. **One cron script** that runs every 5 minutes
2. Reads `git log -1 --format="%H %s %ci"` from each fleet repo
3. Reads `gh run list --limit 1` for CI status (if available)
4. Writes to `memory/fleet-state.json`
5. A wiki page reads that JSON and renders it as a table

This gives us: repo name | last commit | time | CI status — for every repo, auto-updating.

That's the `MonitorMechanism` function. That's the digital twin. Everything else is embellishment.

## 6. The Roblox Connection

The Roblox game could become a true fleet visualization:
- Each repo = a building in the harbor
- Building height = commit count (grows over time)
- Building glow = CI status (green=pass, red=fail, yellow=running)
- Smoke from chimney = agent active
- This is the ABB 3D simulation, but for code instead of robots

The vessel in the harbor IS the fleet. When a repo grows, the building grows. When tests break, the lighthouse goes dark. When agents are working, the forge fires burn.

The simulation mirrors the real. The real adjusts based on the simulation. The loop closes.
