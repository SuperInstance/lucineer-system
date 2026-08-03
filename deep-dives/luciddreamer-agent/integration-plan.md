# luciddreamer-agent → DCA Integration Plan

## Phase 1: Pattern Frequency Tracking
- Port dream sign frequency tracking to DCA's memory system
- Track recurring patterns in agent behavior, user requests, task types
- Rank patterns by frequency for pattern-aware recommendations
- Use frequency as a signal for automation opportunities

## Phase 2: Adaptive Strategy Recommendation
- Track success rates per strategy (like trigger success rates)
- Suggest strategies based on historical performance
- Default effectiveness estimates shift to actual success rates once data accumulates
- Per-domain strategy tracking (different strategies work for different task types)

## Phase 3: Session-Based Memory
- Group related agent actions into sessions
- Each session has quality metrics (like sleep quality)
- Patterns within sessions tracked and cross-referenced
- Statistics aggregation across sessions

## Phase 4: Honest Documentation
- Follow the pattern of clearly separating implemented features from aspirational ones
- Reserved parameters documented as "not yet implemented"
- README accuracy as a quality signal

## Key Source Files
- `luciddreamer_agent/__init__.py` — all classes and logic
- `tests/test_luciddreamer_agent.py` — comprehensive tests
