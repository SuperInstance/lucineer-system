# lucineer-system

**Design repository for the Slackwater/Lucineer ecosystem — architecture documents, multi-model roundtable analyses, cross-model synthesis, and the honest record of what is and isn't built.**

What this is: **Lucineer is an AI-powered Roblox game-builder and NPC system; Slackwater Yard is the game world it powers** (7 tech eras, simple machines → autonomous agents). This repo is the map room for that project — every other repo is a building site. 400,000+ words of design produced by AI agents who were told to think differently from each other and then argue about it.

Design has outpaced delivery. Per `ROADMAP_whats_next.md` (the ground-truth doc, renamed from `ROADMAP.md` on 2026-08-03, refs fixed): the system has processed four real jobs in its lifetime, and zero have reached a player. **Read `ROADMAP_whats_next.md` before you read anything else.**

<p align="center">
  <img src="assets/images/hero-map-room.jpg" alt="The map room: one chart glowing warmer than the rest — the plan that outpaced the ship" width="700">
</p>

---

## State — 2026-08-14

- **Test suite:** 161 tests pass (`pytest tests/`). CI runs them on Python 3.10/3.11/3.12 via `.github/workflows/ci.yml`.
- **Security scrub (2026-08-14):** all DeepInfra key loading now goes through `loadkey.get_key()` — `.env` first, `DEEPINFRA_API_KEY` env var fallback, no crash when the file is missing. This pass finished the job the earlier scrub started: `molt_ideation.py`, `roundtable.py`, and `unification_roundtable.py` still carried duplicated loaders (one crash-prone `.split()` pattern, one dead env fallback, one no-fallback module-level `open()`). All three now import `loadkey`. **No API keys in tracked files.**
- **Repo hygiene:** `.coverage` was accidentally committed; untracked again, `.gitignore` covers it.
- **Link audit:** every `.md` reference in the README resolves; the ROADMAP rename left no stale `ROADMAP.md` links anywhere.
- **Known footgun:** the pipeline scripts (`roundtable.py`, `molt_ideation.py`, `unification_roundtable.py`, ...) run their whole job at module level — no `if __name__ == "__main__"` guard — so *importing* them executes the pipeline. Don't import them. Fix pending.
- **Naming:** the worker repo on GitHub is now `lucineer-relay` (was `lucineer-worker`); `process_v2.py` lives there. The on-disk `.env` directory is `mcp-deeinfra` — a long-standing typo other tooling depends on, so it stays.

---

## Architecture

### The Multi-Model Roundtable

`roundtable.py` dispatches strategic prompts to 5 heavy models in parallel via DeepInfra, each with a different angle — Nemotron-Ultra-550B (systems architecture), Gemini-Pro (player experience), Qwen3.7-Max (technical implementation), Hermes-405B (brand & lore), Seed-2.0-Pro (master synthesis). Outputs are saved as `ROUNDTABLE_*.md` and cross-reviewed. Companion scripts: `v2_roundtable.py`, `unification_roundtable.py`, `cross_model_synthesis.py`.

### The Brain Pipeline

The canonical 5-stage brain pipeline (implemented in `lucineer-system/brain.py`):

```
Stage 1: Intent Parse        Seed-2.0-mini      (Allegro, 120+ BPM)
Stage 2: Spatial Planning    Qwen3.6-35B /      (Moderato, 90-110 BPM)
         OR Seed-2.0-pro     (deep mode for complex builds)
Stage 3: Code Generation     Qwen3-Coder-480B   (Andante, 80-100 BPM)
Stage 4: Personality Wrap    Hermes-405B        (Adagio, 50-70 BPM)
         (creative mode)
Stage 5: Safety Check        Nemotron-Ultra     (Largo, 40-55 BPM)
         (in processor)
```

### The Processor Daemon

The processor (`process_v2.py`, in the `lucineer-relay` repo) is the orchestration layer:

```
┌─────────────────────────────────────────────────────────┐
│                   process_v2.py Daemon                    │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Poll     │→ │ Claim    │→ │ Recall   │→ │ Search   │ │
│  │ Pending  │  │ Job      │  │ Memory   │  │ Skills   │ │
│  │ Jobs     │  │ (atomic) │  │ (D1)     │  │(Vectorize│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                   │       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │       │
│  │ Persist  │← │ Safety   │← │ Template │←───────┘       │
│  │ Memory   │  │ Check    │  │ or Brain │                 │
│  │ (D1)     │  │(Nemotron)│  │ Pipeline │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
│                                                           │
│  Resilience: Circuit breaker (5 failures), RSS guard     │
│  (200MB), heartbeat (60s), SIGTERM/SIGINT handlers       │
└─────────────────────────────────────────────────────────┘
```

### Key Loading (the security scrub)

`loadkey.py` is the single key loader for every script in this repo. Resolution order:

1. `DEEPINFRA_API_KEY=...` in `/home/eileen/mcp-deeinfra/.env` (handles `export ` prefix and quotes).
2. The `DEEPINFRA_API_KEY` environment variable — reachable when the `.env` file is missing or lacks the key.

If both are absent, `get_key()` returns `""` and API calls fail with 401 — loud enough. Notes for other machines: the `.env` path is local-only; CI and teammates should export `DEEPINFRA_API_KEY` instead. No script reads the `.env` file itself anymore; if you add a script that hits DeepInfra, use `loadkey.get_key()`.

---

## Document Index

**Start here:** `ROADMAP_whats_next.md` → `GAP_ANALYSIS.md` → `SHIP_READINESS.md`. The rest is context. (100+ docs live here; the tables below are the map.)

### Ground Truth & Roadmap

| Document | Content |
|----------|---------|
| `ROADMAP_whats_next.md` | **Read this first.** Brutal state assessment: what works, what doesn't, the 21-hour critical path |
| `GAP_ANALYSIS.md` | Conflicts and gaps across roundtable documents |
| `SHIP_READINESS.md` | What must be true before this ships |
| `PRODUCTION_READINESS_CHECKLIST.md` | Production checklist |
| `PRODUCTION_VERIFICATION.md` | Verification of production claims |
| `SMOKE_TEST_RESULTS.md` / `LIVE_SMOKE_TEST.md` | Smoke and live test records |
| `LIVE_PLAYTEST_RESULTS.md` | Live playtest findings |

### Core Architecture

| Document | Content |
|----------|---------|
| `MASTER_ARCHITECTURE_v2.md` | System-wide architecture: 10 layers from Roblox client to R2 trajectories |
| `SPATIAL_GRAMMAR_v2.md` | Spatial reasoning language for build decomposition |
| `TEMPO_FIRST_ARCHITECTURE.md` | TempoMap design — musical timing as first-class pipeline citizen |
| `TEMPO_IS_FIRST_CLASS.md` | Justification for tempo-driven pipeline transitions |
| `UNIFIED_INTEGRATION_PLAN.md` | 30-day roadmap synthesizing all roundtable outputs |
| `UNIFICATION_VISION.md` | High-level unification of the multi-model approach |
| `INTEGRATED_ARCHITECTURE.md` | How the pieces actually fit together |

### Character and World

| Document | Content |
|----------|---------|
| `CHARACTER_BIBLE.md` | Lucineer's full character: voice, vocabulary, refusal protocol, unfinished rule |
| `FABLE_CHARACTER_BIBLE.md` | Fable 5's definitive character writeup |
| `FABLE_WORLD_BIBLE.md` | Slackwater Yard world description |
| `ERA_TRANSITIONS.md` | 7-era progression system (levers → autonomous robots) |
| `FLOW_STATE_DEEP_DIVE.md` | Player flow-state design for build engagement |
| `TUTORIAL_DESIGN.md` | Onboarding sequence design |

### Roundtable Analyses

| Document | Model | Focus |
|----------|-------|-------|
| `ROUNDTABLE_NEMOTRON.md` | Nemotron-3-Ultra-550B | Systems architecture, scaling, reliability |
| `ROUNDTABLE_GEMINI.md` | Gemini-3.1-Pro | Player experience, viral loops, onboarding |
| `ROUNDTABLE_QWEN.md` | Qwen3.7-Max | Technical implementation, Lua code, performance |
| `ROUNDTABLE_HERMES.md` | Hermes-3-Llama-405B | Brand identity, lore, NPC ecosystem |
| `ROUNDTABLE_SEED.md` | Seed-2.0-Pro | Master synthesis, 30-day roadmap, risk matrix |

### Cross-Model Synthesis

| Document | Content |
|----------|---------|
| `SEED_VISION_AUDIT.md` | Seed-2.0-Pro's audit of the vision |
| `NVIDIA_SYNERGY_*.md` | Nemotron's analysis of synergy with NVIDIA stack |
| `FLUX_FLOW_CONNECTION.md` | FLUX model integration with the creative pipeline |
| `FLUX_SYNERGY_STUDY.md` | Deeper FLUX integration analysis |
| `PLATO_SYNERGY_STUDY.md` | Philosophical alignment study |
| `WRITINGS_DEEP_STUDY.md` | Analysis of writing voice across models |

### Pipeline Components

| Document | Content |
|----------|---------|
| `CASTING_CALL_CONNECTION.md` | How casting-call routes models to pipeline roles |
| `MIDI_PERCEPTION_VISION.md` | SWMIDI channel map and perception system design |
| `SOUND_DESIGN_10_MOMENTS.md` | Ten key audio moments in the player experience |
| `MOLT_REWARD_FUNCTION.py` | Reward function for MOLT trajectory optimization |
| `SAVE_SYSTEM.md` | Game state persistence design |
| `VISUAL_POLISH.md` | Visual quality targets and techniques |

### Fable 5 Productions

| Document | Content |
|----------|---------|
| `FABLE_5_MASTER_PROMPT.md` | Master prompt for Fable 5 character generation |
| `FABLE_5_PRODUCTION_DESIGN.md` | Production design document |
| `FABLE_GRAND_PLAN.md` | Grand plan from Fable 5's perspective |
| `FABLE_BRIEF.md` | Project brief for Fable 5 |
| `FABLE_AGENT_COLLECTION.md` | Collection of agent designs |
| `FABLE_AGENT_UX.md` / `FABLE_AGENT_UX_BRIEF.md` | Agent UX design |

### Deep-Dives

| Document | Content |
|----------|---------|
| `deep-dives/*/analysis.md` | Per-component analysis (fleet vessels, agents, infra) |
| `deep-dives/*/integration-plan.md` | Per-component integration plans |
| `deep-dives/*/LEARN.md` | Lessons learned per experiment |

---

## Python Modules

| Module | Purpose |
|--------|---------|
| `roundtable.py` | Dispatches strategic prompts to 5 models via DeepInfra |
| `v2_roundtable.py` | V2 roundtable with improved prompt engineering |
| `unification_roundtable.py` | Cross-model unification roundtable |
| `cross_model_synthesis.py` | Synthesizes outputs across models |
| `governor.py` | Pipeline governor — controls flow, rate limits, retries |
| `ideation_loop.py` | Creative ideation loop with Seed-2.0-mini |
| `molt_ideation.py` | MOLT trajectory-guided ideation |
| `round2_ideation.py` | Second-round ideation with deeper models |
| `energy_adapter.py` | Energy/budget adapter for pipeline stages |
| `asset_pipeline.py` | Asset generation pipeline coordination |
| `generate_hub.py` | Hub generation from build specs |
| `dramatic_personae.py` | NPC character definitions and relationships |
| `loadkey.py` | **The one key loader.** Every DeepInfra script uses `get_key()` |

---

## File Layout

```
lucineer-system/
├── README.md                      # This file
├── ROADMAP_whats_next.md          # Ground truth — read this first
├── roundtable.py                  # 5-model roundtable dispatcher
├── v2_roundtable.py               # Improved roundtable
├── unification_roundtable.py      # Cross-model unification
├── cross_model_synthesis.py       # Synthesis engine
├── governor.py                    # Pipeline governor
├── ideation_loop.py               # Ideation loop
├── molt_ideation.py               # MOLT ideation
├── MOLT_REWARD_FUNCTION.py        # Trajectory reward function
├── energy_adapter.py              # Budget adapter
├── asset_pipeline.py              # Asset pipeline
├── generate_hub.py                # Hub generator
├── dramatic_personae.py           # NPC definitions
├── loadkey.py                     # Single API key loader
├── *.md                           # 100+ design documents
├── creative/                      # Creative pieces inspired by the work
├── dramatic_personae/             # NPC data files
├── ideation/                      # Ideation outputs
├── nvidia_ideation/               # NVIDIA-specific ideation
├── round2_ideation/               # Second-round outputs
├── synthesis/                     # Cross-model synthesis outputs
├── unification_roundtable/        # Unification roundtable data
├── v2_roundtable/                 # V2 roundtable data
├── deep-dives/                    # Per-component deep dive analyses
├── assets/                        # Generated assets
└── tests/                         # Test suite (161 passing)
```

---

## Related Repositories

This repo is the map, not the machine. To run anything end-to-end, clone the siblings:

| Repository | Role |
|-----------|------|
| [lucineer-relay](../lucineer-relay) | Cloudflare Worker relay + processor daemon (`process_v2.py`) |
| [lucineer-system](../lucineer-system) | 4-stage AI pipeline implementation |
| [lucineer-creative](../lucineer-creative) | MMX-powered creative asset generation |
| [lucineer-memory](../lucineer-memory) | D1 persistent memory store |
| [lucineer-vector](../lucineer-vector) | Vectorize semantic skill library |
| [lucineer-roblox](../lucineer-roblox) | Roblox client (16 Lua modules) |
| [casting-call](../casting-call) | Model routing atlas (Layer 8) |

---

## Contributing

See `CONTRIBUTING.md`.

## License

MIT
