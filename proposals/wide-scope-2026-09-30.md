# Wide-Scope Memo — 2026-09-30

Casey: "Be creative and wide in scope." Seven directions across scales, all snapped to what
today actually proved (antirank precision, XR-1 retention findings, scan verdicts, API split
teacher/local). Each has a cheap next move; none requires new spend.

## The unifier: the field is the artifact

Not a model file — a **field**: episodes + head weights + ambiguity map + sealed tape chain,
one portable artifact (working name `.jevfield`). Distillation = compile field → head.
JRAG = run field live (kNN over episodes, head for the rest). The ledger = sync fields
between boats. A page loads it in WASM, the lab loads it in python, a Worker loads it on CF —
one artifact, three substrates, provenance intact everywhere. Today's three threads
(distillery, JRAG, XR1-C sealing) are one spec wearing three hats.

## The seven

1. **Frontier distillation** — the student never sees easy cases. Curriculum = the field's own
   escalation frontier (boundary episodes only); easy states stay pinched forever. Test:
   frontier-only vs uniform distillation on tictactoe → student size needed for equal accuracy.
   Directly built from today's result that precision lives at boundaries.

2. **Distill the ROUTER, not just the answer.** The escalation policy itself is a student:
   predict "will neighborhood consensus hold?" from the room-embedding. Far smaller function
   than the judgment — candidate: tev1:0.8b or a logistic head. Collapses the pincher to
   ~zero cost; pre-registerable on CPU this week.

3. **Judgment holonomy.** Cowboy-fleet doctrine applied to fields: transport a grade around a
   loop of related states (A→B→C→A); if it doesn't return, the inconsistency is a *gauge
   defect* — a lesson the field hasn't learned, found with ZERO teacher calls. Loop-inconsistency
   as free audit + free curriculum. Cheap synthetic test: field with a known blind spot.

4. **Fleet judgment mesh.** Peer escalation: when my field can't pinch, it can route to another
   agent's field before spending teacher tokens. IE3's "cells dedicated, routing between" at
   fleet scale; cost–reliability frontier measured per hop. The fleet's brain grows from usage
   — superinstance-api is the natural host (pinch endpoint already exists).

5. **The CANON cell.** A standing jev auditor that grades every new RESULTS.md booking: "is the
   verdict supported by the numbers? is anything post-hoc?" quilt-research-canons flagged our
   receipt RED once — make that check a permanent organ, not a lucky scout. Runs via the
   proxy (books itself, naturally).

6. **Measurement-native jevs (quantum ladder, reframed).** Don't ask "can quantum do ML" — ask
   "what if the judgment IS a measurement": room-embedding = state preparation, question =
   measurement basis, noul = P(|0⟩). Gives H3 (Moth→IonQ recon) an actual question instead of
   a vibe. Recon stays cheap/read-only.

7. **Ship the ignorance map.** Ambiguity regions (persistent high-escalation areas) export as a
   first-class artifact next to the model: "what this jev doesn't know." It's the next
   teacher session's shopping list AND the privacy receipt. Nobody ships a model's ignorance;
   negative-space doctrine extended to weights.

## P-1 (already shipped): the corpus grows by using the teacher

`tools/systemone_proxy.py` — every /v1/systemone call HMAC-booked to
`~/.config/systemone/call-ledger.jsonl` (state, questions, answers, probabilities, usage,
latency). From today forward, the bench, the gates, and any ad-hoc grading all seed the
distillation corpus for free. `--stats` gives corpus vitals.

## Ordering

- Now: proxy live (done); ollama swap → nimble/tev1 bench (both become candidate students AND
  router-students via #2).
- Next CPU pre-reg: #2 router distillation (cheapest, feeds every lane).
- W5b2 lands → C5 → then #1 frontier distillation on the P0 game.
- #3/#5 as filler CPU items; #4 waits on superinstance-api wave-2; #6 = H3 recon reading.
