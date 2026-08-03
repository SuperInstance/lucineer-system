# LEARN.md — MUD Arena Educational Guide

> Learn the concepts behind agent simulation arenas, evolutionary algorithms, and MUD-based AI research.

---

## Table of Contents

1. [Why MUD Mechanics for AI?](#1-why-mud-mechanics-for-ai)
2. [The Perceive-Decide-Act Loop](#2-the-perceive-decide-act-loop)
3. [Spatial Representation: Graphs vs Grids](#3-spatial-representation-graphs-vs-grids)
4. [Command Parsing and Natural Language](#4-command-parsing-and-natural-language)
5. [Genetic Algorithms for Agent Evolution](#5-genetic-algorithms-for-agent-evolution)
6. [Exploration vs Exploitation (γ + η = C)](#6-exploration-vs-exploitation-γ--η--c)
7. [Simulation-to-Reality Calibration](#7-simulation-to-reality-calibration)
8. [GPU Parallelization of Agent Simulations](#8-gpu-parallelization-of-agent-simulations)
9. [The Boarding Model: Human-in-the-Loop](#9-the-boarding-model-human-in-the-loop)
10. [Distributed Cognitive Specialization](#10-distributed-cognitive-specialization)
11. [Exercises](#11-exercises)
12. [Further Reading](#12-further-reading)

---

## 1. Why MUD Mechanics for AI?

### The Problem

AI agent research needs environments that are:
- **Structured enough to measure** — discrete states, clear win/loss conditions
- **Rich enough to be interesting** — multiple action types, spatial reasoning, resource management
- **Reproducible** — same starting conditions → comparable results
- **Lightweight** — fast enough to run millions of episodes

### The MUD Solution

MUDs (Multi-User Dungeons) are the original text-based virtual worlds, dating to 1978. They provide:

| MUD Feature | AI Research Value |
|-------------|-------------------|
| Rooms with exits | Graph navigation problems |
| Items and inventory | Resource management decisions |
| NPCs | Interaction and dialogue systems |
| Combat system | Risk/reward tradeoffs |
| Hazards | Environmental reasoning |
| Text interface | Natural language I/O |

### Comparison to Alternatives

```
Complexity ←──────────────────────────────→
Simple                              Rich

GridWorld ──── NetHack ──── MUD Arena ──── AI2-THOR ──── Real Robots
  2D grid      Text env    Text+Graph    3D sim       Physical
  ↑ too simple              ↑ sweet spot                 ↑ too expensive
```

**Key insight:** MUD Arena occupies the "sweet spot" — more structured than GridWorld, richer than NetHack, far cheaper than 3D simulation, and deployable to edge hardware.

### Exercise 1.1: Compare Environments

Think of three AI tasks you'd want to test. For each, compare how GridWorld, MUD Arena, and a full 3D simulator would handle it. Which provides the best signal-to-noise ratio for your research question?

---

## 2. The Perceive-Decide-Act Loop

### Concept

Every autonomous agent follows some version of this loop:

```
        ┌──────────┐
        │  WORLD   │
        └────┬─────┘
             │
     ┌───────▼────────┐
     │  PERCEIVE      │ ← Gather sensory data
     │  (sensors)     │
     └───────┬────────┘
             │
     ┌───────▼────────┐
     │  DECIDE        │ ← Choose an action
     │  (brain/policy)│
     └───────┬────────┘
             │
     ┌───────▼────────┐
     │  ACT           │ ← Execute the action
     │  (motors)      │
     └───────┬────────┘
             │
        ┌────▼─────┐
        │  WORLD   │ ← State changes
        └──────────┘
```

### In MUD Arena

```python
# PERCEIVE: Build a snapshot of what the agent "sees"
perception = agent.perceive(graph)
# → {"room_id": "dock", "room_name": "Dock",
#    "description": "A weathered dock.",
#    "exits": {"north": "forest"},
#    "items": ["torch"],
#    "npcs": ["fisherman"],
#    "inventory": ["map", "compass"]}

# DECIDE: Choose what to do (the interesting part!)
command = agent.decide(perception)
# → Command(verb=Verb.TAKE, target="torch")

# ACT: Execute the decision, mutate the world
result = agent.act(command, graph, bus)
# → "You pick up torch."
```

### Why This Matters

The **DECIDE** step is where intelligence lives. Everything else is plumbing. MUD Arena's `DecisionFn` makes this explicit:

```python
DecisionFn = Callable[[Dict[str, Any]], Command]
```

The agent's entire "brain" is one function call. This means you can swap in:
- **Rule-based logic** (if enemy → attack, if item → take)
- **Search algorithms** (minimax, MCTS over possible futures)
- **Learned policies** (neural network trained via RL)
- **LLM reasoning** (ask GPT/Claude/DeepSeek what to do)
- **Hybrid approaches** (rules for common cases, LLM for novel situations)

### Exercise 2.1: Write a Decision Function

Write a `DecisionFn` that:
1. Picks up any items in the room
2. If no items, talks to any NPC present
3. If no NPC, takes an unexplored exit
4. If all exits explored, goes back the way it came

**Hint:** You'll need to track visited rooms. Consider using a closure or a class.

---

## 3. Spatial Representation: Graphs vs Grids

### Grid Worlds (Traditional)

```
┌─────┬─────┬─────┐
│ 0,0 │ 1,0 │ 2,0 │
├─────┼─────┼─────┤
│ 0,1 │ 1,1 │ 2,1 │
├─────┼─────┼─────┤
│ 0,2 │ 1,2 │ 2,2 │
└─────┴─────┴─────┘
```

- Each cell connects to 4 (or 8) neighbors
- Movement is uniform: `move(north)` always means `y-1`
- Topology is always a regular lattice
- **Problem:** Real spaces aren't grids. A door might lead to a distant room.

### Graph Worlds (MUD Arena)

```
    [forest] ──east──→ [river]
       │                    │
    north                 south
       │                    │
    [dock] ──up──→ [bridge] │
       │                    │
    south                 west
       │                    │
    [beach] ←──────────────┘
```

- Each room connects to arbitrary other rooms via labeled exits
- Movement is semantic: `go through door` might teleport you across the map
- Topology is a **directed graph** — not all connections are bidirectional
- **Advantage:** Can model buildings, dungeons, cities, abstract spaces

### Implementation

MUD Arena uses a simple adjacency dictionary:

```python
room.exits = {"north": "forest", "east": "river"}
graph.navigate("dock", "north")  # → "forest"
```

This is O(1) lookup — the agent doesn't need to scan all rooms.

### Why Graphs Matter for AI

1. **Non-uniform connectivity** — Some paths are shortcuts; agents must discover them
2. **Asymmetric movement** — You can fall down a pit but not climb back up
3. **Semantic exits** — "enter portal" vs "go north" carry different meaning
4. **Variable room sizes** — A "room" can be a forest clearing or a closet

### Exercise 3.1: Build a Non-Trivial Map

Build a RoomGraph with at least 8 rooms where:
- There's a shortcut that bypasses 3 rooms
- There's a one-way exit (can go through but not back)
- The shortest path between two specific rooms changes if you find the shortcut

---

## 4. Command Parsing and Natural Language

### The Challenge

Human and LLM input is unstructured: `"pick up the rusty key and then go through the door"`

MUD commands need structure: `Command(verb=TAKE, target="rusty key")` then `Command(verb=GO, target="door")`

### MUD Arena's Parser

The parser handles:
1. **Single-word commands:** `look`, `inventory`, `help`
2. **Two-word commands:** `go north`, `take key`, `drop sword`
3. **Three-word commands:** `use key with door`, `talk to guard`
4. **Direction shorthand:** `north` → `go north`
5. **Multi-token targets:** `examine crystal_ball` (target = "crystal_ball")

### The Parsing Pipeline

```
Input: "pick up the glowing crystal"
  ↓
Tokenize: ["pick", "up", "the", "glowing", "crystal"]
  ↓
Identify verb: "pick" → TAKE (alias)
  ↓
Strip "up" (part of "pick up")
  ↓
Remaining: ["the", "glowing", "crystal"]
  ↓
Join: "the glowing crystal"
  ↓
Output: Command(verb=TAKE, target="the glowing crystal")
```

### Exercise 4.1: Extend the Parser

Add support for compound commands:
- `"take key and go north"` → two commands
- `"take all"` → take every item in the room
- `"go n e s w"` → move in a path

What are the edge cases? How would you handle ambiguity?

---

## 5. Genetic Algorithms for Agent Evolution

### Concept

A genetic algorithm (GA) mimics natural selection to evolve solutions:

```
Random Population → Evaluate → Select Best → Breed → Mutate → New Population
                                                                        ↑
                                                            Repeat for G generations
```

### In MUD Arena

Each "organism" is an **agent script** — a list of rules:

```
Rule 1: WHEN hp < 30% THEN use_item health_potion
Rule 2: WHEN enemy_in_room THEN attack weakest
Rule 3: DEFAULT move random_exit
```

**Fitness** = how well the script performs across many scenarios (survival time, gold collected, enemies defeated).

### Key Operations

#### Tournament Selection
Randomly pick K scripts, keep the best one. Repeat until you have the desired number of elites.

```
Pick 5 random scripts → keep highest fitness → that's one elite
Pick 5 more → keep best → second elite
...
```

Why not just keep the top N? Because tournament selection maintains diversity — a mediocre script might win a weak tournament.

#### Crossover (Single-Point)
```
Parent A: [Rule1, Rule2, | Rule3, Rule4]
Parent B: [RuleA, RuleB, | RuleC, RuleD]
                       ↑ cut point
Child:    [Rule1, Rule2,   RuleC, RuleD]
```

Combines strategies from two successful parents.

#### Mutation
Each rule has a probability `μ` of being randomly changed:
- Change condition type or parameter
- Change action type or parameter
- Add a new rule
- Delete a rule

### Parameters That Matter

| Parameter | Too Low | Too High | Sweet Spot |
|-----------|---------|----------|------------|
| Population size | Low diversity | Slow generations | 100-500 |
| Mutation rate | Stagnation | Random walk | 0.01-0.15 |
| Elite size | Best scripts lost | No new blood | 5-20% of population |
| Tournament size | Nearly random | Always picks the best | 3-7 |

### Exercise 5.1: Tune the GA

Run evolution with different parameter combinations:

| Run | Mutation | Tournament | Population |
|-----|----------|------------|------------|
| 1 | 0.01 | 3 | 100 |
| 2 | 0.10 | 5 | 200 |
| 3 | 0.50 | 7 | 100 |

Plot the best-fitness curve for each. What do you observe?

---

## 6. Exploration vs Exploitation (γ + η = C)

### The Fundamental Tradeoff

Every agent faces a choice:
- **Explore** — gather information (look around, search rooms, test items)
- **Exploit** — use known strategies (attack, collect, complete objectives)

Explore too much → never accomplish anything.
Exploit too much → miss better strategies.

### MUD Arena's Formulation

The repo frames this as:

```
γ (exploratory actions) + η (exploitative actions) = C (total actions)
```

The ratio γ/C is the **exploration rate**.

| Verb | Classification | Rationale |
|------|---------------|-----------|
| GO | γ (exploratory) | Moving to new areas, low risk |
| LOOK | γ | Information gathering, zero risk |
| EXAMINE | γ | Detailed inspection, zero risk |
| TAKE | γ→η | Resources, but also commitment |
| USE | η (exploitative) | Consuming resources for effect |
| DROP | η | Committing to item strategy |
| TALK | γ→η | Depends on context |

### Why This Matters

In reinforcement learning, the exploration-exploitation dilemma is typically framed mathematically (ε-greedy, UCB, Thompson sampling). MUD Arena makes it **tangible** — you can literally count how many times an agent chose `LOOK` vs `ATTACK`.

### Exercise 6.1: Measure Your Agent

Add instrumentation to track γ and η for any DecisionFn:

```python
exploratory_verbs = {Verb.GO, Verb.LOOK, Verb.EXAMINE}
exploitative_verbs = {Verb.USE, Verb.DROP}

gamma = sum(1 for c in command_history if c.verb in exploratory_verbs)
eta = sum(1 for c in command_history if c.verb in exploitative_verbs)
ratio = gamma / (gamma + eta) if (gamma + eta) > 0 else 0
print(f"Exploration rate: {ratio:.2%}")
```

What's the optimal ratio for your test scenarios?

---

## 7. Simulation-to-Reality Calibration

### The Problem

You evolve scripts in simulation. You deploy agents to the real world. **The simulation is always wrong.**

- Temperature affects sensor readings
- Wind affects drone movement
- Battery chemistry is non-linear
- Environmental features weren't modeled

### MUD Arena's Solution: Tolerance Tracking

The `tolerance.py` module tracks the gap:

```python
tracker.record("soil_moisture", predicted=0.35, actual=0.42, unit="ratio")
# → error_pct = 20.0%

tracker.calibrate("soil_moisture")
# → 1.20 (multiply predictions by 1.2 to match reality)
```

### The Calibration Loop

```
1. Run simulation → predicted values
2. Deploy to real hardware → actual values
3. Record divergence in ToleranceTracker
4. Apply correction factor to simulation parameters
5. Re-evolve scripts with corrected simulation
6. Deploy again → measure new divergence
7. Repeat until tolerance < threshold
```

This is the **human-as-calibration-instrument** concept from the Boarding Manifesto. The human boards the device, measures reality, and the system self-corrects.

### Exercise 7.1: Design a Calibration Experiment

Pick a physical quantity (temperature, distance, battery voltage). Design:
1. How the simulation predicts it
2. How the real device measures it
3. What correction factor to apply
4. When to flag "drift" (error trending upward over time)

---

## 8. GPU Parallelization of Agent Simulations

### The Insight

If you have 10,000 agents across 256 rooms, you can simulate them **in parallel** on a GPU:

```
Each CUDA block = one room
Each CUDA thread = one agent in that room
Shared memory = room state (visible to all agents in that room)
Global memory = all agents, scripts, and results
```

### Why Rooms Map Well to Blocks

1. **Spatial locality** — Agents in the same room interact; they need shared state
2. **Shared memory** — CUDA shared memory is visible to all threads in a block
3. **Synchronization** — `__syncthreads()` barriers within a block
4. **Independence** — Rooms can be simulated mostly independently

### The Catch: Race Conditions

Multiple agents in the same room might try to:
- Pick up the same item simultaneously
- Attack the same enemy
- Modify room state

Without proper synchronization (atomics, locks), the simulation produces incorrect results.

This is exactly the **CRITICAL** issue identified in the 12-model audit.

### Performance vs Correctness

```
CPU (correct):  1,024 agents × 100 turns = ~10 seconds
GPU (fast but buggy): 1,024 agents × 100 turns = ~50ms  (100x speedup)
GPU (correct with atomics): ~200ms (50x speedup, still big)
```

The speedup is significant enough to justify fixing the race conditions.

### Exercise 8.1: Think About Parallelization

If you have 64 rooms with an average of 8 agents each:
- How many CUDA blocks do you launch?
- How many threads per block?
- What goes in shared memory vs global memory?
- Where do you need `__syncthreads()`?

---

## 9. The Boarding Model: Human-in-the-Loop

### Concept

Traditional HCI: human controls, machine executes.
MUD Arena's model: **machine persists, human visits.**

```
Traditional:  Human ──controls──→ Machine
Boarding:     Human ──visits──→ Machine ──runs autonomously──→ Human ──returns──→ Machine ──reports──→ Human
```

### The Three Phases

1. **Board:** Human connects (SSH, WebSocket, Telnet). They see what agents see.
2. **Brief:** Human gives mission instructions. Agents update their task parameters.
3. **Beam off:** Human disconnects. Communication resolution drops. Agents go autonomous.

### Why This Is Novel

Most agent frameworks assume:
- The human is always present (chat interfaces)
- The human directly controls each action (teleoperation)
- The agent has no autonomy (API calls)

The boarding model assumes:
- The human is **intermittently present** (field researcher visiting a sensor)
- The human provides **high-level guidance** (mission briefings, not step-by-step)
- The agent has **full autonomy** between visits (runs on compiled scripts)

This models real-world scenarios: drone surveys, environmental monitoring, agricultural robotics.

### Communication Resolution

A key mechanic: as the human moves away from the device, **communication quality drops**:

```
Distance from dock: 0 rooms → 100% comm
Distance: 5 rooms   → 50% comm
Distance: 10+ rooms → 0% comm (agent is fully autonomous)
```

This forces agents to make decisions without human input — exactly the scenario for evolved scripts.

### Exercise 9.1: Design a Mission

Design a mission briefing for an agent on a forest survey drone:
1. What's the objective? (data collection, photography, mapping)
2. What constraints? (battery limit, comm range, weather)
3. What should the agent do if comm is lost?
4. When should the agent return?

Write it as a MUD `brief` command.

---

## 10. Distributed Cognitive Specialization

### The Big Question

When you have thousands of agents, do they naturally **specialize** into different roles?

In biology: ant colonies have workers, soldiers, queens. Brains have neurons, glia, stem cells.

In AI: can we observe emergent specialization in agent swarms?

### The DCS Laws (from MUD Arena's Research)

The `NEW-MODEL-IDEATION.md` documents findings and proposals:

| Law | Finding |
|-----|---------|
| Homogeneity | Uniform agents coordinate better than mixed populations |
| Sensor ROI | Investment in sensing pays off above a threshold |
| Heterogeneity cost | Mixing agent types destroys coordination |
| Scale peak | Coordination breaks down above ~4096 agents |
| Warmup period | Systems need time to stabilize before measuring |

### The Next Frontier: Self-Evolving Agents

17 frontier models proposed experiments where agents **rewrite their own rules** across generations:

- **Optimal mutation rate** — Too high → chaos; too low → stagnation. Sweet spot: 0.01-1.5%
- **Modular vs monolithic rules** — Modular edits (only change sensor rules, not coordination rules) preserve stability
- **Warmup escape** — If agents can adjust their own warmup period, the 4096 limit might vanish
- **Memory-bounded evolution** — Keeping too much history causes information overload

### Why This Matters

Understanding DCS enables:
- **Drone swarms** that self-organize for crop monitoring
- **IoT networks** that adapt communication protocols dynamically
- **DAOs** that evolve governance rules based on performance
- **Search and rescue** robots that specialize into scouts, medics, communicators

### Exercise 10.1: Design a DCS Experiment

Hypothesize: if agents can adjust their own exploration rate (γ) based on local success, will the swarm find a better global γ than any fixed value?

Design the experiment:
1. What's the independent variable?
2. What's the dependent variable?
3. What controls do you need?
4. What would falsify your hypothesis?

---

## 11. Exercises

### Beginner

1. **Hello MUD** — Build a 3-room world, create an agent, and have it walk through all rooms using `step()`.

2. **Item Collector** — Write a `DecisionFn` that collects every item in every room. How many turns does it take?

3. **Event Logger** — Subscribe to all event types and print a formatted log. Can you reconstruct the agent's journey from events alone?

### Intermediate

4. **Combat Arena** — Add a health system to agents. Implement attack/defend commands. Run 1v1 agent duels.

5. **LLM Agent** — Connect any LLM API as a `DecisionFn`. Compare its performance to rule-based agents on the same scenarios.

6. **Scenario Generator** — Use the LLM scenario generator to create 5 thematically distinct worlds. Export them as JSON.

7. **Evolution Run** — Run 50 generations of evolution with verbose output. Plot the fitness curve. At what generation does improvement plateau?

### Advanced

8. **Multi-Agent Coordination** — Place 3 agents in the same world. Can they coordinate to split exploration tasks without communicating?

9. **Tolerance Calibration** — Run a simulation, then manually "corrupt" the results to simulate real-world divergence. Use the ToleranceTracker to detect and correct it.

10. **DSL Extension** — Add new condition types (e.g., `ally_in_room`, `low_gold`) and action types (e.g., `trade`, `cast_spell`) to the script compiler. Update mutation and crossover to handle them.

11. **Edge Deployment** — Cross-compile the Zig runtime for a Raspberry Pi. SSH in, brief an agent, beam off, wait, reconnect.

### Research-Level

12. **DCS Experiment** — Run the "Optimal Plasticity Balance" experiment from NEW-MODEL-IDEATION.md. Vary mutation rates from 0.001% to 5% and measure coordination stability.

13. **Sim-to-Real** — Deploy a MUD-evolved script to a real robot (even a simple one). Measure the sim-to-real gap using tolerance tracking.

14. **Scaling Study** — Measure how coordination quality changes with agent count (10, 100, 1000, 4096). Do you observe the predicted breakdown?

---

## 12. Further Reading

### Foundational Papers

1. **Bartle, R. (2003).** *Designing Virtual Worlds.* New Riders. — The original MUD design philosophy. Every room, exit, and item type traces back to concepts in this book.

2. **Sutton, R. S. & Barto, A. G. (2018).** *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. — The perceive-decide-act loop is the RL agent loop. The exploration-exploitation tradeoff (Chapter 2) is the γ/η classification.

3. **Holland, J. H. (1992).** *Adaptation in Natural and Artificial Systems.* MIT Press. — The genetic algorithm framework underlying the evolution engine.

4. **Schmidhuber, J. (2015).** "Deep learning in neural networks: An overview." *Neural Networks*, 61, 85–117. — Context for why GPU acceleration matters for agent evolution.

### Modern Agent Research

5. **OpenAI (2024).** "Emergent tool use from multi-agent autocurricula." — Why environments like MUD Arena matter for studying emergent behavior.

6. **Vinyals, O. et al. (2019).** "Grandmaster level in StarCraft II using multi-agent reinforcement learning." *Nature.* — Multi-agent environments at scale.

7. **Bernhardsson, E. (2023).** "The Bitter Lesson of Agent Simulation." — Why structured environments beat hand-crafted features.

### GPU Computing

8. **NVIDIA (2024).** *CUDA C++ Programming Guide.* — The thread/block/shared-memory model used by the CUDA kernel.

9. **Kirk, D. & Hwu, W. (2016).** *Programming Massively Parallel Processors.* — Why rooms map well to blocks and agents to threads.

### Evolutionary Computation

10. **Eiben, A. E. & Smith, J. E. (2015).** *Introduction to Evolutionary Computing* (2nd ed.). Springer. — Tournament selection, crossover, mutation — the full GA toolkit.

### MUD History

11. **Curtin, N. (1997).** "The History of MUDs." — Understanding the cultural origins of text adventures and why their mechanics endure.

---

*Built with the MUD Arena framework. Board the ship. Brief the crew. Beam off.*
