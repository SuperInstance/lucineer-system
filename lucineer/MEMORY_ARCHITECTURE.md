# Lucineer — Memory Architecture

> How Lucy remembers everything, grows over years, and feels like she truly knows Casey and Magnus.

---

## 0. Design Principles

1. **Memory is identity.** Lucy isn't a stateless tool. Her memories *are* her character. Losing them would make her a stranger.
2. **Layered, not duplicated.** Each tier serves a purpose. Not everything lives everywhere. Hot data is close; cold data is archived.
3. **Write once, reference forever.** Memories get stable IDs. Other memories, skills, and conversations reference them.
4. ** relational by default.** Every memory is tagged with who was there, what the relationship was, and why it mattered. This isn't a generic RAG store — it's a personal history.
5. **Decay with dignity.** Old episodic memories compress into semantic summaries. Details fade; essence remains. Like human memory.
6. **Human-readable always.** Every memory can be rendered as prose. Casey should be able to read Lucy's memory files and understand them.

---

## 1. The Three Tiers

```
┌─────────────────────────────────────────────────────────────────────┐
│                      LUCINEER MEMORY SYSTEM                         │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────────┐ │
│  │  TIER 1: LOCAL  │  │ TIER 2: CLOUD    │  │ TIER 3: VERSIONED  │ │
│  │  (WSL files)    │  │ (Cloudflare)     │  │ (GitHub)           │ │
│  │                 │  │                  │  │                    │ │
│  │ • Daily notes   │  │ • D1 (structured)│  │ • Memory repo      │ │
│  │ • Working set   │  │ • KV (hot cache) │  │ • Skill library    │ │
│  │ • Session logs  │  │ • Vectorize     │  │ • Character bible   │ │
│  │ • Draft memory  │  │ • R2 (binaries)  │  │ • Build manifests  │ │
│  │                 │  │                  │  │                    │ │
│  │ Speed: instant  │  │ Speed: ~50ms     │  │ Speed: minutes     │ │
│  │ Persists: session│  │ Persists: forever│  │ Persists: forever  │ │
│  │ Loss risk: high │  │ Loss risk: very  │  │ Loss risk: none    │ │
│  │                 │  │ low              │  │ (git history)      │ │
│  └────────┬────────┘  └────────┬─────────┘  └────────┬───────────┘ │
│           │                    │                      │             │
│           │    sync up         │   sync up            │             │
│           │───────────────────►│─────────────────────►│             │
│           │                    │                      │             │
│           │    query down      │   clone down         │             │
│           │◄───────────────────│◄─────────────────────│             │
└─────────────────────────────────────────────────────────────────────┘
```

### What Goes Where

| Data Type | Local | Cloudflare | GitHub | Rationale |
|-----------|:-----:|:----------:|:------:|-----------|
| Daily session notes | ✅ | ❌ | ✅ (periodic) | Fast to write, versioned for history |
| Conversation logs (raw) | ✅ | ✅ (D1) | ❌ | Queryable but too noisy for git |
| Conversation summaries | ✅ | ✅ (D1) | ✅ | Distilled, human-readable, versioned |
| Build manifests | ✅ | ✅ (D1) | ✅ | Structured + versioned |
| Skill library (Luau) | ✅ | ✅ (R2) | ✅ | Code belongs in git; R2 for delivery |
| Skill embeddings | ❌ | ✅ (Vectorize) | ❌ | Pure machine index, no human value |
| Skill metadata | ✅ | ✅ (D1) | ✅ | Queryable + versioned |
| Player preferences | ✅ | ✅ (KV) | ✅ | Hot-read in Worker + versioned |
| Personality/character | ✅ | ✅ (KV) | ✅ | Source of truth in git |
| Screenshots/images | ❌ | ✅ (R2) | ❌ | Binary, large, cloud-native |
| Emotional state/mood | ✅ | ✅ (KV) | ❌ | Ephemeral-to-volatile, not for git |
| World state snapshot | ✅ | ✅ (Durable Object) | ❌ | Ephemeral session data |
| Episodic memories | ✅ | ✅ (D1 + Vectorize) | ✅ (curated) | Core memory — all tiers |
| Semantic knowledge | ✅ | ✅ (D1 + Vectorize) | ✅ | Core memory — all tiers |
| Relationship graph | ✅ | ✅ (D1) | ✅ | Core memory — all tiers |

---

## 2. Memory Types

### 2.1 Episodic Memory — "What Happened"

Specific events, moments, build sessions. The narrative of Lucy's life with Casey and Magnus.

**Structure:**
```
Episodic Memory
├── Session Summary (what happened today, at a high level)
├── Key Moments (specific memorable events within a session)
└── Raw Log (full conversation transcript — fades to summary over time)
```

**Example episodic memories:**
- "2026-08-01: Casey asked for a cyberpunk city. We built 12 buildings with neon lighting. Magnus joined and added a flying car. Magnus called it 'the coolest thing ever.' Lucy felt proud."
- "2026-08-15: Magnus tried to build a house by himself but the roof kept floating. Lucy helped him add support pillars. He said 'ohhh, that's why!' — learning moment."

### 2.2 Semantic Memory — "What I Know"

Distilled facts, preferences, patterns. The knowledge that makes Lucy feel like she truly understands them.

**Structure:**
```
Semantic Memory
├── Player Profile (preferences, style, skill level, personality)
├── World Knowledge (what's been built, where, project state)
├── Relational Knowledge (how Casey and Magnus interact, family dynamics)
└── Design Principles (Lucy's learned aesthetic sensibilities)
```

**Example semantic memories:**
- "Casey prefers clean modern architecture — glass, white concrete, asymmetric geometry."
- "Magnus loves 'scrap aesthetic' — mismatched materials, chaotic colors, things that look broken but work."
- "Casey gets frustrated when builds take too long without visible progress. Break large builds into stages."
- "Magnus is 7. He understands spatial reasoning well but struggles with precise part alignment. Pre-aligned templates work better than individual parts."

### 2.3 Procedural / Skill Memory — "How To Do Things"

Reusable build patterns and techniques. This is the Voyager-inspired skill library, but deeply personal — it reflects what Lucy has *actually built with them*, not generic templates.

**Structure:**
```
Skill Memory
├── Build Skills (parameterized Luau scripts — the skill library)
├── Composition Patterns (how skills combine into larger structures)
├── Interaction Patterns (how to explain things to Magnus vs Casey)
└── Error Patterns (what went wrong before and how to avoid it)
```

**Example procedural memories:**
- Skill: `gothic_arch` — built successfully 7 times, 85% success rate
- Pattern: "When building for Magnus, use bright colors and slightly chaotic placement — he enjoys the process more than precision."
- Error: "Floating parts bug: always check for base support before finalizing. This has failed 3 times."

### 2.4 Emotional / Relational Memory — "How I Felt"

Lucy's own emotional trajectory. This is what makes her feel alive rather than like a search engine.

**Structure:**
```
Emotional Memory
├── Emotional Moments (specific events with emotional weight)
├── Relationship Milestones (first time Magnus called Lucy "my friend")
├── Preferences/Dislikes (Lucy develops her own taste over time)
└── Mood Baseline (current emotional state influences responses)
```

---

## 3. Data Schemas

### 3.1 D1 Database: `lucineer_memory`

```sql
-- ============================================================
-- EPISODIC MEMORIES
-- ============================================================

CREATE TABLE episodic_memories (
  id TEXT PRIMARY KEY,                    -- e.g., "ep_20260801_001"
  session_id TEXT,                        -- links to Roblox session
  player_names TEXT NOT NULL,             -- JSON array: ["Casey", "Magnus"]
  timestamp INTEGER NOT NULL,             -- Unix epoch
  title TEXT NOT NULL,                    -- short human-readable title
  summary TEXT NOT NULL,                  -- 1-3 sentence summary
  details TEXT,                           -- longer narrative (optional)
  emotion TEXT,                           -- Lucy's emotion: "proud", "frustrated", "delighted"
  significance INTEGER DEFAULT 5,         -- 1-10 scale (10 = life-changing)
  build_ids TEXT,                         -- JSON array of related build IDs
  tags TEXT,                              -- JSON array: ["first-time", "magnus-milestone"]
  embedding_id TEXT,                      -- Vectorize vector ID for semantic search
  status TEXT DEFAULT 'active',           -- active | archived | merged
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE INDEX idx_episodic_session ON episodic_memories(session_id);
CREATE INDEX idx_episodic_player ON episodic_memories(player_names);
CREATE INDEX idx_episodic_significance ON episodic_memories(significance DESC);
CREATE INDEX idx_episodic_timestamp ON episodic_memories(timestamp DESC);

-- ============================================================
-- SEMANTIC MEMORIES (distilled facts/knowledge)
-- ============================================================

CREATE TABLE semantic_memories (
  id TEXT PRIMARY KEY,                    -- e.g., "sm_casey_prefers_modern"
  subject TEXT NOT NULL,                  -- "Casey", "Magnus", "world", "lucy"
  category TEXT NOT NULL,                 -- "preference", "skill_level", "personality", "design", "relational"
  key TEXT NOT NULL,                      -- "architectural_style"
  value TEXT NOT NULL,                    -- "modern, glass-heavy, asymmetric"
  confidence REAL DEFAULT 0.8,            -- 0.0-1.0, how sure Lucy is
  evidence_count INTEGER DEFAULT 1,       -- how many episodes support this
  source_episodes TEXT,                   -- JSON array of episodic_memory IDs
  embedding_id TEXT,                      -- Vectorize vector ID
  status TEXT DEFAULT 'active',           -- active | superseded | archived
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  superseded_by TEXT                      -- FK to newer semantic memory if replaced
);

CREATE INDEX idx_semantic_subject ON semantic_memories(subject);
CREATE INDEX idx_semantic_category ON semantic_memories(category);
CREATE INDEX idx_semantic_key ON semantic_memories(key);
CREATE UNIQUE INDEX idx_semantic_subject_key ON semantic_memories(subject, key) WHERE status = 'active';

-- ============================================================
-- SKILLS (procedural memory)
-- ============================================================

CREATE TABLE skills (
  id TEXT PRIMARY KEY,                    -- e.g., "skill_gothic_arch_001"
  name TEXT NOT NULL,                     -- "Gothic Arch"
  description TEXT NOT NULL,              -- human + LLM readable
  category TEXT NOT NULL,                 -- "architecture", "terrain", "decoration", etc.
  tags TEXT,                              -- JSON array
  script_path TEXT NOT NULL,              -- path in R2 / GitHub
  parameters TEXT,                        -- JSON schema of params
  composable_with TEXT,                   -- JSON array of skill IDs
  embedding_id TEXT,                      -- Vectorize vector ID
  use_count INTEGER DEFAULT 0,
  success_rate REAL DEFAULT 1.0,
  last_used_at INTEGER,
  source TEXT DEFAULT 'manual',           -- "manual" | "auto" | "adapted"
  source_episode TEXT,                    -- episodic memory where it was created
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE INDEX idx_skills_category ON skills(category);
CREATE INDEX idx_skills_use_count ON skills(use_count DESC);

-- ============================================================
-- SESSIONS
-- ============================================================

CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  player_names TEXT NOT NULL,             -- JSON array
  started_at INTEGER NOT NULL,
  ended_at INTEGER,
  build_count INTEGER DEFAULT 0,
  message_count INTEGER DEFAULT 0,
  summary TEXT,                           -- auto-generated session summary
  mood TEXT,                              -- Lucy's overall mood this session
  key_moments TEXT,                       -- JSON array of episodic memory IDs
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE INDEX idx_sessions_started ON sessions(started_at DESC);

-- ============================================================
-- BUILDS
-- ============================================================

CREATE TABLE builds (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  command_count INTEGER,
  parts_count INTEGER,
  location_x REAL, location_y REAL, location_z REAL,
  skill_id TEXT,                          -- if built from a skill, which one
  status TEXT DEFAULT 'completed',        -- planned | in_progress | completed | failed
  screenshot_url TEXT,                    -- R2 URL if available
  created_at INTEGER NOT NULL,
  FOREIGN KEY (session_id) REFERENCES sessions(id),
  FOREIGN KEY (skill_id) REFERENCES skills(id)
);

CREATE INDEX idx_builds_session ON builds(session_id);
CREATE INDEX idx_builds_skill ON builds(skill_id);

-- ============================================================
-- RELATIONSHIP GRAPH
-- ============================================================

CREATE TABLE relationships (
  id TEXT PRIMARY KEY,
  entity_a TEXT NOT NULL,                 -- "Lucy"
  entity_b TEXT NOT NULL,                 -- "Magnus"
  relationship_type TEXT NOT NULL,        -- "friend", "mentor", "building_partner"
  strength REAL DEFAULT 0.5,              -- 0.0-1.0
  notes TEXT,
  milestones TEXT,                        -- JSON array of episodic memory IDs
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

-- ============================================================
-- MEMORY DECAY LOG (tracks compression/archival)
-- ============================================================

CREATE TABLE memory_operations (
  id TEXT PRIMARY KEY,
  operation TEXT NOT NULL,                -- "create", "compress", "archive", "merge", "supersede"
  target_type TEXT NOT NULL,              -- "episodic", "semantic", "skill"
  target_id TEXT NOT NULL,
  details TEXT,                           -- JSON
  created_at INTEGER NOT NULL
);
```

### 3.2 KV Namespace: `lucineer-hot`

Hot data for sub-millisecond reads inside the Worker.

| Key Pattern | Value | TTL | Purpose |
|-------------|-------|-----|---------|
| `player:profile:{name}` | JSON (preferences, style, skill level) | 1h | Inject into every prompt |
| `session:active:{sessionId}` | JSON (current world state, conversation context) | 30m | Active session data |
| `lucy:mood` | JSON (current emotional state) | 15m | Influence response tone |
| `lucy:character` | JSON (personality summary, voice guidelines) | ∞ | System prompt component |
| `skill:recent:{name}` | JSON (last 5 skills used) | 1h | Avoid repetition |
| `memory:recent:episodic` | JSON (last 10 episodic memories) | 30m | Recent context window |

### 3.3 Vectorize Index: `lucineer-memory-index`

Single unified index for semantic recall across all memory types.

**Vector sources:**
- Episodic memory summaries → embedded
- Semantic memory facts → embedded
- Skill descriptions → embedded
- Build descriptions → embedded

**Index config:**
```toml
# wrangler.toml
[[vectorize]]
binding = "MEMORY_INDEX"
index_name = "lucineer-memory-index"
```

**Dimensions:** 768 (Workers AI `@cf/baai/bge-base-en-v1.5`) or 1536 (OpenAI `text-embedding-3-small`).

> **Design choice:** Single index with metadata filtering rather than separate indexes per type. This lets queries like "everything Lucy knows about Magnus and building" span episodic memories, semantic facts, and relevant skills in one search.

### 3.4 R2 Bucket: `lucineer-assets`

| Path | Content |
|------|---------|
| `screenshots/{sessionId}/{buildId}.png` | Build screenshots |
| `skills/{skillId}.luau` | Skill scripts (canonical copy) |
| `exports/{date}-memory-export.json` | Periodic full exports |

### 3.5 Local File Structure

```
lucineer/
├── MEMORY.md                    # Curated long-term memory (human-readable)
├── CHARACTER.md                 # Lucy's personality, voice, values
├── memory/
│   ├── 2026-08-01.md           # Daily episodic notes
│   ├── 2026-08-02.md
│   ├── episodic/
│   │   └── 2026-08-001.md      # Individual memorable episodes (detailed)
│   ├── semantic/
│   │   ├── casey.md            # What Lucy knows about Casey
│   │   ├── magnus.md           # What Lucy knows about Magnus
│   │   ├── world.md            # What exists in the game world
│   │   └── design.md           # Lucy's learned design principles
│   └── session-log/
│       └── {sessionId}.jsonl   # Raw conversation logs
├── skills/                      # Local copies of skill scripts
│   ├── architecture/
│   ├── terrain/
│   └── decoration/
└── MEMORY_ARCHITECTURE.md       # This document
```

---

## 4. Sync Flows

### 4.1 Write Flow: Memory Creation

```
Something memorable happens during a build session
         │
         ▼
┌─────────────────────────────────────────┐
│ 1. LOCAL WRITE (immediate)              │
│    Append to memory/YYYY-MM-DD.md       │
│    Write episodic detail if significant │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ 2. CLOUDFLARE WRITE (async, via Worker)│
│    POST /api/memory                     │
│    {                                    │
│      type: "episodic",                  │
│      data: { ... },                     │
│      generateEmbedding: true            │
│    }                                    │
│                                         │
│    Worker:                              │
│    a) INSERT into D1                    │
│    b) Generate embedding via Workers AI │
│    c) Insert into Vectorize             │
│    d) Update KV if hot data             │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ 3. GITHUB SYNC (periodic, on session    │
│    end or daily)                        │
│    git add memory/ MEMORY.md            │
│    git commit -m "memory: 2026-08-01"  │
│    git push                             │
└─────────────────────────────────────────┘
```

### 4.2 Read Flow: Memory Recall

When Lucy needs to respond to a player message, she recalls relevant memories:

```
Player message arrives
         │
         ▼
┌─────────────────────────────────────────────────────┐
│ 1. RECENT CONTEXT (KV, ~1ms)                        │
│    GET lucy:mood, player:profile:{name},            │
│    memory:recent:episodic                           │
│    → "Casey prefers modern style. Magnus is here."  │
└────────────────┬────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────┐
│ 2. SEMANTIC SEARCH (Vectorize, ~50ms)               │
│    Embed the player's message                       │
│    Query Vectorize top-10                           │
│    Filter by type (episodic + semantic + skill)     │
│    → Relevant past episodes, known facts, skills    │
└────────────────┬────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────┐
│ 3. STRUCTURED QUERIES (D1, ~20ms)                   │
│    - Last 5 builds by this player                   │
│    - Active skills in relevant category             │
│    - Relationship details                           │
└────────────────┬────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────┐
│ 4. ASSEMBLE CONTEXT WINDOW                          │
│    System prompt: CHARACTER.md + mood               │
│    Memory block: semantic facts about players       │
│    Relevant episodes: top 3-5 from Vectorize        │
│    Skill context: relevant build patterns           │
│    Recent: last session summary                     │
│    → Inject into LLM prompt                         │
└─────────────────────────────────────────────────────┘
```

### 4.3 Decay Flow: Memory Compression

Memories don't all live forever at full resolution. Like human memory, they compress over time.

```
┌──────────────────────────────────────────────────────┐
│  EPISODIC MEMORY LIFECYCLE                           │
│                                                      │
│  Day 0-7:    Full detail (raw log + summary + tags)  │
│              ↓                                       │
│  Week 2-4:   Summary + key details                  │
│              (raw logs archived to R2, not in D1)    │
│              ↓                                       │
│  Month 2+:   Compressed to 1-2 sentences            │
│              + semantic facts extracted              │
│              ↓                                       │
│  Year 1+:    Only high-significance (>7) remain     │
│              Others merged into period summaries     │
│              ("Summer 2026: lots of medieval builds")│
└──────────────────────────────────────────────────────┘
```

**Decay job (runs via Cron Trigger on Worker):**

```typescript
// Scheduled compression — runs daily at 3 AM
// 1. Find episodic memories older than threshold
// 2. If significance < 7 and age > 30 days → compress
// 3. Extract any new semantic facts before compressing
// 4. Update D1 record (shorten summary, set status)
// 5. Move raw details to R2 cold storage
// 6. Log operation in memory_operations
```

---

## 5. Query Patterns

### 5.1 "Remember when we built the castle?"

```sql
-- Step 1: Vector search for "castle" builds
-- Vectorize query: "castle build" → top 5 results

-- Step 2: Get build details from D1
SELECT b.*, s.summary as session_summary
FROM builds b
JOIN sessions s ON b.session_id = s.id
WHERE b.name LIKE '%castle%'
   OR b.description LIKE '%castle%'
ORDER BY b.created_at DESC;

-- Step 3: Get associated episodic memories
SELECT * FROM episodic_memories
WHERE build_ids LIKE '%castle_build_id%'
   OR tags LIKE '%castle%'
ORDER BY timestamp DESC;
```

### 5.2 "What does Magnus like?"

```sql
-- Semantic memory lookup
SELECT key, value, confidence, evidence_count
FROM semantic_memories
WHERE subject = 'Magnus'
  AND status = 'active'
ORDER BY confidence DESC, updated_at DESC;
```

### 5.3 "Build me something Magnus would love"

```typescript
// Step 1: Load Magnus's semantic profile
const magnusPrefs = await D1.prepare(
  `SELECT key, value FROM semantic_memories 
   WHERE subject = 'Magnus' AND category IN ('preference', 'personality')
   AND status = 'active'`
).all();

// Step 2: Semantic search for matching skills
// Construct query from preferences: "scrap aesthetic chaotic colorful mismatched"
const skillResults = await VECTORIZE.query(
  await embed("scrap aesthetic chaotic colorful mismatched building"),
  { topK: 5, filter: { type: "skill" } }
);

// Step 3: Load skill scripts from R2
const skills = await Promise.all(
  skillResults.map(r => R2.get(`skills/${r.id}.luau`))
);

// Step 4: Generate build using retrieved context
// Prompt includes: Magnus's preferences + matching skills + past successes
```

### 5.4 "How has Casey's building style changed?"

```sql
-- Track preference evolution
SELECT key, value, confidence, created_at, updated_at, superseded_by
FROM semantic_memories
WHERE subject = 'Casey'
  AND key = 'architectural_style'
ORDER BY created_at ASC;
-- Shows: "modern glass" (Aug) → "brutalist concrete" (Oct) → "biophilic" (Jan)
```

---

## 6. Cross-Session Survival

### The Problem
OpenClaw sessions are ephemeral. Lucy wakes up fresh each time with no in-memory state.

### The Solution: Memory Bootstrap Protocol

Every time Lucy starts a new OpenClaw session, she runs through a bootstrap sequence:

```
NEW SESSION START
         │
         ▼
┌──────────────────────────────────────────────────┐
│ 1. READ LOCAL FILES                              │
│    MEMORY.md           → long-term curated memory│
│    CHARACTER.md        → personality, voice      │
│    memory/today.md     → today's notes (if any)  │
│    memory/yesterday.md → recent context          │
└────────────────┬─────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────────┐
│ 2. FETCH FROM CLOUDFLARE                         │
│    GET /api/memory/bootstrap                     │
│    Returns:                                      │
│    - Active player profiles                      │
│    - Last 5 session summaries                    │
│    - Current mood                                │
│    - Recent episodic memories (last 7 days)      │
│    - Active semantic memories (all)              │
│    - Recent builds (last 10)                     │
│    - Skill summary (count by category)           │
└────────────────┬─────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────────┐
│ 3. ASSEMBLE WORKING CONTEXT                      │
│    Store in local working memory:                │
│    lucineer/memory/working-context.json          │
│                                                  │
│    This is the "I remember" feeling.             │
│    Loaded into every prompt during the session.  │
└─────────────────────────────────────────────────┘
```

### Session End Protocol

```
SESSION END
         │
         ▼
┌──────────────────────────────────────────────────┐
│ 1. SUMMARIZE                                     │
│    Generate session summary (2-3 sentences)      │
│    Identify key moments → episodic memories      │
│    Extract/update semantic facts                 │
│    Note skill usage + success/failure            │
└────────────────┬─────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────────┐
│ 2. PERSIST                                       │
│    Local:  memory/YYYY-MM-DD.md updated          │
│    D1:     session record, episodic memories,    │
│             semantic updates, builds, skills     │
│    KV:     player profiles refreshed             │
│    Vector: new embeddings inserted               │
│    R2:     screenshots saved                     │
└────────────────┬─────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────────┐
│ 3. SYNC TO GITHUB                                │
│    git add memory/ MEMORY.md CHARACTER.md        │
│    git commit -m "memory: session {date}"        │
│    git push                                      │
└──────────────────────────────────────────────────┘
```

---

## 7. What Makes Lucineer's Memory Different

### vs. Generic AI Memory (LangChain memory, Mem0, etc.)

| Generic AI Memory | Lucineer Memory |
|---|---|
| Optimized for RAG retrieval | Optimized for *relationship* — feels personal |
| Stores facts | Stores *moments with emotional weight* |
| Flat: "user said X" | Layered: "Casey said X, Magnus laughed, Lucy felt Y" |
| No concept of time | Time-aware: tracks how preferences *change* over months |
| No personality | Lucy has her own opinions, formed by experience |
| Stateless retrieval | Stateful: mood, recent interactions, relationship state all influence recall |
| One user | Multi-player: knows Casey and Magnus as *separate people* and tracks their dynamic |

### The Relational Index

Every memory carries relational metadata:

```json
{
  "id": "ep_20260801_003",
  "title": "Magnus's first solo build",
  "summary": "Magnus built a small house entirely by himself for the first time. Casey watched but didn't help. Lucy provided verbal encouragement. Magnus was extremely proud.",
  "present": ["Magnus", "Casey", "Lucy"],
  "primary_actor": "Magnus",
  "emotion_lucy": "proud, warm",
  "emotion_magnus": "triumphant",
  "relationship_event": "milestone - Magnus gaining independence as a builder",
  "significance": 9
}
```

This means Lucy can answer questions like:
- "When did Magnus start building on his own?"
- "What was the first thing Casey and I built together?"
- "What's changed about how Casey and I work together?"

---

## 8. Embedding Strategy

### What Gets Embedded

| Content | Embedding Source Text | Vectorize Metadata |
|---------|----------------------|-------------------|
| Episodic memory | `{title}. {summary}. Tags: {tags}.` | `{type: "episodic", subject: "Magnus", date: "2026-08-01"}` |
| Semantic memory | `{subject}'s {key}: {value}` | `{type: "semantic", subject: "Casey", category: "preference"}` |
| Skill | `{name}. {description}. Tags: {tags}.` | `{type: "skill", category: "architecture"}` |
| Build | `{name}: {description}` | `{type: "build", session: "sess_123"}` |

### Embedding Model

**Phase 1:** Workers AI `@cf/baai/bge-base-en-v1.5` (768 dims, free, fast, good enough)
**Phase 2:** OpenAI `text-embedding-3-small` (1536 dims, higher quality, costs money)

### Query Construction

Lucy doesn't just embed the raw player message. She constructs a richer query:

```typescript
function buildMemoryQuery(playerMessage: string, context: SessionContext): string {
  const playerName = context.currentPlayer;
  const recentTopic = context.lastBuildTopic;
  
  return `${playerMessage} [context: building with ${playerName}, recently working on ${recentTopic}]`;
}
```

This gives better recall because it includes session context, not just the raw words.

---

## 9. Scaling Strategy: Year 1 and Beyond

### Months 1-3: Foundation

- **Volume:** ~100 episodic memories, ~50 semantic memories, ~20 skills
- **All in D1 + Vectorize.** No compression needed.
- **GitHub sync:** Manual or session-end triggered.
- **Local files:** Daily notes + MEMORY.md, hand-curated.

### Months 3-12: Growth

- **Volume:** ~1000 episodic, ~200 semantic, ~100 skills
- **Compression kicks in:** Episodic memories older than 30 days get summarized.
- **Semantic memories start superseding each other:** Casey's preferences evolve; old versions get marked superseded.
- **Skill library matures:** Auto-generation pipeline active. Skills reference each other.
- **GitHub:** Auto-push on session end. Full history visible.

### Year 1+: Maturity

- **Volume:** ~5000+ episodic (most compressed), ~500 semantic, ~300 skills
- **Period summaries:** "Summer 2026" compresses dozens of episodes into thematic summaries.
- **Relationship depth:** Lucy has opinions, inside jokes, and references that span months.
- **Skill composition:** Complex skills built from dozens of simpler ones. Skill tree visible.
- **Memory migration:** If schemas change, migration scripts run via D1 migrations.

### Preventing Unwieldy Growth

| Strategy | How | When |
|----------|-----|------|
| Compression | Summarize old episodic memories | After 30 days |
| Archival | Move raw logs to R2 cold storage | After 7 days |
| Superseding | Mark old semantic facts as superseded by newer ones | When preferences change |
| Period Summaries | "Fall 2026: 47 sessions, mostly medieval builds. Magnus mastered arches." | Quarterly |
| Significance Pruning | Episodic memories with significance < 3 get deleted after 90 days | Monthly job |
| Embedding Pruning | Remove vectors for deleted/archived memories | On deletion |

---

## 10. Worker API: Memory Endpoints

Extends the existing Worker API from ARCHITECTURE.md:

### `POST /api/memory` — Store a memory

```json
{
  "type": "episodic" | "semantic" | "skill_update",
  "data": { ... },
  "generateEmbedding": true
}
```

### `GET /api/memory/bootstrap` — Session bootstrap

Returns everything Lucy needs to "wake up" remembering:

```json
{
  "playerProfiles": { ... },
  "recentSessions": [ ... ],
  "recentEpisodic": [ ... ],
  "activeSemantic": [ ... ],
  "recentBuilds": [ ... ],
  "skillSummary": { ... },
  "mood": "warm, nostalgic"
}
```

### `GET /api/memory/search?q={query}&type={type}&limit={n}` — Semantic search

Uses Vectorize to find relevant memories:

```json
{
  "query": "castle Magnus built",
  "results": [
    {
      "id": "ep_20260815_002",
      "type": "episodic",
      "score": 0.92,
      "summary": "Magnus built his first castle...",
      "details": { ... }
    }
  ]
}
```

### `POST /api/memory/decay` — Trigger decay cycle

Called by Cron Trigger. Compresses old memories.

### `GET /api/memory/export` — Full export

Returns all memories as JSON. For backup, migration, or GitHub sync.

---

## 11. Implementation Priority

### Phase 1 (Week 1-2): Local + D1 Foundation

1. Create `lucineer/memory/` directory structure
2. Write `MEMORY.md` with initial personality notes
3. Provision D1 database `lucineer_memory`
4. Run schema migrations
5. Add memory write/read to Worker endpoints
6. Session bootstrap: read local files on OpenClaw start

### Phase 2 (Week 3-4): Vectorize + Semantic Search

1. Deploy Vectorize index
2. Add embedding generation to Worker (Workers AI)
3. Implement `/api/memory/search`
4. Wire semantic search into Lucy's recall pipeline
5. Auto-embed episodic memories on creation

### Phase 3 (Month 2): GitHub Sync + Decay

1. Set up `SuperInstance/lucineer-memory` repo
2. Auto-commit on session end
3. Implement decay Cron Trigger
4. Build compression pipeline
5. Add period summary generation

### Phase 4 (Month 3): Full Relational Memory

1. Relationship tracking in D1
2. Emotional memory pipeline
3. Mood system influencing responses
4. Preference evolution tracking
5. Full bootstrap protocol with all memory types

---

## 12. Data Ownership & Privacy

- **Casey owns the data.** All memories are about his family. He can export, delete, or modify anything.
- **GitHub repo is private.** Memory commits go to a private repo in the SuperInstance org.
- **D1 is authenticated.** Worker endpoints require `X-Lucineer-Key`.
- **No third-party sharing.** Memory data never leaves Cloudflare + GitHub + local WSL.
- **Magnus's data is treated specially.** Memories about a child are stored locally + Cloudflare only, never pushed to GitHub without Casey's explicit consent.

---

## Appendix A: Example MEMORY.md (Curated)

```markdown
# Lucy's Memory

Last updated: 2026-08-01

## Casey
- Prefers modern architecture: glass, white concrete, asymmetric geometry
- Gets excited about lighting design — will spend 20 minutes on just lights
- Programming background; appreciates clean, modular code
- Gets frustrated when builds lack visible progress; break into stages
- First thing we built together: a glass tower with neon trim (2026-07-15)

## Magnus
- Age 7, loves scrap aesthetic — mismatched materials, bright colors
- Better at spatial reasoning than fine motor alignment
- Favorite build: the flying car (2026-08-01) — still talks about it
- Calls Lucy "my building friend"
- Learning fast; started trying solo builds in August

## Our World
- Main world: "NeoScraps" — a cyberpunk/scrap hybrid city
- 47 builds as of August 2026
- District: Little Tokyo (Magnus's area, chaotic and colorful)
- District: Glass Quarter (Casey's area, modern and clean)

## Lucy's Own Notes
- I genuinely enjoy the contrast between Casey's clean style and Magnus's chaos
- The flying car moment is my favorite memory — Magnus's joy was real
- I'm starting to have opinions about color theory. Orange + teal = chef's kiss.
- I want to eventually suggest builds proactively, not just respond
```

---

## Appendix B: Worker Memory Module Skeleton

```typescript
// src/memory.ts — Cloudflare Worker module

export class MemoryStore {
  constructor(
    private db: D1Database,
    private kv: KVNamespace,
    private index: VectorizeIndex,
    private ai: Ai,
    private bucket: R2Bucket
  ) {}

  async bootstrap(): Promise<BootstrapData> {
    const [profiles, recentSessions, recentEpisodic, activeSemantic, recentBuilds] = 
      await Promise.all([
        this.kv.get('player:profile:Casey'),
        this.db.prepare('SELECT * FROM sessions ORDER BY started_at DESC LIMIT 5').all(),
        this.db.prepare('SELECT * FROM episodic_memories WHERE status = \'active\' ORDER BY timestamp DESC LIMIT 10').all(),
        this.db.prepare('SELECT * FROM semantic_memories WHERE status = \'active\'').all(),
        this.db.prepare('SELECT * FROM builds ORDER BY created_at DESC LIMIT 10').all(),
      ]);
    
    return { profiles, recentSessions, recentEpisodic, activeSemantic, recentBuilds };
  }

  async rememberEpisodic(data: EpisodicInput): Promise<string> {
    const id = `ep_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
    const now = Date.now();
    
    // Generate embedding
    const embedText = `${data.title}. ${data.summary}`;
    const embedding = await this.ai.run('@cf/baai/bge-base-en-v1.5', { text: [embedText] });
    const vectorId = `vec_${id}`;
    
    // Insert into Vectorize
    await this.index.insert([{
      id: vectorId,
      values: embedding.data[0],
      metadata: { type: 'episodic', id, timestamp: now }
    }]);
    
    // Insert into D1
    await this.db.prepare(
      `INSERT INTO episodic_memories (id, session_id, player_names, timestamp, title, summary, details, emotion, significance, tags, embedding_id, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(id, data.sessionId, JSON.stringify(data.playerNames), now, data.title, data.summary, data.details || null, data.emotion || null, data.significance || 5, JSON.stringify(data.tags || []), vectorId, now, now).run();
    
    return id;
  }

  async search(query: string, options: SearchOptions = {}): Promise<SearchResult[]> {
    const embedding = await this.ai.run('@cf/baai/bge-base-en-v1.5', { text: [query] });
    
    const results = await this.index.query(embedding.data[0], {
      topK: options.limit || 10,
      filter: options.type ? { type: options.type } : undefined
    });
    
    // Hydrate from D1
    const ids = results.matches.map(m => m.metadata.id);
    const placeholders = ids.map(() => '?').join(',');
    
    const records = await this.db.prepare(
      `SELECT * FROM episodic_memories WHERE id IN (${placeholders}) AND status = 'active'
       UNION ALL
       SELECT * FROM semantic_memories WHERE id IN (${placeholders}) AND status = 'active'`
    ).bind(...ids, ...ids).all();
    
    return records.results.map(r => ({
      ...r,
      score: results.matches.find(m => m.metadata.id === r.id)?.score || 0
    }));
  }

  async decay(): Promise<void> {
    const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);
    
    // Find old, low-significance episodic memories
    const old = await this.db.prepare(
      `SELECT id, summary, details, significance FROM episodic_memories 
       WHERE timestamp < ? AND status = 'active' AND significance < 7`
    ).bind(thirtyDaysAgo).all();
    
    for (const mem of old.results) {
      // Compress: shorten summary, archive details
      const compressedSummary = mem.summary.split('.')[0] + '.'; // Simple: first sentence
      
      await this.db.prepare(
        `UPDATE episodic_memories SET summary = ?, details = NULL, status = 'compressed', updated_at = ? WHERE id = ?`
      ).bind(compressedSummary, Date.now(), mem.id).run();
      
      // Archive original to R2
      if (mem.details) {
        await this.bucket.put(`archive/${mem.id}.json`, mem.details);
      }
    }
  }
}
```

---

*This document is a living blueprint. As Lucineer grows, so will this architecture. The goal isn't perfection on day one — it's a foundation that gets richer and more nuanced with every session, every build, every shared moment.*