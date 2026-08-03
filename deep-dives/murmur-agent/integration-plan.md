# Murmur-Agent → DCA Integration Plan

## Phase 1: Thinking Engine
- Port the 5-strategy thinking cycle to DCA's agent orchestrator
- Each DCA agent gets a Knowledge Tensor (thoughts, clusters, contradictions, open questions)
- Strategy selection adapts to agent role (researcher = explore-heavy, reviewer = contradict-heavy)
- Configurable strategy pools per agent type

## Phase 2: Budget Management
- Adopt the BudgetTracker for all DCA LLM calls
- Daily limits with accumulate/reset strategies
- Per-agent and fleet-wide budget tracking
- Auto-rollover for overnight sessions
- Budget-aware routing (switch to cheaper models when budget is low)

## Phase 3: Git-Native State
- Every DCA agent action → git commit on a dedicated branch
- State snapshots as JSON in commits (tensor, budget, progress)
- Rewind capability via `git checkout`
- Fork/branch for alternative approaches
- Commit history = training data for future model fine-tuning

## Phase 4: Inter-Agent Communication
- Adopt bottle message directories (for-fleet/from-fleet)
- File-based async messaging — no network dependency
- Tender protocol for servicing offline/edge agents
- Standardized fleet certification (DOCKSIDE-EXAM)

## Phase 5: Session Management
- Full save/load for any agent session
- Crash recovery via state files
- Long-running sessions (overnight research, sustained analysis)
- Export to markdown/JSON for human review

## Key Source Files
- `src/engine/thinker.ts` — orchestration pattern
- `src/engine/strategies.ts` — 5 thinking strategies
- `src/engine/budget.ts` — budget tracking
- `src/output/writer.ts` — file persistence
- `src/types.ts` — all interfaces and DEFAULT_CONFIG
- `CHARTER.md` — agent identity format
- `DOCKSIDE-EXAM.md` — fleet certification
