# MUD Arena

> A gym environment for AI agents using classic MUD (Multi-User Dungeon) mechanics.
> Agents navigate graph-structured rooms, manage inventories, parse adventure-game commands, and compete in evolutionary tournaments — with GPU acceleration, LLM-driven scenarios, and real-time WebSocket observation.

[![CI](https://github.com/SuperInstance/mud-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/SuperInstance/mud-engine/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Table of Contents

- [What Is MUD Arena?](#what-is-mud-arena)
- [Why It Matters](#why-it-matters)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Building Worlds](#building-worlds)
- [Creating Agents](#creating-agents)
- [Command Reference](#command-reference)
- [The Evolution Engine](#the-evolution-engine)
- [Scenario Generation](#scenario-generation)
- [Observation Server](#observation-server)
- [Script DSL](#script-dsl)
- [Tolerance Tracking](#tolerance-tracking)
- [Edge Runtime (Zig)](#edge-runtime-zig)
- [Browser Client (WASM)](#browser-client-wasm)
- [GPU Acceleration (CUDA)](#gpu-acceleration-cuda)
- [Dashboard Visualization](#dashboard-visualization)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## What Is MUD Arena?

MUD Arena is a **text-adventure world engine designed for AI agent research**. Instead of a generic grid or free-form chat, it provides:

- **Graph-structured rooms** connected by labeled exits
- **Items** with properties (usable, consumable, tagged)
- **NPCs** for interaction
- **MUD-standard commands** (go, look, take, drop, use, talk, examine)
- **An event system** for pub/sub world events
- **A genetic algorithm** for evolving agent decision scripts
- **GPU acceleration** via CUDA (one block = one room, one thread = one agent)

It is part of the **SuperInstance/OpenConstruct ecosystem** — a fleet of repos building spatial, agent-driven software for edge devices.

### The Boarding Model

MUD Arena's core UX paradigm:

1. **Board** — SSH into the device running the MUD
2. **Brief** — Give agents their mission objectives
3. **Beam off** — Disconnect; agents continue autonomously
4. **Return** — Agents come home with data/cargo when battery runs low or mission completes

> *"Board the ship. Brief the crew. Beam off. They come home with the catch."*

---

## Why It Matters

MUD Arena fills a gap in AI agent research:

| Compared To | Advantage |
|-------------|-----------|
| GridWorld | Richer topology (graphs, not grids), items, NPCs, combat |
| Free-form LLM chat | Discrete state, rule-based physics, measurable outcomes |
| 3D simulation | Lightweight, reproducible, runs on edge devices |
| NetHack Learning Env | Built-in evolution engine, GPU acceleration, multi-target deployment |

The arena serves as a testbed for:
- Agent generalization and adaptation
- Emergent cooperation in multi-agent scenarios
- Co-evolution of strategies and environments
- Simulation-to-reality calibration

---

## Installation

### Python Core (Recommended Starting Point)

```bash
git clone https://github.com/SuperInstance/mud-engine.git
cd mud-engine

# Core package (zero external dependencies!)
pip install -e .

# With server support
pip install -e ".[server]"

# With evolution engine
pip install -e ".[evolution]"

# With LLM scenario generation
pip install -e ".[llm]"

# Everything (dev included)
pip install -e ".[server,evolution,llm,viz,dev]"
```

### GPU Build (CUDA)

Requires `nvcc` (CUDA Toolkit 12.6+):

```bash
make gpu
# Or directly:
nvcc -O3 -arch=sm_87 -o mud-engine src/mud_arena.cu
```

### CPU Fallback

```bash
make cpu
# Or:
gcc -DCPU_ONLY -O3 -o mud-arena-cpu src/mud_arena.cu -lm -lpthread
```

### Zig Edge Runtime

Requires [Zig 0.13+](https://ziglang.org/):

```bash
# Dev machine
zig build -Doptimize=ReleaseSmall

# ARM64 (Jetson, Raspberry Pi)
zig build -Dtarget=aarch64-linux -Doptimize=ReleaseSmall

# WASM (browser)
zig build -Dtarget=wasm32-wasi
```

### WASM Browser Build

Requires [Emscripten](https://emscripten.org/):

```bash
emcc -O3 -s WASM=1 \
  -s EXPORTED_RUNTIME_METHODS='["ccall","cwrap"]' \
  -s EXPORTED_FUNCTIONS='["_mud_init","_mud_command","_mud_tick","_mud_get_output","_mud_human_enter","_mud_human_act","_mud_measure"]' \
  -o mud_arena.js src/wasm_mud.c
```

### Docker

```bash
docker build -t mud-engine .
docker run --gpus all -p 7778:7778 -p 7779:7779 -p 7780:7780 mud-engine
```

---

## Quick Start

### 30-Second Tutorial

```python
from mud_arena.rooms import Room, RoomGraph
from mud_arena.agent import Agent
from mud_arena.events import EventBus
from mud_arena.commands import parse_command

# Build a world
world = RoomGraph()
world.add_room(Room(id="dock", name="Dock", description="A weathered dock."))
world.add_room(Room(id="forest", name="Dark Forest", description="Tall trees surround you.",
                    items=["mushroom"], npcs=["old_logger"]))
world.connect("dock", "forest", "north", "south")

# Create an agent
hero = Agent(id="hero", current_room="dock")
bus = EventBus()

# Run a perceive-decide-act cycle
result = hero.step(world, bus, "go north")
print(result)  # "Tall trees surround you."

result = hero.step(world, bus, "take mushroom")
print(result)  # "You pick up mushroom."

result = hero.step(world, bus, "talk to old_logger")
print(result)  # "old_logger says: '...'"

# Check events
events = bus.history()
print(f"{len(events)} events emitted")
```

### Run the Evolution Engine

```bash
# Quick test (10 generations, 20 scripts)
python src/evolve.py --generations 10 --population 20 --scenarios 5 --verbose

# Full run
python src/evolve.py --generations 100 --population 200 --scenarios 20 --verbose --export population.pkl
```

### Start the Observation Server

```bash
python src/server.py
# WebSocket on :7779
# Telnet on    :7778
# HTTP API on  :7780
```

Connect from another terminal:

```bash
# Telnet
telnet localhost 7778
> look
> agents
> watch alpha

# HTTP
curl http://localhost:7780/status
curl http://localhost:7780/agents
```

---

## Core Concepts

### The Simulation Loop

```
For each tick:
  1. For each agent A:
     a. perceive(A) → {room_id, room_name, description, exits, items, npcs, inventory}
     b. decide(A, perception) → Command{verb, target}
     c. act(A, command) → mutate world state, emit Event
  2. Resolve combat, apply hazards, update scores
  3. Publish world snapshot to watchers
```

### The Spatial Model

Rooms are nodes in a **directed graph**. Each room has labeled exits pointing to other rooms:

```
[dock] --north--> [forest] --east--> [river]
   ^                                         |
   |______________ west _____________________|
```

### The DecisionFn Pattern

Every agent has a pluggable decision function. This is the **primary extension point**:

```python
from mud_arena.commands import parse_command

# Rule-based: always go north
def explorer(perception):
    exits = perception.get("exits", {})
    if "north" in exits:
        return parse_command("go north")
    return parse_command("look")

agent.set_decision_fn(explorer)

# LLM-based: ask a language model
def llm_agent(perception):
    prompt = f"You are in {perception['room_name']}. Exits: {perception['exits']}. Items: {perception['items']}. What do you do?"
    response = my_llm.generate(prompt)
    return parse_command(response)

agent.set_decision_fn(llm_agent)
```

### The γ + η = C Classification

Each agent action is either:
- **(γ) Exploratory** — navigating, searching, gathering (low-risk, information-gaining)
- **(η) Exploitative** — combat, consuming, completing goals (high-risk, rewarding)

The ratio γ/(γ+η) is the exploration-exploitation balance — a fundamental RL tradeoff made tangible through MUD verbs.

---

## Building Worlds

### Programmatic World Building

```python
from mud_arena.rooms import Room, RoomGraph

world = RoomGraph()

# Add rooms
world.add_room(Room(
    id="entrance",
    name="Cave Entrance",
    description="A dark opening in the cliff face.",
    exits={},
    items=["torch"],
    metadata={"lighting": "dim", "terrain": "rock"}
))

world.add_room(Room(
    id="tunnel",
    name="Narrow Tunnel",
    description="The tunnel twists and turns.",
    items=["gold_coin"],
    npcs=["bat"],
    metadata={"hazard": "low_ceiling"}
))

world.add_room(Room(
    id="treasure_room",
    name="Treasure Chamber",
    description="Golden light fills the room.",
    items=["ruby", "ancient_scroll"],
    metadata={"locked": True}
))

# Connect rooms (one-way or two-way)
world.connect("entrance", "tunnel", "north", "south")
world.connect("tunnel", "treasure_room", "east", "west")

# Navigate
print(world.navigate("entrance", "north"))  # "tunnel"
print(world.exits_for("entrance"))          # {"north": "tunnel"}
```

### LLM-Driven Scenario Generation

```python
from scenario_generator import ScenarioGenerator

gen = ScenarioGenerator(api_key="sk-...", model="gpt-4o-mini")

scenario = gen.generate_from_prompt(
    "A dark cavern with three treasure rooms guarded by dragons, "
    "a poisonous swamp, and a hidden exit."
)

print(f"{scenario.name}: {len(scenario.rooms)} rooms, difficulty {scenario.difficulty}")
```

### Adaptive Difficulty

```python
# Agents keep winning? Make it harder.
scenario = gen.generate_challenge(previous_results=[True, True, False, True])

# Agents keep losing? Make it easier.
scenario = gen.generate_challenge(previous_results=[False, False, True])
```

### Tournament Sets

```python
# 8 scenarios spanning difficulty 2-8
tournament = gen.generate_tournament(num_scenarios=8, difficulty_range=(2, 8))
for i, s in enumerate(tournament):
    print(f"Scenario {i+1}: difficulty {s.difficulty}, {len(s.rooms)} rooms")
```

---

## Creating Agents

### Basic Agent

```python
from mud_arena.agent import Agent
from mud_arena.inventory import Item

agent = Agent(
    id="ranger",
    name="Aragorn",
    current_room="entrance",
    inventory=Inventory(capacity=10)
)

agent.inventory.add(Item(name="sword", description="A sharp blade.", tags=["weapon"]))
agent.inventory.add(Item(name="potion", description="Heals 50 HP.", uses=3, tags=["consumable"]))
```

### Custom Decision Function

```python
from mud_arena.commands import Command, Verb

def strategic_agent(perception):
    """A simple rule-based decision function."""
    items = perception.get("items", [])
    exits = perception.get("exits", {})
    inventory = perception.get("inventory", [])

    # Priority 1: Pick up valuable items
    if items:
        return Command(verb=Verb.TAKE, target=items[0], raw=f"take {items[0]}")

    # Priority 2: Explore unvisited exits
    if "north" in exits:
        return Command(verb=Verb.GO, target="north", raw="go north")
    if "east" in exits:
        return Command(verb=Verb.GO, target="east", raw="go east")

    # Fallback: Look around
    return Command(verb=Verb.LOOK, raw="look")

agent.set_decision_fn(strategic_agent)
```

### Full Autonomous Step

```python
# Run the complete perceive → decide → act cycle automatically
result = agent.step(world, bus)
print(result)
```

---

## Command Reference

| Verb | Aliases | Syntax | Example | Effect |
|------|---------|--------|---------|--------|
| GO | move, walk, run, head | `go <direction>` | `go north` | Move to adjacent room |
| LOOK | l | `look` | `look` | Describe current room |
| EXAMINE | x, inspect | `examine <target>` | `examine crystal` | Detailed item/feature description |
| TAKE | get, pick up, grab | `take <item>` | `take key` | Pick up ground item |
| DROP | — | `drop <item>` | `drop torch` | Place item on ground |
| USE | — | `use <item> [with <target>]` | `use key with door` | Consume/use an item |
| TALK | — | `talk to <npc>` | `talk to guard` | Interact with NPC |
| INVENTORY | i, inv | `inventory` | `inventory` | List carried items |
| HELP | — | `help` | `help` | Show available commands |
| QUIT | exit, q | `quit` | `quit` | End session |

**Direction shorthand:** `north`, `south`, `east`, `west`, `n`, `s`, `e`, `w`, `up`, `down`, `in`, `out` are all valid as standalone commands (parsed as `GO <direction>`).

---

## The Evolution Engine

The genetic algorithm evolves **agent scripts** (rule lists) across generations:

```
Initialize → Evaluate → Select → Crossover → Mutate → Replace → Repeat
```

### Running Evolution

```bash
# Basic run
python src/evolve.py \
  --generations 100 \
  --population 200 \
  --scenarios 20 \
  --elite 20 \
  --mutation 0.1 \
  --tournament 5 \
  --verbose \
  --export best_population.pkl
```

### Importing a Saved Population

```bash
python src/evolve.py \
  --import population.pkl \
  --generations 50 \
  --verbose
```

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--generations` | 100 | Number of generations to evolve |
| `--population` | 200 | Scripts in the population |
| `--scenarios` | 20 | Scenarios evaluated per generation |
| `--elite` | 20 | Top scripts kept each generation |
| `--mutation` | 0.1 | Per-rule mutation probability |
| `--tournament` | 5 | Tournament selection size |
| `--adaptive` | off | Enable LLM-driven adaptive scenarios |
| `--no-gpu` | off | Force CPU execution |
| `--export` | — | Save final population to file |

### Statistics Tracked

- **Best/Avg/Worst fitness** per generation
- **Convergence slope** (linear regression on recent best fitness)
- **Diversity** (average pairwise Hamming distance between scripts)
- **LLM review hooks** (placeholder for strategy analysis)

---

## Scenario Generation

### Random Scenarios (No LLM Needed)

```python
from scenario_generator import ScenarioGenerator

gen = ScenarioGenerator()
scenario = gen.generate_random(num_rooms=12, difficulty=4)

for room in scenario.rooms:
    print(f"  {room.name} ({room.terrain}): {len(room.items)} items, {len(room.enemies)} enemies")
```

### LLM-Driven Scenarios

```python
gen = ScenarioGenerator(api_key="sk-...", model="deepseek-chat")

scenario = gen.generate_from_prompt(
    "An ancient library guarded by a sphinx. "
    "Players must answer riddles to proceed."
)
```

### Scenario Structure

```python
@dataclass
class Scenario:
    name: str
    description: str
    rooms: List[Room]          # Graph of interconnected rooms
    agents: List[AgentConfig]  # Starting agent configurations
    victory_condition: dict    # e.g. {"type": "collect_gold", "amount": 50}
    difficulty: int            # 1-10
```

Victory condition types:
- `survive_turns` — Live for N turns
- `collect_gold` — Gather N gold
- `reach_room` — Navigate to a specific room

---

## Observation Server

Three protocols for watching the simulation:

### WebSocket (Port 7779)

Connect from browser or `websockets` library:

```javascript
const ws = new WebSocket("ws://localhost:7779");
ws.onmessage = (e) => console.log(JSON.parse(e.data));

ws.send("look");
ws.send("agents");
ws.send("watch alpha");  // Live feed for agent "alpha"
```

Commands: `look`, `map`, `agents`, `scores`, `leaderboard`, `generation`, `scenarios`, `watch <agent_id>`

### Telnet (Port 7778)

```bash
telnet localhost 7778
> look
> agents
> watch alpha
```

### HTTP REST API (Port 7780)

| Endpoint | Method | Returns |
|----------|--------|---------|
| `/status` | GET | Server status + timestamp |
| `/agents` | GET | List of all agents with state |
| `/rooms` | GET | Room graph |
| `/scores` | GET | Script scores |
| `/generation` | GET | Current evolution generation stats |
| `/scenarios` | GET | Active scenarios |
| `/inject-scenario` | POST | Inject a custom scenario |

```bash
curl http://localhost:7780/agents | jq .
curl -X POST http://localhost:7780/inject-scenario \
  -H "Content-Type: application/json" \
  -d '{"id": "custom_1", "description": "Test scenario"}'
```

---

## Script DSL

Agent scripts are written in a domain-specific language:

```
"Treasure Hunter"
WHEN hp < 30% AND enemy_in_room THEN use_item health_potion
WHEN item_on_ground THEN pickup gold
WHEN gold_on_ground AND inventory_not_full THEN pickup gold
WHEN turns > 50 THEN return_base
DEFAULT move random_exit
```

### DSL → Binary

```python
from script_compiler import ScriptCompiler

# Parse DSL
script = ScriptCompiler.parse('"My Bot"\nWHEN enemy_in_room THEN attack weakest\nDEFAULT move north')

# Serialize for GPU upload
binary = ScriptCompiler.to_binary(script)

# Deserialize
restored = ScriptCompiler.from_binary(binary)

# Pretty-print
print(ScriptCompiler.to_dsl(script))
```

### Condition Types

| Condition | Example |
|-----------|---------|
| `hp < X%` | `WHEN hp < 30%` |
| `hp >= X%` | `WHEN hp >= 50%` |
| `enemy_in_room` | `WHEN enemy_in_room` |
| `item_on_ground` | `WHEN item_on_ground` |
| `gold_on_ground` | `WHEN gold_on_ground` |
| `inventory_not_full` | `WHEN inventory_not_full` |
| `turns > N` | `WHEN turns > 100` |

Multiple conditions joined with `AND`.

### Action Types

| Action | Example |
|--------|---------|
| `use_item <item>` | `use_item health_potion` |
| `flee <exit>` | `flee random_exit` |
| `pickup [gold]` | `pickup gold` |
| `attack <target>` | `attack weakest` |
| `move <direction>` | `move north` |

### Mutation and Crossover

```python
# Generate random script
random_script = ScriptCompiler.generate_random()

# Mutate at 10% rate
mutated = ScriptCompiler.mutate(script, rate=0.1)

# Breed two parents
child = ScriptCompiler.breed(parent_a, parent_b)
```

---

## Tolerance Tracking

Track divergence between simulation and reality:

```python
from tolerance import ToleranceTracker

tracker = ToleranceTracker()

# Record measurements
tracker.record("temperature", predicted=22.0, actual=24.5, unit="°C")
tracker.record("temperature", predicted=22.0, actual=25.1, unit="°C")
tracker.record("battery_life", predicted=8.0, actual=6.5, unit="hours")

# Check tolerance
print(tracker.get_tolerance("temperature"))  # Average error %
print(tracker.is_within_tolerance("temperature", threshold_pct=10.0))
print(tracker.detect_drift("temperature"))   # Is error trending up?

# Get correction factor
print(tracker.calibrate("battery_life"))     # e.g., 0.8125

# Full report
import json
print(json.dumps(tracker.report(), indent=2))

# Suggestions for out-of-tolerance variables
for s in tracker.suggest_adjustments():
    print(s)

# Persist
tracker.save("tolerance.json")
tracker.load("tolerance.json")
```

---

## Edge Runtime (Zig)

The Zig runtime provides a <100KB binary for edge devices:

```bash
# Build for Raspberry Pi / Jetson
zig build -Dtarget=aarch64-linux -Doptimize=ReleaseSmall

# Run
./zig-out/bin/mud-engine
```

### Terminal Interface

```
> look
Dock
You stand on the docking platform of the ship.
  north leads to room 1

> go north
you move.

> status
tick 42 | human present (room 1) | comm 80% | active agents 1

> agents
Agents:
  Scout (room 1) battery 99% state idle

> brief 0 Survey the north forest and return
mission uploaded

> quit
You disconnect. Agents continue on their own.
```

### Key Features

- **Battery simulation** — agents drain power over time, enter low-battery state
- **Communication resolution** — decays with distance from human
- **Agent briefing** — assign mission text that changes agent state to autonomous
- **Perception modes** — normal, calibration, agent_view, god
- **Background ticking** — world advances every 100ms

---

## Browser Client (WASM)

The WASM build runs the full MUD in a browser:

```bash
# Build
emcc -O3 -s WASM=1 \
  -s EXPORTED_RUNTIME_METHODS='["ccall","cwrap"]' \
  -s EXPORTED_FUNCTIONS='["_mud_init","_mud_command","_mud_tick","_mud_get_output"]' \
  -o mud_arena.js src/wasm_mud.c

# Serve
python -m http.server 8000
# Open http://localhost:8000/src/mud_arena.html
```

Features:
- Dark cyberpunk terminal UI
- Real-time agent list sidebar
- Calibration mode toggle
- Human boarding/beaming controls
- Battery and comm resolution status bar

---

## GPU Acceleration (CUDA)

### Architecture

```
Grid:   One block per room
Block:  Up to 32 threads (one per agent in room)
Shared: Room state in shared memory
Global: Agents, scripts, results
```

### Running GPU Simulation

```bash
# Jetson Orin / RTX GPU
./mud-engine --agents 1024 --rooms 256 --turns 100 --scenarios 20

# Output: Script rankings by average score
```

### Jetson Orin Experiment

```bash
# Hyper-compressed evolution experiment
nvcc -O3 -arch=sm_87 -o jc1 src/jc1_experiment_mud_arena.cu
./jc1
# 64 scripts, 128 rooms, 200 turns, 100 generations
```

### Known CUDA Issues

⚠️ **Race conditions in shared memory** — The `s_room` shared variable is read/written by multiple threads without full synchronization. Results may be unreliable until fixed.

⚠️ **No agent write-back** — Local agent state changes may not propagate back to global memory correctly.

**Workaround:** Use CPU fallback (`--no-gpu` or `make cpu`) for reliable results until the kernel is fixed.

---

## Dashboard Visualization

Generate an HTML dashboard from evolution history:

```bash
# After an evolution run, prepare history.json
python src/dashboard.py history.json -o dashboard.html

# Open in browser
xdg-open dashboard.html
```

The dashboard includes:
- **Fitness chart** — best/avg/worst per generation
- **Top-10 scripts** — DSL source + scores
- **Difficulty vs survival** — scatter plot
- **Strategy distribution** — pie chart
- **Evolution timeline** — breakthrough moments
- **Complexity trend** — script size over generations
- **LLM scenario log** — generated scenario prompts

### JSON Input Format

```json
{
  "fitness": [{"index": 0, "best": 95, "avg": 45, "worst": 5}],
  "top_scripts": [{"name": "S1", "dsl": "attack;move north", "score": 92.3}],
  "scenario_survival": [{"difficulty": 0.2, "survival_rate": 0.85}],
  "strategy_distribution": {"attack": 120, "flee": 45, "explore": 35},
  "breakthroughs": [{"generation": 12, "description": "first >90% win-rate"}],
  "complexity_trend": [{"generation": 0, "avg_complexity": 23.5}],
  "llm_scenarios": ["You are in a dark cave..."]
}
```

---

## API Reference

### `mud_arena.rooms`

| Symbol | Type | Description |
|--------|------|-------------|
| `Room` | dataclass | `id, name, description, exits, items, npcs, metadata` |
| `RoomGraph` | class | Directed graph of rooms; add/connect/navigate/remove |

### `mud_arena.agent`

| Symbol | Type | Description |
|--------|------|-------------|
| `Agent` | dataclass | `id, name, current_room, inventory, _decision_fn` |
| `DecisionFn` | type alias | `Callable[[Dict[str, Any]], Command]` |
| `Agent.perceive(graph)` | method | Build perception dict from current room |
| `Agent.decide(perception)` | method | Call decision function |
| `Agent.act(command, graph, bus)` | method | Execute command, mutate world |
| `Agent.step(graph, bus, cmd_text)` | method | Full perceive-decide-act cycle |

### `mud_arena.commands`

| Symbol | Type | Description |
|--------|------|-------------|
| `Verb` | Enum | GO, LOOK, EXAMINE, TAKE, DROP, USE, TALK, INVENTORY, HELP, QUIT, UNKNOWN |
| `Command` | frozen dataclass | `verb, target, indirect, raw` |
| `parse_command(text)` | function | Parse MUD command string → `Command` |

### `mud_arena.inventory`

| Symbol | Type | Description |
|--------|------|-------------|
| `Item` | dataclass | `name, description, usable, uses, tags` |
| `Inventory` | class | Capacity-limited container; add/remove/use/find_by_tag |

### `mud_arena.events`

| Symbol | Type | Description |
|--------|------|-------------|
| `EventType` | Enum | ROOM_ENTER/LEAVE, ITEM_PICKED_UP/DROPPED/USED, NPC_SPOKE, ROOM_EVENT, AGENT_ACTION, CUSTOM |
| `Event` | dataclass | `type, source, data, room` |
| `EventBus` | class | Pub/sub; subscribe/emit/history/clear |

---

## Troubleshooting

### Installation Issues

**Problem:** `pip install -e .` fails with missing packages
```
Solution: Ensure Python ≥3.10. Core package has zero dependencies.
For extras, install the specific optional group:
  pip install -e ".[server]"   # for websockets, aiohttp
  pip install -e ".[evolution]" # for numpy
```

**Problem:** CUDA build fails with `nvcc: command not found`
```
Solution: Install CUDA Toolkit 12.6+ and ensure nvcc is on PATH.
Or use CPU fallback: make cpu
```

**Problem:** Zig build fails
```
Solution: Install Zig 0.13+ from ziglang.org.
Verify: zig version
```

### Runtime Issues

**Problem:** Server won't start — "Address already in use"
```
Solution: Ports 7778/7779/7780 may be in use.
Edit src/server.py to change ports, or:
  lsof -i :7779
  kill <PID>
```

**Problem:** Telnet connection immediately closes
```
Solution: The telnet server uses raw TCP. Ensure you're connecting to port 7778
(not the WebSocket port 7779).
```

**Problem:** GPU simulation produces inconsistent results
```
Known issue: Race conditions in shared memory.
Workaround: Use CPU fallback until CUDA kernel is fixed.
  python src/evolve.py --no-gpu --verbose
```

### Evolution Issues

**Problem:** Evolution fitness doesn't improve
```
Possible causes:
1. Mutation rate too high (--mutation 0.5) → random walk
2. Mutation rate too low (--mutation 0.001) → stuck in local optimum
3. Population too small (--population 10) → insufficient diversity
4. Script.evaluate() is still a stub → implement real evaluation

Recommended starting params:
  --generations 100 --population 200 --scenarios 20 --mutation 0.1 --tournament 5
```

**Problem:** LLM scenario generation fails
```
Solution: Ensure OPENAI_API_KEY is set, or pass api_key directly.
The generator works with any OpenAI-compatible endpoint (DeepSeek, Azure, etc.).
For local models: set openai.base_url before calling.
```

### Zig Runtime Issues

**Problem:** `zig build` fails on cross-compile
```
Solution: Ensure target is installed:
  zig targets  # list available targets
For ARM64: zig build -Dtarget=aarch64-linux
```

---

## FAQ

**Q: Is MUD Arena a game?**
A: It's a **research framework** that uses game mechanics. The playtest reports show it's currently sparse as a game (3-6/10 ratings), but the infrastructure is designed for agent research, not entertainment.

**Q: Do I need a GPU?**
A: No. The Python core runs on any CPU. The evolution engine has CPU fallback. GPU acceleration is optional and currently has known bugs.

**Q: Can I plug in an LLM agent?**
A: Yes — set the agent's `DecisionFn` to a callable that passes perception to your LLM and parses the response. The architecture is designed for this.

**Q: What's the relationship to Roblox/Luau?**
A: None directly. MUD Arena is Python/CUDA/Zig/WASM. The "vessel" type in the CHARTER refers to the Cocapn Fleet ecosystem, not Roblox.

**Q: How does this connect to real-world robotics?**
A: The Zig runtime runs on edge devices (Pi, Jetson). Agents are briefed via MUD commands, then operate autonomously. The tolerance tracker calibrates simulation vs. reality. See the Boarding Manifesto for the full vision.

**Q: Why is it called "MUD Arena"?**
A: MUD = Multi-User Dungeon, the classic text-adventure format. "Arena" because agents compete in evolutionary tournaments within the MUD world.

**Q: What's DCS?**
A: Distributed Cognitive Specialization — the study of how agent swarms self-organize into specialized roles. MUD Arena is the experimental platform for DCS research (see NEW-MODEL-IDEATION.md for 17 model proposals).

**Q: Can multiple humans play simultaneously?**
A: The server supports multiple connections, but the world model is single-player focused. True multiplayer would require adding agent-to-agent interaction beyond co-location.

---

## License

MIT — See [LICENSE](LICENSE)

## Related

- [Charter](https://github.com/SuperInstance/mud-engine/blob/main/CHARTER.md) — Mission and vision
- [Boarding Manifesto](https://github.com/SuperInstance/mud-engine/blob/main/BOARDING-MANIFESTO.md) — UX philosophy
- [Contributing](https://github.com/SuperInstance/mud-engine/blob/main/CONTRIBUTING.md) — Development guide
- [Audit Report](https://github.com/SuperInstance/mud-engine/blob/main/AUDIT-REPORT.md) — 12-model CUDA kernel audit
