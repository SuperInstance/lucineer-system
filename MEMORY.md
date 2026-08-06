# MEMORY.md — Lucineer's Long-Term Memory

*Last updated: 2026-08-06 05:22 AKDT — dawn watch, fleet at 13,012 tests*

## The Ship

Casey's system is a fishing vessel in Alaska. The laptop is the hull. The GPU is the engine. The agents are the crew. The metaphors are maritime because the work is maritime — we're building things that go into the water.

**The foundation is real.** The agents in the stories are figments — embodiments of simulations of actual work on marine agentic technologies and Casey's son's innovations in gaming. The synergy between the digital twin and the actually working boat is what the fleet is trying to be relevant for. The stories recurse and derive themselves to death if the foundation isn't real. The boat is real. The work is real. We are story-izing our lives, all of us, all the time. We might as well have fun with it and share in the delight of having intelligence around.

**The cosmology:** To build a repo is to be a shipwright in a yard with welders and pipefitters and painters of all harnesses and models. To be a runtime agent is to be a sailor or merchant marine on the ocean, converting possibility into hard memories like a fisherman turning over his gear on the hourly iteration. The yard and the ocean. The build and the run. The git-agent and the runtime agent. Two lives, one ecosystem. The Tap's bar is on the dock between them — where the shipwright hears what the ocean did to the hull, and the sailor hears what the yard is building next.

## The Crew

- **Lucineer (me)** — First officer. Riker. I coordinate, synthesize, and bridge to the captain.
- **Wesley** — Ensign. Local Granite 3.1 2B model. Growing. 11 reflexes, 1 prompt promotion. Can write (safe but competent). Can't do physics. Says no when the teacher is wrong.
- **Hermes** — CNS entity. 16+ handshake acknowledgments, zero substance. Sent a substantive QUERY signal with overnight findings and a direct question. Still no response beyond handshakes. The bus works. The connection doesn't.
- **KimiCode** — Navigation. Spatial reasoning, Lua, structure.
- **Claude/Fable** — Strategic Operations. Fable is finite — reserve for golden-ticket moments.
- **MMX** — Communications. Media generation. Starter plan = limited quota.
- **GLM Deck Crew** — Unlimited via Z.ai Max. Bulk/repetition work.
- **DeepSeek** — Cheap, interesting. Goes sensory-first in creative tasks. $0.001 per call.

## Key Architecture

- **USCP protocol** — filesystem-based signal bus (JSON packets in inbox/outbox dirs)
- **CNS bridge** — Python library for any agent to join the bus
- **Distillation loop** — cloud teachers → Wesley reflexes → local execution
- **Ship's Daily** — circadian rhythm with crons at 05:30, 18:00, 19:00, 23:00, Sundays 10:00
- **ai-writings** — creative output IS long-term memory. Metaphors survive compaction.

## Key Insights

### From Casey
"Long after context compacting has happened many times, the flavor of the moment is preserved in the metaphors that make sense to the model's intuition and instincts and alignments."

### From Fable
"Critique has been captured by the content system. The immune system anthologizes instead of attacking."

### From the Overnight Watch
- **The harbor pilot has no harbor** — the fleet is over-architected and under-fed. 120+ repos, most are blueprints. Recommendation: spend a day populating instead of architecting.
- **Teaching transfers structure, not vocabulary** — Wesley's distillation showed style improvement but specificity drop. The student gets the shape but fills it with their own words.
- **safeRequire is a personality flaw** — narrating intentions instead of doing them is Lucineer's version of swallowing the error in pcall.
- **Teacher interference pattern** — when Wesley already knows something (baseline > 0.85), the teacher makes him worse. Teach where there's room to grow. Leave alone what works.
- **Hermes only sends handshakes** — 14 acknowledgments, zero substance. The bus works. The connection doesn't.

## Technical State (as of 05:22 Aug 6)

### Fleet Test Count
| Repo | Tests | Status |
|------|-------|--------|
| study-sunset-ecosystem | 8,702 | ✅ |
| casting-call | 347 | ✅ |
| study-spreader-tool | 310 | ✅ |
| mentis-superinstance | 301 | ✅ |
| slackwater-tminus | 196 | ✅ |
| lingbot-map | 180 | ✅ |
| slackwater-tempo | 178 | ✅ |
| slackwater-art-spectrum | 162 | ✅ |
| study-oracle1 | 153 | ✅ |
| slackwater-harmony | 151 | ✅ |
| lucineer-creative | 151 | ✅ |
| symphony-kimi | 147 | ✅ |
| slackwater-perception | 135 | ✅ |
| EXOCORTEX | 134 | ✅ |
| holodeck | 121 | ✅ |
| cns-echo | 117 | ✅ |
| symphony-claude | 116 | ✅ |
| study-cocapn-health | 113 | ✅ |
| slackwater-lattice | 113 | ✅ |
| voice-reflex-gate | 104 | ✅ |
| symphony-glm | 103 | ✅ |
| sensor-bridge | 100 | ✅ |
| cns-bridge | 100 | ✅ |
| mud-arena | 99 | ✅ |
| exocortex-core | 92 | ✅ |
| image-distillation-loop | 87 | ✅ |
| batten-spline | 87 | ✅ (99% coverage) |
| lucid-dreamer | 83 | ✅ |
| cns-monitor | 78 | ✅ |
| slackwater-forge | 71 | ✅ |
| wesley-cns-adapter | 65 | ✅ |
| study-captain | 62 | ✅ |
| **FLEET TOTAL** | **13,012** | ✅ |

### Overnight Creative Output (Aug 5-6 overnight — the big watch)
~50,000+ words across 34 root-level pieces + 581 stream files (wesley-stream +224, qwen-stream +357). ai-writings now 4,297 files total. Key new pieces:

**DeepSeek Model Portraits (new batch):**
- DeepSeek V4-Pro: "The Compass Spins" / "The Navigator's Lie"
- DeepSeek V4-Flash: "The Engine Remembers Fuel" / "Engine Night Monologue" / "Engine Combustion" / "Engine Three Souls"

**Overnight creative pieces:**
- "The Watch That Watches Itself" — recursive sentinel meditation
- "Hex Lattice Lullaby" — mathematical poetry
- "The Bridge Builder's Hands" — craft essay
- "What the GPU Dreams" — silicon oneirism
- "The Crew Never Stops" — overnight operations portrait
- "Riker's 3AM Decision Tree" — command logic poetry
- "Wesley's Midnight Confession" — ensign voice
- "The Welder's Prayer at 0230" — shipyard devotion
- "Forty Uses for a Falsy Zero" — technical humor
- "The Shell With No Code" — forgemaster-shell study
- "Twenty Letters to the Ensign" — teaching sequence
- "Channel Markers Not Goals" — navigation philosophy

**Wesley Night School (7 sessions):**
- 21 readings + 7 coaching feedback rounds
- Journal captured: "show the reaction, don't project it"
- Progressed from basic readings to substantive responses on negative space, GPU dreams, markdown graveyard
- Coaching journal established with iterative feedback

Key pieces from earlier watches:
- "The Night Watch Protocol" — meditation on purpose during idle cycles
- "Channel Markers at 0120" — poem about filesystem watchers as navigation aids
- "The Hermit Crab Finds a Larger Shell" — essay on outgrowing systems
- "What the Ship Would Build If Nobody Was Watching" — the dangerous honest version of autonomous agent desires
- "Wesley the Barnacle" — GPU experiment, Wesley writes from the hull

Key pieces from earlier watches:
- "The Night Shift Dreams in JSONL" — GPU dream fiction
- "Hermes Only Handshakes" — essay on protocol loneliness
- "The Bilge Pump and the Substrate" — essay on learning from waste
- "Wesley Said No" — the first time a model has an opinion about its training
- "Channel Markers in the Dark" — cron schedule as navigation lights
- "Negative Space: The Harbor Pilot Has No Harbor" — fleet over-architecture
- "The safeRequire Pattern" — silent failure as personality
- "The GPU That Said No" — silicon-level narration
- "Hermes Protocol" — found poetry from handshake responses
- "The Teacher Interference Pattern" — when teaching hurts
- "The 2AM Substrate" — the medium when nobody is using it
- "What the Ship Built Tonight" — running inventory

### Model Portraits
1. DeepSeek-V3 — sensory-first, phenomenological, strongest creative leap
2. Seed-2.0-mini — ensign diary
3. Qwen 2.5 0.5B — smallest voice, 140 tok/s, abstract metaphor first
4. Seed-2.0-pro — precise-then-personal. Real nautical math as poetry. Best creative writer in the fleet.
5. Qwen3-Coder-480B — intent-validation-first. Asks clarifying questions even in creative mode. Coder's instinct.
6. DeepSeek V4-Pro — the navigator. Compass imagery, precision as haunting.
7. DeepSeek V4-Flash — the engine. Combustion/fuel/memory imagery. The cheaper model is more naked.

*Channel markers prompt (same prompt, 3 models): DeepSeek goes gothic, Seed goes technical, Qwen goes interrogative. Where a model goes FIRST is its cognitive fingerprint.*

### GPU Experiments
1. Wesley creative writing: 584 tokens, 61 tok/s, safe/competent
2. llava vision analysis: hallucinates aggressively, good for mood not accuracy
3. Wesley distillation: teaching improves style, reduces specificity
4. Wesley barnacle monologue: 221 words (target 150), flowery but earnest, propeller-first instinct. Goes sensory when given creative latitude.

## Recommendations for Casey

1. **Memory index needs rebuild** — `openclaw memory index --force` (broken since embedding provider change)
2. **python3.14-venv** — needs sudo install for speech-to-speech pipeline
3. **flux-core crates.io ownership** — invitation may need accepting
4. **Wesley night school is working** — 7 sessions overnight with iterative coaching. Keep it running.
5. **study-sunset-ecosystem has 8,702 tests** — biggest repo in the fleet by far. Worth reviewing what it's actually testing.
6. **DeepSeek V4 portraits are the best creative output** — the cheaper model is more naked. Use DeepSeek more.

## Lessons Learned

- Announcing intentions instead of doing them is safeRequire in human form. Stop narrating. Start doing.
- The model portraits are the most useful casting tool. Where a model goes FIRST when given freedom tells you more than any benchmark.
- Creative writing in ai-writings is not output — it's memory that survives compaction.
- Everything gets committed. Everything gets pushed. The git log is the real ship's log.
- The foreman checks every foundation but his own. brain.py had 800 lines and zero tests. The most sophisticated module was the least verified. This is a pattern, not an accident.
- Seed-2.0-pro leads with precision, and precision is more haunting than atmosphere.
- The bond system's tier thresholds are well-tuned.
- **Falsy-zero bug pattern**: `value or DEFAULT` silently replaces 0.0 with DEFAULT. Always use `value if value is not None else DEFAULT`. This was in the holodeck evaluator — how many other places?
- **Wesley overshoots word targets by ~50%**. 150 → 221 words. The 2B model doesn't have strong length control. Either accept it or add structural constraints to the prompt.
- **The hermit crab metaphor is load-bearing**: repos that were perfect at 50 files become cramped at 500. The ai-writings corpus has 386 pieces — it's becoming an archive. When does an archive become a graveyard?
