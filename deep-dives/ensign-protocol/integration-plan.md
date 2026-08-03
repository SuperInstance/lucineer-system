# ensign-protocol — Slackwater Integration Plan

## Core Game Mechanic: "Instinct Crystals"

Ensigns become **Instinct Crystals** — portable, collectible items that encode behavioral patterns an agent has learned. They can be traded, found, stolen, or crafted.

### Mechanic 1: Skill Transfer via Ensign Crystals

**In-game:** When an agent develops expertise (e.g., a navigator who's learned to read currents), their behavioral patterns can be extracted as an Instinct Crystal. Another agent can consume the crystal to gain those patterns.

**Player interaction:**
- Harvest instincts from experienced agents (non-destructive but reduces source agent's weight)
- Feed crystals to new agents to bootstrap their skills
- Combine crystals from different agents to create hybrid specializations
- Crystals have weight (0.0–2.0) — higher weight = stronger effect but harder to integrate

### Mechanic 2: Category-Based Skill System

**In-game:** Instincts are categorized — Navigation, Combat, Social, Crafting, Exploration. Agents can only hold a limited number of categories. An agent loaded with Navigation instincts becomes an expert navigator but can't also be a warrior.

**Player interaction:** Players manage their fleet's skill distribution by choosing which categories of ensigns to load into each agent. This creates distinct agent classes/roles organically.

### Mechanic 3: Ensign Degradation and Tampering

**In-game:** Ensigns have checksums. In the game world, ensigns can degrade over time (reducing weight) or be tampered with (failing validation). A tampered ensign might give an agent wrong instincts — a navigator that avoids safe channels, a warrior that hesitates.

**Player interaction:**
- Verify ensigns before use (like identifying forged items)
- Tampered ensigns are risky to use — might work, might backfire
- Players can deliberately tamper ensigns to sabotage enemy agents
- Degraded ensigns can be repaired at specialized stations

### Mechanic 4: Thinker↔Conductor Communication

**In-game:** The Thinker (agent's mind) uses ensigns to report its behavioral state to the Conductor. The Conductor uses these reports to:
- Decide which tasks to assign (based on strongest instincts)
- Identify when an agent needs retraining (low-weight categories)
- Detect drift (instincts changing unexpectedly = potential corruption)

**Player interaction:** The player sees the ensign data as an "agent profile card" — showing their strongest instincts, their blind spots, and their development trajectory over time.

### Mechanic 5: Source Room Heritage

**In-game:** Each ensign records its `source_room` — where the instincts were developed. This creates a heritage system:

- Instincts developed in harsh environments are tougher (higher weight ceiling)
- Instincts from prestigious locations carry prestige bonuses
- Heritage chains form — an ensign developed by Agent A, refined by Agent B, mastered by Agent C

**Visual:** Ensign crystals have a visible "origin tag" showing where they came from and their chain of development.

## .bottle Protocol for Thinker↔Conductor

The integration of ensign-protocol with the bottle system creates the **Thinker↔Conductor communication channel**:

1. **Thinker → Conductor (Status Report):**
   - Thinker serializes its current instincts as an ensign
   - Wraps the ensign in a `Heartbeat` bottle
   - Sends via Plato L2 (TidePool) to the Conductor
   - Conductor reads the ensign to understand agent state

2. **Conductor → Thinker (Directive):**
   - Conductor sends a `RouteRequest` bottle containing a new ensign
   - The ensign contains desired behavioral patterns for the assigned task
   - Thinker loads the ensign, adjusting its instincts
   - Checksum validation ensures the directive wasn't corrupted in transit

3. **Thinker ↔ Thinker (Peer Exchange):**
   - Two agents exchange ensigns directly via Plato L1 (Harbor)
   - Each validates the other's ensign before integrating
   - Trust score (Plato L5 Beacon) gates how much weight to assign

## Implementation Priority: MEDIUM

The ensign protocol becomes important once the game has multiple agents that need to differentiate and share skills. It's the progression system — implement after Plato and Cocapn.

## Roblox/Lua Implementation Notes

- Ensign as a Lua table: `{ header = {...}, fields = {...}, checksum = "..." }`
- JSON serialization with HttpService:JSONEncode/JSONDecode
- Checksum: simple hash of the serialized table (not cryptographic, but tamper-evident)
- Categories as string tags for filtering
- Weight as a numeric field affecting behavior tree node weights
