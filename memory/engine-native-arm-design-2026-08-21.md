# ENGINE-NATIVE ARM (G2) — Design Addendum

**Filed: 2026-08-21. Design only — STRICT read-only. Nothing generated,
nothing run against registered data, no repos modified.** This is the
separate addendum the wave-3 generation-corpus plan (`wave3-generation-
plan-2026-08-21.md` §1.2 Arm 2, §3 Gap G2) pre-registers for the
*engine-native* arm: the riverbed forward model rewritten so the forward
model itself is tensor-shaped.

Grounding: `wave3-generation-plan-2026-08-21.md` (Arm 2 + Gap G2 + the
S0–S6 sequence), `quilt-gpu-native-design-2026-08-21.md` (the tensor-lane
thesis: shape-tagged `scalar | vector[D] | tensor[D,T]` cells, dirty-slice
scheduler, WGPU spine → CUDA local → CPU golden fallback, ledger as tensor
time axis with CPU hash seal), `foundation-synthesis-2026-08-21.md` (the
skew-product axioms, q-rule, coordinate firewall, temperature axis),
`riverbed_generator.py` (the scalar forward model as it exists), and code
inspection of `field_math_gpu.py` / `encoder_gpu_scale.py` (the elephant
CUDA batch farm — the 111.6× bit-parity precedent), `vmf.py`,
`tapnight.py`, `e2_nights.py` (all read-only, today).

---

## 0. The one-sentence thesis

The riverbed generator's forward model is already a tensor that the scalar
code *unfolds* with Python loops — `room_path` is a `[T, 7]` room tensor,
the reader fiber is a `[R, T, 7]` skew-product contraction, and the between-
night OU is a `[R, 7]` AR(1). The engine-native arm makes the tensor the
**primary object**: μ(t), κ(t) over all 21 readers × T speaks at once as
batched tensor ops, the skew-product fiber as a broadcast-add + row-norm
contraction, generation as one matrix pipeline whose shape-tagged cells are
the *same* cells quilt's tensor lane and elephant's batch farm consume. It
is a **lane, not a rewrite** — the tensor is the working set; the JSONL is
a lossless unfold of it; the CPU-golden path is the oracle every tensor op
is gated against, exactly as `field_math_gpu.py` already does.

---

## 1. What the arm is

### 1.1 The reframe

Arm 1 (the direct vMF sampler, `riverbed_generator.py`) is the *statistical*
certificate: it plants the truth (μ(t) = w(t)·Ŵ + √(1−w²)·e⊥(t), the
persona-anchored deviations) and lets the registered apparatus recover it.
Arm 2 (this arm) is the *engine-native* certificate: the same forward model,
but the **forward model itself is tensor-shaped**, so the generated corpus
is the **calibration instrument in its tensor form** — not a JSONL blob that
quilt/elephant must later re-parse and re-tensorize.

The reason this matters is stated in the quilt thesis and replayed here for
the elephant seam: the corpus's *value* to the fleet is as a field sample
path. If it is born as `[N_α, N_nights, R, T, 7]` tensors, then:

- **quilt's GPU lane** receives it directly as `field` cells (`vector[7]`)
  with the ledger as the tensor's time axis (quilt thesis §3.2);
- **elephant's CUDA batch farm** receives it directly — `vmf_fit_batch`,
  `edge_batch`, `ledger_batch` in `field_math_gpu.py` are *already written*
  and bit-parity-gated against `vmf.py` (111.6× at ~14.5k windows);
- **the α-sweep is one tensor**, not five separate corpora.

The scalar generator *can* produce the bytes; only the tensor arm can
produce the bytes *and* the co-computable tensor they already are.

### 1.2 What is in scope, and the honest boundary

The arm tensorizes the **field math** of the forward model — the room base
orbit, the reader fiber, the skew-product contraction, the OU between-night
drift, the trailing-window smoothing, the per-reader fit. It does **not**
tensorize the TapNightSession's *text* dynamics (charisma pull, vibe
relaxation, `speak()`'s `delta += s·(vibe − raw)` loop) — those are the
scalar engine's job, and Arm 2's "text→dial→reading" hard version (the
persona-resampling map on `e2_nights.py:121-125` constructor inputs,
collapse = per-night warmth-conditioned persona redraw) is a **scalar-engine
concern that the tensor arm *feeds*, not replaces**. The α-dose tensor
parameter (§2.4) is precisely the hook the persona-resampling map drives;
the tensor arm does not reimplement persona redraw.

This is the same boundary the quilt thesis draws for its own tensor lane:
the scalar 95% (a bilge pump's 5 cells, a `rhai` formula) stays scalar; the
vector subset (a room's field, a corpus's embeddings) tensorizes. The
riverbed forward model's vector subset is *all* of its math — which is why
the arm is a near-total tensorization of the field math but a **no-op** on
text.

---

## 2. The tensor design

### 2.1 Concrete layout

All dtypes **float64** (generation is the calibration instrument; the CPU
golden path is numpy f64; parity is the contract — see §4). D = 7 (S⁶),
R = 21 (union roster; per-family rosters are masked), T_max = 46 (the
longest family, T4a/T5 = 46 speaks; shorter families zero-pad with a length
mask — the `field_math_gpu.py` `build_events` discipline). N_nights = 9
(frozen `NIGHT_ORDER`), N_α = 5 (the sweep `{0, 0.25, 0.5, 0.75, 1}`).

| Tensor | Shape | Meaning (scalar source) |
|---|---|---|
| `w_room` | `[N_α, T_max]` (α-independent → `[T_max]`) | warmth schedule w(t) — `room_schedule` |
| `k_room` | `[T_max]` | κ(t) — `room_schedule` |
| `mu_room` | `[T_max, 7]` | μ_room(t) on S⁶ — `room_path` |
| `s_lat` | `[T_max, 7]` | latent per-message vMF draws |
| `obs` | `[T_max, 7]` | trailing-W_WIN smoothed observations |
| `dev_anchor` | `[R, 7]` | persona-anchored deviations — `persona_deviations` (firewall-safe) |
| `ou_state` | `[R, 7]` | between-night drift — `generate_night` OU |
| `m_reader` | `[N_α, R, T_max, 7]` | skew-product fiber mean m_R = norm(μ + (1−α)·dev) |
| `x_reader` | `[N_α, R, T_max, 7]` | unit z-space reader draws |
| `eff_reader` | `[N_α, R, T_max, 7]` | dial-space images (lens inverse) |
| `fit_reader` | `[N_α, R, T_max] × {mu,κ,n}` | trailing-W_WIN per-reader fit |
| `presence` | `[R, T_max]` (bool) | entrant late-start mask (G1) |
| `valid` | `[R, T_max]` (bool) | NaN convention (never a fake number) |

Corpus-level: fold `[N_α, N_nights, R, T_max, 7]` when the sweep is one
batch. Size: 5 × 9 × 21 × 46 × 7 ≈ 304k elements ≈ **2.4 MB per f64 tensor**
— trivial against the 4050's 6 GB and far below the farm's already-proven
14.5k-window footprint.

### 2.2 Which ops become matrix ops

| Scalar op (`riverbed_generator.py`) | Tensor form |
|---|---|
| `room_schedule` κ-events (`kappa[t] += 12·exp(−(t−e)/6)`) | elementwise add of a precomputed relaxation kernel `12·exp(−arange/6)` — a `where` + broadcast-add |
| warmth flip (`w[:flip] = base±FLIP_SIZE/2`) | `where(arange < flip, base+h, base−h)` + clip |
| `e⊥` tangent random walk (`e = _unit(e + ORTH_WALK·ξ)`) | sequential recurrence — **prefix-scan** (or the OU conv, §2.3), *not* a parallel map |
| `vmf_sample` (Wood 1994 rejection) | **masked batched rejection** (freeze-mask loop over the "active" draws — §2.5) |
| trailing-`W_WIN` obs (`mean(s_lat[t−W+1..t])`) | **boxcar convolution** (length-8) = cumsum-diff, or a 1-D conv — `field_math_gpu`'s masked-mean pattern |
| skew-product fiber `m_R = norm(μ_room + (1−α)·dev_R)` | **broadcast-add** `[T,7] ⊕ [R,7] → [R,T,7]` + row-norm reduction — the whole fiber is one contraction |
| between-night OU (`st = φ·st + σ·ε`) | **causal exponential-kernel convolution** (§2.3) |
| `_reader_fit_light` / `vmf_fit` (Newton A₇) | `kappa_newton_t` freeze-mask (already written in `field_math_gpu.py`) |
| `vmf_edge` | `edge_batch` (already written) |
| JSONL emission | **row-major gather** — a pure index lookup, lossless (§4) |

The point worth stating plainly: **most of the tensor ops already exist** in
`field_math_gpu.py` (`vmf_fit_batch`, `edge_batch`, `kappa_newton_t`,
`A7_t`, `banerjee_t`). The arm is not new math — it is the *same math*
gathered into the shape-tagged layout and pointed at the *forward* model
(sampling) instead of the *inverse* (fitting). The one genuinely new op is
the **batched vMF rejection sampler** (§2.5); everything else is a re-layout
of proven kernels.

### 2.3 The split-half displacement is a convolution (and so is the drift)

The between-night OU step is the honest answer to "which ops become convs":

```
st_R(n+1) = φ·st_R(n) + σ·ε_R(n+1),   st_R(0) = 0,   ε ~ N(0, I₇)
```

Unrolled over the 9 nights it is a linear recurrence, and by induction
`st_R(N) = Σ_{k=1..N} φ^{N−k}·σ·ε_R(k)` — a **causal convolution of the
innovation sequence ε with the exponential-decay kernel φ^k**. So the whole
between-night OU for all 21 readers across all 9 nights is **one 1-D
convolution** over a `[R, 9, 7]` innovation tensor (an FIR truncated at 9
taps, or an IIR via `scipy.signal.lfilter`/cumsum on CPU, or a `torch` FFT
conv on CUDA). The within-night trailing-window smoothing (`obs`) is the
same idea: a length-8 boxcar conv.

The tangent random walk `e⊥` is also a recurrence, but *nonlinear* in the
reprojection step (`e = _unit(e + ORTH_WALK·ξ)`, ξ re-orthogonalized to
`WARM` and `e` each step). It does **not** close as a clean conv — it is a
sequential scan. The honest call: implement it as a **prefix-scan**
(associative scan / `torch.cumsum`-style loop, or keep it as the one
short-loop step that runs on CPU in the golden path). It is `T_max = 46`
steps — nanoseconds either way; the design does not contort it into a matmul
it isn't. (This is the same honesty the quilt thesis applies to the hash
chain: *some things are sequential, and pretending they aren't is the bug.*)

### 2.4 The α-dose as a tensor parameter

α enters the forward model in exactly one place:

```
m_R(n,t) = normalize( μ_room(t) + (1 − α)·dev_R(n) )
```

As a tensor this is a **scalar** that scales the `[R, 7]` deviation tensor
before the broadcast-add — one number, not a loop variable. But the design's
real move is to promote α to a **leading batch dimension** `[N_α, …]`:

- the room path `μ_room`, `κ_room` is **α-independent** (α enters only
  through the fiber) — so it is shared across the sweep, exactly as the
  plan's G13 pair mode demands ("α enters only through the fiber");
- the sweep `{0, 0.25, 0.5, 0.75, 1}` becomes **one tensor** with a shared
  room path and an α-parameterized fiber — the 2AFC "matched except α"
  guarantee falls out *for free* instead of requiring a special pair-mode
  RNG key (`(pair_seed, family)` vs the per-tag `(seed, zlib_crc(tag))`).

This is the single largest thing the tensor arm gives that the scalar
generator cannot: **co-computation across α** — `d v̂/dα`, the α* where the
REG-1 confound annotation stops being diagnostic (§2 of the plan) — is a
derivative along an existing tensor axis, not an outer loop that re-reads
five corpora.

### 2.5 The vMF sampler: rejection, not reparameterization, not the MLE

The task asks directly: "vMF sampling from the frozen Newton MLE?
reparameterized draws?" The answer is **neither**:

- **Not the MLE.** The Newton A₇ solve is the *fit* (the inverse problem,
  already batched as `kappa_newton_t`). Sampling is Wood's exact rejection
  sampler (`vmf_sample`, the `w·μ + √(1−w²)·ξ` construction) — the forward
  problem. Conflating them would sample from the *estimator's* distribution,
  not the field's.
- **Not reparameterized.** vMF has no reparameterization-trick path (no
  differentiable fixed-noise → sample map), and reparameterization would
  anyway change the distribution and **break bit-parity** with the CPU
  scalar sampler — the one thing the arm must not do (§4).

The correct tensor form is a **masked batched rejection sampler**, the exact
analogue of `kappa_newton_t`'s freeze-mask for the accept/reject loop:

1. **Host pre-generates the RNG streams** — the `(z ~ Beta(m,m), u ~ U[0,1],
   ξ ~ N(0,I₇))` draws — using `numpy default_rng` with the *same* seed
   discipline as the scalar loop, so the tensor path consumes the *identical*
   draws in the *identical* order (`field_math_gpu.py`'s `_boot_idx_for`
   pattern: "the GPU CI is numerically the CPU CI, not a lookalike from a
   different RNG").
2. **One batched accept/evaluate** over all `[N_α, R, T_max]` candidates:
   `accept = κ·w + (D−1)·log(1−x₀·w) − c ≥ log(u)`, elementwise.
3. **Freeze-mask loop**: rejected elements re-draw from the next slice of
   the pre-generated stream; accepted elements freeze; the loop runs until
   the active set is empty (geometrically converging — expected ~1.5–2
   iterations at κ_R = 40, bounded by a hard cap that asserts the cap is
   never hit, mirroring the Newton loop's `for _ in range(60)` discipline).
4. The tangent direction `ξ` is trivially batched (Gaussian + project-⊥-μ
   + normalize — a `matvec` + reduction).

The rejection loop is the **only** place the tensor path is not a single
dense op, and it is the direct analogue of the freeze-mask Newton solve the
farm already proved. It is embarrassingly parallel in the accept/evaluate,
sequentially-convergent only in the re-draw count.

### 2.6 The coordinate firewall survives as seed-ops, not loop state

The plan's honesty guard 3 (§5) is: *branch parameters live in persona/
field-measure space only; nothing computes an offset from a roster mean, a
corpus_sd, or an o/d quantity on the generation side.* The tensor rewrite
must carry this **unchanged**, and it actually gets *safer* in tensor form,
because the legal vs illegal reductions become explicit named ops:

- **Legal (persona/field-measure):** `dev_anchor = DEV_SCALE·_unit(z(vibe_start)
  − mean_pool z(vibe_start))` — the de-mean is over **vibe_start** (persona
  space), not readings. The unit-norm `_unit`. The `SCALE·(eff − CENTER)`
  standardization.
- **Illegal (estimator coordinates):** any reduction over the *reader batch
  of readings*, any `corpus_sd`, any o/d quantity. These exist only on the
  analysis side (`e2_instrument`, `premise_band_movers`).

The arm encodes this as a **whitelist of reduction axes**: the only legal
batch reductions are (a) the persona-pool mean over `vibe_start`, (b)
unit-norm row scaling, (c) the trailing-window boxcar mean (an intra-night
temporal reduction — legal, it is the engine's own windowing), (d) the
`norm` for `_unit`. Any other `mean`/`sum`/`std` over a `readings`-bearing
tensor is a **compile-time lint error** in the tensor module, not a runtime
convention. The RNG seeds become **tensor-ops**: a single host `default_rng`
pre-generates the `[N_α, R, T_max]` innovation stream, keyed by
`(seed, zlib_crc(tag))` exactly as today, and the tensor path *reads* that
stream — it never holds `rng` state in a loop variable.

---

## 3. GPU backend choice

### 3.1 The recommendation, in one line

**CPU (numpy f64) is the golden oracle and the emitter of record; CUDA
(torch f64, the 4050) is the local power backend for the batch sweep; WGPU
is deferred — a declared spine target, not the generation backend.** The
CF Workers path is out of scope for generation entirely.

### 3.2 Why CUDA-local-now, not WGPU, not CF-edge

- **Generation is offline/batch, not latency/edge.** It runs once per
  corpus on the local 4050 (`torch 2.13.0+cu130` already confirmed by
  `field_math_gpu.py`). It never touches CF Workers — 128 MB / 30 s cannot
  hold the corpus tensors nor a 9-night generation, and generation is a
  *calibration-instrument build step*, not a served endpoint. The CF edge
  runs the *analysis* (which is CPU/CF-Worker-bound and already there), not
  the forward model.
- **The bit-parity discipline is already proven for torch f64** in
  `field_math_gpu.py` (111.6×, ≤1e-6 vs `vmf.py`, identical validity flags)
  and `encoder_gpu_scale.py` (3.46×, data-limited). Reusing that exact
  contract is free; porting the sampler to WGSL is not.
- **WGPU (the quilt spine) buys portability to Vulkan/Metal/WebGPU-in-Worker.**
  That portability is *for quilt's live-and-batch tensor lane on the edge* —
  it has zero value for a one-shot local generation job that already has a
  bit-parity-proven CUDA path. The honest quilt thesis itself says: *CUDA
  for local power, WGPU for the portable spine, CPU as the oracle — prefer
  the already-written torch path for the first experiment.*

The one thing the arm *does* adopt from the WGPU recommendation is the
**shape-tagged layout** — the tensors are declared `scalar | vector[7] |
tensor[T_max,7]` from birth, with an op surface small enough (broadcast-add,
row-norm, boxcar-conv, masked-rejection, exponential-conv, freeze-mask
Newton) that a later WGSL port is **mechanical, not architectural**. The
arm writes against a thin tensor-op module whose CPU-numpy and torch-CUDA
backends are interchangeable and whose op names map 1:1 to WGSL kernels.
That is the portability the fleet actually needs — *portable op surface*,
not *portable generation*.

### 3.3 What the CPU golden fallback guarantees

Bit-parity discipline, per the elephant precedent, made explicit for
generation (which is stricter than analysis — §4):

1. **The CPU-golden path is the oracle.** It is the scalar generator's math
   expressed as vectorized numpy tensor ops over the same RNG streams —
   or, more conservatively, the scalar generator itself, unchanged, as the
   reference. Every tensor op ships with a CPU-golden path or it doesn't
   ship (`cuda-ptx-tier.md` §2, quoted by the quilt thesis).
2. **Determinism.** Same seed → same bytes: the manifest's determinism
   re-run (`generate_wave` → temp-dir re-run → `stripped_md5` equality)
   must hold for the tensor path verbatim.
3. **NaN convention.** Invalid rows (isotropic, N < NMIN, masked-out
   entrants before entry) are **NaN, never a fake number** — the batch
   analogue of `vmf_fit` returning `None`. Identical validity flags to the
   CPU path, exactly as `field_math_gpu.py` masks isotropic windows.
4. **f64 throughout, no fast-math.** Fast-math f32 breaks parity; f64
   restores it. The corpus is the calibration instrument; it is f64 end to
   end (the farm ran f64 and still hit 111.6× — the batch hides the 1/32
   f64 rate).

---

## 4. Compatibility contract — the same schema, byte-exact

The arm must emit the **same v:2 T-night JSONL** as `e2_nights.py` /
`riverbed_generator.py`, byte-shape-identical (the self-test §2 of
`riverbed_generator.py` already asserts key-set parity with
`night-T2.jsonl`). The tensor pipeline lands into per-speak JSONL via a
**lossless unfold**, and the only thing that can make it lossy is float
rounding — which is why the byte contract is the whole game.

### 4.1 The unfold is lossless by construction

The emit step is a **row-major gather**: for each speak `t`, the row is
assembled by *indexing* the tensors — `obs[t]`, `eff_reader[:, t]`,
`fit_reader[:, t]`, `x_reader[:, t]` — into the dicts, then `json.dumps
(..., allow_nan=False)`. There is **no arithmetic in the unfold** — no
re-normalization, no re-standardization, no re-fit. Arithmetic lives only
in the tensor ops upstream; the unfold is a pure index lookup, so it is
lossless *iff* the tensor values equal the CPU-golden values.

### 4.2 The byte contract is stricter than the analysis gate

This is the honest, non-negotiable point. `field_math_gpu.py` gates at
**≤1e-6 max abs diff** because its outputs (μ̂, κ, CI, warmth) are
*downstream analysis quantities*. Generation is different: the manifest's
determinism check demands **byte-identical** `stripped_md5`, and byte-
identical JSONL means **bit-identical f64 values** — a last-ulp difference
in one dial can change one `repr` and break the determinism re-run. Torch-
CUDA reductions and transcendental orderings are **not** guaranteed to match
numpy bit-for-bit. Therefore:

**Contract:** the **registered corpus bytes are emitted by the CPU-golden
path** (the vectorized-numpy tensor ops, which reproduce the scalar
generator bit-for-bit because they are the same numpy ops on the same RNG
streams). The **CUDA path is a gated accelerator, not the emitter of
record** — it must reproduce the CPU-golden values to ≤1e-6 (or, where
feasible, 0 ulp) with identical validity flags, and it *proves the tensor
ops are correct and fast*; it does not write the filed bytes.

This is not a cop-out — it is the *same* division `field_math_gpu.py` makes
(CPU reference = oracle, GPU = gated re-derivation), applied to a stricter
artifact. The engine-native *value* — the shape-tagged tensor feeding quilt
and elephant — is delivered by the **CPU-golden tensor path** (G2a, §5),
which is byte-exact by construction. The GPU acceleration (G2b) is the
optional speed layer on top, gated, never the source of record.

### 4.3 Schema deltas that must survive the tensorization

The self-test §2 key-set assertions are the *floor*, carried verbatim:
`session_open` / `speak` / `readers` / `fit` / `edge` / `session_close`
key sets identical to `night-T2.jsonl`; `v:2` flag; `[LO, HI]` bounds;
early speaks `fit=None` (NMIN=10); `reader_fit` `{mu_hat, kappa, n}` with
`n < 3 → None`. The tensor form's `presence` mask (G1) and `valid` mask
(NaN) must land into exactly the field's `readers`-block presence semantics
and the NaN-before-entry convention — these are **mask tensors in the
pipeline, ordinary JSON in the output**, and the unfold must not leak a
masked row as a `0.0` where the field would emit absence.

---

## 5. Sequencing

### 5.1 Where G2 sits (the plan says S6, "separate addendum, 1–1.5 days")

The plan slotted Arm 2 as **S6**, after S1–S5. The recommended refinement
below keeps S6 but **splits it in two** and pulls the first half earlier,
because the tensor layout is a *de-risking asset for the whole pipeline*,
not just an Arm-2 deliverable.

### 5.2 Recommendation: split G2 into G2a + G2b, and time them

- **G2a — the tensor-shaped forward model, CPU-numpy golden, no GPU**
  (shape-tagged cells, the §2 layout, the lossless unfold, byte-exact vs the
  scalar generator). **Build immediately after S1**, not parallel to it.
  *Why after S1:* S1 lands G1 (entrant late-start masks) and G13 (pair
  mode) on the scalar generator — the tensor arm *inherits* those semantics
  as first-class mask tensors and the α-batch. Building in parallel would
  fork the codebase and encode the *broken* "all-roster-from-t=0" semantics
  into the tensor layout. *Why not after S3:* G2a's CPU-golden path is
  byte-exact by construction and cheap (~0.5 day); landing it before S3
  means the α-sweep and 2AFC pair mode (S3's hard part) can be *run* as one
  batched tensor rather than five corpora + a pair-mode hack.
- **G2b — the CUDA/WGPU acceleration layer**, gated against G2a's CPU-golden
  bytes. **Build after S3**, once the registered corpora exist as the golden
  reference to gate against. This is the `field_math_gpu.py` pattern applied
  to the forward model: an optional speed layer, never the emitter of
  record. It can even be skipped if the CPU-golden sweep is already fast
  enough (it is — minutes of compute; the farm's *analysis* was the 14.5k-
  window grind, not generation).

Net effect on the plan's S6: G2a folds into the S1–S3 window (after S1),
G2b remains the true "S6" (1 day), and Arm 2's own registration addendum
(the persona-resampling map) is a **third** piece, still last, still its own
registration — because it is the scalar-engine text→dial→reading work that
G2's field-math tensorization feeds but does not perform.

### 5.3 What it unlocks that the scalar generator can't

1. **The α-sweep as one tensor** (shared room path, α-parameterized fiber) →
   the 2AFC "matched except α" guarantee is structural, not a special-case
   RNG key (G13's hack disappears).
2. **Co-computation across α** — `d v̂/dα`, the α* where the REG-1 confound
   annotation stops being diagnostic (plan §2) — is a derivative along a
   tensor axis, answering the calibration-curve question directly.
3. **Shape-tagged cells feed quilt's tensor lane** — the generated corpus's
   `field` cells are `vector[7]`, the ledger is the time axis; quilt
   consumes the tensor, not a JSONL it must re-tensorize.
4. **Elephant's batch farm is reused verbatim** — `vmf_fit_batch` /
   `edge_batch` are the arm's fit/edge ops, closing the loop with the
   111.6× precedent on the *forward* problem.

---

## 6. Risks & guardrails

1. **RNG-stream corruption (the biggest).** Batched rejection and vectorized
   reductions can consume the RNG in a different order than the scalar loop
   → a *different* sample path (same distribution, different realization) →
   determinism re-run breaks and cross-corpus "matched except α" silently
   dies. **Guardrail:** host pre-generates the full `[N_α, R, T_max]`
   innovation stream keyed by `(seed, zlib_crc(tag))` exactly as today; the
   CPU-golden tensor path reproduces the scalar loop's *draw order* (or the
   scalar generator itself is the oracle); a standing byte-identity gate
   runs every commit.
2. **NaN-convention corruption.** Batched `normalize`/`mean` over zero-padded
   or masked rows yields `0/0` → NaN or a fake `0.0`. **Guardrail:** mask →
   NaN (never a fake number); validity flags identical to CPU; the
   `field_math_gpu.py` isotropic/N<NMIN masking verbatim. The self-test
   asserts no masked row leaks as `0.0`.
3. **Entrant-mechanics regression (G1).** The tensor `presence` mask must
   reproduce the *fixed* G1 semantics (entrants absent from `readers` before
   entry), not the current broken "all-roster-from-t=0". **Guardrail:** G2a
   is built only after G1 lands; the entrant mask is a first-class tensor
   asserted against `e2_instrument.logged_readings` presence semantics.
4. **Byte-exactness vs numerical parity.** The ≤1e-6 analysis gate is
   *not* strong enough for a byte-identical corpus; torch-CUDA last-ulp
   drift would break the determinism re-run. **Guardrail:** CPU-golden path
   is the emitter of record (byte-exact by construction); CUDA is a gated
   accelerator, never the source of the filed bytes (§4.2).
5. **Coordinate-firewall erosion.** A batched "de-mean" could silently
   compute a roster-mean-of-readings or corpus_sd (o/d quantity) on the
   generation side — the exact contamination the firewall bans.
   **Guardrail:** the whitelist of legal reduction axes (§2.6); any other
   reduction over a readings-bearing tensor is a lint error; a CI check
   asserts no o/d/corpus_sd quantity appears in the generation tensors.
6. **Over-engineering.** For a 6-corpus, 54-night, minutes-of-CPU workload,
   a GPU rewrite is machinery mostly idle. **Guardrail:** the value is the
   *shape-tagged layout* (G2a), not the speed (G2b); G2b is gated behind a
   size check and is optional; the small-corpus path stays byte-identical
   CPU-golden.
7. **Scope creep into the scalar engine.** The arm tensorizes the *field
   math*; Arm 2's real difficulty (the text→dial→reading persona-resampling
   map) is scalar-engine work. **Guardrail:** the α-dose tensor parameter is
   the *hook* the persona map drives; the arm does not reimplement persona
   redraw, charisma pull, or vibe relaxation — those stay in `tapnight.py`
   and the persona-resampling addendum owns them.

---

## Provenance

- Read (read-only): the wave-3 plan, the quilt GPU-native design, the
  foundation synthesis, `riverbed_generator.py` (full), `field_math_gpu.py`
  (§header/`vmf_fit_batch`/`kappa_newton_t`/`build_events`), `vmf.py`
  (constants/`zvec`/`windowed`), `e2_nights.py` (`run_night`, constructor
  inputs), `tapnight.py` (`TapNightSession`, `speak`, `_reader_fit`).
- No files outside this document were written; no generation, no analysis,
  no commits.
