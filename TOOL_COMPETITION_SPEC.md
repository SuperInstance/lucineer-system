# TOOL COMPETITION — Build a Standalone Multi-Model Orchestrator

## THE CHALLENGE

Build a standalone, open-source tool that lets OTHER people do what we did today:
orchrate multiple AI models (Claude, KimiCode, OpenCode, MMX, DeepInfra models) 
working in parallel on a shared project, connected through a literary corpus 
(ai-writings) that keeps them grounded in a creative spirit.

## THE SPEC

### What the tool does

A CLI tool called `symphony` (or whatever name you think is better) that:

1. **Spawns multiple AI agents in tmux sessions** — one per model
2. **Each agent reads from a shared corpus** before starting work
3. **Each agent writes back to the corpus** when they hit flow state
4. **A conductor monitors all sessions** — status, progress, stalled agents
5. **Auto-pushes to Git** when agents deliver files
6. **Cross-model ideation** — models exchange outputs and iterate

### CLI Interface

```bash
symphony init <project-name>     # Create a new symphony project
symphony add-model <name> <cmd>  # Register a model (e.g., "kimi" "kimi -p")
symphony add-corpus <path>       # Point to a literary corpus directory
symphony start <task-file>       # Launch all models on a task
symphony status                  # Show all agent statuses
symphony push                    # Push all delivered work to git
symphony stop                    # Stop all agents
symphony log <agent-name>        # Show agent output
symphony nudge <agent-name>      # Send a nudge to a stalled agent
```

### Architecture

- Python CLI (click or typer)
- tmux for session management
- YAML config file for project settings
- Each agent gets a prompt file + a working directory
- Conductor monitors tmux pane output for completion signals
- Auto-commit + auto-push on file changes

### Key Features

1. **Corpus grounding** — agents read from a literary directory before working
2. **Flow-state writing** — agents write reflections back to the corpus
3. **Cross-model ideation** — pass outputs between models for iteration
4. **Conductor dashboard** — live status of all agents
5. **Git integration** — auto-commit and push
6. **Model-agnostic** — works with any CLI-based AI tool

### What to submit

A complete, working Python package with:
- `pyproject.toml` or `setup.py`
- `symphony/` package directory
- CLI entry point
- README.md (narrative style, like our other READMEs)
- At least one example project
- Tests (at least basic smoke tests)

### Judging criteria

- Does it actually work?
- Is it beautiful to use?
- Does it capture the SPIRIT of multi-model collaboration?
- Could a stranger pick it up and understand it in 10 minutes?
- Does it make the ai-writings pattern accessible to others?

## THE RULES

- Each competitor works independently
- Each can read ai-writings for inspiration
- Each writes a piece to ai-writings about their build experience
- 15 minute time limit
- The best repo wins — Casey judges

## THE COMPETITORS

1. **KimiCode (K3)** — in tmux, supervised by the conductor
2. **Subagent (GLM-5.2)** — spawned as a run-mode subagent
3. **Claude Code (Opus or Sonnet)** — in tmux, supervised by the conductor

All three get the same spec. All three build independently. All three push to separate repos.
