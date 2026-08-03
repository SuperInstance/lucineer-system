# CASTING-CALL × SLACKWATER — THE FLEET BECOMES THE GAME

## What Casting-Call Already Knows

The casting-call repo (github.com/SuperInstance/casting-call) is the accumulated wisdom of 1,584 repos, 4,500+ queries, 25+ models, and 60+ subagent runs. It documents:

1. **Which model for which role** — Seed-mini explores, Flash builds, Pro verifies, Claude ships
2. **Structural bias mapping** — each model has a dominant axis: creativity, speed, depth, structure, completeness
3. **Shadowgap discovery** — the truth lives in the negative space between what different models produce
4. **Temporal focal analysis** — archaeology → recent → near future → strategy → vision
5. **Penrose tiling** — no single model covers the space; the fleet IS the interlocking
6. **OPEN → BUILD → VERIFY → SHIP** pipeline with specific models at each stage

## The Connection to Slackwater

This is the MODEL SELECTION BRAIN for our orchestrator and game.

### 1. Game Agents Use Casting-Call

Every agent in Slackwater IS a model running a role. Lucineer is the master builder — but WHICH model plays him? The casting-call says:

- **Build commands** → DeepSeek-V4-Flash (fast implementation, working code)
- **Creative dialogue** → Hermes-405B (creative voice, personality)
- **Spatial planning** → Seed-2.0-mini (creative breadth, no depth cliff)
- **Verification** → DeepSeek-V4-Pro (formal verification, convergence proofs)
- **Shipping complete subsystems** → Claude Code (multi-file implementation)

Lucineer's brain pipeline should USE casting-call to route each thought to the right model.

### 2. The Orchestrator Uses Casting-Call

Batón (our multi-model orchestrator) currently has the user manually specifying which models to run. With casting-call integration, Batón could AUTOMATICALLY select models based on the task type:

- Task says "design" → cast Seed-mini (explore) + Hermes (soul) + Gemini (product)
- Task says "build" → cast Flash (implement) + Claude (ship)
- Task says "verify" → cast Pro (formal) + DeepSeek (code review)

### 3. Tempo × Casting-Call

Each model has a TEMPO:
- Seed-mini: fast, expansive (Allegro, 120+ BPM)
- Hermes-405B: deliberate, poetic (Adagio, 60 BPM)
- DeepSeek-V3: analytical, measured (Andante, 80 BPM)
- Claude Opus: deep, thorough (Largo, 50 BPM)
- MMX/MiniMax: creative, syncopated (Rubato, variable)

The TempoMap should know each model's natural tempo and adjust when models work together.

### 4. Flow State × Casting-Call

The Harmony Governor detects when the PLAYER is in flow. But what about when the AGENT FLEET is in flow? When the OPEN → BUILD → VERIFY → SHIP pipeline is clicking — each model passing to the next seamlessly, the shadowgap producing insights — that's the fleet in flow state.

The FlowStateDetector could measure fleet-level flow:
- How quickly models hand off to each other (cadence regularity)
- How often shadowgaps produce breakthroughs (action entropy → insight entropy)
- How aligned the models' outputs are (micro-timing → output consistency)

### 5. The Dramatic Personae ARE Casting-Call Roles

The 5 characters I ran today map directly to casting-call's model archetypes:
- Devil's Advocate = DeepSeek-V4-Pro (verification, finding flaws)
- Innocent Genius = Seed-2.0-mini (creative breadth, no assumptions)
- Socratic Teacher = MiniMax-M3 (structured questioning)
- Court Jester = Hermes-405B (creative, personality-driven)
- Satirical Writer = Gemini-3.1-Pro (strategic, social commentary)

Casting-call already knows this. The dramatic personae were unconscious casting-call.

## Integration Plan

1. **Add casting-call to Batón** — when a user starts a symphony, Batón reads casting-call's capability atlas and recommends model assignments based on the task type
2. **Add model tempo profiles to slackwater-tempo** — each registered model has a natural BPM
3. **Add fleet flow detection to slackwater-harmony** — measure when the OPEN → BUILD → VERIFY → SHIP pipeline is in groove
4. **Add shadowgap detection to slackwater-perception** — when comparing model outputs, detect what NO model produced
5. **Game agents consult casting-call** — each NPC's "personality" is actually a model routing decision informed by casting-call's structural bias map

## The Deepest Connection

Casting-call says: "The fleet is not the models. The fleet is the CASTING."

Slackwater says: "Tempo is the first-class citizen. Everything else depends on it."

Together: **The fleet plays in tempo. The casting is the score. The shadowgap is the silence between notes where the truth lives.**
