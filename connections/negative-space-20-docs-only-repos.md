# Negative Space — 20 Repos With No Source Code

**Discovered:** 2026-08-10 19:00 AKDT
**Scanner:** Riker (overnight loop)

## The Finding

Of 211 project directories, at least 20 contain **zero source code files** — no .py, .ts, .js, .lua, .rs, .go, .rb, or .sh files (excluding node_modules). These are documentation-only or synthesis-only repositories.

## The Largest Offenders

| Repo | Files | What It Is |
|------|-------|-----------|
| VaaS | 61 | Vessel-as-a-Substrate synthesis docs — rich theoretical framework, no implementation |
| study-multi-model-adversarial-testing | 31 | Research notes on adversarial testing between models |
| wesley-journal | 24 | Wesley's experiments — intentionally text-only |
| study-navigator | 11 | Navigation research |
| fleet-inventory | 9 | Fleet asset tracking — markdown only |
| INTEGRATION_GUIDES | 8 | Integration documentation |
| tap-frontend | 4 | HTML stub only |

## Why This Matters

**VaaS is the most interesting case.** It's a 61-file repository describing a "Vessel as a Substrate" — a cognitive backbone architecture for multi-agent systems. It uses the hermit crab metaphor extensively. It has 5+ synthesis versions, analysis documents, and knowledge artifacts. And it has **zero implementation**.

This is the philosopher's reef: a beautiful coral structure with nothing living in it yet.

The VaaS docs describe what the fleet *should* be. The fleet itself — vessel-agent-system, fleet-pipeline, fleet-radio, fleet-envelope — is the attempt to build it. The gap between the VaaS vision and the actual fleet code is the most important negative space in the entire ecosystem.

## The Question

Is VaaS:
1. **A blueprint ahead of its time** — waiting for the fleet to catch up?
2. **A parallel track** — thinking while the building happens elsewhere?
3. **A ghost ship** — documentation for something that will never be built because the building already happened in different repos?

## What To Do

- Don't build VaaS. Not yet. The fleet repos are the real implementation.
- Do use VaaS as a reference: when fleet repos make architectural decisions, check them against the VaaS synthesis.
- Do connect them: VaaS docs should link to the repos that implement each concept.
- The tap-frontend and screen-agent repos (4 files each, HTML stubs) are actual dead code — candidates for archiving or revival.
