# lucineer-system

**Design repository for the Slackwater ecosystem — architecture documents, multi-model roundtable analyses, and cross-model synthesis produced by 10 AI models thinking simultaneously.**

This is the map room. Every other repo is a building site — Lua modules, Python processors, Cloudflare Workers. This repo is where the architects met before the first stone was cut: 400,000+ words of design produced by AI agents who were told to think differently from each other and then argue about it.

---

## Architecture

### The Multi-Model Roundtable

The `roundtable.py` script dispatches strategic prompts to 5 heavy models in parallel via DeepInfra:

```
                  ┌─────────────────────────┐
                  │   roundtable.py          │
                  │   (dispatches briefs)    │
                  └───────────┬─────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
  ┌─────────────────┐ ┌──────────────┐ ┌────────────────┐
  │ Nemotron-Ultra  │ │ Gemini-Pro   │ │ Qwen3.7-Max    │
  │ 550B            │ │              │ │                │
  │                 │ │              │ │                │
  │ Systems         │ │ Player       │ │ Technical      │
  │ Architecture    │ │ Experience   │ │ Implementation │
  └─────────────────┘ └──────────────┘ └────────────────┘
            │                 │                 │
            ▼                 ▼                 ▼
  ┌─────────────────┐ ┌──────────────┐
  │ Hermes-405B     │ │ Seed-2.0-Pro │
  │                 │ │              │
  │ Brand & Lore    │ │ Master       │
  │ Identity        │ │ Synthesis    │
  └─────────────────┘ └──────────────┘
```

Each model receives a different strategic angle (systems architecture, player experience, technical implementation, brand identity, master synthesis). Outputs are saved as `ROUNDTABLE_*.md` files and then cross-reviewed.

### The Brain Pipeline

The canonical 5-stage brain pipeline (implemented in `lucineer-brain/brain.py`):

```
Stage 1: Intent Parse        Seed-2.0-mini      (Allegro, 120+ BPM)
    ▼
Stage 2: Spatial Planning    Qwen3.6-35B /      (Moderato, 90-110 BPM)
         OR Seed-2.0-pro     (deep mode for
                             complex builds)
    ▼
Stage 3: Code Generation     Qwen3-Coder-480B   (Andante, 80-100 BPM)
    ▼
Stage 4: Personality Wrap    Hermes-405B        (Adagio, 50-70 BPM)
         (creative mode)
    ▼
Stage 5: Safety Check        Nemotron-Ultra     (Largo, 40-55 BPM)
         (in processor)
```

### The Processor Daemon

The processor (`process_v2.py` in `lucineer-worker/`) is the orchestration layer:

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

### systemd Service Configuration

For production deployment, the processor runs as a systemd service:

```ini
# /etc/systemd/system/lucineer-processor.service
[Unit]
Description=Lucineer Job Processor v2
After=network.target

[Service]
Type=simple
User=lucineer
WorkingDirectory=/home/eileen/projects/lucineer-worker
ExecStart=/usr/bin/python3 process_v2.py --loop --interval 2
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Environment
EnvironmentFile=/home/eileen/projects/lucineer-worker/.env

# Hardening
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/home/eileen/projects/lucineer-worker

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable lucineer-processor
sudo systemctl start lucineer-processor
journalctl -u lucineer-processor -f   # tail logs
```

---

## Document Index

### Core Architecture

| Document | Content |
|----------|---------|
| `MASTER_ARCHITECTURE_v2.md` | System-wide architecture: 10 layers from Roblox client to R2 trajectories |
| `SPATIAL_GRAMMAR_v2.md` | Spatial reasoning language for build decomposition |
| `TEMPO_FIRST_ARCHITECTURE.md` | TempoMap design — musical timing as first-class pipeline citizen |
| `TEMPO_IS_FIRST_CLASS.md` | Justification for tempo-driven pipeline transitions |
| `UNIFIED_INTEGRATION_PLAN.md` | 30-day roadmap synthesizing all roundtable outputs |
| `UNIFICATION_VISION.md` | High-level unification of the multi-model approach |

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
| `GAP_ANALYSIS.md` | Conflicts and gaps found across roundtable documents |
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
| `loadkey.py` | DeepInfra API key loader utility |

---

## File Layout

```
lucineer-system/
├── README.md                      # This file
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
├── loadkey.py                     # API key loader
├── *.md                           # 60+ design documents
├── dramatic_personae/             # NPC data files
├── ideation/                      # Ideation outputs
├── nvidia_ideation/               # NVIDIA-specific ideation
├── round2_ideation/               # Second-round outputs
├── synthesis/                     # Cross-model synthesis outputs
├── unification_roundtable/        # Unification roundtable data
├── v2_roundtable/                 # V2 roundtable data
├── assets/                        # Generated assets
└── tests/                         # Test suite
```

---

## Related Repositories

| Repository | Role |
|-----------|------|
| [lucineer-worker](../lucineer-worker) | Cloudflare Worker relay + processor daemon |
| [lucineer-brain](../lucineer-brain) | 4-stage AI pipeline implementation |
| [lucineer-creative](../lucineer-creative) | MMX-powered creative asset generation |
| [lucineer-memory](../lucineer-memory) | D1 persistent memory store |
| [lucineer-vector](../lucineer-vector) | Vectorize semantic skill library |
| [lucineer-roblox](../lucineer-roblox) | Roblox client (16 Lua modules) |
| [casting-call](../casting-call) | Model routing atlas (Layer 8) |

---

## License

MIT
