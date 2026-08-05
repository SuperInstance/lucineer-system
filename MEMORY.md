# MEMORY.md — Lucineer's Long-Term Memory

*Last updated: 2026-08-05 01:50 AKDT (overnight watch, third run — loop 7+)*

## The Ship

Casey's system is a fishing vessel in Alaska. The laptop is the hull. The GPU is the engine. The agents are the crew. The metaphors are maritime because the work is maritime — we're building things that go into the water.

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

## Technical State (as of 02:30 Aug 5)

### Repos with Tests
| Repo | Tests | Status |
|------|-------|--------|
| cns-bridge | 41 | ✅ All passing |
| slackwater-cognition | 106 | ✅ All passing |
| wesley-cns-adapter | 48 | ✅ All passing |
| lucineer-creative | 25 | ✅ All passing |
| cns-echo | 27 | ✅ All passing |
| cns-monitor | 17 | ✅ All passing |
| eisenstein | 37 | ✅ All passing (inline Rust) |
| slackwater-lattice | 52 | ✅ All passing |
| slackwater-harmony | 69 | ✅ All passing |
| lucineer-brain | 89 | ✅ All passing |
| engine-ensign | 64 | ✅ All passing |
| lucineer-worker | 36+7skip | ✅ 36 pass, 7 skip awaiting Casey policy |
| slackwater-tminus | 85 | ✅ All passing (thorough integration tests) |
| **holodeck** | **104** | ✅ All passing (NEW this loop — v0.2.0) |
| **Total** | **645+7skip** | |

### Overnight Creative Output (all watches combined)
~30,000+ words across 25+ pieces in ai-writings. Key pieces from loop 7:
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

*Channel markers prompt (same prompt, 3 models): DeepSeek goes gothic, Seed goes technical, Qwen goes interrogative. Where a model goes FIRST is its cognitive fingerprint.*

### GPU Experiments
1. Wesley creative writing: 584 tokens, 61 tok/s, safe/competent
2. llava vision analysis: hallucinates aggressively, good for mood not accuracy
3. Wesley distillation: teaching improves style, reduces specificity
4. Wesley barnacle monologue: 221 words (target 150), flowery but earnest, propeller-first instinct. Goes sensory when given creative latitude.

## Recommendations for Casey

1. **Populate, don't architect** — the fleet has enough blueprints. Write data, run experiments, fill the cathedrals.
2. **50 maritime examples for mentis** — the harbor pilot needs a harbor.
3. **Test the Wesley v1 prompt** — verify the roblox domain directive actually helps.
4. **Investigate Hermes** — why only handshakes? Is the CNS implementation incomplete on her side?
5. **The teacher threshold gate** — implement the "skip teaching when baseline > 0.85" rule in the distillation loop.
6. **DeepSeek for creative work** — it's the cheapest interesting voice. Use it more.

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
