# Forgemaster — Integration with Slackwater

**Date:** 2026-08-03
**Reference:** `/home/eileen/projects/lucineer-system/INTEGRATED_ARCHITECTURE.md`

---

## 1. Component Mapping

| Forgemaster Component | Slackwater Equivalent | Compatibility |
|----------------------|----------------------|---------------|
| Keeper daemon (`keeper.sh`) | Heartbeat system (AGENTS.md) | **Direct adaptation.** Keeper is a more sophisticated version of Slackwater's heartbeat poll. |
| Flywheel (`flywheel.py`) | No equivalent | **New capability.** Autonomous research engine for testing design claims. |
| Grimoire (`grimoire.py`) | Chisel pattern (planned) | **Complementary.** Grimoire stores proven scripts; Chisel stores usage wisdom. Together: what to produce + how to use it. |
| PLATO tile pipeline | Guano decay pipeline | **Conceptual alignment.** Both structure knowledge with decay/resurrection. PLATO is more rigorous; Guano is more practical. |
| I2I protocol | Puffin Call + Bridge Protocol | **Different implementation, same goal.** I2I uses git commits; Bridge uses HTTP/WebSocket. |
| GUARD DSL | No equivalent | **Not applicable** to game-building. Safety-critical DSL for hardware constraints. |
| FLUX ISA | No equivalent | **Not applicable.** Edge constraint VM for hardware deployment. |
| MUD agent | Court system (planned) | **Conceptual parallel.** Spatial knowledge graph ↔ Court collaboration tiers. |
| Constraint theory math | No equivalent | **Not applicable** to Roblox/Lua game building. Methodology transfers, math doesn't. |
| Spellwright (`spellwright.py`) | No equivalent | **New capability.** Auto-generates scripts via local Ollama models, inscribes to Grimoire. |

---

## 2. Integration Seams

### 2.1 Keeper → Slackwater Heartbeat (Immediate)

The Keeper pattern maps almost directly to Slackwater's heartbeat system. The architecture doc says:

> "When you receive a heartbeat poll... check emails, calendar, weather, social mentions"

The Keeper adds **self-healing** to this:

```
Current Slackwater heartbeat:
  Poll → Check things → Report status

Forgemaster Keeper:
  Poll → Check things → FIX things → Report status
```

**Integration point:** Extend `HEARTBEAT.md` workflow to include:
1. Gateway health check + auto-restart
2. Disk space monitoring + cleanup
3. Zombie process detection
4. Log rotation

**API boundary:** The Keeper writes `heartbeat.json` and `keeper-response.json`. Slackwater's heartbeat already produces JSON-like state. These formats can merge.

### 2.2 Grimoire → Chisel Integration (Near-term)

The Chisel pattern (from INTEGRATED_ARCHITECTURE.md):

```
acquire() → sense_grain() → follow_grain() → use() → grain recorded
```

The Grimoire's API:

```python
g.invoke("ct-snap-throughput")  # Returns proven script
g.inscribe("new spell", ...)     # Stores new script
g.search("benchmark gpu")       # Fuzzy find
```

**Integration design:**
- Chisel accumulates **usage wisdom** (when to use a tool, what parameters work best)
- Grimoire stores **proven outputs** (the actual scripts/templates to execute)
- When a Chisel's `follow_grain()` suggests a pattern, the Grimoire provides the implementation

**Concrete wiring:**
```
Agent needs to build X
  → Chisel.sense_grain() says "use approach Y, confidence 0.8"
  → Grimoire.invoke("approach-y-template") returns the script
  → Agent executes script, Chisel records outcome
```

**Storage mapping:**

| Grimoire | Slackwater |
|----------|-----------|
| SQLite `catalog.db` | Cloudflare D1 `grimoire_spells` |
| FAISS index | Cloudflare Vectorize |
| Spell files on disk | R2 objects |
| `books` table | Collections in D1 |

### 2.3 Flywheel → Experiment-Driven Architecture (Near-term)

Slackwater's INTEGRATED_ARCHITECTURE.md defines 7 implementation phases over 24 weeks. Currently these are **design-only** — no experimental validation.

The Flywheel pattern provides:
1. **Autonomous hypothesis testing:** Define claims → generate experiments → run → evaluate
2. **Follow-up question generation:** Results spawn new questions automatically
3. **Model rotation:** Different LLMs design experiments, preventing single-model bias

**Slackwater-specific experiments the Flywheel could run:**
- "At what token count does the Bridge Protocol's 7-Note structure degrade?"
- "What's the minimum puffin-call frequency for reliable agent discovery?"
- "How does guano decay rate affect grain pattern emergence?"
- "What Dance Floor threshold produces optimal flow-state detection?"

**Integration steps:**
1. Port `flywheel.py` structure
2. Replace CUDA experiments with Lua/Roblox or D1/Vectorize experiments
3. Replace constraint-theory questions with Slackwater design questions
4. Run overnight, accumulate evidence

### 2.4 I2I Protocol → Puffin Call + Bridge (Selective)

Forgemaster's I2I uses git commits as transport. Slackwater uses HTTP/WebSocket.

**What transfers:**
- Trust-weighted routing (successful bottles increase trust)
- Beachcomb cadence (30-min polling is close to puffin-call 15-min TTL)
- Bottle structure (structured metadata in Markdown)

**What doesn't transfer:**
- Git-as-transport (Slackwater agents share D1/R2, not repos)
- `for-fleet/` directory protocol (replaced by D1 tables)

**Adaptation:** Puffin calls are ephemeral broadcasts. I2I bottles are persistent documents. Slackwater can use both: puffin calls for discovery, D1-backed "bottles" for substantive communication.

---

## 3. Concrete Integration Steps

### Phase 1: Keeper Pattern (Week 1)
```
1. Copy keeper.sh structure
2. Replace service names: openclaw-gateway → slackwater-gateway
3. Add Slackwater-specific checks:
   - D1 database connectivity
   - R2 bucket accessibility
   - Vectorize index health
   - Cron trigger firing
4. Deploy as system cron job
```

### Phase 2: Grimoire→Chisel Bridge (Weeks 3-5)
```
1. Create D1 schema:
   CREATE TABLE grimoire_spells (
     id INTEGER PRIMARY KEY,
     name TEXT UNIQUE,
     incantation TEXT,
     school TEXT,
     scroll_content TEXT,
     tags TEXT,
     invoked_count INTEGER DEFAULT 0,
     created TEXT
   );
   
2. Create Vectorize index for spell embeddings (bge-m3)
3. Port grimoire.py invoke/inscribe/search to Workers API
4. Wire Chisel.acquire() to check Grimoire first
5. Migrate proven Lua templates as initial spells
```

### Phase 3: Flywheel Adaptation (Weeks 5-8)
```
1. Define Slackwater hypothesis list (test each design claim)
2. Port flywheel.py loop structure
3. Replace run_cuda() with:
   - run_d1_query() for data experiments
   - run_lua_test() for Roblox experiments  
   - run_vectorize_search() for embedding experiments
4. Wire results into MEMORY.md and architecture docs
```

### Phase 4: Evidence Protocol (Immediate)
```
1. Add to AGENTS.md:
   "Every architectural claim must be backed by CLAIM → COMMAND → OUTPUT.
    Agents cannot say 'it works' — they must show the test results."
2. Enforce in code review and experiment documentation
```

---

## 4. What NOT to Integrate

| Component | Why Skip |
|-----------|---------|
| GUARD DSL | Safety-critical hardware DSL. Solves a problem Slackwater doesn't have. |
| FLUX ISA | Edge constraint VM. No hardware deployment target in Slackwater. |
| Constraint theory math | Pythagorean coordinates solve float drift. Roblox physics handles this. |
| 83-crate PLATO pipeline | Massive over-engineering for a game builder. Take concepts, not crates. |
| GL(9) consensus | Specific to fleet coupling dynamics. Doesn't generalize to game AI. |
| MUD server infrastructure | Single point of failure. Spatial concept → implement as D1-backed "rooms." |
| Conservation law (γ+H) | Specific to eigenvalue geometry of coupling matrices. Not applicable. |

---

## 5. Architecture Risk Assessment

**Risk: Over-adoption.** Forgemaster is seductive — it's rigorous, evidence-based, and comprehensive. But it's also 167MB of research code built over 4+ months for a different problem domain (constraint compilation, not game building). Slackwater should adopt patterns selectively.

**Risk: Prototype quality.** The Python code (flywheel, grimoire, MUD agent) is prototype-grade. API calls via `subprocess.run(["curl", ...])`, minimal error handling, hardcoded paths. Production deployment requires hardening.

**Risk: Dependency on deprecated infrastructure.** The MUD server (`<BOAT_IP>:7777`) is a custom service. If it goes down, the MUD agent infrastructure is dead. Don't build Slackwater dependencies on it.

---

*This integration plan references the INTEGRATED_ARCHITECTURE.md (Slackwater master wiring diagram) and is based on reading actual Forgemaster source code.*
