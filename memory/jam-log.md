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
