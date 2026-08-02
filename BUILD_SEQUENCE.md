# LUCINEER BUILD SEQUENCE — ARCHITECTURE-FIRST
# =============================================
# Layer 0 → Layer 3. Each layer is the foundation for the next.
# Every team member has a role that matches their strengths.
# =============================================

## DEPENDENCY GRAPH (why this order matters)

```
Layer 0: INFRASTRUCTURE (must be solid before anything builds on it)
  ├── Job Queue Hardening (#6) ─────┐
  ├── API Key Security (#3) ────────┤
  ├── Processor Daemon ─────────────┼──► safe to serve real players
  └── Text Filtering (#5) ──────────┘
                                    │
Layer 1: CORE EXPERIENCE ───────────┤
  ├── Unified Personality (#7) ─────┤
  ├── BuildAnimator.lua ────────────┼──► the magic moment works
  ├── Regenerated rbxlx ────────────┤
  └── Studio Playtest ──────────────┘
                                    │
Layer 2: DEPTH & POLISH ────────────┤
  ├── Upgraded Templates ───────────┤
  ├── Sound Design ─────────────────┤
  ├── Skill Library Expansion ──────┼──► head-turning quality
  └── Voice Line Integration ───────┘
                                    │
Layer 3: WORLD & STORY ─────────────┤
  ├── NPC Ecosystem ────────────────┤
  ├── Progression System ───────────┤
  ├── Social/Viral Mechanics ───────┤
  └── Slackwater Hub Build ─────────┘
```

## TEAM ASSIGNMENTS

### KimiCode (K3) — Roblox Lua Master
Best at: Luau code, spatial reasoning, client-side architecture
Layer 0: Fix job claiming in Worker TypeScript (#6)
Layer 1: Write BuildAnimator.lua (the wow-factor animation system)
Layer 2: Upgrade CommandExecutor with material/color systems
Layer 3: NPC behavior trees in Luau

### Claude Code (Opus) — Systems Architect  
Best at: Deep reasoning, security, TypeScript, architecture
Layer 0: API key security (#3), Text filtering (#5), Worker queue hardening (#6)
Layer 1: Unified personality system (#7) — merge the two contradictory personas
Layer 2: Sound design architecture
Layer 3: Progression system implementation

### OpenCode (GLM-4.6) — Memory & Systems Designer
Best at: Structured design, database schemas, system documentation
Layer 0: Memory worker endpoint audit and fix
Layer 1: Wire bond_level progression into memory
Layer 2: Achievement system D1 schema
Layer 3: NPC state persistence design

### MMX + DeepInfra (Seed-mini / DeepSeek / Hermes) — Creative Pipeline
Best at: Content generation, voice lines, skills, ideation loops
Layer 0: Generate text filter rules
Layer 1: 50 better voice lines (Fable-quality, not generic)
Layer 2: 20 more skills (batch 4), sound asset generation
Layer 3: NPC dialogue trees, quest text, lore content

### DeepInfra Heavy Models (Nemotron-Ultra / Qwen3-Coder / Gemini) — Consultants
Best at: Code review, architecture validation, implementation plans
Layer 0: Security audit of the full stack
Layer 1: BuildAnimator review and optimization
Layer 2: Visual polish code generation
Layer 3: Viral mechanic implementation code
