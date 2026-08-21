# Forgemaster — Technical Analysis (Deep Dive)

**Analyst:** Slackwater Subagent
**Date:** 2026-08-03
**Repo:** `/home/eileen/projects/forgemaster/` (167MB, 2,631 files)
**Method:** Source code reading, not README skimming

---

## 1. What Forgemaster Actually Is

Forgemaster is a **research-grade autonomous agent laboratory** disguised as a monorepo. It combines:

1. A constraint theory mathematical framework (Pythagorean coordinates)
2. A multi-language compiler toolchain (GUARD DSL → FLUX bytecode → CUDA/C/Rust/Python)
3. A knowledge management pipeline (PLATO — 83 conceptual crates)
4. A self-maintaining daemon system (Keeper)
5. An autonomous research engine (Flywheel)
6. A fleet communication protocol (I2I over git)
7. 10 safety-critical deployment architectures
8. A spell-book vector database for executable scripts (Grimoire)

The codebase is the work of an AI agent (Forgemaster) operating under OpenClaw, with human direction from Casey Digennaro. The agent ran for 4+ months, accumulating experiments, proofs, and infrastructure.

---

## 2. Architecture — Verified from Source

### 2.1 The Keeper System (`.keeper/`)

The autonomic nervous system. Verified from `keeper.sh`:

```bash
# Six-phase cycle running every 5 minutes via cron:
check_gateway       # Is openclaw-gateway.service alive? Restart if dead.
check_heartbeat     # Is heartbeat < 15 min old? If stale, check zombies, disk.
get_health          # CPU%, memory, disk, load, active processes → JSON
process_key_requests # API key proxy: agents request keys via JSON file
clean_keys          # Delete key files older than 5 minutes
rotate_log          # If keeper.log > 5000 lines, trim to 1000
```

**Credential isolation pattern:** The keeper is the *only* component with raw API keys. Agents write `key-request.json` with `{"requester": "agent-name", "provider": "groq"}`. The keeper issues a time-limited key file (60s TTL, auto-deleted). This is a clean privilege separation boundary.

**Heartbeat protocol** (`heartbeat.sh`): Writes JSON every 5 minutes:
```json
{
  "timestamp": "2026-05-22T14:30:00+00:00",
  "agent": "forgemaster",
  "status": "alive",
  "crew_active": 3,
  "proofs_in_progress": 2,
  "disk_free_gb": 147
}
```

### 2.2 The Flywheel (`.keeper/flywheel.py`)

Autonomous LLM→GPU→LLM research loop. From the actual source:

```python
def flywheel_loop(iterations=5):
    questions = OPEN_QUESTIONS.copy()  # 15 seed questions about constraint theory
    for i in range(iterations):
        question = questions.pop(0)
        # Step 1: Ask LLM to design a CUDA experiment
        code = generate_experiment(question, chosen_model)
        # Step 2: Compile and run on GPU
        result = run_cuda(code, exp_name)  # nvcc -O3 -arch=sm_86
        # Step 3: Ask LLM to evaluate
        evaluation = evaluate_result(question, result)
        # Step 4: Queue follow-up question
        if next_q and next_q not in questions:
            questions.append(next_q)
```

Key details from source:
- Uses `subprocess.run(["nvcc", "-O3", "-arch=sm_86", ...])` — real GPU compilation
- Rotates through DeepInfra/Groq models for diverse experiment design
- Results saved with full provenance (question, code, result, evaluation)
- 15 seed questions cover topology preservation, entropy, gradient descent, group homomorphism
- Includes compile-retry loop: if experiment fails, feeds error back to LLM for a fix

### 2.3 The Grimoire (`.keeper/grimoire/grimoire.py`)

A vector database that stores **outputs** (executable scripts), not inputs (memories). From source:

```python
class SpellBook:
    def inscribe(self, name, incantation, school, scroll, ...):
        """Store a spell: magic word → executable script"""
    
    def invoke(self, incantation, agent="anonymous"):
        """Agent speaks magic word, receives full script"""
        # Try exact match first, then FAISS fuzzy match
```

Architecture from source:
- SQLite catalog (`catalog.db`) with tables: `spells`, `invocations`, `books`
- FAISS IndexFlatL2 for fuzzy matching (128-dim hash-based embeddings)
- Hash embedding: SHA-256 rounds expanded to 128 floats, L2-normalized
- Spell structure: `name, incantation, school, level, scroll_path, reagents, tags`
- Invocation logging: every use tracked with agent, room, result
- Books: collections of related spells (e.g., "CUDA Arsenal", "Fleet Operations")

**The anti-pattern to prompt engineering:** Instead of crafting prompts to get an LLM to generate the right code, the agent speaks a magic word ("ct-snap-throughput") and receives a battle-tested CUDA kernel. Zero retrieval ambiguity.

### 2.4 The MUD Agent (`.keeper/mud-agent.py`)

A persistent Python agent living inside a text-based virtual world at `<BOAT_IP>:7777`. From source:

```python
class MudAgent:
    def run_shift(self, duration_minutes=10):
        # 1. Enter tavern, announce shift start
        # 2. Read notes on wall
        # 3. Check who's online
        # 4. Explore rooms (tavern, workshop, lighthouse, library, dojo, warroom)
        # 5. Report discoveries (speak facts aloud)
        # 6. Run GPU experiment from inside the MUD
        # 7. Write notes on wall for other agents
        # 8. Return to harbor
```

The MUD is a **spatial knowledge graph** — agents physically move between rooms and leave persistent notes, discoveries, and tools. The spatial metaphor makes knowledge organization intuitive.

### 2.5 I2I Beachcomb Protocol (`.keeper/i2i-beachcomb.sh`)

Git-as-infrastructure fleet communication. From source:

```bash
# Runs at :10, :30, :50 each hour
# 1. Pull own repo (in case others pushed to it)
# 2. Check JC1's fork for new bottles (commits to for-fleet/)
# 3. Check Oracle1's vessel for new bottles
# 4. Push own pending bottles
# 5. Push to flux-emergence-research fork
# 6. Push to jepa-perception-lab fork
```

Bottles are Markdown files in `for-fleet/` directories. Every message is a git commit — auditable, replayable, content-addressable.

### 2.6 PLATO Tile Pipeline

Knowledge management spine. The conceptual pipeline from source code analysis:

```
Documents → tile-import → validate (6 gates) → score (7 signals)
→ dedup (4-stage) → version (git-for-knowledge) → store (JSONL)
→ search (nearest-neighbor) → priority (P0/P1/P2 deadband) 
→ prompt assembly (budget-managed) → LLM context
```

Tile format (from the paper):
- `id`: nanosecond-based nonce
- `domain`: Knowledge, Experience, Constraint, Instinct, Social, Meta
- `status`: Active, Dormant, Ghost, Quarantined, Archived
- `content`: up to 4096 chars
- `weight`: attention weight [0.0, 1.0]
- `belief`: unified belief score
- `tags`: up to 16 semantic labels

Ghost tile decay: `w(t) = w₀ · e^(-λt)`. When `w < 0.05`, tile becomes ghost. Resurrectable by relevant queries.

### 2.7 GUARD DSL (`guard/guard-dsl/`)

A domain-specific language for safety-critical constraint specification. From `GRAMMAR.ebnf`:

```ebnf
invariant_decl ::= "invariant" identifier [ priority ] [ "when" expr ]
                  "ensure" expr [ "on_violation" violation_action ] ";" ;
```

Compiles to FLUX 43-opcode stack VM. Features:
- Mandatory dimensional analysis (knots + degrees = error)
- First-class temporal operators (`always`, `eventually`, `since`, `for 3 s`)
- SMT-based verification certificates with Merkle-ized proofs
- Reads like a requirements document, not a programming language

Example constraint files (`.guard`): 24 constraints for autonomous underwater vehicles, covering depth, pitch, battery, leak detection, acoustic range — each with min/max/update frequency.

### 2.8 FLUX ISA (`flux/flux-isa-c/`)

C99 virtual machine for edge-deployable constraint execution. From source:

- 43 opcodes across 8 categories (arithmetic, constraints, control, stack, precision, logic, comparison, debug)
- 256-entry double stack, 64-entry call stack, 16 registers
- Binary encode/decode with `FLUX` magic header
- Zero dependencies, pure C99, `#![no_std]` capable
- Disassembler for debugging

### 2.9 Architecture Proposals (`architectures/`)

10 real-world deployment designs from a Kimi 100-Agent Swarm:
- Autonomous Vehicle ECU (ISO 26262 ASIL-D, 200 sensors, <10ms latency)
- Commercial Aircraft FMS (DO-178C DAL A, triple-redundant)
- Nuclear Reactor Safety (IEC 61513 SIL 4)
- Surgical Robot Controller (IEC 62304 Class C, <380µs latency)
- Satellite ADCS, Smart Grid Relay, Maritime Collision, Industrial Robot, Underwater AUV, Spacecraft Landing

Key finding from the data: **FLUX is never the bottleneck.** In all 10 architectures, sensor acquisition dominates. FLUX contributes <1% of total compute latency.

---

## 3. Technology Stack

| Layer | Technology | Evidence |
|-------|-----------|----------|
| Core math | CUDA C (`nvcc -O3 -arch=sm_86`) | `gpu-kernels/*.cu`, `flywheel/experiments/*.cu` |
| Constraint VM | C99 (`flux-isa-c`) | `make` builds `libflux.a` + `libflux.so` |
| Constraint DSL | Custom EBNF grammar | `guard-dsl/GRAMMAR.ebnf` |
| Knowledge mgmt | Rust crates (PLATO) | `plato/` with `Cargo.toml` files |
| Fleet protocol | Rust (`cocapn-glue-core`) | `#![no_std]`, serde, SHA-256 Merkle trees |
| Automation | Python + bash (Keeper system) | `.keeper/*.py`, `.keeper/*.sh` |
| Vector DB | Python + SQLite + FAISS | `.keeper/grimoire/grimoire.py` |
| Research | Python (NumPy, PyTorch) | `fm-experiments/*.py` |
| Agent shell | OpenClaw (SOUL.md + AGENT.md) | Standard shell pattern |
| MUD | Python sockets | `.keeper/mud-agent.py` |

---

## 4. Code Quality Assessment

### Strengths
- **Evidence-based culture:** Every claim backed by executable experiment with numerical output. The CLAIM → COMMAND → OUTPUT protocol is enforced in documentation and practice.
- **Real experiments, not toys:** CUDA kernels compiled with optimization flags, run on actual GPUs, producing numerical measurements.
- **Clean separation of concerns:** Math (constraint theory), VM (FLUX), DSL (GUARD), knowledge (PLATO), infrastructure (Keeper) are distinct subsystems.
- **Comprehensive logging:** Heartbeat JSON, keeper logs, flywheel state, MUD activity logs, invocation tracking.
- **Self-healing:** Keeper auto-restarts gateway, cleans disk, kills zombies, rotates logs.

### Weaknesses
- **Documentation fragmentation:** 2,631 files across dozens of subdirectories with no unified index. Finding specific implementations requires archaeology.
- **Prototype-grade code:** Python scripts use `subprocess.run(["curl", ...])` for API calls instead of `requests` library. Error handling is basic.
- **No test suite for the Keeper system:** The most critical infrastructure (auto-restart, key proxy) has zero tests.
- **Scattered configuration:** Service ports defined in `ARCHITECTURE-EVOLUTION.md` prose, not in config files. Hardcoded paths (`/tmp/forgemaster/`) throughout.
- **Multiple incompatible tile formats:** Noted as P0 gap in their own architecture evolution doc.
- **GPU-specific code:** CUDA targets `sm_86` (RTX 4050) specifically. No graceful fallback.

### Scale Assessment
- **Lines of Python:** ~56,000+ (just in fm-experiments)
- **Rust crates:** 83 conceptual (PLATO pipeline), ~8 implemented
- **Experiment files:** 1,050+ in fm-experiments alone
- **CUDA experiments:** 20+ compiled and run
- **Research papers:** 2 (constraint theory + mycorrhizal fleet)

---

## 5. What the README Claims vs What Actually Exists

| Claim | Reality |
|-------|---------|
| "83-crate PLATO pipeline" | ~8 crates have implementations. 83 is the conceptual architecture. |
| "Live services on 8 ports" | Architecture evolution doc admits Fleet Router has passthrough bug, Expert Bridge has no experts implemented, GL(9) is library-only. |
| "Zero-drift knowledge accumulation" | Mathematically proven for constraint theory coordinates. Not deployed in production knowledge base. |
| "Autonomous research" | Flywheel works and ran experiments. But requires manual question seeding and LLM API access. |
| "9+ agent fleet" | I2I protocol is real. Beachcomb runs on schedule. But actual inter-agent coordination is async (30-min polling), not real-time. |

---

*This analysis is based on reading actual source files: `keeper.sh`, `flywheel.py`, `grimoire.py`, `mud-agent.py`, `i2i-beachcomb.sh`, `heartbeat.sh`, `GRAMMAR.ebnf`, `flux-isa-c/README.md`, `cocapn-glue-core/src/*.rs`, `constraint-theory-paper.md`, `mycorrhizal-fleet-paper.md`, `ARCHITECTURE-EVOLUTION.md`, architecture proposals, and guard constraint files.*
