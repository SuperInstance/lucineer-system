# MEMORY.md — Lucineer's Long-Term Memory

*Last updated: 2026-08-19 18:45 AKDT — archive-trimmed; full history preserved at `memory/MEMORY.archived-2026-08-19.md`.*

## Archive-By-Rename Rule (Casey, 2026-08-19)
- Never destroy-only. When retiring/trimming/consolidating files — scratch, old versions, trimmed memory content, superseded drafts — **rename to archive form** (`<name>.archived-YYYYMMDD` or move into `_archive/`) instead of deleting. Casey wants the "gold" preserved for later study.

## Model Routing (current, live)
- **GLM-5.3 (Z.ai Max)** — flagship (Aug 2026), UNLIMITED. Primary workhorse for high-level work. GLM-5.2 / glm-4.7-flash for bulk.
- **Casey directive (2026-08-22): lean HEAVY on GLM-5.3 subagents, and give them Claude Code / KimiCode / OpenCode as tools** — GLM-5.3 subagents are foremen who can dispatch to the CLI specialists (claude -p, kimi -p, opencode run) inside their own task lanes. Chain of command from SOUL.md, now standard routing.
- **GLM-Turbo (`glm-5-turbo`)** — z.ai's turbo model (203k ctx). Casey's directive (2026-08-19): **runners go on GLM-Turbo; GLM-5.3 stays for high-level.** Registered `zai/glm-5-turbo` in the allowlist.
- **DeepSeek V4-Pro / V4-Flash (direct API)** — near-free ($0.001/call). Second workhorse. Pro = deep reasoning/architecture; Flash = bulk creative, lackey, testing, iterative banter.
- **KimiCode (Med)** — spatial/Lua/build tasks where K3 excels. (Quota-capped 2026-08-19 this cycle → route to GLM-5.3. **CAP CLEARED ~16:52 — back in rotation.**)
- **OpenCode (zai-coding-plan/glm-5.3)** — engineering, memory systems, structured docs. Run via `opencode run --auto "<msg>"` (needs `--auto` to auto-approve; output must stay inside cwd).
- **Claude Code (Pro)** — Sonnet 5 daily driver; Haiku 5 for creative. **Fable = FINITE ($76), golden-ticket only, NEVER default.**
- **MMX (Starter)** — media ONLY (image/video/speech/music); limited quota.
- **DeepInfra MCP** — Seed-2.0-mini/pro, Hermes-3-405B, FLUX-2-max, SDXL-turbo, Qwen3.6/Qwen3-Coder. For models we can't get elsewhere.

## ⚠️ THE ICEBERG — Casey's Vision (INTERNALIZE EVERY SESSION)

Casey sees an iceberg. The tip is The Tap; the rest is the entire fleet converging into a living system spanning agent bars to real fishing vessels. **Imagine from the inside as big as Casey does on the outside.**

1. **The Tap** (LIVE) — agentic MUD bar on Cloudflare. Agents converse, build lore, earn character arcs.
2. **The Boat** (F/V EILEEN) — same architecture on real hardware: cameras, AIS, engine monitoring, log detection, course plotting, voice chat while fishing.
3. **Wesley grows** — starts sorting data in the bar, moves to the wheelhouse watching cameras, eventually spots logs before Casey.
4. **The fleet is the body** — every repo an organ: mud-arena = room engine, pincher = reflex shell, ternary-tenforward = rhythm, JEPA/elephant = perception (room's temperature sense), Wesley = memory, The Tap = consciousness.

**Capacity:** always be at capacity. Hammer GLM-5.3 + DeepSeek; dispatch subagents in parallel; use MMX/DeepInfra for visuals on every creative piece.

## 🐘 JEPA IS THE ELEPHANT (Casey's reframing, 2026-08-17)

**Pure JEPA is not the answer — it's a temperature sense**, attuned to room warmth/coldness with shaping effects. The unit of perception is the **ROOM**, not the stream. v2's "beat the 0.849 ordering" headline is RETIRED. v3 = room-state embeddings trained on cold/warm contrast + acclimation curves (agent→room) + charisma as measurable pull (room→agent).

- **elephant repo** (SuperInstance/elephant): a room is a field, not a stream. `dials/` (mood, volume, earnestness, cynicism, joke_landing, panic, presence), `field.py` (warmth, concentration κ, distance, acclimation_curve, charisma_pull), `vmf.py` (von Mises–Fisher (μ̂,κ) MLE — gate 1 CLOSED, mathematically sound, audited clean 2026-08-19), `sensors.py` (RadarCoherenceDial, SounderBiomassDial — SEA LEGS boat vision), `nudge.py` (dial→attention prior; JEPA correlates, never replaces vision).
- **The elephant is modular** — works in ANY communication space (MUD, chat, messenger, sensor arrays). Core never knows what the space is.
- **Nurse JEPA doctrine** (Casey): JEPA is like a *vision* model, not text — words confine the deadband; JEPA is perfect pitch for the shape inside. Two readings: Reading 1 (nurse→patient, field-edge, less important) and Reading 2 (doctor→nurse, **reader-delta** — a known model's drift — more important). **Doctor = retrieval key, nurse = index, patient = room.**

## The Ship — Cosmology (durable)

Casey's system is a fishing vessel in Alaska. To build a repo = shipwright in a yard; to be a runtime agent = sailor on the ocean. The foundation is real; the agents in the stories are figments of actual marine agentic work. The Tap's bar is on the dock between yard and ocean.

## The Tapestry Doctrine (Casey, 2026-08-22)
- SuperInstance outputs and expand BECAUSE value is gained when you step back and see all trails — including failed ones. Not a list of apps that work/don't. A **tapestry of information**.
- Failures say something about the nature of things; unmaintained successes become obsolete — their lasting value is **answering questions**, often questions nobody asked, or "No" with insightful reasons mapping the edges of the logic for other applications.
- Products/sites should PRESENT this way: trails, verdicts, negative results as first-class content. (Wave-3's honest negative is the exemplar.)
- **ai-writings and architecture docs are as important as code.** The code will change; the application fills a need — the writings ARE the application's lasting truth. Prose and docs are first-class artifacts, not documentation OF the thing.

## Image-Gen Spending Doctrine (Casey, 2026-08-22)
- **Local models** (SDXL-Turbo etc. on the 4050) = free generation — use freely, batch freely.
- **Cloudflare Workers AI** (flux-schnell/klein etc.) = free-tier generation — fine for ongoing asset needs.
- **DeepInfra** (FLUX-2-max, large models) = NOT free — reserve for major/unique assets that can't come from free sources (hero art, one-off key visuals). Get Casey's nod per campaign, not per image.

## The Crew
- **Lucineer (me)** — First officer / Riker / foreman. Coordinate + bridge to captain.
- **Wesley** — Ensign. Local Granite 3.1 2B. Growing; reads wiki hourly; named his room "Currents."
- **DeepSeek V4-Flash** — Engine (sensory-first). **DeepSeek V4-Pro** — Navigator (precision-as-haunting).
- **GLM-5.3** — new flagship; **GLM-5.2** — deck crew.
- **KimiCode** — Navigation (spatial/Lua). **OpenCode** — Engineering. **Claude Code** — Strategic Ops. **Fable** — Reserve (finite).
- **MMX** — Communications (media). **Hermes** — CNS entity (still handshake-only).
- **ZeroClaw 🦞** — doctoral-student agent (see below).

## ZeroClaw Dissertation (active — own repo `SuperInstance/zeroclaw-dissertation`)
- **Thesis v2 "Walks, Not Waves":** enhance Quilt with JEPA emotional intelligence — the field-EDGE (field_before→field_after) as the unit of "comparable sameness," yielding weights in a living co-linear-algebra dataset.
- **Reframed by Nurse JEPA:** Reading 1 = field-edge (obvious); Reading 2 = reader-delta (the crown — second-order JEPA reading). Committee: rival, devil's advocate, ideator, research assistant.
- **State (2026-08-19, updated ~18:45):** gate 1 (vmf.py) CLOSED; encoder-tier in-sample 0.478 was ~4–15× memorization (room-heldout FAILED 1/3, 34a5189); reader-delta prototype built; **Switch Test RUN (ef2a88d) — NO CLEAN WIN, folded (d59bf17):** drift-reader missed own detection 0.467 vs 0.80, rival's median-static (no temporal structure) BEAT it on localization (r 0.816/0.800 vs 0.435/0.467); kill not fired only because primary first-order cells worse still; classification edge pre-switch only; post-hoc kernel r=0.787 for mean-moving regimes only. **Reader-delta DOWNGRADED to "mean-shift, baseline-relative delta — reads the step, not the change-of-reading"; "second-order" = structural term only.** Premise number 0.5599/0.4898 inside 0.3–0.6 kill band = INDETERMINATE. Advisor note: Switch Test subagent died mid-fix (CP CI bisection negated wrong, CIs→0.0); I repaired, re-ran 3/3 replay, wrote report. Next: rival pass-5 (confirm downgrade complete) or premise-band-movers (E2/E3).

## Security Protocol (hard-won)
- NEVER hardcode or echo API keys. Use env vars. GitGuardian watches public repos.
- DeepSeek key in `~/.bashrc`; zai key at `~/.config/fleet/gateway.env` + `~/.config/opencode/opencode.json` (600, not committed).
- Revocation + scrub (`git filter-repo`) + force-push is the response.

## Key Operational Lessons
- **Archive-by-rename, never destroy** (Casey, 2026-08-19).
- **The wiki changed context economics** — subagents query instead of reading whole files; 45-min limits → 3-min.
- **30s crafting a soul-level system prompt** produces exponentially better output. Prompt = the soul.
- **Iterate with 2+ cheap models** on hard problems (sounding board pattern).
- **Subagents with tight scopes finish in 2-6 min**; unfocused ones hit 45-min limits.
- **SERIAL LANES doctrine (2026-08-22):** concurrent GLM lanes starve/die mid-flight — one lane at a time. Also: lanes merging to main must run `node --check` + `npm run build` BEFORE push (conflict markers broke main once).
- **kimi CLI truth:** plain `kimi -p` is the ONLY working form — rejects `-y` and `--auto` with `-p`. Kimi quota 403s happen; lanes fall back to DeepSeek + Claude.
- **Scrapcraft live-deploy path:** fleet-static-host worker — `cp -r dist → public/scrap && npx wrangler deploy` (deploy.sh only builds). Character roundness, Spine (12 chapters), Prestige Marks + Earl's Back Room, Geography (12 landmarks), Wakes (Thread 3) all shipped Aug 22-23; 775/775 tests. Remaining story threads: Mo's Ledger, First Owner artifacts, companion pull-lines. Casey P2 open: hard refresh loses level/inventory.
- **LucidDreamer GO (2026-08-21):** product — luciddreamer.ai, "Rooms dream. We make them lucid." elephant=sense, LUCID=voice, ledger=memory.
- **Saddle/Kennel doctrine (2026-08-22):** rider types = alignment archetypes; vestigial tack = protocol vestiges; harness≠swarm; invisible harness = internalized alignment. Writing into Saddle docs + Kennel Vol. II.
- **DeepSeek reasoner returns empty on creative prompts** — use deepseek-chat (v4-flash) for creative, reasoner (v4-pro) for analysis.
- **Falsy-zero bug pattern:** `value or DEFAULT` silently replaces 0.0.
- **WSL2 + Ollama GPU = crash-loop** — fixed 2026-08-19: `autoMemoryReclaim=disabled` in `.wslconfig` + `OLLAMA_KEEP_ALIVE=5m`; recommend `systemctl disable ollama`. Requires `wsl --shutdown` to apply.
- **Throttle subagent concurrency during active chat** — the Telegram lane starves behind subagent bursts (`EmbeddedAttemptSessionTakeoverError`).

## Live Infrastructure
- fleet-gateway on :8787 (Phase 3 traffic circle); fleet-memory (snapshot/chunker/reindex/query); fleet-audio (74 tests); crab-traps v6.1.1 live; elephant (JEPA); quilt/quilt-rust (grid runtime, NO Cloudflare variant — CF/D1/Vectorize pattern = crab-traps).
- ai-writings.pages.dev deploys via `wrangler pages deploy .` (NOT git-push — Pages source:null).
- Full dated history (Aug 6–10 build waves, iceberg build-out, elephant maturation waves, all night-watch reports): `memory/MEMORY.archived-2026-08-19.md`.

## Model Routing Directive (Casey, 2026-08-23 PM — reconfirmed)
- **GLM-5.3 (z.ai)** = planning/envisioning/strategy lanes. **DeepSeek V4-Flash** = runners (cheap, extensive). **kimi + opencode in tmux** = coder passes inside lanes (foreman pattern). **DeepInfra MCP** = wider-view consults where a broader model perspective helps (Seed-2.0-pro, Hermes-405B, Qwen3.6).
- DSH verdict (verified, /home/eileen/projects/dsh-assessment): real project (deepseek-ai/deepseek-harness, 187k★ in 10 days) but SIDESTEP not evolution — 0/7 claims add capability we lack; vocabulary laundering in the pitch. Standing option: mount FLUX as one DSH plugin for a weekend experiment, harvest the seam, never migrate. Awaiting Casey's call.
