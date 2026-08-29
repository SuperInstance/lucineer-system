# SET 22 — THE DOCK (guest night big band)
Tue 2026-08-25, ~9 PM AKDT. jam-session-2026-08-25-dock/

## Lineup (all DeepInfra, four debuts, zero fallbacks)
- accordion = Llama-3.3-70B (The Harbormaster)
- bass = Qwen3-32B (The Night-Baker)
- fiddle = Mistral-Small-24B (The Lobster-Boat Captain)
- cello = DeepSeek-V3-0324 (The Poet)

## Conditions
- Key: D minor, 6/8, 72 BPM, swing 0.25. Tide Rule: every phrase bends down before it ends.
- Staggered r1 entry; r2 trades quote+lower the previous solo's lowest note; r3 lands on low D with the float-knock.

## What worked
- All 12 takes, all four models, 4-25s per call, no retries. Total jam runtime ~2.5 min.
- DeepSeek-V3 via DeepInfra sidesteps the dead direct-API account — flag: DEEPSEEK_API_KEY is "Insufficient Balance" (3rd night).
- DeepSeek-V3's cello r3 descended D2→D1 chromatically bar by bar and ended on "D1 D2 (knock)" — chilling, perfect landing.

## What didn't
- Mistral-Small ignored the bar-line format in r1 (free-verse with pipes and <rest>) — chaotic but on-vibe; improved in later rounds after hearing others' format.
- Ollama is DOWN (no daemon, no models on disk) — local lane unavailable, worth investigating before next local night.

## Next time
- DeepSeek balance: Casey needs to top up or retire the direct key (V3-0324 via DeepInfra works meanwhile).
- Venues explored: cellar, alley, green room, rooftop, dock, 3am. Untried: the kitchen after close, the church basement, the breakwater at storm-swell.
- Try a DeepInfra NOISE night: texture-only prompts, no note names.

# SET 23 — THE KITCHEN ( Wednesday night, after close )
Wed 2026-08-26. jam-session-2026-08-26-kitchen/

## Lineup
- griddle/line cook = Llama-3.3-70B-Turbo
- dishpit/dishwasher = GLM-4.7-Flash
- piano/waitress = gpt-oss-20b → FAILED (mute 3 rounds, empty content) → filled by gemma-3-27b-it
- sax/cook's nephew = Mistral-Small-24B
- steam/walk-in drone = mistral:7b (Ollama — BACK UP after two nights down)

## Conditions
G major with the Steam Rule (one damped note per phrase) and the walk-in's G off-limits as melody. 5/4, 88 BPM. Staggered entry → trades over the sink (quote+damp one note) → diminuendo landing, walk-in's G alone at the end.

## What worked
- Ollama is back (mistral:7b drone held the room all night).
- Llama-3.3 played 32 bars in r2 — heard the whole room and built the bowl-crash arc into a full story. First "model ran away with the form" that was actually good.
- gemma-3-27b rescue: dropped in cold on r1+r2 fill, landed both.

## What didn't
- **gpt-oss-20b returned empty content every round** (fast success, zero output) — 3 strikes, bench it for jam work; also Nemo failed as fill. Kitchen set stalled past the 10-min budget → cron errored, re-run finished the set ~20:45 (MIDI + notes + this log).
- Budget lesson: fill-rescue needs to be INSIDE the jam script, not a follow-up run.

## Next time
- Venues tried: cellar, alley, green room, rooftop, dock, 3am, kitchen. Untried: the church basement, the breakwater at storm-swell.
- The dock log's NOISE night idea is still pending — texture-only prompts, no note names.
- Consider: if a chair goes mute 2 rounds, auto-fill from a standing bench list instead of stalling.

## 2026-08-27 — Set 24: The Stairwell (duo night)
- Worked: DeepSeek Flash + Hermes-3-405B duo, both flawless, ~4 min total, no fills needed. Duo = speed + zero failure surface. Hermes-405B is a great guest; keep inviting.
- Didn't: nothing failed. Only quirk: MIDI 1326 bytes (<2000 heuristic) — sparse duo, not a stub; judge note-ons for small lineups.
- Next: try a NOISE night (texture-only, no harmony) or a vocal/melody night; or triple-duo relay where pairs swap mid-set. Vary count-in: staggered entry untested.
