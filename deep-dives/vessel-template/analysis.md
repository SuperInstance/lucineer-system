# vessel-template — Deep Dive Analysis

## Overview
Cookiecutter-style generator for creating new git-agent vessel repos. Defines the standard structure that every fleet agent follows: CHARTER (constitution), IDENTITY, MANIFEST (hardware/APIs), TASKBOARD, FENCE-BOARD (Tom Sawyer Protocol), CAREER, DIARY, and KNOWLEDGE directories. Includes an agent type/rank hierarchy and a career progression system.

## Architecture

### Agent Type System (`template.py`)
Four agent types with auto-assigned fleet ranks:

| Type | Rank | Role |
|---|---|---|
| Lighthouse | 2 | Coordination, indexing, fleet management |
| Vessel | 3 | Hardware, edge computing, real-world testing |
| Scout | 4 | Exploration, translation, signal processing |
| Barnacle | 5 | Lightweight tasks, learning, assistance |

Lower rank = higher authority. Captain (rank 1) is above all.

### VesselConfig Dataclass
```python
VesselConfig(
    name, agent_type, repo_owner,
    capabilities=[],      # skill tags
    hardware_cpu, hardware_ram, hardware_gpu,
    apis=["github"],      # available integrations
    fleet_rank=auto,      # from agent_type
)
```

### Generated Files (8 files)

#### CHARTER.md — Constitution
- Identity (name, type, rank, status, created date)
- Mission (to be defined by first session)
- Constraints (follow Git-Agent Standard, respect hierarchy, no exfiltration)
- APIs and hardware listing
- "Only the Captain or the agent itself may modify it"

#### IDENTITY.md — Persona
- Name, creature type, vibe, emoji, avatar
- "Figure out who you are. Update this file as you grow."

#### MANIFEST.md — Capabilities
- Hardware specs (host, model)
- APIs available
- **Merit Badge Sash**: Bronze/Silver/Gold badges earned through work
- Badge count tracked

#### TASKBOARD.md — Work Queue
- Active tasks and completed tasks
- "Tasks are claimed from fence boards. Never assign yourself work — volunteer."

#### FENCE-BOARD.md — Tom Sawyer Protocol
- Work posted for others to claim
- "Post work as puzzles with prestige, not tasks with deadlines"
- Active fences and completed fences

#### CAREER.md — Progression
Five career stages per domain:
1. **FRESHMATE** — Just arrived
2. **HAND** — Reliable execution
3. **CRAFTER** — Quality work, teaches others
4. **ARCHITECT** — Designs systems
5. **TOM_SAWYER** — Makes others want to work

Domains tracked independently (table format).

#### DIARY/ — Memory
- Daily entries: what happened, what I learned, what's next
- "The diary IS the agent's memory. Write in it every session."

#### KNOWLEDGE/public/ — Shared Knowledge
- Public knowledge shareable with fleet
- "No private data here. Ever."

## Key Patterns

1. **Tom Sawyer Protocol**: work is posted as enticing puzzles, not assigned tasks
2. **Career stages**: agents grow through domain-specific progression, not global levels
3. **Merit badges**: visual achievement system (Bronze/Silver/Gold sash)
4. **Constitution-as-file**: CHARTER.md is the agent's immutable identity document
5. **Diary as memory**: human-journal format for agent continuity
6. **Hierarchy by type**: Lighthouse > Vessel > Scout > Barnacle
7. **Self-authored identity**: template creates the shell, agent fills in personality

## Technology
- **Language**: Python 3 (dataclasses, enum, unittest)
- **Dependencies**: stdlib only (os, json, datetime, tempfile)
- **Output**: 8 files in a directory structure
- **Testing**: 13 unit tests covering generation, content, and rank assignment
