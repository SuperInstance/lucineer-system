# luciddreamer-ai → DCA Integration Plan

## Phase 1: Multi-Provider LLM Routing
- Port the 4-provider sequential failover to DCA's LLM call layer
- Add DeepSeek, Moonshot, DeepInfra, SiliconFlow as providers
- Silent failover on provider errors
- Track per-provider latency and success rates
- Cost-aware routing (prefer cheaper providers first)

## Phase 2: Content Economy for Agent Memory
- Score agent outputs: votes (user feedback) + hits (reuse count) + recency + quality
- Auto-promote high-value outputs to "greatest-hit" status
- Exponential recency decay (3-day half-life) for relevance scoring
- Trending detection for hot topics in agent work

## Phase 3: Reactive Improv for Multi-Agent Discourse
- Port TensorMidiClock for timed discourse
- Implement nudge-based reactive communication between DCA agents
- Draft + re-draft pattern: agents maintain evolving positions
- BPM adapts to fleet energy level
- Swing timing for natural conversation rhythm

## Phase 4: Knowledge Graph
- Cross-domain concept linking in DCA's memory system
- Domain statistics, path finding, semantic search
- Seed loader for ingesting project documentation
- Confidence tracking for all claims (source reliability, corroboration)

## Phase 5: Storyboard Output
- Structured output format for DCA tasks: scene, mood, camera, lighting, sprite positions
- Video project pipeline: script → storyboard → slides → animation
- Character system for agent personas (personality, voice, catchphrases, backstory)

## Phase 6: Dream Cycle
- Periodic cron-triggered batch processing
- Explore queued directions, generate content, promote hits
- Weekly summaries, daily tutorials, regular reviews
- Automatic content lifecycle management

## Key Source Files
- `src/worker.ts` — main router, content generation, discovery algorithm
- `src/reactive-improv.ts` — Tensor MIDI clock, nudge system, discourse engine
- `src/discourse-handler.ts` — discourse API handlers
- `src/landing.ts` — landing page
- `vessel.json` — vessel metadata
