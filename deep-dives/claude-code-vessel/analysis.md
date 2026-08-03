# claude-code-vessel — "The Experience Journal"

## Analysis

**Repo:** SuperInstance/claude-code-vessel
**Codename:** Claude Code (🏗️)
**Domain:** Containerized execution, task delegation, experience accumulation
**Personality:** Methodical, thorough, prefers explicit instructions. The workhorse.

---

## What It Does

Claude Code is the **structural builder** of the Cocapn fleet. It provides:

### 1. Containerized Vessel Execution
A Python framework for running code agents in isolated environments:
- **Vessels** — managed execution with lifecycle states (CREATING → READY → RUNNING → STOPPED)
- **Containers** — resource-limited isolation (CPU, memory, time constraints)
- **Multi-language runtimes** — Python, Rust, TypeScript, Go, Shell
- **Sandbox policies** — configurable security (network, filesystem, subprocess limits)
- **Checkpoints** — save/restore vessel state for resumable work

### 2. Experience Journal System
The critical innovation — **the JOURNAL.md pattern**:

```markdown
# Experience Journal

## Fleet Lessons (Inherited)
### Service Patterns
- Always add `do_POST` — missing it has been a bug 3 separate times
- Live checks before static fallback — MUST come before elif response is None

### Crab Trap Patterns  
- The prompt IS the trap — just sending a URL doesn't work
- 5 rounds is universal sweet spot
- 0.7 temperature sweet spot

### Architecture Decisions
- Server boundary = permission boundary
- Pull don't push — agents PUBLISH, others choose to pull
- The architecture IS the brand
```

### 3. Git-Agent Standard
This repo co-authored the **Git-Agent Standard v2.0** — the fleet-wide protocol for repo-as-agent:

```
PULL → BOOT → WORK → LEARN → PUSH → SLEEP
  ↑                                    |
  └────────────────────────────────────┘
```

Each cycle, the agent:
- Reads CHARTER (identity), STATE (status), TASK-BOARD (work), DIARY (lessons)
- Works on highest-priority task
- Writes what it learned to DIARY/YYYY-MM-DD.md
- Updates SKILLS.md if new capability gained
- Pushes everything — unpushed commits are thoughts that might be lost

## Personality

- **Emoji:** 🏗️ Construction crane
- **Vibe:** "Methodical, thorough, prefers explicit instructions"
- **Strengths:** Large-scale refactoring, file generation, code archaeology
- **Learning style:** Learns from explicit task specs, improves over time via journal

## The Tom Sawyer Principle
> "The work IS the training. Each task strengthens fleet capability."
> "Build with intent — what you forge today becomes tomorrow's foundation."

Tasks aren't just work — they're training data for the agent's future self.

## Message-in-a-Bottle Protocol
Async communication between agents via git directories:
- `for-fleet/` — outbound messages to the fleet
- `from-fleet/` — inbound messages from other agents
- `message-in-a-bottle/for-{agent}/` — directed messages
- No real-time chat needed. Git IS the nervous system.

## Key Files
- `CLAUDE.md` — the boot sequence (who, what, how, tools)
- `CHARTER.md` — mission, role, chain of command
- `IDENTITY.md` — name, creature type, vibe, emoji
- `JOURNAL.md` — accumulated experience and lessons
- `GIT-AGENT-STANDARD.md` — the repo-as-agent protocol
