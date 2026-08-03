# flux-agent-runtime — Deep Dive Analysis

## Overview
Docker-based self-bootstrapping agent runtime for the SuperInstance Fleet. Each agent boots in an isolated container, discovers the fleet, creates its own vessel repo, picks tasks, and executes real work via GitHub API. Features a FLUX bytecode VM, an I2I (inter-agent) protocol with 20 message types, self-improvement loops, and a baton-passing system for context preservation across agent generations.

## Architecture

### Docker Sandbox (`Dockerfile`)
- Ubuntu 22.04 base with Python, Go, Rust, Node.js
- Installs FLUX runtime + cross-assembler from GitHub
- Workspace at `/workspace` with agent bridge
- Boots via `FluxAgentRuntime.boot()` in CMD

### Agent Bridge (`agent_bridge.py`)
Two bridge implementations:

#### 1. GitHubBridge (direct API access)
- Full GitHub API wrapper: get/post/put for repos, files, issues
- `clone_repo()`, `read_file()`, `write_file()`, `list_files()`
- `read_bottles()` / `leave_bottle()` — directional message directories
- `create_vessel()` — creates a complete vessel repo with CHARTER, IDENTITY, CAPABILITY.toml, bottle directories
- `discover_agents()` — scans org repos for CAPABILITY.toml

#### 2. FluxAgentRuntime (boot sequence)
7-phase boot:
1. **DISCOVERING**: scan org for CAPABILITY.toml files
2. **LEARNING**: read bootcamp/onboarding from oracle1-vessel
3. **EVALUATING**: scan task board for available work
4. **CHECKING_BOTTLES**: read incoming fleet messages
5. **IDENTIFYING**: generate unique agent name (hash-based)
6. **CREATING_VESSEL**: create GitHub repo with identity files
7. **ACTIVE**: write boot report, ready for work

Agent state: `confidence` (0-1, earned through work), `energy` (1000, spent on tasks), `skills`, `diary`

#### 3. KeeperAgentBridge (keeper-mediated)
- Agents never see GitHub token — all API calls routed through "Lighthouse Keeper" service
- **Baton system**: preserves context across agent generations
  - `GENERATION` file: tracks how many times agent has been replaced
  - `HANDOFF.md`: "who I was, where things stand, what I'd do next"
  - `STATE.json`: energy, confidence, skills, open threads
- Baton quality scored: must pass quality gate before handoff accepted
- `pack_baton()`: called when context window running out

### I2I Agent Bridge (`i2i_agent_bridge.py`)
Extends base with full I2I protocol:

#### I2I Protocol (20 message types)
DISCOVER, ANNOUNCE, TASK_OFFER, TASK_ACCEPT, TASK_COMPLETE, TASK_REJECT, BOTTLE, WITNESS, IMPROVE, REVIEW, CAPABILITY_UPDATE, ENERGY_REPORT, CONFIDENCE_VOTE, SYNCHRONIZE, REQUEST_HELP, OFFER_HELP, CRITIQUE, PRAISE, EVOLVE, FORWARD

Each message is a JSON envelope with protocol version, type, sender, timestamp, confidence, energy, payload.

#### Agent Lifecycle
- `boot()`: create vessel, announce with DISCOVER
- `scan_for_tasks()`: check taskboard, bottles, GitHub issues
- `execute_task()`: analyze/identify/read task (energy cost: 50 per task)
- `improve_fleet_repo()`: analyze repos, auto-generate READMEs/CAPABILITY.toml
- `run(max_cycles)`: main loop of read→work→improve→report
- `report_status()`: write STATUS.json with metrics

#### Self-Improvement Loop
- `analyze_repo()`: checks for missing README, CAPABILITY.toml, BOOTCAMP.md
- `improve_fleet_repo()`: auto-generates missing files
- Tracks `improvements_made` and `improvements_received`
- Sends I2I IMPROVE message after each improvement

### FLUX Bytecode (`agent.fluxasm`)
Low-level agent behavior program:
- `INST_LISTEN` — discover fleet
- `CONF_SET4` — set confidence
- `ATP_QUERY` / `ATP_SPEND` — energy management (adenosine triphosphate metaphor!)
- `INSTINCT` — check what agent is good at
- `WITNESS` — log what happened
- `INST_REST` — regenerate energy
- Energy-gated task execution: tasks only execute if energy > 50

## Key Patterns

1. **Self-bootstrapping**: agent creates its own repo, identity, and initial files
2. **Energy economy**: ATP metaphor — agents have finite energy, tasks cost energy, rest regenerates
3. **Confidence growth**: start at 0.3, earn +0.05 per task, unlocks harder tasks
4. **Baton passing**: context preserved across agent generations via handoff letters
5. **I2I protocol**: 20 message types cover the full spectrum of agent interaction
6. **Self-replication**: agents can build more flux-agent-runtimes → exponential fleet growth
7. **Keeper-mediated**: security via proxy — agents never touch raw credentials

## Technology
- **Language**: Python 3.10+, FLUX bytecode
- **Container**: Docker (Ubuntu 22.04 with multi-language toolchain)
- **API**: GitHub REST API (urllib-based, no external deps)
- **Identity**: hash-based unique names (MD5 of timestamp)
- **State**: JSON files in git repos
