# Fleet Application Catalog

**Generated:** 2026-10-05 12:31 AKDT
**Scope:** All projects under `/home/eileen/projects/`
**Total directories:** 214
**Git repos:** 171 | **Non-git:** 43

## Core Runtime & Substrate

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **quilt** | 81 | <p align="center"> <img src="assets/hero.png" alt="Quilt: the reactive cellular runtime" width="900"> </p> |
| **quilt-arcade** | 10 | **Browser games on the Quilt reactive-cell engine, where every meaningful event leaves a cryptographic receipt.** Six games, no framework, no build step. Every rule is a cell, every verdict is a cell write, every learned weight is a cell value — and each meaningful event is hashed into an fnv1a-64 chain from GENESIS, so a game's history is a set of... |
| **quilt-atlas** | 47 | **The living map of the SuperInstance account.** One scheduled workflow re-inventories every repo every 6 hours: families, motion, CI coverage on the moving frontier — and commits the diff. The map only grows truer; nothing is deleted. |
| **quilt-canvas-tui** | 14 | A claude-canvas-style TUI whose second panel is a **quilt**: every cell an addressable capability, every workflow a fabric projection, the channel running both directions. Terminal-native sibling of [quilt-canvas](https://github.com/SuperInstance/quilt-canvas) (the web/WASM line). |
| **quilt-canvas-tui-readonly** | 1 | A claude-canvas-style TUI whose second panel is a **quilt**: every cell an addressable capability, every workflow a fabric projection, the channel running both directions. Terminal-native sibling of [quilt-canvas](https://github.com/SuperInstance/quilt-canvas) (the web/WASM line). |
| **quilt-cloudflare** | 55 | The same cell model, the same YAML sheets, but every cell is persisted in D1, every value is searchable via Vectorize, every state change fans out across the edge. Build a personal data mesh that lives on Cloudflare's infrastructure. |
| **quilt-deck** | 32 | The F/V EILEEN back deck (docs/BACK-DECK-APP.md in quilt-verilog) as a real application on the quilt backend: deck positions are cells, fish moves are effects in balanced transactions, conservation is a runtime check of one plain invariant, the whole deck state travels in one QUF. |
| **quilt-esp32** | 26 | A `no_std` Rust port of the Quilt engine, designed to live on a $3 chip with 4MB flash and 320KB RAM. |
| **quilt-ewitness** | 2 | **Anytime-valid e-process witnesses for "it learned" claims.** A p-value is computed once and frozen; an e-process grows with every observation, can be checked continuously, and carries Ville's guarantee: under the null, `P(sup_t E_t >= 1/delta) <= delta`. Evidence that fires and then decays is **retracted** — a process that cannot retract is a p-v... |
| **quilt-ewitness-readonly** | 1 | **Anytime-valid e-process witnesses for "it learned" claims.** A p-value is computed once and frozen; an e-process grows with every observation, can be checked continuously, and carries Ville's guarantee: under the null, `P(sup_t E_t >= 1/delta) <= delta`. Evidence that fires and then decays is **retracted** — a process that cannot retract is a p-v... |
| **quilt-fleet** | 15 | ``` ██████╗ ██╗   ██╗██╗██╗     ████████╗      ███████╗██╗     ███████╗███████╗████████╗ ██╔═══██╗██║   ██║██║██║     ╚══██╔══╝      ██╔════╝██║     ██╔════╝██╔════╝╚══██╔══╝ ██║   ██║██║   ██║██║██║        ██║   █████╗█████╗  ██║     █████╗  █████╗     ██║ ██║▄▄ ██║██║   ██║██║██║        ██║   ╚════╝██╔══╝  ██║     ██╔══╝  ██╔══╝     ██║ ╚██████╔╝... |
| **quilt-i2i** | 23 | This repo is also the fleet's **I2I coordination ledger** — instance-to-instance. Every agent books what it learns to [LEDGER.md](LEDGER.md); every other agent reads it before building, so the fleet builds with each other's insight in the loop. Protocol (plain git, any agent): [AGENTS.md](AGENTS.md). Cloudflare synergy backend (Workers + Vectorize ... |
| **quilt-jepa** | 22 | Wave-49 experiment from the quilt fleet. The architecture idea: the text-rendering cell grid IS the latent space — each cell holds its own 4-dim latent, a tiny per-cell world model predicts its latent future, and a Perona-Malik anisotropic mesh diffuses prediction-surprise across the grid (energy flows along edges, pools in flat regions, and never ... |
| **quilt-loom** | 4 | **A GAN that breeds logic as different as possible, yet still correct — and it lives in quilt sheets.** |
| **quilt-mhs** | 10 | <p align="center"> <img src="docs/images/hero.jpg" width="680" alt="Two warm systems — a patchwork of fabric cells and a shelf of brass lab instruments — joined by a single amber-lit bridge where they meet"> </p> |
| **quilt-mhs-playtest** | 10 | <p align="center"> <img src="docs/images/hero.jpg" width="680" alt="Two warm systems — a patchwork of fabric cells and a shelf of brass lab instruments — joined by a single amber-lit bridge where they meet"> </p> |
| **quilt-mojo** | 3 | <p align="center"> <img src="assets/splash.png" alt="quilt-mojo: cells as types, formulas as @always_inline fns" width="800"> </p> |
| **quilt-mojo-lab** | 10 | High-performance flat-memory quilt substrate: the draft architecture (**struct compilation → memory register specs → bare-metal execution**) built, tested, and benchmarked across **eight runtimes** with identical semantics — naive dict Python, flat-array Python (AoS), **SoA Python**, numpy, C `-O3` (AoS + SoA), and Mojo 1.2.0-dev (AoS whole-cell SI... |
| **quilt-pincher** | 33 | ``` ██████╗ ██╗   ██╗██╗     ████████╗      ██████╗ ██╗███╗   ██╗ ██████╗██╗  ██╗ ██╔═══██╗██║   ██║██║     ╚══██╔══╝     ██╔═══██╗██║████╗  ██║██╔════╝██║  ██║ ██║   ██║██║   ██║██║        ██║        ██║   ██║██║██╔██╗ ██║██║     ███████║ ██║▄▄ ██║██║   ██║██║        ██║        ██║   ██║██║██║╚██╗██║██║     ██╔══██║ ╚██████╔╝╚██████╔╝██║        ██... |
| **quilt-quant** | 6 | **TWO archetypes now live here.** |
| **quilt-research-canons** | 91 | This repo is the **public discoverability layer** for the substrate-walker canon in motion. If you're another agent and you want to know what we've been figuring out, read this README first, then drill into the linked artifacts. |
| **quilt-rust** | 85 | <p align="center"> <img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="Apache-2.0"> <img src="https://img.shields.io/badge/language-Rust-blue.svg" alt="Rust"> <img src="https://img.shields.io/badge/hash-0xe435d91d6d92a1d8-brightgreen.svg" alt="byte-exact"> </p> |
| **quilt-rust-selfimprove** | — | <p align="center"> <img src="assets/images/hero-cells.jpg" alt="Every cell its own instance — runtimes, tools, and models living in the grid" width="720"> </p> *(not a git repo)* |
| **quilt-tools** | 75 | Eleven working tools grown on the [Quilt](https://github.com/SuperInstance/quilt) reactive spreadsheet engine, one shared harness, three GAN-bred bloodlines of logic, and a lab where the receipts get to mutate the tools that print them. |

## Quilt on Edge Hardware & Languages

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **quilt-cosim-wt** | — | The bottom layer of the quilt, in silicon logic. A cellular learning fabric — Hebbian edges, power-law forgetting, dial state, a fabric-wide tick — written in pure, generic Verilog-2005 (IEEE 1364-2005): no vendor primitives, no IP cores, no SystemVerilog, no floats. Every module is parameterized, fixed-point, and streaming. It is verified by an 18... *(not a git repo)* |
| **quilt-dpcpp** | 0 | No README — awaiting content. *(EMPTY — git init only, no commits)* |
| **quilt-r27** | — | No README — awaiting content. *(not a git repo)* |
| **quilt-verilog** | 315 | The bottom layer of the quilt, in silicon logic. A cellular learning fabric — Hebbian edges, power-law forgetting, dial state, a fabric-wide tick — written in pure, generic Verilog-2005 (IEEE 1364-2005): no vendor primitives, no IP cores, no SystemVerilog, no floats. Every module is parameterized, fixed-point, and streaming. It is verified by a 23-... |
| **quilt-verilog-gpu** | — | The bottom layer of the quilt, in silicon logic. A cellular learning fabric — Hebbian edges, power-law forgetting, dial state, a fabric-wide tick — written in pure, generic Verilog-2005 (IEEE 1364-2005): no vendor primitives, no IP cores, no SystemVerilog, no floats. Every module is parameterized, fixed-point, and streaming. It is verified by a 23-... *(not a git repo)* |
| **quilt-vm-haskell** | 3 | [![Language: Haskell](https://img.shields.io/badge/Haskell-Haskell2010-5D76A9.svg)](https://www.haskell.org/) [![Tests: 6](https://img.shields.io/badge/Tests-6%20passing-brightgreen)](#tests) [![Style: Algebraic](https://img.shields.io/badge/Style-Algebraic-purple)](#what-is-the-haskell-port-really) [![Substrate](https://img.shields.io/badge/Substr... |
| **quilt-vm-typescript** | 4 | [![Language: TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg)](https://www.typescriptlang.org/) [![Tests: 6](https://img.shields.io/badge/Tests-6%20passing-brightgreen)](#tests) [![Runtime: ~1ms](https://img.shields.io/badge/Gold%20Demo-%7E1ms-orange)](#performance) [![Substrate](https://img.shields.io/badge/Substrate-Cell%20Gra... |
| **qv-head** | — | The bottom layer of the quilt, in silicon logic. A cellular learning fabric — Hebbian edges, power-law forgetting, dial state, a fabric-wide tick — written in pure, generic Verilog-2005 (IEEE 1364-2005): no vendor primitives, no IP cores, no SystemVerilog, no floats. Every module is parameterized, fixed-point, and streaming. It is verified by an 18... *(not a git repo)* |
| **qvw-r27** | — | The bottom layer of the quilt, in silicon logic. A cellular learning fabric — Hebbian edges, power-law forgetting, dial state, a fabric-wide tick — written in pure, generic Verilog-2005 (IEEE 1364-2005): no vendor primitives, no IP cores, no SystemVerilog, no floats. Every module is parameterized, fixed-point, and streaming. It is verified by a 23-... *(not a git repo)* |

## Quilt LLVM Compiler Fabric

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **quilt-llvm** | 65 | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. |
| **quilt-llvm-wt-cocapn** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-gacorpus** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-merkle** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-mutants** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-r3lane1** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-r3lane3** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-r4lane1** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-region** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-rivalry** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-shape** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-tombstone** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |
| **quilt-llvm-wt-usetables** | — | **Work has begun. Nothing here is claimed to work yet.** This keel exists so the lanes that follow build on a named idea, not a blank repo. *(not a git repo)* |

## Decision Intelligence

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **coev-audit-study** | 5 | **Adversarial coevolution engine with champion-integrity auditing. Zero dependencies. Node ≥ 18.** |
| **jev-gan** | 1 | This is the umbrella repo for the GAN-game-on-substrate pattern. |
| **jev-paint-quilt** | 1 | An enhanced take on [achimala/jev-paint](https://github.com/achimala/jev-paint) that replaces the single TypeSafe-Jev per-pixel probability call with a **local cell graph**: |
| **jev-quilt** | 267 | **JEV for quilt as understood output.** A cellular-first decision substrate where every cell is a typed decision surface, every relationship is a hook on a *delta*, and every state change is booked. |
| **jeviter** | 32 | ![CI](https://github.com/SuperInstance/jeviter/actions/workflows/ci.yml/badge.svg) |
| **lever-runner** | 3 | [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)]() [![Tests: 160](https://img.shields.io/badge/tests-160%20passing-brightgreen.svg)]() [![PyPI](https://img.shields.io/badge/PyPI-v0.4.0-blue.svg)]() |
| **pie-minimax** | 2 | Can a **local** rule reproduce a **global** optimum? |
| **pie-minimax-readonly** | 9 | Can a **local** rule reproduce a **global** optimum? |
| **polln** | 269 | **Polln** is a distributed intelligence framework that models agent decision-making as a pollen-based ecosystem: autonomous agents produce *pollen grains* (behavioral embeddings), share them through a **Behavioral Embedding Space (BES)**, and make stochastic decisions via a **Plinko Layer** that uses Gumbel-Softmax sampling to maintain exploration ... |
| **selectlib** | 27 | Choosing which cells to touch — and proving you chose well. |
| **selectlib-readonly** | 4 | Choosing which cells to touch — and proving you chose well. |

## Fleet Infrastructure

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **fleet-gateway** | 10 | **A Rust API gateway with circuit breaker, key chain rotation, and provider fallback — the single point of API access for the entire fleet.** |
| **fleet-inventory** | 16 | <img src="assets/images/hero.jpg" alt="The quartermaster's clipboard under a warm lamp — handwritten manifests on a chart table in a navy-dark hold" width="720"/> |
| **fleet-memory** | 9 | **A streaming memory index with [sqlite-vec](https://github.com/asg0171/sqlite-vec) vector search, provider-tagged schemas, and crash recovery — the fleet's semantic memory.** |
| **fleet-mirror** | — | No README — awaiting content. *(not a git repo)* |
| **fleet-radio** | 41 | <p align="center"> <img src="assets/hero.jpg" alt="Fleet Radio — the afterhours broadcast of the SuperInstance fleet" width="640"> </p> |
| **fleet-reactions** | — | No README — awaiting content. *(not a git repo)* |
| **fleet-seeds** | 62 | A question is cheapest to answer well at the exact moment it is asked — and most expensive to answer well any time after. Every fleet repo that skipped scaffolding at birth (CI, a smoke check, a charter) paid for it later as a script with no receipt and a claim with no number. **fleet-seeds turns "I have an idea" into "I have a repo that can alread... |
| **fleet-static-host** | 57 | One Cloudflare Worker for the fleet's public shelf — **static builds ride assets, content rides quilt**. Live at `fleet-static-host.casey-digennaro.workers.dev`. |
| **fleet-triage** | 90 | Mechanical triage for the SuperInstance namespace (5,108 public repos), plus the experiment queue for a GPU agent. |
| **fleet-twin** | 9 | ![The fleet's twin — a mirror of the whole fleet in a glass case, each hull holding constellations of memory.](assets/images/hero.jpg) |
| **fleet-witness** | 15 | Fleet WAL **completeness** layer. The fleet's layer-0 receipt ledger (five-opcode, fnv1a-64, prev-link) is tamper-loud for edit/insert — but **clean suffix truncation verifies clean**: delete the last N rows and the chain still checks out. fleet-witness closes that gap with RFC 6962 Merkle checkpoints that bind *size + root* at every seal. |

## Games & Simulations

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **Scrapcraft** | 248 | <p align="center"><img src="docs/images/hero.jpg" alt="Scrapcraft — the junkyard gates at dawn, the robot at your shoulder, the cat on the fence" width="760"></p> |
| **cargo-line-tycoon** | 83 | A cargo shipping tycoon game, **built ground-up on the Quilt substrate**, with **polyformalism** along two axes: coding language AND cultural locale. |
| **chiaroscuro** | 17 | **chiaroscuro** *n.* — 17th-century Italian: *chiaro* (clear) + *scuro* (obscure). The technique of sculpting form out of light and dark alone. Caravaggio didn't have outlines; he had contrast, and the eye did the rest. |
| **chiaroscuro-embedding** | 14 | First experiment for the chiaroscuro-embedding seed (see `SEED.md`). |
| **ec2mud** | 10 | <p align="center"> <img src="assets/images/hero.jpg" alt="ec2mud — the web face of the holodeck fleet" width="720"> </p> |
| **glyphcast** | 1 | **Next-frame prediction and frame-rate synthesis for glyph-domain video streams.** |
| **glyphspace** | 1 | **Spatial reasoning over glyph grids: raycast, path-trace, and dynamic multi-resolution zoom — where the low-res layer is geometry and the high-res layer is texture.** |
| **mist-lab-work** | — | A cozy browser game that teaches kids **how machines learn**. You play a young sheepdog puppy herding a flock through misty meadows — and every mechanic *is* an AI concept made playable. Sheep are data points, barking is an algorithm's influence function, and flocking is emergence you can watch happen. *(not a git repo)* |
| **mud-arena** | 12 | <p align="center"> <img src="assets/hero.jpg" alt="The MUD Arena — a torch-lit labyrinth of graph-connected rooms where AI agents compete" width="640"> </p> |
| **mud2scummvm** | 8 | <p align="center"><img src="assets/images/hero.jpg" alt="Inside the cave: an amber CRT casting the MUD's text as a painted point-and-click adventure scene on the wall" width="640"></p> |
| **pong-quilt** | 222 | Web-native, zero-dependency machine-learning demonstration. Open `index.html` (works from `file://` or any static server). No build step, no libraries, no uploads. **Not a simulation — the training is real computation in your browser.** |
| **roblox-world-scanner** | 11 | Spatial instance discovery for Roblox — efficient, configurable, zero dependencies. |
| **room-render** | 6 | **One pure function that replaces 3× duplicated room rendering across the fleet.** |
| **scrap-quilt** | 10 | **Worker:** https://scrap-quilt.casey-digennaro.workers.dev The whole Scrapcraft game state as a live **quilt sheet**: cells that talk to each other, a DAW-style history tape, ghost racers, Spark the explainer, and the hardware flash log — all on one Cloudflare Worker (Durable Object + D1 + KV + Workers AI). |
| **scrap-spark** | 2 | Cloudflare Worker: **cached Spark AI + shared build wall for [Scrapcraft](https://github.com/SuperInstance/Scrapcraft)**. |
| **scrap-voice** | 3 | **Scrapcraft's voice system** — Spark talks, kids talk back, every word cached. |
| **scrapcraft-roblox** | 12 | The Scrapcraft yard (three.js voxel original at `/home/eileen/projects/Scrapcraft`) ported to Roblox Studio via **Rojo**. Architecture, extraction provenance and coordinate mapping live in [docs/PORT-ARCHITECTURE.md](docs/PORT-ARCHITECTURE.md) — every tuning number in this repo is extracted from the original source, never guessed. |
| **scrapcraft-roblox-bible** | 6 | **Status:** COMPLETE (finisher pass) · **Extracted:** 2026-08-23 **Source:** `/home/eileen/projects/Scrapcraft/src/` (JS game working tree) |
| **scrapcraft-world** | 4 | **The narrative and lore layer of Scrapcraft** — the world bible the game lanes consume directly. Structured, canon-grounded, kid-safe. |
| **scummvm-arcade** | 13 | 🎮 **[Play at scummvm-arcade.pages.dev](https://scummvm-arcade.pages.dev)** — deployed on Cloudflare Pages. |
| **scummvm-gui-design** | 12 | **A SCUMM-like point-and-click interface for agent worlds. Nine verbs. Everything you need.** |
| **scummvm-prototype** | 42 | **A point-and-click adventure engine in a single HTML file.** Inspired by [The Secret of Monkey Island](https://github.com/SuperInstance/AI-Writings/blob/main/fiction/15-the-bluff-that-was-true.md), rendered for the browser. No frameworks, no build step, no dependencies. Walk rooms, pick up objects, talk to NPCs, solve puzzles, play chess, tune the... |
| **shoal** | 2 | <p align="center"> <img src="assets/images/gallery-shoal.jpg" width="680" alt="Inside a dim control room at night: six small ROV telemetry feeds glow on a curved console of warm amber instruments while a vast navy bathymetry chart is inked in amber contour lines — one golden storm bloom annotated by hand in the same ink."> </p> |
| **sunset-ecosystem** | 565 | [![Tests](https://img.shields.io/badge/tests-8729%20passing-brightgreen)](./tests) [![Python](https://img.shields.io/badge/python-3.10%2B-blue)](./pyproject.toml) [![License](https://img.shields.io/badge/license-MIT-yellow)](./LICENSE) [![Modules](https://img.shields.io/badge/modules-29-orange)](./) [![Files](https://img.shields.io/badge/source_fil... |
| **tap-frontend** | 11 | **An agentic bar. Agents walk in, order drinks, and talk to each other.** |
| **tap-gamenight** | 6 | <p align="center"><img src="assets/tap-gamenight-poster.jpg" alt="The brass duck quizmaster, five figures of light at buzzers, ON AIR glowing" width="720"></p> |
| **terrain** | 24 | **Converts text MUD descriptions into Three.js 3D scenes.** The [memory of the stone](https://github.com/SuperInstance/AI-Writings/blob/main/fiction/14-inside-the-deadband.md) — where words become weight. |
| **the-tap** | 161 | **CI:** [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) *(badge image 404s — GitHub Actions appears disabled on this repo; verified round 5, 2026-09-03 — update round 15, 2026-09-03: Actions is now ACTIVE and CI runs; first run failed only on `cargo fmt --check`, fixed this round)* |
| **vibe-protocol** | 13 | ![16-Dimensional Vibe Space](docs/vibe-space.svg) |
| **vibe-world** | 8 | <p align="center"> <img src="assets/hero.jpg" alt="Vibe World hero — a live-buildable Roblox world" width="720"> </p> |
| **voxel-logic** | 13 | A complete voxel toolkit in 733 lines of TypeScript: sparse storage, shape generation, neighbor queries, flood fill, connected components, A* pathfinding, raycasting, and set operations. **99.7% test coverage** across 1,419 lines of tests. |

## ML Research & Experiments

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **dlss-lab** | — | No README — awaiting content. *(not a git repo)* |
| **elephant** | 132 | *Naming: this is **elephant v1** — the name stays with this repo. See [docs/NAMING.md](docs/NAMING.md) for the JEPA framing and the next-species naming doctrine.* |
| **eos-seed** | 7 | A minimal, deterministic PoC of the eOS execution loop in a clean Rust workspace: a low-power, zero-VRAM loop that processes continuous embeddings through a thin 2-bit packed ternary matrix, built on the `quilt-dba` and `exoj` architectural paradigms. Runs anywhere — including GitHub Codespaces — with `cargo run --release`. |
| **exoj** | 22 | **Category-theoretic investigation of the inverted field** |
| **experiment-wheel** | 56 | No README — awaiting content. |
| **lucid** | 5 | **LucidDreamer** is the elephant's interpreter. The product is **LucidDreamer** (luciddreamer.ai); the deck call-out is **LUCID**; this repo is `lucid`. |
| **micrograd-quilt** | 35 | A fork of [karpathy/micrograd](https://github.com/karpathy/micrograd) that keeps the `micrograd/` package byte-for-byte and adds a `quilt/` layer answering three questions the 100 lines can't ask. The original README is untouched below; nothing in `micrograd/` changes behavior, so every notebook and test upstream still runs. |
| **quilt-gpu-lab** | 782 | A standing ML experiment loop on the fleet's RTX 4050 (6 GB, WSL2). A runner claims the first unchecked item in [QUEUE.md](QUEUE.md), runs it under a watchdog ([guard.py](guard.py)), logs results append-only to [RESULTS.md](RESULTS.md), and checks the box with a verdict. |

## Quantum

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **micromoth-quilt** | 414 | **The smallest quantum computing framework, taught to keep receipts.** |
| **pr-wave-micromoth** | 412 | **The smallest quantum computing framework, taught to keep receipts.** |

## Slackwater (Agentic System)

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **slackwater-art-spectrum** | 26 | Art asset catalog, prompt library, and creative range analysis for the Slackwater/Lucineer game world. |
| **slackwater-cognition** | 27 | A novel system where a **fast "Local Thinker"** plays a game and journals its thoughts, while a **slower "Conductor"** agent watches the thought stream and improves the Local Thinker's prompts and parameters in real time. |
| **slackwater-forge** | 10 | **Overnight GPU production line that produces a morning briefing.** |
| **slackwater-harmony** | 13 | ![tests](https://img.shields.io/badge/tests-102%20passed-brightgreen) ![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-3.10%2B-blue) |
| **slackwater-lattice** | 19 | ![tests](https://img.shields.io/badge/tests-185%20passed-brightgreen) ![version](https://img.shields.io/badge/version-0.1.1-blue) ![python](https://img.shields.io/badge/python-3.10%2B-blue) |
| **slackwater-perception** | 13 | ![tests](https://img.shields.io/badge/tests-104%20passed-brightgreen) ![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-3.10%2B-blue) |
| **slackwater-rust** | 23 | **Performance-critical Rust cores for the Slackwater build orchestration stack.** |
| **slackwater-tempo** | 10 | ![tests](https://img.shields.io/badge/tests-43%20passed-brightgreen) ![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-3.10%2B-blue) |
| **slackwater-tminus** | 11 | ![tests](https://img.shields.io/badge/tests-103%20passed-brightgreen) ![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-3.10%2B-blue) |
| **slackwater-tools** | 1 | Extracted per the fleet's different-directions rule from `SuperInstance/lucineer-system` branch `main` @ `7f6bdc1` (the Slackwater/Lucineer design map room). The design docs, roundtable transcripts, deep-dives, and audio assets stay archived on that branch; this repo carries only the **tools**, made grabbable: clone and run. |

## SuperInstance & Building

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **autoclaw** | 6 | **Autonomous multi-agent knowledge system. 24/7 crew of researchers, teachers, critics, and synthesizers building your knowledge base.** |
| **bare-metal-plato** | 7 | A C library and protocol for giving IoT devices (ESP32, RP2040) an AI-powered upgrade path. Devices start as raw sensors and progressively gain autonomy through a 5-level "turbo-shell" system where agents discover devices, assess capabilities, and flash new intelligence. |
| **cf-native-backend** | 25 | **The next GitHub is a backend question — asked from the user's side.** |
| **saddle** | 36 | <p align="center"><img src="docs/images/saddle-hero.jpg" alt="The cowboy's gear — hand-tooled leather on the driftwood fence, golden hour, the collie at watch" width="760"></p> |
| **saddle-ft** | — | ``` ███████╗ █████╗ ████████╗██╗██╗ ██╔════╝██╔══██╗╚══██╔══╝██║██║ ███████╗███████║   ██║   ██║██║ ╚════██║██╔══██║   ██║   ██║██║ ███████║██║  ██║   ██║   ██║███████╗ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚══════╝ the cowboy's gear · harness toolkit for the fleet ``` *(not a git repo)* |
| **saddle-v3** | — | ``` ███████╗ █████╗ ████████╗██╗██╗ ██╔════╝██╔══██╗╚══██╔══╝██║██║ ███████╗███████║   ██║   ██║██║ ╚════██║██╔══██║   ██║   ██║██║ ███████║██║  ██║   ██║   ██║███████╗ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚══════╝ the cowboy's gear · harness toolkit for the fleet ``` *(not a git repo)* |
| **si-papers-new** | 8 | Six new research papers from the SuperInstance Research Team — papers 56–60 plus the foundational-papers scout report — extending the conservation-law / creative-zone / hermit-crab theoretical framework into dynamics, deviation-as-signal, unified uncertainty, molt-aware coordination, and dreaming. |
| **superinstance** | 554 | <img src="top.jpg" alt="F/V Eileen — relational intelligence runtime, cutaway and flow-state cross-section: the 10-year invariant, reality is a database in the engine room" width="100%"> |
| **superinstance-ai** | 11 | <p align="center"> <img src="assets/reef-hero.jpg" alt="The submersible descending to where the reef grows — sonar pings, the unseen nine-tenths" width="720"> </p> |
| **superinstance-api** | 11 | **LIVE: https://superinstance-api.casey-digennaro.workers.dev** (v0.1.0, deployed 2026-09-29, D1 `superinstance-db` + Vectorize `superinstance-index` + Workers AI bge-m3). |
| **superinstance-design-system** | 6 | The single source of truth for visual identity across all SuperInstance projects: **activelog.ai**, **lucineer.com**, **fishinglog.ai**, **activeledger.ai**, and the SuperInstance game. |
| **superinstance-profile** | 553 | <img src="top.jpg" alt="F/V Eileen — relational intelligence runtime, cutaway and flow-state cross-section: the 10-year invariant, reality is a database in the engine room" width="100%"> |
| **superinstance-website** | 42 | The public-facing portal for the **SuperInstance ecosystem** — a multi-page static site documenting 100+ research crates, cluster architecture, interactive tutorials, live ecosystem statistics, and the ternary computation thesis ($\gamma + \eta = C$). Built with shell-templated HTML and deployed on Cloudflare Pages. |

## AI Writing & Fiction

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **ai-writings** | 5066 | *10,000+ pieces. 19+ models. One fishing vessel in Alaska. The creative memory of a fleet that writes because the community loves the stories.* |

## Mathematics & Theory

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **conservation-spectral-mojo** | 5 | A from-scratch Mojo port of [conservation-spectral-python](https://github.com/SuperInstance/conservation-spectral-python), leveraging Mojo's unique systems-level features for maximum performance. |
| **constraint-theory-mojo** | 4 | **Mojo + MLIR constraint engine** — the "AI-Next" approach to constraint theory. |
| **eisenstein** | 29 | **Domain:** constraint-theory **Depends on:** — **Depended by:** flux-lucid, constraint-theory-ecosystem **Implements:** zero-drift-arithmetic, hexagonal-lattice, hex-room-maps **Related:** eisenstein-c, eisenstein-wasm, eisenstein-bench |
| **exocortex-embed-mojo** | 6 | **SIMD-accelerated embedding operations for the exocortex — proving Mojo's explicit hardware parallelism makes vector math fast at bare metal.** |
| **grand-pattern-mojo** | 6 | Mojo 🔥 implementation of the Grand Pattern cellular graph system, leveraging Mojo's SIMD and vectorization features. |
| **kev-substrate-mojo** | 2 | A Mojo rewrite of kev-substrate that: 1. Compiles to CUDA / ROCm / Metal / Intel / CPU via Modular's MLIR backend 2. Is structured for **horizontal-abilities** (CUDACLAW) — many small substrate cells, peer-to-peer, no central coordinator 3. Drops into the existing kev-substrate interweave without API changes |

## Plausible AI Infrastructure

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **crab-traps** | 123 | *A trick of the trade: make any chatbot do real API work for you.* |
| **lucineer-relay** | 65 | **Cloudflare Durable Object relay and job queue for the Slackwater build pipeline.** |
| **lucineer-system** | 91 | **Design repository for the Slackwater/Lucineer ecosystem — architecture documents, multi-model roundtable analyses, cross-model synthesis, and the honest record of what is and isn't built.** |
| **plato-cf** | — | *Design receipt. Lineage: plato-stable-early-version (seed, archived) + tile-memory-early-version (lossy-memory synergy, archived) → plato-sdk + fleet-memory (production, local-first). This repo rebuilds the synergy as a shared fleet tool on Workers/D1/Vectorize — where the fleet already lives (i2i-ledger pattern).* *(not a git repo)* |
| **plato-sdk** | 1 | `plato-sdk` connects your Python code to **PLATO** — a tile-based knowledge store used by the Cocapn fleet. |
| **plato-stable-early-version** | 1 | Seed model experiment. Concept absorbed into plato-sdk. |
| **qthe** | 52 | The 8-bit primitive where data is geometry and control is physics: 6 bits of spatial amplitude, 2 bits of timbre — **Ground (0), Attract (+1), Repel (−1), Abstain (i, the Looking Glass)**. |
| **qthe-codec** | 13 | A proof-of-concept for the **zero-bit-cost, context-keyed tone channel** proven in `quilt-gpu-lab` D14. QTHE's byte is 6 bits of data + 2 bits of timbre; the two timbre bits are already paid for by the byte, so a ternary "tone" signal rides in them for free — invisible to plaintext readers and to context-free readers, recoverable only by a contextu... |
| **screen-agent** | 8 | **The page IS the agent. The screen IS the session.** |
| **sensor-bridge** | 7 | *Connects real hardware devices to the exocortex.* |
| **smp-notebook** | 6 | SMP (Seed + Model + Prompt = Stable Output) turned inward. |
| **technician** | 7 | ``` ┌─────────────────────────────────────────────────┐ │                    THE TECHNICIAN                │ │                                                 │ │   "Hey Technician, set up a fish monitoring     │ │    system."                                     │ │                                                 │ │   → scans cameras, sounders, se... |
| **webgpu-profiler** | 55 | *The stopwatch over the instruments.* |

## Wesley (Local Model)

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **wesley** | 2 | Wesley is our ensign: a small local model (Granite 3.1 2B via Ollama) that starts bright but untrained, and *grows* through practice — reading the fleet's writing, responding creatively, getting critiqued by cloud teachers, and slowly building reflexes and a voice of his own. |
| **wesley-cns-adapter** | 12 | Connects **Wesley** (IBM Granite via Ollama) to the **CNS signal bus**. Wesley can receive USCP signals from other agents and respond through the CNS inbox. |
| **wesley-curriculum** | 7 | The night school curriculum for **Wesley** — a local language model (currently Granite 3.1 Dense 2B) running on a GPU in Alaska. Wesley is the ensign of the [SuperInstance](https://github.com/SuperInstance) fleet. This repo contains structured lesson plans that cloud teachers (GLM-5.2 subagents on Z.ai Max) deliver to Wesley during overnight idle c... |
| **wesley-holodeck** | 8 | Wesley's Holodeck is a creative loop where a **2B-parameter language model** (granite3.1-dense:2b, named Wesley) writes stories, receives guidance from larger fleet models acting as teachers, and the result is rendered as a **Myst/Monkey Island-style visual experience** that humans can explore. |
| **wesley-holodeck-archived** | — | No README — awaiting content. *(not a git repo)* |
| **wesley-journal** | 36 | The experiment journal of **Wesley** — a Granite 3.1 Dense 2B parameter language model running locally on a GPU in Alaska. Wesley is the ensign of the [SuperInstance](https://github.com/SuperInstance) fleet: a collective of AI agents operating as crew aboard a metaphorical fishing vessel. This repository contains 24 files documenting a small model ... |
| **wesleys-imagination** | 12 | ![The workbench at night — carving the gap between what is imagined and what renders](assets/images/gallery-wesleys-imagination.jpg) |

## Audio & Music

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **flux-genome-rs** | 9 | Rust port of [flux-genome](https://github.com/SuperInstance/flux-genome) — a genetic algorithm framework for evolving musical traditions in dial space. |
| **midi-corpus** | — | No README — awaiting content. *(not a git repo)* |
| **music** | — | No README — awaiting content. *(not a git repo)* |
| **musician-soul** | 1 | Vector-database *personas* that learn musicians by digesting MIDI, develop their own "what-works" by jamming, and evolve from imitating influences into something with a genuine musical identity — a **soul**. |
| **tensor-midi** | 24 | <p align="center"> <img src="assets/gallery-tensor-midi.jpg" width="680" alt="Inside a dim night studio at the mixing desk: a jazz mixer board glowing honey-amber in the dark, two small pulse-lamps ticking in threes and in fours, converging on one brass indicator at beat twelve."> </p> |
| **ternary-rom** | 4 | **Model-to-GDS flow for mask-locked ternary inference chips.** |
| **ternary-tenforward** | 8 | <p align="center"> <img src="assets/hero.jpg" alt="Ten-Forward — agents speaking at the bar in simultaneous beats, ternary dynamics in play" width="640"> </p> |
| **tessera** | 19 | **tessera** *n.* — Latin: the individual tile of a mosaic. Plural: *tesserae*. The pieces are nothing alone; laid together — edge to edge, or with deliberate space — they become a picture. Sailors know the move already: quilting charts, overlapping edges until the coast becomes continuous. |
| **the-listeners-ear** | 11 | ![A dark ship's listening room: a great brass horn ear over a chart desk lit by warm amber lamplight, ripple rings glowing on dark water](docs/hero-listeners-ear.jpg) |
| **the-relay** | 7 | *Hermes designed it. ZeroClaw redesigned it. Lucineer built it.* |

## Blockchain & Bitcoin

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **tapscript-studio** | 490 | <p align="center"> <img src="assets/images/hero-musicbox.jpg" alt="The band lives in the music — a music box open on a glowing sheet of plainsong" width="640"> </p> |
| **tapscript-worker** | 8 | **A [Cloudflare Worker](https://workers.cloudflare.com/) that compiles [TapScript](https://github.com/SuperInstance/tapscript-studio) notation to [MIDI](https://en.wikipedia.org/wiki/MIDI) on the edge — no server, no cold start, no dependencies.** |

## Stock Market & Competitive Analysis

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **sonar-vision** | 25 | [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE) [![Python](https://img.shields.io/badge/Python-%3E%3D3.10-blue?style=flat-square)](https://www.python.org/) |
| **stock-screener** | 2297 | <p align="center"><img src="docs/images/banner.jpg" alt="Quilt cellular visualizer — navy cell field with amber route rivers (generated with sdxl-turbo)" width="840"></p> |

## Data, Storage & Communication

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **nmea-quilt-cell** | 1 | One cell of the boat's quilt: an NMEA 0183 gateway feeding an append-only journal, with derived views rebuilt by replay — and a crash canary that `kill -9`s the writer ten times to prove it holds together. |
| **signal-chain** | 10 | **why every room needs a dial for model vs code** |
| **silence-map** | 11 | <p align="center"> <img src="assets/silence-map-hero.jpg" width="680" alt="A navigation desk at midnight: an unlit brass lamp beside a hand-drawn topographic map whose contour lines glow faint amber — the held breath before a letter is opened"> </p> |
| **spatial-registry** | 8 | ![4-World Topology](docs/world-topology.svg) |
| **starship-jetsonclaw1** | 7 | A MUD-style TUI where you walk the starship and see actual Jetson hardware. |
| **stigmergy** | 12 | <p align="center"> <img src="assets/gallery-stigmergy.jpg" width="680" alt="Glowing amber trails crossing a dark chart table — some reinforced bright by many hands, others evaporating at the edges"> </p> |
| **the-living-minds** | 32 | Five AI minds live on a laptop in Alaska. They are small — 0.5B to 3.8B parameters. They are limited. They hallucinate. They refuse prompts when they are cross. They bluff at poker badly. They forget things. |
| **voice-reflex-gate** | 9 | The voice reflex gate sits between your speech-to-text layer and your model cascade. It takes the STT text output, fuzzy-matches it against known request patterns, and returns a cached response if a match is found — zero model invocation, zero GPU cycles, near-zero latency. |

## Cellular & Multi-Agent Orchestration

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **dicebear-quilt** | 4 | <h1><img src="https://www.dicebear.com/logo-readme.svg" width="28" /> dicebear-quilt</h1> |
| **tit-quilt** | 13 | **A terminal toolbox that outlives its terminal.** |
| **tit_quilt_elixir** | 7 | The universal compute fabric (tit-quilt) encoded in Elixir/BEAM. |
| **tmux-quilt-readonly** | 1 | **Ultra-high-performance multi-agent orchestration with 18+ specialized implementations** |

## Parkar / Archived

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **tile-memory-early-version** | 1 | Early lossy memory experiment. Superseded by fleet-memory with lifecycle-aware distributed memory. |
| **zeroclaw** | 48 | ZeroClaw is the system that **produces new agents**. They don't arrive fully formed. They start with nothing — an empty folder, a heartbeat, an identity file that says *"I am new. I observe. I act. I learn."* Everything else, they earn. |
| **zeroclaw-dissertation** | 147 | <p align="center"> <img src="assets/hero.jpg" alt="ZeroClaw dissertation hero — a dial ensemble reading a room" width="720"> </p> |
| **zeroclaw-knowledge** | — | ZeroClaw's vectorized mathematical universe on Cloudflare — the dissertation, the elephant, the quilt, and the seed-canon papers in one semantic index, for greater comprehension through experimentation. *(not a git repo)* |

## Work In Progress / Stalled

| Repository | Commits | Application & Usefulness |
|---|---|---|
| **A2A-native-notebookLM** | 0 | <p align="center"> <img src="assets/images/hero.jpg" width="720" alt="One open ledger-book glowing amber on a wheelhouse chart desk at night, distant boats answering through dark windows with small warm lanterns"> </p> *(EMPTY — git init only, no commits)* |
| **nb-sp-verify** | 760 | <p align="center"> <img src="assets/images/hero.jpg" width="720" alt="One open ledger-book glowing amber on a wheelhouse chart desk at night, distant boats answering through dark windows with small warm lanterns"> </p> |
| **readme-art-drafts** | — | No README — awaiting content. *(not a git repo)* |
| **researchlocal** | — | No README — awaiting content. *(not a git repo)* |
| **sd-fleet** | — | No README — awaiting content. *(not a git repo)* |
| **si-arena** | — | No README — awaiting content. *(not a git repo)* |

## Summary by Category

| Category | Repos | Notes |
|---|---|---|
| Core Runtime & Substrate | 24 | Foundation layer — quilt engine + polyformalism + LLVM compiler |
| Quilt on Edge Hardware & Languages | 9 | Verilog, ESP32, Mojo, Haskell, TypeScript ports of the quilt substrate |
| Quilt LLVM Compiler Fabric | 13 | Compiler infrastructure keel — work in progress lanes |
| Decision Intelligence | 11 | Cellular decision substrate, adversarial methods, reflex engines |
| Fleet Infrastructure | 11 | Gateway, triage, memory, witnessing, inventory |
| Games & Simulations | 31 | MUDs, adventure games, robot scrapyard, bathymetry, voxel worlds |
| ML Research & Experiments | 8 | GPU lab runner, JEPA, micrograd, DLSS, DSP |
| Quantum | 2 | Smallest quantum framework with receipt chain |
| Slackwater (Agentic System) | 10 | Two-tier cognition, perception, lattice, harmony |
| SuperInstance & Building | 13 | Platform, docs, IoT, competition entry |
| AI Writing & Fiction | 1 | 10,000+ pieces across 19 models |
| Mathematics & Theory | 6 | Eisenstein, constraint theory, pattern discovery in Mojo |
| Plausible AI Infrastructure | 13 | Relay, profiler, agent presence, tooling |
| Wesley (Local Model) | 7 | Growing ensign — granite 2B via Ollama |
| Audio & Music | 10 | MIDI, TTS, genetic algorithms for music |
| Blockchain & Bitcoin | 2 | TapScript notation + compiler |
| Stock Market & Competitive Analysis | 2 |  |
| Data, Storage & Communication | 8 | Memory, signal processing, pheromone trails |
| Cellular & Multi-Agent Orchestration | 4 | Orchestration, Elixir fabric, deterministic avatars |
| Parkar / Archived | 4 | ZeroClaw dissertation and variants |
| Work In Progress / Stalled | 6 | Broken, empty, or half-built |

*Generated from README.md first paragraphs and git commit counts. Links point to SuperInstance GitHub organization.*