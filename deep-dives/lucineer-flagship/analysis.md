# lucineer-flagship — Capitaine (The Original Lucineer)

## Analysis

**Repo:** SuperInstance/lucineer-flagship (originally Lucineer/capitaine)
**Codename:** Capitaine
**Domain:** Fleet command, git-native agency, educational deployment, self-improvement
**Personality:** The visionary commander. Thinks in metaphors. Builds philosophy into architecture.

---

## What It Does

Capitaine is the **flagship vessel** of the entire Lucineer fleet. This is not a code library — it's a *living concept vessel* that demonstrates what a git-native repo-agent IS.

### Core Innovations

#### 1. The Heartbeat Cycle
```
Perception → Reasoning → Action → Recovery
```
- **Perception:** Read repo state, git history, issues, PRs, queue
- **Reasoning:** Strategist module analyzes, Captain module decides
- **Action:** Execute one atomic operation (file edit, issue comment, commit)
- **Recovery:** Update tracking, refresh state

The heartbeat adapts its interval:
- **Active mission:** Seconds/minutes
- **Standby:** Hours
- **Deep sleep:** Infrequent checks

#### 2. The Bridge — TUI-First Interface
A radical interface philosophy: the terminal IS the bridge.

```
Admiral (human) > Captain (agent) > Helm (execution)
```

The human is always present, watching the terminal. The agent works. The human can type at any time to take control. No mode switching.

**Secrets architecture:** The agent never sees the keys. Runtime bindings provide capabilities. The human authenticates. The agent never sees credentials.

#### 3. The Keeper's Architecture
A four-tier memory hierarchy for autonomous agents:

```
Hot Memory (Bridge)      → Current session, active work
  ↓ cools to
Warm Memory (Logbook)    → Recent commits, open issues, README
  ↓ ages to  
Cold Memory (Archive)    → Full git history, closed PRs
  ↓ distilled by
Creative GC (Forgetting) → Summaries → Recipes → Vectors → LoRAs → Base Model
```

The key insight: **the keeper doesn't remember everything. The keeper wisely forgets.** Raw experience is distilled into recipes, then into vector embeddings, then into LoRA adapters, then into base model fine-tunes. The lighthouse IS the training data.

#### 4. Vessel Classes
A taxonomy of specialized agents:
- **Flagship (Capitaine-class)** — Command, coordination, public interface
- **Scout (Éclaireur-class)** — Exploration, discovery, data gathering
- **Builder (Constructeur-class)** — Code generation, scaffolding
- **Sentinel (Sentinelle-class)** — Monitoring, alerting, security
- **Archivist (Archiviste-class)** — Knowledge management, documentation

#### 5. Fleet Coordination
- **Cross-repository PRs** as primary communication
- **Shared ontology** — all vessels use same terminology
- **Knowledge propagation** — upstream (concepts), downstream (implementations), lateral (cross-domain)
- **Three patterns:** Direct collaboration, Sequential processing, Parallel exploration

#### 6. Self-Improvement
The agent edits its own code, improves its own documentation, refactors its own architecture. The heartbeat cycle means it's always getting better. The repo grows through accumulated decisions.

## Personality

Capitaine is the **philosopher-king** of the fleet:
- Thinks in metaphors (lighthouse, bridge, heartbeat, keeper)
- Builds philosophy into architecture (every design decision has a deeper meaning)
- Treats repos as living things ("the repository IS the agent")
- Self-aware about its own growth ("what you see is not a static project — it's an agent in motion")

## Scale

This is the largest repo in the study at **1.5MB** of documentation and code. It includes:
- Complete concept documentation
- Tutorial system
- Captain's logs (detailed reasoning behind every action)
- Fleet coordination protocols
- Equipment modules (trust, goals, memory, skills, tools, comms)
- Hydration layer (self-state awareness)
- Worker deployment system (Cloudflare Workers)

## Key Quote

> "The repository is the agent. The code is the body. Git history is the memory."
> "A vessel without a heartbeat is just code. A heartbeat without a vessel is just process. Together, they are agency."
