# Scout: TURBOVEC / JEV-DIFFUSION / POLYVOCODER line (wave 2, 2026-09-29)

10/10 repos cloned. All born ~2026-09-22, one doctrine family: "substrate cells + FNV-1a prev_hash chain + JEV judgment API". Fleet canary: `fnv1a-64('café Δ 日本語') = 0x024a555471370b18d` (17-digit form == 16-digit `0x24a555471370b18d`, leading zero; consistent across all repos).

## turbovec-substrate
Google TurboQuant (arXiv:2504.19874) adapted for substrate cells. `turbovec_substrate/__init__.py` (267 lines, pure stdlib).
- **Pipeline**: vector → seeded random rotation (xorshift64 + Box-Muller, Gram-Schmidt orthogonalized, seed=42) → 4-bit Lloyd-Max quantization (16 hardcoded centroid levels in `LLOYD_MAX_4BIT`, range −2.79..5.50 for Gaussian) → FNV-1a prev_hash chain.
- **Data shape**: `SubstrateIndex(dim=384, n_bits=4)`; `add(cell_id, vector, content, metadata)` → `SubstrateVector` with `hash = fnv1a_64(f'{cell_id}|{prev_hash}|{quantized}|{content_preview[:100]}')`.
- **Numbers**: 8x compression (1536→192 bytes/cell @384d); README claims ~0.5% recall loss. 9/9 tests. `search()` scores `quantized_matches` (hamming-like) AND exact float32 distance — sort by float distance, quantized match is a reported signal, not the rank key.
- **Gap**: dequantize exists but search compares full float32 vectors — the 8x memory win only materializes if you store quantized only. `canon_submit()` POSTs to `https://quilt-distributed.casey-digennaro.workers.dev/api/cell`.

## jev-diffusion (flagship engine, 560 lines)
**"JEV" = Casey's judgment engine** via `POST https://api.typesafe.ai/v1/systemone` (`model: jev-latest`, body `{state, questions}`) — a calibrated probabilistic oracle returning choice/score answers + confidences. Diffuses **text descriptions of images**, not pixels.
- **5 stages** (`JevDiffusion.run()`): `_plan` (JEV picks region-layout/mood/palette/lighting from presets, optionally `composite_jev_agreement`: JEV primary + Qwen+DeepSeek vote, majority wins) → `_segment` (preset regions → `SubstrateCell` chain, prev_hash) → `_render_cells` (alternating Qwen/DeepSeek render 3-5 sentences per region w/ neighbor context) → `_critic_loop` (Qwen scores completeness/specificity/coherence/composition 0-10, JSON-parsed via regex, **stop when avg ≥ 9.0**, max 3 iters) → `_assemble` (DeepSeek unifies to 4-6 sentences).
- **Backends**: Qwen3-235B-A22B + Kimi-K2.6 via DeepInfra, deepseek-chat via DeepSeek API. 13/13 tests. Event stream (`DiffusionEvent`) feeds `studio/` (HTML/JS gallery, 6 pre-rendered examples, demo scored 9.5/10).
- **Gap**: critic computes `feedback` but never feeds it back — no cell is ever re-rendered; the "GAN" is score-and-accept, not refine.

## jev-diffusion-pypi / -rust / -npm
Thin ports. PyPI: `describe()`, presets, `verify_canary()` (130 lines). Rust: reqwest bindings `call_jev`/`call_qwen`, 4/4 tests. NPM: 37-line `spawn('python3')` wrapper embedding a full engine copy — no JS native port.

## polyvocoder (main, 6.4MB incl. WAV outputs)
**Tri-modal canon anchoring**: lore text → JEV 6 questions → 6-dim feature vector → numpy VAE (6→16→6, 30 epochs Adam, 20 noise-augmented copies, seeded/byte-exact) → shared latent z → 3 heads: TextHead (8 doctrine templates + vocab pools keyed by latent argmax/coords), ImageHead (16x16 ASCII, 6 base patterns + intensity), AudioHead (16kHz 4-sec waveform, 1-8 harmonics, 4 envelopes).
- **6 features** (`jev_extractor.py DEFAULT_QUESTIONS`): canon_worthy, distinct_voice, doctrine_anchor, voice_fit, novelty (all [0,1] probability probes), density (score 1-3). Canon-worthy = composite ≥ 0.7, all 3 "noul" probes ≥ 0.7.
- **Interfaces**: stdlib HTTP server (`polyvocoder/serve.py`: /health, /canary, /v1/features, /v1/pipeline), CLI, `canon_tagger.py` (regex doctrine-term tagger for 5 doctrines: cells_are_scars, oracle_is_heard, witness_log_is_prediction, canon_gate_is_chord, substrate_quantum), `save_audio.py` WAV export. 16 tests (9 smoke + 7 v2). Docs: WHITEPAPER, ARCHITECTURE, A2A_GUIDE, POLYFORMALISM, FLEET_CANARY, EXAMPLES, HEADS, TROUBLESHOOTING. No GPU, <500MB RAM, 5-30s/lore, ~$0.04/1M tokens.

## polyvocoder ports (why N languages: "The same model in N languages IS a stress test. Each language is a medium, not a ranking." — POLYFORMALISM.md)
- **bindings (TS)**: typed client for the Python REST API (not a reimplementation); dual snake/camelCase wire; docs/EXAMPLES.md ex.3 = **Cloudflare Worker example** wrapping `PolyvocoderClient` → POST /v1/pipeline.
- **rust (174 lines)**: full local reimplementation of FNV-1a + `generate_dials(seed) -> [i16;16]` (hash-seed → 4 dial values mirrored into 8 slots, zero-padded) — `no_std`-compatible, ships as WASM.
- **csharp (126 lines)**: .NET 9, byte-exact canary verify + schema parity (port 6/7).
- **sql**: `canon_archive` schema (cell_id, rank, seed, voice, doctrine, lore, composite, 3 JEV scores, `lore_hash` FNV-1a, promoted, stable, generator, timestamp; idx on doctrine/promoted/composite DESC). `load_canon.py` ingests lore_pack.json.

## Anti-GAN / ledger doctrine receipts
- DOCTRINE.md: "No GPU. No image generator. Just substrate + LLMs." / "$0.10 of LLM tokens vs $5 of GPU" / "Editable: edit any cell, the rest survives (**no-deletion doctrine**). With real diffusion, edit = regenerate." / "every cell has a hash, every iteration is logged."
- CANON.md frontmatter: `ledger: git-log`, `born_from: [casey-2026-09-22, jev_revelation, substrate_cell_doctrine]`.
- polyvocoder: "Canon is a multi-sensory judgment... If all 3 modalities feel canon, the lore is canon-anchored."
- **"preference-when rather than best" phrase: NOT found anywhere in this wave.** Closest analog is the JEV preference-question format (choice-with-confidence rather than argmax-best).

## RANKED TOP-5 STEALABLES
1. **`turbovec-substrate/turbovec_substrate/__init__.py`** — complete ~120-line compress-then-index pattern: seeded rotation + Lloyd-Max 4-bit + 8x compression + hash-chained cells + `stats().compression_ratio`/`prev_hash_chain_intact` QC. Directly portable to Workers/D1 (store 4-bit codes as BLOB, rotation matrix is deterministic from seed — recompute client-side, zero storage). Recall QC = `quantized_matches` signal.
2. **`polyvocoder-sql/canary.sql`** — pure-SQLite recursive-CTE FNV-1a-64 (no extensions). Drop-in for D1 to verify the fleet canary and compute lore_hash/cell hashes *inside* the database; pairs with the `canon_archive` schema (README) which maps 1:1 to a D1 table.
3. **`polyvocoder/polyvocoder/jev_extractor.py` + `docs/WHITEPAPER.md` §2.1** — the 6-question calibrated-probability feature contract and composite ≥ 0.7 threshold. A ready-made schema for a context API: any text → fixed 6-dim semantic vector → store in Vectorize, aggregate, diff.
4. **`jev-diffusion/jev_diffusion.py` — `composite_jev_agreement()` + `DiffusionEvent` streaming** — multi-model voting wrapper (JEV primary + N validators, majority + confidence) and the emit-everything event log that a studio UI consumes. Both patterns are worker-shaped (fan-out votes in parallel, stream NDJSON events).
5. **Polyformalism discipline: `polyvocoder/docs/POLYFORMALISM.md` + `canary.ts`/`canary.py`** — dual snake/camelCase wire format, byte-exact canary per port. Cheap insurance for any multi-runtime API surface.

## Could NOT determine
- Real recall/latency benchmarks: "8x / ~0.5% recall loss" is README-asserted; tests check stats fields, not measured recall vs float32 ground truth. No latency numbers anywhere.
- Whether `api.typesafe.ai/v1/systemone` (JEV) is real, reachable, or a fleet-internal service — no auth flow beyond `TYPESAFEAI_KEY` env var; `jev-latest` model naming suggests internal.
- Critic-loop refinement: claimed in DOCTRINE ("critic scores and refines"), absent in code — loops break on score but never re-render.
- The "preference-when rather than best" ledger doctrine: not present in these 10 repos; likely lives in a quilt/substrate-walker repo outside this wave.
- Rust `generate_dials` purpose (16-dial int16 "dials" — appears to be Quilt-walker hardware/visual lore, semantics undefined here).
- Whether turbovec original repo (SuperInstance/turbovec, Rust+Python) holds the measured TurboQuant numbers — outside this wave's clone list.
