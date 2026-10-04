# The Local Orchestrator — "Sawyer" Architecture
**Date:** 2026-09-27 · **Author:** design subagent · **Status:** seed v1, iterate with Casey

Casey's vision: a low-level engineer that runs always-on at the edge of the local GPU + system and **orchestrates rather than grinds** — a Tom Sawyer who gets others to paint the fences. It recruits cudaclaws (CUDA algorithm-bots), algorithm bots on any local chip, and fleet subagents when their lanes are free. It is budget-aware and load-aware: throttles down when other work is happening, throttles up at idle. Flow-state is an ethos constraint: **the hardware is thinking all the time; prompts are nudges, higher LLM calls are guides.**

Hardware: RTX 4050 6GB (CUDA 13.4 via `/dev/dxg`, WSL2), Ryzen AI 9 HX 370 (NPU + CPU lanes). Seed workload: chiaroscuro — realtime webcam→ASCII renderer (Mirror/Sculptor/Studio/Director doors), extending into screen-region capture, video processing, and a two-panel viewer.

## 1. Components

- **Sawyer daemon** (`sawyerd`) — systemd unit, `Restart=always`, `MemoryMax` set, lives on ext4 (never `/mnt/c`). Owns no compute itself; it only holds **leases**. Small poll loop (1s tick), O(queue) memory, spool checkpointed to disk.
- **Sensor bus** — reads NVML (GPU util, VRAM, temp/power), `/proc` load, WSL2 host signals (foreground app via Windows bridge), and the **budget ledger**.
- **Job spool** — append-only job records on ext4; each job is resumable and idempotent (chunked, never O(corpus)).
- **Worker registry** — every worker (cudaclaw, chip bot, subagent) registers a **contract**: capability, chip, VRAM/SM/CPU cost, expected duration, preemption semantics.
- **Chiaroscuro lane** — first-class resident workload; its doors (Mirror → +Screen capture → Studio/Director two-panel) are the visible face of the machine "thinking."

## 2. Throttle & Scheduler

The scheduler is a **ramp, not a switch** — four levels with hysteresis (EMA-smoothed signals, 30–60s dwell before transitions, so it never flaps):

- **L0 Parked:** interactive/other work owns the machine. Sawyer only sensors + spool. Chiaroscuro drops to minimum fps or frame-skips.
- **L1 Trickle:** spare cycles exist. One cheap worker (e.g., ASCII render at low res, CPU/NPU bot).
- **L2 Cruise:** machine mostly idle. Multiple cudaclaws; VRAM budget honors a **standing headroom reserve (~1.5–2GB)** so foreground work never stalls.
- **L3 Harvest:** deep idle (overnight, lid-open-and-walked-away). Full queue drain, video batch processing, long kernels.

Budget is two-lane by design: **local compute is free — harvest it; LLM calls are metered — they are guides, not grinders.** The ledger caps higher-model calls per epoch; when a problem needs brains, Sawyer escalates to a guide (GLM-5.3 subagent), then returns to local grinding. Flow-state means the default is autonomous drift work; humans and LLMs only nudge direction.

## 3. Recruitment

- **cudaclaws:** self-contained CUDA kernel-bots (single binaries with a JSON contract header). Sawyer launches by contract, watches duration, and can evict (SIGTERM → checkpoint → requeue) instantly. VRAM is the scarce currency — contracts declare it; the scheduler admits by best-fit.
- **Chip bots, any silicon:** same contract interface over different runtimes — Ryzen AI NPU via ONNX/Vitis EP, CPU lane for Liquid LFM2.5-2.6B (the boat brain, offline), iGPU. Chip-agnostic recruitment is what makes "hundred boats" possible: one registry, many silicons.
- **Subagents:** Sawyer never calls cloud models directly for grinding. It posts **task cards** to the fleet queue; the main agent dispatches GLM-5.3 subagents *when their lanes are free* (subscription lanes = effectively unmetered, but attention is the real budget). Subagent output lands back in the spool as new jobs or contracts.

## 4. Phases (concrete ships)

**Phase 1 — The Fence (2–3 weeks):** chiaroscuro gains the **Screen door** (screen-region capture → ASCII pipeline), video file ingestion, and the **two-panel viewer** (source | render). Ship `sawyerd` v0: sensor bus + L0/L1 throttle only, one cudaclaw contract (the chiaroscuro kernel chain). Success = always-on without ever visibly stealing from Casey's foreground work.

**Phase 2 — The Painters (next):** full four-level ramp, spool + registry, 3–5 cudaclaws (frame-diff, edge-detect, palette LUT, batch transcode), first NPU bot, VRAM headroom enforcement, budget ledger with nightly harvest windows. Success = overnight video queue drains itself at L3 and yields before morning use.

**Phase 3 — The Crew:** subagent task-card recruitment, guide escalation path (local drift → stuck → one GLM-5.3 consult → resume local), self-telemetry (what did the machine think about all week?), and a Director door that composes long-form output from harvested queues. Success = Sawyer plans its own next jobs from leftover artifacts.

## Keystone decision

**The unit of orchestration is a preemptible, resource-declared job contract — not a process.** Every worker, from a CUDA kernel to a cloud subagent, advertises cost and can be paused/evicted/requeued without ceremony. This one choice makes throttling trivial (ramp = how many contracts Sawyer honors), makes recruitment symmetric across chips, and keeps the daemon crash-safe. Its corollary: the free-lane/metered-lane split — local silicon thinks for free, LLMs are nudges.
