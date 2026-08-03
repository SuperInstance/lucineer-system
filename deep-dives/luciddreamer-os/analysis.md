# luciddreamer-os — Deep Dive Analysis

## What It Does
A **concept OS for dream visualization and orchestration**. Currently minimal — an Express.js server with a Socket.IO-based orchestrator that routes messages to multiple AI agents via configurable providers (Ollama for local, OpenAI-compatible APIs for cloud).

## Architecture
- **server.js**: Express + Socket.IO server
- **orchestrator.js**: Core class that manages multi-agent conversations
  - Maintains agent list with system prompts, negative prompts, temperature settings
  - Routes messages to active agents sequentially
  - Supports "breakdown" workflow mode (break task into atomic steps)
  - Dual-path LLM calls: Ollama (local) vs OpenAI-compatible (cloud)

## Key Features
1. **Multi-Agent Orchestration**: Multiple agents with different providers, system prompts, and parameters
2. **Provider Abstraction**: Works with Ollama (local), OpenAI, Anthropic, or any OpenAI-compatible API
3. **Breakdown Mode**: Tasks can be broken into atomic steps before execution
4. **Negative Prompts**: Per-agent constraint specifications (what NOT to do)
5. **Real-time**: Socket.IO for live agent status updates and message streaming

## Code Quality
- **Minimal/Early-stage**: README acknowledges "In Progress" status
- **Functional**: The orchestrator works but is basic — sequential agent calls, no parallel execution
- **Notable**: Clean provider abstraction pattern, negative prompt support

## DCA / Slackwater Integration Points
- **Provider Abstraction**: The Ollama-vs-cloud path selection maps to DCA's model routing
- **Negative Prompts**: Per-agent constraints — what the agent should NOT do
- **Breakdown Mode**: Automatic task decomposition into atomic steps
- **Socket.IO Real-time**: Live agent status updates (thinking, responding)

## Patterns to Adopt
1. **Provider abstraction with dual-path** — local (Ollama) vs cloud (API) with same interface
2. **Negative prompts** — constraint specification alongside system prompts
3. **Breakdown workflow** — automatic task decomposition into atomic steps
4. **Real-time status** — agent thinking/responding status via WebSocket
