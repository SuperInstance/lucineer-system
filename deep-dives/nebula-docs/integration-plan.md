# nebula-docs → DCA Integration Plan

## Phase 1: Three-Tier Response System
- **Fast Path**: Cache common agent responses, serve from KV/memory (<1s)
- **Similar Path**: Embedding-based intent matching with LLM confirmation (~1s)
- **Slow Path**: Full LLM reasoning for novel requests (2-10s)
- Route automatically based on confidence and cache hit

## Phase 2: Reflex Library
- Build a growing cache of validated agent responses
- Intent → response mapping stored in KV or local files
- Coverage expands over time as more requests are handled
- Automatic cache invalidation when underlying data changes

## Phase 3: Sub-Agent Delegation
- Main DCA orchestrator handles intent parsing
- Spawns specialized sub-agents for execution
- Results flow back to the orchestrator
- Human stays in the conversation throughout

## Phase 4: Embedding-Based Intent Matching
- Embed all incoming requests (BGE base, 384-dim)
- Match against historical intents
- If similar intent found, adapt cached response
- Much faster than full LLM for common patterns

## Phase 5: Edge Processing
- Deploy DCA response layer at the edge (Cloudflare Workers)
- KV for reflex storage
- Durable Objects for agent coordination
- Minimize latency for common requests

## Key Source Files
- `README.md` — architecture and pipeline description
- `AGENT.md` — agent configuration
