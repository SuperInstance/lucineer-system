# Quilt, GPU-native — design thinking on innate scaling · 2026-08-21

**Commissioned:** Captain's directive 2026-08-21 10:48 · **Author:** quilt GPU-native design thinker (subagent, read-only)
**Question:** *"let's think about how, on a deeper level, quilt could be closer to GPU-native for innate scaling abilities."*
**Inputs read:** quilt/README.md, quilt-rust/README.md + src/crates layout, elephant/scripts/ (the CUDA batch farm — `field_math_gpu.py`, `encoder_gpu_scale.py`), quilt-rust/docs/{cell-ledger,cuda-ptx-tier,field-edge-ledger-bridge,mojo-tier}.md, crates/field-edge-bridge/, memory/{quilt-synergy-map,cloudflare-migration-plan}-2026-08-21.md, elephant/vmf.py + field.py.
**Constraint honored:** read-only everywhere; nothing modified, no commits.

---

## 0. The one-sentence thesis

Quilt is not a program that could *use* a GPU — it is a **reactive graph of cells** that, the moment its vector-valued cells (fields, embeddings) are shaped as tensors from birth, *is* a GPU program whose scheduler is the reactive engine and whose audit trail is the ledger. The fleet has already proven the pattern twice in elephant (`field_math_gpu.py` — 111.6×, bit-parity to CPU, commit 5c8a44f; `encoder_gpu_scale.py` — 3.46×, *data-limited not capacity-limited*, 3af376b). Quilt-rust has already sketched the tier (`docs/cuda-ptx-tier.md`) and the wasm target (`crates/quilt-core-wasm`). What is missing is the **decision to make the grid itself tensor-shaped**, rather than keep bolting GPU onto a per-cell engine.

---

## 1. What "GPU-native" means for quilt — the level argument

### 1.1 The wrong answer: "quilt can use a GPU"

The bolted-on reading is what elephant's `field_math_gpu.py` already does *outside* quilt: a standalone script reads the logs, reproduces the vMF math on CUDA, and reports a speedup. That is a **batch farm**, not a grid. It is correct and valuable and *not* GPU-native — because the engine that owns the cells doesn't know the farm exists. The grid stays an `RwLock<IndexMap>` of individually-addressed cells; the GPU is a visitor that drops in, does math, and leaves. Nothing about the grid's *shape* changes, so nothing about the grid's *scaling* changes.

### 1.2 The three levels, and which one is the point

GPU-native is a claim about **where the tensor lives**, and there are three candidate levels:

1. **Per-cell kernels.** Each cell's evaluator becomes a tiny kernel launch. This is the *finest* grain and the *worst* idea: a cell is a scalar or an `rhai` expression; launch + host↔device copy overhead dwarfs the work by orders of magnitude. This is "GPU-native" in name only — the bolted-on mistake at its maximum granularity. **Reject.**

2. **Batched cell-grid compute.** Cells of the same vector shape are gathered into a batch tensor `[N, D]` (state) or `[N, D, T]` (window/history), and one operation — a vMF fit, an edge delta, an embedding matmul, a hysteresis transition — runs over all N at once. This is the grain at which elephant proved 111.6×, and it is the *correct* primary level. The reactive engine's "mark dependents stale, recompute" loop is unchanged in spirit; only the **recompute** of vector-valued cells becomes a batched op instead of a per-cell loop. **This is the point.**

3. **The ledger as a tensor log.** The deepest version: the cell ledger (today an append-only, hash-chained, double-entry record per cell) becomes the **time axis of a tensor** — all cells' state history laid out as `[N, D, T]` — with the hash chain as a *verification overlay* on top. The working set is the tensor; the seal is the chain. This is not a separate level so much as the *consequence* of level 2 done consistently: if state is a tensor, then state-over-time is a tensor, and the ledger is just the tensor's third dimension plus a proof it wasn't tampered with.

**The answer:** GPU-native quilt = **level 2 as the primary move, level 3 as the natural endpoint, level 1 rejected.** The grid is conceived so that its vector-valued cells are tensor rows, the reactive engine is the dirty-slice scheduler over that tensor, and the ledger is the tensor's time axis with a bit-for-bit seal.

### 1.3 The honest boundary: not every cell is a tensor

This is the point the "everything is a cell" philosophy must not paper over. Eight cell kinds exist, and they do **not** all tensorize:

| Cell kind | Value shape | Tensor-native? |
|---|---|---|
| `value`, `formula` (scalar `rhai`), `io` | scalar / bool / JSON | **No** — per-cell, stays on CPU |
| `api`, `program`, `router` | heterogeneous, side-effecting | **No** — I/O bound, not compute bound |
| `listener` | trigger / propagation | **No** — graph walk, not tensor |
| `sensor` / **`field`** (room dials) | `vector[D]`, `D = 7` | **Yes** — the elephant seam |
| `vector` / embedding / vector-store | `vector[D]`, `D = 384…768…4096` | **Yes** — the RAG seam |

GPU-native quilt is therefore **not a rewrite of the whole engine**; it is a **tensor lane** that runs *beside* the scalar reactive engine. The scalar 95% of a sheet (a bilge pump's 5 cells, a router's rules) never touches the GPU and shouldn't. The tensor 5% (a room's field, a corpus's embeddings, a ledger's delta/imbalance series) is where the scaling lives. The design that respects this is the one that scales; the design that ignores it is a rewrite that loses the spreadsheet's ergonomics for nothing.

---

## 2. The three scaling axes — and which one the fleet actually needs

### 2.1 The axes

**(a) Single-grid throughput — many cells on one GPU.** Batch N cells through the *same* op. This is `field_math_gpu.py` verbatim: ~14.5k trailing windows, one CUDA pass, 111.6×. For quilt: 10k `field` cells recompute their μ̂/κ/warmth in one pass when a message lands.

**(b) Grid size — cells as tensor rows, the whole grid is one op.** When the grid *itself* is large, the tensor *is* the grid: embed-all over a corpus is one GEMM; retrieval is `query @ corpus.T`; the whole 8,800-piece `ai-writings` corpus is a single matrix. Here the reactive engine's `O(dependents)` walk is irrelevant — there are no dependents, just one dense batch.

**(c) Distribution — multi-GPU / edge-worker tensor sharding.** Rows (cells) split across devices; cross-shard edges become communication. This is quilt-mesh/quilt-fleet's natural tensor form: shard the cell-tensor, all-reduce the deltas.

### 2.2 Which matters for the fleet's actual use — ranked honestly

1. **(b) Grid-as-tensor — the RAG corpora. FIRST.** `quilt-rag`'s embedder/store/retriever cells are *already* tensor ops (cosine similarity = normalized matmul). The fleet's largest owned objects — 8,800+ pieces of `ai-writings`, 2,786 pre-embedded, `collective-unconscious`'s Vectorize index — are corpora. Embedding, indexing, and retrieval-by-feeling are exactly the shape where "the grid is one batched op" is not a metaphor but a matmul. This is the axis with **live, already-sized data today**.

2. **(a) Batched throughput — the elephant field math. SECOND.** The room-field seam (μ̂, κ, warmth, edge, drift) is proven at 111.6×. It matters for **offline/batch** field computation (tap-night analysis, premise measurement), not live — see §5 for the threshold.

3. **(c) Distribution. LAST, and mostly not soon.** The fleet is **wide, not deep**: many *small* grids (a handful of Tap rooms, each with dozens of cells), not one huge grid. One RTX 4050's 6 GB already holds every field the fleet computes. Distribution buys nothing until a single grid genuinely exceeds one device — and the Cloudflare edge already provides "distribution" in a different, already-paid-for sense: shard by **Worker**, not by GPU. Build (a)+(b) first; (c) is a flag to raise, not a plan to fund.

> **Why the fleet's live use is the weak axis:** The Tap's rooms are small and latency-sensitive; fleet-radio and RAG are large and latency-insensitive. GPU-native wins where the fleet is **batch-shaped** (radio pipelines, RAG corpora, elephant fields), not where it is **interactive** (a live room). The doc returns to this in §5 — it is the honest center of gravity.

---

## 3. Concrete architecture — how quilt-rust changes

### 3.1 The backend layering

Recommend a **three-tier spine with one portable front**:

```
                        ┌──────────────────────────────────────┐
                        │  quilt-tensor  (abstract tensor ops) │
                        │  batched cell ops as reductions /    │
                        │  matmuls / elementwise / gathers     │
                        └──────────────┬───────────────────────┘
             ┌───────────────┬─────────┴──────────┬───────────────────┐
             ▼               ▼                    ▼                   ▼
      ┌─────────────┐ ┌─────────────┐   ┌──────────────────┐   ┌──────────────┐
      │   WGPU      │ │   CUDA      │   │  WebGPU-in-Worker│   │   CPU (rayon)│
      │ (wgpu)      │ │ (cudarc /   │   │  (wasm32 target, │   │  (numpy /    │
      │ Vulkan/Metal│ │  torch ext) │   │   quilt-core-wasm│   │   reference) │
      │ 4050 · mac  │ │ 4050 local  │   │  CF edge Worker  │   │  GOLDEN path │
      └─────────────┘ └─────────────┘   └──────────────────┘   └──────────────┘
```

- **WGPU is the spine.** `wgpu` compiles the *same WGSL shader* to Vulkan (the RTX 4050), Metal (mac), and — critically — **WebGPU**, which runs in a browser/Worker on the edge. This is what makes "GPU-native" compatible with the Cloudflare migration posture: quilt-rust *already* compiles to `wasm32-unknown-unknown` and has `crates/quilt-core-wasm`. **WebGPU-in-Worker is not a new dream; it is the same kernel, already-compilable target.** WGPU is the one layer that covers laptop + mac + edge with a single shader language.
- **CUDA is the local power backend.** The RTX 4050 (6 GB, CUDA + Ollama idle) is the test bench. Two paths exist and both are already half-proven: (i) a torch/`cu130` extension mirroring `field_math_gpu.py` verbatim, or (ii) pure-Rust `cudarc`/`cust` matching the `cuda-ptx-tier.md` `edge_batch` kernel sketch. Prefer (ii) for a self-contained `quilt-gpu` crate (no Python in the deploy artifact); use (i) for the *first experiment* (§4) because it is already written and bit-parity-proven.
- **CPU is the golden fallback and the *oracle*.** The current reference core stays exactly as it is — the per-cell `rhai` evaluator + the serial `vmf_fit`. It is not just the fallback; it is the **bit-parity oracle** every tensor op is gated against (this is the discipline `field_math_gpu.py` and `cuda-ptx-tier.md` both already demand — do not let it lapse into a nice-to-have).

### 3.2 The cell-tensor layout

A grid of **N vector-valued cells × D dials × T timesteps**:

```
current state:        S  = [N, D]          one row per cell, D = 7 (room) or 384 (embedding)
history / window:     H  = [N, T, D]       trailing window, T = cap (64 in elephant)
before/after edge:    Δ  = H[t] − H[t−1]    [N, D] per step
ledger (tensor log):  L  = [N, D, T_all]    full state history, chain-sealed overlay
```

Concretely for the elephant room seam (the fleet's canonical vector cell): a `field` cell is a room whose state is a 7-dial reading (`mood, volume, earnestness, cynicism, joke_landing, panic, presence`). A batch of **R rooms × 64-window × 7 dials** is a `[R, 64, 7]` tensor, and the whole vMF fit + edge + drift computation is the batch farm's `vmf_fit_batch` → `edge_batch` → `ledger_batch` chain, *operating on the cell tensor instead of on log files*.

### 3.3 Which ops become matrix ops

| Op (today, per-cell) | Tensor form |
|---|---|
| normalize readings (zvec) | row-wise `x / ‖x‖₂` — elementwise + a reduction |
| **vMF MLE** μ̂, ρ, κ | `sum / N` (reduction) → `ρ = ‖mean‖` (norm) → `μ̂ = mean/ρ` (scale) → Banerjee init (elementwise) → **Newton on A₇(κ)=ρ** (a 60-iter *batched elementwise* solve with per-element freeze masks — embarrassingly parallel, not a matmul) |
| bootstrap CI (B=200) | advanced-index gather + mean (reduction) |
| jackknife SE(μ̂) | leave-one-out: `(S − xᵢ)/(N−1)` + normalize + reduce |
| **edge delta** `d_mu` | row diff + norm: `‖μ̂_a − μ̂_b‖₂` |
| `d_warmth` (signed valence) | **dot product**: `ŵ · Δ` (matvec) |
| `d_log_kappa`, drift | elementwise `log`, `sqrt(d_w² + d_k²)` |
| **hysteresis transitions** | batched elementwise compare + `torch.where`/`select` (the deadband/NMIN honesty gates become mask tensors) |
| **embedding / RAG retrieval** | **matmul**: row-normalize then `Q @ K.T` — the single most GPU-native thing quilt does |

The reactive *propagation* (which cells are stale) is a **sparse graph walk** and stays on CPU — it is the *schedule*, not the *math*. The engine decides what is dirty; the tensor lane evaluates the dirty vector subset in one batch. This is the clean division: **CPU owns the dependency graph and the schedule; the GPU owns the dense evaluation of vector-valued cells.**

### 3.4 What stays scalar (and must, on principle)

- The **hash chain** stays on CPU/host. SHA-256 is integer math and the seal must be **bit-for-bit** — `cuda-ptx-tier.md` §2 already makes this exact call ("hash-on-GPU only with an exact ryū port"). The tensor is the working set; the chain is a CPU-side seal overlay. Canonical `ryū` float rendering + SHA-256 never enters the fast-math lane.
- Scalar `value`/`formula`/`io`/`router`/`api`/`program` cells never leave the per-cell path.
- The **address** is the primary key, always. A tensor cell is *indexed by its stable id*; the tensor is a storage/exec layout, not a renaming. `quilt get room.field` must still work; it returns a row slice, not a coordinate.

---

## 4. The local test bench — the first GPU-native experiment

**Bench:** RTX 4050 Laptop, 6 GB, CUDA (`torch 2.13.0+cu130` confirmed by `field_math_gpu.py`), Ollama installed and idle. It is enough — elephant's whole 14.5k-window farm ran on it in float64 and only touched a fraction of VRAM.

**The experiment — small, falsifiable, bit-parity-disciplined:**

> **Batch 10,000 synthetic cells through vMF MLE + edge on GPU vs CPU; report speedup *and* bit-parity, and find the crossover.**

Mirror `field_math_gpu.py`'s discipline exactly (it is the fleet's gold standard for this):

1. **Synthetic corpus.** Generate 10,000 rooms, each a 64-window × 7-dial `[64, 7]` field sampled from a vMF with κ drawn across the full regime — `{0.5, 2, 8, 20, 500}`, plus the adversarial cases the farm already encodes: saturated-identical, near-RHOMAX, antipodal-isotropic, exactly-NMIN, rho-just-under-clamp. Same `default_rng(0)` index streams on host so GPU bootstrap draws the *identical* resamples.
2. **GPU path.** `vmf_fit_batch` + `edge_batch` on CUDA, float64, end-to-end (H2D upload + compute + D2H download included).
3. **CPU oracle.** `elephant.vmf.vmf_fit` serial over all 10k windows (cache to disk, the farm's `cpu_reference` pattern).
4. **Gate.** max|Δ| over {μ̂, κ, ρ, warmth, CI, SE, axis_spread} ≤ **1e-6**; saturated-flag agreement exact; invalid windows (isotropic, N<NMIN) flagged identically (NaN, never a fake number). Pass = bit-parity AND identical validity flags.
5. **Measure.** speedup end-to-end; peak VRAM; and — the *new* deliverable — **the crossover point**: sweep batch size 1k → 100k and report where CPU wins (launch/copy overhead) and where GPU wins. The farm already gives the ceiling (111.6× at 14.5k); the quilt experiment contributes the *floor*, which is the number that decides whether the tensor lane is worth it for live grids at all.

**Second, quilt-specific gate (the bridge, one step past elephant):** write the *same* 10k cells as an actual quilt sheet — 10k `field` cells, each a 7-dial vector — and run the scalar reactive engine's per-cell evaluator over them. Assert the tensor lane reproduces the reactive engine's values **bit-for-bit on the vector subset**. This is `field-edge-bridge.md` identity 4 (`imbalance ≡ d_mu` on the unit sphere) generalized: the tensor lane is not a *lookalike* of the grid, it *is* the grid, executed dense. If this gate passes, GPU-native quilt is real; if it fails, the tensor layout has a semantic gap that must be closed before anything else is built.

**What the experiment falsifies:** "the GPU helps at fleet scale." It will almost certainly confirm the *batch* ceiling and *disconfirm* the *live* case — which is the correct, honest outcome, and precisely why it's worth running before anyone rewrites the engine.

---

## 5. Risks & the honest counter

### 5.1 The threshold — where does the GPU actually win?

The fleet's grids are **mostly small**. The bilge pump is 5 cells; the Tap is a handful of rooms; the current engine already evaluates **10,000 pure-value cells in < 1 ms** on CPU (quilt-rust README, measured). Against that, a GPU pass pays: kernel launch (~5–20 µs), H2D/D2H copy, and — the killer — **float64 at 1/32 the f32 rate** on consumer silicon (the 4050's f64 throughput is deliberately crippled; that's why the elephant farm ran f64 *and still* hit 111.6× — the batch was big enough to hide it).

**Threshold (hypothesis, to be pinned by §4):** the GPU wins when a single tick touches **≥ ~1k–5k vector cells with the same op**, or when a **batch/offline job** runs over a large corpus. Below that, CPU reference is faster *and* simpler. The fleet's **live interactive** use is almost all below threshold (latency-bound, small, heterogeneous); its **batch** use (nightly radio pipelines, RAG embed/index/retrieve, elephant field analysis) is above. Therefore:

> **GPU-native quilt is a batch-and-corpus capability, not a latency capability.** It makes the *night* fast, not the *tap* fast. Trying to make the tap fast with a GPU adds latency (launch + copy), not removes it — the tap stays on CPU/CF edge, and that is correct, not a compromise.

### 5.2 What quilt *loses* by going tensor-shaped

1. **Per-cell ergonomics.** A scalar `rhai` formula (`=a + b`) is readable, debuggable, one line. A tensor cell is a *column in a matrix* — `quilt get cell.id` returns a slice, and the "spreadsheet that thinks" becomes a spreadsheet again (a grid, not named addresses). **Mitigation:** the address stays the primary key; tensor is exec layout, not identity. But the *feel* of "every cell is a small live machine" is partly an artifact of per-cell evaluation, and the dense lane does lose some of it.

2. **Debuggability.** A NaN in tensor row 4,213 is a black box; a per-cell evaluator tells you which cell and which input. The elephant farm's answer — **CPU reference as oracle + a standing bit-parity gate in CI** — must become a *permanent contract* (`golden.json` conformance, `cuda-ptx-tier.md` §2), not a one-off script. Every tensor op ships with a CPU golden path or it doesn't ship.

3. **The ledger's append-only grain.** The ledger is append-only and hash-chained — each seal depends on the previous. That is **inherently sequential**, while the tensor wants to be one big parallel write. Real tension. **Resolution:** the tensor is the working set; the chain seals *batches* via a Merkle overlay rather than single `prev_hash` entries — at the cost of the simple, readable "prev_hash" chain model. The seal itself stays CPU-side (bit-for-bit). This is a genuine design cost, and it should be named, not hidden.

4. **Precision vs. speed.** Fast-math f32 breaks bit-parity; f64 restores it but is slow and VRAM-hungry on the 4050. The honest posture is **two lanes**: f32 for throughput where 1e-3 is acceptable (embeddings, ranking, the tensor render), f64 for the golden/parity path (ledger seals, vMF reference). "Innate scaling" via f32 comes *at the cost of* the parity guarantee — a real trade the Captain should ratify, not discover later.

5. **The over-engineering risk, stated plainly.** For a grid that is *mostly small*, a tensor lane is machinery that will be mostly idle. The defense is not to skip it — the fleet already owns the large batch workloads (RAG, radio, elephant) where it pays — but to **gate the lane behind a size check** (only dispatch to GPU when the dirty batch exceeds the threshold), so the small-grid experience is byte-for-byte what it is today.

---

## 6. The Captain's other directive — the grid painting itself

**Directive (context):** local GPU image generation to visualize *"the curvature of situations."*

**The unification:** the cell-tensor is *also* the texture map. A cell-grid **is** an image in waiting — cells are texels, dials are channels, edges are gradients, time is frames. The grid can literally render itself, and "curvature" has a *precise* meaning in the field math that makes this more than a metaphor.

### 6.1 κ is curvature, not a metaphor

In the vMF model the fleet already runs, **κ (the concentration parameter) *is* the curvature of the field**: high κ = a tight, rigid, low-entropy distribution (few ways for the room to be — a *crisis* or a *ritual*); low κ = a diffuse, warm, many-ways field. The elephant seam already reads `κ` per room per window. So "the curvature of a situation" is not something to *invent* for the visualization — it is **already computed** as `κ`, and `d_mu` (the edge) is the *rate of change* of curvature, and the hysteresis transitions are the *inflections*. The visualization directive and the GPU-native directive are the same tensor read two ways.

### 6.2 Two render passes, both from the same tensor

**Pass 1 — deterministic, GPU-native (wgpu fragment shader).** The cell-tensor `[N, D]` → a texture: each cell maps to a position (its row/column spatial axes), its 7 dials map to RGBA + depth/normal channels, `κ` maps to brightness/saturation (curvature = intensity), `d_mu` maps to a glow/edge highlight, `d_warmth` maps to a hot/cold colormap. This is a *copy + shader*, pure wgpu, no diffusion model — the grid painting itself as a heat-map of its own curvature, at 60 fps if asked. This is the *honest*, reproducible layer: the picture is a function of the grid, bit-for-bit.

**Pass 2 — expressive (local diffusion on the 4050, FLUX/SDXL).** Take Pass 1's texture as the **control-net / img2img init** and condition a prompt ("render the room's field as it felt tonight") to produce the atmospheric illustration — the fleet's existing hero-image vocabulary (brass traces, midnight navy, honey amber) over a *correct* curvature base. The AI layer adds the *voice*; Pass 1 supplies the *truth* it must not distort.

### 6.3 Why this unifies the two directives

- The **same cell-tensor** that makes the grid scale (the tensor lane, §3) is the **same tensor** that makes the grid *visible* (the texture, §6). No separate dashboard, no second data model.
- Pass 1 makes "curvature of situations" a **deterministic, GPU-native, testable** artifact — it can be bit-parity-gated like every other tensor op (render the golden `room.field` vector, assert the texel color).
- Pass 2 answers the *expressive* half of the directive using the GPU that is already idle, on the same bench that §4's experiment is designed for — so the visualization work and the scaling work share hardware, tooling, and the parity discipline.

---

## 7. Bottom line (for the Captain)

1. **GPU-native quilt = a tensor lane, not a rewrite.** Shape-tag cell values (scalar | `vector[D]` | `tensor[D,T]`); the reactive engine becomes the dirty-slice scheduler over the vector subset; the ledger becomes the tensor's time axis with a CPU-side bit-for-bit seal. Scalar cells, `rhai`, the address model, and the hash chain all stay exactly as they are.

2. **The fleet's GPU payoff is batch-shaped, not interactive.** RAG corpora (grid-as-tensor, axis b) and elephant field math (batched throughput, axis a) pay now; live Tap rooms stay on CPU/CF edge (correctly). Distribution (axis c) is a flag, not a plan.

3. **Layering:** WGPU as the portable spine (one WGSL shader → 4050, mac, *and* WebGPU-in-Worker on CF edge via the existing `quilt-core-wasm` target), CUDA for local power, CPU as the golden oracle. Everything gated by bit-parity, exactly as elephant's farm already does.

4. **First experiment (§4):** 10k synthetic cells through vMF+edge GPU-vs-CPU, bit-parity ≤ 1e-6, find the crossover. Plus the quilt-specific gate: the tensor lane must reproduce the scalar engine's vector values bit-for-bit. This is cheap (already-written code exists in elephant), falsifiable, and decides the architecture before anyone rewrites anything.

5. **The honest counter (§5):** for mostly-small grids this is over-engineering — so gate the lane behind a size threshold and keep the small-grid path byte-identical. The tensor-shaped losses (per-cell ergonomics, debuggability, the ledger's sequential grain) are real and must be bought deliberately, not discovered.

6. **The visualization directive is the same tensor read two ways (§6):** κ *is* the curvature of a situation; the cell-grid renders itself as a texture (deterministic wgpu pass), and the local 4050's diffusion layer (FLUX/SDXL) turns that true curvature map into the expressive image — unified, not bolted on.

---

### The single most important architectural decision

> **Make the cell value type shape-tagged — `scalar | vector[D] | tensor[D,T]` — and run a tensor lane for the vector subset *beside* the scalar reactive engine, demoting the engine to a dirty-slice scheduler over that tensor while the ledger's hash chain stays a CPU-side, bit-for-bit seal. GPU-native quilt is a lane, not a rewrite.**

Everything else — WGPU-vs-CUDA, which axis first, the threshold, the render pass — follows from this one choice. Get it wrong (rewrite the whole engine, or keep bolting on a batch farm that the engine doesn't know about) and the scaling stays accidental; get it right and the grid's scaling is *innate* — it falls out of the data being tensor-shaped from birth.

---

*Read-only session: no repo files modified, no pushes, no commits.*
