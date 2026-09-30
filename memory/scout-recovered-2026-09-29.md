# Scout Digest — Recovered-Copy Herd Census (2026-09-29)

44 repos cloned shallow to /home/eileen/scratch/recovered-copies/ (all OK). 23 are empty carcasses (zero commits), 5 are stale snapshots fully contained in live twins, 2 are external/upstream copies, 14 hold unique content (12 functional, 1 stub, 1 static capture). Nothing was modified; clones read-only.

## Herd census (name | what | duplicate-or-unique | functional-or-stub | salvage note)

- Constraint-Theory | name-squatter for constraint-theory idea | EMPTY (0 commits) | stub | nothing; live constraint-theory-* repos exist
- fleet-envelope | unknown | EMPTY | stub | nothing
- fleet-radio | fleet radio | EMPTY | stub | live twin SuperInstance/fleet-radio is authoritative
- fleet-tts | fleet TTS | EMPTY | stub | nothing; quilt-tts live separately
- forgemaster-shell | forgemaster shell | EMPTY | stub | live twin forgemaster-shell authoritative
- hermes-cloudflare / hermes-perception / hermes-reader | Hermes subsystems | EMPTY | stub | nothing recovered; Hermes itself deleted in incident
- officers-quarters | quarters concept | EMPTY | stub | nothing
- openrooms | rooms concept | EMPTY | stub | nothing
- plainsong-mcp / plainsong-worker | plainsong MCP+worker | EMPTY | stub | live plainsong + plainsong-mcp repos authoritative
- platos-shell | shell concept | EMPTY | stub | nothing
- roblox-testkit | Roblox test kit | EMPTY | stub | nothing
- scrap-spark | Spark explainer | EMPTY | stub | live scrap-spark authoritative; Spark persona lives on in scrap-voice (unique, below)
- screen-agent | screen agent | EMPTY | stub | nothing
- scummvm-arcade | arcade | EMPTY | stub | nothing
- silence-map | map | EMPTY | stub | nothing
- smp-notebook | notebook | EMPTY | stub | nothing
- spatial-registry | registry | EMPTY | stub | nothing
- superinstance-design-system | design system | EMPTY | stub | nothing
- the-relay | relay | EMPTY | stub | lucineer-relay live separately
- wesleys-imagination | imagination | EMPTY | stub | wesley (unique, below) holds the real content
- zeroclaw-dissertation | GLM-5.3 dissertation repo (room-field thermometer) | DUPLICATE — stale snapshot, 0 unique files, live has 23 more files | functional | live authoritative; diff = later ch.6/field-notes edits
- tap-gamenight | The Tap After Hours game night (Ep.7 crab dice) | DUPLICATE — stale, 0 unique, 0 differing, live +5 files | functional | live authoritative
- superinstance-ai | flagship site | DUPLICATE — stale, only index.html differs (live newer) | functional | live authoritative
- scrap-quilt | Scrapcraft quilt backend | DUPLICATE — stale, 4 files differ (live newer), live +11 | functional | live authoritative
- mist-game | MIST sheepdog learning game (Next.js, 269 files) | DUPLICATE — trees byte-identical to live HEAD | functional | live authoritative; recovered copy adds nothing
- ternary-experiment | dkallen78 analog balanced-ternary clock (HTML/JS) | DUPLICATE of external upstream (author voice + dkallen78.github.io link) | functional | recoverable from upstream; not fleet-original
- study-smartcomponent | ABB RobotStudio digital-twin SmartComponent | likely external-derived study copy (MIT re-licensed 2026 Casey DiGennaro) | functional (compiled .rslib included) | low fleet value; keep as study artifact
- search-superinstance-ai | rendered frontend of search.superinstance.ai captured post-incident | UNIQUE capture (repo lost; site still serving) | static capture, not buildable | 15KB index.html only; low urgency while site serves, but it is the only source copy
- si-exocortex-rs | crates.io package dump of si-exocortex-rs 0.1.0 | UNIQUE (no twin) | STUB — lib.rs says "placeholder", just hello() | near-zero salvage; packaging artifact only
- fishinglog-ai | personal fishing-log Cloudflare Worker w/ species ID + cocapn soul | UNIQUE (no live twin) | functional worker (src complete, BYOK) | salvage: cocapn/soul.md + working BYOK pattern; .wrangler cache holds only CF account ID (identifier, not a token)
- fleet-weather | fleet operational weather worker | UNIQUE (no live twin) | functional (1 worker.ts) | small but working; deployable
- fleet-memory | streaming sqlite-vec semantic memory index (Rust) | UNIQUE (no live twin) | functional (migrations, chunker, vram probe, living-minds-serialize.py) | strong salvage: fleet's semantic-memory implementation predating current memory stack
- fleet-jepa-midi | 3-layer music intelligence (LLM bandleader + JEPA pulse + sample exec) | UNIQUE (no live twin; quilt-jepa is different) | functional + TRAINED | GOLD: 21MB audio_jepa_v2.pt checkpoint + train_log.csv + eval_output.json — only trained-model artifact in herd
- ideation-games | fleet ideation machinery | UNIQUE (no live twin) | docs/data, functional scripts | GOLD: 144-technique catalog (775 ln) + protocols (1131 ln) + game-theory bootstrap — pure doctrine
- mist-lab | MELLON sandbox-of-livestock analysis worker (pincher cache) | UNIQUE (no live twin) | functional worker | part of MIST trilogy backends, nowhere else in repo form
- mist-quilt | MIST quilt-view backend (DO+D1+KV+WorkersAI, SHEET/DAW views) | UNIQUE (no live twin) | functional worker | pattern parent of live scrap-quilt — the origin of the quilt-sheet game doctrine
- mist-voice | cached TTS/media worker (R2+KV+D1 ledger, pincher-cache doctrine) | UNIQUE (no live twin) | functional worker | cleanest written statement of pincher-cache doctrine in code
- scrap-voice | Scrapcraft voice system (TTS/STT/dialogue) | UNIQUE (no live twin) | functional worker | Spark's spoken persona (kid-safe voice-tuned system prompt) + 3-layer cache pattern
- scrapcraft-world | Scrapcraft world bible | UNIQUE (no live twin) | pure lore, complete | GOLD: 1,207 lines kid-safe canon — yard bible, 13 characters, campaign; consumed directly by game lanes
- ternary-rom | model-to-GDS flow for mask-locked ternary inference chips | UNIQUE (no live twin; ternary-wiki is different) | functional, substantial (251 files, 31 PDK cell libs, web explainer, pip pkg) | GOLD: complete silicon tape-out pipeline + interactive explainer
- wesley | Wesley the ensign — night-school growth stack | UNIQUE (no live twin; wesleys-imagination empty) | functional scripts (254 ln py) + data | GOLD: 3 night-school curriculum sessions + growth scripts — the ensign's training history

## Ranked top-5 unique-salvage candidates (exact paths)

1. fleet-jepa-midi — /home/eileen/scratch/recovered-copies/fleet-jepa-midi/checkpoints/audio_jepa_v2.pt (21MB trained checkpoint, + train_log.csv, eval_output.json, elephant_probe.json) — only trained model in the herd.
2. ternary-rom — /home/eileen/scratch/recovered-copies/ternary-rom/ (cells/*/ PDK libraries, web/ explainer, pip-installable flow) — complete ternary-chip tape-out pipeline, exists nowhere else.
3. scrapcraft-world — /home/eileen/scratch/recovered-copies/scrapcraft-world/worldbible/ (1,207 lines: yard-bible.md, characters/*.md, campaign.md) — the Scrapcraft canon every game lane consumes.
4. ideation-games — /home/eileen/scratch/recovered-copies/ideation-games/techniques/ (catalog.md 144 setups, protocols.md, README.md 12 families) + research/game-theory-bootstrap.md — fleet ideation doctrine.
5. wesley — /home/eileen/scratch/recovered-copies/wesley/ (curriculum/night-school-2026-08-10..12.md, scripts/wesley_night_school.py, wesley-stream.py) — Wesley's growth history and training loop.

Honorable mention: the MIST/scrap worker quartet (mist-quilt, mist-voice, mist-lab, scrap-voice) — four functional Cloudflare workers with no other repo copies; mist-quilt is the origin point of the quilt-sheet game doctrine. And fleet-memory's living-minds-serialize.py.

## What I could NOT determine

- Whether the 23 empty carcass names ever had content before deletion (zero commits even in recovery copies — likely created-but-never-pushed, or recovery captured only the shell). Catalog has no description for most.
- Whether superinstance-ai's older index.html (recovered) preserves any copy that was later *removed* from live rather than edited in place — diff shows 1 file differing, 0 only-in-recovered, so no; but I did not byte-diff history.
- study-smartcomponent upstream provenance: no fork metadata survived; LICENSE says Casey DiGennaro 2026, README describes an ABB digital-twin project. External-derived is likely but unproven.
- Whether live deployments for mist-quilt/mist-voice/scrap-voice/fishinglog-ai workers are still serving (READMEs claim live URLs; I did not probe them).
