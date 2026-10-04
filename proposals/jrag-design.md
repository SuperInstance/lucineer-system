# JRAG — a growing judgment field (design + research brief)

*Drafted 2026-09-30 by Lucineer from Casey's brief: "a pincher-like system... a new type of embedding
agents... a JRAG — a synergy of JEPA and Jev in a novel growing system for building intelligence
from usage. Simple games first, building to more complex applications, successes and failures
guiding the progress."*
*Status: proposal + research brief. Companion to `quilt-distillery-design.md` (same-day).*

## The one-liner
JRAG inverts RAG: instead of retrieving *text* to condition a *generator*, it retrieves **lived
situations** (JEPA room embeddings grown from usage) to condition a **judgment cell** (Jev) — and
when the neighborhood can't answer, it pinches to a teacher and **compiles the new experience back**
into the field. Intelligence accumulates where the application actually lives.

## Why the synergy is coherent (each piece fixes the other's weakness)
- **JEPA** gives perception: an encoder trained to predict *representations* of future/adjacent
  states, not raw values — "temperature sense," the room's structure. Alone, it's just a good
  encoder with no memory and no decisions.
- **Jev** gives decision: graded typed answers (noul/choice/score) over a state. Alone, it's frozen
  at training time — it can't learn from what happens after deployment.
- **RAG (inverted)** gives memory: a growing field of episodes — (state-embedding → outcome, grade,
  tape hash) — that the jev conditions on. Alone, classic RAG just stuffs context into a chat model;
  here it feeds a judgment *cell*, so retrieval output is a grade, not prose.
- **The pincher** gives economy: if the k nearest episodes agree with known outcomes, answer from
  the field — zero teacher tokens, <50 ms. Only genuine novelty escalates, and the escalation
  *becomes* new field (compile-back). This is the superinstance-api reflex seam, grown a memory.

## Architecture
```
state x ──f_θ (JEPA-trained encoder)──▶ z (room embedding)
z ──▶ field lookup (kNN) ──▶ evidence E = {(zᵢ, outcomeᵢ, gradeᵢ, tapeᵢ)}
E + z ──▶ jev head g_φ ──▶ graded answers
pinch policy π: consensus(E) high → answer from field (reflex)
              : else → teacher T grades it → episode written back (growth)
periodic "sleep": consolidation — distill E into g_φ, tier/demote stale rooms,
                  continue JEPA pretraining of f_θ on replayed usage streams
```

## Growth mechanics (the novel core)
1. **Compile-back**: every escalated judgment lands as a new episode with its provenance tape
   (XR-1: values materialised → growth is fault-localisable; a wrong answer traces to the episode
   that taught it).
2. **Consolidation = the distillery's sleep phase.** The two same-day lanes *meet here*: JRAG is the
   runtime organ; quilt-distillery is its offline consolidation. Periodically, clusters of episodes
   are distilled into the jev head (weights absorb the neighborhood → generalization), the field is
   re-tiered (full/gist/hint, plato-style), and stale rooms demote with receipts. Hippocampus →
   cortex, on a schedule.
3. **Failures are first-class and stickier.** Retention weight favors failure episodes and
   pinch-boundary episodes — they define where competence ends. "Successes and failures guiding
   progress" is literally the retention policy, not a slogan.
4. **Two growth curves to steer by** (literature names): the ***escalation rate*** (our "pinch
   ratio" — % of situations answered from grown intelligence, should climb with usage; demoted to a
   diagnostic — see F3) and the ***cost–reliability frontier*** (teacher tokens per unit competence,
   should fall). When consolidation lifts agreement but escalation rate stalls, the frontier is
   generalization, not memory — and the next data collection targets the boundary (curriculum
   mining from the distillery design).

## Games ladder (simple → complex, each stage a real test)
- **P0 — tictactoe, usage-grown player/grader.** Encoder starts as a random projection (bright but
  knowing nothing); field starts empty. Play against the perfect solver: field consult → pinch on
  consensus → else solver grades every move (free, infinite, perfect teacher) → compile-back. Every
  N games: consolidation. State space is small (~5k reachable positions) so the escalation rate can
  saturate — that saturation curve is *half* the demo (competence approaching solver level while
  teacher calls per game decay to zero, field size bounded by consolidation). **But F3 (scan):
  saturation alone is obtainable as a coverage artifact via the escalation→density feedback loop —
  the P0 verdict REQUIRES a held-out generalization measure** (fresh opponent pool +
  consolidated-head-only play with the field detached).
- **P1 — connect4.** State space explodes; the field can never cover it. Now the JEPA encoder + jev
  head must *generalize* and the pinch ratio plateaus honestly below 100% — the plateau is the
  measurement of grown (not memorized) intelligence. JEPA pretraining on self-play streams earns its
  keep here.
- **P2 — hold'em tilt/spice jevs.** Hidden information: rooms must encode *uncertainty structure*;
  teachers = model roster (taste questions where disagreement is the product). Failure-heavy
  retention should shine where outcomes are noisy.
- **P3 — out of games.** i2i book routing, inbox triage, relay stimulus gating — the same organ on
  non-game usage; field lives in Vectorize (i2i-ledger pattern), head ships as wasm jev.

## Honest novelty check — SCAN VERDICT (2026-09-30, full scan: /home/eileen/scratch/jrag/jrag_prior_art.md)
**Partially novel — not named as a unit; every load-bearing piece is already named. Adopt the
literature's names and compete on measurements.**
- Closest authored system: **PinSieve** (arXiv:2608.24040) — grey-zone routing + escalation + a
  governed "memory flywheel." A reviewer would call JRAG "PinSieve applied to graded judgments."
- Per-claim: episode retrieval = CBR 4R cycle (Aamodt & Plaza 1994) + MFEC/NEC; judgment-as-
  retrieval-output = REIC (2506.00210); pinch/escalation = learning-to-defer + **R2V** (2605.16604,
  calibrated step-level escalation router — already trained); compile-back = CBR's **Retain** +
  retrieval-augmented RL (2202.08417, retrieves over experience then distils into parameters);
  sleep = "Language Models Need Sleep" (2606.03979) + episodic→semantic consolidation (2607.01988).
- **Warnings:** ER-JEPA (2609.36952, posted 2026-09-29) already does JEPA + episodic replay;
  EPM-JEPA (2606.12979) tested JEPA + accumulated experience with a **small/null effect** — take
  F5 seriously.
- **Names adopted loudly:** *escalation rate* (not pinch ratio), *cost–reliability frontier* (not
  teacher-tokens-per-competence), learning-to-defer (the pinch's formal home). "Neural case-based
  reasoning" is a free name (zero arXiv hits) but weak.
- **Where the contribution survives:** the *joint two-curve measurement* (escalation rate +
  cost–reliability frontier) against held-out generalization across P0→P1; consensus defined over
  *graded* outputs; retention privileging failure/boundary episodes; gated-consolidation discipline;
  provenance tapes (with the F4 caveat).

## Falsifiers (first three, sized cheap)
- **J1:** P0 saturation — pinch ratio reaches ≥95% within the small state space with consolidated
  field ≤2 MB, draw-rate vs solver monotonically improving. CPU, hours.
- **J2:** consolidation lift — agreement on held-out episodes strictly improves after each sleep
  phase, and post-consolidation *forgetting* (old episodes answered by head alone) stays <5%.
  CPU, hours.
- **J3:** boundary honesty — escalation (pinch escapes) correlates with true difficulty (solver
  disagreement/error rate) with AUC ≥0.75: the system escalates where it *should*. Reuses the
  ambiguity-map machinery.
- **J4 (GPU, later):** JEPA pretraining beats random-projection encoder on P1 plateau height
  (same field budget). Sharpened by scan F5: on small/near-stationary boards random projection may
  suffice (2606.27014's bound; EPM-JEPA's null effect) — JEPA is expected to earn its keep only
  from P1; pre-register that expectation.

**Scan-added attacks** (each cheap, from /home/eileen/scratch/jrag/):
- **F1 consensus ⟂ competence:** hubness, density bias, and graded-consensus definition sensitivity
  can make consensus systematically miscalibrated. Test: calibration curve of consensus vs actual
  correctness on held-out boards; tune the consensus definition on train, evaluate frozen.
- **F2 consolidation may not lift, and aggregate agreement hides boundary regressions** (cf.
  2605.12978 — utility can rise then fall *below* no-memory; 2209.05245 downscaling trade-off).
  Test: per-boundary-band accuracy tracked across sleep phases, never just aggregate.
- **F3 escalation rate is a coverage artifact:** the escalation→density feedback loop can produce
  the full P0 saturation curve with zero generalization. Test: held-out measure paired with every
  saturation claim (now built into P0's gates).
- **F4 provenance dies at the parametric boundary:** after consolidation, "which episode taught
  this?" needs a leave-one-out influence test to survive; if it fails, keep an addressable episodic
  layer beside the weights (2607.01988 keeps one for exactly this reason).
- **F5 encoder ablation:** random projection vs JEPA encoder, same field budget, P0 and P1 — if the
  gap is null at P0, that is a *finding*, not a failure (JEPA's value should appear at P1+).

## Repo shape (if Casey greenlights as its own repo)
`jrag/` — `field/` (index + tiers + receipts), `encoder/` (JEPA), `head/` (jev head, ternary-ready),
`pinch.py` (policy), `sleep.py` (consolidation = distillery bridge), `tape.py` (episode provenance),
`games/` (P0–P2 harnesses), receipts. Alternatively JRAG starts as a lane *inside* the distillery
repo and splits when the field code outgrows it.

## Open questions for Casey
1. Own repo (`jrag`) or lane inside quilt-distillery until P1?
2. Field storage for P0–P1: local (sqlite/HNSW in-process) vs i2i-ledger/Vectorize from the start?
