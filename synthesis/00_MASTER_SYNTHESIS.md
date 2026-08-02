

# SLACKWATER — UNIFIED INTEGRATION PLAN v1.0
**Master Architect Synthesis**  
*Incorporating Cross-Reviews from 6 Models*

---

## 1. SYSTEM MAP — The Neural Yard
*How the 12+ subsystems connect into a single runtime loop.*

```text
[PLAYER INPUT] 
    │
    ├──(Voice/Text)──> [TINKERPAD INTERFACE] <──(Vibe-Coding Engine)── [LLM ROUTER]
    │                       │                         │
    │                       ▼                         ▼
    │               [AGENT ORCHESTRATOR]      [TECH TREE STATE]
    │                       │                         │
    │           ┌───────────┼───────────┐             │
    │           ▼           ▼           ▼             │
    │      [PERSONALITY] [SKILL]   [SAFETY]           │
    │      (Rook/Pike)   (Era 0-6) (Autonomy Slider)  │
    │           │           │           │             │
    │           └───────────┼───────────┘             │
    │                       ▼                         │
    │               [ACTION QUEUE]                    │
    │                       │                         │
    ▼                       ▼                         ▼
[WORLD PHYSICS] <── [RESOURCE MANAGER] <── [PERCEPTION SYSTEM]
    │                       │                         │
    │                       ▼                         │
    └──────────────── [GLOBAL EVENT BUS] ─────────────┘
            │               │               │
            ▼               ▼               ▼
      [Virality Clip]  [Scarcity Dialogue] [Era Unlock]
```

**Key Connections:**
1.  **TinkerPad ↔ LLM Router:** Translates natural language to era-appropriate instructions (Blueprints → Circuits → Code) per `05_vibe_code_eras.md`.
2.  **Agent Orchestrator ↔ Personality:** Assigns tasks based on synergy/clash matrix (`01_agent_coordination.md`).
3.  **Action Queue ↔ Safety:** Validates actions against griefing rules & autonomy slider (`06_autonomous_perception.md`).
4.  **Resource Manager ↔ Tech Tree:** Enforces bottleneck pacing & legacy cost penalties (`03_era_balance.md`).
5.  **Global Event Bus ↔ Virality:** Triggers recordable moments during conflicts or scarcity (`04_agent_viral_moments.md` + `02_scarcity_dialogue.md`).

---

## 2. INTEGRATION PRIORITIES
*What to wire first to ensure stability before complexity.*

1.  **Priority 1: The Core Loop (Era 0-1 + Resource Flow)**
    *   **Why:** Without a functional build/craft loop, agents have nothing to do.
    *   **Scope:** Implement Era 0 (Simple Machines) and Era 1 (Power Transmission) recipes. Wire the **Resource Manager** to enforce the `03` balance fixes (Bottleneck N+3, Legacy Cost Penalty).
    *   **Deliverable:** Player can gather stone/wood, craft a lever, and power a basic mill without agents.

2.  **Priority 2: Agent Personality & Conflict System**
    *   **Why:** This is the unique selling point. Agents must feel distinct before they feel smart.
    *   **Scope:** Implement **Rook** (Structure) and **Pike** (Speed). Wire the **Arbitration Protocol** (`structural_authority: rook`). Integrate the **Autonomy Slider** (`06`) so players can toggle between "Manual" and "Assisted."
    *   **Deliverable:** Player assigns a wall build; Rook and Pike argue via voice bubble; Rook wins load-bearing decisions.

3.  **Priority 3: Vibe-Coding Evolution & Era Progression**
    *   **Why:** This gates the long-term engagement (17-hour target).
    *   **Scope:** Build the **TinkerPad** interface to shift from Mechanical Blueprints (Era 0-1) to Circuit Diagrams (Era 2-3) to Code Blocks (Era 4+). Connect to **Tech Tree State**.
    *   **Deliverable:** Player unlocks Era 2; TinkerPad UI changes from gears to wires; agents unlock new skills.

---

## 3. CONFLICTS FOUND
*Where models disagreed and the Master Architect's resolution.*

| Conflict | Model A | Model B | Resolution |
| :--- | :--- | :--- | :--- |
| **Agent Roster** | `01` uses Rook, Pike, Lucineer, etc. (8 agents) | `Original` uses Role-based (Mechanic, Millwright, etc.) | **Hybrid Model:** Use `01` names for *personalities* (Rook = Mechanic, Lucineer = Millwright). Roles define *skills*, Names define *behavior*. |
| **Era Count** | `Original` lists 7 Eras (1-7) | `03` critiques pacing for 7 Eras (0-6) | **Standardize to 0-6:** 7 Total Eras. Adopt `03`'s timing (17 hours total) and bottleneck shifts (N+3). |
| **Coding Interface** | `05` suggests evolving UI (Blueprints → Code) | `06` implies standard API calls for agents | **Dynamic UI:** The *Player* sees evolving UI (`05`). The *Agents* use standardized API calls (`06`) backend. |
| **Scarcity Tone** | `02` suggests humorous/desperate dialogue | `04` suggests dramatic conflict (Rook vs. Vex) | **Contextual Tone:** Scarcity triggers `02` dialogue (internal stress). Conflict triggers `04` drama (external clash). |
| **Autonomy** | `06` suggests 4-level slider | `01` implies fixed protocols (Rook veto) | **Layered Control:** Slider controls *initiative*. Protocols control *validation*. (e.g., Full Autonomy still requires Rook veto on structure). |

---

## 4. THE 10 BIGGEST INSIGHTS
*Golden nuggets from the cross-model exchange.*

1.  **Friction is Content:** Agent arguments (Rook vs. Pike) are not bugs; they are shareable viral moments (`01` + `04`).
2.  **The Bottleneck Rule:** Bottleneck Resource N must only become common in Era N+3 to prevent early inflation (`03`).
3.  **Legacy Penalty:** Recipes from 2+ eras back cost +50% extra materials to prevent spamming old tech (`03`).
4.  **Vibe-Coding Evolution:** The coding interface must mature with the player (Blueprints → Circuits → Code) to avoid cognitive overload (`05`).
5.  **17-Hour Sweet Spot:** Total playtime for first clear should be ~17 hours. Adjust recipe costs by +55% to hit this (`03`).
6.  **Safety First:** Agents need an "Action Validation" layer to prevent griefing before execution (`06`).
7.  **Scarcity Voices:** Resource dry-ups should trigger specific character dialogue lines to maintain immersion (`02`).
8.  **Structural Veto:** Rook (Structure) must always have veto power over Pike (Speed) on load-bearing items (`01`).
9.  **Closed-Loop Metallurgy:** Lucineer + Cinder creates a zero-waste metal loop, teaching sustainability via mechanics (`01`).
10. **The Foreman Role:** A "Maren" type agent is needed to teach players without doing the work for them (`04`).

---

## 5. WHAT'S MISSING
*Systems nobody designed yet.*

1.  **Economy/Trading System:** How do players trade resources with NPCs or each other? (Scarcity implies trade, but no mechanism defined).
2.  **Persistence/Save Structure:** How is the 17-hour progress saved? (Session-based vs. Persistent World).
3.  **LLM Cost Routing:** `06` mentions API spikes, but no specific budget/caching strategy for the *player-facing* LLM calls (vibe-coding).
4.  **Multiplayer Sync:** How do agent states sync between multiple players in the same yard? (Who owns the agent?).
5.  **Disaster System:** `04` mentions rainstorms collapsing walls, but no systemic weather/disaster engine is defined.

---

## 6. THE 30-DAY BUILD PLAN
*Week by week, incorporating all insights.*

### **Week 1: The Foundation (Core Loop & Balance)**
*   **Goal:** Playable Era 0-1 with correct resource pacing.
*   **Tasks:**
    *   Implement Era 0-1 recipes with `03` balance tweaks (Cost +55%, Bottleneck N+3).
    *   Build **Resource Manager** with Legacy Penalty logic.
    *   Create **TinkerPad** v1 (Mechanical Blueprints).
    *   **Milestone:** Player can build a waterwheel that actually turns without agents.

### **Week 2: The Crew (Agents & Personality)**
*   **Goal:** Rook and Pike are alive, arguing, and building.
*   **Tasks:**
    *   Implement **Agent Orchestrator** with `01` Synergy/Clash Matrix.
    *   Code **Arbitration Protocol** (Rook Veto).
    *   Integrate `02` Scarcity Dialogue triggers.
    *   Build **Autonomy Slider** (Manual → Assisted).
    *   **Milestone:** Player assigns a wall; agents build it while arguing; player can override.

### **Week 3: The Evolution (Tech & Vibe-Coding)**
*   **Goal:** Progression to Era 3 with evolving interfaces.
*   **Tasks:**
    *   Expand **TinkerPad** to Era 2-3 (Circuit Diagrams).
    *   Connect **Tech Tree State** to Agent Skill Unlocks.
    *   Implement **Safety Validation** layer (`06`).
    *   Script **Viral Moment** #1 (Structural Dispute) for testing.
    *   **Milestone:** Player unlocks Electricity; agents can wire lights; interface changes.

### **Week 4: The Polish (Virality & Integration)**
*   **Goal