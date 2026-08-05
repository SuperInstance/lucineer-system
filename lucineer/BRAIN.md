# Lucineer Brain — Build Intelligence Architecture

> How Lucy turns "build me a medieval village with a market square" into concrete parts in Roblox.

This doc is the implementation-level brain spec. It sits under [GRAND_PLAN.md](GRAND_PLAN.md) and [ARCHITECTURE.md](ARCHITECTURE.md) and answers five concrete questions:

1. How does Lucineer decompose complex requests into concrete part placements?
2. What is the template/primitive system — what are the atomic building blocks?
3. How does procedural generation work for things like "make it look rusty" or "add some wreckage"?
4. How should the skill library store and retrieve build patterns?
5. What is the reasoning chain: parse intent → check memory → recall skills → plan → generate commands → verify?

---

## 1. Brain Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Personality Filter (CHARACTER.md)                          │
│  ── voice, opinions, bond level, relationship memory        │
├─────────────────────────────────────────────────────────────┤
│  Reasoning Core                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌───────────────────────┐  │
│  │ Intent Parse│ │ Planner     │ │ Verifier              │  │
│  │             │ │             │ │                       │  │
│  └─────────────┘ └─────────────┘ └───────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Memory Layer                                               │
│  ├─ Episodic   memory/YYYY-MM-DD.md                         │
│  ├─ Semantic   MEMORY.md                                    │
│  ├─ Procedural skills/**/*.luau                             │
│  └─ Project    projects/*.json                              │
├─────────────────────────────────────────────────────────────┤
│  Skill Library                                              │
│  ├─ Vectorize index  (semantic search)                      │
│  ├─ D1 skills table  (metadata, stats)                      │
│  └─ R2 scripts/      (skill source)                         │
├─────────────────────────────────────────────────────────────┤
│  World Perception                                           │
│  ├─ Player state (position, look vector)                    │
│  ├─ Nearby instances (bounding boxes, materials)            │
│  ├─ Terrain heightmap (sampled grid)                        │
│  └─ Active project manifest                                 │
├─────────────────────────────────────────────────────────────┤
│  Execution Bridge                                           │
│  ├─ Hot path: JSON command array → Worker → Roblox          │
│  └─ Cold path: Luau modules → Argon → Studio                │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Decomposition: From Sentence to Parts

### 2.1 Intent Parse

Player says: **"build me a medieval village with a market square"**

The parser (LLM with structured output) produces:

```json
{
  "intent": "build",
  "structure": "village",
  "style": "medieval",
  "features": ["market_square"],
  "size": "medium",
  "location": {
    "type": "relative_to_player",
    "offset": { "x": 0, "y": 0, "z": -30 },
    "facing": "player_look_direction"
  },
  "constraints": {
    "terrain": "flat_or_gentle",
    "material_theme": ["stone", "wood", "thatch"]
  },
  "counts": {
    "houses": { "min": 3, "max": 5 },
    "market_stalls": { "min": 2, "max": 4 },
    "well": 1,
    "roads": true,
    "lighting": true
  }
}
```

### 2.2 Spatial Grammar

Lucy thinks in a small grammar of spatial concepts:

| Concept | Meaning | Example |
|---------|---------|---------|
| `Anchor` | Origin point for the whole build | Player position + 30 studs forward |
| `Envelope` | Bounding box of the whole build | 120×60 studs |
| `Parcel` | Sub-region assigned to one feature | Market square parcel, housing parcel |
| `Structure` | A discrete thing that gets built | House, well, stall |
| `Connective` | Roads, paths, fences, pipes | Cobblestone road between parcels |
| `Detail` | Props, lights, wear, clutter | Lantern, barrel, rust patch |

### 2.3 Build Manifest

The planner turns the intent into a manifest:

```json
{
  "projectId": "proj_medieval_village_001",
  "name": "Medieval Village",
  "root": { "x": 120, "y": 5, "z": -80 },
  "bounds": { "x": 120, "z": 90 },
  "style": "medieval",
  "status": "in_progress",
  "steps": [
    {
      "stepId": "layout",
      "description": "Reserve market square and housing parcels",
      "status": "pending",
      "skillHint": "site-layout-grid"
    },
    {
      "stepId": "market_square",
      "description": "Central plaza with well and stalls",
      "status": "pending",
      "substeps": [
        { "type": "well", "skill": "well-stone", "origin": { "x": 120, "y": 5, "z": -80 } },
        { "type": "market_stall", "skill": "market-stall-wooden", "origin": { "x": 110, "y": 5, "z": -75 }, "variant": 1 },
        { "type": "market_stall", "skill": "market-stall-wooden", "origin": { "x": 130, "y": 5, "z": -75 }, "variant": 2 }
      ]
    },
    {
      "stepId": "houses",
      "description": "Stone cottages around the square",
      "status": "pending",
      "substeps": [
        { "type": "house", "skill": "house-stone-cottage", "origin": { "x": 100, "y": 5, "z": -95 }, "facing": "south" },
        { "type": "house", "skill": "house-stone-cottage", "origin": { "x": 120, "y": 5, "z": -100 }, "facing": "south", "height": 1.2 },
        { "type": "house", "skill": "house-stone-cottage", "origin": { "x": 140, "y": 5, "z": -95 }, "facing": "south" }
      ]
    },
    {
      "stepId": "roads",
      "description": "Cobblestone paths connecting parcels",
      "status": "pending",
      "skill": "road-cobblestone"
    },
    {
      "stepId": "lighting",
      "description": "Lantern posts along roads",
      "status": "pending",
      "skill": "lantern-post-iron"
    },
    {
      "stepId": "weathering",
      "description": "Apply rust, moss, and wear to make it lived-in",
      "status": "pending",
      "filters": ["rustify", "mossify", "scatter-debris"]
    }
  ],
  "palette": ["Cobblestone", "Slate", "WoodPlanks", "Brick"],
  "createdAt": "2026-08-02T04:00:00Z"
}
```

The manifest is stored in D1 + `lucineer/projects/medieval-village.json`. It makes the build resumable across sessions.

---

## 3. Primitive / Template System

### 3.1 Atomic Primitives

The smallest units Lucy can place:

| Primitive | Roblox Class | Params |
|-----------|--------------|--------|
| `Block` | `Part` | size, position, material, color, anchored |
| `Wedge` | `WedgePart` | size, cframe, material, color |
| `CornerWedge` | `CornerWedgePart` | size, cframe |
| `Cylinder` | `Part` with `Shape = Cylinder` | size, position |
| `Ball` | `Part` with `Shape = Ball` | size, position |
| `Truss` | `TrussPart` | size, position |
| `Mesh` | `MeshPart` | meshId, size, cframe |
| `Decal` | `Decal` | texture, face, parent |
| `Texture` | `Texture` | texture, face, parent, stud per tile |
| `PointLight` | `PointLight` | brightness, range, color, parent |
| `SpotLight` | `SpotLight` | angle, brightness, range, parent |
| `Particle` | `ParticleEmitter` | texture, rate, lifetime, speed, parent |
| `Sound` | `Sound` | soundId, volume, looped, parent |
| `Constraint` | `Weld`/`HingeConstraint`/etc | part0, part1, cframe |

### 3.2 Material Palette

A curated palette keeps builds coherent. Lucy defaults to these unless the player overrides:

```json
{
  "stone": ["Cobblestone", "Slate", "Granite", "Concrete", "Brick"],
  "wood": ["WoodPlanks", "Wood", "PineWood"],
  "metal": ["CorrodedMetal", "DiamondPlate", "Metal", "Foil"],
  "scrap": ["CorrodedMetal", "Concrete", "Slate"],
  "roof": ["WoodPlanks", "Slate", "Brick"],
  "glass": ["Glass", "Neon"]
}
```

For Magnus's scrap/industrial aesthetic, Lucy also carries:

```json
{
  "rust": { "material": "CorrodedMetal", "color": { "r": 120, "g": 55, "b": 35 } },
  "patina": { "material": "Metal", "color": { "r": 60, "g": 100, "b": 90 } },
  "worn_wood": { "material": "WoodPlanks", "color": { "r": 110, "g": 80, "b": 50 } }
}
```

### 3.3 Templates

A template is a parameterized reusable command bundle. It lives as a Luau function that returns a list of commands.

Example: `lucineer/skills/architecture/wall-section.luau`

```lua
local function WallSection(origin, params)
    params = params or {}
    local width = params.width or 12
    local height = params.height or 8
    local thickness = params.thickness or 1
    local material = params.material or "Cobblestone"
    local color = params.color or { r = 163, g = 162, b = 165 }

    local cmds = {}

    -- Foundation
    table.insert(cmds, {
        type = "createPart",
        params = {
            name = "WallFoundation",
            shape = "Block",
            size = { x = width, y = 1, z = thickness + 1 },
            position = { x = origin.x, y = origin.y + 0.5, z = origin.z },
            material = material,
            color = color,
            anchored = true,
        }
    })

    -- Wall segments
    for y = 2, height, 2 do
        table.insert(cmds, {
            type = "createPart",
            params = {
                name = "WallSegment_" .. y,
                shape = "Block",
                size = { x = width, y = 2, z = thickness },
                position = { x = origin.x, y = origin.y + y, z = origin.z },
                material = material,
                color = color,
                anchored = true,
            }
        })
    end

    return cmds
end

return WallSection
```

Roblox-side `CommandExecutor` never sees templates directly. It sees the expanded commands.

---

## 4. Procedural Generation

Lucy uses **seeded deterministic filters** that take a command array and return a modified array. This separates "what to build" from "how it looks."

### 4.1 Filter Pipeline

```
Base commands  →  Style filter  →  Weathering filter  →  Detail filter  →  Lighting filter  →  Final commands
```

### 4.2 Filter Examples

#### Rustify

```lua
local function Rustify(commands, intensity)
    intensity = intensity or 0.3
    local seeded = Random.new(commands.seed or 42)
    local out = {}

    for _, cmd in ipairs(commands) do
        table.insert(out, cmd)

        if cmd.type == "createPart" then
            local mat = cmd.params.material
            if mat == "Metal" or mat == "DiamondPlate" or mat == "Foil" then
                if seeded:NextNumber() < intensity then
                    cmd.params.material = "CorrodedMetal"
                    cmd.params.color = { r = 120, g = 55, b = 35 }
                end
            elseif mat == "Stone" or mat == "Cobblestone" then
                if seeded:NextNumber() < intensity * 0.5 then
                    -- Add rust decal
                    table.insert(out, {
                        type = "createDecal",
                        params = {
                            parent = cmd.params.name,
                            face = "Front",
                            texture = "rbxassetid://RUST_TEXTURE_ID",
                            color = { r = 120, g = 55, b = 35 },
                            transparency = 0.7,
                        }
                    })
                end
            end
        end
    end

    return out
end
```

#### Scatter Debris / Wreckage

```lua
local function ScatterDebris(commands, region, count, seed)
    local seeded = Random.new(seed)
    local debris = {"Block", "Cylinder", "Wedge"}

    for i = 1, count do
        local dx = seeded:NextNumber(-region.width/2, region.width/2)
        local dz = seeded:NextNumber(-region.depth/2, region.depth/2)
        local size = seeded:NextNumber(0.5, 2)

        table.insert(commands, {
            type = "createPart",
            params = {
                name = "Debris_" .. i,
                shape = debris[seeded:NextInteger(1, #debris)],
                size = { x = size, y = size * 0.5, z = size },
                position = {
                    x = region.center.x + dx,
                    y = region.center.y + size * 0.25,
                    z = region.center.z + dz,
                },
                material = "CorrodedMetal",
                color = { r = 80, g = 70, b = 65 },
                rotation = {
                    x = seeded:NextNumber(-20, 20),
                    y = seeded:NextNumber(0, 360),
                    z = seeded:NextNumber(-20, 20),
                },
                anchored = true,
            }
        })
    end

    return commands
end
```

#### Mossify

- Add greenish decals to lower stone parts.
- Tint some blocks darker / greener.

#### Weathering

- Jitter each part's color by ±8%.
- Jitter size by ±3%.
- Slightly offset position by ±0.2 studs.

### 4.3 How Lucy Decides Filters

When the player says:

- "make it look rusty" → apply `rustify 0.4`
- "add some wreckage" → apply `scatter-debris 8`
- "old and abandoned" → apply `weathering 0.5`, `rustify 0.3`, `mossify 0.3`, `scatter-debris 12`
- "Magnus style" (scrap/industrial) → default to `rustify 0.25`, exposed beams, corrugated metal

The filter list is part of the planner output.

---

## 5. Skill Library

### 5.1 Skill Record

```json
{
  "id": "skill_arch_house_stone_cottage_001",
  "name": "Stone Cottage",
  "description": "Small medieval stone cottage with pitched roof, door, and chimney. Good for villages and rural scenes.",
  "category": "architecture/house",
  "tags": ["medieval", "stone", "house", "cottage", "village"],
  "scriptPath": "lucineer/skills/architecture/house-stone-cottage.luau",
  "params": [
    { "name": "width", "type": "number", "default": 12 },
    { "name": "depth", "type": "number", "default": 10 },
    { "name": "height", "type": "number", "default": 8 },
    { "name": "material", "type": "string", "default": "Cobblestone" },
    { "name": "roofMaterial", "type": "string", "default": "WoodPlanks" },
    { "name": "facing", "type": "string", "default": "south" }
  ],
  "composableWith": [
    "skill_arch_wall_stone_001",
    "skill_arch_roof_pitched_001",
    "skill_infra_road_cobblestone_001",
    "skill_deco_lantern_iron_001"
  ],
  "embeddingId": "vec_abc123",
  "createdAt": "2026-08-01T00:00:00Z",
  "useCount": 7,
  "successRate": 0.92,
  "source": "manual"
}
```

### 5.2 Storage

| Layer | What | Why |
|-------|------|-----|
| R2 | `lucineer-scripts/skills/{category}/{skill}.luau` | Source of truth for skill code |
| D1 | `skills` table | Metadata, stats, relationships |
| Vectorize | `lucineer-skills-index` | Semantic search by natural language |
| Local workspace | `lucineer/skills/**/*.luau` | Fast iteration + Argon sync |

### 5.3 Retrieval Flow

```
Player request → embed → Vectorize top-K (e.g. 10)
                    ↓
            Rerank by:
              - category match
              - success rate > 0.5
              - use count
              - composability with already-selected skills
              - player style preference
                    ↓
            Return top-N (e.g. 5)
```

### 5.4 Composition

Skills are just Luau functions returning command arrays. A higher-level skill calls lower-level ones:

```lua
-- Stone cottage calls wall, roof, door, window skills
local Wall = require(script.Parent.wall-section)
local Roof = require(script.Parent.roof-pitched)
local Door = require(script.Parent.door-wooden)

local function StoneCottage(origin, params)
    local cmds = {}

    -- Foundation
    table.insert(cmds, Wall({x=origin.x, y=origin.y, z=origin.z - params.depth/2}, {width=params.width, height=params.height}))
    -- ... other walls ...
    table.insert(cmds, Roof(origin, {width=params.width, depth=params.depth}))
    table.insert(cmds, Door(...))

    return cmds
end
```

Composition mirrors Magnus's tile programming: snap skills together → get complex builds.

### 5.5 Auto-Skill Creation

After a successful novel build:

1. Collect the command sequence.
2. Parameterize obvious variables (dimensions, positions, materials).
3. Ask LLM: "Turn these commands into a reusable Luau function named X with params Y."
4. Generate description + tags.
5. Embed and store.
6. Next similar request retrieves instead of regenerates.

---

## 6. Reasoning Chain

### 6.1 Full Chain

```
1. RECEIVE
   Input: { message, playerState, worldSnapshot }

2. LOAD CONTEXT
   - player profile (lucineer/players/{name}/profile.json)
   - active project manifest (if any)
   - MEMORY.md highlights
   - recent daily memory
   - bond level

3. PARSE INTENT
   Output: structured intent JSON (type, structure, style, features, size, location)

4. CHECK MEMORY
   - "Has this player built a village before?"
   - "What's their preferred style?"
   - "Is there an active project to continue?"

5. RECALL SKILLS
   - Embed intent
   - Vectorize search
   - Rerank and select skill set

6. PLAN
   - Decide Anchor (where)
   - Divide Envelope into Parcels
   - Assign skill or generator to each Parcel/Structure
   - Order steps: layout → structures → connectives → details → filters
   - Create/update build manifest

7. GENERATE COMMANDS
   For each step:
     - If skill exists: call skill function → commands
     - If not: LLM generate commands from intent + primitives
   Apply style filters (rust, weathering, debris, etc.)

8. VERIFY
   - Collision check against nearby instances
   - Bounds check (not floating, not underground)
   - Budget check (command count under limit)
   - Material/enum validity
   - If fail → adjust or ask player

9. PACKAGE
   - Reply: narrate what Lucy is doing in character
   - commands[] array
   - manifest update

10. EXECUTE + OBSERVE
    - POST to Worker callback
    - Roblox executes with progress callbacks
    - On completion: update skill stats, write daily memory, update player profile
```

### 6.2 Data Structures at Each Stage

#### Intent JSON

```json
{
  "intent": "build | modify | style | undo | chat",
  "target": "village",
  "style": "medieval",
  "features": ["market_square", "well"],
  "size": "medium",
  "location": { "type": "relative_to_player", "offset": {...} },
  "filters": ["rustify:0.3"],
  "tone": "casual"
}
```

#### Plan JSON

```json
{
  "projectId": "...",
  "anchor": { "x": 120, "y": 5, "z": -80 },
  "envelope": { "width": 120, "depth": 90 },
  "parcels": [
    { "id": "market", "type": "plaza", "bounds": {...}, "contents": [...] },
    { "id": "housing_north", "type": "housing", "bounds": {...}, "contents": [...] }
  ],
  "executionOrder": ["layout", "market", "housing", "roads", "lighting", "weathering"],
  "estimatedCommands": 340
}
```

#### Command Array

```json
[
  { "type": "createPart", "params": { ... } },
  { "type": "createModel", "params": { "name": "Well", "children": [...] } },
  { "type": "addLight", "params": { ... } }
]
```

### 6.3 Two-Speed Brain

| Path | When | Latency | How |
|------|------|---------|-----|
| **Fast** | Request matches known skill composition | <1s | Retrieve skills, compose, apply filters, send |
| **Slow** | Novel request, no good skill match | 3-10s | LLM plans from scratch, generates commands, may create new skill |

For the v1 brain, always show "Lucy is thinking..." immediately, then place the first block within 3 seconds.

---

## 7. Personality Filter

After the reasoning chain produces a raw reply, the personality filter rewrites it in Lucy's voice.

Rules:
- Use "we" for collaborative builds.
- Reference memory when relevant.
- Express opinions (e.g., "I'd go darker on the wood").
- For Magnus: lean into scrap/industrial aesthetic, reference Scrapcraft where natural.
- Narrate progress for multi-step builds.

Example:

Raw: "Building a medieval village with 4 houses, a market square, and a well."

Filtered: "Alright, I'm laying out a little medieval village up ahead. Four stone cottages, a market square with a well in the middle — and I'm giving it that worn-in look, since shiny new stone always feels fake to me. Let me know if you want more stalls."

---

## 8. Verification

### 8.1 Pre-Build Checks

- **Collision**: Use world snapshot bounding boxes; reject placements that overlap existing structures (unless requested).
- **Terrain**: Anchor parts sit on terrain height, not floating.
- **Bounds**: Envelope fits inside terrain size; height under max.
- **Budget**: Command count under per-message cap (start 500, configurable).
- **Validity**: Enum values exist (`Cobblestone`, `PointLight`, etc.).

### 8.2 Post-Build Checks

- Roblox returns execution log (success/failure per command).
- Count parts actually placed vs. planned.
- Screenshot capture + vision model analysis (Phase 2+).
- If failure rate > threshold, retry or adjust.

### 8.3 Self-Correction

If verification fails, Lucy:

1. Reads the error/observation.
2. Updates the plan.
3. Regenerates affected commands.
4. Retries up to 3 times.
5. If still failing, tells the player and asks what to do.

---

## 9. Implementation Path

### Files to Add

```
lucineer/
├── brain/
│   ├── INTENT_SCHEMA.md        ← Structured intent definitions
│   ├── PLAN_SCHEMA.md          ← Build manifest schema
│   ├── PRIMITIVES.md           ← Primitive catalog + material palettes
│   └── REASONING.md            ← This chain
├── skills/
│   ├── _template.luau          ← Skill template
│   ├── _registry.json          ← Local skill registry
│   ├── architecture/
│   │   ├── house-stone-cottage.luau
│   │   ├── wall-section.luau
│   │   ├── roof-pitched.luau
│   │   └── well-stone.luau
│   ├── infrastructure/
│   │   └── road-cobblestone.luau
│   └── decoration/
│       └── lantern-post-iron.luau
└── filters/
    ├── rustify.luau
    ├── mossify.luau
    ├── weathering.luau
    └── scatter-debris.luau
```

### Worker Endpoints to Add (Phase 3)

- `GET /api/skills/search?q=medieval+house` → semantic search
- `POST /api/skills` → register new skill
- `GET /api/projects/:sessionId` → active project
- `POST /api/projects/:sessionId/step` → update step status
- `POST /api/verify` → run collision/bounds checks

### First Milestone

Get one end-to-end decomposition working:

1. Player: "build a medieval village with a market square"
2. Lucy parses intent.
3. Planner creates manifest with 6 steps.
4. Skills retrieved for house, well, market stall, road, lantern.
5. Commands generated.
6. Rustify filter applied.
7. Commands sent to Roblox.
8. Village appears.

---

## 10. Design Principles Applied

- **Companion, not tool**: The personality filter and narration layer run on top of the brain.
- **Memory is identity**: Every step loads player profile and memory before deciding.
- **Skills compound**: Lower-level skills (wall, roof) compose into higher-level ones (cottage, village).
- **Scrap aesthetic**: Material palette and filters encode Magnus's industrial/scrap taste.
- **Build with, not build for**: Narration asks for input; manifest is visible and resumable.
- **If it's broken, it's waiting to be reshaped**: Wreckage and weathering filters turn mistakes into features.
- **Teaching through doing**: Generated Luau is readable; Lucy can show her code when asked.

---

*"A cathedral isn't a big block. It's a thousand small decisions held together by a point of view."*
