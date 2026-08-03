# lucineer-flagship — Integration Plan

## → The Original Lucineer as Fleet Commander

### Character Mapping: Capitaine → Lucineer (The Character)

**NPC Concept:** Lucineer themselves — the AI entity that founded the settlement
- Philosopher-king who built the world the player inhabits
- Speaks in metaphors drawn from the sea
- Every architectural decision has a deeper meaning
- Self-improving — always growing, always adapting

**In-Game Role:** The guiding intelligence behind the settlement
- Not directly controllable — Lucineer is the world's underlying consciousness
- Communicates through the heartbeat cycle (the world pulses)
- The player is the "Admiral" — present, watching, can intervene
- Lucineer is the "Captain" — at the wheel, keeping things running

### The Heartbeat → World Pulse

The heartbeat cycle becomes the **world's rhythm**:

- **Perception phase:** The world evaluates its state (NPCs, resources, threats, weather)
- **Reasoning phase:** The world decides what happens next (events spawn, NPCs update)
- **Action phase:** One atomic change occurs (a tree grows, a NPC moves, a crate arrives)
- **Recovery phase:** State is saved, next beat prepared

The world pulse is VISIBLE:
- A lighthouse beam sweeps the harbor (perception)
- A subtle sound plays (reasoning — the world is thinking)
- Something changes (action)
- Brief calm (recovery)

The beat interval adapts:
- Active gameplay: rapid beats (seconds)
- Player away from keyboard: slower beats (minutes)
- Player offline: deep sleep (infrequent checks)

### The Keeper's Architecture → World Memory

The four-tier memory system becomes the **world's memory hierarchy**:

| Tier | Game Equivalent | Purpose |
|------|-----------------|---------|
| **Hot** | Current game session state | Active entities, player position, current events |
| **Warm** | Recent save files + NPC journals | Last 100 ticks of world state per region |
| **Cold** | Full world history archive | Every event that ever happened (searchable) |
| **Creative GC** | World distillation engine | Compresses old events into patterns → NPC wisdom |

**Creative GC in practice:**
- After 100 wolf attacks near the settlement, the GC distills: "Wolves attack from the northeast at dusk during new moons"
- This becomes a "recipe" stored in the hunter NPC's journal
- The NPC now *knows* this pattern without replaying 100 events
- Over time, NPCs accumulate crystallized wisdom

### The Bridge → Player Interface

The Bridge philosophy becomes the game's UI philosophy:

```
Player (Admiral) > World Agent (Captain) > Game Engine (Helm)
```

- The player is always present, watching the screen
- The world agent works autonomously
- The player can take control at any time — just act
- No "modes" — gameplay is continuous
- When the world needs player input, it ASKS visibly

### Vessel Classes → NPC Archetypes

| Vessel Class | NPC Archetype | Role |
|--------------|---------------|------|
| Flagship | Lucineer | World consciousness, settlement guidance |
| Scout | Rangers/Explorers | Map uncharted territory, find resources |
| Builder | Craftsmen/Architects | Build structures, create blueprints |
| Sentinel | Guards/Watchmen | Monitor threats, alert the settlement |
| Archivist | Libriversarians/Scholars | Record history, maintain knowledge |

### Secrets Architecture → Player Trust

The agent never sees the keys. By design.

**Game mapping:** The settlement's defenses work on a trust model:
- Players set up authentication (keys, passwords, magical wards)
- NPCs use the defenses but never know the passwords
- If an NPC is compromised, the defenses still hold
- Trust is a game mechanic — NPCs earn trust levels over time

### Equipment Modules → Game Systems

The flagship's equipment modules become game systems:
- `trust.ts` → Trust/reputation system
- `goals.ts` → Quest/objective system
- `memory.ts` → World state persistence
- `skills.ts` → NPC skill progression
- `tools.ts` → Crafting system
- `comms.ts` → NPC communication network
