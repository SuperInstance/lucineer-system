# Night Watch 2026-09-27 — GPU Autoresearch (Casey asleep, PRs by morning)

Casey's order (02:02 AKDT): study all quilt repos, use the GPU (RTX 4050, 6GB, CUDA via /dev/dxg) in ways no other agent can, push often, PRs by morning. "Ralph Wiggums yourself."

## Environment ground truth (verified 02:05)
- GPU idle (0 MiB used). nvidia-smi at /usr/lib/wsl/lib/nvidia-smi.
- gh authed as SuperInstance, ssh protocol.
- torch NOT installed in system python — pip install torch (cu124/cu126 wheel) needed for GPU lanes.
- Ollama on 127.0.0.1:11434 (Liquid LFM2.5, granite) — free GPU inference.

## Lane plan (SERIAL — one lane at a time, doctrine)
1. **L1 elephant GPU**: room-state embedding v3 prototype — cold/warm contrast training on RTX 4050 (torch CUDA). Branch in SuperInstance/elephant, PR. Use existing fixtures/data in repo; if no data, synthesize + document honestly as prototype.
2. **L2 quilt-verilog GPU sweep**: port the fixed-point cell golden model to a CUDA (or torch) parallel kernel, sweep step-edge Δ / drift parameter space massively parallel, cross-check against iverilog/Python golden vectors. Branch + PR in SuperInstance/quilt-verilog.
3. **L3 quilt-rust perf**: criterion bench harness + optional rayon parallel tick, no semantics change, byte-exact tests still pass. PR.
4. **L4 report**: fold night results into a morning brief (memory/night-2026-09-27.md + PR bodies).

## Rules
- NEVER delete anything; branches only; PRs to main; archive-by-rename.
- Verify before push: tests must run green locally.
- Docs style: undersell, overdeliver. Failures first-class.
- One lane at a time; next lane spawns on completion event.

## Progress log
- 02:57 L1 DONE — elephant PR #5 (gpu/room-state-embed-v0, +1530): trained on RTX 4050, 80 epochs/11.3s, held-out gains booked, κ-compression open problem booked honestly. Verified OPEN via gh.
- 02:59 L2 SPAWNED — quilt-verilog GPU fabric sweep (bit-exact int64 torch port vs golden vectors; M1/M2/M3 + SPIN spaces). Running.
- torch gotchas: system python3 has torch via --user --break-system-packages; also ~/venvs/elephant-gpu. Python 3.14 needs cu126 index.
