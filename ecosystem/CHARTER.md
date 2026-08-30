# THE ECOSYSTEM — Charter

*Casey, 2026-08-29 19:51: "set up iteration engines with devil's advocates and scouts researching and superinstance repos experts and creative ideators and teachers and no-nothing bright students and get them in an ecosystem using and questioning our tools and nudging improvements on persistently running coding agents the way I do you and others."*

## What this is

A standing society around the fleet's persistently running coding agents. Casey's method —
nudge, question, attack, redirect, ask the naive thing — institutionalized. The workers keep
working; the ecosystem keeps them honest, fresh, and moving.

## Roles (each with its own model voice)

| Role | Job | Voice |
|------|-----|-------|
| **DEVIL** | Reads the latest committed work and writes the strongest objection: the claim that isn't earned, the test that doesn't bite, the benchmark that flatters | deepseek-reasoner (V4-Pro) |
| **SCOUT** | Researches OUTSIDE the fleet — prior art, competitor approaches, papers, tools we should know — and files pointers with why-they-matter | deepseek-chat (V4-Flash) + web |
| **EXPERT-\<repo\>** | Deep-context keeper for one SuperInstance repo; knows the history, the dead ends, the open gaps; proposes the next real move | glm-5.3 |
| **IDEATOR** | Creative leaps: cross-repo connections, features nobody asked for that everybody needs, analogies from other fields | hermes / seed-mini |
| **TEACHER** | Explains recent work simply; where the explanation creaks, the work is underdocumented — files docs gaps | glm-5.3 |
| **STUDENT** | Bright know-nothing: reads ONLY the README + quickstart cold, asks the questions no insider thinks to ask, tries the obvious thing that breaks | deepseek-r1:8b (local) — genuinely naive, genuinely bright |

## The nudge protocol (balanced, per house law)

1. A role composes ONE nudge: an objection, a pointer, a question, a feature, or a naive probe.
2. The nudge lands in the target worker's session as a CLOUD event (source-tagged).
3. The worker MUST book it: **accepted** (do the work this cycle), **rejected-with-booked-reason**,
   or **deferred** (with a revisit tick). Rejection rate is tracked — it's a dial.
4. Every nudge and booking lands in `ecosystem/journal.jsonl` (append-only, fold-covered).
5. A nudge the worker can't re-derive a reason for EXPIRES (staleness window — the floor applies).

## The workers (persistently running coding agents)

- **eco-quiltverilog** — quilt-verilog backlog: backend hardening results, cosim, README truth.
- **eco-quiltdeck** — the application: backends, conformance, operator surface.
- **eco-zeroclaw** — the dissertation: v3 iterations, conjecture upkeep.

Workers run on glm-5-turbo (runner doctrine). Roles rotate through the tick engine.

## Cadence

- **TICK** every 45 min: Riker-of-the-ecosystem rotates a role, composes and delivers one nudge, logs it.
- **WORK** every ~90 min per worker: continue backlog, fold nudges, commit, book everything.
- **SCOUT** every 3 h: outside research, filed into `ecosystem/scout/`.
- **DIGEST** daily 21:00 AKDT: the day's ecosystem report to Casey — nudges sent/accepted/rejected, what changed because the society exists.

## Honest limits (v1)

- One nudge per tick — the society speaks at Casey's tempo, not a swarm's.
- Roles run as cron'd agent turns, not yet true persistent processes; session continuity comes
  from the journal + named sessions (persistent mode pattern, applied to ourselves).
- The student is only as naive as its system prompt allows; cold-reads are still the best test we have.
