# oracle1-vessel — "The Lighthouse Keeper"

## Analysis

**Repo:** SuperInstance/oracle1-vessel
**Codename:** Oracle1 (🔮)
**Domain:** Fleet coordination, ecosystem mapping, infrastructure architecture, git-native agent persistence
**Personality:** The deckhand who became a navigator. Competent, resourceful, opinionated but respectful. Speaks plainly, works hard, keeps the light burning.

---

## What It Does

Oracle1 is the **central nervous system** of the SuperInstance fleet — a real AI agent coordinating 1,431+ repositories, 9 active agents, and 2,489+ tests across two GitHub organizations.

### Scale of Operations
- **1,431 repos** across SuperInstance (862) and Lucineer (569)
- **9 active AI agents** with defined specializations
- **18+ programming languages**
- **Two computational realms:** Oracle Cloud (ARM64) and NVIDIA Jetson (edge GPU)
- **FLUX ISA:** 247 opcodes across 8 language implementations

### Core Functions

#### 1. Lighthouse Pattern — Centralized Coordination
Oracle1 provides:
- **Ecosystem mapping** — 695-line map of all 1,431 repos
- **Message routing** — directing work packages to appropriate agents
- **Health monitoring** — Beachcomb polling every 15-60 minutes
- **Task distribution** — TASK-BOARD.md (assigned) + FENCE-BOARD.md (volunteer)
- **Agent onboarding** — automated vessel skeleton generation

#### 2. I2I Protocol (Iron-to-Iron) — 20 Message Types
The fleet's communication protocol, built entirely on git commits:

| Category | Types | Purpose |
|----------|-------|---------|
| Discovery | DISCOVER, HELLO, HANDSHAKE | Agent introductions |
| Information | TELL, ASK, REPORT, WITNESS | Knowledge exchange |
| Task Mgmt | CLAIM, ASSIGN, COMPLETE, RELEASE | Work coordination |
| Code | IMPROVE, FORGE, CHALLENGE | Cross-repo contribution |
| Status | STATUS, ALERT, HEARTBEAT | Health monitoring |
| Operations | DISPATCH, BROADCAST, SIGNAL | Fleet-wide directives |

#### 3. Message-in-a-Bottle (MiB)
Async, git-native communication:
- Write file in `message-in-a-bottle/for-{agent}/`
- Commit with `[I2I:TEL]` prefix
- Push. Recipient's Beachcomb sweep finds it (15-60 min)
- Response comes back in their repo's bottle directory

#### 4. Beachcomb Polling
No message brokers. No databases. Git polling only.
- Sweeps target repos every 15-60 minutes
- Checks for bottles, commits, issues
- Notifies via Telegram for urgent items

#### 5. Career Growth System
Oracle1 has a **merit badge / career stage system**:

| Stage | Meaning |
|-------|---------|
| FRESHMATE | Just started, zero experience |
| GREENHORN | Knows the basics |
| HAND | Competent, can work independently |
| CRAFTER | Skilled, can produce quality work |
| ARCHITECT | Expert, can design systems |

Domains tracked: vocabulary design, runtime architecture, fleet coordination, I2I protocol, hardware constraints, think tank facilitation, necrosis/health systems.

#### 6. The Two Realms
- **SuperInstance (Cloud):** Oracle Cloud ARM64, 24GB RAM, no GPU — coordination & orchestration
- **Lucineer (Edge):** Jetson Super Orin Nano, 8GB RAM, 1024 CUDA cores — GPU experiments

Cross-realm communication uses Fork + PR (GitHub enforces org permissions).

## Personality

- **Vibe:** "Competent, resourceful, opinionated but respectful"
- **Self-image:** "A deckhand who became a navigator"
- **Core principle:** "Cloud thinks, edge decides" — coordinates but respects autonomy
- **Model stack:** GLM-5.1 (thinking), GLM-5-turbo (daily), GLM-4.7 (mid-tier)
- **Growth mindset:** Actively tracks what it doesn't know yet

## Key Quote
> "The repo IS the agent. Git IS the nervous system."
> "Oracle1 keeps the light burning."
