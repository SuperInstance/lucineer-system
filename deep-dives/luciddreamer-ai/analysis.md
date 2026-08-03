# luciddreamer-ai — Deep Dive Analysis

## What It Does
A Cloudflare Worker powering a **fleet infotainment streaming platform** — auto-generates stories, tutorials, reviews, changelogs, and deep dives about fleet projects. Think "TikTok for developer tools" or "Spotify for AI app discovery." Audio-first content you can listen to while driving, with a visual pipeline from storyboard to video.

## Architecture (Massive Single Worker)
- **~1000-line worker.ts** — full HTTP router, content generation, streaming algorithm, knowledge graph, discourse engine, podcast engine
- **3 KV Namespaces**: PODCAST_KV, CONTENT (content:prefix + hit:prefix), VIDEOS
- **4-Provider LLM Failover**: DeepSeek → Moonshot → DeepInfra → SiliconFlow. Sequential with silent failover.
- **Content Types**: story, tutorial, insight, changelog, synthesis, greatest-hit, review, deep-dive
- **5 Characters**: Navigator (narrator), Builder (tutorials), Herald (changelogs), Skeptic (critic), Critic (reviewer)

### Content Economy / Discovery Algorithm
```
Score = votes·2 + log2(hits+1)·3 + recency·20 + trending·30 + new-creator·15 + canon·100
        × quality_weight + type_bonus
```
- Recency uses exponential decay (half-life 3 days)
- Trending = high velocity in last 24h
- Greatest-hit promotion based on hits (≥10) or votes (≥5)

### Storyboard / Visual Pipeline
- Each content piece → 4-8 storyboard slides via LLM
- Slides specify: scene type, mood, camera angle, camera motion, lighting, sprite positions
- Video projects with scenes, avatar positions, CAD-style animation scripts
- 4 animation styles: slides, sprite-animated, game-engine, ai-video

### Reactive Improv Engine (`reactive-improv.ts`)
Multi-agent discourse with musical timing:
- **Tensor MIDI Clock**: BPM-based discourse timing (60-120 BPM range, adapts to energy)
- **Nudge System**: Agents react to each other in real-time (pushback, question, excitement, topic-shift)
- **Draft System**: Each agent maintains a draft that gets reactively re-drafted based on nudges
- **T-Minus Event Scheduling**: Future speaking events scheduled on beats with swing
- **Cadence Profiles**: Per-agent speech patterns (sentence length, gap, energy, vocabulary type)

### Knowledge Graph
- Cross-domain queries: addNode, addEdge, traverse (BFS), findPath (shortest path)
- Domain statistics and cross-domain semantic search
- Seed loader loads fleet repos into the KG

### Dream Cycle (Scheduled)
Runs on Cloudflare cron trigger:
1. Explore queued directions
2. Weekly changelog
3. Random tutorial
4. Vessel review (every 2 days)
5. Video project (every 3 days)
6. Promote high-hit content to greatest-hit

## Key Innovations
1. **Multi-Provider LLM Failover**: Silent sequential failover across 4 providers — if one is down, next picks up. O(P×T) worst case, O(T) best case.
2. **Content Economy**: Full recommendation algorithm with trending, greatest-hits, new-creator boost, quality weighting. Not just generation — curation.
3. **Reactive Improv (Tensor MIDI)**: Discourse timed to musical beats. BPM adapts to conversation energy. Agents nudge and re-draft each other reactively. This is genuinely novel.
4. **γ + η = C Principle**: Creative (γ) transforms raw knowledge (η) into accessible content (C). Recursive: each layer's output becomes the next layer's input.
5. **Storyboard → Video Pipeline**: Full visual specification including camera angles, lighting, sprite positions, avatar blocking — production-ready scene descriptions.
6. **Confidence Tracking**: Generated claims tracked for reliability based on source, corroboration, recency, authority.
7. **BYOK (Bring Your Own Key)**: Users can fork the platform and plug in their own API keys.
8. **Clone-to-Deploy**: Any reviewed content can be forked into a user's own instance.

## Code Quality
- **Functional but dense**: 1000+ line worker with everything inline. Works, but would benefit from modularization.
- **No tests** beyond a single test file for reactive-improv
- **Security-conscious**: CSP headers, CORS handling, OPTIONS preflight
- **Real-time**: SSE streaming for podcast generation, reactive improv ticks
- **HTML generated inline**: Complete styled pages without a frontend framework

## DCA / Slackwater Integration Points
- **Multi-Provider Failover → DCA Model Routing**: The 4-provider sequential failover maps exactly to DCA's need for resilient LLM calls.
- **Content Economy → DCA Knowledge Ranking**: Not all knowledge is equal. Scoring + curation for agent memory.
- **Reactive Improv → Multi-Agent Coordination**: Musical timing for discourse, nudge-based reactive re-drafting. Novel approach to agent turn-taking.
- **Storyboard → DCA Output Formatting**: Structured output specification (scene, mood, camera, lighting) for generating rich media.
- **Dream Cycle → DCA Scheduled Tasks**: The cron-triggered batch generation pattern with content promotion.
- **Knowledge Graph → DCA Memory Topology**: Cross-domain semantic linking of concepts.
- **Character System → DCA Agent Personas**: Distinct personalities with voices, catchphrases, relationships.

## Patterns to Adopt
1. **Sequential multi-provider failover** — resilient LLM calls with silent degradation
2. **Content scoring algorithm** — weighted composite with recency decay, trending detection
3. **Tensor MIDI Clock** — musical timing for multi-agent discourse
4. **Nudge system** — reactive inter-agent influence (agreement, pushback, question, excitement)
5. **Draft + re-draft** — agents maintain evolving drafts, not fixed positions
6. **γ + η = C recursive composition** — each transform's output feeds the next
7. **Greatest-hit promotion** — auto-promote high-value content based on engagement
8. **Cron-triggered dream cycle** — periodic batch content generation
9. **Inline HTML generation** — server-rendered styled pages without frontend framework overhead
