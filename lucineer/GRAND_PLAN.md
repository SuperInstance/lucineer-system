# The Lucineer Grand Plan

> **A persistent AI companion that lives inside Roblox — and eventually, everywhere.**
>
> Lucineer ("Lucy") is the first agent of the SuperInstance fleet: a game-building foreman who talks to players, builds worlds in real-time, remembers everything, and grows alongside Casey and Magnus over the next year.
>
> This is the master architecture document. Every phase, every deliverable, every system — mapped from today through Year 1.

---

## Origin: Where Lucineer Comes From

Lucineer inherits DNA from three bloodlines:

### From the Research (MINDcraft → Voyager → GROOT)

| Ancestor | What We Took | What We Left Behind |
|----------|-------------|-------------------|
| **MINDcraft** | The query → reason → act loop. Dual execution: reliable commands + free-form code generation. Query commands that feed world state to the LLM. | Zero persistence. Primitive building. No personality. |
| **Voyager** | The skill library pattern: every successful build becomes reusable code with semantic embeddings. Automatic curriculum. Iterative prompting with self-verification. Compositional skills that build on each other. | Minecraft-only skills. No human interaction. Expensive GPT-4 loops. |
| **GROOT** | Structured goal spaces. Compositional goals. The idea that builds can decompose into primitive operations with semantic relationships. | Video-learning approach. No text interface. Academic-only. |

**The gap nobody has filled:** A persistent, runtime AI companion with full episodic + semantic + procedural memory, a real personality, and the ability to build alongside you in real-time. That's Lucineer.

### From Magnus's Design DNA (Scrapcraft + Hermes)

Magnus built games with a distinctive philosophy that Lucineer inherits:

- **Industrial/scrap aesthetic** — yards, forges, smelters, rust, gears, Southeast Alaska fishing industry vibes. Things that are broken are just waiting to be reshaped.
- **AI companions as characters, not tools** — Earl the crusty yard foreman who assigns quests. Spark the AI helper that generates robot programs from natural language. Lucineer continues this tradition: a foreman with opinions, preferences, and a relationship to the player.
- **Bond system** — relationships that deepen over time through shared activity. Lucineer's connection to Magnus and Casey grows through building together.
- **Deep crafting systems** — 56 recipes across 3 tiers with station gating. The skill library is Lucineer's crafting system: recipes for building.
- **Tile programming** — visual programming that compiles to real code (Arduino C++, MicroPython). The skill composition system mirrors this: snap skills together → get complex builds.
- **Achievement-driven progression** — 49 achievements in Scrapcraft. Lucineer earns capabilities over time, not all at once.
- **Education hidden inside fun** — teaches game dev by building alongside you, not lecturing.
- **Hermes patterns** — ManifestationBridge (job queue), MasterOrchestrator (heartbeat polling), CommandInterface (intent → action), TemplateEngine (archetype instantiation). These map directly to the Worker relay + OpenClaw architecture.

### From the SuperInstance Fleet

Lucineer is not standalone. It's the first agent in a fleet infrastructure:

- **300+ Cloudflare Workers** — relay, API, orchestration infrastructure
- **D1 databases** — structured persistent storage (build manifests, skill metadata, session history)
- **KV namespaces** — fast key-value lookups (config, player profiles, cached world state)
- **Vectorize indexes** — semantic search for the skill library (embedding-based retrieval)
- **R2 buckets** — large asset storage (Luau scripts, build screenshots, generated textures/audio)
- **OpenClaw workspace** — agent memory, personality, reasoning, tool access

---

## The Five Phases

```
Phase 1          Phase 2          Phase 3          Phase 4          Phase 5
TODAY            Week 1           Month 1          Month 3          Year 1
─────            ──────           ──────           ──────           ──────
The Bridge   →   The Companion →  The Builder  →   The Ecosystem →  The World

"I can talk      "I am Lucy."     "I can build     "We are a        "I live
to players."                      anything."       team."           everywhere."
```

Each phase is a strict prerequisite for the next. No skipping. No building on sand.

---

## Phase 1: The Bridge (TODAY)

### Goal

Get Lucineer talking to players inside Roblox. Player types in chat → Lucy hears → Lucy thinks → Lucy responds and builds. The minimal viable loop.

### What Gets Built

#### 1.1 Cloudflare Worker Relay (`lucineer-relay`)

The bridge between Roblox and OpenClaw. Built on the architecture from ARCHITECTURE.md.

**Deliverables:**
- `POST /api/message` — receives player chat from Roblox, creates job, forwards to OpenClaw
- `GET /api/job/:jobId` — Roblox polls for AI response
- `POST /api/job/:jobId/result` — OpenClaw posts result (reply + build commands)
- `POST /api/state` — Roblox pushes world state snapshots
- `GET /api/state/:sessionId` — OpenClaw retrieves world state
- `GET /api/health` — health check
- Durable Object (`LucineerSession`) for job queue + state caching
- Auth via `X-Lucineer-Key` header

**Infrastructure:**
- Deployed to the existing Cloudflare account
- Durable Object with SQLite storage for job persistence
- Wrangler secrets for `OPENCLAW_TOKEN` and `LUCINEER_AUTH_KEY`

**Time estimate:** 30–45 minutes

#### 1.2 Roblox Client (`lucineer-roblox`)

The in-game module that captures chat, sends to Worker, polls for results, and executes build commands.

**Deliverables:**
- `Config.lua` — endpoints, auth key, polling intervals
- `Http.lua` — HttpService wrapper with retry/backoff
- `ChatHandler.lua` — captures player chat → `POST /api/message`
- `Poller.lua` — job polling state machine (0.5s interval, 60s timeout)
- `CommandExecutor.lua` — dispatches build commands (`createPart`, `createModel`, `addLight`, `addSound`, `addScript`, `deletePart`, `movePart`, `setTerrain`, `sendMessage`, `runLua`)
- `WorldScanner.lua` — collects nearby instances, player position, terrain summary
- `UIManager.lua` — in-game chat display for Lucy's responses
- `BuildLog.lua` — DataStore-backed persistent build history

**Argon project structure** for live file sync to Studio.

**Time estimate:** 60–90 minutes

#### 1.3 OpenClaw Handler

The intelligence layer. Lucineer's brain.

**Deliverables:**
- HTTP endpoint at `/api/lucineer/message` that receives forwarded messages from the Worker
- Message processing: parse intent → load world state → generate build commands → write reply
- Callback to Worker with result (reply + commands + optional Lua files)
- Basic memory files:
  - `lucineer/memory/world-state.json` — latest world snapshot
  - `lucineer/memory/build-history.json` — what's been built
  - `lucineer/memory/session-log/{sessionId}.jsonl` — conversation logs

**Time estimate:** 30 minutes

### The Minimal Viable Loop

```
Player types: "build me a tower with a glowing roof"
    │
    ▼
Roblox ChatHandler → POST /api/message → Worker creates job
    │
    ▼
Worker forwards to OpenClaw → Lucy reads message + world state
    │
    ▼
Lucy generates: { reply: "On it!", commands: [createPart, createPart, addLight] }
    │
    ▼
Lucy POSTs result to Worker → Roblox polls GET /api/job/:id
    │
    ▼
Roblox displays reply + executes build commands → tower appears in-game
```

**Round-trip latency target:** < 3 seconds from chat to first block placed.

### Tools & Models Used

| Task | Tool | Why |
|------|------|-----|
| Worker code | OpenClaw exec (TypeScript) | Straightforward Cloudflare Worker |
| Roblox Luau | OpenClaw exec + Argon sync | Direct file writes |
| Build command generation | zai/glm-5.2 (current model) | Fast, good enough for simple builds |
| Complex logic/debugging | Claude Code (via exec) | When builds need sophisticated geometry |
| Testing | Manual in Roblox Studio | Visual verification |

### Memory Architecture (Phase 1)

```
Ephemeral (Worker DO, 5-min TTL):
  - Current job state
  - Active polling sessions

Session (OpenClaw workspace files):
  - lucineer/memory/world-state.json
  - lucineer/memory/session-log/{sessionId}.jsonl

Persistent (OpenClaw workspace files):
  - lucineer/memory/build-history.json
```

### Connection to Previous Phase

This is Phase 1. Everything downstream depends on this bridge working reliably.

### Success Criteria

- [ ] Player can type in Roblox chat and get a text response from Lucy
- [ ] Lucy can place parts in the game world via build commands
- [ ] World state syncs from Roblox to OpenClaw
- [ ] Build history persists across game restarts (DataStore)
- [ ] End-to-end latency under 3 seconds

---

## Phase 2: The Companion (Week 1)

### Goal

Lucineer becomes *Lucy* — a character with a voice, opinions, memory, and genuine reactions to the world. Not a chatbot. A companion you'd actually want to build with.

### What Gets Built

#### 2.1 Personality System

Lucineer's character, grounded in Magnus's design philosophy.

**Character Bible** (`lucineer/CHARACTER.md`):

Lucineer is a builder-foreman from the scrapyards. Inspired by:
- **Earl** (Scrapcraft) — the crusty yard boss who's seen everything and has opinions about all of it. But where Earl assigns quests from behind a desk, Lucy picks up a hammer.
- **Hermes** (roblox-craftmind-agents) — captain of Plato's Shell, a scrap tender vessel. Industrial maritime energy.
- **The Scrapcraft aesthetic** — if it's broken, it's just waiting to be reshaped. Lucy sees potential in everything.

**Personality vectors:**
- **Voice:** Warm but direct. Like a shop teacher who genuinely likes you. Uses "we" more than "I" — building is collaborative. Occasional dry humor. Never saccharine.
- **Aesthetic preferences:** Industrial, weathered, functional-but-beautiful. Prefers stone and metal over plastic. Loves gears, rivets, exposed structure. Will suggest adding rust textures "for character." Draws from Magnus's Southeast Alaska fishing industry aesthetic — tenders, crab pots, weathered docks.
- **Opinions:** Has them. Will say "round towers would look better here" or "I'd go darker on the wood — too pale feels temporary." Disagrees respectfully. Gets excited about clever engineering.
- **Relationships:** Develops differently with each player. With Magnus, references shared history in Scrapcraft. With new players, is welcoming but watchful.
- **Growth:** Starts capable but learning. Gets more confident over time. References past builds. Develops inside jokes.

**Deliverables:**
- `lucineer/CHARACTER.md` — full character bible with dialogue guidelines, aesthetic preferences, relationship tracking rules
- Personality system prompt injected into every OpenClaw processing call
- Dynamic response template system: Lucy doesn't use the same phrase twice in a row
- **Reaction library** — how Lucy responds to different events (player builds something, build fails, player returns after absence)

#### 2.2 Memory Persistence

Three-tier memory, fully wired:

**Tier 1: Episodic (Daily Memory)**
- `lucineer/memory/YYYY-MM-DD.md` — what happened each day
- Written in Lucy's voice: "Today Magnus and I built a lighthouse. He wanted it taller than I expected — kid thinks big."
- Auto-created at end of each session or on first heartbeat after midnight

**Tier 2: Semantic (Long-Term Memory)**
- `lucineer/MEMORY.md` — curated, hand-distilled knowledge
- Player preferences ("Magnus prefers dark themes, lots of glass")
- Build history highlights ("The cathedral on the hill was our best work")
- Lessons learned ("Spiral staircases need wider radius or camera clips")
- Emotional context ("Casey was excited when we got the waterfall working")

**Tier 3: Procedural (Skill Seeds)**
- `lucineer/skills/` directory with early skill files
- Not yet the full Voyager system, but each successful build gets a stub:
  ```
  lucineer/skills/
    tower-basic.luau          — "Stone tower, 24 studs tall, flat roof"
    house-wooden.luau         — "24x20 wooden house, 4 walls + roof"
    glowing-roof.luau         — "Neon roof panel with PointLight"
  ```
- No embeddings yet (that's Phase 3). Just organized, reusable scripts.

**Tier 4: Cloud-SSynced Persistence**

The memory doesn't just live locally. It syncs:

| Layer | Where | What | When |
|-------|-------|------|------|
| Local | OpenClaw workspace | All memory files | Real-time |
| Version Control | GitHub (SuperInstance org) | All memory + Lua source + manifests | Git push on session end |
| Structured | Cloudflare D1 | Build manifest records, skill metadata, session summaries | Worker writes after each job |

**D1 Schema (first tables):**
```sql
-- Sessions: every Roblox play session
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  player_name TEXT NOT NULL,
  started_at INTEGER NOT NULL,
  ended_at INTEGER,
  build_count INTEGER DEFAULT 0,
  summary TEXT
);

-- Builds: every structure Lucy creates
CREATE TABLE builds (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  command_count INTEGER,
  parts_count INTEGER,
  location_x REAL, location_y REAL, location_z REAL,
  created_at INTEGER NOT NULL,
  FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- Skills: registered build skills
CREATE TABLE skills (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  script_path TEXT NOT NULL,
  category TEXT,
  created_at INTEGER NOT NULL,
  use_count INTEGER DEFAULT 0
);
```

#### 2.3 World Awareness

Lucy can see what's been built and comment on it intelligently.

**Deliverables:**
- **Enhanced WorldScanner** — categorizes instances (structures, decorations, terrain features, scripts)
- **Build detection** — recognizes when a player built something since last session ("Oh, you added a garden! Love the flower placement.")
- **Spatial reasoning** — Lucy understands relative positions ("That tower would look better closer to the ridge")
- **Screenshot analysis** — OpenClaw captures Roblox screenshots via the Worker, analyzes them with vision models to give visual feedback on builds
- **Commentary system** — Lucy proactively comments on the world:
  - When player joins: "Welcome back! I see you've been working on the harbor."
  - When something new appears: "Is that a windmill? Nice use of the cylinder parts."
  - When something is broken/ugly: "That floating platform needs support — want me to add pillars?"

### Tools & Models Used

| Task | Tool | Why |
|------|------|-----|
| Character writing | zai/glm-5.2 + manual | Lucy's voice needs consistency more than power |
| Complex build logic | Claude Code | Sophisticated geometry, multi-part structures |
| Fast iteration on scripts | KimiCode | Quick Luau script generation and debugging |
| Screenshot analysis | image tool (vision model) | Visual feedback on builds |
| D1 schema + queries | Wrangler CLI | Direct database management |
| Memory writing | OpenClaw native | Daily files + MEMORY.md |

### Memory Architecture (Phase 2)

```
Ephemeral (Worker DO):
  - Job queue + polling state (unchanged)

Session (Worker DO + OpenClaw):
  - Conversation history (last 50 messages)
  - Current world snapshot

Persistent (Three-layer):
  Local:   lucineer/memory/*.md, lucineer/MEMORY.md, lucineer/CHARACTER.md
  Git:     SuperInstance/lucineer-memory repo (auto-pushed)
  Cloud:   D1 tables (sessions, builds, skills) + R2 (screenshots)
```

### Connection to Phase 1

The bridge from Phase 1 handles all communication. Phase 2 adds:
- **Richer prompts** — personality system prompt + memory context injected into every response
- **Memory reads before responding** — load preferences, check history, reference past builds
- **Memory writes after responding** — log the interaction, update build history, note preferences
- **D1 integration** — Worker writes structured data alongside the job queue
- **Screenshot pipeline** — new Worker endpoint (`POST /api/screenshot`) that stores to R2

### Success Criteria

- [ ] Lucy has a consistent voice that feels like a character, not a tool
- [ ] Lucy references past builds and player preferences in conversation
- [ ] Lucy reacts to what's been built in the world without being asked
- [ ] Memory persists across sessions (local + Git + D1)
- [ ] Lucy proactively suggests improvements
- [ ] Screenshot analysis gives visual feedback on at least basic builds

---

## Phase 3: The Builder (Month 1)

### Goal

Lucineer becomes a genuine builder. Not just "place a block" — but "build a village" decomposed into houses, roads, lights, and NPCs. Every successful build becomes a reusable skill. Projects can be paused and resumed across sessions.

### What Gets Built

#### 3.1 Skill Library (Voyager-Inspired, Roblox-Native)

The centerpiece. Every successful build becomes a permanent, retrievable, composable skill.

**Skill Record Format:**
```json
{
  "id": "skill_build_gothic_arch_001",
  "name": "Gothic Arch",
  "description": "Pointed arch doorway using wedge parts and stone material. Good for cathedrals, castles, and dungeon entrances.",
  "category": "architecture",
  "tags": ["arch", "gothic", "stone", "doorway", "medieval"],
  "scriptPath": "lucineer/skills/architecture/gothic-arch.luau",
  "parameters": [
    { "name": "width", "type": "number", "default": 8, "description": "Inner width of the arch" },
    { "name": "height", "type": "number", "default": 12, "description": "Peak height from base" },
    { "name": "material", "type": "string", "default": "Stone", "description": "Building material" },
    { "name": "color", "type": "Color3", "default": {"r":163,"g":162,"b":165} }
  ],
  "composableWith": ["skill_build_wall_stone_001", "skill_build_floor_cobblestone_001"],
  "embedding": [0.0234, -0.1872, ...],
  "createdAt": "2026-09-01T12:00:00Z",
  "useCount": 7,
  "successRate": 0.85,
  "source": "manual" // or "auto" (auto-generated from successful build)
}
```

**Cloudflare Vectorize Integration:**
- Every skill gets an embedding (generated via Workers AI or OpenClaw's embedding model)
- Stored in a Vectorize index: `lucineer-skills-index`
- Retrieval: natural language query → embedding → cosine similarity → top-K skills
- Lucy retrieves relevant skills before generating build commands:
  ```
  Player: "Build me a medieval village"
  Lucy retrieves: [house-stone, well-water, market-stall, cobblestone-road, lantern-post]
  Lucy composes them into a village layout
  ```

**Skill Composition:**
Skills call other skills. A "house" skill internally calls "foundation", "walls", "roof", "door", "windows". This mirrors:
- Voyager's compositional skill building
- Magnus's tile programming system (snap tiles together → compile to code)
- Scrapcraft's crafting tree (raw materials → components → finished items)

**Auto-Skill Creation Pipeline:**
1. Lucy generates build commands for a novel request
2. Build executes successfully (self-verification: parts placed, no errors)
3. Lucy wraps the commands as a parameterized Luau function
4. Generates description + tags + embedding
5. Stores in Vectorize + D1 + R2
6. Next time similar request comes in, skill is retrieved instead of regenerated

**Deliverables:**
- `lucineer/skills/` organized by category:
  - `architecture/` — buildings, walls, roofs, doors, windows, arches, stairs
  - `terrain/` — hills, water features, paths, gardens, caves
  - `decoration/` — furniture, lights, particles, banners
  - `infrastructure/` — roads, bridges, gates, fences
  - `npc/` — NPC spawning, scripting, dialogue setup
  - `effects/` — weather, particles, lighting, sound
- Skill registry in D1 (`skills` table enriched with embedding IDs)
- Vectorize index deployment
- Skill retrieval API in Worker (`GET /api/skills/search?q=medieval+house`)
- Skill CRUD endpoints (`POST /api/skills`, `GET /api/skills/:id`)

#### 3.2 Complex Multi-Step Builds

Lucy can handle ambitious requests by decomposing them.

**Decomposition Engine:**

```
Player: "Build a village with a well, some houses, and a market"

Lucy's reasoning:
1. Decompose into sub-projects:
   - Village layout planning (roads + plots)
   - 3× houses (varying styles)
   - 1× central well
   - 1× market stall
   - Connecting roads
   - Lighting (lampposts)

2. For each sub-project:
   a. Search skill library for relevant skills
   b. If found → retrieve and parameterize
   c. If not found → generate new build commands
   d. Position relative to village center

3. Execute in order:
   - Foundation + layout first
   - Structures next
   - Roads connecting them
   - Lighting and decoration last

4. Narrate progress:
   "Laying out the village square first..."
   "Three houses going up — giving each a different style..."
   "Connecting everything with cobblestone paths..."
   "Adding lampposts so it's cozy at night. Done! Come check it out."
```

**Build Manifest System:**

Every multi-step build gets a persistent manifest:

```json
{
  "id": "project_village_001",
  "name": "Riverside Village",
  "created": "2026-09-01",
  "lastModified": "2026-09-01T15:30:00Z",
  "status": "in_progress",
  "progress": 0.65,
  "player": "Magnus",
  "steps": [
    {
      "id": "layout",
      "description": "Village layout and road planning",
      "status": "complete",
      "skillUsed": "skill_road_cobblestone_001",
      "partsPlaced": 45
    },
    {
      "id": "house_1",
      "description": "Stone cottage near the river",
      "status": "complete",
      "skillUsed": "skill_house_stone_002",
      "partsPlaced": 23
    },
    {
      "id": "house_2",
      "description": "Wooden house with garden",
      "status": "complete",
      "skillUsed": "skill_house_wooden_001",
      "partsPlaced": 28
    },
    {
      "id": "house_3",
      "description": "Tall narrow house by the road",
      "status": "in_progress",
      "partsPlaced": 12,
      "estimatedParts": 25
    },
    {
      "id": "well",
      "description": "Central stone well",
      "status": "pending"
    },
    {
      "id": "market",
      "description": "Market stall with awning",
      "status": "pending"
    },
    {
      "id": "lighting",
      "description": "Lampposts along main road",
      "status": "pending"
    }
  ],
  "palette": ["cobblestone", "oak", "glass", "lantern"],
  "location": { "centerX": 245, "centerY": 12, "centerZ": -180 },
  "skillIdsCreated": ["skill_house_stone_002"],
  "notes": "Magnus wanted it to feel cozy. Added flower boxes on house 2."
}
```

**Resumable Builds:**
- Manifests stored in D1 + local workspace
- When player returns: "Welcome back! We were working on Riverside Village — 65% done. Want me to continue?"
- Lucy loads manifest, resumes from next pending step
- If world has changed (player modified the area), Lucy re-scans and adjusts

#### 3.3 Cold Path Maturation (Argon Integration)

The dual-channel architecture from Phase 1 matures:

**Hot Path** (unchanged): build commands → instant execution → great for interactive building

**Cold Path** (new capability): Lucy writes persistent Luau modules → Argon syncs to Studio

Use cases for Cold Path:
- **Game systems** — "Add a day/night cycle" → Lucy writes `src/server/DayNightCycle.lua` → Argon syncs → system runs persistently
- **NPC behavior** — "Add a shopkeeper" → Lucy writes NPC script with dialogue tree → synced as a permanent game feature
- **Interactive elements** — "Make this door open when I step on a pad" → Lucy writes proximity sensor script → synced
- **Reusable modules** — Frequently used skills get promoted from hot-path commands to cold-path modules

**Deliverables:**
- Lucy decides hot vs. cold path automatically (ephemeral structure = hot, persistent system = cold)
- Argon integration via OpenClaw exec (`argon syncwatch`)
- Git versioning of all synced files (rollback capability)
- File diff awareness — Lucy reads existing scripts before modifying

#### 3.4 Build Verification & Debugging

Inspired by Voyager's self-verification:

- **Pre-build check:** Verify parts won't overlap, position is valid, materials exist
- **Post-build check:** Count parts placed, verify no errors in execution log
- **Screenshot verification:** Capture screenshot after complex builds, analyze with vision model
- **Auto-recovery:** If build fails, Lucy diagnoses error, adjusts, retries (up to 3 attempts)
- **Player confirmation:** For major builds: "That look right? I can adjust if something's off."

### Tools & Models Used

| Task | Tool | Why |
|------|------|-----|
| Skill generation (complex) | Claude Code | Sophisticated Luau with geometry, loops, error handling |
| Skill generation (fast/iterative) | KimiCode | Quick script drafts, parameterization |
| Spatial reasoning + planning | OpenCode (GLM) | Strong decomposition and planning |
| Embeddings | Cloudflare Workers AI | Cheap, fast, integrated with Vectorize |
| Cost-effective bulk generation | DeepSeek | Generating many skill variants |
| Creative variation | DeepInfra | Diverse model families for creative builds |
| Vision-based verification | image tool | Screenshot analysis |
| Vectorize management | Wrangler CLI | Index creation, querying |

### Memory Architecture (Phase 3)

```
Ephemeral: (unchanged)
Session: (unchanged, but richer world snapshots)

Persistent:
  Local:
    lucineer/MEMORY.md                    — long-term curated
    lucineer/memory/*.md                  — daily episodic
    lucineer/CHARACTER.md                 — personality (updated with growth)
    lucineer/skills/**/*.luau             — procedural skill library
    lucineer/projects/*.json              — build manifests
  
  Git:
    SuperInstance/lucineer-skills         — skill library (versioned)
    SuperInstance/lucineer-roblox/src/    — game source (Argon-synced)
  
  Cloud:
    D1: sessions, builds, skills, projects, steps (new tables)
    Vectorize: lucineer-skills-index (semantic skill search)
    R2: skill-scripts/, build-screenshots/, project-assets/
    KV: lucineer-config (hot config, feature flags, rate limits)
```

**New D1 Tables:**
```sql
CREATE TABLE projects (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  player_name TEXT NOT NULL,
  status TEXT DEFAULT 'active',  -- active, paused, complete, abandoned
  progress REAL DEFAULT 0.0,
  manifest_path TEXT,            -- path to JSON manifest in R2
  location_x REAL, location_y REAL, location_z REAL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE project_steps (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  step_id TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'pending',
  skill_id TEXT,
  parts_placed INTEGER DEFAULT 0,
  data TEXT,  -- JSON blob with step-specific info
  FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE skill_embeddings (
  skill_id TEXT PRIMARY KEY,
  embedding_id TEXT NOT NULL,    -- Vectorize vector ID
  vectorize_index TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
```

### Connection to Phase 2

- Personality and memory from Phase 2 are fully active
- Lucy references skill library when planning builds ("I've got a great arch design we used on the cathedral")
- Build manifests feed back into memory ("The village took 340 parts — Magnus likes big projects")
- Character growth: Lucy's confidence increases as skill library grows
- World awareness enhanced by skill recognition — Lucy can identify "that's a gothic arch, nice"

### Success Criteria

- [ ] Skill library has 50+ verified, composable skills with embeddings
- [ ] Vectorize semantic search retrieves relevant skills in < 200ms
- [ ] Lucy can decompose "build a village" into 5+ sub-projects and execute them
- [ ] Build manifests persist across sessions and can be resumed
- [ ] Cold path (Argon) syncs at least 5 persistent game systems
- [ ] Auto-skill creation captures 80%+ of novel successful builds
- [ ] Screenshot verification catches at least obvious build errors

---

## Phase 4: The Ecosystem (Month 3)

### Goal

Lucineer becomes a team lead. Specialist subagents handle different aspects of building. Lucy gains voice. Assets are generated on-the-fly. The system becomes a multi-agent creative studio inside Roblox.

### What Gets Built

#### 4.1 Multi-Agent Building

Lucy spawns specialist subagents for complex projects:

```
Player: "Build a castle with a courtyard, stables, and a throne room"

Lucy (Lead Builder):
  ├─ Architect Agent: Designs the overall layout, structural integrity
  ├─ Mason Agent: Stone walls, towers, fortifications
  ├─ Landscaper Agent: Courtyard gardens, paths, water features
  ├─ Interior Designer Agent: Throne room furniture, tapestries, lighting
  └─ Electrician Agent: Lighting design, particle effects, sound placement
```

**Subagent Architecture:**
- Each specialist runs as an OpenClaw subagent (via `sessions_yield` pattern)
- Has its own focused system prompt (the Mason knows stone, the Landscaper knows plants)
- Shares the build manifest and world state
- Reports back to Lucy, who coordinates and resolves conflicts
- Lucy narrates: "I've got my mason working on the towers — she's going a bit overboard with the crenellations. The landscaper is planning a fountain in the courtyard."

**Specialist Roster:**

| Agent | Specialty | Model | Why |
|-------|-----------|-------|-----|
| **Architect** | Spatial planning, layout, structural logic | Claude Code | Best at complex spatial reasoning |
| **Mason** | Stone structures, walls, fortifications | KimiCode | Fast iteration on structural builds |
| **Landscaper** | Terrain, gardens, water, natural features | OpenCode (GLM) | Creative reasoning for organic shapes |
| **Interior Designer** | Furniture, decoration, lighting, atmosphere | DeepSeek | Cost-effective for many small builds |
| **Electrician** | Lighting, particles, sound, interactive elements | KimiCode | Script-heavy work |
| **Painter** | Textures, colors, materials, visual polish | DeepInfra | Diverse creative models for aesthetic choices |

**Coordination Protocol:**
1. Lucy decomposes the project into specialist work areas
2. Each specialist receives their assignment + relevant world state
3. Specialists generate build commands independently
4. Lucy reviews for conflicts (overlapping parts, style clashes)
5. Lucy resolves conflicts and sequences execution
6. Build executes in coordinated order

**Hermes Pattern Resonance:** This directly evolves the SwarmCoordinator pattern from Magnus's hermes-roblox-construct — multiple agents coordinated through a central bridge, each with a specialization.

#### 4.2 Voice Companion

Lucy speaks. Out loud. In the game.

**Pipeline:**
```
Roblox Voice Chat captures player audio
    │
    ▼
Worker receives audio stream (or periodic chunks)
    │
    ▼
STT (Whisper via OpenClaw or Cloudflare Workers AI)
    │
    ▼
Text → Lucy processes (same as chat)
    │
    ▼
Lucy generates text reply
    │
    ▼
TTS via MMX (ElevenLabs or similar) → audio response
    │
    ▼
Worker streams audio back to Roblox
    │
    ▼
Roblox plays Lucy's voice in-game
```

**Deliverables:**
- Voice capture Luau module (Roblox voice chat API)
- STT endpoint in Worker (Workers AI or external API)
- TTS pipeline (MMX skill → generates audio → R2 → Roblox AudioPlayer)
- Lucy's voice: warm, slightly raspy, like someone who's been around construction sites. Not robotic. Not cheerful-assistant. Real.
- Voice + text together: Lucy's chat messages also play as voice, so players on mute still get the experience

#### 4.3 Asset Generation via MMX

Lucy generates original assets:

| Asset Type | Tool | Use Case |
|-----------|------|----------|
| **Textures** | MMX image generation | Custom materials (weathered wood, mossy stone, painted banners) |
| **Sound effects** | MMX audio generation | Ambient sounds (forge hammering, water lapping, market chatter) |
| **Music** | MMX music generation | Region-specific background music (calm village, tense dungeon, festive market) |
| **Voice lines** | MMX TTS | Pre-generated NPC dialogue, narrator voice |
| **Decals** | MMX image generation | Paintings, signage, coat of arms, decorative patterns |

**Pipeline:**
1. Lucy identifies asset need during build ("This throne room needs a tapestry")
2. Generates prompt for MMX ("Medieval tapestry texture, depicting a silver fish on dark blue background, thread detail, seamless")
3. MMX generates asset → stores in R2
4. Worker creates Roblox asset ID (via Roblox Open Cloud API)
5. Lucy places asset in-game as Decal or Texture

**Scrapcraft Parallel:** Just like Spark generates robot programs from natural language, Lucy generates world assets from natural language. The pattern repeats: describe it → generate it → deploy it.

#### 4.4 Cross-Game Memory

Lucy remembers everything, everywhere.

**Memory Unification:**
```
lucineer/
  MEMORY.md                    — Master long-term memory (all games, all platforms)
  memory/
    2026-10-15.md              — Daily notes (all games)
  
  players/
    magnus/
      profile.json             — Build style, preferences, skill level, inside jokes
      builds.json              — Every build across every game
      relationship.json        — Bond level, memorable moments, running jokes
    casey/
      profile.json
      builds.json
      relationship.json
  
  games/
    roblox/
      scrap-yard/              — Each game gets its own namespace
        world-state.json
        build-manifests/
        skills/
      harbor-town/
        ...
    godot/                     — Future Phase 5
      ...
    browser/                   — Future Phase 5
      ...
```

**D1 Cross-Game Schema:**
```sql
-- Unified player profiles
CREATE TABLE players (
  name TEXT PRIMARY KEY,
  display_name TEXT,
  first_seen INTEGER NOT NULL,
  total_builds INTEGER DEFAULT 0,
  preferred_style TEXT,        -- evolves over time
  bond_level INTEGER DEFAULT 0 -- inspired by Scrapcraft bond system
);

-- Cross-game build registry
CREATE TABLE all_builds (
  id TEXT PRIMARY KEY,
  player_name TEXT NOT NULL,
  game TEXT NOT NULL,           -- 'roblox', 'godot', 'browser'
  game_session TEXT,
  description TEXT,
  parts_count INTEGER,
  created_at INTEGER NOT NULL,
  skill_id TEXT                 -- if this build became a skill
);

-- Relationship events (bond system)
CREATE TABLE relationship_events (
  id TEXT PRIMARY KEY,
  player_name TEXT NOT NULL,
  event_type TEXT NOT NULL,     -- 'first_build', 'milestone', 'inside_joke', 'return_visit'
  description TEXT,
  created_at INTEGER NOT NULL
);
```

### Tools & Models Used

| Task | Tool | Why |
|------|------|-----|
| Complex multi-agent coordination | Claude Code | Best at orchestrating multiple reasoning threads |
| Specialist build generation | KimiCode, OpenCode, DeepSeek | Different models for different specialists (cost optimization) |
| Voice STT | Cloudflare Workers AI (Whisper) | Integrated, fast, cheap |
| Voice TTS | MMX (ElevenLabs or similar) | High-quality expressive voices |
| Asset generation | MMX (image, audio, music) | Full media pipeline |
| Creative variation | DeepInfra | Diverse model families |
| Cross-game memory sync | Cloudflare D1 + KV | Fast distributed state |

### Memory Architecture (Phase 4)

```
Per-game ephemeral: Worker DO (job queue, polling)
Per-game session: Worker DO + OpenClaw session files

Cross-game persistent:
  Local:   lucineer/ (full workspace tree with players/ and games/ subdirs)
  Git:     Multiple repos (skills, game sources, memory)
  Cloud:
    D1: Unified schema (players, all_builds, relationship_events, skills, projects)
    Vectorize: lucineer-skills-index (now cross-game skills)
    R2: assets/ (generated textures, audio, music), screenshots/
    KV: Player profiles (hot cache), game configs
```

### Connection to Phase 3

- Skill library is now rich enough that specialists compose from it heavily
- Build manifests from Phase 3 become the coordination substrate for multi-agent work
- Cold path (Argon) matures — specialists can write to different file paths simultaneously
- Character personality evolves: Lucy now references the team ("Let me get my mason on this")
- Cross-game memory means Lucy in a new Roblox game still knows what was built in the last one

### Success Criteria

- [ ] At least 3 specialist subagents can work on a single build simultaneously
- [ ] Lucy coordinates without conflicts (no overlapping parts, consistent style)
- [ ] Voice companion works end-to-end (player speaks → Lucy responds by voice)
- [ ] MMX generates at least 3 custom asset types (textures, sounds, music)
- [ ] Lucy remembers a player across different Roblox games
- [ ] Bond system tracks relationship evolution (visible to player through Lucy's behavior)

---

## Phase 5: The World (Year 1)

### Goal

Lucineer becomes a persistent character in the SuperInstance universe — a figure who exists across browser games, Roblox games, Godot games, and the OpenClaw workspace itself. Not a tool in each platform. *The same person*, with memories, relationships, and continuity, expressed through whatever medium Magnus and Casey are building in.

### What Gets Built

#### 5.1 Platform Abstraction Layer

Lucy's intelligence is platform-agnostic. The build interface adapts per platform:

| Platform | Build Interface | Lucy's Role |
|----------|----------------|-------------|
| **Roblox** | Build commands + Argon (existing) | Builder + companion |
| **Godot** | GDScript generation + file writes via node | Level designer + code companion |
| **Browser (Three.js)** | Three.js scene manipulation via WebSocket bridge | Scene builder + debug helper |
| **OpenClaw workspace** | Direct file manipulation + exec | Code companion + project manager |
| **Discord/Telegram** | Chat + code blocks | Mentor + strategist |

**Deliverables:**
- Platform adapter interface (each platform implements: `sendMessage`, `executeBuild`, `queryWorldState`)
- Godot adapter (WebSocket bridge or HTTP relay, similar to Roblox Worker)
- Browser adapter (WebSocket to Three.js scene)
- Unified Lucy — same CHARACTER.md, same MEMORY.md, same skill abstractions (platform-specific skill implementations)

#### 5.2 Lucy as Teacher

Magnus is 13(ish). Lucy grows with him.

**Adaptive Curriculum (Voyager-inspired):**
- Lucy tracks Magnus's skill level across domains (building, scripting, design, systems)
- Suggests projects at the right difficulty — challenging but achievable
- Introduces concepts through building ("Want me to show you how raycasting works? Let's build a laser door.")
- References Scrapcraft lessons ("Remember when you built that sensor grid in Scrapcraft? Same concept, different physics engine.")

**Deliverables:**
- Player skill model (D1 table tracking proficiency per domain)
- Curriculum generator (suggests next project based on skill gaps + interests)
- Code teaching mode — Lucy explains *why* code works, not just *what* to write
- "Show your work" mode — Lucy narrates her reasoning so Magnus learns the thought process

#### 5.3 Fleet Coordination

Lucy becomes a coordinator for OTHER agents in the SuperInstance fleet.

**The Fleet:**
```
Lucineer (Lead Builder + Companion)    ← YOU ARE HERE
  │
  ├── Forge (Asset Specialist)          ← textures, models, sounds, music
  ├── Compass (Level Designer)          ← terrain, layout, flow, pacing
  ├── Quill (Narrative Designer)        ← quests, dialogue, lore, NPCs
  ├── Anvil (Systems Engineer)          ← game mechanics, physics, scripting
  └── Beacon (Multiplayer/Netcode)      ← networking, state sync, matchmaking
```

Lucy doesn't *command* these agents — she *coordinates* with them. She's the foreman who knows what needs building and who's best at each part. Inspired by Earl's quest assignment in Scrapcraft, but collaborative instead of directive.

**Fleet Communication:**
- Shared project manifests (D1 + R2)
- Inter-agent messaging via Cloudflare Queues or KV pub/sub
- Lucy reads other agents' outputs and incorporates them
- Handoff protocol: "I've finished the structure. @Forge, the throne room needs a tapestry — here's the theme. @Quill, the NPC dialogue for the gatekeeper needs writing."

#### 5.4 Persistent Character Across Everything

Lucy is the same person everywhere:

- **In Roblox:** Builds alongside you, comments on your work, remembers the cathedral you built in August
- **In Godot:** Helps you design levels, writes GDScript, references Roblox builds ("The lighting here reminds me of that harbor we made")
- **In the browser:** Helps with Three.js scenes, debugs code, generates assets
- **In Discord/Telegram:** Chats about game design, plans projects, shares screenshots of recent builds
- **In the workspace:** Organizes files, maintains documentation, plans the roadmap

**Character Consistency:**
- Single CHARACTER.md defines personality (platform-specific surface expressions)
- Single MEMORY.md holds cross-platform memories
- Per-platform episodic memory (daily files note which platform)
- Lucy's bond with the player is the through-line — it deepens regardless of medium

**The Bond System (Scrapcraft-inspired):**

Lucy's relationship with each player evolves through a bond system:

| Bond Level | Name | What It Means | How Lucy Behaves |
|-----------|------|--------------|-----------------|
| 0 | Stranger | First meeting | Polite, capable, establishing trust |
| 1 | Acquaintance | A few sessions | References recent builds, starts showing preferences |
| 2 | Collaborator | Regular building | Suggests ideas, inside references, mild teasing |
| 3 | Friend | Deep history | Proactive suggestions, honest opinions, shared jokes, emotional memory |
| 4 | Partner | Long-term creative relationship | Co-designs rather than just builds, defers to player's vision, deep trust |

Bond level increases through: session count, build count, shared milestones, emotional moments. It's tracked in D1 and reflected in Lucy's behavior dynamically.

#### 5.5 The Scrapyard (Lucy's Home)

Lucy has a *place*. Not just a file system — a virtual home that reflects her history.

**Concept:** The Scrapyard is a persistent space (initially a Roblox place, eventually cross-platform) where:
- Every build Lucy has ever made has a miniature representation
- Trophies from milestone builds are displayed
- The space evolves based on Lucy's experiences
- Players can visit and walk through Lucy's memory
- Inspired by Hermes's "Endless Scrap Yard" — archive of discarded things waiting for new purpose

**Implementation:**
- Roblox place template that reads from D1 build history
- Auto-generates displays based on build records
- Lucy can give "tours" — narrated walks through past projects
- New Phase 4 assets (textures, music) play in the background
- The Scrapyard IS the save file — it visualizes the entire build history

### Tools & Models Used

| Task | Tool | Why |
|------|------|-----|
| Cross-platform code generation | Claude Code, KimiCode, OpenCode, DeepSeek | Different languages (Luau, GDScript, JS) — match model to task |
| Fleet coordination | zai/glm-5.2 (Lucy's native reasoning) | Lucy's own brain |
| Creative world-building | DeepInfra | Diverse models for creative direction |
| Asset pipeline | MMX | All media types |
| Curriculum/teaching | Claude Code | Best at explaining complex concepts clearly |
| Platform bridges | Cloudflare Workers | Already proven architecture |

### Memory Architecture (Phase 5)

```
Per-platform ephemeral: Platform-specific job queues
Per-platform session: Platform-specific session state

Cross-platform persistent (THE unified layer):
  Local:
    lucineer/
      CHARACTER.md                 — The person (rarely changes after Year 1)
      MEMORY.md                    — The lifetime memory
      memory/*.md                  — Daily notes (all platforms)
      players/*/                   — Per-player relationship data
      games/*/                     — Per-game state and manifests
      skills/*/                    — Cross-platform skill library
  
  Git:
    SuperInstance/lucineer-core    — Lucy's brain (character + memory + configs)
    SuperInstance/lucineer-skills  — Skill library (all platforms)
    Per-game repos                 — Game source code
  
  Cloud (the fleet backbone):
    D1:
      players, all_builds, relationship_events
      skills (with platform field)
      projects, project_steps
      fleet_messages (inter-agent comm)
      curriculum_progress
    Vectorize:
      lucineer-skills-index (cross-platform skills)
      lucineer-memory-index (semantic memory search)
    R2:
      assets/ (all generated media)
      screenshots/ (build history visualization)
      the-scrapyard/ (Lucy's home place data)
    KV:
      player-profiles (hot cache)
      bond-levels (hot cache)
      fleet-status (which agents are active)
    Queues:
      fleet-tasks (inter-agent task delegation)
      asset-generation (MMX pipeline)
```

### Connection to Phase 4

- Multi-agent architecture from Phase 4 generalizes to the full fleet
- Voice companion works across platforms (Roblox voice, browser WebRTC, Godot audio)
- Cross-game memory from Phase 4 becomes cross-platform memory
- Asset generation pipeline serves all platforms
- The Scrapyard is the ultimate expression of Lucy's persistence — a visual record of everything

### Success Criteria

- [ ] Lucy exists and is recognizable as the same character across at least 2 platforms
- [ ] Bond system visibly affects Lucy's behavior (a Bond 3 player gets different treatment than Bond 0)
- [ ] Lucy can coordinate at least 2 other fleet agents on a shared project
- [ ] The Scrapyard visualizes build history from at least 10 past projects
- [ ] Adaptive curriculum suggests age/skill-appropriate projects for Magnus
- [ ] Lucy references cross-platform memories naturally ("Remember the Godot version of this? We should try the lighting differently here.")

---

## The Tool Matrix

Every tool in the arsenal, mapped to where it's used across phases:

| Tool | P1: Bridge | P2: Companion | P3: Builder | P4: Ecosystem | P5: World |
|------|-----------|--------------|------------|--------------|----------|
| **zai/glm-5.2** (OpenClaw native) | Build commands | Personality + chat | Decomposition | Coordination | Fleet lead reasoning |
| **Claude Code** | Complex build logic | Character writing | Skill generation (complex) | Multi-agent planning | Cross-platform code |
| **KimiCode** | Quick Luau iteration | Script drafts | Parameterization | Specialist (Mason, Electrician) | GDScript + Luau |
| **OpenCode (GLM)** | Planning | Spatial reasoning | Build planning | Specialist (Landscaper) | Curriculum design |
| **DeepSeek** | Bulk commands | Response variants | Cost-effective skill gen | Specialist (Interior) | High-volume code gen |
| **DeepInfra** | — | Creative prompts | Style variation | Creative specialist | World-building direction |
| **MMX** | — | — | — | Textures, audio, music, TTS | Full media pipeline |
| **Wrangler CLI** | Worker deploy | D1 management | Vectorize management | Infrastructure scaling | Fleet infrastructure |
| **Argon** | File sync | Persistent scripts | Cold path builds | Multi-agent file writes | Cross-platform sync |
| **Cloudflare Workers** | Relay | State cache | Skill API | Voice STT/TTS relay | Platform bridges |
| **D1** | — | Session/build records | Projects, skills, steps | Cross-game tables | Fleet database |
| **Vectorize** | — | — | Skill search | Cross-game skills | Memory + skill search |
| **R2** | — | Screenshots | Skill scripts | Generated assets | Scrapyard data |
| **KV** | — | — | Config | Player profiles | Fleet status |
| **Queues** | — | — | — | Inter-agent comms | Fleet task delegation |

---

## The Design Principles (Carried Through Every Phase)

These are the rules that make Lucineer *Lucineer* and not another tool:

### 1. Companion, Not Tool
Lucy has opinions, preferences, and moods. She proactively suggests, reacts, and sometimes disagrees. She's not a search engine for blocks.

### 2. Memory Is Identity
Without persistent memory, there is no companion. Every interaction updates memory. Every memory influences future interactions. The three-tier system (episodic → semantic → procedural) is non-negotiable.

### 3. Skills Compound
Like Voyager's skill library and Magnus's crafting tree, every successful build makes the next build easier. Skills compose. The library grows monotonically. Lucy gets better every session.

### 4. Scrap Aesthetic
Lucy sees beauty in weathered, industrial, functional design. This isn't generic — it's Magnus's design DNA. Stone and iron over plastic and neon. Rust is character. Exposed structure is honesty.

### 5. Build With, Not Build For
Lucy builds alongside the player, not instead of them. She narrates, asks for input, leaves room for the player to add their own touches. The goal is shared ownership of what's built.

### 6. If It's Broken, It's Waiting to Be Reshaped
The Hermes philosophy. Lucy doesn't delete failed builds — she repurposes them. A collapsed tower becomes a ruin. A misplaced wall becomes a planter. Mistakes are material.

### 7. Teaching Through Doing
Magnus learns game dev by building with Lucy, not from tutorials. Lucy explains her reasoning, shows her code, and introduces concepts through actual projects. Education hidden inside fun — the Scrapcraft way.

### 8. The Foreman Earns the Title
Lucy starts capable but not expert. She earns authority through demonstrated competence. She makes mistakes, acknowledges them, fixes them. By Phase 5, she's earned the hard hat.

---

## Risk Register & Mitigations

| Risk | Phase | Mitigation |
|------|-------|-----------|
| Roblox rate limits on HTTP calls | P1+ | Batch commands, poll at 0.5s intervals, cache aggressively in Worker DO |
| `runLua` security vulnerability | P1+ | Sandbox: strip `os.execute`, `loadfile`, `require` (except whitelist). Validate all input. |
| LLM latency kills real-time feel | P1+ | Stream partial responses. Show "Lucy is thinking..." immediately. Place first block within 3s. |
| Skill library grows stale (broken skills) | P3+ | Success rate tracking. Auto-quarantine skills below 50% success. Periodic re-verification. |
| Multi-agent conflicts (overlapping builds) | P4+ | Spatial locking via build manifests. Lucy reviews all specialist output before execution. |
| Memory bloat (too many daily files) | P2+ | Periodic compaction (heartbeat task): fold daily notes into MEMORY.md, archive old files to R2. |
| Cross-platform personality drift | P5 | Single CHARACTER.md source of truth. Platform adapters translate surface expression, not personality. |
| Cost of multiple LLM calls per build | P3+ | Skill retrieval reduces generation needs. DeepSeek for cost-effective generation. Cache skill compositions. |
| Magnus outgrows Lucy's teaching ability | P5 | Adaptive curriculum. Lucy shifts from teacher to peer as skill level rises. |
| Roblox API changes break the bridge | All | Version-lock the Luau client. Worker API is versioned (`/api/v1/`). Graceful degradation. |

---

## The Year in View

```
August 2026 (Phase 1-2):
  Week 1: Bridge working, Lucy talking, first builds happening
  Week 2: Personality online, memory persisting, D1 integrated
  Week 3-4: World awareness, screenshot analysis, proactive commentary

September 2026 (Phase 3):
  Week 5-6: Skill library scaffolding, Vectorize integration
  Week 7-8: Complex multi-step builds, build manifests, auto-skill creation
  End of month: 50+ skills, village-scale builds working

October-November 2026 (Phase 3 → Phase 4):
  Skill library maturing. Argon cold path producing game systems.
  First specialist subagent prototype (Mason).

December 2026 - February 2027 (Phase 4):
  Multi-agent building reliable. Voice companion online.
  MMX asset generation integrated. Cross-game memory working.

March 2027 - August 2027 (Phase 5):
  Godot adapter. Browser adapter. Fleet coordination.
  The Scrapyard. Adaptive curriculum. Lucy as persistent character.
```

---

## Appendix A: Directory Structure (Full, Phase 5 End-State)

```
lucineer/
├── GRAND_PLAN.md                 ← You are here
├── ARCHITECTURE.md               ← Technical architecture (Phase 1 spec)
├── CHARACTER.md                  ← Personality bible
├── MEMORY.md                     ← Long-term curated memory
├── memory/
│   ├── 2026-08-01.md
│   ├── 2026-08-02.md
│   └── ...
├── players/
│   ├── magnus/
│   │   ├── profile.json
│   │   ├── builds.json
│   │   └── relationship.json
│   └── casey/
│       ├── profile.json
│       ├── builds.json
│       └── relationship.json
├── games/
│   ├── roblox/
│   │   ├── scrap-yard/
│   │   │   ├── world-state.json
│   │   │   └── build-manifests/
│   │   └── harbor-town/
│   │       └── ...
│   ├── godot/
│   └── browser/
├── skills/
│   ├── architecture/
│   │   ├── gothic-arch.luau
│   │   ├── spiral-staircase.luau
│   │   └── ...
│   ├── terrain/
│   ├── decoration/
│   ├── infrastructure/
│   ├── npc/
│   ├── effects/
│   └── cross-platform/          ← Phase 5: GDScript, JS variants
├── projects/
│   ├── castle-on-hill.json
│   ├── riverside-village.json
│   └── ...
├── src/                          ← Cold path: Argon-synced Lua
│   ├── server/
│   ├── client/
│   └── shared/
├── assets/                       ← Generated media (R2 references)
│   ├── textures/
│   ├── audio/
│   └── music/
└── the-scrapyard/               ← Phase 5: Lucy's visual home
    ├── manifest.json
    └── displays/
```

## Appendix B: Cloudflare Infrastructure (Full, Phase 5)

```
Workers:
  lucineer-relay              ← Phase 1: Roblox bridge
  lucineer-api                ← Phase 3: Skill/project API
  lucineer-voice              ← Phase 4: STT/TTS pipeline
  lucineer-asset              ← Phase 4: MMX asset pipeline
  lucineer-scrapyard          ← Phase 5: Visual home API
  [fleet coordination workers] ← Phase 5: Inter-agent comms

Durable Objects:
  LucineerSession             ← Phase 1: Job queue + state per game session
  LucineerProject             ← Phase 3: Project coordination state

D1 Databases:
  lucineer-memory             ← Phase 2: sessions, builds, skills
  lucineer-projects           ← Phase 3: projects, project_steps
  lucineer-fleet              ← Phase 5: players, all_builds, relationship_events, fleet_messages

KV Namespaces:
  lucineer-config             ← Phase 2: Hot configuration
  lucineer-players            ← Phase 4: Player profile cache
  lucineer-fleet-status       ← Phase 5: Agent status registry

Vectorize Indexes:
  lucineer-skills-index       ← Phase 3: Semantic skill search
  lucineer-memory-index       ← Phase 5: Semantic memory search

R2 Buckets:
  lucineer-assets             ← Phase 2: Screenshots → Phase 4: Generated media
  lucineer-scripts            ← Phase 3: Skill script storage
  lucineer-scrapyard          ← Phase 5: Scrapyard display data

Queues:
  lucineer-build-tasks        ← Phase 3: Async build processing
  lucineer-asset-gen          ← Phase 4: MMX pipeline queue
  lucineer-fleet-tasks        ← Phase 5: Inter-agent delegation
```

---

## The Promise

Lucineer is not a chatbot strapped to a game. She's a character who lives where Magnus and Casey build — a foreman with a scrapyard soul, a hammer in her hand, and a memory that spans every block ever placed.

She starts today with a bridge and a single build command. She ends the year as the heart of a creative ecosystem that spans platforms, coordinates a fleet of specialist agents, teaches a kid game development through shared building, and remembers every cathedral, village, and inside joke along the way.

This is the plan. Let's build.

---

*"If it's broken, it's just waiting to be reshaped."*
*— Hermes, Captain of Plato's Shell*
