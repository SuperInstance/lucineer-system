# Scout Digest — slackwater-lattice & related repos

**Date:** 2026-09-29 · **Scout:** slackwater-scout (fleet lane) · **Mode:** read-only, 12-min box
**Directive (Casey, 18:38):** "think about SuperInstance/slackwater-lattice and related repos too — these are seed for expansion ... create and evolve packages and deployments and releases where ready"

**Method:** shallow clones to `/home/eileen/scratch/` (ext4); inspected manifest + README + CI + API; ran each test suite locally; probed PyPI / crates.io / npm for the *actually published* version vs. the manifest version. No repo modified, nothing published, nothing pushed.

---

## 1. slackwater-lattice
**(a)** Exact-integer geometry on the Eisenstein A₂ hexagonal lattice — Eisenstein arithmetic, collision-checked build placement, A* pathfinding on the 6-neighbor graph, plus a Lua port for Roblox.
**(b)** Manifest `0.1.0`; **PyPI `slackwater-lattice` 0.1.0 live (HTTP 200, releases `['0.1.0']`)**. README badges accurate. Local: **127 passed**.
**(c)** Already released. Next release: bump `pyproject.toml` **and** `slackwater_lattice/__init__.py` (`__version__`) together → `uv build && twine upload dist/*`
**(d) Expansions:**
1. **Projection layer.** New `slackwater_lattice/genome.py` → `to_genome(points) -> dict` (nodes/edges/rings/hex_line runs) so a fabric genome is renderable and ledger-diffable. 1 module + 1 test file.
2. **Fleet ledger adapter.** New `slackwater_lattice/ledger.py`: Eisenstein coord → receipt key (`routing_key`, book/replay helpers). Feeds the i2i lane; ~120 LOC.
3. **Export the hidden geometry API.** `geometry.py` ships `hex_line`, `flood_fill`, `hex_ring`, `bounding_points`, but **none are in `__init__.__all__`** — real public-API gap. Edit `slackwater_lattice/__init__.py` only, zero new code.

## 2. hex-lattice-explorer
**(a)** Single-file canvas web tool (`index.html`) rendering the A₂ Eisenstein lattice with Pythagorean48 direction overlays and hover inspection.
**(b)** No manifest, no package — nothing to publish; a static deployment. CI exists; no tests. AGENT.md marks it an "ensign" room with a `memory/` journal.
**(c)** Not a package. Deploy = enable GitHub Pages (main / root); `index.html` is self-contained, no build.
**(d)** 1. **Render the fabric genome** — consume `to_genome()` JSON, add `renderGenome(genome)` in `index.html`. The projection layer, visually. 2. **Ternary dial overlay** — color nodes by {-1,0,+1} from ternary-lattice. 3. **Ledger receipt pins** — permalink markers per booked receipt on lattice coords.

## 3. base60-lattice
**(a)** TypeScript Base-60 navigational lattice — 360° bisection/trisection interlacing, 3-4-5 walks, hex tiling, compass rose, and `LatticeStamp` (sexagesimal time → lattice coords).
**(b)** Manifest `1.0.0`, but **npm 404 — unpublished.** Tests **466 passed / 0 fail** (only after `npm i tsx`; not runnable as-shipped). `main` points at raw `src/index.ts` → would ship unbuilt TS.
**(c)** Fix `package.json` (`"files":["dist"]`, `main`/`types` → `dist/`, `prepublishOnly: npm run build`, move `tsx` deps→devDeps) → `npm run build && npm publish --access public`
**(d)** 1. **A2 routing adapter** — new `src/hex-routing.ts`: axial ↔ Eisenstein (a,b) so base60 and slackwater share one neighbor graph. 2. **Ternary dial field** — new `src/dials.ts`: 3-state dials per hex + edge transitions. 3. **Ledger time gate** — extend `latticeStamp.ts` (`bucketKey`/`latticeMatch` already exist) with `bookWindow()`.

## 4. ternary-lattice
**(a)** Rust Z₃ lattice ops — vector add, inner product, matrix/vector & matrix/matrix multiply, seeded sampling, LWE sample, Hamming weight. Post-quantum-flavored.
**(b)** Manifest `0.1.1`; **crates.io max_version `0.1.1` (0.1.1, 0.1.0) — released, in sync.** Tests 17 unit + 1 doc **all pass**, zero deps.
**(c)** Already released. Next: bump `Cargo.toml` → `cargo publish`
**(d)** 1. **Ternary dials** — new `src/dials.rs`: `Dial{state:i8}` step/rotate/deadband + `quantize(f64)->i8`. 2. **Ledger hash** — new `src/ledger.rs`: deterministic Z₃ inner-product digest of a receipt body → tamper-evident gist. 3. **A2 embedding** — project small vectors onto Eisenstein neighbors (bridge to slackwater).

## 5. penrose-lattice
**(a)** Penrose tilings as spectral graphs — Fibonacci substitution, inflation/deflation symmetry, Farey sequences.
**(b)** Manifest `0.1.0`; **crates.io `penrose-lattice` 0.1.0 published, in sync.** Tests **21 passed**. ⚠️ **Binary-only** (`src/main.rs`) — the published crate exposes **no library API**, so nothing can depend on it.
**(c)** Split `src/main.rs` → `src/lib.rs` (public API) + thin `main.rs` CLI. Since it's already published this is a *0.2.0* job → `cargo publish`
**(d)** 1. **Penrose zoom API** — expose `inflate(tiling, steps)` / `deflate(...)` in `lib.rs` so zoom levels are addressable (LOD primitive). 2. **Genome projection** — emit the same `to_genome()` JSON shape as slackwater → one renderer, two geometries. 3. **Zoom→ledger key** — stable key per (tiling, inflation level, tile id) → a zoomed view becomes a receipt coordinate.

## 6. crystal-lattice
**(a)** Rust crystallography structures — `UnitCell`, `BravaisType`, `Miller`, `Defect`/`DefectType`, `SymmetryOp` (compose, order, determinant).
**(b)** Manifest `0.1.0`; **crates.io 404 — NOT published.** Tests **57 passed**, zero deps. Most complete *unshipped* crate in the set.
**(c)** Nothing structural needed → `cargo publish` (optionally `cargo package --offline` first to validate).
**(d)** 1. **Defect → lattice-key projection** — map `Defect` positions to A2 coords → defects as bookable events. 2. **Symmetry→dedup keys** — use `SymmetryOp::order`/`determinant` to canonicalize positions into equivalence classes. 3. **Miller routing** — `Miller::zone_axis` + `spacing` as plane descriptors for a 3D A2 router.

---

## Ranked release-readiness

| # | Repo | Version | Published | Tests | Blocker | Command |
|---|---|---|---|---|---|---|
| 1 | crystal-lattice | 0.1.0 | ❌ 404 | 57 ✅ | none — code ready | `cargo publish` |
| 2 | base60-lattice | 1.0.0 | ❌ 404 | 466 ✅ | package.json main/files + tsx misclassified | `npm run build && npm publish --access public` |
| 3 | penrose-lattice | 0.1.0 | ✅ binary-only | 21 ✅ | no lib API (lib split → 0.2.0) | `cargo publish` |
| 4 | slackwater-lattice | 0.1.0 | ✅ live | 127 ✅ | none — bump for next | `uv build && twine upload dist/*` |
| 5 | ternary-lattice | 0.1.1 | ✅ live | 17+1 ✅ | none — bump for next | `cargo publish` |
| 6 | hex-lattice-explorer | n/a | n/a (static) | none | not a package | enable GitHub Pages |

## Top-3 PR-sized expansions (target files)
1. **Export slackwater's hidden geometry API** — `slackwater-lattice/slackwater_lattice/__init__.py` (+ tests). `hex_line`/`flood_fill`/`hex_ring`/`bounding_points` work but are unreachable by consumers. One file, no new code, unblocks the projection layer.
2. **base60 → slackwater A2 routing adapter** — new `base60-lattice/src/hex-routing.ts` (+ tests). Axial↔Eisenstein conversion; TS navigational lattice and Python geometry kernel share one graph. Independent, non-breaking, PR-sized.
3. **Penrose lib split for a zoom API** — `penrose-lattice/src/lib.rs` (new) + `src/main.rs` (thin CLI). Turns a binary-only published crate into a depend-able library and makes `inflate()`/`deflate()` the addressable Penrose-zoom primitive.

## Best "seed" candidate
**`slackwater-lattice`.** It is the geometry kernel the whole set orbits: exact integer A₂ arithmetic, zero float drift, already on PyPI, 127 passing tests, and it *already ships a Lua port* — so the same math deploys to Python and Roblox today. hex-lattice-explorer visualizes it; base60 duplicates its hex tiling in TS (a routing/merge target); ternary needs it to project {-1,0,+1} onto neighbors; penrose and crystal both want the same genome JSON shape. Expanding it (genome projection + ledger adapter + exported geometry API) upgrades every sibling at once, and each step is PR-sized.

## Explicit unknowns
- **Published state verified via public APIs only** (PyPI/crates.io/npm JSON), not by downloading artifacts. penrose/ternary confirmed published; **crate contents not diffed against local HEAD** (clones were `--depth 1`) — source drift unmeasured.
- **base60 tests ran only after a live `npm i tsx`** — as-shipped (no network / frozen lockfile) the suite is non-runnable; fresh-runner CI behavior not observed.
- **No CI run history checked** (no `gh run list`); "CI exists" ≠ "CI green". README badges treated as claims, not evidence.
- **hex-lattice-explorer has no test surface** — no automated check can confirm it renders.
- **Publish permissions not probed** — whether the org/token may publish these crates/packages is unknown; only "not yet published" is established.
- LICENSE files present in all six repos, but not compared to each manifest's declared license string.
- Snapshot taken at one moment; repos are live and may have moved during the window.
