# superinstance-agent — Slackwater Integration Plan

## Core Game Mechanic: "The Oracle"

The RAG agent becomes the **Oracle** — an in-game NPC that players can ask questions about the game world, other agents, and the ecosystem. The Oracle doesn't know everything — it knows what it can retrieve from its embedded knowledge base.

### Mechanic 1: Knowledge Base as Discoverable Content

**In-game:** The Oracle's Vectorize index is populated with game world knowledge — NPC profiles, location descriptions, item properties, historical events, quest information. As the player explores, new content gets embedded and added to the index.

**Player interaction:**
- Ask the Oracle questions in natural language
- The Oracle retrieves relevant knowledge and generates an answer
- Quality of answer depends on what's in the knowledge base
- Players can "teach" the Oracle by providing new information (books, artifacts, observations)

### Mechanic 2: Conservation of Information (γ + η = C for RAG)

**In-game:** The Oracle has a conservation constraint — the information demand of the question (γ) must be met by the information supply of the answer (η). If the knowledge base doesn't have enough relevant content, the answer is incomplete.

**Player interaction:**
- The Oracle visibly strains when asked about unknown topics (low η — conservation violation)
- Players see a "knowledge confidence" meter on Oracle responses
- Completing the Oracle's knowledge base becomes a meta-game (collect all the lore)

### Mechanic 3: Embedding-as-Identity for NPCs

**In-game:** Every NPC, location, and item has a semantic embedding (their γ-component). When an agent encounters something, it sends a probe (η) that matches against the embedding. This determines recognition — agents "recognize" things that are semantically close to their training.

**Player interaction:**
- NPCs react differently based on semantic similarity to things they know
- A guard trained on "threats" will recognize a sword as weapon-like even if it's a novel type
- Show this as a "recognition aura" — familiar things glow, unfamiliar things are dark

### Mechanic 4: Multi-Model Routing

**In-game:** Different agents use different AI models for different tasks, just as superinstance-agent routes between BGE (fast retrieval) and Llama (deep generation). In Slackwater:

- **Fast agents** (guards, workers) use simple pattern matching (BGE-equivalent)
- **Deep agents** (story NPCs, quest givers) use full LLM reasoning (Llama-equivalent)
- The Conductor routes questions to the appropriate tier based on complexity

**Player interaction:** Players learn which agents can handle complex questions vs simple ones. Asking a guard about cosmic philosophy gets a confused response; asking a sage gets a thoughtful one.

### Mechanic 5: The Debug Report as "Corruption"

The DEBUG-REPORT.md from the real repo (metadata field name mismatch causing empty descriptions) becomes a game mechanic:

**In-game:** Agent knowledge can become corrupted — field mismatches, degraded embeddings, stale data. Players encounter agents who "know" things but can't articulate them (empty description bug as a narrative device).

**Player interaction:**
- Diagnose corrupted agents (mini-game: identify which metadata fields are wrong)
- Fix corruption by providing the correct mappings
- Corrupted agents give garbled quest info until repaired

## Implementation: Thinker Architecture

The superinstance-agent directly informs the **Thinker** component design:

```
Player/NPC Request
    ↓
[Local Embedding (BGE or lighter)] → semantic vector
    ↓
[Vector Search (local or cloud)] → relevant context
    ↓
[LLM Generation (cloud or edge)] → response
    ↓
Answer + Confidence Score
```

### Cost-Conscious Implementation

Using the routing strategy from TOOLS.md:
- **Local/cheap**: Embeddings via Cloudflare Workers AI (BGE-small)
- **Cloud/medium**: Generation via GLM-5.2 (Z.ai Max plan, unlimited)
- **Premium/rare**: DeepSeek-V3 for complex reasoning quests

## Implementation Priority: MEDIUM-HIGH

The Thinker is the brain of individual agents. It needs the communication protocol (Plato) and fleet coordinator (Cocapn) first, but it's the system that makes agents feel alive.

## Roblox/Lua Implementation Notes

- Embedding search via Cloudflare Worker relay (already have Lucineer Relay Worker)
- Local pattern matching for fast agents (simple keyword/intent detection)
- Full RAG only for named story NPCs
- Cache responses for common queries
- Conservation meter: if retrieval score < threshold, show "uncertainty"
