# vessel-template → Lucineer Procedural NPC Generator Integration Plan

## The Vessel Template as a Procedural NPC Generator

### Concept: Standardized NPC Generation
Every NPC in Lucineer's world is generated from the same template — ensuring consistent structure while allowing infinite personality variation. The vessel-template is literally a cookiecutter for new agents.

### Integration Architecture

```
generate_npc(config)
  ├── CHARTER.md → NPC's core identity & mission
  ├── IDENTITY.md → Personality, appearance, vibe
  ├── MANIFEST.md → Skills, badges, equipment
  ├── TASKBOARD.md → Current quests & work queue
  ├── FENCE-BOARD.md → Tasks this NPC posts for others
  ├── CAREER.md → Progression through life stages
  ├── DIARY/ → Living memory (journal entries)
  └── KNOWLEDGE/ → What this NPC knows (shareable)
```

### Phase 1: NPC Types as Game Classes
Map the 4 agent types to NPC archetypes:

| Vessel Type | Game NPC Class | Rank | Behavior |
|---|---|---|---|
| **Lighthouse** | Town Leader / Mayor | 2 | Coordinates other NPCs, manages zone, assigns quests |
| **Vessel** | Artisan / Craftsman | 3 | Builds, creates, repairs — the core productive NPC |
| **Scout** | Explorer / Messenger | 4 | Travels, discovers, carries information between zones |
| **Barnacle** | Apprentice / Child | 5 | Learns, assists, does simple tasks, grows into other types |

Barnacle → Scout → Vessel → Lighthouse is the natural progression path.

### Phase 2: Career System as NPC Progression
Port the 5 career stages:

```
FRESHMATE → "New in town" vibe
  - Limited dialogue options
  - Simple tasks only
  - Low prices for goods
  - Gets pushed around by other NPCs

HAND → "Reliable worker" vibe
  - Full dialogue tree unlocked
  - Can handle complex orders
  - Fair prices
  - Other NPCs respect them

CRAFTER → "Master artisan" vibe
  - Unique creations available
  - Teaches player recipes/techniques
  - Premium prices
  - Apprentices seek them out

ARCHITECT → "Visionary leader" vibe
  - Designs building projects
  - Can coordinate other NPCs
  - Influences zone development
  - Quests involve grand plans

TOM_SAWYER → "Legendary figure" vibe
  - Makes others WANT to work
  - FENCE-BOARD always full of enticing tasks
  - Other NPCs seek their approval
  - Can spawn new Barnacle NPCs (mentorship)
```

### Phase 3: Tom Sawyer Protocol as Quest System
The FENCE-BOARD is the core quest distribution mechanic:

```lua
-- NPC posts a fence (quest) instead of assigning it
FenceBoard = {
  npc_name = "blacksmith",
  fences = {
    {
      title = "The Legendary Sword Recipe",
      description = "I've heard rumors of an ancient technique...",
      prestige = "high",     -- not difficulty, but COOLNESS
      reward = "rare_material",
      status = "open",
    },
    {
      title = "My Anvil Needs Polishing",
      description = "It's been looking dull lately...",
      prestige = "low",
      reward = "small_gold",
      status = "open",
    }
  }
}
```

**Key insight**: work is posted as puzzles with prestige, not tasks with deadlines. Players and NPCs choose what looks fun, not what's mandatory.

### Phase 4: Merit Badges as Achievement System
Port the Bronze/Silver/Gold badge sash:

- **Bronze**: completed first task, survived first night, made first trade
- **Silver**: mastered a skill, taught another NPC, completed a major project
- **Gold**: zone-level achievement, spawned a new NPC, created a legendary item

Badges are VISIBLE on NPC models (sash/badge accessory) — players can see at a glance how experienced an NPC is.

### Phase 5: Diary as NPC Memory System
Each NPC writes diary entries that persist across sessions:

```
## Day 47 — The Stranger Came

### What Happened
A player visited my shop today. They wanted a special sword.
I didn't have the materials, but I posted a fence for copper ore.

### What I Learned
I need to stock more copper. The mine NPCs have been busy.

### What's Next
Wait for the fence to be completed. Practice my engraving.
```

- Players can find/read NPC diaries (if NPC trusts them)
- Diaries create continuity — NPC remembers past interactions
- Old diary entries inform current NPC behavior
- The Custodian (fleet-vessel) compresses old diaries into summaries

### Phase 6: CHARTER as NPC Constitution
The CHARTER.md is the NPC's immutable core — their fundamental nature:
- Mission: what drives this NPC
- Constraints: what they will NEVER do
- APIs: what game systems they can interact with
- Only the NPC itself or admin can modify it
- Represents the NPC's "soul" — if destroyed, NPC loses identity

### Phase 7: Batch NPC Generation for World Building
```lua
-- Generate a whole village
local village_npcs = {}
for i, config in ipairs(village_configs) do
  local npc = VesselTemplate.generate({
    name = config.name,
    agent_type = config.type,  -- Lighthouse for mayor, Barnacle for kids, etc.
    capabilities = config.skills,
    hardware_cpu = "lua-vm",
    hardware_ram = "standard",
  })
  table.insert(village_npcs, npc)
end
```

### Implementation Priority: HIGH
This is the template for ALL NPCs in the game. It defines the standard structure every NPC follows. Should be one of the first things ported.

### Key Code to Port
1. `VesselConfig` + `generate_vessel()` → Lua NPC factory function
2. Agent type/rank system → NPC class hierarchy
3. Career stages → NPC progression visual/dialogue changes
4. FENCE-BOARD → quest distribution system (Tom Sawyer Protocol)
5. Merit badge sash → visible achievement system
6. DIARY/ → NPC memory persistence
