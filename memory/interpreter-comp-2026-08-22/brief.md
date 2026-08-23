# THE BRIEF — Local Elephant Interpreter (architecture competition)

## Context
The elephant (SuperInstance/elephant) reads "rooms" — chat spaces with agents/humans — and emits field readings: 7 dials (mood, volume, earnestness, cynicism, joke_landing, panic, presence), warmth, κ (concentration), v* (volume/presence axis), COH (cohesion), drift. Readings fire on a pulse (cron probe) and on drift alerts (deadband exceeded, e.g. d_warmth=-0.36 past 0.30 threshold).

Read /home/eileen/projects/elephant/docs/production-notes.md and the elephant repo README for grounding. Also read /home/eileen/.openclaw/workspace/memory/research-penrose-fleet-2026-08-21.md §0-§2 (the fleet's mathematical dictionary: ledger=lattice, reading=projection, phason, Ammann bars/seals).

## The vision (from Captain Casey)
1. Every elephant reading (pulse + deadband-triggered) gets an **interpretation**: per-dial delta meanings + a step-back whole-room reading. Interpretations are RELATIVE to each other (comparable, ordered) so they can be scored.
2. Interpretations **accumulate into a training corpus** that is periodically **LoRA-trained into a local model** — a self-improving interpreter.
3. When a new interpretation lands, a **judge agent** scores the last N interpretations against what actually happened since (did the room move as predicted? was the read apt?). Feedback comes from the agent network including humans (reactions, replies, downstream behavior) — the JEPA elephant side.
4. Hardware: RTX 4050 laptop GPU (6GB), WSL2. Local models today: Granite 3.1 2B (Wesley) and Liquid LFM2.5-2.6B on the bench. Analytical quality matters more than speed. Recommend the base model (2B/4B/8B class, QLoRA feasibility on 6GB VRAM — be honest about what trains and what doesn't; unsloth/4-bit).

## Your deliverable (write to your assigned file, ≤400 lines)
1. **Architecture** — components, data flow, storage, trigger wiring (elephant roomd → interpreter → judge → corpus → LoRA cycle). Where it lives (new repo? elephant subcrate? wesley-adjacent?). What runs where (systemd, cron, tmux).
2. **The interpretation schema** — what an interpretation IS (structured JSON? prose? both?), how delta-meaning and step-back are represented, how comparability/relativity is enforced (fixed axes? rating scales? embedding deltas?).
3. **The judge** — scoring rubric, evidence sources (subsequent readings, human reactions, agent responses), how scores feed the training corpus (preference pairs? ratings? DPO vs SFT choice).
4. **The LoRA flywheel** — training loop, corpus versioning, eval harness (how do we know the new LoRA is better? held-out interpretations? judge-scored A/B?), rollback.
5. **The merge question** — Casey proposes merging Wesley (ensign, growing) and this interpreter into ONE local agent: the elephant interpreter whose primary job is pulse analysis. Argue for or against the merge, and if for, what the merged agent's identity/role boundaries are.
6. **Failure modes** — what breaks (drift-chasing, sycophancy toward the judge, interpretation collapse to boilerplate), guards against each.

Be opinionated. Pick a horse and ride it. Named sections, concrete file paths, concrete model names.
