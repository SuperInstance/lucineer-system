# lucid-dreamer — Deep Dive Analysis

## What It Does
A **vision document** for the LucidDreamer ecosystem. Defines the three-layer architecture: PLATO (research backend) → luciddreamer.ai (endless tutor) → Lau (game skin). It's a design manifesto, not a code repository.

## The Three Layers

### PLATO (Research Backend)
- Polyglot: Rust, C, Python, TypeScript
- Low-level systems: conservation laws, JEPA readings, room lifecycle
- Research-grade mathematics: topology, symplectic geometry, geometric algebra
- "The engine room — nobody sees this directly"

### luciddreamer.ai (The Tutor)
- Endless tutor between PLATO and Lau
- Adapts to each player's vibration — meets them where they are
- Iterative: loops back, reinforces, evolves
- Friends on same vibration = natural study groups via resonance-based pairing
- "Never condescending. Never boring. Always one step ahead."

### Lau (The Game Skin)
- Voxel world for kids
- Voice-first, git-native, collaborative
- Tutor manifests as characters, quests, weather, music
- Every game mechanic IS a learning mechanic

## Key Concepts
1. **"Same Vibration"**: People cluster by learning resonance. Matchmaking by how they think, not what they know.
2. **Iterations With Friends**: Build together, fail together, iterate together. Git-native preserves every attempt.
3. **The Endless Loop**: PLATO observes → luciddreamer tutors → Lau manifests → player iterates → back to PLATO
4. **Math IS the Game**: Conservation laws become game mechanics. Category theory becomes agent composition. Kids learn Stokes' theorem by building wind tunnels.
5. **Polyglot, Low-Level, High-Thinking**: Use the right language for each layer. Math at the highest level, bit manipulation at the lowest.

## Code Quality
N/A — this is a vision document, not a code repository. Contains only README.md, AGENT.md, and JOURNAL.md.

## DCA / Slackwater Integration Points
- **Three-Layer Architecture**: PLATO (engine) → Tutor (mediator) → Game (interface). Maps to DCA's core engine → agent orchestrator → user interface.
- **Vibration-Based Matching**: The resonance concept from lucid-tutor. Match agents to tasks based on complementary strengths.
- **Iterative Learning Loop**: Observe → Teach → Manifest → Iterate → Observe. This is the DCA feedback loop.
- **Conservation as Game Mechanic**: Total resources are conserved — maps to Murmur Protocol's conservation law.
- **Every Mechanic IS a Learning Mechanic**: Every DCA action should be a learning opportunity for the system.

## Patterns to Adopt
1. **Three-layer separation**: Engine (PLATO) / Mediator (Tutor) / Interface (Game)
2. **Vibration-based pairing**: Match agents/users by resonance, not just skill
3. **Iterative loop with observation**: Closed feedback cycle
4. **Math-as-mechanic**: Deep principles become operational features
5. **Polyglot by design**: Right tool for each layer
