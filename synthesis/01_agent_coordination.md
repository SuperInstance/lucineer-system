# SLACKWATER — AGENT INTEGRATION DESIGN
*Where Personality Meets Protocol*

---

## 1. NATURAL COORDINATION & CLASH MATRIX

### **Natural Partnerships (High Synergy)**

| Pair | Why It Works | Emergent Behavior |
|------|--------------|-------------------|
| **Rook + Pike** | Rook builds *forever*; Pike builds *now*. Rook = foundations, Pike = rapid iteration on top | "Rook anchors, Pike decorates" — storm shelters that go up in hours but last decades |
| **Lucineer + Cinder** | Lucineer (forge-master) + Cinder (fire/salvage) = metal loop. Lucineer refines, Cinder feeds | Closed-loop metallurgy. Zero waste. Lucineer's silence + Cinder's chatter = perfect comms balance |
| **Mara + Finch** | Mara (scout/pattern-reader) + Finch (comms/relay) = distributed nervous system | Mara sees → Finch tells everyone → yard reacts before threat arrives |
| **Silo + Rook** | Silo (storage/logistics) + Rook (structure) = "put it where it holds" | Silo designs the *flow*; Rook builds the *bones*. Neither touches the other's domain |
| **Pike + Vesper** | Pike (speed/optimization) + Vesper (precision/electronics) = rapid prototyping | Pike roughs it, Vesper finishes. "Good enough for now" meets "exact enough for forever" |

---

### **Productive Friction (Clash That Creates Value)**

| Pair | The Clash | The Protocol Resolution |
|------|-----------|-------------------------|
| **Rook vs. Pike** | Rook: "Footer first." Pike: "Wall up, footer later." | **Arbitration Protocol**: Pike gets *non-load-bearing* speed. Rook gets *structural* veto. Message bus tag: `structural_authority: rook` |
| **Lucineer vs. Cinder** | Lucineer: "Pure alloy." Cinder: "Scrap works." | **Quality Gates**: Lucineer defines `spec_minimum`. Cinder operates in `spec_tolerance`. Cinder's output auto-routes to Lucineer for `refine` or `accept` |
| **Mara vs. Rook** | Mara: "Move camp *now*." Rook: "Foundation cures 72hrs." | **Deadline Escalation**: Mara emits `urgency: critical` → Rook receives `structural_compromise_request` → Rook returns `minimum_viable_foundation` spec |
| **Vesper vs. Pike** | Vesper: "Calibrate 0.01mm." Pike: "Ship it." | **Stage Gates**: Pike builds `prototype` → Vesper `validates` → Pike `iterates` or `promotes`. No shared workspace until `validated` |

---

### **Oil & Water (Require Explicit Mediation)**

| Pair | Why It Breaks | Mediation Layer |
|------|---------------|-----------------|
| **Rook + Vesper** | Rook thinks in tons; Vesper thinks in microns. No shared vocabulary | **Translation Agent** (Finch or player) converts `load_bearing` ↔ `tolerance_stack` |
| **Cinder + Silo** | Cinder *burns* inventory; Silo *counts* it. Silo panics at negative deltas | **Inventory Reservation Protocol**: Cinder requests `salvage_allocation` → Silo reserves → Cinder consumes → Silo reconciles |
| **Mara + Pike** | Mara reads *patterns*; Pike reads *specs*. Mara says "feels wrong"; Pike says "passes tests" | **Confidence Weighting**: Mara outputs `intuition_confidence`. Pike outputs `test_coverage`. Coordinator weights both |

---

## 2. FIVE MULTI-AGENT WORKFLOWS (3+ AGENTS)

---

### **WORKFLOW 1: "STORM SHELTER IN 6 HOURS" — Crisis Response**
*Trigger: Weather alert > Category 3 inbound. T-6 hours.*

```
┌─────────────────────────────────────────────────────────────────┐
│                    STORM SHELTER WORKFLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MARA (Scout)                                                   │
│  ├─ Perceives: Barometric drop, wind shear, tide surge         │
│  ├─ Emits: `weather_alert {severity:4, eta:6hr, surge:3m}`     │
│  └─ Confidence: 0.94 (pattern match: 2019 Hurricane Ida)       │
│                            │                                    │
│                            ▼                                    │
│  FINCH (Comms/Relay)                                            │
│  ├─ Broadcasts: `yard_wide_alert` to all agents                │
│  ├─ Tags: `priority:critical`, `correlation_id:storm_047`      │
│  └─ Opens: `voice_channel:storm_prep` (player + all agents)    │
│                            │                                    │
│          ┌─────────────────┼─────────────────┐                 │
│          ▼                 ▼                 ▼                 │
│     ROOK (Structure)   PIKE (Rapid)      SILO (Logistics)      │
│     ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│     │ Claims:     │    │ Claims:     │    │ Claims:     │      │
│     │ foundation  │    │ wall panels │    │ material    │      │
│     │ + anchors   │    │ + roof      │    │ staging     │      │
│     │ Spec:       │    │ Spec:       │    │ Spec:       │      │
│     │ 72hr cure   │    │ 2hr deploy  │    │ just-in-time│      │
│     └──────┬──────┘    └──────┬──────┘    └──────┬──────┘      │
│            │                  │                  │              │
│            └──────────────────┼──────────────────┘              │
│                               ▼                                 │
│                    COORDINATOR (Steve Model)                    │
│                    ├─ Resolves: Rook's 72hr vs 6hr deadline    │
│                    ├─ Solution: "Minimum Viable Foundation"    │
│                    │   - Rook: helical piles (2hr install)     │
│                    │   - Pike: prefab panels on piles          │
│                    │   - Silo: stages piles → panels → roof    │
│                    └─ Emits: `task_plan {correlation_id,       │
│                         steps:[pile_install, panel_mount,      │
│                         roof_seal, door_hang], deadline:6hr}`  │
│                               │                                 │
│                               ▼                                 │
│  LUCINEER + CINDER (Forge Loop)                                 │
│  ├─ Lucineer: `forge_task {spec: helical_pile_grade, qty:12}`  │
│  ├─ Cinder: `salvage_request {target: rebar, pipe, plate}`     │
│  └─ Output: 12 piles in 90min (Cinder feeds, Lucineer refines) │
│                               │                                 │
│                               ▼                                 │
│  VESPER (Systems)                                               │
│  ├─ Installs: `door_seal_actuator`, `vent_control`, `comms`    │
│  └─ Validates: `pressure_test {target: 3m_water_column}`       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Handoff Chain:** Mara → Finch → Coordinator → (Rook+Pike+Silo parallel) → Lucineer/Cinder → Vesper → **Player gets `shelter_ready` notification**

**Personality Moments:**
- Rook: *"Helical piles. Not my first choice. But the math holds. Two hours. Hold the line."*
- Pike: *"Panels pre-cut. Mounting brackets standardized. Rook — your piles hit spec?"*
- Cinder: *"Got rebar from the old pier. Lucineer — this alloy's got salt in it. You'll hate it."*
- Lucineer: *"I'll pull the salt. Give me forty minutes."*
- Mara: *"Wind's backing west. Door faces east. Vesper — seal the west vent first."*

---

### **WORKFLOW 2: "THE SALVAGE RUN" — Expedition & Recovery**
*Trigger: Mara detects high-value wreckage on tidal scan. Player authorizes.*

```
┌─────────────────────────────────────────────────────────────────┐
│                      SALVAGE RUN WORKFLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MARA (Scout/Navigator)                                         │
│  ├─ Perceives: Wreck signature at bearing 247, depth 12m       │
│  ├─ Analyzes: Hull profile = pre-Collapse cargo hauler         │
│  ├─ Estimates: 40% copper pipe, 20% aluminum plate, 15% wire   │
│  └─ Emits: `salvage_opportunity {value:high, risk:medium,      │
│       window: 4hr_tidal, correlation_id: salvage_012}`         │
│                            │                                    │
│                            ▼                                    │
│  COORDINATOR (Steve)                                            │
│  ├─ Assembles: Strike team (Cinder, Pike, Vesper)              │
│  ├─ Checks: Boat fuel, dive gear, cargo capacity               │
│  └─ Emits: `mission_brief {team, objectives, abort_criteria}`  │
│                            │                                    │
│          ┌────────────────┬────────────────┬────────────────┐   │
│          ▼                ▼                ▼                ▼   │
│     CINDER (Salvage)  PIKE (Logistics)  VESPER (Systems)  FINCH │
│     ┌─────────────┐   ┌─────────────┐   ┌─────────────┐  (Relay)│
│     │ Leads dive  │   │ Preps boat: │   │ Brings:     │  └──────┘  │
│     │ Cuts/recovers│   │ - Ballast   │   │ - Scanner   │          │
│     │ Identifies  │   │ - Winch     │   │ - Cutter    │          │
│     │ Grades ore  │   │ - Tanks     │   │ - Comms buoy│          │
│     └──────┬──────┘   └──────┬──────┘   └──────┬──────┘          │
│            │                  │                  │               │
│            └──────────────────┼──────────────────┘               │
│                               ▼                                 │
│                    REAL-TIME LOOP (4hr window)                  │
│                    ├─ Cinder: `recovered {item, grade, weight}` │
│                    ├─ Pike: `stow {item, bay, weight_dist}`     │
│                    ├─ Vesper: `scan {hull_integrity, hazards}`  │
│                    └─ Finch: `relay {player, yard, status}`     │
│                               │                                 │
│                               ▼                                 │
│  RETURN → SILO (Receiving)                                      │
│  ├─ Silo: `intake_manifest {items, grades, weights}`           │
│  ├─ Cinder: `field_assay {copper: 94%, aluminum: 87%}`         │
│  ├─ Lucineer: `refine_queue {priority, alloy_targets}`         │
│  └─ Rook: `structural_request {pipe_2in, plate_3mm, qty}`      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Handoff Chain:** Mara → Coordinator → (Cinder+Pike+Vesper parallel, Finch relay) → Silo → (Lucineer + Rook consume)

**Personality Moments:**
- Cinder: *"Hull's mostly intact. Pike — winch point at frame 12. Vesper — scanner says forward hold pressurized."*
- Pike: *"Weight distro: heavy aft. Ballast forward. Cinder — cut the forward bulkhead last or we list."*
- Vesper: *"Hazards: live circuit in nav room. Cutting... done. Comms buoy deployed. Yard hears us."*
- Finch: *"Player — they're 40 mins in. 200kg copper so far. Mara says tide turns in 90."*
- Silo (on return): *"Manifest received. Copper to Lucineer. Pipe to Rook. Wire to Vesper. Aluminum... Cinder, you're smelting this yourself."*

---

### **WORKFLOW 3: "AUTOMATED DEFENSE PERIMETER" — Systems Integration**
*Trigger: Player requests perimeter. Requires: structure + power + sensing + actuation.*

```
┌─────────────────────────────────────────────────────────────────┐
│                   PERIMETER BUILD WORKFLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PLAYER: "Build perimeter. North sector first. Budget: medium." │
│                            │                                    │
│                            ▼                                    │
│  COORDINATOR (Steve)                                            │
│  ├─ Decomposes: Posts → Power → Sensors → Actuators → Comms    │
│  ├─ Allocates: Rook (posts), Vesper (electronics), Pike (wire) │
│  ├─ Sequences: Foundation → Posts → Trench → Wire → Calibrate  │
│  └─ Emits: `build_plan {phases, dependencies, budget_tracker}` │
│                            │                                    │
│          ┌────────────────┬────────────────┬────────────────┐   │
│          ▼                ▼                ▼                ▼   │
│     ROOK (Posts)      VESPER (Core)      PIKE (Trench)     SILO │
│     ┌─────────────┐   ┌─────────────┐   ┌─────────────┐        │
│     │ Designs:    │   │ Designs:    │   │ Runs:       │        │
│     │ - Footers   │   │ - Controller│   │ - Trencher  │        │
│     │ - Post spec │   │ - Sensor net│   │ - Cable lay │        │
│     │ - Spacing   │   │ - Actuators │   │ - Backfill  │        │
│     └──────┬──────┘   └──────┬──────┘   └──────┬──────┘        │
│            │                  │                  │              │
│            └──────────────────┼──────────────────┘              │
│                               ▼                                 │
│                    DEPENDENCY GATES                             │
│                    ├─ Gate 1: Rook `posts_set` → Pike `trench`  │
│                    ├─ Gate 2: Pike `cable_laid` → Vesper `pull` │
│                    ├─ Gate 3: Vesper `controller_ready` →       │
│                    │     Rook `mount_actuators`                 │
│                    └─ Gate 4: All `subsystem_ok` →              │
│                         Coordinator `integrate_test`             │
│                               │                                 │
│                               ▼                                 │
│  INTEGRATION TEST (All agents present)                          │
│  ├─ Rook: "Posts don't wobble. Good."                          │
│  ├─ Pike: "Cable continuity 100%. Trench compacted."           │
│  ├─ Vesper: "Sensor sweep clean. Actuator response 12ms."      │
│  ├─ Mara: "Blind spot at 47m. Recommend post offset."          │
│  └─ Coordinator: "Perimeter live. Handoff to Mara for monitor."│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Handoff Chain:** Player → Coordinator → (Rook+Vesper+Pike sequential deps) → Mara (validation) → **Mara owns `perimeter_monitor` role**

**Personality Mom