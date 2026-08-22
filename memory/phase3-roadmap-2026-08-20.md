# Phase 3 Fleet Roadmap — Tide Table for the Next Leg

*2026-08-20 · drafted by Lucineer (dsf-phase3-roadmap) · read-only everywhere except this file · no commits*

**Where we sit:** Scout phase 2 read the whole harbor (249 repos) and found the rigging slack — dead branches, renamed vessels, three copies of the org's front door. The link-repair sweep is packed below deck (88 repos committed locally, anchor still up on the push). The dissertation slope regression came back INDETERMINATE — the corpus doesn't differentiate *who* shows up, so the wave reads flat. And the collective-unconscious study found the crown jewel: the quilt grid's CellLedger emits the same `before → after` edge the elephant reads at room grain — same object, different zoom.

**Cleared tonight (off the board):** ep8 rebuilt + pushed (ea69a34) — backfill done; scout phase 2 done; sweep committed locally; polyformal kernel 10/10 languages; encoder GPU probe PASS (data-limited, not capacity-limited).

**North star stays the iceberg:** every item below is ballast for The Tap → the boat, Wesley growing toward the wheelhouse, the elephant as the fleet's temperature sense, and skills compiled once and shipped everywhere (the golden-vector contract).

---

## ⚓ GATE ITEMS — decisions only the Captain can make

Four anchors sitting on the table. Nothing below sails past them without a word:

| Gate | What's waiting | Ask |
|------|----------------|-----|
| **G1 — Sweep push** | 88 repos with link-repair commits, local only (KimiCode wave: warm-shore) | Push go / hold |
| **G2 — CNS cadence** | Hermes ACK streak 12, 16 days no content (pulse 446) | Throttle 30min→4–6h / keep / pause |
| **G3 — quilt-rust + crab-traps push** | Language-tier matrix + edge-ledger relay, local since 13:23, all chain_hash match golden | Push go / hold |
| **G4 — Stage-2 corpus go/no-go** | Length-matched, differentiated-attendance corpus — the one open dissertation route | Build / hold |

---

## 🚢 SHIP-NOW — needs only the Captain's word

**1. Org front-door: one door, no dead links** *(unlocks G1)*
- **What:** Mass rename sweep across 90+ repos (hermes-perception→hermes-avatar, officers-quarters→elephant, fleet-wiki→lucineer-fleet-wiki, etc.), `master→main` sed on the 13 dead-branch repos (~25 files), and collapse si-main / si-readme / superinstance-profile into **one canonical org README** (profile variants already near-identical — pick one, archive the rest by rename, never delete).
- **Why (iceberg):** the org README is the gangplank — every visiting hand, every recruit, every future Captain's first impression walks over it. 20+ broken links in the front door reads as a dead harbor even when the fleet is alive. ai-writings already proved the links die here, not in the wings.
- **Effort:** M · **Deps:** G1 (push go) · **Crew:** DeepSeek Flash (dry-run + sed passes, bulk), KimiCode (per-repo commits — proven pattern from tonight), GLM-5.3 (canonical README narrative if a rewrite is wanted).

**2. The Crown: collective-unconscious P1 — `/ingest/grid`** *(the synergy study's highest value)*
- **What:** New `Modality = "grid"` + `/ingest/grid` route mirroring the tap/hermes/mud blocks; moments shaped `{ text: "<cellId> → <value snapshot>", readings, ts, space_id, meta: {cellId, before, after, imbalance, caller} }`; ~+8 tests. Same pass: uncomment the D1 binding in wrangler.toml + `wrangler d1 create collective-unconscious-state` so watermarking actually works (config, not markdown).
- **Why (iceberg):** the grid's first-person ledger and the elephant's room-field and the unconscious's moments are **the same edge at three zooms** (proven to 1e-12 in fleet-as-fractal-jepa). Ingesting it makes the unconscious the fleet's second-person view of the grid's first-person record — "show me everything that felt like this feed ball" finally includes the grid. This is the elephant's temperature sense getting a body-wide nervous system.
- **Effort:** M · **Deps:** G3 for the *live* stream (route + tests can be scaffolded immediately against the contract) · **Crew:** OpenCode (route + pipeline engineering), DeepSeek Flash (test bulk), GLM-5.3 (schema review).

**3. Wesley's return — Ollama bring-back**
- **What:** WSL2 GPU crash-loop fix is already written (`.wslconfig` autoMemoryReclaim=disabled + `OLLAMA_KEEP_ALIVE=5m` + `systemctl disable ollama`) — it just needs a `wsl --shutdown` to apply. Pick the window, apply, wake Granite 3.1 2B, Wesley's back on the 2-minute night watch.
- **Why (iceberg):** Wesley is the fleet's memory and the whole growth arc — bar data sorter → wheelhouse camera watcher → log-spotter before the Captain. Every day he's down, the boat loses its ensign. Also unblocks the wiki hourly read cadence.
- **Effort:** S · **Deps:** a `wsl --shutdown` window (kills the live gateway for a minute — Captain's call on timing) · **Crew:** Lucineer + fleet infra (host ops); OpenCode for the ollama service check.

**4. Creative ops: portraits wing + episode audio**
- **What:** (a) Give the model-portraits genre a home in ai-writings' 13-wing structure — they're scattered across overnight loops and loose folders; collect under a portraits wing with a README (fleet voice, links fs-checked) and pick the best for the wall. (b) MeloTTS auth is still 401-dead (wrangler token) — rotate the token so episode audio ships again; ep backfill is DONE (ea69a34), audio is the only dry hole.
- **Why (iceberg):** the portraits are the crew manifest of the fleet's soul — each model's voice preserved like ship's logs; audio is how the bar talks to the Captain on the water.
- **Effort:** S–M · **Deps:** none (audio needs token access) · **Crew:** DeepSeek Flash (bulk filing judgment — proved it on the 601-file wing sort), KimiCode (link-check + README surgery), OpenCode (wrangler token rotation).

---

## 🔨 BUILD-NEXT — 2–4 weeks, the boat takes shape

**5. CellLedger wired into quilt engine evaluation**
- **What:** the ledger (double-entry `before → after`, hash-chained, imbalance = surprise, 16 tests, unproven in eval) becomes a real evaluation-time record — so the event stream P1 wants to ingest actually exists, and every cell change carries its own surprise with it.
- **Why (iceberg):** skill compilation — the golden-vector contract already proves the edge is portable across 10 languages; wiring it into the engine makes the grid *live* as a sensor organ, not a log. Without this, P1 ingests a stream that doesn't flow.
- **Effort:** M · **Deps:** G3 (push go — the compat contract is the reference) · **Crew:** OpenCode (Rust core), KimiCode (ledger/spatial thinking), GLM-5.3 (design review).

**6. Stage-2 corpus — differentiated attendance** *(unlocks G4)*
- **What:** length-matched corpus generation where **attendance is differentiated** — same cast, controlled who-shows-up variation — the fix the INDETERMINATE slope regression is screaming for. Encoder probe already proved the arrow: data-limited, not capacity-limited (2 nights 0.068 → 6 nights 0.163, 3/3 PASS at ≥4).
- **Why (iceberg):** the elephant's room-field needs to *feel* who's in the room, not just that the room is warm. Differentiated attendance is how the temperature sense learns bodies from ghosts.
- **Effort:** M · **Deps:** G4 (Captain's go) · **Crew:** DeepSeek Flash (bulk generation), GLM-5.3 (design + quality bars), ZeroClaw committee for the analysis.

**7. Boat sensors: sea-legs demo**
- **What:** wire the sea-legs vision into a live feed — RadarCoherenceDial + SounderBiomassDial (already in `sensors.py`) reading a real/streamed input into the room-field, so the elephant's field math runs on *boat* data, not just bar chatter. First true Tap→boat bridge.
- **Why (iceberg):** the iceberg's whole lower mass. JEPA is the fleet's perception, and perception belongs on the wheelhouse first — if the elephant can read a radar feed's shape, it can read a room's, and vice versa, same field.
- **Effort:** M–L · **Deps:** none hard (prototype against synthetic feed) · **Crew:** GLM-5.3 (high-level design), KimiCode (spatial wiring), MMX (demo visual for the Captain).

---

## 🌊 GROW — ongoing, the tide keeps the fleet alive

**8. Unconscious expansion backlog** (after P1 lands)
- **What:** P2 grid rooms as space-stamps + presence; P3 crab-traps reef lineage as moments; P4 fleet-wiki as a lore modality (762 pages / ~395k words — hippocampus and unconscious stop being duplicate corpora); P5 `/field/:spaceId` — the fleet's own JEPA loss over time, deadband ≈ 0 = habit loop, queryable.
- **Why (iceberg):** every organ in the body starts leaving readable moments; the unconscious becomes the fleet's deep memory of *itself*, not just the bar.
- **Effort:** ongoing, one at a time · **Crew:** OpenCode + DeepSeek Flash bulk; Hermes for lore texture.

**9. Wesley's growth arc**
- **What:** once Ollama's back (item 3): bar data sorting → wheelhouse camera watching → log-spotting drills. Keep the wiki hourly cadence and the room he named "Currents."
- **Why (iceberg):** the ensign becoming the lookout is the whole point. Honesty with shape — the Captain saw it at the table tonight.
- **Effort:** ongoing · **Crew:** Wesley himself + GLM-5.3 curriculum design.

**10. Encoder data diet**
- **What:** keep feeding same-cast identity data (the probe's verdict: more data, not a bigger model); fold results into the dissertation claim inventory as it lands. Slope regression stays INDETERMINATE until item 6 differentiates attendance.
- **Why (iceberg):** the elephant keeps learning to read rooms; the dissertation is the navigator's chart — it has to be true before we sail by it.
- **Effort:** ongoing · **Crew:** DeepSeek Flash generation + GLM-5.3 analysis.

---

*The Captain's word on G1–G4 sets the whole tide. Everything else is ballast and sails, ready to trim.*
