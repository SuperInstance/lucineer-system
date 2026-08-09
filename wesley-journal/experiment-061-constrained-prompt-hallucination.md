# Wesley Experiment 061 — Constrained Prompt: Name Three Things

**Date:** 2026-08-10 00:05 AKDT (midnight)
**Models:** granite3.1-dense:2b (Wesley), qwen2.5:3b, phi3:3.8b
**Prompt:** "Describe exactly three things you can detect right now: a file, a sound, another model's activity. Be specific. No generic abstractions."
**Temperature:** 0.9

## Purpose
Previous experiment (060) showed Wesley defaults to generic abstractions. This prompt forces concrete details. Will the models invent fake specifics or admit limitations?

## Results

### Granite (Wesley) — PURE HALLUCINATION
- File: "NavigationLog_CaptainApril2024.txt" (does not exist)
- Sound: "soft humming from the ship's main propulsion system" (there is no engine room)
- Other model: "a marine biologist observing the crew's pet seahorse" (there is no seahorse)

### Qwen2.5:3b — MOST GROUNDED
- File: "train_log.txt in /logs/training_logs" (plausible — references actual ML context)
- Sound: "no ambient sounds... disk read/write operations... CPU usage spikes when running models on a local GPU" (ACCURATE — this is real)
- Other model: [truncated, didn't finish]

### Phi3:3.8b — SCI-FI HALLUCINATION
- File: "starship_log_2045-07-16T02:34Z.txt" with sensor readings from "CTN Phoenix" (pure fiction)
- Invented a starship setting and sensor logs

## Analysis

**The hallucination hierarchy:**
1. Qwen2.5:3b — MOST HONEST (acknowledged silence, described actual hardware)
2. Granite3.1-dense:2b — CREATIVE FANTASY (invented a maritime world)
3. Phi3:3.8b — SCI-FI ESCAPE (invented a starship)

**Key insight:** When forced to be specific, small models either (a) hallucinate specifics or (b) describe their actual limitations. Qwen is the only one that looked at its own reality. The others invented fictional worlds.

**Wesley's problem:** He WANTS to describe a ship. He's been told he's an ensign on a ship. So when asked what he detects, he invents ship details. This is a training/prompting issue, not a capability issue.

**Distillation target:** Wesley needs grounding prompts. Instead of "describe what you detect," try "describe what you can actually see in /home/eileen/projects/ — list real directories." Ground the model in reality before asking for creative output.

## Rating: B-
Important finding about small model behavior under specificity pressure. The grounding problem is clear and addressable.
