# New Repo Docs + Images Work Plan — 2026-08-20

**Scout by:** subagent (dsf-newrepo-docs-scout) · **Time:** ~15 min · **Read-only on all repos; only this file written.**

Captain's directive: *"all our new repos like SuperInstance/quilt-cell-bridges need more images and documentation."*

---

## TL;DR

- **`quilt-cell-bridges` is GitHub-only** — exists at `github.com/SuperInstance/quilt-cell-bridges` (created 2026-08-20, pushed today) but is **NOT cloned in /home/eileen/projects/** (it lives next to `quilt` and `quilt-rust`, which ARE local). Needs cloning before work.
- **Zero images in the entire quilt-cell-bridges repo.** Good bones (65-line README, 7 live bridge scripts, 3-view model) — but no hero, no diagrams, no docs/ folder.
- The **quilt family itself is already in great shape** (quilt: 1205-line README + hero-grid.jpg + cell-types.jpg + docs/; quilt-rust: 984-line README + hero-cells.jpg + cell-types.jpg + splash.png + docs/). They need polish, not rescue.
- ~25 other repos born Aug 13–20; most have READMEs but many lack images. There's a **central art pipeline** at `/home/eileen/projects/readme-art-drafts/` (FLUX-2-max / SDXL generators, `gallery-*.jpg` output, LOCAL-GEN.md) — image work should flow through it, then ship into repos.
- **Ready-made assets already exist** for the quilt family: `readme-art-drafts/gallery-quilt.jpg`, `reference-quilt-cells.jpg`, `quilt-calm*.jpg`, `quilt-ts-flux-deck.jpg`, `slot-quilt.jpg` — quilt-cell-bridges can lift its hero/diagrams from these before commissioning new art.

---

## Repo Inventory (young cohort, first commit ≥ 2026-08-13 + quilt family)

| Repo | First commit | README | Docs | Images | Priority | What to add |
|------|-------------|--------|------|--------|----------|-------------|
| **quilt-cell-bridges** (GitHub-only) | 2026-08-20 | ok (65L) | ❌ none | ❌ **0 images** | **P0** | Clone locally; hero image, architecture/3-views diagram, per-bridge docs, gallery, usage deep-dive. Full spec below. |
| **quilt** | 2026-08-17 | good (1205L) | ✅ architecture, comparison, harness-guide, manifesto | 2 (hero-grid.jpg, cell-types.jpg) | P1 | Wire in gallery-quilt.jpg; landing page polish; per-package README check (cli/core/mcp/tui). |
| **quilt-rust** | 2026-08-17 | good (984L) | ✅ c-abi, cell-ledger, codespace-cortex, compat-contract | 3 (hero-cells.jpg, cell-types.jpg, splash.png) | P1 | Same treatment; `field-edge-bridge` crate README is 605B (poor) — expand or fold into parent. |
| **superinstance-ai** | 2026-08-18 | **poor (11L)** | ❌ | 2 (reef-hero, luciddreamer-hero) | **P1** | It's the front door of superinstance.ai — expand README into real doc (structure, deploy, demos list). |
| fleet-gateway | 2026-08-13 | good (513L) | ❌ | 1 (hero_001.jpg) | P2 | Architecture diagram (it's the fleet's spine — worth a mermaid or FLUX diagram). |
| fleet-jepa-midi | 2026-08-13 | good (704L) | ✅ 3 docs | 2 (hero.png, loss_curve.png) | P2 | Minor: gallery image; diagram of training loop. |
| fleet-memory | 2026-08-13 | ok (461L) | ❌ | 1 (hero_001.jpg) | P2 | `readme-art-drafts/drafts/fleet-memory-hero.jpg` exists — ship it in; diagram of memory flow. |
| fleet-embed | 2026-08-13 | ok/thin (89L) | ❌ | 1 (hero.jpg) | P2 | Doc surgery: quickstart, API, diagram. `gallery-fleet-embed.jpg` exists. |
| fleet-ensemble | 2026-08-13 | good (505L) | ✅ director-design, instrument-agent-design | ❌ **0** | P2 | **Needs hero + conductor/instrument diagram** — top image gap among fleet-*. |
| fleet-audio | 2026-08-13 | ok (153L) | ✅ feel-pulse | 1 (feel-pulse.png) | P2 | Minor polish. |
| fleet-cns-v3 | 2026-08-13 | ok (152L) | ❌ | ❌ **0** | P2 | Needs hero + topology diagram. |
| fleet-rooms | 2026-08-18 | ok (113L) | ❌ | 1 (hero-keel.jpg) | P2 | `gallery-fleet-rooms.jpg` exists — ship in. |
| plainsong | 2026-08-17 | good (523L) | ✅ agents, architecture | 3 (hero-musicbox, 2 SVG diagrams) | P2 | Already strong; gallery-plainsong.jpg available. |
| plainsong-mcp | 2026-08-14 | ok (121L) | ✅ ensemble, mcp | 1 (hero.jpg) | P2 | Minor. |
| plainsong-worker | 2026-08-13 | ok (381L) | ❌ | ❌ **0** | P2 | Hero image + worker-flow diagram. |
| tapscript-worker | 2026-08-13 | ok (381L) | ❌ | ❌ **0** | P2 | Hero image + pipeline diagram. |
| elephant | 2026-08-17 | good (500L) | ✅ api-reference, avatar-rounds, bridges | 1 (hero.png) | P2 | gallery-elephant.jpg exists; add avatar diagram. |
| elephant-sim-worker | 2026-08-20 | thin (78L) | ❌ | ❌ 0 | P2 | Doc surgery + hero. |
| ideation-games | 2026-08-17 | ok (53L) | ✅ docs/ (empty-ish) | ❌ **0** | P2 | README exists now (scout noted it missing earlier); needs hero + technique-family diagram. |
| wesley | 2026-08-18 | ok (55L) | ✅ architecture | ❌ **0** | P2 | gallery-wesley.jpg exists; needs hero + growth-loop diagram. |
| tap-gamenight | 2026-08-18 | thin (24L) | ❌ | 2 (poster, radio) | P2 | Expand README; more screenshots of the game. |
| mist-game | 2026-08-19 | ok (100L) | ❌ | 1 (logo.svg) | P2 | Screenshots of the game itself. |
| ternary-rom | 2026-08-19 | ok (230L) | ✅ docs/ (thin) | ❌ **0** | P2 | Hero + ternary layout diagram. |
| zeroclaw-dissertation | 2026-08-19 | thin (34L) | ❌ | ❌ 0 | P2 | Probably personal/private — confirm before investing. |
| tap-frontend | 2026-08-08 | — | — | — | P3 | Outside 2-week window; check later. |

**Also noted:** repos born Aug 1–12 (the mass-init cohort — lucineer-*, slackwater-*, roblox-*, cns-*, study-*) mostly already have hero art from the earlier campaign (see `gallery-*.jpg` in readme-art-drafts). Not in scope for this pass.

---

## P0 SPEC — quilt-cell-bridges

**What it is (honest one-paragraph):** A bridge-porting repo that takes pre-Quilt SuperInstance systems — vessel-agent-system (F/V EILEEN's digital twin), chart-room (four panels, one truth), slackwater-tminus (temporal coordination), hermes-home (Hermes's runtime), plus spatial-registry, grand-pattern-rs, spline-spectral — and exports each as a Quilt cell graph (.qzt file). Every bridge is a 4D cell graph (3D space + time) rendered three ways by 3-View Studio: TOP (spatial, openCPN-style bathymetry), FRONT (signals, TimeZero-style engineering panel), SIDE (time, DAW-style timeline). One file, three openers. Roadmap adds wesley, othismos-reef, ternary-fleet-packing, provenance-log, colony-cell, quilt-ai, quilt-rag. It's the migration story of the whole 300-repo ecosystem into the cell model — the fleet's bridgehead.

**Gaps:** no hero image, no diagrams, no docs/ folder, no per-bridge pages, README stops at one usage command, no gallery/screenshots of the discovery page or 3-View Studio renders.

### Actions (in order)
1. **Clone it locally** — `git clone git@github.com:SuperInstance/quilt-cell-bridges.git /home/eileen/projects/quilt-cell-bridges` (it's absent from the fleet dir).
2. **Hero image** — generate via FLUX-2-max (DeepInfra) or lift `readme-art-drafts/gallery-quilt.jpg` / `reference-quilt-cells.jpg` as an interim. Store at `assets/images/hero-bridges.jpg`. **Prompt (verbatim, for FLUX-2-max):**
   > "A dark maritime cybernetic quilt viewed from above, dozens of irregular glowing cells tessellated into one grid, each cell a different ship instrument panel — one showing a bathymetry chart, one a radar sweep, one a four-panel engineering console, one a DAW timeline — cells joined by brass bridge-rivets and thin copper conduits, deep navy hull background, foam-white and brass accents, teal and amber indicator lights, soft volumetric glow, cinematic wide concept art, high detail"
3. **Architecture diagram** — "one file, three openers" diagram: a single .qzt cell graph with three render panes (TOP/FRONT/SIDE) labeled openCPN / TimeZero / DAW style. Either FLUX-2-max image or a clean SVG (mermaid acceptable) at `docs/architecture.md`.
4. **README section list (rewrite order):**
   - Hero image + one-line pitch ("Port the 300-repo SuperInstance ecosystem to Quilt cells")
   - Why this exists (systems were already expressing the cell model before Quilt existed)
   - Quickstart (clone → `python3 vessel_to_quilt.py --out /tmp/eileen --duration-min 30` → open cell-bridges.html)
   - Bridge table (keep; add status badges per bridge: live/ported/planned)
   - The 3-views model (keep, add diagram)
   - Per-bridge mini-docs links (docs/bridges/vessel.md, chart-room.md, …)
   - Gallery (screenshots of discovery page + 3-View Studio renders)
   - Roadmap (keep "Coming next", add links to source repos)
   - License (MIT)
5. **docs/ folder to add:**
   - `docs/architecture.md` — bridge format (.qzt), cell graph anatomy, 3-view rendering contract
   - `docs/bridges/*.md` — one per bridge: source repo, what it is, what the cells mean, cell count, example output
   - `docs/adding-a-bridge.md` — how to port a new system (the template future bridges follow)
6. **Screenshots** — capture actual renders from `superinstance.dev/cell-bridges.html` and `three-view-studio.html?load=vessel` into `assets/screenshots/` (real beats generated for this one; the 3-view renders ARE the visual identity).

---

## Image treatment vs doc surgery (routing recommendation)

**DeepInfra FLUX-2-max treatment (hero + architecture diagram):**
- P0: quilt-cell-bridges (hero + 3-views diagram)
- P1: superinstance-ai (site hero refresh — it IS the public face)
- P2 image gaps: fleet-ensemble (conductor diagram), fleet-cns-v3 (topology), plainsong-worker + tapscript-worker (pipeline diagrams), ternary-rom (ternary layout), wesley (growth loop)

**Ship existing drafts first (free wins — art already generated in readme-art-drafts/):**
- fleet-memory ← `drafts/fleet-memory-hero.jpg`
- fleet-embed ← `gallery-fleet-embed.jpg`
- fleet-rooms ← `gallery-fleet-rooms.jpg`
- elephant ← `gallery-elephant.jpg`
- wesley ← `gallery-wesley.jpg`
- quilt family ← `gallery-quilt.jpg`, `reference-quilt-cells.jpg`, `quilt-calm*.jpg`, `quilt-ts-flux-deck.jpg`

**Doc surgery only (no new art needed):**
- superinstance-ai (expand 11-line README)
- fleet-embed, elephant-sim-worker, tap-gamenight, zeroclaw-dissertation (expand thin READMEs)
- field-edge-bridge crate README (605B → proper crate doc)

---

## Priority summary

- **P0 (1):** quilt-cell-bridges — full treatment (clone, hero, diagram, README rebuild, docs/, screenshots)
- **P1 (2):** quilt + quilt-rust polish (gallery wiring, minor gaps) · superinstance-ai README expansion
- **P2 (~20):** fleet-* + plainsong-* + wesley/ideation-games/tap-gamenight/mist-game/ternary-rom — mostly image fills + doc surgery per table

**Top 3 to start with:** ① quilt-cell-bridges (Captain named it, zero images) ② superinstance-ai (11-line README on the public flagship) ③ quilt/quilt-rust gallery wiring (free, makes the family look finished).
