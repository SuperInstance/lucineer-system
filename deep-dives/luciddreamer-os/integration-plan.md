# luciddreamer-os → DCA Integration Plan

## Phase 1: Provider Abstraction Layer
- Port the dual-path LLM call pattern (Ollama local vs cloud API)
- Same interface for all providers
- Automatic path selection based on availability and task requirements
- Per-agent provider configuration

## Phase 2: Negative Prompts
- Add negative prompt support to all DCA agents
- Constraints specified as "what NOT to do" alongside system prompts
- Per-role constraint templates
- Validation that outputs don't violate negative prompts

## Phase 3: Task Breakdown Mode
- Automatic decomposition of complex tasks into atomic steps
- "Breakdown" flag on any task triggers step decomposition before execution
- Steps executed sequentially or in parallel based on dependencies
- Progress tracking per step

## Phase 4: Real-Time Status
- WebSocket-based agent status updates
- Live "thinking..." / "responding..." indicators
- Agent activity feed for dashboards

## Key Source Files
- `orchestrator.js` — multi-agent orchestration pattern
- `server.js` — Express + Socket.IO setup
- `config.json` — provider configuration format
