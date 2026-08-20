# JEPA-RAG Scout — Reference Doc (cold, exact)

*Scout: reference subagent · 2026-08-19 · Source: `/home/eileen/projects/elephant`*
*Primary files: `elephant/jepa_rag.py` (~700 lines), `docs/jepa-rag.md`, `tests/test_jepa_rag.py`, `docs/jepa-zeitgeist-2026-08-17.md`, `docs/jepa-cross-pollination-map.md` (G0 gap).*

---

## 1. SCHEMA — the moment and the hit

A **moment** is a plain dict, ingested by `JepaMemory.ingest()` (`elephant/jepa_rag.py`):

| field | type | what it carries | provenance |
|-------|------|-----------------|------------|
| `text` | str | the shadow — witness words (transcript chunk / bar line / joined room message trail) | required, must be non-empty (else `ValueError`) |
| `readings` | dict[str, float] | the JEPA reading vector — what the room FELT | **computed by the dial bank, never hand-set**; partial dicts allowed, missing dials read 0.0 (vector origin) |
| `ts` | float | time stamp — "when" | `moment_from_text`: default 0.0 · `moment_from_room`: default **last message's ts** · `moments_from_markdown`: **synthetic — `base_ts + chunk_index * step` (default step 300s)** — encodes chunk ORDER, not wall-clock |
| `space_id` | str | space stamp — "which room" | caller-supplied; default `"unspecified"` |
| `meta` | dict | anything else worth riding along | caller-supplied (e.g. `{"source": filename, "chunk": i, "name": "dawn watch"}`) |

**The 9 dials** (`JEPA_DIAL_NAMES` = `DEFAULT_DIALS` order in `elephant/dials/__init__.py`; dim order matters — it is the vector layout):

1. `mood` (±) · 2. `volume` · 3. `earnestness` · 4. `cynicism` · 5. `joke_landing` (±) · 6. `panic` · 7. `presence` · 8. `model_vs_code` · 9. `vision`

(NB: `dials/__init__.py` docstring says "eight dials" but ships 9 — the bullet list omits `vision`; the code is 9.)

**Index structures** (`JepaMemory.index()`, numpy only, rebuilt lazily on change):
- `_vectors` (N×9) raw reading matrix · `_unit` (N×9) L2-normalized
- `_fields` (N×2) = `[warmth, concentration κ]` per moment (from `RoomField`)
- `_ts` (N,) · `_spaces` (N,) object array · `_tf` (N×V) dense bag-of-words term-frequency matrix
- No learned embeddings, no vector DB. `top_k=None` = every matching moment, ranked.

**MomentHit** (dataclass, returned by every query): `text, readings, ts, space_id, meta, score, vector (np.ndarray N×9), index` + helpers: `.field` (RoomField), `.warmth()`, `.board()` (one-line readout: score, warmth, κ, mood, panic, space, ts), `.reading_line()` (all 9 dials in order). The canonical full vector rides along even if ingested partial (`_hit()` merges).

**Reader / arrival stamps: ABSENT.** No reader identity anywhere in the moment schema. `moment_from_text` synthesizes `Message(author="[witness]")`. The reading is "the default DialBank's reading of the text", not any identified agent's (Personal-Elephant vs Room-Elephant from `presets.py` is NOT used by jepa_rag — no per-reader tagging). `ts` is a single float; message-level arrival order inside a room is collapsed into the joined shadow.

---

## 2. RETRIEVAL — how query_field (and kin) work

All queries return ranked `MomentHit`s. Math: numpy cosine / masks only.

| query | mechanics (exact) | notes |
|-------|-------------------|-------|
| `query_text(q)` | bag-of-words cosine vs `_tf`, **zero-overlap moments masked to `-inf`** (no shared words = no evidence = not a hit) | the normal-RAG way |
| `query_readings(profile)` | dict of dial→float: **cosine in JEPA space** via `_unit @ (q/‖q‖)` — raw cosine, **negative = anti-aligned feeling (honest)**; unspecified dials read 0.0 · dict of dial→(lo,hi): **range constraints** — rank by fraction of dials inside bounds ("mood > 0.6, panic < 0.2" literal; a panicky moment can never sneak in via proximity) · accepts RoomField / vector too | THE first-class-citizen query |
| `query_field(field)` | **exact alias of `query_readings`** — nearest neighbors in JEPA space ("the perfume query": moment that felt most like this field / right now) | named for the use, same cosine |
| `query_time(window)` | **hard filter**: moments outside `(start,end)` excluded; inside, ranked `1 − |t−center|/(span/2)` (proximity to center); single float = exact match | `top_k=None` = whole window |
| `query_space(space_id)` | **hard filter**: only that space; ranked newest-first — `(ts−tmin)/span` — the **recency** score (1.0→0.0) | "what did the wheelhouse feel like?" |
| `query_combined(parts, weights)` | weighted sum: `w_text·text_sim + w_readings·reading_sim + w_time·time_prox + w_space·space_match`; defaults **readings 0.5, text 0.3, time 0.1, space 0.1**; renormalized over present dims; each dim clipped [0,1]; **space & time are SOFT here** (wrong-space scores 0 but can still rank on other dims) | the captain's "alongside" |

Frequency/velocity context (zeitgeist/cross-pollination map): the retrieval side itself has no frequency/velocity mechanics — the only stamp-derived ranking is **recency** in `query_space`. Frequency/velocity live upstream in the dials (`room.density()` messages/min → panic/volume; acclimation rate = attunement's velocity, P9) and feed the readings, not the retrieval index.

**Honesty guarantee (tested, `test_hits_carry_their_terrain_context`):** every query type returns hits carrying the full reading vector (all 9 dials), space_id, meta, and text — the witness with its terrain. The reading is **computed, not hand-set** (deterministic dial bank over the shadow), so a hit's vector is reproducible/auditable.

---

## 3. HONESTY GAP — what it can vs cannot guarantee

**Can guarantee (moment-level provenance):**
- The hit's reading vector was **computed by the dial bank from the stored shadow** at ingest (reproducible, auditable, not vibes).
- **Which space** (room): `space_id` rides on every hit. ✔
- **Which time** (coarse): `ts` rides on every hit — but see the caveat: for markdown-chunked transcripts, ts is **synthetic chunk order** (`base_ts + i·step`), not true event time. Only room-built moments carry a real message ts.
- Retrieval honesty: raw cosine can be negative (opposite feeling); range constraints are literal; `top_k=None` shows the whole room; zero lexical overlap never ranks.

**Cannot guarantee (the gap):**
- **Which reader / whose reading**: no reader identity is stored. The reading is "the default bank's read" — in zeitgeist terms it is neither tagged Room-Elephant nor Personal-Elephant; you cannot retrieve "the moment as the captain felt it" vs "as the welder felt it". One anonymous, objective-ish read per moment.
- **Which edge / which transition**: moments are isolated state snapshots. There is **no `field_before`/`field_after`**, no delta, no step size. You can retrieve "a moment that felt panicky" but never "the moment the room *went* warm→cold", never "the felt size of the change", never "who pulled whom" (that is G0, the fleet's missing hippocampus, per `jepa-cross-pollination-map.md`).
- **Order-of-arrival**: not logged. Message-level arrival is collapsed into the joined shadow; `ts` is one float; synthetic for chunked files. G0 says explicitly: no repo logs order-of-arrival/event-time — charisma (room→agent vs agent→room) stays poetry.
- **Presence masks**: `presence` is a single scalar dial (pheromone trace), not a mask/set of who was present. You cannot retrieve "moments with the welder present but the watch absent".
- **Ground-truth claim**: readings are the bank's deterministic function of the text — it can claim "the bank read it this way", never "the room objectively was this way" (that is exactly the zeitgeist distinction, and JEPA-RAG sits on the un-credited side of it).

---

## 4. GAPS vs the EDGE framing — delta table

| edge-framing requirement | current JEPA-RAG | delta needed |
|---|---|---|
| `field_before` / `field_after` edges | ✗ **absent** — snapshots only; `_fields` (N×2 warmth/κ) describes the moment itself | store `field_before` + `field_after` reading dicts per moment (or per consecutive pair), index both |
| felt size of step | ✗ **absent** — no delta anywhere | `step = field_after − field_before` (per-dial vector) + scalar `‖step‖`; index in a step matrix |
| retrieve BY edge (start, end, step) | ✗ no edge query — `query_field` is nearest-state, not nearest-transition | new `query_edge(step_profile)` = cosine over step vectors (or range constraints per dial, same idiom as `query_readings`); `query_edges(before_field, after_field)` for start+end |
| reader identity | ✗ **absent** — default DialBank, `[witness]` author, no agent id | add `reader_id` (or `readings_by_reader`) to the moment; wire PersonalElephant per-reader readings from `presets.py` |
| presence masks | ✗ `presence` is a scalar dial | add `present: set[agent_id]` / mask vector to the moment; query by set overlap |
| order-of-arrival | ✗ **absent** — `ts` synthetic in chunk path; message order collapsed | log `arrival_seq` + event-time vs arrival-time per message (G0); keep `ts` as event time, add arrival as separate field |
| stable identity | ✗ moments have only positional `index`; no ids, no links | add `moment_id` (and `prev_id`/`next_id` or a transitions table) so edges are addressable |

**Minimal schema extension to retrieve BY EDGE (not moment):**
1. `moment_id: str` (stable id; `prev_id` for chain).
2. `field_before: Dict[dial,float]` + `field_after: Dict[dial,float]` on the moment (the dial bank already reads any Room — the machinery exists, only the two-state capture and storage are missing).
3. `step: Dict[dial,float]` derived at index time (`field_after − field_before`), stored as an (N×9) step matrix beside `_vectors`.
4. `reader_id` (who read it), `present: set[agent_id]`, `arrival_seq` (order-of-arrival).
5. New `query_edge(profile)` — same cosine/range mechanics as `query_readings`, but over the step matrix; `MomentHit` gains `field_before`, `field_after`, `step`.

No new infra needed: numpy matrices already pattern-match; the gap is schema + one matrix + one query + capture-at-ingest of two consecutive fields. (This is also G0's "cheapest of all" enabling move — timestamp fidelity, no new ML.)

---

## 5. VERDICT (one paragraph)

JEPA-RAG today is an **honesty guarantee for moment retrieval, and an honesty aspiration for provenance** — specifically for relational/edge provenance. What it guarantees is real and tested: retrieval by feeling as a first-class dimension, and every hit carrying its computed (not hand-set) reading vector plus space and time stamps — the witness with its terrain, reproducible and auditable. What it cannot do is the fleet's actual honesty question: **whose** reading (no reader identity), **which step** (no field_before/field_after, no felt size of change), **what order** (no arrival fidelity), **who was there** (no presence mask). On the moment axis it is honest; on the edge axis — the axis the fleet's social observables (charisma vs acclimation, "who pulled whom") actually live on — it is aspiration: G0, the missing hippocampus, is still missing from the schema, and the code's own docstrings ("retrieval by feeling") cannot close a gap the schema was never asked to carry.

---

## SUMMARY (5 lines)

1. **Schema:** moment = {text, readings (9 dials: mood, volume, earnestness, cynicism, joke_landing, panic, presence, model_vs_code, vision — computed by default DialBank, not hand-set), ts, space_id, meta}; no reader id, no arrival order, no presence mask, no edges.
2. **Retrieval:** six numpy queries — text (BoW cosine, zero-overlap excluded), readings (raw cosine or literal (lo,hi) range constraints), field (alias of readings, the perfume NN), time (hard window, proximity-ranked), space (hard filter, recency-ranked), combined (readings 0.5 / text 0.3 / time 0.1 / space 0.1, renormalized, space+time soft); every hit = MomentHit with the full vector riding along.
3. **Honesty gap:** guarantees space stamp, computed-reading provenance, and whole-room visibility (top_k=None); cannot say WHICH reader felt it, WHICH edge/transition, in WHAT arrival order, or WHO was present — ts for chunked transcripts is synthetic chunk order.
4. **Edge deltas:** missing field_before/field_after, step vector, reader_id, presence mask, arrival_seq, moment ids — minimal extension = capture two consecutive fields at ingest, derive step matrix, add `query_edge` (same cosine/range idiom) — no new infra, G0's cheap move.
5. **Verdict:** honesty guarantee on the moment axis (tested: every hit carries its terrain), honesty aspiration on the edge axis — the fleet's "who pulled whom" question remains poetry until the schema carries edges, readers, and arrival order.
