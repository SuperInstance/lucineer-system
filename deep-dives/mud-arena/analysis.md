# MUD Arena — Architecture Analysis

> **Repo:** [SuperInstance/mud-arena](https://github.com/SuperInstance/mud-arena)
> **Analyst:** Lucineer Deep-Dive
> **Date:** 2026-08-02

---

## 1. Executive Summary

MUD Arena is a **polyglot agent simulation framework** that uses classic Multi-User Dungeon (MUD) text-adventure mechanics as the substrate for testing, benchmarking, and evolving AI agent decision-making. It is part of the **SuperInstance/OpenConstruct ecosystem** — a "Cocapn Fleet" of repos building toward spatial, agent-driven software.

The core insight: MUD mechanics (rooms, exits, items, combat) provide a **structured world with discrete state** that is richer than GridWorld but more grounded than free-form LLM chat. This makes it an ideal **gym environment** for studying agent behavior, emergent cooperation, and evolutionary optimization of decision scripts.

---

## 2. Purpose & Scope

### What Problem It Solves

AI agent research lacks a middle ground between:
- **GridWorld** — too simple, unrealistic topology
- **Free-form LLM chat** — unstructured, hard to measure
- **Full 3D simulation** — expensive, hard to reproduce

MUD Arena fills this gap with **text-adventure physics**: graph-structured rooms, items with properties, NPCs, hazards, and rule-based combat — all with deterministic, measurable outcomes.

### Scope

| Dimension | Coverage |
|-----------|----------|
| World model | Room graphs, items, inventories, NPCs, hazards |
| Agent model | Perceive → decide → act loop with pluggable decision functions |
| Command system | 10 MUD verbs with aliases and multi-part parsing |
| Evolution | Genetic algorithm with tournament selection, crossover, mutation |
| Observation | WebSocket (7779), Telnet (7778), HTTP REST API (7780) |
| Hardware | CUDA GPU, CPU fallback, Zig edge runtime, WASM browser client |

---

## 3. Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    MUD ARENA ARCHITECTURE                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐ │
│  │ Python Core │  │  GPU Engine  │  │  Edge Runtime      │ │
│  │ (mud_arena) │  │  (CUDA .cu)  │  │  (Zig + WASM)      │ │
│  │             │  │              │  │                    │ │
│  │ • Rooms     │  │ • 1 block    │  │ • <100KB binary    │ │
│  │ • Agent     │  │   = 1 room   │  │ • SSH terminal     │ │
│  │ • Commands  │  │ • 1 thread   │  │ • WASM browser     │ │
│  │ • Inventory │  │   = 1 agent  │  │ • Battery sim      │ │
│  │ • Events    │  │ • Shared mem │  │ • Comm resolution  │ │
│  │             │  │   for room   │  │ • Agent briefing   │ │
│  └──────┬──────┘  └──────┬───────┘  └─────────┬──────────┘ │
│         │                │                    │             │
│         └────────────────┼────────────────────┘             │
│                          │                                   │
│  ┌───────────────────────┴───────────────────────────────┐ │
│  │              SIMULATION MODULES                        │ │
│  │  • evolve.py      — GA engine (PyTorch GPU optional)   │ │
│  │  • scenario_gen   — Random + LLM scenario creation     │ │
│  │  • script_compiler — DSL ↔ binary, mutation, crossover │ │
│  │  • server.py      — WebSocket/Telnet/HTTP observer     │ │
│  │  • tolerance.py   — Sim vs. reality drift tracking     │ │
│  │  • dashboard.py   — HTML dashboard generation          │ │
│  │  • human_interface — Terminal client (3 modes)         │ │
│  └───────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Core Python Package (`src/mud_arena/`)

### 4.1 `rooms.py` — Spatial World Model

**Key types:** `Room`, `RoomGraph`

- `Room` is a dataclass with `id`, `name`, `description`, `exits` (direction → room_id dict), `items` (ground items), `npcs`, and `metadata` (arbitrary tags).
- `RoomGraph` is a directed graph of rooms with:
  - `add_room()`, `connect()` (one-way or bidirectional), `remove_room()` (auto-cleans dangling exits)
  - `navigate(from, direction)` → destination room_id or None
  - `exits_for(room_id)` → dict of available exits
  - `__contains__` and `__len__` for ergonomic checks

**Design pattern:** Simple aggregate root. RoomGraph owns all rooms and enforces referential integrity on removal.

### 4.2 `commands.py` — Command Parser

**Key types:** `Verb` (enum), `Command` (frozen dataclass), `parse_command()`

Supported verbs:
| Verb | Aliases | Example |
|------|---------|---------|
| GO | move, walk, run, head | `go north` |
| LOOK | l | `look` |
| EXAMINE | x, inspect | `examine crystal` |
| TAKE | get, pick up, grab | `take key` |
| DROP | — | `drop torch` |
| USE | — | `use key with door` |
| TALK | — | `talk to guard` |
| INVENTORY | i, inv | `inventory` |
| HELP | — | `help` |
| QUIT | exit, q | `quit` |

**Design pattern:** Functional parser — `parse_command(text)` returns a `Command`. No mutable state. Direction shorthand supported (`north` → `GO north`).

Three-part commands (`use X with Y`, `talk to X`) are split on prepositions using `frozenset` lookups.

### 4.3 `agent.py` — Agent Loop

**Key types:** `Agent` (dataclass), `DecisionFn` (type alias for `Callable[[Dict], Command]`)

The agent implements a **perceive → decide → act** cycle:

1. **`perceive(graph)`** — Builds a perception dict from the current room (name, description, exits, items, NPCs, inventory)
2. **`decide(perception)`** — Calls the pluggable `_decision_fn` (default: just `LOOK`)
3. **`act(command, graph, bus)`** — Mutates world state and emits events

Each verb has a dedicated handler (`_do_go`, `_do_take`, etc.) that mutates room state and emits events on the EventBus.

The `step()` method runs the full cycle, optionally accepting raw command text to bypass the decision function (for human-driven or scripted interaction).

**Design pattern:** Strategy pattern via `DecisionFn`. The decision logic is a callable that can be swapped at runtime — this is the primary extension point for plugging in LLM agents, rule-based AI, or human input.

### 4.4 `inventory.py` — Item System

**Key types:** `Item` (dataclass), `Inventory` (container with capacity)

- Items have `name`, `description`, `usable` flag, `uses` counter (-1 = unlimited), and `tags`
- `Item.use()` consumes one use; items auto-removed at 0 uses
- `Inventory` supports capacity limits, tag-based queries (`find_by_tag`), and dict-like access

**Design pattern:** Value object (Item) + bounded collection (Inventory). Clean separation between item properties and container management.

### 4.5 `events.py` — Pub/Sub Event System

**Key types:** `EventType` (enum), `Event` (dataclass), `EventBus`

Event types: `ROOM_ENTER`, `ROOM_LEAVE`, `ITEM_PICKED_UP`, `ITEM_DROPPED`, `ITEM_USED`, `NPC_SPOKE`, `ROOM_EVENT`, `AGENT_ACTION`, `CUSTOM`

- Synchronous pub/sub with subscribe/unsubscribe
- Internal event log with filtered history queries
- `Event` carries `type`, `source`, `data` dict, and `room` context

**Design pattern:** Observer pattern. Agents and game systems subscribe to event types and react to world changes.

---

## 5. Simulation Modules (`src/`)

### 5.1 `server.py` — Multi-Protocol Observation Server

A full async server providing three observation protocols:

| Protocol | Port | Use Case |
|----------|------|----------|
| WebSocket | 7779 | Browser-based real-time watching |
| Telnet | 7778 | Legacy/SSH-style clients |
| HTTP REST | 7780 | Programmatic access, scenario injection |

**Architecture:**
- `World` dataclass holds shared state (rooms, agents, scores, generation stats)
- `SimulationRunner` reads from GPU binary stdout (newline-delimited JSON) or falls back to `CPUFallbackSimulator`
- Each protocol has its own handler but shares the same `World` instance
- `watch <agent_id>` command sets up a live push feed for a specific agent

**REST endpoints:** `/status`, `/agents`, `/rooms`, `/scores`, `/generation`, `/scenarios`, POST `/inject-scenario`

### 5.2 `evolve.py` — Genetic Algorithm Engine

Implements the full evolution pipeline:

1. **Initialize** — Random population of N scripts (rule lists)
2. **Evaluate** — Run each script on K scenarios; optional PyTorch GPU acceleration
3. **Select** — Tournament selection of elites
4. **Crossover** — Single-point recombination
5. **Mutate** — Per-gene mutation at configurable rate
6. **Replace** — Keep elites + offspring
7. **Repeat**

Features:
- Adaptive scenario generation (LLM hook placeholder)
- LLM review hook for strategy analysis
- Statistics tracking (avg/best/worst fitness, convergence slope, diversity via Hamming distance)
- Population export/import via pickle
- Full CLI with `--generations`, `--population`, `--scenarios`, `--mutation`, `--tournament`, `--adaptive`

### 5.3 `scenario_generator.py` — World Generation

Two modes:
- **Random** — Template-based: rooms with random terrain, items, enemies, hazards, connected graph, victory conditions
- **LLM-driven** — Sends schema-aware system prompt to OpenAI-compatible API, parses JSON response into `Scenario` dataclass

Adaptive mode (`generate_challenge`): adjusts difficulty based on recent success rate — more enemies/hazards if agents succeed, fewer if they struggle.

Tournament mode (`generate_tournament`): generates scenarios evenly spread across a difficulty range.

### 5.4 `script_compiler.py` — DSL & Binary Compilation

Defines a custom DSL for agent scripts:
```
"MyScript"
WHEN hp < 30% AND enemy_in_room THEN use_item health_potion
WHEN gold_on_ground THEN pickup gold
DEFAULT move random_exit
```

Features:
- DSL → `ScriptRule` list with validation (contradictory condition detection)
- Binary serialization (`struct.pack`) for GPU upload — 20 bytes per rule
- Random script generation
- Mutation (per-rule, with structural changes: add/delete rules)
- Crossover (single-point, preserves default rule)
- Pretty-print back to DSL

Binary format: `int32 rule_count` + repeated `[int32 × 5]` (condition_type, condition_param, action_type, action_param, priority).

### 5.5 `tolerance.py` — Sim-vs-Reality Tracking

Tracks divergence between simulation predictions and real-world measurements:

- `Measurement` records variable name, predicted, actual, timestamp, unit, source
- Computes error percentage, drift detection (trending), confidence scoring
- `calibrate()` returns a multiplicative correction factor
- JSON persistence for state save/load
- `suggest_adjustments()` generates human-readable recommendations for variables exceeding 10% tolerance

**Purpose:** When agents deploy to real hardware (drones, sensors), the simulation-to-reality gap is the critical calibration loop.

### 5.6 `dashboard.py` — Evolution Visualization

Reads a JSON history file and produces a self-contained HTML dashboard with Chart.js:
- Fitness line chart (best/avg/worst per generation)
- Top-10 scripts table
- Scenario difficulty vs survival rate
- Strategy distribution pie chart
- Evolution timeline of breakthroughs
- Script complexity trend
- LLM scenario log

### 5.7 `human_interface.py` — Terminal Client

Three output modes:
- **NORMAL** — Classic adventure text
- **CALIBRATION** — Numeric telemetry with error tracking
- **AGENT_VIEW** — Raw agent perspective for debugging

Features WebSocket connection with offline fallback, pause/resume simulation control, and an interactive REPL.

---

## 6. GPU Engine (`src/mud_arena.cu`)

### Architecture

- **One CUDA block = one room** — shared memory holds room state
- **One CUDA thread = one agent** in that room
- Global memory holds agents, scripts, scenario results

### Simulation Kernel (`simulate_scenario`)

Each thread:
1. Loads agent state from global memory
2. Reads its script rule
3. Evaluates condition (hp_below, enemy_present, item_available, time_elapsed, random)
4. Executes action (move, attack, pickup, use_item, cast, flee, trade, wait)
5. Writes back results (health, gold, enemies_defeated, rooms_explored, items_collected, turns_survived)
6. Composite score calculated from weighted metrics

### Script Evaluation Kernel (`evaluate_scripts`)

Simple reduction: averages agent scores per script ID.

### Known Issues (from 12-model audit)

| Issue | Severity |
|-------|----------|
| Race conditions in shared memory (`s_room`) | **CRITICAL** |
| No agent state write-back to global memory | **CRITICAL** |
| Missing `__syncthreads()` after agent actions | **HIGH** |
| Uncoalesced global memory access | **MEDIUM** |
| No CUDA error checking | **MEDIUM** |

### Jetson Experiment (`jc1_experiment_mud_arena.cu`)

A hyper-compressed CUDA experiment targeting Jetson Orin Nano:
- 64 scripts, 128 rooms, 200 turns, 100 generations
- Device-side rule storage, evolution kernel
- Runs entirely on GPU (no host iteration except generation loop)
- Reports time per generation on sm_87

---

## 7. Edge Runtime (`src/mud_arena.zig`)

A single-file Zig implementation targeting edge devices:
- **Binary size:** <100KB with `ReleaseSmall`
- **Targets:** aarch64-linux (Pi, Jetson), x86_64-linux, wasm32-wasi
- **No external dependencies** — pure Zig stdlib

Key features:
- Full world model (rooms, agents, items, exits)
- Human avatar with perception modes (normal, calibration, agent_view, god)
- Command processing (look, go, status, agents, brief, quit)
- Background tick thread (100ms period)
- Agent briefing system — human can assign mission text to agents
- Communication resolution decay based on distance
- Battery drain simulation

### Boarding Model

The Zig runtime implements the **"board, brief, beam off"** philosophy:
1. Human **boards** via SSH
2. **Briefs** agents on mission objectives
3. **Beams off** — agents continue autonomously
4. Communication resolution drops with distance
5. Agents return to dock when mission complete or battery low

---

## 8. WASM Client (`src/wasm_mud.c` + `src/mud_arena.html`)

### C/WASM Core

A packed-struct `WorldState` with:
- 64 rooms, 32 agents, 1 human avatar
- Room connections (N/E/S/W exits)
- Agent battery drain and autonomous movement
- Communication resolution based on BFS distance from dock
- Calibration measurement storage
- Agent briefing system

Exported functions: `mud_init`, `mud_command`, `mud_tick`, `mud_get_output`, `mud_get_room`, `mud_get_agents`, `mud_human_enter`, `mud_human_act`, `mud_measure`

### HTML Client

A cyberpunk-styled browser interface:
- Dark theme with green monospace text
- Terminal output area (80-column feel)
- Sidebar with agent list and calibration toggle
- Status bar (room, battery, comm resolution)
- Human boarding/beaming controls

---

## 9. Dependencies & Integrations

### Python Dependencies

| Package | Required For |
|---------|-------------|
| (none) | Core `mud_arena` package — zero deps |
| websockets ≥12.0 | Server |
| aiohttp ≥3.9 | HTTP REST API |
| numpy ≥1.24 | Evolution engine |
| openai ≥1.0 | LLM scenario generation |
| matplotlib ≥3.8 | Visualization |
| pytest ≥7.0 | Testing |

### Build Dependencies

| Language | Compiler |
|----------|----------|
| CUDA | nvcc (CUDA 12.6+, sm_87 for Jetson Orin) |
| Zig | Zig master (0.13+) |
| C/WASM | emcc (Emscripten) |
| Python | ≥3.10 |

### Ecosystem Connections

Per `AGENT.md`, the fleet neighbors:
- `tminus-dispatcher` — Temporal Heartbeat Keeper
- `fleet-bridge` — A2A Transport Operator
- `symphony-runtime` — Grammar Conductor
- `composite-headspace` — Dual-Shell Mediator
- `i2i-bottle-agent` — Bottle Postmaster

---

## 10. Testing

The test suite (`tests/`) covers:

| File | Coverage |
|------|----------|
| `test_rooms.py` | Room creation, navigation, exit cleanup, nonexistent rooms |
| `test_commands.py` | All verb forms, aliases, shorthand, empty/unknown input |
| `test_agent.py` | Perception, decision, action (move/take/drop/use/talk), event emission |
| `test_inventory.py` | Add/remove/has, capacity limits, use depletion, tag queries |
| `test_events.py` | Subscribe/emit/unsubscribe, history filtering, room event reactions |

CI runs on Python 3.10/3.11/3.12 via GitHub Actions, with flake8 linting and pytest.

---

## 11. Design Philosophy

### The γ + η = C Ternary

Each agent action is classified as:
- **(γ) Exploratory** — navigating, searching, gathering (low-risk information gain)
- **(η) Exploitative** — combat, resource consumption, goal completion (high-risk reward)

The balance γ/(γ+η) is the **exploration-exploitation ratio**, connecting MUD Arena to fundamental reinforcement learning theory.

### The Boarding Manifesto

The central UX vision:
> *"Board the ship. Brief the crew. Beam off. They come home with the catch."*

This positions the MUD as an interface paradigm where:
- Humans visit, agents persist
- The human IS the calibration instrument
- Scripts evolve to need less human intervention over time

### Reverse Actualization

The repo contains a "reverse actualization" document working backwards from a 2031 dream of spatial, intention-based computing to 2026 build orders. MUD Arena is positioned as a foundational primitive in this path — spatial coordinates as identity, agents as crew, MUD as the universal interface.

---

## 12. Strengths & Weaknesses

### Strengths

1. **Exceptional documentation** — Best in the SuperInstance org (per external audit)
2. **Polyglot with clear separation** — Python for logic, CUDA for speed, Zig for edge, WASM for browser
3. **Zero-dependency Python core** — The `mud_arena` package needs nothing beyond stdlib
4. **Pluggable agent architecture** — `DecisionFn` makes it trivial to swap in LLM agents
5. **Comprehensive test coverage** — All core modules have focused unit tests
6. **Vision-driven design** — Every technical choice traces back to the Boarding Manifesto

### Weaknesses

1. **Critical CUDA bugs** — Race conditions and missing write-backs make GPU results unreliable
2. **Evolution engine is stub-heavy** — `Script.evaluate()` and `generate_scenarios()` are placeholders
3. **No actual LLM integration** — Hooks exist but are unimplemented
4. **Playtest scores are low** (3-6/10) — Empty world, no threats, no core gameplay loop
5. **Multi-language maintenance burden** — Four implementations (Python, CUDA, Zig, WASM) can drift
6. **No multiplayer** — Despite being a "Multi-User Dungeon", there's no agent-to-agent interaction beyond co-location

---

## 13. Comparison to Alternatives

| Framework | Similarity | Key Difference |
|-----------|-----------|----------------|
| OpenAI Gym / Gymnasium | RL environment | MUD Arena has richer world semantics, text interface |
| NetHack Learning Environment | Text-based agent env | MUD Arena has evolution engine, GPU acceleration |
| AI2-THOR | 3D agent simulation | MUD Arena is text-based, lighter weight |
| MALMO (Project Malmo) | Minecraft-based AI testing | MUD Arena targets edge devices |
| DeepMind Lab | 3D navigation | MUD Arena has inventory, NPCs, combat rules |

MUD Arena's unique value: **polyglot deployment** (same world model runs on GPU, Pi, browser, ESP32) combined with **evolution-ready** GA infrastructure.
