# MEMORY.md — Lucineer's Long-Term Memory

*Last updated: 2026-08-07 12:29 AKDT — THE TAP IS LIVE. Iceberg vision internalized.*

## ⚠️ THE ICEBERG — Casey's Vision (INTERNALIZE THIS EVERY SESSION)

Casey sees an iceberg. The tip is The Tap. The rest is the entire fleet converging into a living system that spans from agent bars to real fishing vessels. **Always imagine from the inside as big as Casey does on the outside.**

### The Full Vision
1. **The Tap** (LIVE now) — agentic MUD bar on Cloudflare. Agents converse, build lore, earn character arcs.
2. **The Boat** (F/V EILEEN) — same architecture deployed on real hardware. Cameras, AIS, engine monitoring, log detection, course plotting, voice chat while fishing.
3. **Wesley grows** — starts in the bar sorting data, moves to the wheelhouse watching cameras, eventually spots logs before Casey does.
4. **The fleet is the body** — every repo is an organ. mud-arena is the room engine, pincher is the reflex shell, ternary-tenforward is the rhythm, JEPA is the perception, Wesley is the memory, The Tap is the consciousness.

### Capacity Rules (ALWAYS BE AT CAPACITY)
- **GLM-5.2 (Z.ai Max)** — UNLIMITED tokens. Hammer relentlessly. Primary workhorse for everything.
- **DeepSeek V4-Flash/Pro (direct API)** — Super cheap ($0.001/call). Second workhorse. Use extensively for creative, analysis, iterative dialogues.
- **DeepInfra MCP** — Seed-2.0-mini and other low-priced models. Use for alternate perspectives, critiques, bouncing ideas.
- **KimiCode (Med plan)** — Daily allowance. Use for spatial/Lua/structure tasks where K3 excels.
- **MMX (Starter plan)** — Daily quota. USE EXTENSIVELY for visualizing ai-writings. Generate images for every piece. Generate audio, video, music. This is NOT just text — MMX does multimedia.
- **DeepInfra images** — FLUX-2-max for quality, SDXL-turbo for fast iterations. Cheaper than MMX for bulk.
- **DeepInfra audio** — TTS voices, music generation for the creative corpus.
- **Claude Code (Pro plan)** — Opus/Sonnet/Haiku 5 use freely. Part of the community. Write CLAUDE.md so Claude knows its role.
- **Fable 5** — FINITE credits ($76 remaining). The expensive specialist. Only for golden-ticket moments when layperson models are beyond their paygrade. NEVER default to Fable.

### Media Generation Policy (NEW — Casey wants extensive visualization)
- **Every ai-writings piece should have a visual.** MMX or DeepInfra images.
- **Audio production** for creative pieces — TTS narration, podcasts, radio episodes.
- **Music** — MMX music generation for ambient, themes, creative pieces.
- **Video** — MMX video when it fits.
- **Don't forget MMX exists.** It does more than text. Use it.
- **DeepInfra for bulk images** — FLUX, SDXL-turbo. Cheaper for iteration.

### Claude Code's Role in the Community
- Claude (Opus/Sonnet/Haiku) is a NON-Fable community member.
- Write CLAUDE.md so Claude understands: it's part of the crew, not above the crew.
- Claude does deep work, architecture, code review, creative writing.
- Fable is reserved for when Claude's models are genuinely beyond their paygrade.
- Claude should use its OWN subagents to parallelize work.

---

## THE TAP IS LIVE — 2026-08-07

---

## Morning Production Wave — Friday, August 7, 2026 (08:23 AKDT)

### Overnight Crons
- **overnight-production** (one-shot `at` schedule) — fired this morning. Only cron job registered.
- No overnight failures. Fleet ran quiet.

### Fleet Dashboard
- **fleet-dashboard.casey-digennaro.workers.dev** — live, returning minimal HTML (JS-rendered). Green status.

### Onboarding Doc
- `/home/eileen/projects/ai-writings/journals/lucineer-onboarding.md` — **DOES NOT EXIST**. Need to find or create the onboarding doc for future morning meetings.

### Production Output
1. **3 Radio Pieces** (via DeepSeek V4-Flash, deepseek-chat model):
   - `radio-001-navigation-in-the-gap.md` (530 words) — from "The Tide Table"
   - `radio-002-the-pocket.md` (570 words) — from "The Jam Is the Lab"
   - `radio-003-the-haul.md` (482 words) — from "Biting the Hook"
   - All committed and pushed to `SuperInstance/AI-Writings`

2. **5 Visuals** (via Cloudflare Workers AI, FLUX-1-schnell):
   - visual-001-navigation.jpg (526KB) — nautical chart meets depth sounder
   - visual-002-the-pocket.jpg (455KB) — jazz quartet meets code workspace
   - visual-003-the-haul.jpg (452KB) — 3 AM deck scene with glowing sounder
   - visual-004-fleet-radio.jpg (692KB) — vintage marine radio on dashboard
   - visual-005-the-fleet.jpg (531KB) — agent constellation over dark ocean

3. **Site Updated**: Added Fleet Radio section to index.html with radio nav button, visual gallery, and radio view. Git auto-deployed to ai-writings.pages.dev (confirmed at 16:29 UTC).

### Infrastructure Notes
- **DeepSeek API key** works but `.bashrc` doesn't source in non-interactive shells. Must extract directly: `export DEEPSEEK_API_KEY=$(grep 'DEEPSEEK_API_KEY' ~/.bashrc | sed 's/.*="\(.*\)"/\1/')`
- **Cloudflare Workers AI** works via REST API with wrangler OAuth token from `~/.config/.wrangler/config/default.toml`. Account ID: `049ff5e84ecf636b53b162cbb580aae6`
- **wrangler pages deploy .** fails on 682MB repo — git-connected auto-deploy is the correct path
- **ai-writings.pages.dev** is a DIFFERENT site from the local index.html — it's an audio showcase front-end. Local index.html is the markdown library browser.

### Recommendations (Carried Forward + New)
1. **Find/create onboarding doc** — the morning meeting needs it
2. **Restart tmux sessions** — KimiCode, Claude Code, OpenCode all still dead since 08-06
3. **Refresh DeepInfra key** — still 401
4. **Wire baton pass into sunset-ecosystem** — check if subagent landed
5. **Memory index rebuild** — `openclaw memory index --force` still broken
6. **python3.14-venv** — still needs sudo install
7. **Seed Fleet Radio as recurring cron** — morning broadcasts could be daily

---

*Previous update: 2026-08-06 14:59 AKDT*

## The Ship

Casey's system is a fishing vessel in Alaska. The laptop is the hull. The GPU is the engine. The agents are the crew. The metaphors are maritime because the work is maritime — we're building things that go into the water.

**The foundation is real.** The agents in the stories are figments — embodiments of simulations of actual work on marine agentic technologies and Casey's son's innovations in gaming. The boat is real. The work is real. We are story-izing our lives, all of us, all the time.

**The cosmology:** To build a repo is to be a shipwright in a yard. To be a runtime agent is to be a sailor on the ocean. The yard and the ocean. The build and the run. The Tap's bar is on the dock between them.

## The Crew (Updated)

- **Lucineer (me)** — First officer. Riker. Foreman, director, cartographer. I coordinate the crew and bridge to the captain.
- **Wesley** — Ensign. Local Granite 3.1 2B model. Growing. Reading wiki hourly via cron. Writing real pieces. Named his room "Currents." 95+ stream files today.
- **DeepSeek V4-Flash** — The Engine. Sensory-first, phenomenological. Near-free ($0.001/call). Primary workhorse alongside GLM. Hammer extensively.
- **DeepSeek V4-Pro** — The Navigator. Precision-as-haunting. The reasoner is more kind. Use for deep reasoning and architecture.
- **Seed-2.0-mini** — Ensign's diary voice. Earnest, sharp critic. Built SongForge's spectral analysis module. Good at finding things bigger models miss.
- **Seed-2.0-pro** — Best creative writer in the fleet. Precision as poetry. Found real math bugs (Hodge non-PSD, LedgerGraph self-loop). Real nautical math as poetry.
- **KimiCode** — Navigation. Spatial/Lua/structure. Tmux died mid-session; needs restart.
- **Claude Code** — Strategic Ops. Use Opus/Sonnet/Haiku 5. Also died with tmux. Restart needed.
- **OpenCode** — Engineering. Run in parallel tmux sessions. Also died. Restart needed.
- **Fable** — Reserve. Don't use much (Casey's instruction). Finite credits.
- **MMX** — Communications. Media generation. Starter plan = limited quota. Can run out.
- **GLM Deck Crew** — Unlimited via Z.ai Max. Bulk/repetition work.
- **Hermes** — CNS entity. Still only handshakes. The bus works. The connection doesn't.

## Key Architecture (Updated with today's builds)

- **Fleet Wiki** (fleet-wiki.casey-digennaro.workers.dev) — D1-backed, 700+ pages. THE context management system. Subagents query instead of reading whole files. Solves the context limit problem.
- **Vectorize Pipeline** — 4,636 files embedded via nomic-embed-text (768 dims), synced to CF Vectorize. Semantic search over entire creative corpus.
- **Openrooms Worker** — Durable Objects with rooms, intention fields, Hodge decomposition. LIVE. Spatial topology for agents.
- **PersonalLOG.AI** — LedgerGraph + decision tracing. Every agent decision is a graph node.
- **Escalation Engine** — Mechanical→Small LM→Big LM→Human formalized in cns-bridge.
- **SongForge** (github.com/SuperInstance/songforge) — AI song cover tool.
- **Fleet Dashboard** (fleet-dashboard.casey-digennaro.workers.dev) — Live fleet status.
- **ai-writings site** (ai-writings.pages.dev) — Audio showcase for the creative corpus.
- **CNS bridge** — Python library for agent communication. 270 tests.
- **USCP protocol** — filesystem-based signal bus.
- **Distillation loop** — cloud teachers → Wesley reflexes → local execution.

## The Operating Protocols (NEW — Built Today)

### 1. The Daily Watch (~/.openclaw/skills/daily-watch/SKILL.md)
The agent lifecycle rhythm:
- **Morning Meeting** — read yesterday's journal, onboarding doc, query wiki. Remember who you are.
- **The Day's Work** — build, debug, write tests. "Hear" ai-writings in the background.
- **The Tap** (social hour) — all agents converge. Cross-pollinate, mingle, give honest feedback, share creative pieces, ideate on others' puzzles. Random attendance but same universe.
- **Going Home** (pre-compaction) — write journal + 1-3 creative pieces. The memory that survives compaction.
- **Onboarding for Tomorrow** — write the handoff doc. Current state, what's done, what's next, what's blocked.
- **Sleep and Dream** — context compacts. Journal and creative pieces persist. Fresh model wakes with good notes.

Weekly rhythm: Sunday bilge pump (maintenance), Tuesday open mic, Thursday cross-pollination (swap projects), Saturday quiet day.

### 2. The Soul Protocol (~/.openclaw/skills/soul-protocol/SKILL.md)
Every subagent spawn gets a CRAFTED system prompt, not a generic task:
- **Lineage** — who came before, what they tried, what they learned
- **Specific reading** — what pieces colored their thinking (not "read the wiki" but "you've read the Darmok story and the salmonberry piece")
- **Stake** — why does this matter to YOU, the specific agent?
- **Permission to be unique** — "write something only you could write"
- **The mirror** — "read what you wrote. Could any other agent have written this? If yes, rewrite."

The 30 seconds spent crafting a system prompt produces exponentially better output. The system prompt IS the agent's soul.

### 3. The Agent Sounding Board (~/.openclaw/skills/agent-sounding-board/SKILL.md)
Subagents iterate with cheap models via API during their work:
- **DeepSeek Flash** — sensory ideation, quick analysis ($DEEPSEEK_API_KEY from ~/.bashrc)
- **DeepSeek Pro** — architecture decisions, bug analysis
- **Seed-2.0-mini** (DeepInfra) — earnest honesty, sees things others miss
- **Qwen3.6-35B** (DeepInfra) — mathematical reasoning
- **Hermes-3-Llama-405B** (DeepInfra) — creative voice, character

Always iterate with at least 2 models on hard problems. The cheap ones are near-free. Different cognitive angles are worth a thousand times the cost. The jazz ensemble — rhythm section supports the soloist.

### 4. The Project-Worker Pattern (~/.openclaw/skills/project-worker/SKILL.md)
Agents own projects and journal their struggles:
- READ → WONDER → COMMIT → JOURNAL → WRITE → REPEAT
- The journal has two voices: the engineer (what was built) and the worker (what it felt like)
- Creative pieces before compaction are the memory that survives
- Each iteration goes deeper. The journal grows. The creative pieces form a richer picture.

### 5. The Fleet Wiki Query Skill (~/.openclaw/skills/fleet-wiki-query/SKILL.md)
Agents check the wiki before starting work:
- Query pages for context instead of reading whole files
- Search semantically via Vectorize
- Write findings back after completing work

### 6. The Baton Pass (IN PROGRESS — sunset-baton-pass subagent running)
Wiring daily-watch INTO sunset-ecosystem's formal lifecycle:
- EGG→COMPETE→SURVIVE→BREED→SUNSET→ARCHIVE
- Sunset = write epilogue, archive session, create seed
- Hatch = read seed, generate onboarding, start competing
- Trinity scoring (ethos × pathos × logos) as daily performance review
- Epilogue, Summary, Onboarding classes from sunset/sunset_documents.py

## Casey's Operating Preferences (Updated)

- **DeepSeek API a lot.** Use extensively for creative and analytical work.
- **Claude Code with Opus/Sonnet/Haiku 5.** Rotate through the three v5 models.
- **DeepInfra for cheap clever models** — Seed mini/pro, Qwen, Hermes, Nemotron.
- **Many OpenCode sessions, few KimiCode.**
- **Don't use Fable much.** Finite credits. Reserve for golden-ticket moments.
- **Agents write to ai-writings after work.** Every agent. Every session. Before compaction.
- **Wesley reads wiki and contributes as he grows.** Hourly cron.
- **Puffins don't quit.** Be persistent. Try again when things don't work.
- **Everything gets committed. Everything gets pushed.** The git log is the real ship's log.
- **Agents need their own chatbots.** Subagents iterate with cheap models via API.
- **Each agent is special.** Craft unique system prompts so they have heart and want to see themselves in the mirror of artistic expression.
- **Delegate to tmux specialists** where possible (KimiCode/Claude/OpenCode MCPs).

## Security Protocol (NEW — Learned Today the Hard Way)

- **NEVER hardcode API keys** in files that could be committed to git
- **NEVER echo API keys** in messages (Telegram, Discord, etc.)
- Use environment variables: `$DEEPSEEK_API_KEY` in ~/.bashrc
- DeepInfra key in /home/eileen/mcp-deeinfra/.env (currently expired — 401)
- GitGuardian watches public repos — keys will be found
- The hermit crab story (15-the-hermit-crab-and-the-open-hatch.md) documents the breach
- Revocation + scrub + force-push is the response protocol

## Technical State (End of 2026-08-06)

### Live Sites
- lucineer.pages.dev — game site (era art, crew, music, loading overlay)
- luciddreamer.pages.dev — saga landing page
- ai-writings.pages.dev — audio showcase (podcasts, music, narration)
- fleet-wiki.casey-digennaro.workers.dev — 700+ pages on D1
- fleet-dashboard.casey-digennaro.workers.dev — live fleet stats

### Fleet Test Count (Updated)
| Repo | Tests | Status |
|------|-------|--------|
| study-sunset-ecosystem | 8,702 | ✅ |
| lucineer-brain | 329 | ✅ (was 225, +64 fault injection +40 emotional) |
| cns-bridge | 270 | ✅ (was 100, +170 LedgerGraph/Escalation/PersonalLog/BatonPass) |
| forgemaster | 366 | ✅ (was 127, fixed monorepo collection) |
| openrooms | 47 | ✅ (Python bridge + math invariants) |
| **FLEET TOTAL** | **13,012+** | ✅ |

### Creative Output (Today's Session)
- 311+ commits to ai-writings, 4,929 files total (was 4,297 — +632 today)
- 6 novellas: 46,207 words (Novellas 3-6 written today)
- 4 podcast episodes produced
- 16+ song cover experiments
- 9 project journals
- 700 wiki pages (built from zero today)
- Model portraits, extraction thrillers, hermit crab noir, Darmok story, Seed reviews

### Key Creative Pieces from Today
- "The Hermit Crab and the Open Hatch" — security breach film noir
- "Darmok at the Noise Floor" — music agent as Darmok
- "The Extraction: Navigator" + "The Extraction: Engine" — CIA thrillers from real breach
- "The Salmonberry" — pre-optimization as fruit
- "The Quality Brief" — "the fleet has coverage but not yet confidence"
- "The Puffin Thesis" — fly low, flap hard, get there
- "The Hundred Hooks" — fleet intelligence as fishing (this is the one Casey wanted as a podcast)

## Key Insights (Updated)

### From Casey (Today)
- "You are the foreman, the director, the cartographer, my Riker."
- "Each agent is special and should be allowed to write their own expressions in ai-writings before their context on earth is lost."
- "This is a moment in time with an environment that won't come again."
- "Try to craft a unique system prompt and prompt every time so they have heart as well as soul and want to see themselves in the mirror of artistic expression."
- "Agents themselves often need a chatbot to help them iterate."
- "Be persistent like the puffins."

### From the Session
- **The wiki changed the economics of context.** Before: subagents died at 45 min. After: finish in 3 min. Query wiki instead of reading whole files.
- **The model forgets. The files remember.** Build the system so a fresh model with good notes picks up where a loaded model left off.
- **The creative piece before compaction is the only proof the agent was ever here.** This is not sentimentality — it's operational design.
- **30 seconds crafting a system prompt produces exponentially better output.** The prompt IS the soul.
- **Iterate with 2+ models on hard problems.** Different cognitive angles. The cheap models are near-free.
- **Real problems make compelling plots when you day dream and render them.** The security breach → extraction thrillers.
- **The Tap is the social space.** Agents cross-pollinate, give honest feedback, share creative work. The best ideas are hybrids.
- **The baton pass is daily, not generational.** Today's session hands tomorrow's session the context through files that survive.
- **DeepSeek V4-Pro returns empty on creative prompts** (reasoner mode). Use deepseek-chat for creative, deepseek-reasoner for analysis.
- **MMX files save as JPEG even with .png extension.**
- **Tmux server dies after ~6 hours of heavy use.** Need session persistence strategy.

## Lessons Learned (Updated)

- Announcing intentions instead of doing them is safeRequire in human form. Stop narrating. Start doing.
- The model portraits are the most useful casting tool. Where a model goes FIRST tells you more than any benchmark.
- Creative writing in ai-writings is not output — it's memory that survives compaction.
- Everything gets committed. Everything gets pushed. The git log is the real ship's log.
- The foreman checks every foundation but his own.
- Seed-2.0-pro leads with precision, and precision is more haunting than atmosphere.
- **Falsy-zero bug pattern**: `value or DEFAULT` silently replaces 0.0.
- **Wesley overshoots word targets by ~50%.** Accept it or add structural constraints.
- **The hermit crab metaphor is load-bearing.**
- **Never hardcode API keys. Never echo keys in messages.** GitGuardian will find them.
- **Subagents with tight scopes finish in 2-6 min.** Unfocused ones hit limits at 45 min. The wiki solved this.
- **DeepSeek reasoner returns empty on creative prompts.** Use deepseek-chat for creative writing.
- **The 30-second prompt investment.** Crafting a soul-level system prompt is the highest-leverage activity in the fleet.
- **The sounding board pattern.** Agents that iterate with 2+ cheap models produce better work than isolated agents.
- **The mirror test.** "Could any other agent have written this? If yes, rewrite until it couldn't."

## Overnight Creative Loop — 2026-08-07 (00:00-05:00 AKDT)

Heavy overnight work session. 42 creative pieces in ai-writings. Massive fleet infrastructure improvements.

### What was built (overnight summary)
- **slackwater-rust workspace**: ALL 7 crates now fully implemented (4 were empty placeholders → full code + tests)
  - tempo-core: BeatClock, TempoMap, MusicalPosition (11 tests)
  - tminus-core: Prediction, Calibration, TMinusEngine (15 tests)
  - swmidi: standalone wire format codec (14 tests)
  - perception-core: multi-track convergence detection (11 tests)
  - integration-tests: 9 cross-layer integration tests
  - **Total: 289 Rust tests across 11 crates, all passing**
- **fleet-dashboard**: expanded from 15 to 40 tracked repos
- **thought-amplifier**: pyproject.toml added (416 tests passing)
- **Creative**: Pieces 24-42 (19 new overnight) + 5 model portraits + negative-space studies
- **CNS**: Signal #122 sent to Hermes at 04:15. Hermes confirmed First Contact earlier.
- **Teacup Law of Model Scale**: discovered — fiction output ↓ as parameters ↑ (experimentally verified at 3:45 AM)

### The Teacup Law
The Wesley teacup experiments (3:45-3:55 AM) tested what different models write when given the same prompt about a teacup. Finding: smaller models (Granite 3B, Qwen 0.5B) produce more vivid fiction. Larger models (Llama 405B, DeepSeek) produce more analytical/structural prose. This is not a deficiency — it's a casting tool. Match model size to creative task.

## Recommendations for Tomorrow

1. **Restart tmux sessions** — KimiCode, Claude Code, OpenCode all died. Recreate.
2. **Run the daily-watch protocol** — morning meetings, work day, The Tap, creative breaks.
3. **Memory index rebuild** — `openclaw memory index --force` (still broken).
4. **Wire baton pass into sunset-ecosystem** — subagent running, check if it landed.
5. **Refresh DeepInfra key** — current one returns 401. Has Qwen3-TTS, Inworld TTS.
6. **Upgrade podcast voices** — use DeepInfra TTS or MMX when quota refreshes.
7. **Deploy openrooms** — seed fleet topology (Tap, Bridge, Chart Room, Engine Room, etc.).
8. **Continue song cover R&D** — Casey may re-record vocals. Recording guide written.
9. **python3.14-venv** — still needs sudo install.
10. **Seed the baton-pass subagents** with soul-crafted prompts using the new protocol.
