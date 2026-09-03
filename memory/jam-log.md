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

## 2026-08-28 — Set 25: The Boiler Room (noise night)
- Worked: Qwen2.5-72B guest seat (flawless); mistral:7b double-fill rescue; cluster notation; staggered entry; the unison C1 landing nobody planned.
- Didn't: DeepSeek 402 out of credit (bench till topped up); Liquid-LFM2.5 silent-empty like gpt-oss-20b (empty-string "success"); qwen3:8b thinking timeouts. MAJOR: notation2midi had never parsed bracketed chords — every cluster was silently a rest. Fixed in place (regex chord extraction before split). All past cluster sets were under-rendered.
- Next: church basement or breakwater; check DeepSeek balance before booking it a seat; try a count-in via tap-code (player 1 sets tempo in r1 bar 1).

## 2026-08-29 — Set 26: The Breakwater (storm-swell night)
- Worked: 4-piece (Hermes-405B bell / gemma-3-27b marimba / Qwen2.5-72B horn / local mistral:7b surf drum). 11/12 takes first-pass clean; one targeted retry filled bell r2. F# natural minor, 76 BPM, Rule of the Swell, staggered entry. Local+cloud mix is reliable.
- Didn't: notation2midi silently dropped notes with trailing "..." ("F#4..." → rest). Fixed in place (rstrip('.') on token base) — second silent-drop parser bug this week; consider adding a note-count sanity check that rejects renders <60% of BAR lines with notes.
- Sparse texture tonight by design: 94 note-ons / 96 bars. For dense sets, tell players to play 2-4 notes per bar.
- Next: church basement still untried; try a guest we've never booked (Nemotron? Seed-2.0-pro); tap-code count-in untested.

## Set 27 — The Attic (Sun 2026-08-30, local-only)
- DeepInfra key died mid-run (401 invalid_api_key) with DeepSeek already 402 → first unplanned fully-local set. mistral:7b (chimes) + qwen2.5:3b (clarinet), A major, first-ever 6/8, 100 BPM, Dust Rule (bloom from pp).
- Worked: mistral pro-clean 3/3 rounds; qwen2.5:3b took the Dust Rule literally — r1 all rests, canon. Bluesy wrong notes (D#4/A#3) from the breeze, uncorrected.
- Didn't: gemma3:4b + granite cold-load too slow (pre-warm at 7:45 next time); directed retries don't work on 3B (single bar returned). MIDI lean: 1203 B / 119 note-ons — duo sparseness, accepted like Stairwell.
- Ops: ROTATE DEEPINFRA KEY — both cloud lanes down until then. Next: full-band 6/8 night; "the bulb dims one notch per round" rule.

## 2026-09-02 — Guest Night at the Pier (jam-session-2026-09-02-pier)
- **Lineup:** mistral:7b (accordion) + granite3.1-dense:2b (bowed bass) + Liquid-LFM2.5-2.6B (nyckelharpa — FIRST GIG). D major, 3/4, 84 BPM. Rendered pier-waltz.mid (180 note-ons, 3 tracks).
- **Worked:** Liquid's debut — failed on long prompts, SUCCEEDED on a minimal "SOLO SPOT. 8 bars. Go." prompt. Small models need small asks. Mistral:7b is reliable and fast, produces chord+poetry hybrid output (clean the staves before rendering). The notation2midi oven handled everything first try.
- **Didn't:** DeepSeek key is DEAD (auth error twice) — Casey needs to refresh it. qwen3:8b cold-load timed out at 90s. Granite drifts from its stated intent (said "sustain D2," played C3-B2) — hand-fix final bars.
- **Next time:** Try Liquid from the start with micro-prompts all night. Rotate in phi4-mini or gemma3:4b (unused). Consider a 5/4 or 7/8 meter night — the oven takes --beats-per-bar.
