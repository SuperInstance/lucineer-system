# Murmur-Agent — Deep Dive Analysis

## What It Does
A **budget-agnostic, local-first, git-native thinking agent** that runs sustained iterative exploration on any topic. You give it a topic, it thinks in cycles using 5 complementary strategies, and every thought becomes a git commit with a markdown file. Designed for overnight/long-running research sessions.

## Architecture
- **TypeScript** (Node.js ≥18) + **C CLI** (zero-dependency, POSIX)
- **Core Modules**:
  - `Thinker` (`engine/thinker.ts`): Main orchestrator. Cycles through strategies, enforces budget, writes output, persists state.
  - `Strategies` (`engine/strategies.ts`): 5 thinking strategies (explore, connect, contradict, synthesize, question)
  - `BudgetTracker` (`engine/budget.ts`): API call/token budget management with daily limits, accumulate/reset strategies, auto date rollover
  - `OutputWriter` (`output/writer.ts`): Writes thoughts as markdown/JSON, serializes knowledge tensor, generates summaries
- **Knowledge Tensor**: Evolving data structure tracking thoughts, clusters, contradictions, open questions, total tokens
- **Git Integration**: Each thought → markdown file + git commit on `murmur/thinking` branch

## The 5 Thinking Strategies
1. **Explore** (0.60-0.80 confidence): Breadth-first search, picks from 10 candidate angles (historical origins, cross-domain applications, failure modes, etc.)
2. **Connect** (0.50-0.80): Picks 2 random prior thoughts, finds conceptual bridges
3. **Contradict** (0.50 fixed): Contrasts highest vs lowest confidence thoughts to find blind spots
4. **Synthesize** (0.40-0.90, grows): Counts recurring themes, identifies patterns, assesses maturity
5. **Question** (0.30-0.60): Meta-cognitive Socratic questioning ("What are we not asking?")

Strategy selection cycles through all 5 with 20% chance of repeating for depth.

## Key Innovations
1. **Knowledge Tensor**: Not just a list of thoughts — tracks clusters, contradictions between thoughts, and open questions. Self-organizing.
2. **Budget-Agnostic Design**: Works with unlimited API (OpenAI/Anthropic), budgeted API (daily limits with rollover), local models (Ollama), or no LLM at all (pure heuristic strategies).
3. **Git-Native Persistence**: Every thought is a commit. Every commit is a training snapshot. Rewind to any point = valid state. This is training data as a side effect.
4. **Session State Save/Load**: Full tensor + budget + thought count serialization for crash recovery and long-running sessions.
5. **Dual Implementation**: TypeScript for development machines, C CLI for edge devices (Raspberry Pi, Jetson). Same commands, different runtimes.
6. **Fleet Integration**: CHARTER.md, STATE.md, DOCKSIDE-EXAM.md, BOOTCAMP.md. Bottle messages via for-fleet/from-fleet directories. Tender-compatible (offline, shallow clone, portable state).
7. **Scout-Class Agent**: Operates on Plane 2 (Pattern) of the fleet abstraction framework — finds and amplifies patterns.

## Code Quality
- **Excellent**: 50+ tests, clean interfaces, fully typed
- **Modular**: Each component (Thinker, Budget, Strategies, Writer) is independently usable
- **Documented**: Comprehensive README with architecture diagrams, API reference, use cases
- **Practical**: Strategies produce genuinely useful structured output, not just placeholder text

## DCA / Slackwater Integration Points
- **Thinking Loop Pattern**: Gather → Think → Write → Commit → Rest → Repeat. Maps to DCA's observe-plan-act cycle.
- **Budget Tracker**: Critical for DCA cost management — same accumulate/reset strategies needed.
- **Knowledge Tensor → DCA Memory**: Clusters, contradictions, open questions — exactly what DCA's memory system needs.
- **5-Strategy Cycle**: Explore/Connect/Contradict/Synthesize/Question is a powerful meta-cognitive framework for any agent.
- **Git-as-State**: Every state change is a commit — perfect for audit trails and rollback.
- **Bottle Messages**: File-based inter-agent communication protocol.

## Patterns to Adopt
1. **Strategy-based thinking cycles** — 5 complementary approaches prevent tunnel vision
2. **Knowledge tensor with clusters + contradictions** — structured evolving memory
3. **Budget-agnostic operation** — graceful degradation from expensive LLM to free heuristics
4. **Git-native state** — every thought is a commit, every commit is a snapshot
5. **Bottle message directories** — simple, resilient, file-based async communication
6. **Session save/load** — critical for long-running processes
7. **Dual implementation strategy** — high-level for dev, low-level for edge
8. **20% repeat-for-depth** — occasional strategy repetition prevents shallow cycling
