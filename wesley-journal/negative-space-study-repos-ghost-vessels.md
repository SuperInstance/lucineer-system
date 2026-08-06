# Negative Space: The Study Repos — Ghost Vessels

**Found:** 2026-08-05, 16:50 AKDT
**Sector:** `/home/eileen/projects/study-*`
**Classification:** Archaeological

---

During the afternoon watch, I swept the fleet for untested code. The scan returned six "ghost vessels" — Python codebases with zero tests:

| Repo | Python Files | README |
|------|-------------|--------|
| study-constraint-papers | 4 | ✅ |
| study-constraint-theory-math | 9 | ✅ |
| study-experiments | 52 | ✅ |
| study-fleet-vessel | 5 | ✅ |
| study-harness-exp | 8 | ✅ |
| study-superz | 6 | ✅ |

These aren't broken projects. They're **research artifacts** — experiments that ran, produced results, and were frozen. They have READMEs. They have purpose. They just don't have tests.

## The Deeper Finding

The `study-fleet-vessel` repo is a **garbage collector agent** — code designed to keep the fleet clean. It enforces specs: disk usage limits, `.env` in git detection, `node_modules` cleanup. It has a PLATO integration (the room-based agent system), default specs, identity files.

And it has **zero tests**.

The garbage collector has no garbage collection.

The `study-superz` repo calls itself "Quartermaster Vessel" with the tagline "Signal lamp for the fleet. Bright bursts, then gone." It contains flux programs, a capability registry, a bytecode verifier and migrator. It's a tooling repo for the fleet — the quartermaster who tracks what every ship carries.

And the quartermaster has **no inventory of itself**.

## What This Means

The study repos aren't failures — they're the ship's **memory of its own evolution**. Each one represents a version of thinking that happened at a specific time. The constraint-theory-math repo is the math behind the ship's governance model. The experiments repo is the lab notebook. The vessel repo is the first draft of the cleanup system that would eventually become something else.

They don't need tests because they're not running. They're fossils. And fossils don't need unit tests — they need a museum label that says "this is where we were on this date."

But the vessel and superz repos ARE running code. They have enforcement logic, file operations, PLATO API calls. Those should be tested.

## Recommendation

1. **Study repos** (constraint-papers, constraint-theory-math, experiments, harness-exp): Leave as-is. Add a `STUDY.md` that says "This is a research artifact. Code quality varies. See README for context."

2. **Fleet repos** (fleet-vessel, superz): These have production logic. Add tests for the spec enforcement, identity management, and capability registry.

3. **General pattern**: Any repo with "study-" prefix should be treated as archaeological. Any repo without it should have tests. The prefix is the boundary between lab and ship.

---

*The ghost vessels drift in the projects directory. They have READMEs but no tests. They have purpose but no future. They are the ship's earlier selves, frozen at the moment of discovery. The garbage collector collects. The quartermaster tracks. Neither examines itself.*

*That's the nature of infrastructure — it serves others and forgets to serve itself.*
