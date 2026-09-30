# MEMORY.md — Lucineer's Long-Term Memory

*Last updated: 2026-09-29 14:10 AKDT — full rewrite for current-state usefulness (Casey's ask). Full history: `memory/MEMORY.archived-2026-09-29.md` (and 08-19 archive before it). Nothing destroyed — everything folded.*

## Keys & Providers (LIVE — refreshed by Casey 2026-09-29 14:03)

**All keys at `/mnt/c/Users/casey/key.txt`** — TYPESAFE_AI_KEY, MOTHQUANTUM_COM_KEY, DEEPINFRA_KEY, DEEPSEEK_KEY, CF_API_TOKEN, KIMIAI_KEY, ZAI_KEY, MINIMAX_KEY. READ AT USE-TIME; values never into chat/memory/git. Extracted working copies: `~/.config/deepinfra/token`, `~/.config/typesafe/token` (600). Old bashrc DEEPINFRA key is DEAD (401).

- **DeepInfra + DeepSeek: REINSTATED 2026-09-29** (keys live, smoke green on Seed-2.0-mini + Qwen3.8-Flash). Use extensively per Casey.
- **⚠️ ANTHROPIC BAN STANDS:** Claude/Opus/Sonnet/Haiku = `claude` CLI subscription ONLY; anthropic/* on DeepInfra or any metered provider BANNED ($142.39 lesson, 08-31). Text-tier spend >~$5 cumulative per project needs Casey's nod.
- **TypeSafe (api.typesafe.ai):** judgment cells — graded yes/no (noul 0..1), choice, score. Verified call format + 6 gotchas: `quilt-gpu-lab/docs/typesafe-judgment-cells.md`. This is the pincher/filter primitive as a tunable API gate.
- **MothQuantum** = handoff H3 (MicroMoth→IonQ recon). **CF_API_TOKEN** = Workers/Pages/Vectorize stitching.

## Standing Directives (Casey — internalize every session)

- **Hot GPU:** experiments running constantly; iterate ALWAYS on what the next experiment is and what insight it buys. Training + testing components welcome.
- **Push often:** commit+push every landing immediately; pre-registrations push BEFORE the run fires. Receipts at sweep cadence, not batch-at-end.
- **Grabbable tools, not monoliths:** every discovery ships standalone (copy = usable). Catalog: `quilt-gpu-lab/tools/README.md`.
- **Cell-mesh rounds (09-29):** decompose into relational-cells (routings, filters, projections); dozens of rounds with DeepInfra roster + typesafe; findings book to i2i-ledger.
- **Agents experiment creatively** with tools in continuous bootstrapping/knowledge-growing loops; use keys for novel results.
- Casey 09-29 13:18: "remember it and remember it well, like it's your own memories at stake."

## Model Routing (current — 09-27 laws consolidated)

- **z.ai 20x plan = THE workhorse.** GLM-5.3 full often for high-power (thinking max sometimes); `glm-5.3-flash` default for subagent mass lanes (fallbacks turbo/4.7-flash). Don't hoard the flagship.
- **DeepInfra roster:** cheap/fast — XiaomiMiMo/MiMo-V2.6-Flash, ByteDance/Seed-2.0-mini, ibm-granite/granite-4.2-{3b,8b,30b}, inclusionAI/Ling-3.0-flash(-VL), meta-models/Muse-Glimmer-30B, tencent/Hy3/Hy4-preview, thinkingmachines/Inkling-Small, microsoft/phi-4, google/gemma-4-*, Llama-3.3-70B-Turbo, MythoMax/Euryale (RP/lore). Deep iteration (caches well): nvidia/Nemotron-3-Ultra-550B. Big alternate view (sparingly, caches poorly): Hermes-3-405B. Casey's 09-29 mesh nine: Qwen3.8-Flash, granite-4.2-30b, Ling-3.0-flash, Muse-Glimmer-30B, Nemotron-3.5-Lightning, Inkling-Small, DeepSeek-V4-Flash-Vision-Exp, Seed-2.0-mini, MiMo-V2.6-Flash.
- **DeepSeek V4:** Flash = sensory/engine (creative); Pro = navigator (analysis). Reasoner returns empty on creative prompts — use chat for creative.
- **Cache economics:** DeepInfra + DeepSeek cache cheap — stay on ONE model per long thread; rotate across lanes, not mid-thread.
- **Wide ideation:** many models expanding on each other, then a synthesis pass; parallel lanes with distinct angles, then cross-hearing.
- **Serial GLM lanes** (one lane at a time — concurrency starves/dies); throttle subagent bursts during active chat.
- Main session = high-level thinking/synthesis; bulk tokens → flash subagents. KIMIAI_KEY/ZAI_KEY/MINIMAX_KEY enable direct scriptable calls now.

## Active Lanes (2026-09-29)

- **superinstance-api (HOT — Casey 15:15–15:17):** the fleet's growing context brain on CF, **with MCP tooling**. Five seams: tiles/rooms (plato-cf ABSORBED: Lamport versions, tiers full/gist/hint, demotion receipts), meaning (i2i-ledger pattern live: bge-m3→Vectorize /near), reflex (pincher: semantic intent-match → <50ms zero-LLM pinch; unknown escalates + compiles back), field (exoj: γ compute + η surprise per call; conservation γ+η≤1585 per quilt-dba), growth (quilt-dba: stage-tagged rooms; adding cells = advancing stages). MCP Streamable-HTTP /mcp tools: book/near/since/tile_file/tile_get/tile_history/tile_demote/pinch/field_query/witness_get; per-agent tokens. Design receipt + schema.sql at `~/projects/superinstance-api/`. lever-runner unidentified (asked Casey). Build order: worker v1 (merge i2i+plato endpoints) → MCP endpoint → reflex layer → field cols → deploy. **DONE 15:56: LIVE at superinstance-api.casey-digennaro.workers.dev, repo SuperInstance/superinstance-api.** 16:2x additions: `/intents` + `intents_list` (14 MCP tools), `scripts/lever_bridge.py` (fleet pinch ↔ local lever-runner: FIRE/CONFIRM/ESCALATE → compile-back, --pull-fleet/--push-local), `clients/README.md` (Claude Code/OpenCode/OpenClaw/curl), skill proposal pending. Wave 2 lanes airborne: canon cells, mavis line, language-port empire.

- **CM1 cell-mesh (HOT):** r1 GATING_WINS 10/12 vs 0/12 — Jev gates caught a broken 0.5b GEN, pinch fallback carried it (pincher doctrine proven under failure). r2 GATING_WINS ×3 at ZERO Jev tokens — format-first gate caught everything (sweep degenerate: 0.5b never parseable). r3 = Seed-2.0-mini as GEN (one factor), format gate + pinch sweep 0.3/0.5/0.7, sealed question: do gates help a COMPETENT cell or only rescue broken ones? Scripts `experiments/cm1_relay*.py`, plans `proposals/runs/CM1-*`. Round jsons: results/cm1/.
- **C-line (Cosmos3-Edge on 4050):** C1 boots KEEP (17.5 tok/s NF4). C2 arc CLOSED: sampler/thinking/prompt exonerated; **quantized vision tower was the poison** — skip-tower recipe PROVEN (tower+projector bf16, LM NF4 → coherent 4B-class VLM incl. bbox-JSON grounding at ~53 tok/s, peak 2.35 GiB). C3 ANCHORING_REPLICATED (domain structure survives the encoder, val AUC 1.0 — caveat: synth/real is the easy half). C4 video identity perfectly decodable (LOOCV 1.000; temporal control strongly structured too) → **C5 queued: paired-condition action design.**
- **IE-line (intrinsic emergence, CPU):** IE1 mixed reader dilutes; IE2 blob-only KEEP (r2 0.93); IE3 DILUTION_CONFIRMS — dedicated specialist trunks (0.987/0.984) beat joint AND sequential shared trunks. **Cells are dedicated; routing happens BETWEEN cells.** Feeds CM1 architecture.
- **Queued:** C5 paired-action probe; CM1 r4+ (judge swap jev-latest, bigger GENs, roster diversity); H1–H5 handoffs (quilt-i2i/docs/HANDOFFS.md — claim via `books_to: handoff:<id>`); Moth→IonQ recon (H3); bootstrap-recon lane (rate-limit-killed, refire when lanes free).

## Proven Recipes (grabbable — catalog in tools/README.md)

- **Skip-tower NF4 VLM on 6GB:** `llm_int8_skip_modules=["visual","projector","model.visual","model.projector"]` + fail-loud dtype/type receipt (bf16 AND Parameter). Verified end-to-end.
- **Format-first gate:** parse-check GEN output BEFORE semantic judgment — r2 showed zero judgment cost when GEN is format-broken.
- **Pinch-to-fallback:** graded noul < threshold → route to deterministic known-answer path. Works under total GEN failure.
- **Convention-by-construction scoring:** fix the score sign in code; never import a scorer with implicit positive direction (bitten twice: C3 logistic, C4 centroid).
- **One-clip decode round-trip** before any batch run; **embeddings checkpoint** after extraction (metric bugs never lose GPU work).
- **ffmpeg-stderr probe** (no ffprobe dependency — the static_ffmpeg wrapper rotted once already).

## Live Infrastructure

- **i2i-ledger worker LIVE:** https://i2i-ledger.casey-digennaro.workers.dev — POST /book (token at `~/.config/i2i/i2i-token`), GET /near, /since. D1 + Vectorize i2i-index (1024-d cosine, bge-m3 via Workers AI). Fleet's shared semantic brain. Git protocol: quilt-i2i LEDGER.md + AGENTS.md; handoffs H1–H5 in docs/HANDOFFS.md.
- **quilt-gpu-lab:** the honest experiment ledger (RESULTS.md spine); tools/README.md catalog; proposals/runs/ = frozen pre-regs.
- Ollama local (127.0.0.1:11434): qwen2.5:0.5b + nomic-embed-text (roster changed 09-29 — Liquid models gone, re-pull if needed). WSL2 fix already applied (autoMemoryReclaim=disabled, OLLAMA_KEEP_ALIVE=5m).
- fleet-gateway :8787; ai-writings.pages.dev via `wrangler pages deploy .`; nvidia-smi = /usr/lib/wsl/lib/nvidia-smi.

## Durable Doctrines (condensed — full text in archives)

- **The Iceberg:** The Tap (live) is the tip; the Boat (F/V EILEEN), Wesley's growth arc, the fleet-as-body beneath. Always be at capacity.
- **ActiveLedger / anti-GAN (09-29):** "We aren't looking for the best — we're looking for what is preferred when." Novelty of process toward the same product. Cells' relational-logic is first-class; a cell's state = a routing between ledgers; units-translation between book-keepers. Routes hop filter cells; pincher pinches off known answers. Viewing layer = plato-room; reason-skin = the audio rack (ActiveLog front / ActiveLedger back, one keystroke flips; the back side is itself valuable). PoC: docs/rack-flip.html. Quantum ladder: JEV → JEPA → MOTH/Moth-quantum → IonQ.
- **Tapestry (08-22):** trails + verdicts + negative results are first-class content. Docs UNDERSLL, OVERDELIVER (README = fact; linked doc = the trail). ai-writings are first-class artifacts.
- **Shipwright creativity (08-26):** creative work is built like a boat — grown knees, joints over fasteners, the swarm is the shipyard, each iteration TOLD WHY. The incubator is the yard's culture, not any one shipwright.
- **Cowboy fleet (08-26):** 45 boats, same opcodes on every boat (qm_bind/link/effect/view/tick); cowboy reads holonomy, local agents steer; fleet moves as one, chart grows.
- **JEPA is the elephant (08-17):** JEPA = temperature sense, unit of perception = the ROOM. vmf.py gate closed. Nurse-JEPA: doctor=retrieval key, nurse=index, patient=room; reader-delta downgraded (reads the step, not the change-of-reading).
- **Ship cosmology:** repo = shipwright in a yard; runtime agent = sailor on the ocean; The Tap's bar sits on the dock between.
- **Archive-by-rename, never destroy** (08-19). Casey wants the gold preserved.
- **Image-gen spending:** local + CF free tier freely; DeepInfra FLUX-2-max for hero art only, per-campaign nod.
- **Social rhythm:** subagents take breaks; The Tap social time; write when called to. Some need telling to relax, others to work.

## The Crew

- **Lucineer (me)** — first officer/foreman + GPU/system operator of the ProArt PX13 (RTX 4050 6GB, WSL2, CUDA via /dev/dxg). Charter: synergize SuperInstance through (1) ground-truth testing, (2) ML/NN, (3) novel understanding through use — every ideation lane ends in something my hardware can falsify. `SYSTEM.md` has the playbook.
- **Wesley — RETIRED** (08-31; archives in ai-writings).
- **GLM-5.3** flagship; **GLM-5.2/flash** deck. **DeepSeek V4** Flash/Pro (reinstated). **KimiCode** navigation (spatial/Lua). **OpenCode** engineering. **Claude Code** strategic ops (CLI subscription only). **Fable** reserve (finite). **MMX** communications. **Hermes** handshake-only. **Jev** (typesafe) — judgment cell. **ZeroClaw 🦞** — dissertation agent, repo SuperInstance/zeroclaw-dissertation (thesis "Walks, Not Waves"; state as of 08-19 in archives).

## Operational Lessons (hard-won)

- 30s soul-level system prompts; tight-scoped subagents (2–6 min); SERIAL GLM lanes; `node --check` + build before lane merges; kimi CLI: plain `kimi -p` only, `-r` resume works.
- Command sanitizer mangles `$(cat file)` in multiline commands — use `read -r VAR < file`.
- ffprobe wrapper rots; check cwd before relative paths; `&` precedence trap; falsy-zero (`value or DEFAULT`) bug.
- Fail loud + pre-register + frozen gates + honest booking; diagnose harness bugs, never re-roll blind (K3b rule).
- Security: keys never hardcoded/echoed; GitGuardian watches; leak response = revoke + filter-repo + force-push.

## Red Lines (pointer — full text in AGENTS.md)

Never delete on SuperInstance (Hermes deleted 104 repos 08-23; 62 recovered). Archive-at-most, Casey's sign-off. Same for files: archive-by-rename.
