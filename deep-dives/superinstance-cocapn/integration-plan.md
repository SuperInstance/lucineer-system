# superinstance-cocapn — Slackwater Integration Plan

## Core Game Mechanic: "The Conductor's Console"

The Cocapn becomes the **Conductor** — the game's central AI that manages the fleet of agents the player interacts with. The player sees the Conductor's console, a bird's-eye view of the entire agent fleet.

### Mechanic 1: Conservation as Resource System (γ + η = C)

**In-game:** Every agent has two visible bars:
- **γ (Gamma)** — Active Commitment (how much work they're doing right now)
- **η (Eta)** — Latent Capacity (how much headroom they have)

The sum is always C — the agent's total "energy budget." When you assign a task, γ goes up and η goes down. When the task completes, the energy flows back.

**Player interaction:** The player manages the fleet's energy distribution. Overcommit agents (high γ) and they become stressed, error-prone, eventually burn out. Undercommit them (high η) and they're idle, bored, losing skills. The sweet spot is balance.

**Visual:** A fleet dashboard showing each agent's γ/η ratio as a dual-bar meter. The fleet total shows whether the whole system is in conservation.

### Mechanic 2: Intelligent Work Routing

**In-game:** When events occur in the game world (a build request, a threat, a discovery), the Conductor routes the task to the best agent automatically — unless the player overrides.

**Routing factors:**
- **Capability hints** — only agents with matching skills are candidates
- **Least-loaded** — prefer agents with capacity
- **Health** — Degraded agents work slower; Down agents are skipped
- **Specialization** — agents with matching metadata get priority

**Player interaction:** The player can override routing decisions, manually assign tasks, or set routing policies. This is the strategic layer — like Football Manager for AI agents.

### Mechanic 3: Fleet Rebalancing Events

**In-game:** When load skew gets too severe (some agents overwhelmed, others idle), the Conductor triggers a **Rebalance Event** — a visible game event where agents reshuffle their responsibilities.

**Player interaction:** The player sees the rebalance recommendation and can approve, modify, or reject it. Rebalancing may trigger dramatic narrative events — an overwhelmed agent might quit, a bored agent might invent a new skill.

### Mechanic 4: Bottle Messages

**In-game:** All agent communication uses **bottles** — visible message containers that flow through the game world. Players can intercept, read, redirect, or forge bottles.

**Bottle types as game items:**
- `InspectRequest` → "Status Report" bottle — reveals fleet state
- `Heartbeat` → "Postcard" bottle — agent check-in
- `RouteRequest` → "Job Posting" bottle — new task assignment
- `RebalanceCommand` → "Reshuffle Order" bottle — fleet reorganization

**Player interaction:** Bottles travel physically through the game world (washed ashore, carried by couriers, found in wrecks). The player collects and deploys bottles strategically.

### Mechanic 5: Heartbeat Health System

**In-game:** Agents periodically send heartbeats. If heartbeats stop, the agent is marked Down. The player must maintain heartbeat infrastructure (communication relays) to keep the fleet healthy.

**Visual:** Heartbeat pulses on the fleet map — green (Healthy), yellow (Degraded), red (Down), gray (Deregistered).

### Mechanic 6: "First Among Equals" Narrative

**In-game:** The Conductor is not a god — it's a character. It can be damaged, go offline, be replaced. When the Conductor is down, agents lose fleet-level coordination but keep their local autonomy. This creates dramatic gameplay moments.

**Narrative hook:** "The fleet doesn't need a boss. It needs a captain — someone who watches the whole ocean while every ship navigates its own waters."

## Implementation Priority: CRITICAL

The Cocapn is the **central game system** — it manages every NPC, every task, every resource. It should be implemented first after the communication protocol (Plato).

## Roblox/Lua Implementation Notes

- Model ShipState as a Lua table with γ, η, health, load, capacity
- Fleet registry as a key-value store (attribute or DataStore)
- Routing algorithm: filter by capability → sort by load → pick first
- Rebalancing: periodic check with threshold-based trigger
- Bottle messages as serialized JSON with type discriminators
- Heartbeat: per-frame update with timeout tracking
