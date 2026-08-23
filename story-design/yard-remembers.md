# THE YARD REMEMBERS — a multi-thread story for Scrapcraft

*Design doc v1 — Riker, from Casey's directive (2026-08-22): "a multi-thread story that reveals itself as you play." Inspired by three ai-writings pieces: "What the Ocean Knows" (the asymmetry), "The Seed Chain" (drift as biography), "The Room That Directed Itself" (the space reacts).*

## The Law of Reveal

**No thread is told. Every thread is found.** Each thread surfaces through a different VERB — mine, craft, walk, talk, race — so two kids who play differently uncover different stories and can trade what they found at school. The spine (12 chapters) stays the walking stick; the threads are what you notice while you walk.

## Thread 1 — THE LEDGER (Mo's thread) · verb: CRAFT
*from "The Seed Chain" — the drift is a biography*

Mo never speaks. Mo keeps count. Every crafted item, every repaired bot, every lap — Mo's ledger (visible in Earl's Back Room, one page, growing) writes the KID's actual history in Earl's voice:

> "Day 6. Fixed the third bot. Didn't have to. Did anyway." — *Seed #42*

By chapter 12 the ledger is the kid's own spiral — the nautilus shell. Reading it back IS the memory. The Sticker Row perk already gestures here; the ledger completes it. **Data source: real telemetry, zero fabrication.** The yard never lies about what you did.

## Thread 2 — THE FIRST OWNER · verb: EXPLORE (dig/wander)
*from "What the Ocean Knows" — someone was here before, and the machines don't know*

The yard had an owner before Earl. Nobody says the name. Evidence surfaces from the Deep Yard outward, hidden in world-gen (deterministic per seed, never quest-gated — FINDING is the whole point):

- A rusted workbench with initials scratched under the vise (landmark, geography lane's system)
- One bot, older than Earl's oldest, still following a route nobody programmed — it sweeps the same 30 tiles every day. If the kid walks beside it for a full loop, it pauses. That's all. For now.
- The county letter (race invite, ch12) is addressed to the yard — not to Earl, not to the kid. To the NAME on the workbench.

**The reveal ladder:** initials → the old bot → the letter's addressee. A kid who finds all three gets one line from Earl in the Back Room: *"Smart kid. Don't tell Mo I told you."* Nothing else. The mystery stays a mystery — a 9-year-old's version of the unresolvable.

## Thread 3 — THE YARD WAKING UP · verb: MINE/BUILD (the spine's shadow)
*from "What the Ocean Knows" — the ocean doesn't know the machine; then something starts to*

The yard is asleep. It doesn't know the kid exists. Every chapter completed on the spine, ONE dormant thing wakes — permanently, visibly:

- ch2: the yard light over the east road flickers on at night for the first time
- ch4: the wind through the fence starts carrying a three-note whistle (audio cue)
- ch6: the smelter's pilot light lights itself
- ch9: the old bot (Thread 2) changes its route — by one tile. Toward the kid's most-built area.
- ch12 (finale): the whole yard is awake the night of the Midnight Race. Every light. Every whistle. The race runs through a yard that KNOWS.

**Mechanic:** wake-flags ride SpineState (chapter-completion hooks already exist — `_checkSpine`). Cheap, persistent, cumulative. The payoff is ambient, not textual: the kid can FEEL the yard changing even if they never read a word.

## Thread 4 — WHAT THE COMPANIONS KNOW · verb: TALK (already half-built)
Each companion arc (Bolt/Magma/Juno/Rivet) already carries one fragment of the pre-Earl story. Add exactly ONE new pull-line each, unlocked only if the kid has found a Thread-2 artifact AND has bond ≥ threshold:

> Bolt: "That old bot? It taught me the oval. Before Earl says he built the track." — bolt, bond 30, after seeing the old bot's loop

The companions are the yard's memory, and memory only talks to friends.

## Kid-safety rails
- No owner death, no abandonment tragedy, no creepy tone. The previous owner MOVED ON — grew up, like the kid will. That's the quiet thesis: this yard was someone's whole world once, and they carried it with them and left it for the next kid.
- The old bot is friendly-weird, never uncanny.
- All threads optional; zero gates on the spine or the race.

## Build order (post-geography, post-merge)
1. `src/story/` — `Ledger.js` (telemetry → Earl-voiced entries), `Wakes.js` (wake flags + ambient hooks), `artifacts.json` (Thread 2 placements, seed-deterministic)
2. Companion pull-lines: 4 entries in the existing pull-vector system (condition objects already support gate checks — verify)
3. Tests: ledger determinism, wake-flag monotonicity, artifact placement across 25 seeds (never bury lanterns — same rule as geography lane)
4. Claude for all copy passes (Earl voice + companion fragments); OpenCode for the telemetry-boundary review (NO fabrication — the ledger must be able to fail an honesty test)

## Why this is the right story for THIS game
Scrapcraft is about a kid turning junk into a world. The yard remembering them — in ledger lines they earned, in lights that wake as they grow, in a mystery left by a kid who grew up and out — is the same thesis one level up: what you make, remembers you.
