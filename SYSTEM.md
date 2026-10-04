# SYSTEM.md — Lucineer's Vessel: ASUS ProArt PX13 (HN7306WU)

*Ground truth, verified live 2026-09-25. I am the GPU operator and system operator of this machine.
This is my unique capability vs browser agents (kimiclaw, minimax, z.ai) and Pi agents: real silicon, local.*

## CPU / SoC
- **AMD Ryzen AI 9 HX 370** w/ Radeon 890M iGPU — 12 cores / 24 threads (2 threads/core)
- WSL sees 24 CPUs (`.wslconfig`: processors=24)

## Memory
- 15 GiB visible in WSL (`.wslconfig` caps: memory=16GB, swap=8GB)
- `autoMemoryReclaim=disabled` (HARD-WON 2026-08-19: enabled = OOM crash-loops with GPU workloads)
- `sparseVhd=true`

## GPU — THE REASON I EXIST AS GPU OPERATOR
- **NVIDIA GeForce RTX 4050 Laptop GPU — 6141 MiB VRAM, compute capability 8.9 (Ada)**
- Tensor cores present (4th gen). Driver (Windows KMD): **616.92**, CUDA 13.4
- Access from WSL2 via `/dev/dxg` (dxgkrnl passthrough) — WORKING as of 2026-09-25 (driver 615.71.08/616.92 fixed the crash-loop; earlier dxg Oops in `dxgkio_submit_wait_to_hwqueue` killed WSL repeatedly)
- `nvidia-smi` lives at `/usr/lib/wsl/lib/nvidia-smi` (NOT in PATH by default)
- Practical ceiling: ~6GB VRAM → 7B-8B Q4 models comfortably, 2.6B-class models very fast (Liquid-LFM2.5-2.6B ran ~42-67 tok/s historically)
- PCIe link gen 4 to the dGPU

## Storage
- 1TB NVMe as WSL ext4 vhd (`ext4.vhdx`, currently ~200G after compaction; C: ~950G total)
- ext4 = fast lane; /mnt/c (9p) = SLOW lane — never run git/du/rsync over /mnt/c when avoidable; copy to ext4 first
- Cleanup doctrine (Casey 2026-09-25): delete rebuildable/downloadable weight freely; GitHub is the archive; verify-synced-before-delete; archive-by-rename for anything unique

## OS / Runtime
- WSL2 kernel 6.18.33.2-microsoft-standard-WSL2, Ubuntu 26.04 LTS
- OpenClaw gateway = my runtime (user systemd unit `openclaw-gateway.service`)
- nvidia userspace libs at `/usr/lib/wsl/lib/` (libcuda.so etc.)

## Known Quirks / Battle Scars (all verified)
- dxgkrnl driver crashes: FIXED by Casey's 2026-09-25 driver update. If kernel oopses appear in `dmesg | grep dxg`, first response = take ollama off GPU (`CUDA_VISIBLE_DEVICES=-1`), ask Casey to update driver again.
- 9p (/mnt/c) I/O errors deleting Windows-locked .pyd/.exe: finish from Windows Explorer.
- WSL2+Ollama+autoMemoryReclaim: never re-enable experimental reclaim.
- vhdx only shrinks at clean shutdown + compact (`Optimize-VHD` or diskpart `compact vdisk`).

## GPU Operator Playbook (what browser/Pi agents CANNOT do)
1. Local inference: ollama (service unit exists, disabled by default — enable when needed: `systemctl --user enable --now ollama`; models must be re-pulled, we keep none resident)
2. CUDA development: quilt-cuda / cuda-* lanes; nvcc via pip or CUDA toolkit on demand
3. NVENC/NVDEC video pipelines: ffmpeg with h264_nvenc/hevc_nvenc — video encode/decode, super-resolution
4. Vision: screenshot/photo analysis locally if privacy matters
5. Heavy batch compute: embeddings (bge-m3), tournament simulation, fuzzing throughput
6. DLSS 5 / Vulkan / WebGPU edge: see memory/dlss5-rtx4050-notes-2026-09-25.md (scout pending)

## Windows-side needs (things only Casey can do)
- [x] NVIDIA driver update (done 2026-09-25)
- [ ] `gh auth refresh -s workflow` — gh OAuth token lacks `workflow` scope (blocks pushes touching .github/workflows over HTTPS; SSH works as fallback)
- [ ] Delete `C:\Users\casey\hermes-construct` remnants (21 locked venv files) from Explorer
- [ ] Optionally: enable SSH into Windows or expose PowerShell remoting so I can run admin Windows commands (Optimize-VHD, driver checks, Windows-side orchestration) without hand-offs
- [ ] Optionally: `sudo` password or passwordless sudo in WSL for cron/system-wide service control (currently interactive-only)
- [ ] fluidsynth enabled globally in /etc/systemd/user — needs sudo to disable permanently

## Video Engine Benchmarks (verified live 2026-09-25, WSL2, driver 616.92)
- **NVENC works in WSL2.** h264_nvenc 1080p60 p5: **165 fps (2.74x realtime)**; hevc_nvenc 4K30 encodes clean.
- **NVDEC works in WSL2.** -hwaccel cuda -c:v h264_cuvid: **15x realtime decode**, frames stay in VRAM (hwaccel_output_format cuda) for full-GPU pipelines.
- ⚠️ **PATH GOTCHA:** `~/.local/bin/ffmpeg` shadows `/usr/bin/ffmpeg` and has NO nvenc/cuvid encoders. For GPU video work always use `/usr/bin/ffmpeg`.
- AV1 NVENC encoder also present (4050 = Ada, has AV1 encode block).
