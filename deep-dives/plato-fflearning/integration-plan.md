# PLATO Forward-Forward Learning — Slackwater/Lucineer Integration Plan

> How `plato-fflearning` fits into the Lucineer multi-agent game-building ecosystem

---

## 1. What Is This in Ecosystem Terms?

The Lucineer system is a multi-agent game-building pipeline where AI agents collaboratively build a Roblox game. Each agent (Lucineer himself, plus 12 recruitable NPCs) has different specializations, personalities, and skill levels. The system uses a 5-model pipeline running through Cloudflare Workers with D1, Vectorize, and R2.

`plato-fflearning` provides a **learning signal** that's currently missing from this stack. Right now:

- **Lucineer-vector** stores 55 skills the system already knows
- **Lucineer-memory** (D1, 9 tables) records what happened
- **Lucineer-brain** routes tasks to the right model
- But nothing tracks **whether an agent is getting better at its job over time**

FF learning fills this gap. It answers: "Is oracle1 actually reliable?" and "Should we trust this agent's tiles?"

---

## 2. Mapping to Slackwater Concepts

### 2.1 Apprenticeship Chains

In Slackwater, agents progress through technology eras — a junior builder becomes a master builder through accumulated experience. FF goodness maps directly:

| Slackwater Concept | FF Learning Equivalent |
|--------------------|-----------------------|
| Bond level (0–100) | Goodness score (0.0–1.0) |
| Bond threshold to unlock abilities | Goodness threshold (0.7) for tile reinforcement |
| Agent performs task successfully | Positive pass |
| Agent fails or imagines failure | Negative pass |
| Master teaches apprentice | Master's positive pass reinforces shared tiles |
| Apprentice makes mistake | Negative pass, goodness drops, tiles not reinforced |

**Integration**: When a player crafts an item with an NPC's help, the NPC gets a positive pass if the craft succeeds (real outcome) and a negative pass if it fails. Over time, the NPC's goodness score determines what recipes it can teach — only agents above the "high" threshold (0.6) can teach advanced-era recipes.

### 2.2 Grain Patterns

In the Lucineer system, "grain" refers to the texture and quality of agent output — fine-grained, well-structured work vs. coarse, sloppy work. FF learning provides a grain-quality signal:

- **Fine grain**: Agent consistently produces positive passes → high goodness → tiles reinforced → next agent starts from a better knowledge base
- **Coarse grain**: Agent accumulates negative passes → low goodness → tiles not reinforced → knowledge doesn't propagate

This creates a **quality filter**: only knowledge from agents with proven track records gets permanently stored in the tile library.

### 2.3 Skill Lineage

When agent A's tiles get reinforced (goodness > 0.7) and agent B later retrieves those tiles, B benefits from A's learning. This is skill lineage:

```
Agent A (goodness 0.85) → positive tile reinforced
                            ↓
Agent B retrieves tile → B starts with A's knowledge
                            ↓
B has positive experience → B's goodness rises
                            ↓
B's tiles reinforced → C can learn from B
```

This is the **feed-forward** part: learning cascades forward through agent generations without backward propagation. Each agent learns locally and contributes globally.

---

## 3. Concrete Integration Architecture

### Phase 1: PLATO Server Bridge (1–2 days)

**Problem**: The library uses `/room/{name}` but PLATO server's actual API is `POST /submit` with a `room` field.

**Action**: Fix the HTTP integration:

```python
# Current (broken):
requests.post(f"{self.plato_url}/room/{self.positive_room}", json=tile)

# Fixed:
requests.post(f"{self.plato_url}/submit", json={**tile, "room": self.positive_room})
```

Also fix the tile count query — PLATO exposes `GET /room/{name}` which returns room details + tiles, so the GET call is correct.

**Deliverable**: Library that actually talks to a running PLATO server.

### Phase 2: D1 Persistence (1 day)

**Problem**: Goodness is in-memory. Process restart = amnesia.

**Action**: Store goodness state in the existing Lucineer D1 database:

```sql
CREATE TABLE IF NOT EXISTS ff_goodness (
    agent TEXT NOT NULL,
    goodness REAL DEFAULT 0.5,
    last_updated INTEGER,
    PRIMARY KEY (agent)
);

CREATE TABLE IF NOT EXISTS ff_passes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT NOT NULL,
    pass_type TEXT NOT NULL,  -- 'positive' or 'negative'
    experience TEXT,
    goodness_before REAL,
    goodness_after REAL,
    timestamp INTEGER
);
```

**Deliverable**: Goodness survives restarts; pass history is queryable.

### Phase 3: Cloudflare Worker Endpoint (1–2 days)

**Action**: Expose FF learning through the existing Lucineer relay worker:

```
POST /ff/pass          → record positive/negative pass
GET  /ff/state/{agent} → get learning state
GET  /ff/fleet         → fleet-wide state
POST /ff/cycle         → run learning cycle
```

**Deliverable**: FF learning accessible from Roblox Lua via HTTP.

### Phase 4: Roblox Integration (2–3 days)

**Action**: Create a Lua module that hooks FF learning into game events:

```lua
-- When a crafting action succeeds:
FFLearning.positive(agentId, "Crafted bronze sword successfully")

-- When it fails:
FFLearning.negative(agentId, "Failed to craft bronze sword")

-- Gate abilities behind goodness:
if FFLearning.getGoodness(agentId) > 0.7 then
    -- Unlock advanced recipes
end
```

**Deliverable**: NPCs in the game have measurable, evolving expertise that gates their abilities.

### Phase 5: Pipeline Integration (1 day)

**Action**: Feed FF goodness into the model routing pipeline:

- Agents with high goodness → trusted with complex tasks → routed to stronger models
- Agents with low goodness → routed to cheaper models for simpler tasks
- Fleet average goodness → displayed in dashboard

**Deliverable**: Model routing is informed by actual agent track records.

---

## 4. Connection to Existing Repos

| Repo | Connection | Integration Point |
|------|-----------|-------------------|
| `lucineer-relay` | HTTP bridge | Add `/ff/*` endpoints |
| `lucineer-memory` | D1 database | Add `ff_goodness` and `ff_passes` tables |
| `lucineer-system` | Model routing | Use goodness as a routing factor |
| `lucineer-vector` | Skill embeddings | Reinforced tiles get embedded |
| `lucineer-roblox` | Game client | Lua FFLearning module |
| `plato-server` | Tile storage | Fix API calls, add FF-specific rooms |

---

## 5. Apprenticeship Chain Design

The most powerful integration is using FF learning to model **master-apprentice relationships**:

```
Master Agent (goodness > 0.8)
    ↓ creates reinforced tiles
Apprentice retrieves tiles
    ↓ attempts task
Success → positive pass (apprentice goodness rises)
    ↓ apprentice creates own tiles
Failure → negative pass (apprentice goodness falls)
    ↓ tiles not reinforced, master's tiles remain authoritative
```

This mirrors how real apprenticeship works:
1. Master demonstrates (positive tile with high confidence)
2. Apprentice attempts (learning cycle)
3. Outcome determines tile propagation
4. Only successful apprentices' tiles enter the permanent library

### Concrete: Lucineer Teaching System

Lucineer (the master builder NPC) starts with goodness 0.85. When a player crafts with him:
- His tiles (building patterns, recipe knowledge) are already reinforced
- If the craft succeeds, both Lucineer and the player's helper NPC get positive passes
- If it fails, negative pass — the helper NPC's goodness drops
- Helper NPCs below 0.4 goodness can only assist with basic tasks
- NPCs above 0.7 goodness can teach other NPCs

This creates **emergent skill hierarchies** in the game world.

---

## 6. Grain Pattern Integration

### Fine-Grained vs. Coarse-Grained Agents

FF goodness can classify agent output quality:

```
Goodness > 0.7 → "fine-grained" agent
  → tiles go to `verified_patterns` room
  → embeddings weighted higher in Vectorize
  → other agents prefer these tiles

Goodness 0.4–0.7 → "moderate-grained" agent
  → tiles go to `experimental_patterns` room
  → embeddings normal weight

Goodness < 0.4 → "coarse-grained" agent
  → tiles go to `unreliable_patterns` room
  → embeddings suppressed
  → agent flagged for retraining
```

### Implementation: Vectorize Metadata

When creating embeddings in `lucineer-vector`, add goodness as metadata:

```python
metadata = {
    "agent": agent_id,
    "goodness": ff.get_goodness(agent_id),
    "pass_type": "positive",
    "verified": goodness > 0.7
}
```

This lets you filter searches: `vector_search(query, filter={"verified": True})` to only get knowledge from high-goodness agents.

---

## 7. Recommended Fork Changes

To make `plato-fflearning` production-ready for Lucineer:

1. **Fix the API calls** — use `/submit` with `room` field
2. **Add D1/SQLite persistence** — replace `self.state` dict with a database
3. **Implement `_reinforce_tiles()`** — actually POST confidence bumps to PLATO
4. **Add negative tile weakening** — POST low-confidence tiles to mark unreliable patterns
5. **Add configurable constants** — pass DECAY, BOOST, PENALTY, THRESHOLD in `__init__`
6. **Add logging** — replace `except: pass` with `logger.warning()`
7. **Fix the float precision bug** — use `round(avg, 4)` in fleet average
8. **Add domain-agnostic defaults** — remove `fleet_orchestration` bias
9. **Add batch operations** — `positive_pass_batch()` for processing multiple experiences
10. **Add export/import** — dump and restore goodness state

---

## 8. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| PLATO server API changes | Medium | High | Pin to specific PLATO version; add integration tests |
| Goodness gaming (agents farm positive passes) | Medium | Medium | Rate-limit passes; require human-confirmed outcomes |
| State loss (in-memory) | High (current) | High | Phase 2 D1 persistence |
| Cost of HTTP calls per pass | Low | Low | Batch passes; async queue |
| Overfitting to PLATO-specific tile format | Low | Medium | Abstract tile creation behind interface |

---

## 9. Timeline

| Phase | Duration | Dependencies | Outcome |
|-------|----------|-------------|---------|
| 1. PLATO API fix | 1–2 days | Running PLATO server | Working HTTP integration |
| 2. D1 persistence | 1 day | Phase 1 | Goodness survives restarts |
| 3. Worker endpoints | 1–2 days | Phase 2 | FF API accessible from game |
| 4. Roblox Lua module | 2–3 days | Phase 3 | In-game FF learning |
| 5. Pipeline integration | 1 day | Phase 3, 4 | Model routing by goodness |
| **Total** | **6–9 days** | | **End-to-end FF learning** |

---

## 10. Long-Term Vision

FF learning becomes the **reputation system** for the entire agent fleet:

- Every model in the pipeline (Seed-2.0-mini, Qwen3.6, Qwen3-Coder-480B, Hermes-405B, Nemotron-Ultra) gets a goodness score
- Goodness feeds into the γ + η = C conservation law: high-goodness agents get more cognitive budget
- The fleet becomes self-improving: agents that consistently produce good work get more responsibility, and their knowledge propagates through reinforced tiles
- Players see this as emergent NPC behavior: "Lucineer is really good at building" isn't scripted — it's earned through hundreds of positive passes

This is the feed-forward part of "feed-forward learning": knowledge flows forward through the system, each agent building on what previous agents earned, without ever computing a backward gradient.
