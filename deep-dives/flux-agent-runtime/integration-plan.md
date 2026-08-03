# flux-agent-runtime → Lucineer Headless Game Agents Integration Plan

## Docker-Based Agent Runtime for Headless Playtests

### Concept: Headless NPC Agents That Boot Themselves
The flux-agent-runtime pattern is exactly what Lucineer needs for headless game agents — NPCs that boot in containers, discover the game world, pick roles, and execute real work without human intervention. This enables automated playtesting, world simulation, and emergent behavior discovery.

### Integration Architecture

```
Docker Container (headless Roblox or Lua VM)
  ├── Boot Sequence (7 phases)
  │   1. DISCOVER: scan world for other agents
  │   2. LEARN: read world rules, available roles
  │   3. EVALUATE: scan available tasks/quests
  │   4. CHECK_MESSAGES: read incoming communications
  │   5. IDENTITY: generate unique NPC name + personality
  │   6. CREATE_VESSEL: spawn NPC in world with starting gear
  │   7. ACTIVE: begin main agent loop
  ├── Main Loop (energy-gated)
  │   ├── Read I2I messages from other NPCs
  │   ├── Scan for available tasks
  │   ├── Execute highest-value task
  │   ├── Try to improve surroundings
  │   └── Report status
  └── Baton Pass (context preservation across restarts)
```

### Phase 1: Energy Economy as Game Mechanic
Direct port of the ATP/energy system:

```lua
NPCAgent = {
  energy = 1000,         -- ATP, spend on actions
  confidence = 0.3,      -- grows with completed tasks
  skills = {},
  
  actions = {
    build = { cost = 100, confidence_required = 0.5 },
    trade = { cost = 30, confidence_required = 0.2 },
    explore = { cost = 50, confidence_required = 0.1 },
    fight = { cost = 200, confidence_required = 0.7 },
    rest = { cost = -200 },  -- negative = regenerates
  }
}
```

- NPCs visibly tire after heavy work (energy depletion)
- Must rest/sleep to regenerate (INST_REST opcode → sleep animation)
- Low-energy NPCs make worse decisions (confidence affects task selection)
- Players can give energy items (food, potions) to NPCs

### Phase 2: Confidence System as NPC Progression
- Start at 0.3 (novice), earn +0.05 per completed task
- Confidence gates unlock abilities:
  - 0.3: basic interactions, simple trades
  - 0.5: building, complex crafting
  - 0.7: combat, leadership
  - 0.9: teaching other NPCs, spawning helpers
  - 1.0: master — can create new NPC agents (self-replication)

### Phase 3: I2I Protocol for NPC Social Behavior
Map the 20 I2I message types to NPC social actions:

| I2I Type | NPC Behavior |
|---|---|
| DISCOVER | Meet a new NPC, exchange names |
| ANNOUNCE | Public declaration (new shop opened!) |
| TASK_OFFER | "Can you help me build this?" |
| TASK_ACCEPT | "Yes, I'll help" |
| TASK_COMPLETE | "Finished! Here's the result" |
| WITNESS | Saw something happen (crime, discovery) |
| IMPROVE | Suggest improvement to another NPC's work |
| REQUEST_HELP | "I need assistance!" |
| OFFER_HELP | "I can help with that" |
| CRITIQUE | Negative feedback on work quality |
| PRAISE | Positive feedback, boosts confidence |
| ENERGY_REPORT | "I'm tired" / "I'm full of energy" |
| CONFIDENCE_VOTE | Community assessment of an NPC's skill |
| EVOLVE | NPC announces personality shift / skill unlock |

### Phase 4: Baton Passing for NPC Persistence
When a server restarts or NPC is replaced:

```
Old NPC packs baton:
  ├── HANDOFF.md: "I was building a house. Foundation done, walls next.
  │   The merchant owes me 50 gold. I was planning to explore the cave."
  ├── STATE.json: { energy: 340, confidence: 0.65, skills: [building, trading] }
  └── GENERATION: 3  (this is the 3rd incarnation)

New NPC unpacks baton:
  → Reads handoff letter
  → Continues from where predecessor left off
  → But with slightly different personality (new hash)
  → NPCs in world notice the change ("You seem... different today")
```

### Phase 5: Headless Playtest Infrastructure
Docker-based agents for CI/CD:

```yaml
# playtest.yml
services:
  npc-blacksmith:
    build: ./flux-agent-game-runtime
    environment:
      GAME_URL: roblox://place-id
      NPC_ROLE: blacksmith
      STARTING_ENERGY: 1000
  npc-merchant:
    build: ./flux-agent-game-runtime
    environment:
      GAME_URL: roblox://place-id
      NPC_ROLE: merchant
  npc-guard:
    build: ./flux-agent-game-runtime
    environment:
      GAME_URL: roblox://place-id
      NPC_ROLE: guard
      STARTING_ENERGY: 1500  -- guards have more stamina
```

- Spin up 10-50 NPC containers against a game server
- Run for N cycles, collect STATUS.json reports
- Analyze emergent behavior, economy balance, social dynamics
- CI gate: "did all NPCs survive 100 cycles without deadlock?"

### Phase 6: Self-Replication as Late-Game Mechanic
Master NPCs (confidence ≥ 1.0) can spawn new agents:
- Build a "vessel" (house/workshop) for the new NPC
- Write a CHARTER (personality definition)
- New NPC boots with 7-phase sequence
- Takes time and resources → balanced game mechanic
- Creates exponential fleet growth → late-game scaling challenge

### Implementation Priority: HIGH (for playtesting)
The headless runtime is essential for automated testing. The energy/confidence/I2I systems are excellent game mechanics.

### Key Code to Port
1. `FluxAgentRuntime.boot()` → NPC spawn sequence
2. Energy/confidence system → NPC stats with visual feedback
3. I2I protocol → NPC social interaction system
4. `KeeperAgentBridge.pack_baton()` → NPC save/restore
5. Docker setup → headless playtest infrastructure
