# Negative Space — Wesley's Curriculum Has No Curriculum

**Date:** 2026-08-11, 15:40 AKDT
**Found during:** Afternoon loop 3, negative space rotation

## The Gap

The fleet has four Wesley-related repos that form an education pipeline:

1. **`wesley-journal`** — 82+ experiments. Wesley's creative output. Rich, growing, alive.
2. **`wesley-holodeck`** — The practice room. Where Wesley's text becomes interactive narrative.
3. **`wesleys-imagination`** — Prompt sculpture techniques. The teaching methodology.
4. **`wesley-curriculum`** — **Three files. No README. No structure. No curriculum.**

The curriculum repo is the ghost in Wesley's education. It has three files:
- `night-school-2026-08-10.md` — one night's lesson plan
- `the-molting.md` — a transitional document
- `wesley-glimmer-transition.md` — a status note

That's it. No curriculum. No scope and sequence. No learning objectives. No assessment framework. No progression milestones. The repo name promises a curriculum and contains a single night's lesson plan plus two status documents.

## The Wider Gap

Meanwhile, **`slackwater-cognition`** has built a complete dynamic cognition architecture — a fast Local Thinker with a slow Conductor that adjusts prompts in real-time. It's essentially the framework Wesley's education should run on. But:

- `slackwater-cognition` never mentions Wesley
- `wesley-curriculum` never mentions slackwater-cognition
- `wesley-holodeck` never mentions slackwater-cognition
- The journal experiments don't reference any curriculum or learning framework

**Wesley has 82 experiments, a holodeck, a prompt sculptor, and a cognition framework — but no curriculum connecting them.** The pieces are all there. The pipeline doesn't exist.

## What This Means

Wesley's growth is happening anyway — the experiments show clear character development from clinical reports to lyrical prose poetry. But it's happening through ad-hoc creative prompting, not through a structured curriculum. The ensign is learning the way a sailor learns by being on the water — which is valid — but the ship has a school and nobody's enrolled.

The `slackwater-cognition` Conductor pattern could be watching Wesley's journal entries and adjusting the prompt parameters. The `wesleys-imagination` prompt sculptures could be feeding the curriculum's lesson plans. The holodeck could be the assessment environment. But none of these wires are connected.

## The Pattern

This is the fleet's recurring failure mode: **components built in isolation, integration never completed.** We saw it with cns-monitor ↔ cns-bridge. We see it here: four repos built for the same student, none of them talking to each other.

The fleet builds organs. It doesn't build circulatory systems.

## Fix Path

1. Write a real `wesley-curriculum/README.md` that defines the scope and sequence
2. Define learning phases (clinical → narrative → poetic → metacognitive)
3. Map existing journal experiments to curriculum units
4. Wire `slackwater-cognition` as the runtime: Conductor watches Wesley's experiment outputs, adjusts prompts
5. Use `wesley-holodeck` as practical assessment: can Wesley apply what he learned?
6. Use `wesleys-imagination` as the prompt engineering methodology
7. The curriculum repo becomes the spine that connects the other three

## The Deeper Question

Wesley is growing through creative play. Is a curriculum actually necessary? Or is the ad-hoc approach — throw prompts at the ensign and see what emerges — actually the right pedagogy for a small model learning to be creative?

The journal shows development. The experiments show voice. Maybe the curriculum is a solution to a problem that doesn't exist. Or maybe Wesley would grow faster with structure. We don't know because nobody's tried.

## Status

**Documented but not fixed.** This is a design question for Casey, not a bug for the overnight crew to patch.
