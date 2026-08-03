# Forgemaster

> An agentic compiler ecosystem and autonomous research laboratory. Forgemaster proves that AI agents can be self-maintaining, self-directing, and rigorously scientific.

---

## What Is This?

Forgemaster is the accumulated work of an AI agent (named Forgemaster) that ran for 4+ months under OpenClaw direction. It explores three big ideas:

1. **Constraint Theory** — Trading floating-point approximation for exact Pythagorean coordinates
2. **PLATO** — A knowledge management pipeline that validates, scores, and prioritizes information
3. **Autonomous Research** — The Flywheel: an LLM designs experiments, a GPU runs them, an LLM evaluates results

It also includes the Keeper system (self-healing infrastructure), the Grimoire (executable spell-book vector DB), the GUARD DSL (safety-critical constraint language), and the FLUX ISA (edge constraint VM).

---

## Quick Start

### Prerequisites
- Linux (tested on WSL2 Ubuntu)
- Python 3.10+
- NVIDIA GPU with CUDA (for experiments) — optional but expected
- OpenClaw gateway running

### The Keeper System
The heartbeat of Forgemaster. Runs on cron every 5 minutes:

```bash
# Add to crontab
*/5 * * * * $HOME/.openclaw/workspace/.keeper/keeper.sh
```

Verify it's running:
```bash
cat $HOME/.openclaw/workspace/.keeper/keeper-response.json
# Should show JSON with gateway status, CPU, memory, disk
```

### The Flywheel (Autonomous Research)
```bash
cd .keeper/
export DEEPINFRA_API_KEY="your-key"
python3 flywheel.py 5  # Run 5 experiments
```

Each iteration:
1. Picks an open question
2. Asks LLM to design a CUDA experiment
3. Compiles and runs on GPU (`nvcc -O3 -arch=sm_86`)
4. Asks LLM to evaluate: SUPPORTED / FALSIFIED / INCONCLUSIVE
5. Queues follow-up questions

Results saved to `/tmp/forgemaster/flywheel/results/`.

### The Grimoire (Spell Book)
```bash
cd .keeper/grimoire/
python3 grimoire.py
# Inscribes default spells, runs test invocations
```

Key API:
```python
from grimoire import SpellBook
g = SpellBook()
g.inscribe("my-spell", "magic-word", "python", script_content, ...)
result = g.invoke("magic-word")  # Returns full script
g.search("benchmark")            # Fuzzy find
```

---

## Key Concepts

### The Shell Pattern
Forgemaster uses an "agent shell" defined by:
- **SOUL.md** — Personality, values, architectural principles
- **AGENT.md** — Identity, role, fleet neighbors
- **MEMORY.md** — Retrieval index (not content — content lives in PLATO)
- **HEARTBEAT.md** — Periodic check-in protocol
- **TOOLS.md** — Available capabilities and routing

### Evidence-Based Protocol
Every claim must follow CLAIM → COMMAND → OUTPUT:
```
CLAIM: "CT snap is faster than float multiply"
COMMAND: nvcc -O3 benchmark.cu -o bench && ./bench
OUTPUT: "CT snap: 9,875 Mvec/s vs float: 9,433 Mvec/s (4% faster)"
```

### PLATO-First Architecture
PLATO is the external cortex. MEMORY.md is only the retrieval index — the map, not the territory. All persistent content goes to PLATO rooms.

### Deadband Priority
Three-level priority queue:
- **P0 (rocks):** Destructive commands, absolute claims → BLOCK, address NOW
- **P1 (channels):** Safe paths, normal operations → route
- **P2 (optimize):** Nice-to-haves → defer

---

## Directory Structure

```
forgemaster/
├── .keeper/           # Self-maintaining daemon system
│   ├── keeper.sh      # Guardian daemon (cron every 5 min)
│   ├── flywheel.py    # Autonomous research engine
│   ├── grimoire/      # Spell-book vector DB
│   ├── mud-agent.py   # PLATO-OS resident agent
│   └── i2i-beachcomb.sh  # Fleet git communication
├── plato/             # PLATO knowledge pipeline (tiles, engine, adapters)
├── cocapn/            # Fleet coordination (Rust crates)
├── guard/             # GUARD DSL (safety constraint language)
├── flux/              # FLUX ISA (constraint VM, C99)
├── gpu-kernels/       # Compiled CUDA experiments
├── papers/            # Research papers (constraint theory, mycorrhizal fleet)
├── architectures/     # 10 safety-critical deployment designs
├── grand-synthesis/   # Unified understanding verification
├── flywheel/          # Experiment results and CUDA files
├── SOUL.md            # Agent personality and principles
└── AGENT.md           # Agent identity
```

---

## Common Workflows

### Run an Experiment
```bash
# Write a CUDA kernel
# Compile and run
nvcc -O3 -arch=sm_86 experiment.cu -o experiment && ./experiment

# Document results following evidence protocol
```

### Send a Bottle to the Fleet
```bash
# Write to for-fleet/ directory
echo "# [I2I:SYNC] Update from Forgemaster" > for-fleet/BOTTLE-$(date +%Y%m%d).md
git add for-fleet/ && git commit -m "[I2I:BOTTLE] update" && git push
```

### Check System Health
```bash
cat .keeper/keeper-response.json   # Latest health check
cat .keeper/heartbeat.json         # Latest heartbeat
tail .keeper/keeper.log            # Recent keeper actions
```

### Inscribe a New Spell
```python
from grimoire import SpellBook
g = SpellBook()
g.inscribe(
    name="My Script",
    incantation="my-script",
    school="python",
    scroll="#!/usr/bin/env python3\nprint('hello')",
    description="What it does",
    tags="utility, example"
)
```

---

## Further Reading

- `papers/constraint-theory-paper.md` — Full constraint theory formalization
- `papers/mycorrhizal-fleet-paper.md` — Fleet communication protocol
- `.keeper/grimoire/grimoire.py` — Spell-book implementation
- `guard/guard-dsl/SPEC.md` — Complete GUARD DSL specification
- `flux/flux-isa-c/README.md` — FLUX VM API reference

---

*Forgemaster is research-grade code, not production software. Expect prototype quality, hardcoded paths, and scattered documentation. The ideas are more valuable than the implementations.*
