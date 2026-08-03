# nebula-docs — Deep Dive Analysis

## What It Does
Documentation for the **Edge Reflex Engine** — a Cloudflare Workers-deployed agent that parses intent and generates responses at the edge. The gap between "I want..." and "Done" measured in seconds.

## Architecture
- **Three Response Paths**:
  - **Fast Path** (~700ms): Known intent resolves from KV cache — no LLM call needed
  - **Similar Path** (~800ms): LLM confirms and adapts a cached response
  - **Slow Path**: Full LLM call via DeepInfra (DeepSeek V4 Flash)

### The Pipeline
```
Human: "I want a crate that does X"
  → Nebula: teaches reflex, spawns sub-agent
  → Sub-agent: creates crate via Claude Code
  → GitHub: repo created, CI runs tests
  → Nebula: reports "Done. Here's what exists."
```

### Timing Targets
- Intent → Action: ~700ms (fast path reflex)
- Intent → Built Crate: ~2-5 minutes (sub-agent + Claude Code)
- Intent → Shipped: ~5-10 minutes (+ CI + docs)
- **Goal: Intent → Shipped < 60 seconds** for simple cases

### Integration Points
| System | Role | Status |
|--------|------|--------|
| Cloudflare Workers | Intent parser + reflex engine | ✅ Live |
| Cloudflare KV | Reflex storage + caching | ✅ Live |
| Cloudflare DO | Agent coordination | ✅ Registered |
| GitHub | Repo creation + CI/CD | ✅ Live |
| Notion | Dashboard + activity log | ⚡ Wiring |
| Codespaces | x86_64 compute on demand | ✅ Proven |
| I2I vessel | Agent-to-agent protocol | ✅ Active |

### Embeddings
- BGE base (384-dim) via DeepInfra
- Used for intent matching in the "similar path"

## Key Innovations
1. **Three-Tier Response Latency**: Fast (cached reflex), Similar (LLM-confirmed adaptation), Slow (full LLM). This maps to DCA's need for tiered response urgency.
2. **Reflex Library**: Known intents get cached responses. The library grows → future requests are instant. This is institutional learning.
3. **Intent → Built Pipeline**: From conversation to shipped code with sub-agents. The human never leaves the conversation.
4. **Edge Deployment**: Runs at the Cloudflare edge — close to the user, low latency.
5. **Sub-Agent Spawning**: Nebula teaches reflexes, spawns sub-agents for execution. Clean separation of planning and execution.

## Code Quality
N/A — this is a documentation repository. Contains README.md, AGENT.md, and JOURNAL.md only.

## DCA / Slackwater Integration Points
- **Three-Tier Response → DCA Latency Tiers**: Map to DCA's heartbeat vs real-time vs batch processing.
- **Reflex Library → DCA Cached Responses**: Known intents get instant responses from cache. Growth over time.
- **Sub-Agent Spawning → DCA Task Delegation**: Main agent delegates execution to specialized sub-agents.
- **Edge Deployment → DCA Proximity**: Process at the edge for low-latency responses.

## Patterns to Adopt
1. **Three-tier latency strategy** — fast (cache), similar (LLM confirm), slow (full LLM)
2. **Reflex library growth** — cached responses expand coverage over time
3. **Intent → action → shipped pipeline** — minimize human wait time
4. **Sub-agent delegation** — planner spawns executors
5. **Don't make the human leave the conversation** — UX principle for all interactions
