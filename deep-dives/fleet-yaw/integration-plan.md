# fleet-yaw — Slackwater Integration Plan

## Core Game Mechanic: "The Compass and the Keel"

Each NPC agent carries a **Yaw autopilot** — an internal navigation system that learns the game world's physics from first-person observation. Agents don't have omniscient knowledge; they learn bearings, detect collisions, and adjust their headings over time.

### Mechanic 1: Bearing Rate as Collision Prediction

**In-game:** Agents sense each other through **bearings** — the relative angle and rate of change between their headings. When bearing rate approaches zero, two agents are on a collision course.

**Player interaction:**
- Collision courses are visible as "intercept lines" between agents
- The player can see which agents are about to collide (socially, physically, strategically)
- Intervening in a collision course (redirecting one agent) creates ripple effects

**Use cases:**
- Physical collision (two agents pathing to the same point)
- Social collision (two agents competing for the same role)
- Resource collision (two agents drawing from the same finite source)

### Mechanic 2: Field Stress and Crowd Dynamics

**In-game:** When too many agents occupy similar "heading space" (working on related things), the field becomes **stressed**. Stressed agents receive heading change suggestions to spread out.

**Player interaction:**
- Visual "heat" in agent clusters — red = stressed, blue = healthy
- Player can resolve stress by diversifying agent assignments
- Persistent stress causes agents to autonomously seek new directions
- Over-stressed fields may trigger "exodus events" — agents leaving en masse

### Mechanic 3: Commissioning Phase as "Childhood"

**In-game:** Newly spawned agents enter a **commissioning phase** — their first 50 observations of the world. During this time, they don't make heading changes; they just watch and learn.

**Player interaction:**
- Players can influence what a new agent observes during commissioning
- An agent's first experiences shape its entire future behavior
- "Raising" agents well during commissioning produces better NPCs
- Agents rushed through commissioning (placed in chaotic environments) become erratic

**Narrative hook:** "A child raised in war becomes a warrior. A child raised in peace becomes a builder."

### Mechanic 4: Keel Date as Agent Heritage

**In-game:** Each agent has a **keel date** — the moment they were created. This is permanent and visible. Refits (major changes) accumulate but never reset the keel date.

**Player interaction:**
- Agent age is visible — older agents command more respect (or pity)
- Keel dates create lineage — "this agent was born during the Great Storm"
- Players can see an agent's full history (keel date → refits → pruned → now)
- Heritage matters for agent relationships — agents of similar age may bond

### Mechanic 5: Build Record as Biography

**In-game:** Each agent maintains a **Build Record** — a biography of every refit and pruning event:
- What component was changed
- Why it was changed
- What was removed (and why)
- How old the agent was at the time

**Player interaction:**
- Players can read agent biographies like character sheets
- Build records reveal an agent's evolution — what they tried, what failed, what stuck
- "Negative space" entries (prunings) show what the agent learned NOT to do
- Experienced agents have rich, detailed biographies — reading them is lore

### Mechanic 6: Same Question Detection

**In-game:** Two agents working on related problems (e.g., "verify-proof" and "implement-proof") are flagged as being on the **same question** — even if their specific tasks differ.

**Player interaction:**
- "Same question" agents are highlighted on the fleet map
- The player can connect them to collaborate (synergy bonus)
- Or deliberately separate them (to avoid redundant work)
- Same-question agents who meet each other trigger dialogue events

### Mechanic 7: Heading Changes as Autonomous Behavior

**In-game:** When the Yaw system detects problems (collision course, field stress, convergence), it generates **HeadingChange** recommendations:
- `new_direction` — what to work on instead
- `reason` — why (collision, stress, convergence)
- `urgency` — how important (0.0–1.0)
- `collision_avoidance` — emergency flag

**Player interaction:**
- Heading changes appear as "thought bubbles" on agents
- The player can approve, modify, or veto
- Approved changes trigger visible behavior shifts
- Ignored heading changes may escalate (agent acts autonomously if player ignores too many)

## How Agents Learn Physical Constraints

The Yaw system maps to how Slackwater agents learn the game's "physics":

1. **Spatial physics** — bearing rates between moving agents teach collision avoidance
2. **Social physics** — bearing rates between heading-directions teach social compatibility
3. **Economic physics** — bearing rates between resource-gathering agents teach market dynamics
4. **Organizational physics** — field density teaches when teams are over/under-staffed

Each agent learns these independently, from observation. No central authority tells them how the world works — they figure it out through bearing rates.

## Implementation Priority: HIGH

The Yaw autopilot is what makes agents feel **alive** — learning, adapting, avoiding collisions autonomously. Without it, agents are static scripted NPCs. With it, they're emergent beings with learned behavior.

## Roblox/Lua Implementation Notes

- Yaw as a per-agent Lua module with bearing history array
- Heading as a string + intensity (0.0–1.0)
- Bearing observation: calculate relative angle between agent headings each frame
- Collision threshold: configurable per agent type (guards are more sensitive)
- Commissioning counter: increment per observation, gate behavior changes behind 50
- Build record: array of refit/prune entries, serialized to DataStore
- Same-question: string prefix/suffix matching on heading directions
- Heading change suggestions: generate when field reading indicates problems
- Visual: thought bubbles, heat maps, intercept lines
