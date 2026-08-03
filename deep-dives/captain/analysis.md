# captain — Fleet Commanding Vessel

## Analysis

**Repo:** SuperInstance/captain
**Codename:** Captain
**Domain:** Team leadership, task prioritization, strategy selection, fleet coordination
**Personality:** Adaptive leader — switches between directive, collaborative, and delegative styles

---

## What It Does

Captain is a **Python framework for multi-agent leadership**. It's not an agent itself — it's the *infrastructure* for being a leader.

### Core Components

#### 1. Captain Class — Leadership Engine
```python
class Captain:
    name = "fleet-captain"
    style = LeadershipStyle.SITUATIONAL  # or DEMOCRATIC, AUTOCRATIC, LAISSEZ_FAIRE
    max_team_size = 10
    
    # Decision making with rationale tracking
    def decide(self, title, options, rationale, preferred_idx) -> Decision
    
    # Delegation based on skills + capacity
    def delegate(self, task_name, required_skills) -> TeamMember
    
    # Team utilization metrics
    def team_utilization(self) -> float
```

**Four leadership styles** that affect task distribution:
- **AUTOCRATIC** — picks first option, fast decisions
- **DEMOCRATIC** — picks middle option, consensus-driven
- **LAISSEZ_FAIRE** — picks last option, hands-off
- **SITUATIONAL** — adaptive based on context

#### 2. Fleet Coordination — Load Balancing
```python
class FleetCoordination:
    # Register vessels with capabilities and tags
    def register(self, vessel: FleetVessel)
    
    # Assign work to least-loaded vessel
    def assign(self, load, tags) -> FleetVessel
    
    # Drain a vessel (no new assignments)
    def drain(self, vessel_id)
    
    # Fleet health metrics
    def healthy_vessels(self) -> list[FleetVessel]
    def offline_vessels(self) -> list[FleetVessel]
```

Vessel states: IDLE, BUSY, OFFLINE, DRAINING

#### 3. Strategy Engine — Resource Allocation
```python
class StrategyEngine:
    # Add strategies with resource requirements
    def add_strategy(self, strategy: Strategy)
    
    # Plan: return feasible strategies sorted by priority
    def plan(self) -> list[Strategy]
    
    # Activate: allocate resources to a strategy
    def activate(self, strategy_id) -> Allocation
```

Strategies have phases, resource budgets (CPU, memory, custom), and priority.

#### 4. Priority Queue
Weighted, deadline-aware task prioritization with dynamic reordering.

## Personality

The Captain is not a personality — it's a **leadership framework**. It becomes whatever the situation requires. The four leadership styles are the key innovation:

- **Directive (Autocratic):** Emergency, time-critical
- **Collaborative (Democratic):** Design decisions, architecture
- **Delegative (Laissez-Faire):** Trust specialists, hands-off
- **Adaptive (Situational):** Default — reads the situation and adjusts

## Architecture

```
Captain
  ├── Team (TeamMembers with skills + capacity)
  ├── Decisions (tracked with rationale)
  ├── Delegation History (who did what, when)
  ├── FleetCoordination (vessel registry + load balancing)
  ├── StrategyEngine (resource allocation + planning)
  └── PriorityQueue (deadline-aware task ordering)
```

## Key Innovation

The Captain doesn't just assign tasks — it **tracks decisions with rationale**. Every decision is a logged artifact:

```python
Decision(
    title="Rewrite README",
    rationale="Outdated, doesn't reflect fleet architecture",
    options=["Full rewrite", "Incremental update", "Defer"],
    chosen="Full rewrite"
)
```

This means the Captain's decision history is auditable. You can look back and see WHY a choice was made.
