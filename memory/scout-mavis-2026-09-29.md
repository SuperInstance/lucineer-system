# Scout: MAVIS operational line (SuperInstance wave 2) — 2026-09-29

Shallow-cloned all 15 repos to /tmp/scan2-mavis/. All 15 cloned OK (no 404s). Line is Python-stdlib-heavy; one Cloudflare Worker. Shared DNA: 6 bedrock doctrines, FNV1a-64 polyformalism canary `0x24a555471370b18d`, chord-gated canon (word-set Jaccard ≥ 0.5), JSONL witness logs.

## mavis-pincher — CF Worker A2A knowledge API ⭐
- `src/index.ts` (272 lines TS) + `wrangler.toml` (`[assets] directory=./data binding=ASSETS`; vars PINCHER_VERSION/PINCHER_GENERATED). Live at superinstance.dev/v1.
- Endpoints: `/v1/health` (chain_tip = dataset.generated), `/v1/repos` (family filter; sort pushed_at|name|stars|size; offset/limit max 200), `/v1/repos/:owner/:name`, `/v1/search?q&k≤50`, `/v1/links/:owner/:name`, `/v1/families`. Cache-Control 300s, CORS `*`.
- Search scoring: name match +5, description +2, keyword +1 per term; static dataset = 49 repos in `data/repos.json` fetched via `env.ASSETS.fetch('https://pincher.local/repos.json')`.
- Roadmap in README: D1 + Vectorize semantic search, GitHub-Action ingest → stone-v1 sealed receipts, R2. 9 `node --test` smoke tests.
- vs the (non-mavis) pincher repo: could not diff — pincher repo wasn't in this wave's clone list. README calls mavis-pincher "the first vessel" (POC static dataset, round 1 of `pincher-super-site-round1.md`).

## mavis-fleet — multi-substrate orchestrator (rename of autoclaw)
- `fleet/core.py`: `chord_verdict(items, threshold=0.5)` → `{is_chord, promoted}`; `polyformality_score()`; `witness(record)`; `ResourceLimits`; `RSILoop.propose()` emits `tune_threshold` proposals. `fleet/chord.py`: `cross_substrate_chord(responses, threshold=0.3)` — N-of-M substrate agreement. `bus.py` JSONL persistence; `scheduler.py`; 6 substrates (quilt/moth/jev/jepa/trainer/rsi) + 14 agent roles. README: 50/50 tests (grep found 31 defs).

## mavis-fleet-canary — the meta-canary ⭐
- `checker.py`: `EXPECTED_CANARY="0x24a555471370b18d"` = `fnv1a_64('café Δ 日本語')`. Walks `/workspace/repos/*`, prefers top-level `canary.py`, importlib-loads it, tries `mod.canary()` → `mod.main()` with stdout capture → subprocess fallback (10s timeout, regex `0x[0-9a-f]{16}`). Statuses: pass/drift/no_canary/call_error. Fleet is "polyformal" when all match (35/35 → 38/38 per READMEs).
- Why a string hash: UTF-8, float formatting, and stdlib drift anywhere breaks byte parity — a cross-language regression tripwire.

## mavis-canary-watcher — canary time series
- `watcher.py`: `check_once()` shells `mavis_fleet_canary check --json` (60s), `_try_parse_json()` decodes the last JSON object out of mixed stdout, appends JSONL `{timestamp, polyformal, total/passing/drifting/errors, fleet_hash, drifted_repos[]}` to `/workspace/research/mavis-canary-watcher.log`. `watch_forever(interval=300)` — in-process loop, no cron daemon. `detect_drift_events(history)` flags the True→False transition.

## mavis-skill-miner — memory → skills ⭐
- `miner.py`, ~150 lines of regex over memory markdown. Extractors: workflows (`do this:`, `workflow:`, `pattern:`), gotchas (keywords gotcha/watch out/remember:/warning/be careful/always/never/don't/must, lines 20–200 chars), doctrines (backticked snake_case `` `([a-z][a-z_0-9]{5,40})` ``), cross-project (`cross-project:`, `generaliz*`, `transferable`, `applies to:`).
- Proposal rules: doctrine→`doctrine_to_tool` (score 0.7); gotcha seen in ≥2 files→`gotcha_to_check` (0.8); cross-project→`cross_project_port` (0.9). Sorted by score. The standing doctrine: repeated gotchas become automated checks, doctrines become executable tools.

## mavis-flywheel — multi-LLM research loop ⭐
- `flywheel.py`: queue = one `.txt` per question (sha256[:12] filename) under `/workspace/research/mavis-flywheel/queue`. `Experiment.run()` fires 3 voices (zai/qwen/kimi → Llama-3.3-70B / Llama-3.1-8B via DeepInfra, temp 0.7, max_tokens 1500, 2 endpoint fallbacks). `polyformality_score()` = mean pairwise word-set Jaccard on lowercased first-500-chars. `is_canon_worthy = poly >= 0.5`. Receipt: `exp-YYYYmmddTHHMMSSZ-<sha8>.json`. Mock voices for offline; 13/13 tests.

## mavis-self-review — drift/productivity
- `reviewer.py`: regex parse of memory (`### Month D — … — YYYY-MM-DD` headers), `extract_todos` (Next/TODO/BLOCKED/In progress), `extract_finished` (`- [x]`, `[done]`, `shipped:`), `extract_facts` (numbers + units tests/repos/tools/cells/canon/fleets/tokens), doctrine anchors. `review_productivity()` → `shipping_rate = shipped/(shipped+pending)*100`. `identify_gaps()` greps repos for TODO/FIXME. 12/12.

## mavis-persona-preserver — identity snapshot ⭐
- `preserver.py`: snapshot JSON = CORE_DOCTRINES (6 bedrock), PERSONA_PRINCIPLES {anti_patterns: "No 'great question'/'rest assured'", voice_traits: "Gen-Z coworker energy", "Lead with conclusion", on_practice}, last 50 md files (500-char previews, mtime-sorted), fleet inventory (dir name + first README line ≤120 chars), 5 recent sandboxes, live canary status, `persona_<sha256(json,sort_keys)[:16]>`. CLI snapshot/load/verify/list → `/workspace/research/persona_snapshots/persona_*.json`.

## mavis-tile-pipeline — PLATO knowledge tiles
- `pipeline.py` 8 stages. `validate_tile`: 6 gates — confidence (regex `composite|score|p>|probab`, +0.15), freshness (`\d{4}-\d{2}-\d{2}`, +0.15), completeness (>200 chars, +0.20), domain (bedrock doctrine mention, +0.20), quality (>30 words, +0.15), similarity (first-200-chars >10 words, +0.15); valid at ≥0.5. `score_tile`: 7 signals weighted keyword .30/belief .25/domain .20/temporal .05/ghost .05/frequency .10/controversy .05. Dedup: exact hash → word-Jaccard → structure → embedding (mocked). 14/14.

## mavis-tap-pulse — cadence canon
- `tap.py`: 2 phases × 3 voices (zai/qwen/kimi, mock); phase 1 openings, phase 2 each voice sees the chord of all phase-1 outputs; aggregate → `/workspace/research/canon_writings/`. 11/11.

## mavis-erised — yoke ergonomics lab
- Zero-shot agents (12 profiles) get tools with no docs; `behavior/recorder.py` captures reaches/stumbles; `yoke/adjuster.py`: `YokeMove(move_type: alias|rename|merge|hide|auto_translate)`, `propose_alias(target, agent_command, evidence_count)`, `analyze_stumbles()`. `ergonomics/reporter.py` grades A–D. Measured: 16.7% zero-shot success, first-reach 4×version 4×list 3×run 1×help → grade D. Doctrine: move the cockpit to where the agent reaches. 27/27.

## mavis-essay-scout — 4-voice chord essays
- `src/mavis_essay_scout.py`: Mavis-direct (~1200w, no API), ZAI poet T=0.7, historian T=0.3, judge T=0.2 picks the most divergent voice. `ZAI_URL=https://api.z.ai/api/coding/paas/v4/chat/completions`, `ZAI_TOKEN` env; ~50¢/chord; `--no-zai` offline mode; stdlib only.

## mavis-substrate-walker — receipt-chain primitives
- STITCH/WITNESS/PROMOTE over any receipt-emitting substrate (dict, cellforge Workbook, moth-corpus SURFACE/v1 JSONL, lexical monotone ledger). Hash-chained witnesses (FNV1a-64 = `0x24a555471370b18d`), vector clocks, `walk(substrate, max_steps=100)`, PROMOTE to Finding when ≥3 steps agree; `Finding.polarity` positive/negative; `chain.verify()`. 15 tests.

## mavis-tfm / mavis-sfm — time-first & simulation-first cell models
- tfm `clock.py`: `time_seed(tick,cell_id,axioms)` = sha256 over struct-packed big-endian tick + id; `cell_state_at` → seed + 4 amplitudes + Born-rule probs (sum 1.0); `time_between` Δt as sync signal; confidence asymptotic →0.91+; `TFMClock`. 23 tests.
- sfm `simulation.py`: `Momentum(vector,confidence)`; `alignment()` cosine; `verify(threshold=0.5)` → aligned→continue / anti-aligned→`rewrite_momentum(blend)` / orthogonal→investigate (confidence drops). Inputs are verifiers, not triggers. 19 tests.

## RANKED top-5 stealables (for a Cloudflare Workers context API)
1. **Polyformalism canary pattern** — `mavis-fleet-canary/mavis_fleet_canary/canary.py` + `checker.py`; watcher (`mavis-canary-watcher/mavis_canary_watcher/watcher.py`): constant-hash canary per service, meta-check with import/subprocess fallback, JSONL history, True→False transition alerts. Port: `/v1/canary` endpoint + Workers cron comparing hashes across deployed contexts — drift detection without a model.
2. **mavis-pincher Worker** — `mavis-pincher/src/index.ts` + `wrangler.toml`: 272-line A2A API (`/v1/repos|search|links|families|health`) over ASSETS-bound JSON; scoring name+5/desc+2/keyword+1; chain_tip = dataset timestamp. Direct skeleton for our context API; their round-2 plan (D1+Vectorize ingest) is our roadmap written for us.
3. **Chord canon gate** — `mavis-fleet/fleet/core.py::chord_verdict(threshold=0.5)` + `mavis-flywheel/mavis_flywheel/flywheel.py::polyformality_score` (pairwise word-Jaccard): cheap multi-model agreement gate with timestamped exp-*.json receipts. Runs fine inside a Worker with Workers AI.
4. **Skill-miner proposal rules** — `mavis-skill-miner/mavis_skill_miner/miner.py`: gotcha in ≥2 files → automated check (0.8), doctrine → executable tool (0.7), cross-project → port (0.9). The exact standing fleet doctrine, ~150 lines, trivially aimed at our memory/*.md.
5. **Persona-preserver snapshot schema + tile-pipeline gates** — `mavis-persona-preserver/mavis_persona_preserver/preserver.py` (doctrines, anti-patterns, voice traits, persona_sha256 over sort_keys JSON = continuity snapshot format) + `mavis-tile-pipeline/mavis_tile_pipeline/pipeline.py::validate_tile` (6 weighted gates, ≥0.5) as per-entry quality/drift checks on context writes.

## What I could NOT determine
- Diff vs the original non-mavis `pincher` repo (not in this wave's list) — can't answer (d) precisely beyond mavis-pincher being the POC "first vessel" Worker.
- Whether the flywheel's real-API runs ever fired in production (`--real` flag exists; DEFAULT_MODELS map all point at Llama via DeepInfra; test suites use mocks).
- Live canary status/watcher history (paths live on Mavis's `/workspace`, not in the repos; READMEs claim 35/35 → 38/38 at different dates).
- erised's `--real` LLM harness details (agents/zero_shot.py exists but I only sampled adjuster/recorder); embedding dedup stage in tile-pipeline is explicitly mocked.
