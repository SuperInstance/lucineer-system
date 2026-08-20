# Devil's Advocate — Second Pass: the EDGE Framing

*2026-08-19 · Fleet doctrine review, adversarial pass 2.*
*Target under attack: the first pass's reframing — "conversations are EDGES, not rooms; field_before → field_after; sameness = matched displacement geometry; collinear walks = same push direction; charisma/acclimation become the retrieval key."*

Sources weighed: `elephant/elephant/field.py`, `room.py`, `presets.py`, `dials/`, `tapnight.py`, `jepa_rag.py`, `nudge.py`, `docs/jepa-rag.md`, `docs/jepa-zeitgeist-2026-08-17.md`, `fleet-jepa-midi/research/elephant-sense-v3-design-2026-08-17.md` (probe numbers §8), and the first pass `devils-advocate-conversation-temperature.md`.

---

## 1. VERDICT

**STANDS-WITH-CONDITIONS — and the conditions are pre-registered, currently failing, and load-bearing. On the numbers the doctrine already has (fine gap 0.015 < noise floor 0.05), the edge framing is de facto FALLS today: its central object is a quantity the doctrine's own decisive experiment measured at statistical zero. It survives only as a renamed room-snapshot system, unless and until the deadman switch in §3 fires the other way.**

The first pass did something quietly self-cancelling. It killed "conversation temperature" on the ground that *within-room ordering is retired and within-room contrast is invisible* (citing the 0.015 fine gap), then rebuilt the replacement *on that exact within-room quantity* — the displacement `field_before → field_after` *inside a room over time*. The word "edge" did the laundering. In the doctrine, the edge is **cross-room**: `μ̂_B − μ̂_A`, walking from sauna to plunge, gap 0.271 — real, felt, large. The reframing borrowed that legitimate name and pasted it onto the *within-room* drift, which is the 0.015 — the thing the probe says is noise. The cross-room edge was never in doubt and is already served by room-snapshot retrieval; the within-room "edge" is the only thing that would make conversation-retrieval *distinct* from room-retrieval, and it is precisely the part that does not exist yet.

This is decisive, not nuanced: **the framing is a correct and doctrine-native *idea* — an edge is the only thing that could separate "galley fight" from "galley coffee" (same start field, different edges) — but it is an idea about a vector no shipped system computes, compared by a metric that deletes the one quantity the idea needs, and gated on a measurement that is currently below noise. The idea is right; the object is empty.**

---

## 2. Attack lines

### 2.1 The edge is the retired within-room objective wearing a new name

The doctrine retired within-room ordering because "the elephant is invisible from inside a room" (v3 §0), and the probe confirmed it: the fine sauna/plunge gap (which trades-night) is **0.015** — statistical zero — while the coarse cross-room gap (speech vs music) is **0.271**. The first pass cited exactly this to kill the naive claim. Then it defined a conversation as `field_before → field_after`, i.e. a *within-room temporal displacement* — the very 0.015. The cross-room "edge" (0.271) is already covered by room-snapshot retrieval and needed no reframing; the within-room "edge" is what would make conversation retrieval distinct from room retrieval, and it is the quantity the doctrine already measured at zero. **The reframing resurrected the retired objective and called it the salvage.** If the edge is cross-room, it's not a conversation, it's a room walk; if it's within-room, it's the retired target. There is no third reading.

### 2.2 μ̂ does not exist in the shipped system — the "edge" is a displacement of a vector nothing computes

The reframing's edge is `μ̂_after − μ̂_before`, a von Mises–Fisher *mode*. But nothing runnable produces μ̂. `field.py` ships `warmth()` (a fixed-weight scalar projection) and `concentration()` (a `norm(vector − 0.5)·2` proxy the README confesses "measures extremity, not yet temperature"). `JepaMemory`'s field matrix is literally **2-D `[warmth, concentration]`** (jepa_rag.py: `self._fields = np.zeros((0, 2))`). There is no vMF MLE, no κ-as-MLE, no μ̂ anywhere in executable code — they live only in the v3 *design doc*. So "matched displacement geometry" is, in any system that actually runs, a **2-D delta (Δwarmth, Δκ)** — and one of those two axes (κ) is the self-confessed-broken proxy. The framing is a dissertation arguing about a vector that no interpreter ever builds. It must either ship μ̂ first, or admit the "edge" is a two-scalar delta, one of whose scalars is known-broken.

### 2.3 `distance()` discards magnitude — the "felt size of the step" is unrepresentable

The coda celebrates "where they start, where they end, and the **felt size of the step** between." But the only distance metric on offer, `RoomField.distance()`, normalizes both fields and returns `‖a − b‖`: **pure direction, magnitude deleted**. A whisper and a scream in the same dial direction are the "same edge." The single quantity that would separate "a fight" (large displacement) from "a quip" (small displacement) — the step *size* — is exactly what `normalize()` throws away. "Sameness = matched displacement geometry" needs both direction *and* magnitude; the metric keeps only direction. Either the framing admits its geometry is direction-only (and then a fight and a sigh are indistinguishable), or it specifies a new metric it has not built.

### 2.4 Collinearity across rooms is ill-defined — heterogeneous dial bases, κ scales, presence masks

"Collinear walks = same push direction" presumes two displacement vectors live in the same vector space. They do not. Two edges live in rooms with different `DIAL_BOUNDS` (mood/joke_landing ∈ [−1,1]; volume/earnestness/cynicism/panic/presence ∈ [0,1]), different `DIAL_CENTER` (earnestness/presence rest at 0.5, everything else at 0), different κ scales (a "loose" κ = 0.5 in a sauna is not the same tightness as κ = 0.5 in a cold plunge), and — per the doctrine's own rule — different presence *masks* (presence is a mask, never a feature; two rooms with different occupants aggregate their displacement over *different attended subsets*). Which 7-vector is "collinear"? The raw delta — then per-axis scale heterogeneity makes "same direction" mean +0.3 mood (a third of its range) vs +0.3 panic (a third of its range but semantically a stampede) and the comparison is apples-to-oranges. The unit delta — then the step size is gone (attack 2.3). The framing never says, and cannot, because the affine frames differ. **Collinearity across a sauna and a plunge pool is a metaphor, not a metric.**

### 2.5 Charisma/acclimation as the retrieval key is a popularity-of-people index — the zeitgeist conflation re-entering as "charisma"

The charisma observable is `⟨ μ̂_after − μ̂_before , unit(e_agent − μ̂_before) ⟩` — the room's displacement projected onto the direction of a *specific person*. Keying retrieval on that is keying retrieval on **"which person moved the room,"** a popularity-of-people index, not a temperature-of-room index. And it is frequency-weighted by construction: `charisma_pull` scales with interactions (`s = 1 − e^(−charisma·n)`, tapnight.py), so the busiest speaker produces the largest edge and dominates retrieval. That is the busy ≠ warm conflation the first pass quarantined under the name "zeitgeist" (§2.4) — now walking back in through the door labeled "charisma." The thermometer has become a who-moved-the-needle leaderboard, and the retrieval key is an attention-economy statistic about people wearing a field-theory coat.

### 2.6 Cold-start: edges need two snapshots, so single-message and field-invariant conversations are unretrievable by construction

An edge is before→after. A one-message conversation has no "before." A conversation that never perturbs the field (two people quietly agreeing over coffee) has edge ≈ 0 — indistinguishable from the noise floor. So edge-retrieval is structurally blind to exactly the conversations that *don't* move the field, which the doctrine says is most of them ("the elephant is invisible from inside a room"). The framing silently privileges long, eventful, field-moving conversations and makes stillness unretrievable — a memory with a hole in the shape of most nights. Worse: `JepaMemory.ingest()` already *requires* non-empty text, and a single message is a *point*, never an edge — so the framing's own storage substrate cannot even hold the object it claims to retrieve.

---

## 3. THE DEADMAN SWITCH SPEC

Pre-registered now, executed before any dissertation prose is drafted. Five bullets, grad-student-executable:

1. **Threshold.** On the existing control — trades-nights 1–4 (same cast, same room, four nights) — the **fine room-gap must climb from 0.015 to ≥ 0.10** cosine (≥ 2× the ~0.05 encoder noise floor), with **speaker-heldout discrimination ≥ 0.50** (chance = 0.25). The single success sentence: *"fine gap 0.015 → X ≥ 0.10, speaker-heldout ≥ 0.50, within-room spread preserved (no collapse)."*

2. **Failure condition.** If, after the §2.3 contrastive head / fine-tune (fixed τ = 0.15, explicit within-room spread regularizer), the fine gap does **not** clear 0.10 in **three consecutive runs** — or clears it only by collapsing within-room spread to zero — the edge thesis is declared dead. "Clear margin above noise" means gap > 0.05 + 2σ of the encoder's per-pair distance distribution, not a one-run lucky crossing.

3. **Scope of the kill.** The deadman switch kills **only the conversation-as-edge retrieval layer** (edge-similarity as a retrieval key, charisma/acclimation as the primary key). It does **not** kill room-snapshot retrieval, moment-grain `query_field`/`query_readings`, or the cross-room edge (0.271) — those already run and become the fallback.

4. **Fallback thesis (pre-registered now, not retrofitted).** Collapse to **room-centroid / room-snapshot retrieval** — the first pass's §3.1. Retrieval unit = room-anchored vMF snapshot `(μ̂, κ)` + stamps; comparison = `distance()` **cross-room only**; a conversation is retrieved strictly as *the room-field over its time-window*, never as a vector, never as an edge. Within-room ordering stays retired, full stop.

5. **Is the fallback still a dissertation? YES — conditionally.** It is worth a dissertation **iff** it shows (a) cross-room retrieval generalizes beyond the speech-vs-music pole to genuinely distinct *speech* rooms, and (b) κ-as-true-vMF-MLE + the spread regularizer preserve within-room structure (no collapse). If it cannot show even (a), the fallback degrades to the already-shipped moment-grain `query_field` — a working feature, not a dissertation — and the honest deliverable is "the elephant was already built; here is the test harness." **Pre-register this now so the fallback does not quietly become a re-description of existing code wearing dissertation clothing.**

---

## 4. The one condition that would make me concede

Show me a **runnable** μ̂/κ field — real vMF MLE, not the `norm(vector − 0.5)·2` extremity proxy — in which a *within-room, same-cast* conversation measurably displaces μ̂ above the noise floor (fine gap opens ≥ 0.10, speaker-heldout intact, within-room spread preserved), **and** demonstrate that two conversations with *matched edges* (same start-field class, same signed shift, same Δκ) are retrieved as "the same felt event" across **two different rooms with different presence masks** — such that a galley fight retrieves *another fight*, and not merely *another galley*. If the edge is measurable *and* cross-room matched-displacement retrieval beats room-snapshot retrieval on a retrieval benchmark, I concede the framing is right — and it becomes the *better* dissertation than the fallback, because it is the only design that separates "what happened" from "where it happened." Until then the edge is a beautiful object that does not yet exist, and I will keep saying so.

---

## Summary (10 lines)

1. VERDICT: STANDS-WITH-CONDITIONS; on current numbers (0.015 < 0.05) it is de facto FALLS — a correct idea about an empty object.
2. The reframing laundered the *within-room* drift (0.015, noise) under the *cross-room* edge's name (0.271, real).
3. The edge is the retired within-room objective resurrected: cross-room = a room walk, within-room = the retired target.
4. μ̂ exists nowhere runnable — the shipped field is 2-D `[warmth, κ]`, and κ is the confessed-broken extremity proxy.
5. `distance()` normalizes and discards magnitude — "the felt size of the step" cannot be represented.
6. Collinearity across rooms is ill-defined: heterogeneous dial bounds, centers, κ scales, and presence masks.
7. Charisma/acclimation as retrieval key = a popularity-of-people index; busy≠warm re-enters as "charisma."
8. Cold-start: edges need two snapshots — single-message and field-invariant conversations are unretrievable by construction.
9. DEADMAN SWITCH: fine gap must hit ≥ 0.10 with speaker-heldout ≥ 0.50 in 3 runs, else collapse to room-centroid retrieval (still dissertation-worthy only if it beats `query_field`).
10. Concession condition: a runnable μ̂ where a same-cast conversation displaces it above noise, and matched edges retrieve a fight-not-a-galley across rooms.

---

*Devil's advocate, fleet doctrine review, second pass, 2026-08-19. One file written; no repo files modified.*
