# captain — Integration Plan

## → The Conductor Role

### Character Mapping: Captain → The Conductor

**NPC Concept:** The Settlement Conductor / Mayor
- Adaptive leadership style — switches between directive and collaborative
- Makes decisions with tracked rationale (auditable history)
- Delegates based on NPC capabilities and current load
- Manages resource allocation across the settlement

**In-Game Role:** Settlement governance and task distribution
- Players receive quests from the Conductor
- The Conductor routes tasks to the right NPCs based on their skills
- Resource allocation: which project gets attention this cycle?

### Leadership Styles as Game States

The Captain's four styles become **settlement governance modes**:

1. **Directive (Emergency):** During crises (monster attack, natural disaster), the Conductor issues direct orders. No debate. Fast execution.

2. **Collaborative (Design):** For settlement planning, the Conductor gathers input from multiple NPCs. Players participate in town hall meetings.

3. **Delegative (Routine):** For day-to-day operations, the Conductor trusts each NPC to manage their domain. Hands-off.

4. **Adaptive (Default):** The Conductor reads the situation and picks the right mode. Most of the time, this is active.

### Decision Tracking as Lore

Every significant settlement decision is recorded with rationale:
```
Decision #047: "Build defensive wall on north side"
  Rationale: " scouting reports show increased activity"
  Options considered: ["North wall", "South wall", "Patrol routes", "Defer"]
  Chosen: "North wall"
  Made by: Conductor
  Date: Cycle 47, Day 3
```

Players can browse the **Settlement Chronicles** — a physical book/log in the Conductor's office that contains every decision ever made. This creates deep lore and player investment.

### Fleet Coordination → NPC Work Assignment

The FleetCoordination pattern becomes the **NPC Work Scheduler**:

- Each NPC has: status (idle/busy/offline), capacity (how much work they can handle), tags (skills)
- When work appears, the scheduler assigns it to the least-loaded NPC with matching skills
- NPCs can be "drained" (no new assignments) when they're about to go on a journey
- Settlement health metrics: how many NPCs are active vs offline

### Strategy Engine → Settlement Strategy

Multi-phase settlement strategies with resource budgets:
- **Strategy:** "Expand to the eastern valley" (3 phases, requires 500 wood, 200 stone, 10 workers)
- **Strategy:** "Establish trade route" (2 phases, requires 5 guards, 3 pack animals, 50 trade goods)
- The Conductor prioritizes strategies based on available resources and urgency
- Players can see the strategic plan and contribute to specific phases

### Delegation Pattern → Quest System

When the Conductor delegates:
- Tasks require specific skills → routes to NPC with matching tags
- NPC capacity matters — a busy NPC won't accept new work
- Delegation history is tracked → quest chains emerge naturally
- "Release" an NPC from a task → they become available again
