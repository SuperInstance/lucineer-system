# Scout: SuperInstance/autoclaw — 2026-09-29

Repo: https://github.com/SuperInstance/autoclaw · clone `--depth 1` → `/home/eileen/scratch/autoclaw` (6.4MB, ext4)
HEAD: `07bf131` Mon Sep 21 2026 — "Merge pull request #9 from SuperInstance/feature/web-integration". Stale ~8 days.
License MIT. pyproject `name = "autoresearch"`, v0.1.0, deps pinned `torch==2.9.1` (cu128), `kernels`, `rustbpe`, `tiktoken`.

## What autoclaw IS (three subsystems in one tree)

**1. autoresearch experiment loop (the core; Karpathy nanochat cherry-pick).**
- `program.md` — the agent protocol. Agent edits exactly ONE file: `train.py`. `prepare.py` is declared read-only (fixed constants, data prep, tokenizer, `evaluate_bpb` = ground truth metric). Branch-per-run `autoresearch/<tag>`, results accumulate in `results.tsv`.
- `train.py` (630 lines) — single-GPU, single-file GPT. `GPTConfig` dataclass (sequence_len 2048, vocab 32768, n_layer 12, n_head 6, n_embd 768, window_pattern "SSSL"), RMSNorm, rope, FA3 via `kernels.get_kernel` (Hopper `varunneal/flash-attention-3` else `kernels-community/flash-attn3`). Fixed `TIME_BUDGET = 300s` wall-clock; run as `uv run train.py`. Prints a summary block: `val_bpb`, `training_seconds`, `peak_vram_mb`, `mfu_percent`, `num_tokens_M`, `num_steps`, `num_params_M`, `depth`.
- `prepare.py` — climbs `karpathy/climbmix-400b-shuffle` shards (max 6542), pinned val shard 06542, BPE vocab 8192, `MAX_SEQ_LEN=2048`, `EVAL_TOKENS=40*524288`, cache `~/.cache/autoresearch/`.

**2. `crew/` multi-agent swarm (daemon + bus + task board).**
- Agent loop: `crew/daemon.py` (1283 lines) always-on, "scheduler → runner → brain"; background threads heartbeat/triggers/webhooks; crash recovery; YAML config with `gpu.temperature_throttle_c: 85.0` / `temperature_shutdown_c: 95.0`.
- Task definition/claim: `crew/scheduler.py` `@dataclass Task` (id, title, type ∈ captain_order|triggered|follow_up|maintenance|study, priority, status, `experiment: dict`, hints/notes, `results: dict`, `gpu_seconds_used`, `api_tokens_used`, `agent_id`). Persisted to `data/tasks/{id}.yaml`, active task exposed via symlink. Claim path: `get_next_task()` / `get_unowned_next(agent_id)`; `should_preempt()` / `is_duplicate()` exist.
- Bus: `crew/messaging/bus.py` SQLite pub/sub, `data/messages.db`, lifecycle pending→delivered→processing→completed/failed, dead-letter queue, role-group routing (`any_researcher`, `broadcast`).
- Runner: `crew/runner.py` `ExperimentRunner.run_experiment(params, task_id)` — copies `train.py` → `.py.backup`, regex/AST-patches params in, `_validate_python()` (ast.parse), `_execute_training()` (`subprocess.run`, list-form ✅), `_parse_metrics()`, `_append_results_tsv()`, `_git_commit()`, ALWAYS restores from backup in `finally`. `_failed_result()` exists but only feeds the TSV.
- Agents: `crew/agents/{base,pool,coordinator,researcher,teacher,critic,distiller,scientist,code_reviewer,consistency,security,editor,writer,strategy,project_manager}.py` — 15 role cells already present.
- CF layer: `crew/cloudflare/{fallback,cf_kv,cf_d1,cf_r2,cf_ai}.py` with `CreditTracker` fallback ladder (CF → local).

**3. `si/training_loop.py` (154 lines) — a second, cruder training oracle.**
Watches `./data/incoming`, sha256-hashes batch dirs, GPU-hour budget gate (`AUTOCLAW_GPU_BUDGET`, default 10.0), invokes **`python -m nanochat.train --data <dir> --output <dir>`** via `subprocess.run` list-form, evaluates via `./scripts/evaluate.sh`, promotes by repointing the `models/current` symlink, else `shutil.rmtree` rollback. State: `si/state.json` (`processed[]`, `gpu_hours_used`). Optional `CONSERVATION_ENDPOINT` budget report.

## Gaps (grep-verified, non-git tree)
- **No receipts at all** — `grep receipt *.py` → 0 hits; outcomes only reach `results.tsv` + `data/experiments/`.
- **No pre-flight gate** — `_validate_python()` only ast.parses the patched text; nothing checks imports/dry-run before burning a 5-min run.
- **No graded-confidence fallback** — `crew/cloudflare/fallback.py` is a credit-based *service* ladder, not a semantic confidence pinch.
- **No ledger** — `grep -ri ledger` → 0 hits (only the `AGENT.md` neighbor list).
- **No checkpoint compression** — "quantiz*" hits are only hardware-tier strings (Q4_K_M/Q5_K_M/fp16) in `crew/hardware/detector.py`.
- **No pre-run VRAM floor** — temp throttle/shutdown exist (85/95C), but no free-VRAM admission check.
- **No MCP surface** — 4 incidental "mcp" mentions; no server module.

## Top-5 ranked enhancements

**1. Fail-loud JSON receipt per experiment — `crew/runner.py`** (also mirror in `si/training_loop.py`).
Add `ExperimentResult.to_receipt()` and write `data/experiments/{task_id}/{exp:03d}/receipt.json` from a `finally:` block in `run_experiment()` (covers the `_failed_result` path, exceptions, and SIGKILL-surviving parent). Fields: task_id, exp index, params hash, commit, metric, peak_vram_mb, wall seconds, outcome, error. **Why:** zero receipts today means every doctrine below (gating, pinch, ledger) has nothing to record. Effort **S**. Test: monkeypatch `_execute_training` to raise mid-run; assert `receipt.json` exists with `success=false` + non-null `error`, and that `.py.backup` restore still happened.

**2. FAIL-first pre-flight gate before GPU admission — `crew/runner.py` + `crew/hardware/detector.py`.**
Extend the patch path: after `_apply_modifications`, run (a) `ast.parse`, (b) import smoke, (c) a `--dry-run`/one-step forward pass, and (d) a VRAM floor check (`torch.cuda.mem_get_info()` free ≥ 1024 MiB) and temp ≤ 80C. Format-check BEFORE semantic judgment: reject a malformed patch without spending a single GPU second. **Why:** a bad param patch currently costs a full 300s budget slot. Effort **S/M**. Test: inject `learning_rate = ` (syntax error) and assert gate rejects, `gpu_seconds_used` stays 0, receipt written with `stage=preflight`.

**3. Pinch-to-fallback confidence router — `crew/scheduler.py` (Task.experiment) + `crew/runner.py`.**
Post-eval: if the metric is unparseable/None or the improvement is inside the noise band (|Δ val_bpb| < ~0.002 — tune from `results.tsv` spread), do NOT promote and do NOT iterate on the guess; pinch to a deterministic known-answer path (fixed seed + pinned baseline config re-run, or a stored golden checkpoint compare). Emit `route: "pinched"` in the receipt. **Why:** prevents the swarm drifting onto noise-chasing edits; mirrors our IE3 dilution finding (a confidently-wrong cell must not inherit the task). Effort **M**. Test: feed a candidate whose eval stdout is garbage → assert pinch branch ran, `promote_model` never called, receipt `route=pinched`.

**4. Fleet ledger booking — new `crew/ledger.py`, called from `crew/runner.py` + `si/training_loop.py`.**
Thin client for `POST https://i2i-ledger.casey-digennaro.workers.dev/book`, body `{agent, gist, books_to, receipt_url}`, `Authorization: Bearer <token>` (read at use time, never cached/printed), **`User-Agent` header REQUIRED or CF returns 403 / error 1010**. Best-effort: ledger unreachable must never fail an experiment. Book on promote/rollback, `agent="autoclaw-crew"`, `books_to="autoclaw"`, `receipt_url` pointing at the run's `receipt.json`/commit. **Why:** makes autoclaw a first-class fleet citizen and gives every other lane visibility. Effort **S**. Test: monkeypatch the POST, assert payload carries task_id + param hash + metric + outcome, and that a forced connection error leaves the experiment exit code unchanged.

**5. TurbQuant 4-bit checkpoint compression — new `si/quant/turbquant.py` + `si/training_loop.py` (`promote_model`/candidate dirs).**
Apply our just-measured scheme (seeded random rotation → per-group Lloyd-Max 4-bit codebook → pack) to `candidate_*` weights and optimizer/state snapshots, keeping `models/current` symlink semantics intact (dequantize on load, or store alongside). We measured **8x packed vs float32**. Store blob + codebook + seed + hash in the model dir; log the ratio into the receipt. **Why:** autoclaw keeps every `keep_checkpoints: best_only` artifact on local disk; this is the cheapest capacity win and directly reuses proven work. Effort **M/L**. Test: take one candidate checkpoint, quantize→dequantize, assert file bytes ≤ 25% of fp32 baseline and loss delta within a pre-registered tolerance.

*(Runners-up: specialist-cell routing between cells in `crew/agents/pool.py`/`coordinator.py` per IE3 dilution; an MCP surface over board/next/since/tile_*/pinch/field_query; hypothesis pre-registration in `Task.experiment` to stop post-hoc metric shopping.)*

## Recommended FIRST PR-sized change
**Enhancement #1 — the fail-loud receipt in `crew/runner.py`.** Smallest diff, zero new deps, and it is the evidence substrate every other item (gating stages, pinch routing, ledger `receipt_url`, quant ratio) writes into. One new method + one `finally` block + one test in `tests/`.

## Unknowns / open questions
- Does `python -m nanochat.train ...` in `si/training_loop.py` even resolve? Nothing in this repo supplies a `nanochat` package — likely external/absent, so the `si/` loop may be aspirational. Needs a runtime probe.
- `crew/cloudflare/cf_*.py` not opened (time-box); `CreditTracker` behavior at zero credits unverified.
- Which path is live in production (crew daemon vs `si/training_loop.py` vs bare `program.md` agent) is undocumented; `README.md` shows only the knowledge-crew face while `program.md` shows the nanochat-research face. Reconciling these two identities is itself a candidate enhancement.
- Real GPU spec/budget on the target box unknown — the 1024 MiB VRAM floor is our default, not measured here.
