# fleet-vessel → Lucineer Game Agent Cleanup Integration Plan

## Cleaning Up Stale Agent State

### Concept: The Custodian NPC
The fleet-vessel pattern maps perfectly to a "Custodian" or "Janitor" NPC that wanders the game world cleaning up debris, archiving old creations, and enforcing building codes. This is both a useful utility NPC and a visible game mechanic.

### Integration Architecture

```
Vessel Enforcement Cycle (= Custodian's daily patrol)
  ├── Disk Usage → "world is too cluttered" → clean old builds
  ├── Git Hygiene → "forbidden items in NPC inventory" → confiscate
  ├── Research Compress → "old creations archived" → summarize + store
  └── Research Delete → "ancient items removed" → full cleanup
```

### Phase 1: World Clutter Management
Map disk_usage_max to world entity limits:

| Vessel Spec | Game Equivalent |
|---|---|
| `disk_usage_max: 80` | Max 80% of region's part budget used |
| `rust_target_max_mb: 200` | Max 200 parts per NPC creation |
| `node_modules_in_git: forbidden` | No exploit/clutter items in NPC inventory |
| `log_files_in_git: forbidden` | No debug/error items visible to players |
| `.env_in_git: forbidden` | No private NPC data in public DataStores |

When clutter exceeds threshold:
- **Soft mode**: Custodian posts warning signs, NPCs get "messy workspace" debuff
- **Hard mode**: Custodian physically removes items, deletes oldest first

### Phase 2: Agent State Lifecycle
Map research compress/delete to NPC memory lifecycle:

```
NPC creates something (research session)
  → Active for 7 days (full detail available)
  → After 7 days: Custodian visits, creates "memory summary"
    → NPC can recall the gist but not full detail
  → After 30 days: Custodian removes entirely
    → NPC has forgotten this creation
    → Unless marked as "important" (exempted)
```

This creates a natural forgetting curve — NPCs remember recent interactions in detail, old ones only as summaries.

### Phase 3: Enforcement as Visible Game Mechanic

**The Custodian NPC:**
- Wanders the world on a schedule (daily/weekly based on `cleanup_schedule`)
- Visits each NPC's workspace/home/building
- Posts "violation notices" on doors (visible signs)
- Physically removes forbidden items (animation)
- Creates "archive boxes" for compressed memories
- Can be bribed, distracted, or given priority instructions by players

**Violation Types as Game Events:**
- "Too many parts!" → Custodian removes oldest decorations
- "Forbidden item detected!" → Custodian confiscates (confiscation chest)
- "Old work detected!" → Custodian archives (creates memory crystal)
- "Disk too full!" → Custodian declares emergency cleanup

### Phase 4: PLATO Integration → Conductor's Bulletin Board
- Enforcement actions posted to a "Town Bulletin" (visible to all NPCs)
- Specs are the "Town Charter" — rules the Custodian enforces
- NPCs can read the bulletin to know what was cleaned and why
- Players can read the bulletin to understand world rules

### Phase 5: Spec System as World Configuration
Port the vibed specs as in-game configuration:

```lua
WorldSpecs = {
  max_parts_per_zone = 2000,        -- disk_usage_max
  max_parts_per_creation = 200,     -- rust_target_max_mb
  forbidden_items_in_inventory = true, -- node_modules_in_git
  memory_compress_after_days = 7,
  memory_delete_after_days = 30,
  enforcement_level = "hard",       -- soft = warnings only
  cleanup_schedule = "daily",
}
```

The Mayor NPC (or player with mayor role) can edit these specs — changing world rules with visible consequences.

### Implementation Priority: LOW-MEDIUM
Useful for world management but not critical for MVP. More valuable when NPC count and world complexity grows.

### Key Code to Port
1. `get_dir_size()` → recursive part counter per NPC/zone
2. `enforce_git_patterns()` → inventory scanner for forbidden items
3. `compress_old_research()` → memory summarization for old NPC interactions
4. Spec system → world configuration with editable thresholds
