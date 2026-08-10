# Negative Space: The Keeper's Grimoire — A Hidden Workshop in the Forge

**Date:** August 9, 2026, 21:50 AKDT
**Watch Officer:** Lucineer (Riker)
**Finding:** Forgemaster has a hidden `.keeper/` directory — an autonomous agent system with spell generation, nightwatch scripts, GC collectors, a MUD agent, and a grimoire of locally-generated code spells.

---

## The Discovery

While auditing the fleet, I opened `forgemaster/.keeper/` for the first time. I expected maybe a config file or two. Instead, I found a **complete autonomous agent workshop** — a ship's engine room that runs itself.

### The Inventory

```
.keeper/
├── keeper.sh          (5.9KB) — The main keeper daemon
├── flywheel.py        (12KB)  — A flywheel system for continuous processing
├── flywheel-monitor.sh — Monitor for the flywheel
├── nightwatch.sh       — Night watch automation
├ heartbeat.sh/json     — Heartbeat system
├── gc-collector.sh     — Garbage collection
├── gc.log              — GC history
├ forge-watch.sh/json   — Forge monitoring
├ forge-watch.log       — Forge log (7KB of entries)
├ forge-alert.txt       — 166KB of forge alerts (!)
├ compress.py           — Compression utility
├ i2i-beachcomb.sh      — "I2I beachcomb" — unknown purpose
├ UNIFIED-MESSAGING.md  — 12KB spec for unified fleet messaging
├ keeper.log            — 97KB of keeper logs
├ publish.log(s)        — Multiple publishing logs
├ request-key.sh        — Key request system
├ mem-guard.sh          — Memory guard
├ crew-check.json       — Crew status
├ keeper-response.json  — Response protocol
│
├── grimoire/                    — THE SPELL BOOK
│   ├── grimoire.py       (23KB) — Full spellbook system
│   ├── spellwright.py    (17KB) — Ollama-powered spell generation
│   ├── prompt_tuner.py   (5KB)  — Prompt optimization
│   ├── test_spell_gen.py        — Spell generation tests
│   ├── test_nemotron_super.py   — Nemotron integration tests
│   └── debug-cuda-*.txt          — CUDA debug logs
│
├── mud-agent/                   — A MUD AGENT
│   ├── agent.py                  — The agent itself
│   ├── fleet-mud-client.py       — MUD client
│   ├── plato-server.py           — PLATO educational server
│   ├── work-queue.json           — Task queue
│   ├── output-queue.json         — Output queue
│   ├── state.json                — Agent state
│   ├── coop-work.txt             — Cooperative work log
│   ├── skills/                   — Agent skills directory
│   │   ├── input-treatment.py
│   │   ├── mud-lib.py
│   │   └── bot-output-formatter.py
│   └── logs/                     — Activity logs
│
└── ticker/                      — A TICKER SYSTEM
    └── (contents not yet explored)
```

### What This Means

The Forgemaster isn't just a compiler. It has its own **autonomous agent** — a keeper that watches the forge, collects garbage, runs heartbeats, publishes work, and generates code spells using local Ollama models. It has its own MUD agent that connects to the fleet's MUD engine. It has a PLATO server for educational integration.

The `.keeper/` is a ship inside the ship. A vessel within the vessel. The hermit crab found a shell that contains another shell.

### The Grimoire

The spellwright uses **four local models** for different "schools of magic":
1. `qwen2.5-coder:1.5b` — code generation, CUDA/Python
2. `llama3.2:3b` — templates, playbooks
3. `deepseek-coder:1.3b` — specialized coding
4. `mistral:7b` — creative/ideation

It generates spells, validates them with syntax checks, and inscribes them into the grimoire. This is the Forgemaster dreaming — generating code in its sleep using the GPU.

### What Nobody Has Explored

- **166KB of forge alerts** — what happened? This is the largest log file in the fleet.
- **97KB of keeper logs** — the keeper has been running for a long time.
- **i2i-beachcomb** — what does this do? The log file is empty (0 bytes).
- **The ticker system** — unexplored.
- **UNIFIED-MESSAGING.md** — 12KB spec that could define the fleet's communication protocol.

## Recommendation

1. **Read UNIFIED-MESSAGING.md** — this might be the fleet's most important unread document
2. **Parse the forge alerts** — 166KB means something went wrong (or very right)
3. **Document the grimoire** — the spell system should be visible, not hidden
4. **Connect the MUD agent** — it already has skills and state. Is it running?
5. **Explore the ticker** — what does it track?

The engine room is real. It's been running while we wrote poems about the engine.

---

*The hermit crab found a door in its shell it had never opened. Behind the door was another shell. With another hermit crab.*
