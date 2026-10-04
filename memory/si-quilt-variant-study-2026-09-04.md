# Cross-Variant Quilt Study — QUIL HLS RFC Feeder

Survey of local repos (README + entry points only), Sept 4 2026. Note: **quilt-cell** and **quilt-live-canon** are not cloned locally; **quilt-dpcpp** is an empty clone (zero commits, .git only — the failed-lane remnant).

## 1. Cell/opcode model vs. the Verilog 5+1 (qm_bind/link/effect/view/tick + forget)

| Variant | Cell model | Opcode alignment | Closeness |
|---|---|---|---|
| **quilt-cuda** | device-memory slice `{state, witness_word, lamport, opcode}`; CUDA Graph = compiled LINK set; `cudaGraphLaunch` = TICK | Full explicit 5+1 table in README; FORGET = graph destroy/`cudaFree`. W13 witness (30 trits + 2 marks), warp ballot as L1 law | ★★★★★ most literal mapping |
| **tit-quilt** | cell `{cell_id, kind, value, version, fn, inputs, witness, dirty, cron}`; kinds VALUE/INPUT/FUNCTION/EFFECT/ROOT | BIND/LINK/TICK/EFFECT/**FORGET** verbs named identically; tombstones, witness sets, hot→cold retention | ★★★★★ |
| **svelte-quilt** | Svelte 5 runes; `bindCell/derivedCell/effectCell/witnessed` + `createGraph` | BIND/LINK/EFFECT/VIEW comments right in App.svelte; "the compiler IS the wavefront" | ★★★★ structural, no TICK/FORGET primitives (runtime handles them) |
| **quilt-esp32** | no_std Rust engine, 64 cells/8 deps/cell; `define`+`add_dep`+`set` API; consumes compiled `.qm` rule tables (JSON op-lists: `bind` ops observed) | `.qm` files are serialized opcode programs; verified on hardware (blink, critic-gate 100% replay agreement) | ★★★★ .qm = an existing opcode-level interchange format |
| **quilt-rust** | 8 CellKinds (Value/Formula/Program(rhai)/Sensor/Api/Listener/Router/Io), YAML sheets, MCP-native | Reactive DAG semantics but no named opcode ISA; rhai replaces EFFECT; no FORGET | ★★★ same substrate, different vocabulary |
| **mist-quilt** | Durable Object sheet, `kind: value|formula`, TS evaluators (no eval), /predict ghost states | VIEW/DAW/predict ≈ VIEW + speculative TICK; no BIND/LINK surface — cells are code-declared | ★★ implicit |
| **nmea-quilt-cell** | append-only JSONL journal + replayed derived views; single writer, seq monotonic | Not opcode-based: journal/replay model. TICK≈append, VIEW≈replay, but no link graph | ★ (deliberately: one cell, not a VM) |
| **quilt-cell** (GitHub) | JS lib, 16-dial Q1.15 vectors, FNV-1a 64-bit state hash, byte-exact cross-language | cell value format, not opcodes | ★ |
| **quilt-live-canon** (GitHub) | 7 ops: NAVIGATE, CONFLUENCE, LINEAGE, GHOST, TICK, CLAIM, DRILL | TICK shared; others are domain verbs on the canon fabric | ★★ a *read-model* dialect |
| **quilt-dpcpp** | empty | — | — |

## 2. Existing textual surface languages (QUIL-like)

- **`.qm` (quilt-esp32, quilt-vm-c lineage)** — the real precursor: JSON op-lists `{format:"qm",version:1,organism, ops:[{op:"bind",target,value}]}`. Compiled rule tables running on metal. Machine interchange, not human-authored HLS.
- **`.cell.yaml` (quilt-esp32 semantic-tower)** — the closest thing to HLS intent: natural-language-ish YAML describing io/raw/rendering/snap/tick with the "language-below-the-horizon lemma" (C target is an optimization, not a specification).
- **YAML sheets (quilt-rust / TS canonical quilt)** — grid of named cells, kinds, rhai/JS formula bodies. De facto authoring format across the fleet.
- **tit-quilt verbs** — a CLI/MCP *protocol* language (BIND/LINK/TICK as commands), not a text file format.
- Nothing is named QUIL; no unified grammar exists. That's the RFC's gap.

## 3. Convergence recommendation — what QUIL must include

**In scope (unify what already converges):**
1. Five core statements mapping 1:1 to the ISA: `bind`, `link`, `effect`, `view`, `tick` — plus `forget` (tombstone semantics, per tit-quilt's provenance law: never delete, hash-survives).
2. **Cell declaration block** = the `.cell.yaml` shape (io, kind, unit, prefilter, tick cadence) — it's the most evolved human surface.
3. **Expression body per cell** — dialect-pluggable (rhai / JS / C / integer micro-units), with a purity requirement separating `view`/formula from `effect`.
4. **Witness as a first-class, optional annotation** (W13 trit-word, or frozenset{(cell,version)} — pick one canonical semantic, two encodings: compact-word for metal, set for hosted).
5. **Determinism envelope**: integer/basis-trick arithmetic profile for byte-exact replay (esp32 critic-gate precedent), plus a float profile for hosted runtimes.
6. Serialization target: `.qm` JSON (or its successor) as the compiled object format — QUIL text → .qm → any backend (Verilog, ESP32, CUDA graph, Svelte runes, rhai).

**Out of scope:**
- Domain read-model verbs (NAVIGATE/CONFLUENCE/DRILL — Live Canon dialect; a *library* over QUIL, not the language).
- Journal/replay persistence policy (nmea model) — orthogonal infra; QUIL only needs `tick` to be replay-pure.
- Engine-specific kinds (Api/Router/Listener in quilt-rust) — express as effect cell + adapter, keep the core at 5+1.
- UI/DAW/viewer concerns (mist-quilt SHEET/DAW are consumers).
- CRDT/federation merge semantics — reference, don't normatively specify yet.

## 4. Top 5 surprises / trails for the wheel

1. **CUDA Graph == compiled LINK set, literally** — quilt-cuda proves the quilt cell-graph is the same data structure as `cudaGraph`; a QUIL→cudaGraph backend is nearly free, and warp ballot = witness OR-union in one instruction.
2. **`.cell.yaml`'s "language-below-the-horizon lemma"** — the spec deliberately omits the target language; that's the correct design principle for QUIL's pluggable expression dialects. Book it as RFC §design-principle.
3. **Integer-only critic gate hit 100.0000% agreement over UART on 500 vectors** — the determinism envelope is already proven cross-device; QUIL's integer profile can be normative, not aspirational.
4. **tit-quilt's tombstone law ("nothing witness-referenced is ever destroyed")** is the missing 6th opcode's real spec — FORGET isn't deletion, it's hash-preserving retirement. The Verilog +1 and tit agree independently.
5. **Svelte 5 runes ARE a quilt frontend** — the compiler's reactivity graph already implements the wavefront; a QUIL→Svelte codegen lane would make every web variant free. Also: quilt-dpcpp is an empty husk (0 commits) — the dpcpp/SYCL GPU lane never started; worth either booking as deliberate gap or reviving.
