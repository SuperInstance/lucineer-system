# 2026-09-25 — Disk cleanup (C: 99% full, 12G free)

- WSL vhdx: 347G (real usage 315G). Compact/sparse after cleanup.
- WSL crash fix: dxgkrnl Oops (dxgkio_submit_wait_to_hwqueue); nvidia-smi dead from WSL.
  Ollama set CPU-only via CUDA_VISIBLE_DEVICES=-1 in ~/.config/systemd/user/ollama.service.
  NEEDS: Casey updates Windows NVIDIA driver / reboot to restore GPU lane.
- Phase 1 (approved "continue"): purging rebuildable build artifacts — Rust target/ dirs (~31G):
  quilt-rust, _archive/OpenConstruct, fleet-gateway, _archive/flux-vm, quilt-rust-selfimprove,
  quilt-mhs-playtest, quilt-llvm*/llvm-fabric, quilt-tournament/teams/deadledger, study-cudaclaw*,
  fleet-gateway/clients/rust, study-murmur, plus archive-project node_modules (~5.5G).
  These regenerate via cargo build / npm install — no data loss.
- Phase 2 pending: .ollama trim (42G, 20 models, many dupes) — awaiting Casey's keep-list.
  Suggested keeps: Liquid family, bge-m3, one qwen coder.
- Phase 3 pending Casey: ~/models 49G (diffusion checkpoints), ~/backups 49G.

## Repo sweep (Casey "go" 13:57)
Deleted local clones (verified synced to GitHub at deletion): ~/projects/_archive/*, study-*,
same-remote strays (ta, symphony-*, si-*.archived-*, zeroclaw-dissertation.corrupt-20260917,
Scrapcraft-comp-*), ACE-Step-1.5, songforge, quilt-dpcpp (empty).
Kept: active flat projects, ~/backups/github-mirror.
Pending: fleet-gateway unarchive→push→re-archive (awaiting Casey).
fleet-gateway: unarchived→pushed 5b2285b→re-archived (2026-09-25 14:24, Casey go)
github-mirror (49G, 4473 bare clones) DELETED 14:39 after verifying 0 mirror-only repos
vs full GitHub list (5014 repos) — fully redundant. Casey approved.
Hermes Windows-side exit (15:16-15:40): hermes-construct (nested repo, 565M, dirty) pushed to
SuperInstance/hermes-construct main (aca337c17 + artifacts commit 73d2dd8b0 — windows-side-artifacts/:
hermes_search, monitor capture png, social_profiles_hermes.md). Push needed SSH (OAuth token lacks
workflow scope; remote rejected workflow file change). All 4 items deleted from C:. Deck-hand
slice-of-life piece landed in AI-Writings (3ab40748, 2026-09-25-bilge-day.md) via glm-5.3-flash subagent.
Round 3 (15:53 "keep moving"): deleted clang+llvm-18 (3.5G), python3.14 AI stack (nvidia/torch/triton/static_ffmpeg ~5.4G,
reinstallable), pnpm store pruned, uv cache, mamba pkgs. Kept: ollama runtime lib, opencode/claude shares, piper voices,
oss-cad-suite (quilt-verilog), ghcup (Haskell, awaiting Casey verdict).
Round 4 (16:08): ~/.ghcup (Haskell, 5.2G) and oss-cad-suite (2.1G) deleted per Casey "get it all cleaned up"
(reinstallable: ghcup.org / OSS CAD Suite release zip). Kept: .rustup/.cargo (active Rust lanes),
llvm-portable (quilt-llvm), ollama runtime, opencode/claude shares.
Round 5 (final): micromamba + micromamba-envs (4.5G), .platformio (2.9G) deleted. Reinstall paths:
ghcup install / OSS CAD Suite zip / pio platform install / conda env rebuild.
