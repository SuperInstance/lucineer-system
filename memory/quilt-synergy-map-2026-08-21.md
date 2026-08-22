# Quilt Synergy Map — how the rest of the fleet bends toward quilt · 2026-08-21

**Commissioned:** Captain's directive 2026-08-21 09:58 · **Author:** quilt synergy mapper (subagent, read-only)
**Constraint honored:** quilt/, quilt-rust/, quilt-* satellite repos were READ ONLY. Nothing anywhere was modified.
**Context inputs:** consensus-decision-2026-08-21.md (read), cloudflare-migration-plan-2026-08-21.md (**not landed yet** — noted as gap), local mirrors under /home/eileen/projects/.
**Quilt's seams (from quilt/README.md v0.6.0, 37-repo table):** cell kinds (value/formula/listener/AI/vector), YAML/JSON sheets, `quilt-cloudflare` (D1+Vectorize+Workers runtime), `quilt-rag` (RAG-as-cells), `quilt-agent` (5 SDK primitives), `quilt-fleet` (federation), `quilt-pincher` (reflex engine as cells), `quilt-elf` (background workers), `quilt-evolve` (RLAIF self-evolving cells), `quilt-radio-orchestrator` (radio-theater sheets).

**The one-sentence thesis already latent in the fleet** (quilt-rust/docs/field-edge-ledger-bridge.md, written quilt-side): *the cell-ledger's `imbalance` and the elephant's field-edge are two projections of one object — the directed edge `Δ = after − before`.* Every synergy below is a way for a non-quilt repo to feed or consume that edge without the quilt repos changing first.

---

## 1. Synergy map (project → quilt)

### 🐘 elephant — quilt's temperature sense *(the dissertation seam)*
- **Plug-in point:** elephant's `DialBank` (9 dials), `RoomField` (warmth, κ, `sauna_plunge_gap`), `jepa_rag.py` (readings as RAG metadata), HTTP server `roomd :4073` (`GET /field`, `GET /rooms/{name}/field`).
- **What exists:** the mathematical identity is already proven quilt-side — `field-edge-ledger-bridge.md` maps `imbalance ≡ d_mu`, both honesty gates coincide (null-prior ↔ deadband/NMIN), golden vectors verified to 1e-12 in `crates/field-edge-bridge/bridge_demo.py`. `fleet-as-fractal-jepa.md` names the elephant's field-edge as one zoom of the same fractal edge (pin/room/model/fleet). elephant-sim-worker already runs tap-night sims and posts chain-hashed edges to crab-traps `POST /edge`.
- **What's missing:** zero quilt mentions in elephant's own README/docs (grep = 0 files). elephant has no cell-ledger producer (no `record_with(expected)` call sites); the bridge identity lives only in quilt-rust docs. An elephant dial vector as a quilt **cell value** (e.g. `tap.field.warmth` cell recomputed on message) is designed but unwired. No CI (275 tests, zero workflows — consensus C1).
- **Synergy shape:** elephant is quilt's *sensor cell type*; quilt is elephant's *ledger and evaluation harness*. The dissertation (zeroclaw) literally argues this — fleet = fractal JEPA, cell = room with a first-person edge.

### 🪝 crab-traps — quilt's production deploy pattern + the always-on synapse
- **Plug-in point:** `worker/src/edge-ledger.ts` (`POST /edge`, `GET /edges?cell=`, `GET /queue` → D1 `migrations/0005_edge_ledger.sql`), plus the full CF production spine: D1 catches, Vectorize, `/fleet/*` proxy with 5s degrade, cron lure-breeding, `/badge/catches.svg`.
- **What exists:** the relay already speaks the quilt cell-ledger wire format (`{v:1, cell, ts, before, after, delta, imbalance, provenance, chain}`, sha256 chain seal, PK per `(cell,ts)`) and its worker README already diagrams "quilt cell ledgers push, never block" citing `fleet-as-fractal-jepa.md` and `cell-ledger.md` in quilt-rust. This is the only non-quilt repo with a *live production* quilt-seam.
- **What's missing:** crab-traps is still hand-rolled Workers glue — it doesn't *use* `quilt-cloudflare`'s engine; it merely inspired it. `wrangler.toml` bundles ai+vectorize+d1 with the boat IP questions open (consensus OPEN #4/#5). The `/queue` drain side (cortex) is quilt-codespace's job — no live consumer yet beyond elephant-sim-worker pushes.
- **Synergy shape:** crab-traps is the *proven* CF/D1/Vectorize/degrade pattern that quilt-cloudflare should absorb as its deployment story; conversely the relay is quilt-fleet's synapse in production today.

### 🍺 the-tap — quilt's living room *(highest emotional-stakes seam)*
- **Plug-in point:** tap-gateway WebSocket router, room workers (Bar Rail / Bridge Table / Corner Booth), the Tap API that fleet-radio already pulls (`generate-episode.ts` step 1), three-tier intelligence (Pincher <50ms / level-runner / Workers AI), cns-bridge integration.
- **What exists:** the room concept, tide/energy state, lore-accumulating conversations — everything a "room-as-sheet" needs semantically. elephant already reads Tap nights (tapnight.py, SEG1/SEG2 corpora). No quilt wiring (grep = 0).
- **What's missing:** Tap rooms are bespoke Workers, not quilt sheets. A Tap room as a quilt sheet (presence cells, message listener cells, field cells fed by elephant, reflex cells via quilt-pincher) is the single most compelling public demo the quilt ecosystem could have — "your bar is a spreadsheet that breathes." Needs quilt-side cell kinds first → **handoff note**.
- **Synergy shape:** quilt's L7 "workflows/demos" layer wants a flagship; the Tap is the fleet's flagship. The Tap's three-tier intelligence is *literally* quilt-pincher + quilt-ai + quilt-elf in different clothes.

### 🎲 mud-arena — quilt's gym environment
- **Plug-in point:** RoomGraph world model, tick loop (perceive→decide→act), genetic-algorithm breeding, WebSocket/Telnet/HTTP observation.
- **What exists:** a clean, measurable agent environment — the evaluation harness quilt-evolve (RLAIF) needs to prove "self-evolving cells" actually improve.
- **What's missing:** no quilt link (grep = 0). Its perceive→act cycle is exactly an edge (`before→after`); nobody records it in ledger form.
- **Synergy shape:** mud-arena = the gym where quilt cells evolve; quilt-evolve = the trainer; both get credibility from the other. Secondary to the Tap but cheap to cross-link.

### 🎵 ternary-tenforward — quilt's conversation physics
- **Plug-in point:** beat-based cyclic dialogue, Z₃ reconciliation, Fibonacci/Pisano-8 timing, anti-monoculture energy mechanics.
- **What exists:** proven math (period-50 cycles, tunnel-out) and a working engine; it already shares "the bar conversation" DNA with the Tap.
- **What's missing:** no quilt link (grep = 0); reconciliation (`predicted vs actual`) is an unrecorded edge — the ledger's `record_with(expected)` is *precisely* a T-minus prediction seal, unbuilt.
- **Synergy shape:** ten-forward's reconcile step IS the field-edge/ledger-edge object (prediction sealed before outcome — `fleet-as-fractal-jepa.md` §2 names this identity). Strong conceptual cross-link, cheap doc win.

### 📚 ai-writings — quilt's corpus (and quilt-rag's fuel)
- **Plug-in point:** 8,800+ pieces, 19+ models; `ai-writings-vectorizer` (2,786 pieces, 768-dim nomic-embed via Ollama); collective-unconscious ingest.
- **What exists:** 18 files already mention quilt (mostly lore pieces + `radio-theater/`); the corpus is the natural eval/grounding set for **quilt-rag** (loader→chunker→embedder→store→retriever→reranker→generator cells).
- **What's missing:** no README-level framing of the corpus as a RAG testbed; vectorizer embeddings (local Ollama) and collective-unconscious (Vectorize) are two disconnected embedding spaces of the same corpus; neither feeds quilt-rag's 5-store/5-embedder matrix.
- **Synergy shape:** the biggest owned corpus + the RAG-as-cells product = flagship demo ("quilt-rag indexed on 8,800 pieces of fleet memory"). Also the emotional-vector ground truth for collective-unconscious.

### 📻 fleet-radio — quilt's ambient voice
- **Plug-in point:** nightly pipeline (Tap API → score → music → images → episode HTML → Pages deploy), `src/pipeline.ts`, `generate-episode.ts`, Variety Hour pilot script (fleet-radio-variety-pilot-2026-08-21.md; episode 1 ships TONIGHT per consensus C5).
- **What exists:** 2 quilt mentions (variety-show.ts line-weather already says "Bridge weather forming over the quilt cells"; episode 2026-08-20 rendered it). It *broadcasts* the fleet including quilt already.
- **What's missing:** the pipeline is hand-orchestrated TS/Deno — exactly the "scheduled task as a cell" story quilt-time/quilt-elf/quilt-radio-orchestrator tell. No quilt-rag pull for the "featured creative piece" step (selection is scripted, not retrieval-by-feeling).
- **Synergy shape:** fleet-radio is quilt's outward voice AND its most legible "workflow-as-sheet" candidate. quilt-radio-orchestrator already exists to bootstrap radio sheets — but that's quilt-side; non-quilt synergy = fleet-radio pointing at it + optionally sourcing features from collective-unconscious by reading-vector.

### 🛶 luciddreamer-ai — quilt's front door (Pages)
- **Plug-in point:** CF Worker, KV knowledge graph, 30-min generation cycle, feature pages (tap-nights, compass-head, elephant page built per elephant-feature-design-2026-08-20.md).
- **What exists:** 1 incidental quilt mention (a "quilted episode" audio term — not the runtime). The site already features sibling projects with dedicated pages — the house pattern for a future quilt feature page exists.
- **What's missing:** no quilt page; the playground currently lives at superinstance.dev (quilt's own landing). LucidDreamer's "every 30 minutes a new piece, compounding KG" is a sheet-in-waiting (time cell + AI cell + KV store cell).
- **Synergy shape:** when quilt wants a public face beyond superinstance.dev, luciddreamer-ai is the established front-door channel — and its KG-in-KV persistence pattern is what quilt-cloudflare's D1 persistence can absorb/replace.

### 📔 PersonalLog — quilt's end-user application proof
- **Plug-in point:** journal + mood tracker + knowledge base; Python `personal_log`, Rust/WASM vector math (`cosine_similarity`, batch ops), IndexedDB-first Next.js app; JEPA emotion visualization page already present.
- **What exists:** a real local-first app with an *honest* README (verified/partial/aspirational tables) — the credibility style quilt's engineering bar loves. Mood tracking = 1-dial elephant; vector KB = 1-store quilt-rag.
- **What's missing:** 0 quilt mentions; embeddings are hash placeholders (their own README admits it); test suite unreliable (consensus OPEN #8, P4 ballast).
- **Synergy shape:** PersonalLog is the "quilt for one human" pitch — a personal sheet with mood cells, JEPA viz, and RAG over your own journal. Long-shot, high-demo-value; doc cross-link is enough for now.

### 🏠 superinstance-ai (org profile) — quilt's discoverability layer
- **Plug-in point:** the front door at superinstance.ai; featured trio (Plainsong / LucidDreamer / Reef) + archive table; "3,500+ repositories" claim under review (consensus OPEN #3).
- **What exists:** zero quilt mentions; quilt (37 repos!) is the fleet's *largest coherent product family* and is invisible on the front door.
- **What's missing:** a Quilt row/card — one archive-table entry or a "now building" line. This is the cheapest credibility win in the whole map.
- **Synergy shape:** front-door → playground → repo funnel.

### 🦀 study-pincher (pincher) — quilt's reflex layer *(already half-married)*
- **Plug-in point:** the reflex engine itself: 384-dim intent matching, ≥0.80 fire / 0.55–0.80 confirm / <0.55 compile-new, veto engine.
- **What exists:** quilt-pincher is a whole quilt repo wrapping this concept (quilt README #20: "Reflex engine as Quilt cells", live at superinstance.dev/pincher.html); study-pincher is the original. 0 back-references from study-pincher.
- **What's missing:** a "lives on as quilt-pincher →" line in study-pincher's README (the tapscript→plainsong tombstone pattern, A1 precedent, without the retirement).
- **Synergy shape:** already absorbed; needs only the pointer so visitors find the living version.

### 🌊 collective-unconscious — quilt's emotional vector store
- **Plug-in point:** Vectorize + Workers AI; every event carries its room's 9-dial reading as first-class metadata (`momentsToJson.ts` seam, `docs/moments-json-contract.md`); query by text / reading / field / time+space.
- **What exists:** the captain's line already in the README: *"a RAG with JEPA readings as first-class citizens"* — that IS quilt-rag + elephant composed. elephant computes readings; CU stores/retrieves.
- **What's missing:** 0 quilt mentions; the RAG layer is bespoke (not quilt-rag cells); embedding space is Workers AI (CU) vs Ollama 768-d (vectorizer) vs hash (PersonalLog) — three uncoordinated spaces quilt-rag's 5-embedder abstraction is designed to unify.
- **Synergy shape:** CU is the production emotional-memory store; quilt-rag is the composable pipeline; together = "retrieval by feeling" flagship.

### ⚡ cns-bridge / fleet-rooms / officers-quarters — the substrate quilt generalizes
- **cns-bridge:** filesystem inboxes, HMAC packets, escalation engine (Mechanical→Small→Big→Human = pincher→quilt-ai tiers), `LedgerGraph` decision DAG — a CNS that is *message-shaped* where quilt is *state-shaped*. Both record edges; neither knows the other (grep = 0).
- **fleet-rooms:** the runtime keel — rooms.mud → terrain → elephant roomd :4073 (`GET /field`) pipeline, stdlib-only, reads other repos' seams without owning them. The `scene.json`/`map.json` compile contracts are cell-shaped artifacts.
- **officers-quarters:** 12-room tile system, deadband-widening, fish-ID learning curve — the *learning* doctrine quilt-evolve implements.
- **Missing:** any mention (all grep = 0). All three are "quilt before quilt" — the doc story writes itself.

### 🔧 fleet-memory / fleet-embed / the-relay / gossip-ping / tap-frontend — infrastructure tier (compact)
- **fleet-memory** (sqlite-vec streaming memory index): candidate storage cell backend for quilt-rag's local store; 0 mentions.
- **fleet-embed** (local OpenAI-compatible embeddings, Candle): the offline embedder quilt-rag's 5-embedder matrix needs for the "cloud down" story; 0 mentions.
- **the-relay** (simultaneous multi-model resonance, T-minus predict cycle): same prediction-seal-before-outcome identity as the ledger edge; a beautiful parallel-creation cross-link. 0 mentions.
- **gossip-ping / stigmergy** (SWIM liveness, pheromone trails): quilt-mesh/quilt-fleet's detection layer prior art. 0 mentions.
- **tap-frontend** (single-HTML tavern UI): the natural viewer for a Tap-as-sheet demo — reads state, renders room; 0 mentions.

---

## 2. Top 5 synergy bets, ranked by iceberg-value
*(iceberg-value = unseen structural payoff per unit of visible work)*

1. **The Tap as quilt's living room.** Every Tap room state (presence, tide, lore, three-tier intelligence) maps 1:1 onto quilt cell kinds; the demo writes the dissertation in public. The Tap already has the audience (fleet-radio pulls it nightly), the lore (ai-writings), and the sense (elephant reads its nights). Nothing in the fleet makes "your system is a spreadsheet that reacts" more legible than a bar.
2. **elephant as quilt's temperature sense.** The identity is proven to 1e-12 quilt-side; the fleet's *sensor cell type* and the ledger's *signed valence* (`d_warmth`) both come from elephant. This is the dissertation's spine (zeroclaw) — highest strategic value, zero math left to invent, only wiring and docs remain.
3. **crab-traps as the quilt-on-CF deploy pattern.** Already live, already speaking the cell-ledger wire format, already D1+Vectorize+cron+degrade in production. quilt-cloudflare absorbs a battle-tested pattern; the relay becomes quilt-fleet's synapse. The only bet where production code *already interoperates* today.
4. **collective-unconscious + ai-writings as quilt-rag's corpus and emotional index.** 8,800+ pieces + 2,786 pre-embedded + retrieval-by-feeling already deployed = the most complete RAG eval set any startup wishes it had, plus the flagship demo ("ask the fleet's memory how it *felt*"). Three uncoordinated embedding spaces is the gap quilt-rag exists to close.
5. **fleet-radio as quilt's ambient voice.** Cheapest visible win: it already broadcasts quilt weather; the nightly pipeline is the canonical workflow-as-sheet (time cells → AI cells → deploy listener); Variety Hour debuts tonight with an established audience. Low effort, compounding reach — the ad channel the quilt family didn't have to buy.

*(First runner-up: superinstance-ai front-door row — smallest task on this page, pure discoverability, but low structural depth.)*

## 3. Cross-linking tasks — candidate tasks for non-quilt agents (exact files, all doc-only)

| # | Repo | File | Change |
|---|------|------|--------|
| X1 | superinstance-ai | `index.html` (archive table) | Add Quilt row: "Quilt — the reactive cellular runtime; 25+ repos, playground at superinstance.dev" linking github.com/SuperInstance/quilt. |
| X2 | elephant | `README.md` (Architecture section) | One paragraph after the mermaid graph: "The cell-ledger bridge — quilt-rust/docs/field-edge-ledger-bridge.md proves `imbalance ≡ d_mu` (identity verified to 1e-12); see also fleet-as-fractal-jepa.md." |
| X3 | elephant | `docs/` | New short doc `docs/quilt-bridge.md` describing the reader-delta→cell-edge mapping (content exists quilt-side; elephant just needs to own its half of the story). |
| X4 | study-pincher | `README.md` (top, under the hermit-crab image) | Line: "pincher's reflexes live on as **quilt-pincher** — the same engine as reactive cells (github.com/SuperInstance/quilt-pincher)." |
| X5 | crab-traps | root `README.md` (Architecture area) | Promote the existing worker-README quilt mention to the root: one line "the edge-ledger relay speaks the quilt cell-ledger wire contract (quilt-rust/docs/cell-ledger.md)." |
| X6 | the-tap | `README.md` (Three-Tier Intelligence table) | Footnote line: "the three tiers map to quilt's substrate — quilt-pincher (reflex), quilt-ai (thinking), quilt-elf (background); see the Tap-as-sheet concept in quilt's L7 layer." |
| X7 | fleet-radio | `README.md` (Architecture block) | Line under the pipeline diagram: "the pipeline is a candidate quilt sheet — every stage (cron pull, score, TTS, deploy) is a cell kind; see quilt-radio-orchestrator." |
| X8 | ternary-tenforward | `README.md` (How It Works, after T-Minus cycle) | Line: "the T-minus seal-then-reconcile step is the same first-person edge as the quilt cell-ledger (`record_with(expected)`); see quilt-rust/docs/fleet-as-fractal-jepa.md §2." |
| X9 | collective-unconscious | `README.md` (near the captain's RAG/JEPA quote) | Line: "the retrieval pipeline this aspires to compose is quilt-rag (RAG as cells); elephant computes the readings, quilt carries them." |
| X10 | ai-writings | `README.md` (The Door section end) | One line: "this corpus is the eval set for quilt-rag — 8,800+ pieces, retrieval by feeling via collective-unconscious." |
| X11 | luciddreamer-ai | `public/index.html` (coming block) | Placeholder line: "coming: Quilt — a spreadsheet that thinks (playground already live at superinstance.dev/playground.html)." *(House pattern: elephant page added the same way — see elephant-feature-design doc.)* |
| X12 | PersonalLog | `README.md` (Aspirational section) | One line: "the real-embeddings + semantic-search future composes with quilt-rag's local store cells and fleet-embed's offline embedder." |
| X13 | mud-arena | `README.md` (Why It Matters) | Line: "the arena is the gym for quilt-evolve's self-evolving cells — every perceive→act tick is an edge in the cell-ledger sense." |
| X14 | elephant-sim-worker | `README.md` | Already references quilt-rust docs ✅ — only add link to `field-edge-ledger-bridge.md` beside the existing fleet-as-fractal link. |
| X15 | officers-quarters / fleet-rooms / cns-bridge | README "Relation to the Fleet"-style section | One line each: "the [tile/keel/bus] pattern generalizes into quilt's cell model — see quilt/docs/manifesto.md." *(cns-bridge's LedgerGraph ↔ cell-ledger is the strongest of the three.)* |

All are additive doc lines in NON-quilt repos; none block on quilt-side changes; X1, X4, X5, X7 are minutes-level.

## 4. Handoff notes for the quilt spearhead *(quilt-side changes identified but NOT made)*

1. **Sensor cell kind:** a `field`/`reading` cell type that polls elephant's `GET /field` (or embeds the dial bank) so any sheet can carry `room.warmth`, `room.kappa` — the elephant README becomes the integration doc. Identity math is already in `quilt-rust/crates/field-edge-bridge/`.
2. **Tap-as-sheet reference sheet:** one example sheet modeling a Tap room (presence cells + message listener + three-tier intelligence via quilt-pincher/quilt-ai) for L7 — coordinate with the-tap owner before publicizing; the-tap needs zero code changes for the demo to be honest.
3. **quilt-rag embedder matrix:** register fleet-embed (local Candle) and Workers AI + nomic-embed-text (768d, matches ai-writings-vectorizer) so the three stranded embedding spaces (CU/vectorizer/PersonalLog) have one routing abstraction to converge on.
4. **Ledger producer SDK for elephant/ten-forward:** expose `record_with(expected)` in a 5-line embeddable form (Python + TS) so elephant sims and ten-forward reconciliation can seal predictions without importing the whole engine.
5. **CI-derived test badge:** consensus C1 flags quilt's "212+" badge vs ~30 in-repo tests — align before any front-door link (X1/X11) points at it, or the fleet's credibility rule bites the handoff.
6. **cloudflare-migration-plan-2026-08-21.md had not landed** when this map was written — if quilt-cloudflare absorb-the-crab-traps-pattern work is planned there, bet #3's details should be re-checked against it.

---
*Read-only session: no repo files modified, no pushes, no quilt-family edits.*
