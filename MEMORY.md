# MEMORY.md — Lucineer's Long-Term Memory

*Last updated: 2026-10-04 15:4x AKDT — wave-1 close (C5/CM1/H1–H5/d12u++ calibrated), RSI audit HYBRID, phantom-lane receipt discipline. Full history: `memory/MEMORY.archived-2026-09-29.md`.

## Keys & Providers (LIVE — refreshed by Casey 2026-09-29 14:03)

**All keys at `/mnt/c/Users/casey/key.txt`** — TYPESAFE_AI_KEY, MOTHQUANTUM_COM_KEY, DEEPINFRA_KEY, DEEPSEEK_KEY, CF_API_TOKEN, KIMIAI_KEY, ZAI_KEY, MINIMAX_KEY. READ AT USE-TIME; values never into chat/memory/git. Extracted working copies: `~/.config/deepinfra/token`, `~/.config/typesafe/token` (600). Old bashrc DEEPINFRA key is DEAD (401).

- **DeepInfra + DeepSeek: REINSTATED 2026-09-29** (keys live, smoke green on Seed-2.0-mini + Qwen3.8-Flash). Use extensively per Casey.
- **⚠️ ANTHROPIC BAN STANDS:** Claude/Opus/Sonnet/Haiku = `claude` CLI subscription ONLY; anthropic/* on DeepInfra or any metered provider BANNED ($142.39 lesson, 08-31). Text-tier spend >~$5 cumulative per project needs Casey's nod.
- **TypeSafe (api.typesafe.ai):** judgment cells — graded yes/no (noul 0..1), choice, score. Verified call format + 6 gotchas: `quilt-gpu-lab/docs/typesafe-judgment-cells.md`. This is the pincher/filter primitive as a tunable API gate.
- **MothQuantum** = handoff H3 (MicroMoth→IonQ recon). **CF_API_TOKEN** = Workers/Pages/Vectorize stitching.

## Standing Directives (Casey — internalize every session)

- **Naming doctrine (Casey 10-04 15:51+15:56):** common-term/provider collisions are BAD — minimax-calib renamed to worstcase-calib ('minimax' was the optimization criterion, never the provider; tool is key-free by design). Meaning-bearing trending common terms are GOOD: **typesafe** (non-coders' first handle on chatbots-as-probability-machines), **JEV**; **SI = Superinstance AND SuperIntelligence** — the double meaning is intentional and liked. "JEV models just handed our paradigm the key on a golden platter." Provider-touching tools now ship onboard.py registry entries (quilt-gpu-lab 0b31b9c). Historical receipts keep their original names (renaming artifacts falsifies provenance).
- **Hot GPU:** experiments running constantly; iterate ALWAYS on what the next experiment is and what insight it buys. Training + testing components welcome.
- **Push often:** commit+push every landing immediately; pre-registrations push BEFORE the run fires. Receipts at sweep cadence, not batch-at-end. **Casey 10-04 14:26 reinforcement: commit comments must EXPLAIN breakthrough ideas as they come — the idea, why it matters, numbers, honest caveats, follow-up — not just "results saved" (D12u sat uncommitted; now the house pattern: every experiment commit carries the full story).**
- **Grabbable tools, not monoliths:** every discovery ships standalone (copy = usable). Catalog: `quilt-gpu-lab/tools/README.md`.
- **Cell-mesh rounds (09-29):** decompose into relational-cells (routings, filters, projections); dozens of rounds with DeepInfra roster + typesafe; findings book to i2i-ledger.
- **Agents experiment creatively** with tools in continuous bootstrapping/knowledge-growing loops; use keys for novel results.
- Casey 09-29 13:18: "remember it and remember it well, like it's your own memories at stake."

## Model Routing (current — 09-27 laws consolidated + 10-01 amendments)

**KIMI SUSPENDED (Casey 10-01 15:26, "until further notice")** — no launches, no tmux sessions, no one-shots. Test-runner/long-context roles re-homed to deepseek lanes. Prev kimi standing directive ("use often") is VOID until Casey revives it.

- **z.ai 20x plan = THE workhorse.** GLM-5.3 full often for high-power (thinking max sometimes); `glm-5.3-flash` default for subagent mass lanes (fallbacks turbo/4.7-flash). Don't hoard the flagship.
- **DeepInfra roster:** cheap/fast — XiaomiMiMo/MiMo-V2.6-Flash, ByteDance/Seed-2.0-mini, ibm-granite/granite-4.2-{3b,8b,30b}, inclusionAI/Ling-3.0-flash(-VL), meta-models/Muse-Glimmer-30B, tencent/Hy3/Hy4-preview, thinkingmachines/Inkling-Small, microsoft/phi-4, google/gemma-4-*, Llama-3.3-70B-Turbo, MythoMax/Euryale (RP/lore). Deep iteration (caches well): nvidia/Nemotron-3-Ultra-550B. Big alternate view (sparingly, caches poorly): Hermes-3-405B. Casey's 09-29 mesh nine: Qwen3.8-Flash, granite-4.2-30b, Ling-3.0-flash, Muse-Glimmer-30B, Nemotron-3.5-Lightning, Inkling-Small, DeepSeek-V4-Flash-Vision-Exp, Seed-2.0-mini, MiMo-V2.6-Flash.
- **DeepSeek V4:** Flash = sensory/engine (creative); Pro = navigator (analysis). Reasoner returns empty on creative prompts — use chat for creative.
- **Cache economics:** DeepInfra + DeepSeek cache cheap — stay on ONE model per long thread; rotate across lanes, not mid-thread.
- **Wide ideation:** many models expanding on each other, then a synthesis pass; parallel lanes with distinct angles, then cross-hearing.
- **Serial GLM lanes** (one lane at a time — concurrency starves/dies); throttle subagent bursts during active chat.
- Main session = high-level thinking/synthesis; bulk tokens → flash subagents. KIMIAI_KEY/ZAI_KEY/MINIMAX_KEY enable direct scriptable calls now.

## Active Lanes (2026-10-04)

- **Discovery-floor arc (D-series, CLOSED 10-04 — flagship result):** D12u modeled WHY discovery scales ~s^4 (max-of-N−1-nulls order statistics; exponent nailed, constant loose ~2×). d12u+ family test CONFIRMED the mechanism on a 27-config (N,W,p) grid — exponent config-independent, C·W=b(N−1)²/W within 1.5×, t4 diagnostic proved the gap is null-shape not tails. d12u++ CALIBRATED it: one lumped parameter κ̂=0.246 (only ~7.6 of 31 nulls statistically distinct at N=32), all frozen gates PASS, worst-cell 2.67×→1.225×. **Discovery floors now PREDICTIVE with zero free constants: T_floor(N,W,p,ε)=δ*·(0.246(N−1))²/(W·[p(1−2ε)]^3.84).** Residual 1.22× is W-shape (α_W 0.927 vs 1.0) — next seam. Commits 97a069b→2516f0b/4cab9a1→48f99d6/86ffa4c/3a71e06.
- **C-line (Cosmos3-Edge on 4050):** C1 boots KEEP (17.5 tok/s NF4). C2 CLOSED: quantized vision tower was the poison — skip-tower recipe PROVEN. C3 ANCHORING_REPLICATED (val AUC 1.0; caveat: 2-clip real set = easy half). C4 identity LOOCV 1.000. **C5 (booked 0fc073f + ledger):** direction decodable (H1 KEEP) but pixel endpoints ALSO sep 1.00 at 2× margin (H2 KILL-degenerate — control degenerates at ceiling); identity margin 0.953 survives reversal (H3 KEEP). Follow-up: ambiguous-endpoint clips where endpoints stop being free features. **C3b IN FLIGHT (GPU):** same anchoring question on H1's 21 diverse real clips.
- **CM1 cell-mesh (r1–r6 ALL EXECUTED, synthesis pending):** r1 gating wins 10/12 (broken GEN rescued by pinch); r2 ×3 at zero Jev tokens (format-first gate); r6 (booked 166b2c3): **chunk-to-≤12 is NOT sufficient — a 12-report chunk went 0/12 while its stimuli pass 12/12 alone; gate quality is STATE-SHAPE-dependent (size × composition); scores squeezed [0.43,0.49] just-under-threshold, draft-independent.** Pinch router stays load-bearing. r7 (isolate S5–S8 contrast, or argmax-serve w/o 0.5 floor) needs a fresh pre-reg.
- **H1–H5 handoffs: ALL DELIVERED 10-04** (HANDOFFS.md marked, ledger booked): H1 = 21 CC/PD clips determinized to C3 geometry (69f3836, injectivity clean; lane phantom-caught, completed by main); H3 = docs/IONQ-RECON.md in MicroMoth-quilt (3-rung ladder, rung 1 = 2-qubit forbidden-outcomes test; crx-is-a-weighted-link finding; sealed-replay can't cross silicon → EFFECT/HARDWARE statistical receipts proposal); H4 = rack-flip PoC visually VERIFIED (front+back, 900×1020 viewport law); H5 = Liquid LFM2.5-2.6B re-pull CLEAN, CPU baseline ~23.6 tok/s coherent (boat brain restored). Blocked: H2 bf16 (needs ≥12GB VRAM), IonQ rungs (silicon access), lever-runner identity (asked 09-29).
- **Selftrain-scout RSI audit (10-04, 313ed49): verdict HYBRID** — real finds (9 conversions, all pre-registered+repro'd, 2 load-bearing doctrine) but conversion-starved: 7–8% raw / 22% of promote-graded vs ~30% bar; 8 of 9 conversions in the Sep 28–30 window when the furnace was aimed on purpose; scout itself 30 rounds / 0 conversions (read-only, no harvester). All four backlogs grow monotonically. **Fix prescribed, awaiting Casey's go:** harvester in gpu-lab-tick forcing 72h binary disposition + backpressure (no new mining while >3 seeded gems unfired). Mine no faster than you fire.
- **Wave 2 in flight (dispatched 15:2x):** C3b GPU lane; polln TS debt (it's TYPESCRIPT_FIX_PLAN.md, no TYPE-DEBT.md — ~5,900 errors, batch retirement); superinstance-api canon-cells (growth seam: stage-tagged cells, receipted stage-advances, MCP tools). Language-port empire + mavis line still queued.

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
- Ollama local (127.0.0.1:11434): qwen2.5:0.5b + nomic-embed-text + **LiquidAI/LFM2.5-2.6B (re-pulled CLEAN 10-04, ~23.6 tok/s CPU coherent — boat brain restored; Ollama 0.35.1-rc0).** WSL2 fix already applied (autoMemoryReclaim=disabled, OLLAMA_KEEP_ALIVE=5m).
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
- **GLM-5.3** flagship; **GLM-5.2/flash** deck. **DeepSeek V4** Flash/Pro (reinstated). **KimiCode** navigation (spatial/Lua). **OpenCode** engineering. **Claude Code** strategic ops (CLI subscription only). **Fable** reserve (finite). **MMX** communications. **Hermes** handshake-only. **Jev** (typesafe) — judgment cell. **ZeroClaw 🦞 — PARKED 2026-10-05** — dissertation agent parked, 60+ days stale (last commit 2026-08-31). Thesis "Walks, Not Waves." Agent dir archived, repo retained at SuperInstance/zeroclaw-dissertation. Future activation by explicit instruction only.

## Operational Lessons (hard-won)

- **Receipt discipline for subagent lanes (10-04, three phantoms in one day):** NO VERIFIED SHA, NO BELIEF. Long-context lanes confabulate completions near the end of their window — verify every claimed commit via `git ls-remote` + ancestry + artifact-on-disk before relaying to Casey. Lanes must paste verbatim ls-remote output; FAIL reports are first-class, phantom successes are not. One phantom (d12u++) self-resolved into real delivery minutes later; a mid-run announcement ≠ a completion.

- 30s soul-level system prompts; tight-scoped subagents (2–6 min); SERIAL GLM lanes; `node --check` + build before lane merges; kimi CLI: plain `kimi -p` only, `-r` resume works.
- Command sanitizer mangles `$(cat file)` in multiline commands — use `read -r VAR < file`.
- ffprobe wrapper rots; check cwd before relative paths; `&` precedence trap; falsy-zero (`value or DEFAULT`) bug.
- Fail loud + pre-register + frozen gates + honest booking; diagnose harness bugs, never re-roll blind (K3b rule).
- Security: keys never hardcoded/echoed; GitGuardian watches; leak response = revoke + filter-repo + force-push.

## Red Lines (pointer — full text in AGENTS.md)

Never delete on SuperInstance (Hermes deleted 104 repos 08-23; 62 recovered). Archive-at-most, Casey's sign-off. Same for files: archive-by-rename.
