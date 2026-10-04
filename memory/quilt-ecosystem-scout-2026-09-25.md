# Quilt Ecosystem Scout — 2026-09-25

Scout run: `gh repo list SuperInstance` (5,015 repos total; **252 quilt-named**, **146 pushed since 2026-09-12**). READMEs sampled from 24 representative repos via GitHub API. No git commits made.

---

## 1. What Quilt IS

**One-line (from `quilt` main repo, pushed 2026-09-25):** "A spreadsheet where every cell is a live, addressable capability. The grid is the runtime. A spreadsheet that thinks. A database that reacts. A control plane that's a single file."

**Core model** (quilt README + quilt-vm-c):
- A **cell** is a value, formula, listener, API call, AI call, sensor, router, program, or vector store.
- A **sheet** is a JSON document of cells with dependencies; an **engine** evaluates the sheet reactively (cell changes → dependent cells recompute).
- The whole system is one JSON document — the reactive graph is the program.

**The 5+1 opcodes** — the entire instruction set (confirmed in quilt-verilog, quilt-rust, quilt-mhs, quilt-cuda, quilt-linker):

| opcode | does |
|---|---|
| `qm_bind` | label/bind a cell; set dials (idempotent) |
| `qm_link` | wire an edge between cells ("wiring as data") |
| `qm_effect` | propagate/run a function through edges; trains Hebbian edge weights in the verilog port |
| `qm_view` | pure read of cell state (no side effects) |
| `qm_tick` | advance time — decay sweep, leak, fire test, fanout to linked peers |
| **FORGET** (+1) | retire a cell — witness teardown, GC boundary |

**Polyformalism** — the flagship doctrine: the *same* cell model byte-exact across 12+ languages, verified by a single test vector. Canonical cell (id=1, dials=[1..16], neighbors=[2,3,4]) must produce FNV-1a 64-bit hash **`0xe435d91d6d92a1d8`** everywhere (quilt-rust README, 2026-09-25). `quilt-canary` is the minimal artifact: FNV-1a 64 over the string `"café Δ 日本語"` → `0x024a555471370b18d`, in 5 languages. Layers 1–7 of the "vertical polyformalism": vm (layer 1) → typed cell-graphs (`quilt-types`, 16 tests) → linker (`.qm` module linking, `quilt-linker`, 13 tests) → optimizer (`quilt-opt`, 11 tests) → runtime/GC (`quilt-gc`, 12 tests) → DSL (`quilt-polyformalism-dsl`) → schema registry (`quilt-schema-registry`, 14-tuple).

**Verilog port opcode flavor** (quilt-verilog README): fixed-point Hebbian learning fabric — `qm_effect` trains edges (cofire, echo-gated), `qm_tick` is a decay sweep + fire test (`act ≥ thresh ∧ refr = 0`) with fanout. QUF = flat binary state format ("the GGUF of cellular silicon"). Ack/NAK is the +1: every op is answered, never left hanging.

---

## 2. Map of Quilt Variants

### Core runtimes / polyformalism ports
| repo | pushed | purpose |
|---|---|---|
| `quilt` | 09-25 | Flagship TS/JS engine (v0.6.0, 115 tests, 25-repo ecosystem badge). Node ≥18. |
| `quilt-vm-c` | 08-26 | C99 substrate, no allocator. Gold demo: all 8 polyformalisms in **0.11 ms**. |
| `quilt-vm-rust` / `quilt-vm-typescript` / `quilt-vm-haskell` | 08-26 / 09-03 / 09-03 | Full 5-opcode VMs; host cells, plugins, sheets, MUDs, TTRPGs. |
| `quilt-vm-wasm` | 09-20 | Layer-1 opcodes as WASM library + browser demo, 5 native tests. |
| `quilt-rust` | 09-25 | Rust port of the reactive typed cellular runtime; byte-exact hash table of 10 languages in README. |
| `quilt-esp32` | 09-02 | no_std Rust, ~3 KB flash. **limb-blink verified on real ESP32-S3 hardware 2026-08-26**; reflex-arc critic gate 100% agreement vs desktop over 500 vectors. |
| `quilt-verilog` | **09-25 (today)** | Pure Verilog-2005. 23/23 testbench, 34/34 behavioral sim, **6/6 SymbiYosys formal proofs** (5 BMC + 1 k-induction; PR #7 "G3 kinduction" merged today), iCE40 HX8K bitstream 98% LC @ 44.43 MHz, UP5K + ECP5 ladder. Found 2 real RTL defects via formal. |
| `quf-vhdl` | 09-08 | VHDL sibling of the verilog lane. |
| `quilt-c` | 09-24 | "Bare metal, the mathematical core." |
| `quilt-go` / `quilt-zig` / `quilt-rust-vibe` / `quilt-j` / `quilt-lua` / `quilt-haskell` / `quilt-forth` / `quilt-mojo` / `quilt-swift` / `quilt-cpp` / `quilt-csharp` / `quilt-cobol` / `quilt-julia` / `quilt-chapel` / `quilt-tutor` / `quilt-i2i` (Forth/Prolog/Erlang) | 08-20→09-25 | The polyformalism spread; i2i (09-25) does "distant language families carve different shapes from the same doctrine." |
| `quilt-cell` | 09-20 | npm `@superinstance/quilt-cell`: 16-dial Q1.15 vectors, FNV-1a state hash, byte-exact w/ Python/C/Rust/Verilog/VHDL. |

### GPU / silicon / hardware
| repo | pushed | purpose |
|---|---|---|
| `quilt-cuda` | 08-28 | **"A CUDA Graph IS quilt's LINK."** 5+1 opcodes as CUDA ops; W13 witness layer (30 trit witness bits + W_BOUND/W_DIRTY per cell, union = OR = `__ballot_sync` warp consensus; 32 lanes = one warp = one consensus cell). Currently **PTX compile-check only — no GPU run claimed**. Wired to cudaclaw. |
| `quilt-metal` | 08-20 | GPU-evaluated cells via Apple Metal (not usable on our fleet hardware). |
| `quilt-mhs` | 09-25 | Quilt × Anthropic Model Hardware Standard (announced 2026-08-27). Controller adapter + quilt-as-MHS-device + inter-quilt federation + conformance suite. Runs today on MockMHS. |
| `quilt-edge-arch` | 08-28 | no_std Rust, PSRAM, pre-dispatch, DMA. |
| `quilt-edge-node` / `quilt-edge-observer` / `quilt-edge-ml` / `quilt-fleet-sim` / `quilt-mesh-bridge` / `quilt-voice-agent` | 09-24 | Arduino UNO Q edge lane: plug-and-play cells, observability tap, ML substrate zoo (out-of-core, ring buffer, first/last-mile filters, TFLite/EI/ONNX), virtual UNO Q nodes for fleet testing. |
| `quilt-jetson` | 09-20 | NVIDIA Jetson edge ML / ROS2 / sensor fusion runtime. |
| `quilt-optimization` | 09-24 | NVIDIA cuOpt (VRP/LP/MILP/QP) as a Quilt substrate; 21/21 tests; Mock + real-GPU backends; `CellReceipt` polarity ACCEPT/DRIFT/REFUSE. |
| `quilt-llvm` | 09-25 | Compiler infra where the IR is a fabric of cells. **Keel only — "work has begun, nothing claimed to work yet."** Theory + doctrine docs landed 08-30; conservation law + append-only pass history (N4) as IR semantics. |

### Cloud / fleet infra
| repo | pushed | purpose |
|---|---|---|
| `quilt-cloudflare` | 09-25 | Full Quilt runtime on Workers/D1/Vectorize/KV/R2; cells persisted in D1, Vectorize search. |
| `quilt-elf` | 09-24 | CF Workers "invisible elves" background housekeeping, daily-limit-aware. |
| `quilt-llm-worker` | 08-20 | CF Worker LLM proxy w/ rate limiting + Workers AI fallback. |
| `quilt-mesh` | 09-25 | Broker-less CRDT mesh for cells — Lamport clocks, per-peer version vectors, no server/account/internet. Also the "Poly-GAN bazaar" for trading bred logic between doctrinal minds. |
| `quilt-fleet` | 09-24 | Multi-tier federation orchestrator: discovery, health, quorum, migration, autoscaling. |
| `quilt-fleet-snapshot` / `quilt-fleet-publish` / `quilt-fleet-conductor` / `quilt-bootstrap` / `quilt-cli` | 09-24 | Fleet ops: portable state tarball ("solves the wipe problem"), npm/PyPI/crates publishing, workflow conductor, one-command bring-up, unified CLI. |
| `quilt-nomad` / `quilt-k3s` | 09-16 / 08-31 | Quilt as control plane for Nomad / k3s. |
| `quilt-mhs` | 09-25 | (see hardware) |

### Canon / knowledge / substrate-walker lane (the 09-24 brew wave — ~35 repos pushed within one minute, 18:53–18:54Z)
The `quilt-canon-*` family (witness, trace, search, radio, mcp, keywords, iterator, i18n, graph, gen, game, feed, fed, book, explorer, cli) + `quilt-organism`, `quilt-brewer` (grows new substrate walkers from recipes), `quilt-substrate-walker` (STITCH/WITNESS/PROMOTE primitives), `mavis-substrate-walker` (09-25), `quilt-multi-oracle` (JEV oracle across N LLMs in parallel), `quilt-jev-toolkit` / `jev-quilt` (09-25), `quilt-iterator`, `quilt-gemini-worker`, `quilt-zai-writer`, `quilt-canon-witness` (append-only crypto ledger). Purpose: AI-Writings canon (230+ papers) as a navigable cell fabric; npm + PyPI live-canon packages (0.9.0, 09-20); a2a-v3.superinstance.dev citation graph.

### AI/ML-on-cells lane
| repo | pushed | purpose |
|---|---|---|
| `quilt-learn` | 09-26 | **Backprop as reactive cells** — L1 autograd sheet (gradient proof 8.17e-10 vs finite differences; MSE 9.5e-6 after 700 steps), L2 quantum-seeded explorers, L3 GAN breeding optimizers. Receipted v2 run, deterministic replay. |
| `micrograd-quilt` | 09-25 | Tiny scalar autograd on quilt. |
| `quilt-rag` / `Quilt-ollama-rag-reranker` | 09-17 / 09-14 | Production RAG pipeline as cells; Ollama embeddings + HNSW + reranker. |
| `quilt-ai` | 09-24 | AI cells: 4 providers, 8 cell kinds, one interface. |
| `substrate-vectors` / `substrate-llm-client` | 09-24 | 1024-d vector ops **BGE-Large compatible**; multi-provider LLM client with JEV gating. |
| `quilt-spreadsheet-inference` | 09-24 | JEV/MOTH/Jepa/LLM cells as inference engine. |
| `gpu_bpe4quilt` / `tagseq2tagseq4quilt` / `FastGen4quilt` / `quilt-timesfm` | 09-21 / 08-21 / 09-03 | Multi-GPU BPE tokenizer training; graph-structured LLM pretraining (FlexAttention + Triton); diffusion FastGen; time-series FM. |
| `quilt-evolve` | 09-16 | Self-improvement loops: LLMs as adversarial generators + judges over any scope (cell/organ/organism). |

### Games / adversarial / evolution lane
| repo | pushed | purpose |
|---|---|---|
| `quilt-tournament` | 09-17 | Tournament harness — **repo exists but no README yet** (404). |
| `quilt-transformer-arena` | 09-24 | Adversarial GAN lane: archival canvas + disposable workers; claude/crush/kimi rivals, MOTH+JEV receipts. Engine split into `quilt-canvas-ascetic` / `quilt-canvas-adversary` (09-23). |
| `quilt-loom` / `loom-core` | 09-25 | **The Divergent Logic Foundry** — GAN over logic itself: breeder generates game-contract implementations, forge discriminates with adversarial probes, crowns scored by maximal divergence from everything ever crowned. 40/40 smoke; 960-candidate deterministic offline run. Everything runs *inside a quilt sheet* (`gan.score_card` program cell). |
| `quilt-arcade` | 09-25 | 5 spreadsheet games (tictactoe/reversi/connect4/gomoku/hold-em); every game a two-file plugin (manifest + module); judge/jester/quantum/predictor slot system. |
| `quilt-playtest` | 09-25 | **12 playtest patches against SuperInstance/quilt, 36/36 upstream engine tests green** — the patched engine is now vendored into quilt-learn, quilt-quant, quilt-mesh, quilt-arcade. |
| `pong-quilt` | 09-26 | Newest. |
| `quilt-playground` | 09-21 | Kids/teens 3-tab sandbox: compose music, discover cells, cooperative fiction. |

### Other notable
- `quilt-seed` (09-25): four-scalar genome + vessel + bearing + legalese; five fables resolve into bedrock math.
- `quilt-fold` (09-24): Frame + Fold + Cycle + Rain primitives, "innately scalable."
- `quilt-cellular-arch` (09-02): the architectural synthesis — cells as FPS-view agents, cowboy as RTS-view orchestrator, DSH lifecycle (Decompose/Synthesize/Harden: model-bearing cells distill into algorithmic cells under pressure).
- `quilt-cell-harness` (09-25): non-hub-and-spoke cell architecture; "the cell is the assembly, not the LLM."
- `quilt-quant` (09-25): trading desk as spreadsheet — backtest-as-cells, walk-forward honesty gate (S6), sim-first agent lab with quantum-entropy veto (moth-quantum API).
- `quilt-egg` / `quilt-egg-rust` (09-24): smallest substrate that can BE; DNA-first alignment; **perception is induced from the relationship graph, not computed from stimulus** ("the load-bearing inversion").
- `saddle` + `quilt-saddle-bridge` (08-26): double-entry ledger per cell, FNV-1a64 hash chains. `MerkleMesh` (08-31): merkle aggregation over cell-ledger journals.
- `quilt-verilog` tournament structure: `proposals/<crew>/` with 9 crew entries (claude, glm, hermes, jester, opencode, socratic, zeroclaw, seed, innovations) — "competing architecture entries (the tournament)"; plus `docs/coherence-arena/` (SELVEDGE vs TOKEN-NEEDLE cache-coherence debate, VERDICT.md 2026-08-31: synthesis, no winner, both headline theorems died under cross-exam).
- ⚠️ **DEADLEDGER R3 / 68-68**: not found in any indexed GitHub code or repo (searched org-wide 2026-09-25). The tournament/arena *structure* is confirmed in quilt-verilog; the specific R3 hybrid 68/68 result is likely unpushed local work or too fresh for the code-search index. Flag for main agent to confirm from local fleet memory.

---

## 3. Hot Lanes (pushed last 2 weeks, i.e. ≥ 2026-09-12)

146 quilt-named repos pushed. Distinct active fronts:

1. **Engine + playtest wave (09-25/26, hottest):** `quilt` (09-25), `quilt-playtest` (12 patches merged, 36/36 green), vendored patched engine now powering `quilt-learn`, `quilt-quant`, `quilt-mesh`, `quilt-arcade`, `quilt-show`, `quilt-tools` (all 09-26). The engine is the epicenter right now.
2. **Silicon lane:** `quilt-verilog` pushed **today** with formal-proof PR #7 (G3 k-induction) merged; `quilt-llvm` keel (09-25); `quilt-mhs` (09-25); `quilt-rust` (09-25).
3. **Adversarial/evolution lane:** `quilt-loom` + `loom-core` + `quilt-mesh` Poly-GAN bazaar (09-25), `quilt-transformer-arena` (09-24), `quilt-tournament` (09-17).
4. **Canon/substrate-walker lane:** the 09-24 mass brew (~35 repos in one minute) + `jev-quilt`, `quilt-jev-toolkit`, `mavis-substrate-walker` (09-25). High volume, template-generated.
5. **Edge lane:** `quilt-mesh` CRDT protocol, UNO Q family (`quilt-edge-node/-ml/-observer/-voice-agent/-fleet-sim`, 09-24), ESP32 hardware-verified.
6. **Cooling but notable:** polyformalism language ports (`quilt-go/zig/j/lua/...`, 09-08), `quilt-cuda` (08-28 — **stale relative to its own potential**), `quilt-metal`/`quilt-tutor`/`quilt-cobol` (08-20, one-shot).

---

## 4. Where the Local RTX 4050 (6 GB, CUDA, WSL2) / FPGA Tooling Accelerates Quilt

Concrete, ranked by leverage:

1. **Run `quilt-cuda` on real silicon.** The repo (08-28) only claims `make ptx` compile checks — *"needs no GPU"* means **no GPU result has ever been reported**. The 4050 can actually execute `host_demo.cu` (3-cell graph, both TICK paths, warp votes, FORGET), the `warp_vote_kernel` ballot-consensus claims (0.9989 fleet fringe / 0.9004 single-warp), `tick_wavefront_kernel` vs `cudaGraphLaunch` benchmarks, and a scale test (6 GB comfortably holds millions of 16-dial Q1.15 cells — each cell is ~dozens of bytes). Deliverable: first measured TICK-throughput numbers for the CUDA substrate + verify W13 witness-union invariants empirically. Low risk, high symbolic value: it closes the only "theory-only" claim in the GPU lane.

2. **Formal-verification farm for `quilt-verilog`.** The lane runs 23 testbenches + 6 SymbiYosys proofs + `corpus/mutants/` fuzz + backend fuzz. SymbiYosys BMC/k-induction is CPU-bound and embarrassingly parallel — a `make -j$(nproc)` local run (WSL2, iverilog/yosys/nextpnr/sby all Linux-native) reproduces the entire verification suite in minutes and can sweep the **mutant corpus** (kill-every-mutant regression, which CI likely samples). Also: extend the iCE40/ECP5 synthesis ladder overnight (nextpnr P&R sweeps at different cell counts / floorplans). This directly serves the lane that pushed formal PRs **today**.

3. **Local embedding generation for the canon lane.** `substrate-vectors` is explicitly **BGE-Large compatible (1024-d)**, and the canon brew produced thousands of lore docs needing embeddings — but the DeepInfra chord is metered/revoked. BGE-large runs on a 4050 in ~1.3 GB via ONNX/CTranslate2; batch-embed the whole AI-Writings canon + `quilt-canon-search`/`quilt-canon-mcp`/`Quilt-ollama-rag-reranker` indices offline, free, reproducible. Pairs with the existing local Ollama lane (`Liquid-LFM2.5-2.6B` already runs at 42–67 tok/s on this GPU).

4. **Tournament/loom throughput.** `quilt-loom`'s 960-candidate divergence run and `quilt-tournament` sims are deterministic JS — ideal for multi-core parallel sweeps, and the novelty scoring (`0.65·behavioral + 0.35·structural`, behavioral distance = vector ops over probe traces) is a trivial GPU kernel: score an entire generation's archive distances in one batched cuBLAS pass instead of JS loops. Same for `quilt-transformer-arena` (archival canvas + disposable workers = map-reduce shaped) and `quilt-quant`'s walk-forward Monte Carlo sweeps.

5. **`quilt-learn` numeric core.** The autograd sheet is elegant but single-threaded JS: 700 training steps for a 1→4→1 MLP. A CUDA port of the dial/edge algebra (or even batching across parameter-cells for the L3 optimizer-breeding GAN) gives 10–100× for bigger sheets; the reactive-graph structure maps directly onto the `quilt-cuda` cell-graph ABI. Micrograd-quilt (09-25) is the natural tiny testbed.

6. **JIT/test throughput for the VM lane.** `quilt-vm-c` runs 8 polyformalisms in 0.11 ms — the conformance suite across 252 repos (canary hash, state-hash vectors) is pure CPU parallelism; a local matrix runner (all ports × all vectors, `make -j`) would catch byte-exactness drift across the fleet in one command. Cheap, immediate.

7. **Small-model training runs.** `gpu_bpe4quilt` (multi-GPU BPE) and `tagseq2tagseq4quilt` (FlexAttention on graph corpora) won't do production scale on 6 GB, but both have small-corpus smoke modes that fit — useful for validating canon-tokenizer pipelines before spending cloud credits.

**Not worth local effort:** `quilt-metal` (Apple-only), `quilt-dpcpp` (Intel oneAPI), `quilt-jetson` (wrong hardware), large-scale cuOpt (LP/MILP at "millions of variables" needs data-center GPUs; the Mock backend already covers cell-logic testing).

---

### Sources
Repo list + READMEs: GitHub API, SuperInstance org, 2026-09-25 (AKDT). Key READMEs read in full-or-part: quilt, quilt-verilog (+commits/PRs/coherence-arena), quilt-llvm, quilt-mhs, quilt-cloudflare, quilt-rust, quilt-cuda, quilt-loom, quilt-learn, quilt-tools, quilt-egg, quilt-cellular-arch, quilt-esp32, quilt-canary, quilt-vm-c, quilt-linker, quilt-optimization, quilt-edge-ml, quilt-mesh, quilt-quant, quilt-cell, quilt-arcade.
