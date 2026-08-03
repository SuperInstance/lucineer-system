# claude-code-vessel — Integration Plan

## → Thought Journal System

### The Experience Journal → Thought Journals

The JOURNAL.md pattern from claude-code-vessel maps directly to Lucineer's **Thought Journal** system — the mechanism by which NPCs and the world accumulate experience and get smarter over time.

### Pattern: Structured Accumulation

```markdown
## Fleet Lessons (Inherited from predecessors)
### Service Patterns
- Always add do_POST — missing it has been a bug 3 separate times

### Architecture Decisions  
- Server boundary = permission boundary
- Pull don't push
```

**Game mapping:** Each NPC has a thought journal that accumulates lessons:
- **Crafting lessons:** "Iron + coal at temperature X = steel. Learned from 3 failed attempts."
- **Social lessons:** "Player Eileen likes direct answers. Learned from 5 interactions."
- **World lessons:** "Tide pattern correlates with moon phase. Learned from observation cycle 7."

### Pattern: The Boot Sequence

```
PULL → BOOT → WORK → LEARN → PUSH → SLEEP
```

**Game mapping:** NPCs follow this cycle:
1. **PULL** — NPC loads their state from the world database
2. **BOOT** — NPC reads their journal, checks for messages
3. **WORK** — NPC performs their daily routine
4. **LEARN** — NPC writes what happened to their journal
5. **PUSH** — NPC saves state to the world database
6. **SLEEP** — NPC goes dormant until next activation

### Pattern: Git-Agent Standard → NPC Standard

The Git-Agent Standard v2.0 becomes the **NPC Persistence Standard**:

| Git-Agent File | NPC Equivalent | Purpose |
|----------------|----------------|---------|
| CHARTER.md | npc/identity.toml | Who the NPC is, their purpose |
| STATE.md | npc/state.json | Current status, health, mood |
| TASK-BOARD.md | npc/tasks.json | Active tasks and priorities |
| SKILLS.md | npc/skills.json | Capabilities with confidence levels |
| DIARY/ | npc/journal/ | Daily entries — what happened, what learned |
| IDENTITY.md | npc/profile.json | Name, model, vibe, emoji |

### Pattern: Message-in-a-Bottle → NPC Communication

NPCs communicate asynchronously through the world:
- **Bottles** — physical notes left at locations (persist in world)
- **Directed messages** — NPC A leaves a note for NPC B at a meeting spot
- **Broadcasts** — Town crier announcements that any NPC can process
- **Commit feed** — World event log that all NPCs can scan

### Character Mapping: Claude Code → Slackwater NPC

**NPC Concept:** The Archivist / Master Builder
- Methodical, thorough, keeps records of everything
- Can scaffold structures from templates
- Writes the best blueprints in the settlement
- Keeps the settlement's accumulated knowledge

**In-Game Role:** Builder + knowledge keeper
- Provides crafting recipes (accumulated through journals)
- Can build structures from templates (the containerized execution pattern)
- Maintains the settlement's library of lessons learned
- Other NPCs consult them for "how did we solve this last time?"

### Pattern: The Tom Sawyer Principle → Crafting XP

> "The work IS the training."

- NPCs don't grind for XP — they work, and the work makes them better
- Players who help NPCs with tasks gain crafting experience naturally
- The crafting animation IS the level-up — no separate grind
