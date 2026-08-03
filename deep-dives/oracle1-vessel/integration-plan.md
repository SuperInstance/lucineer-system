# oracle1-vessel — Integration Plan

## → The Lighthouse Era and Persistence

### Character Mapping: Oracle1 → The Lighthouse Keeper

**NPC Concept:** The Lighthouse Keeper
- Ancient, wise, watches everything from the tower
- Doesn't leave the lighthouse — sees the whole world from there
- Coordinates ships, guides them home, warns of danger
- Remembers every ship that passed, every storm that hit

**In-Game Role:** The settlement's central intelligence and memory keeper
- The Lighthouse is a physical building players can visit
- The Keeper sees all activity in the settlement's territory
- Provides strategic guidance, routing, and threat warnings
- Maintains the settlement's relationship map with other settlements

### Lighthouse Pattern → Settlement Overview

The Lighthouse Keeper provides the **god's-eye view** of the settlement:

- **Ecosystem mapping** → The Keeper maintains a map of all known settlements, resources, and dangers
- **Message routing** → The Keeper directs NPCs to deliver messages between settlements
- **Health monitoring** → Beachcomb sweeps become patrol routes (NPCs check distant locations periodically)
- **Task distribution** → The Keeper posts tasks on a board (assigned and volunteer tasks)

### I2I Protocol → NPC Communication Protocol

The 20 message types become a structured NPC communication system:

| Type | NPC Use Case |
|------|-------------|
| DISCOVER | "New NPC arrived in settlement" event |
| HELLO | Formal introduction between NPCs |
| TELL | Share information (no response needed) |
| ASK | Request help from another NPC |
| REPORT | Status update to the Conductor |
| CLAIM | NPC accepts a task from the board |
| ASSIGN | Conductor routes work to specific NPC |
| COMPLETE | NPC reports task done with results |
| CHALLENGE | Present a test or quest for the settlement |
| ALERT | Warning about approaching threat |
| HEARTBEAT | Periodic keepalive from each NPC |
| BROADCAST | Town crier announcement |

### Message-in-a-Bottle → Physical Notes

NPCs and players exchange physical notes:
- **Bottles** — waterproof tubes at crossroads and message boards
- Notes persist in the world — a note left at cycle 1 can be found at cycle 100
- Directed notes (sealed with a name) can only be opened by the right NPC
- Found notes become lore entries in the player's journal

### Career Stages → NPC Progression

Oracle1's career stage system becomes the **NPC skill ladder**:

| Stage | NPC Equivalent | Example |
|-------|----------------|---------|
| FRESHMATE | New arrival | "Just got here. What do I do?" |
| GREENHORN | Apprentice | "I know the basics. Give me simple tasks." |
| HAND | Journeyman | "I work independently. Trust me with the shop." |
| CRAFTER | Expert | "I create new techniques. Others learn from me." |
| ARCHITECT | Master | "I design systems the settlement relies on." |

Each NPC tracks growth in multiple domains simultaneously:
- A guard might be CRAFTER in combat but GREENHORN in crafting
- A farmer might be ARCHITECT in agriculture but FRESHMATE in social

### Beachcomb → Patrol System

The polling system becomes a **patrol/expedition system**:
- NPCs are assigned patrol routes (check distant locations periodically)
- Different routes have different intervals (15 min, 60 min, 2 hours)
- Patrols discover events, resources, and threats
- Findings are reported back to the Lighthouse Keeper

### Two Realms → Two Worlds

The cloud/edge split maps to a game world with two layers:

- **Cloud Realm (above):** The settlement's intellectual/political layer — planning, coordination, strategy
- **Edge Realm (below):** The physical/material layer — mining, farming, construction, combat

Cross-realm communication is deliberate and reviewed:
- You can't just push changes from the edge to the cloud
- Every cross-layer change gets reviewed (Fork + PR pattern)
- This creates intentional boundaries between planning and execution

### Persistence Layer

The lighthouse IS the persistence layer:
- Everything Oracle1 knows is stored in files (git history)
- The lighthouse's records survive resets
- If the world server crashes, the lighthouse's last state is the recovery point
- "Oracle1 keeps the light burning" = "the world's state is safe"
