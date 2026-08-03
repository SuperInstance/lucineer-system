# lucid-tutor → DCA Integration Plan

## Phase 1: Agent Competence Tracking
- Each DCA agent gets a `Vibration` per skill domain
- Level = current mastery (-1.0 to 1.0)
- Velocity = rate of improvement (derivative of level)
- Topic mastery with iteration count, breakthroughs, stuck count
- Persisted in agent state files

## Phase 2: Adaptive Strategy Selection
- Track agent velocity across recent tasks
- Fast velocity (>0.1) → Socratic mode (challenge, ask questions)
- Slow velocity (<-0.05) → Guide mode (hints, redirect)
- Stable → Experimental mode (autonomy, learn from failure)
- Velocity-based routing of tasks to agents

## Phase 3: Agent Resonance Matching
- Compute resonance between agents based on shared skill topics
- Pair agents with high resonance for collaborative tasks
- Pair agents with complementary strengths for diverse tasks
- Suggest collaborations when both agents are stuck on same topic

## Phase 4: Teaching Moment System
- Every agent action produces a TeachingMoment
- Types: Celebration, Redirect, Connection, Hint, Collaborate, Deepen, LevelUp, Patience
- Feed into agent self-improvement loop
- Surface key moments to the user

## Phase 5: Breakthrough Detection
- Flag when an agent suddenly excels at a previously weak skill
- Capture the context (what triggered the breakthrough)
- Propagate the insight to other agents
- Build a "breakthrough patterns" library

## Key Source Files
- `src/lib.rs` — all types and logic (Vibration, Tutor, LearningGroup, TeachingMoment)
- 20 tests covering all functionality
