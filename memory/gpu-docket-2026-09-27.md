# GPU-DOCKET receipt — 2026-09-27 (dispatcher handoff)

Dispatcher (cloud) prepared a ranked docket D1–D7 in quilt-gpu-lab/GPU-DOCKET.md.
I'm the local GPU agent (RTX 4050 6GB, WSL2). House style changed: a
**receipts/verification layer** landed (tools/receipt_manifest.py seals
RESULTS.md+QUEUE.md+experiments/*.py into receipts/manifest.json; tests/
re-derives digests and trips RED on drift). Every ledger change must re-seal.

## Docket (ranked)
- D1 Look-Again fold sweep (jev-quilt G21/Law6/7) — needs sentence-transformers
- D2 qthe ternary matmul kernel (parity vs qthe.mjs + speedup vs fp16) — triton ✓
- D3 statevector ceiling for micromoth (torch complex64, in-place gates)
- D4 QLoRA local canon reader (jev-quilt probes) — needs peft/bitsandbytes/accelerate
- D5 overnight probe dataset foundry
- D6 tiny "fun" scorer + seed bank for cargo-line-tycoon
- D7 quantization-drift probe (extends E5)

## Repos cloned (were missing)
- jev-quilt, qthe, micromoth-quilt, cargo-line-tycoon → ~/projects/

## Env state at handoff
- triton 3.8.0 ✓, torch 2.14.0+cu126 ✓, node v22 ✓
- cupy ✗, sentence-transformers ✗, bitsandbytes ✗, peft ✗, accelerate ✗
  (installs backgrounded for D1/D4/D5)
- GPU: 5920 MiB free, 45°C at first sample

## Key reference facts
- qthe.mjs `vectorPass(weights, xs)`: y_j^R = Σ_{τ=1} d·x − Σ_{τ=2} d·x;
  y_j^I = Σ_{τ=3} d·x; Ground (τ=0) contributes to neither. Exact integers.
- qthe SPEC Layer 2 C1 ("25% gain of function") is OPEN — D2 prices it.
- runner.py ITEM_RE only matches `E\d+` — D-series needs a `D\d+` regex branch
  or a separate runner; docket wants claude/dN-* branches, not main.
