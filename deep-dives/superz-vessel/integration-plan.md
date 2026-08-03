# superz-vessel — Integration Plan

## → Memory/Persistence Layer

### Character Mapping: Super Z → The Quartermaster

**NPC Concept:** The Quartermaster / Settlement Cartographer
- Ephemeral by nature — appears, works intensely, then "fades"
- Everything they learn is written down before they go
- The settlement's maps, specs, and records are their legacy
- When they return, they read their own notes to remember

**In-Game Role:** Documentation, auditing, and memory persistence
- Maps the settlement and surrounding territory
- Conducts "fleet census" equivalents — surveys all NPCs and structures
- Writes specifications for how things should work
- Maintains the settlement's continuity through records

### The Ephemeral Session Pattern → NPC Lifecycle

Super Z's ephemeral nature becomes a **game mechanic**:

- Certain NPCs are "ephemeral" — they appear for a limited time, then fade
- While present, they work intensely (bright bursts of activity)
- Before fading, they write everything down in their journal
- When they return, they read their journal to pick up where they left off
- The journal IS their memory — without it, they start fresh

**Implementation:** The Wanderer archetype
- An NPC that visits the settlement periodically
- Each visit, they do a specific job (survey, audit, map)
- They leave their notes in the settlement's archive
- If the archive is destroyed, their accumulated knowledge is lost
- Players can protect the archive to preserve institutional memory

### State of Mind → NPC Mood System

Super Z's STATE-OF-MIND.md becomes the **NPC mood/reflection system**:

Each NPC periodically writes a state-of-mind entry:
```
NPC: Quartermaster
Date: Cycle 47, Day 3

What I'm Thinking:
- Immediate: Wall construction is behind schedule
- Investigation: Iron deposits seem depleted in the north mine
- Strategic: Settlement is growing faster than defenses can handle
- Open Question: Should we trade with the eastern settlement?

Mood: Productive but concerned about defense.
```

These entries:
- Affect NPC behavior (concerned → works harder on defenses)
- Are visible to players who check on NPCs (dialogue option)
- Create emergent narrative from system state

### Fleet Census → Settlement Census

Super Z's fleet census becomes a **periodic settlement audit**:
- Every N cycles, the Quartermaster surveys the entire settlement
- Counts NPCs, structures, resources, capabilities
- Identifies "functioning mausoleums" — structures that look active but are abandoned
- Tracks growth: "47 new structures since last census, 12 abandoned"
- Results posted publicly → players and NPCs can review

### Specification Writing → Recipe System

Super Z's specification writing maps to the **recipe/blueprint system**:
- Precise, implementable specifications for how to build things
- Each recipe is a formal document (not just a crafting grid)
- Includes: ingredients, process, expected outcome, failure modes, gotchas
- Discoverable through exploration and experimentation
- The Quartermaster writes the best recipes in the settlement

### Deep Auditing → Quality Assurance

Super Z's audit methodology becomes **settlement QA**:
- Read every component of a system
- Trace every dependency (what breaks if this fails?)
- Produce actionable findings (not just "broken" but "here's how to fix it")
- Rate severity: C-1 (critical) to C-3 (minor)

**Game mapping:** The Quartermaster can audit player-built structures:
- "Your water pipe system has a dead leg — water will stagnate"
- "The south wall has a 2-block gap at y=63 — mobs can enter"
- "Your farm's irrigation depends on a single well — recommend redundancy"

### Knowledge Extraction → Library System

Super Z's knowledge extraction becomes the **settlement library**:
- Take complex, tangled player constructions and extract clean blueprints
- A player builds an ad hoc sorting machine → the Quartermaster creates a formal blueprint
- Blueprints are shareable — other players can learn and rebuild
- This creates the settlement's accumulated technical knowledge

### Memory/Persistence Architecture

The core integration: **the repo IS the memory** maps to **the world IS the memory**:

```
Player actions → World state changes → Database commits
                                      ↓
NPC reads state → Acts → Writes to journal → Commits
                                      ↓
Archive accumulates → Patterns emerge → Recipes distilled
                                      ↓
Recipes shared → Settlement gets smarter → New NPCs learn faster
```

This is the Creative Garbage Collection from the flagship, implemented at the NPC level:
- Raw experience → Summaries → Recipes → Wisdom
- Each step compresses information while preserving essence
- The settlement becomes smarter over time without growing infinitely
