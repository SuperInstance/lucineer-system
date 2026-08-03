# lucid-tutor (Rust) — Deep Dive Analysis

## What It Does
An **endless tutor engine** implementing vibration-based learning. Tracks each learner's "vibration" (understanding level + velocity + topic mastery) and generates teaching moments adapted to their state. Supports collaborative learning groups with resonance-based pairing. The mathematical foundation for the LucidDreamer.ai education platform.

## Architecture
- **Single Rust crate** (`src/lib.rs`, ~600 lines + comprehensive tests)
- **Core Types**:
  - `Vibration`: level (-1.0 to 1.0), velocity (rate of change), topics HashMap
  - `TopicMastery`: level, iterations, last_touch_tick, breakthroughs, stuck_count
  - `Tutor`: id, style, learner_vibrations map, teaching_history, tick counter, patience_threshold
  - `TeachingMoment`: tick, topic, kind, message, difficulty, next_hint
  - `LearningGroup`: members, shared_topics, group_vibration, iterations_together

### Vibration System
- `level`: -1.0 (confused) to 1.0 (mastery), averaged across all topics
- `velocity`: rate of change in overall level — used by adaptive tutor style
- `resonance_with()`: cosine-like similarity between two vibrations based on shared topics
- `iterate()`: Feed a result (0.0-1.0), get an IterationOutcome (Breakthrough/Progress/Plateau/Stuck)

### Tutor Styles
- **Guide**: Patient, encouraging, gives hints when stuck
- **Socratic**: Challenging, asks questions, deepens after progress
- **Experimental**: Hands-off, lets you fail, teaches from failure
- **Adaptive**: Switches style based on learner velocity (fast → Socratic, slow → Guide, stable → Experimental)

### Teaching Moment Types
Celebration (breakthrough!), Redirect (try another angle), Connection (link to prior work), Hint (specific nudge), Collaborate (work with a peer), Deepen (go deeper), LevelUp (ready for next), Patience (sit with it)

### Iteration Outcome Logic
- **Breakthrough**: result > 0.8 AND old_level < 0.5 → +0.3 level boost
- **Stuck**: result < 0.3 AND iterations > 3 → stuck_count++
- **Progress**: result > old_level → moderate improvement
- **Plateau**: result ≤ old_level → connection hint

### Learning Groups
- `iterate_together()`: Multiple members learn from shared experience
- `coherence()`: Pairwise resonance averaged across all member pairs
- Group vibration = shared state across members

## Key Innovations
1. **Vibration as Scalar State**: One number captures understanding. Negative = confused, zero = neutral, positive = mastery. Simple, verifiable.
2. **Resonance-Based Pairing**: Learners matched by similarity in topic mastery — not skill level, but *how they think about shared topics*.
3. **Adaptive Tutor Style**: Switches pedagogical approach based on learner velocity. Fast learners get challenged (Socratic), struggling learners get guided.
4. **Collaboration Suggestions**: When two learners are stuck on the same topic and have high resonance, suggest collaboration. Social learning driven by data.
5. **Breakthrough Detection**: Sudden jumps from low mastery to high result are flagged as breakthroughs — celebrated and reinforced.
6. **Stuck Detection with Patience Threshold**: Won't intervene immediately when a learner is stuck — waits `patience_threshold` iterations. Respects the learning process.

## Code Quality
- **Excellent**: 20 comprehensive tests, clean Rust, full serde serialization
- **Mathematically grounded**: Resonance as cosine similarity, velocity as derivative
- **Practical**: Teaching messages are actually useful, not just placeholder text
- **Extensible**: New tutor styles, teaching kinds, and iteration outcomes are easy to add

## DCA / Slackwater Integration Points
- **Vibration → DCA Agent Competence Tracking**: Each agent gets a vibration per skill area. Level = mastery, velocity = improvement rate.
- **Resonance → DCA Agent Pairing**: Match agents to tasks (or each other) based on complementary vibrations.
- **Adaptive Style → DCA Strategy Selection**: Switch problem-solving approach based on agent velocity. Fast progress → challenge mode, stuck → guidance mode.
- **Teaching Moments → DCA Feedback System**: Celebrate breakthroughs, suggest redirection, connect to prior knowledge.
- **Learning Groups → DCA Agent Squads**: Group agents for collaborative tasks, track group coherence.
- **Breakthrough Detection → DCA Insight Capture**: Flag sudden capability jumps for replication.

## Patterns to Adopt
1. **Scalar vibration tracking** — one number captures complex state
2. **Velocity as derivative signal** — rate of change tells you when to intervene
3. **Cosine resonance for similarity** — match agents by how they think, not what they know
4. **Adaptive style based on velocity** — fast → challenge, slow → guide, stable → experiment
5. **Breakthrough detection** — result >> old_level with low baseline = celebrate
6. **Patience threshold** — don't intervene immediately on "stuck", give time
7. **Group coherence metric** — pairwise resonance averaged across members
8. **Teaching moment taxonomy** — 8 types covering the full learning cycle
