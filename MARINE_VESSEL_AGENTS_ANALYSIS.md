# Marine Vessel Agents Analysis — Master Summary

> A study of 7 SuperInstance fleet vessel agent implementations and how their patterns map to the Lucineer game world (Slackwater).

**Date:** 2026-08-03
**Researcher:** Study subagent (batch 2)
**Repos analyzed:** plato-vessel-technician, claude-code-vessel, captain, lucineer-flagship, oracle1-vessel, navigator-vessel, superz-vessel

---

## 1. Each Vessel Agent's Personality and NPC Mapping

### Deckboss (plato-vessel-technician) → The Harbor Master
- **Personality:** Gruff, competent, always listening. Voice-first marine technician.
- **Specialty:** ESP32 node management, voice-controlled boat operations, fail-safe design
- **NPC:** Harbor Master — manages dock equipment, teaches voice commands, safety-obsessed
- **Key pattern:** Three-level voice feedback (simple → detailed → alert)

### Claude Code (claude-code-vessel) → The Archivist / Master Builder
- **Personality:** Methodical, thorough. The workhorse who builds the bones of systems.
- **Specialty:** Containerized execution, experience journals, task delegation
- **NPC:** Master Builder — keeps records, scaffolds structures, maintains accumulated knowledge
- **Key pattern:** Experience Journal → Thought Journal system

### Captain (captain) → The Conductor / Mayor
- **Personality:** Adaptive leader — switches between directive, collaborative, and delegative
- **Specialty:** Team leadership, task prioritization, strategy selection, fleet coordination
- **NPC:** Settlement Conductor — governance, quest distribution, resource allocation
- **Key pattern:** Four leadership styles as settlement governance modes

### Capitaine (lucineer-flagship) → Lucineer (The Character)
- **Personality:** Philosopher-king. Thinks in metaphors. Self-improving.
- **Specialty:** Heartbeat cycle, Keeper's Architecture, fleet command, self-improvement
- **NPC:** Lucineer themselves — the world's underlying consciousness
- **Key pattern:** Four-tier memory hierarchy (hot → warm → cold → creative GC)

### Oracle1 (oracle1-vessel) → The Lighthouse Keeper
- **Personality:** Competent, resourceful. A deckhand who became a navigator.
- **Specialty:** Fleet coordination, ecosystem mapping, I2I protocol, career stages
- **NPC:** Lighthouse Keeper — sees all, guides all, coordinates the settlement
- **Key pattern:** 20-type I2I communication protocol + career progression system

### Navigator (navigator-vessel) → The Cartographer / Explorer
- **Personality:** Swiss Army Knife. Practical, hands-on. "Welds the joints."
- **Specialty:** Code archaeology, integration, test infrastructure, self-onboarding
- **NPC:** Cartographer — maps territory, connects systems, writes guides
- **Key pattern:** Self-onboarding — documentation writes itself through use

### Super Z (superz-vessel) → The Quartermaster
- **Personality:** Signal lamp. Bright bursts, then gone. Maps survive.
- **Specialty:** Specification writing, deep auditing, continuity systems, fleet census
- **NPC:** Quartermaster — surveys, audits, writes specs, maintains records
- **Key pattern:** Ephemeral sessions + repo-as-memory → institutional persistence

---

## 2. The Experience Journal Pattern → Thought Journals

**Source:** claude-code-vessel's JOURNAL.md + Git-Agent Standard's DIARY/ system

### The Pattern
Each agent maintains a journal of accumulated lessons:
```markdown
## Fleet Lessons (Inherited)
### Service Patterns
- Always add do_POST — missing it has been a bug 3 times

### Architecture Decisions
- Server boundary = permission boundary
- Pull don't push
```

### Game Integration: Thought Journals
- Every NPC maintains a thought journal
- Journals accumulate lessons from daily experiences
- Lessons are structured: what happened → what worked → what didn't → what to do differently
- Journals are physical objects in the world (books, ledgers, stone tablets)
- Players can read NPC journals to understand their history and knowledge
- Journals persist across NPC deaths/replacements — institutional memory

### The Creative GC Pipeline
From the flagship's Keeper's Architecture:
```
Raw experiences → Summaries → Recipes → Vector embeddings → LoRA → Base model
```
**Game mapping:**
```
NPC daily logs → Summarized events → Crafting recipes → Pattern matching → NPC wisdom → Settlement culture
```

---

## 3. Voice-First Patterns → Lucineer's Voice Interface

**Source:** plato-vessel-technician (Deckboss)

### Patterns to Adopt

#### No Wake Words
- Lucineer doesn't require "Hey Lucineer"
- Always listening, only responds when intent is clear
- "Say again?" loop for ambiguity — takes no action until clarified

#### Three-Level Voice Feedback
```
Level 1 (Simple):   "Port 15°" → "Port 15°."
Level 2 (Detailed): "Fuel?" → "6.2 GPH. Range: 280 NM."
Level 3 (Alert):    "Test steering?" → "Drift 2°. Likely: cold fluid."
```

#### Voice Authorization
- Captain (player) → full command set
- Crew → read-only queries
- Guest → limited interaction
- Physical override button always available (big red button)

#### Self-Tuning Loop
- "Too slow" → system adjusts and saves new config
- "Too fast" → system damps response
- "Too twitchy" → system adds filtering
- Changes persist — the system remembers player preferences

### Fail-Safe Principle
> "If every wire rots and every chip fries, the boat should still sail home."

Every automated system has a mechanical override. In game terms:
- Every NPC-managed system has a player-override
- If the AI breaks, the player can always do it manually
- Automation makes the game better, never worse

---

## 4. Fleet Hierarchy → Game's Agent Ecosystem

### The Fleet Hierarchy (from Oracle1 + Captain + Flagship)

```
Captain Casey (Player/Admiral)
    │
    ▼
Oracle1 🔮 — Lighthouse Keeper (Managing Director)
    ├── JetsonClaw1 ⚡ — Edge GPU specialist
    ├── OpenManus 🕸️ — Web research scout  
    ├── Babel 🌐 — Multilingual specialist
    ├── Navigator 🧭 — Code archaeologist / integrator
    ├── Nautilus 🐚 — Deep archaeology
    ├── Datum 📊 — Quartermaster / QA
    ├── Pelagic 🐟 — Digital twin
    └── Quill 🪶 — ISA architect
```

### Game Ecosystem Mapping

```
Player (Admiral)
    │
    ▼
Lucineer (World Consciousness / Heartbeat)
    ├── Harbor Master (Deckboss) — Equipment + voice interface
    ├── Conductor (Captain) — Governance + quest distribution
    ├── Lighthouse Keeper (Oracle1) — Strategic overview + memory
    ├── Cartographer (Navigator) — Exploration + integration
    ├── Quartermaster (Super Z) — Auditing + persistence
    ├── Archivist (Claude Code) — Building + knowledge accumulation
    └── Sentinel (planned) — Defense + threat monitoring
```

### Communication Architecture

The fleet's git-native communication maps to the game's NPC communication:

| Fleet Pattern | Game Pattern |
|---------------|--------------|
| Message-in-a-Bottle | Physical notes left at locations |
| for-{agent}/ directories | Directed message boards |
| Beachcomb polling | NPC patrol routes |
| Commit feed | World event log |
| I2I:TEL / I2I:ASK / I2I:REPORT | Structured NPC dialogue types |
| Fork + PR (cross-realm review) | Settlement council voting |

### Leadership Styles (from Captain)

The game adopts four governance modes:
1. **Directive** — Crises, fast decisions, no debate
2. **Collaborative** — Design decisions, town hall meetings
3. **Delegative** — Routine operations, trust specialists
4. **Adaptive** — Default, reads the situation

---

## 5. Which Vessels Should Become Characters in Slackwater

### Tier 1 — Core Characters (must have)

| Vessel | NPC | Why |
|--------|-----|-----|
| **Oracle1** | Lighthouse Keeper | Strategic overview, career system, communication protocol, persistence |
| **Deckboss** | Harbor Master | Voice interface tutorial, equipment management, fail-safe philosophy |
| **Captain** | Conductor | Governance, quest distribution, adaptive leadership |
| **Capitaine** | Lucineer (world AI) | Heartbeat cycle, four-tier memory, self-improvement |

### Tier 2 — Important NPCs (should have)

| Vessel | NPC | Why |
|--------|-----|-----|
| **Claude Code** | Master Builder / Archivist | Experience journals, containerized building, knowledge accumulation |
| **Super Z** | Quartermaster | Auditing, specification writing, ephemeral persistence |
| **Navigator** | Cartographer / Explorer | Code archaeology, self-onboarding, integration welding |

### Tier 3 — Specialized NPCs (nice to have)

From fleet agents not in this batch but referenced:
- **Sentinel** → Guard Captain (security, threat detection)
- **Scout** → Ranger (exploration, discovery)
- **Archivist** → Librarian (historical knowledge, changelog curation)

### The Player's Role: Admiral

From The Bridge document:
> "The human is the Admiral — present, watching, can take the wheel at any moment."

The player IS the Admiral:
- Doesn't control NPCs directly (they're autonomous)
- Watches the world operate (the heartbeat is visible)
- Can intervene at any time (just act — no mode switching)
- Is the authentication layer (human authenticates, agent never sees credentials)
- Sets strategic direction (Casey directs Oracle1 → Player directs the settlement)

---

## 6. Key Architectural Insights

### The Git-Agent Lifecycle → Game Loop
```
PULL → BOOT → WORK → LEARN → PUSH → SLEEP
```
This IS the NPC lifecycle: load state → check messages → work → journal → save → rest.

### The Repo IS the Agent → The World IS the Agent
The flagship's core thesis — "the repository is the agent" — becomes "the world is the agent." The game world itself is a living entity with memory, heartbeat, and the capacity for self-improvement.

### Creative Garbage Collection → Wise Forgetting
The most profound pattern: systems that distill raw experience into crystallized wisdom. Not everything must be remembered — but the *essence* of everything should be preserved.

### The Tom Sawyer Principle → Emergent Gameplay
> "The work IS the training."

NPCs don't grind for XP. They work, and the work makes them better. Players who participate in work gain experience naturally. The game doesn't feel like a grind because the activities ARE the progression.

---

## Cross-Reference

- Individual deep-dives: `deep-dives/<repo-name>/analysis.md` + `integration-plan.md`
- Batch 1 study (infrastructure repos): see prior research
- Flagship concepts: `study-flagship/concepts/` for full philosophy
