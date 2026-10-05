# SWARM-DECOMPOSITION.md — Build-Level Decomposition of the Swarm Vision

**Date:** 2026-10-04 (post 16:52 vision, Casey)
**Status:** research/design document only — NO code, NO claims of runs. This is
the bridge between Casey's swarm vision and the ZeroClaw build system.
**Companion docs:** `2026-10-04-swarm-architecture.md` (vision-level lanes
S1–S5), `~/projects/zeroclaw/CHARTER.md` (builder contract),
`~/projects/zeroclaw/SEED-SURVEY.md` (verified artifact state).

## 0. Scope and relationship to the architecture doc

The architecture doc decomposes the vision into five lanes (S1 JEV projection,
S2 mutation, S3 stochastic selection, S4 compression, S5 quilted relationships)
at the *vision* level. This doc decomposes the **three lanes Casey named as the
core loop** (JEV selection, mid-process mutation, compression) down to
*mechanism* level — concrete data structures, minimal implementations, success
criteria, failure modes — each grounded in artifacts that RUN today (per
SEED-SURVEY receipts):

- **exoj `core.mjs`** — hex-lattice `Cell` with γ/η amplitudes, conservation
  γ̄+η̄ ≤ 1, `canonicalJSON`, `sha256Hex`, append-only ledger policy.
- **exoj `gan/unitTable.mjs`** — `UnitTable`: deterministic masses via `fnv1a`,
  **no RNG anywhere**. The ancestor of every stochastic-looking mechanism here.
- **zeroclaw `cell-internals`** (Lane 1, poc green) — cell = question + finite
  answer set + decayed pseudo-counts + `n` + sha256-chained tick head;
  distribution = Dirichlet posterior mean; counts+n is the **sufficient
  statistic**.
- **zeroclaw `gate-mechanisms`** (Lane 2, poc green) — gate = directed edge,
  threshold θ, refractory R, adaptation λ (habituation on fire, relaxation
  between), synchronous snapshot semantics, **append-only emission** (damping =
  writing −1 ticks, never editing history).
- **quilt-pincher seam** — `loadZeroclawSpecs` / `parseZeroclawSpec`, grammar
  `zeroclaw-reflex-spec/v1` (`id, intent, trigger, context_sha256, model,
  payload{...}, cites[], provenance{compiledBy:'zeroclaw', parentOrder}`);
  payload stays DATA. Plus `HDCEmbedder` / `Hyper` vectors and
  `ExoJFieldState` — pincher already projects exoj field state into
  hypervectors.
- **MicroMoth** — existing simulation frames (`~/projects/micromoth-quilt`,
  `~/projects/pr-wave-micromoth`).
- **Moth quantum** — the designated stochastic/dice element, *external* to all
  ledgers.

**Division of labor with the architecture doc:** S3 (dice-roll replay) is
absorbed here as the *external roll contract* inside Lane D1 and the sim
namespace in Lane D4. S5 (quilted relationships) is deliberately deferred — it
needs Lane D3's linkable docs to exist before agents can push/pull anything.
Nothing below re-derives S1–S5; it builds under them.

## 0.1 The core loop this doc serves

One turn of the swarm, stated in Casey's terms, mapped to ZeroClaw terms:

```
agent runs its routine
  ├─ mid-process: agent emits ≥1 child design (Lane D2 — mutation)
  │    └─ child goes to MicroMoth sim before real odds (Lane D4)
  ├─ JEV projects: cells' beliefs → firing distribution over candidates
  │    (Lane D1 — projection is pure, deterministic given ledger head)
  ├─ moth quantum rolls the dice against that distribution (external roll)
  ├─ winner fires; its outcome writes ticks back to the cells (D1 feedback)
  └─ non-selected agents compress into linkable docs (Lane D3)
```

JEV is a **projector, not a judge**. That distinction is load-bearing: JEV owns
no beliefs of its own. The distribution is a pure function of the collective's
tick ledgers. Everything opinionated lives in cells and gates, where it is
auditable and append-only.

---

## LANE D1 — JEV Selection: probability projection as composition of cell beliefs

### Question

By what mechanism does JEV turn N agents' worth of cell state into one
normalized distribution over "who fires next" — such that the percentages are
*literal firing odds*, the projection is deterministic given the ledger, and
every live candidate retains nonzero odds (so the dice can always surprise)?

### Proposed approach

**The turn-cell substrate.** Give the swarm one question per candidate:
*"when the swarm needs a next step, is agent A the one that should answer?"*
Answers are the finite set `{A, other}` (or a single shared cell whose answer
set IS the agent roster — see open question below). Each firing outcome is a
tick: the fired agent that succeeded earns `+1` on its own turn-cell; failure
earns `−1`. Outcomes are observed by gates (Lane 2 mechanisms), not invented by
JEV.

**The projection (pure function).** JEV computes, for each candidate A:

```
score(A)  = posterior mean of A's turn-cell      # from counts+n (Lane 1)
weight(A) = max(score(A), floor)                 # exploration floor
P(A)      = weight(A) / Σ_B weight(B)
```

The floor is not an add-on — it falls out of Lane 1's own Laplace/Dirichlet
smoothing. The prior mass `alpha` per answer already guarantees an agent with
zero history keeps nonzero odds. **The cell's smoothing IS the exploration
mechanism.** This is the cleanest graft point in the whole design: no new
mechanism needed, just stop zeroing out the prior.

**The roll (external, moth quantum).** JEV outputs the distribution and stops.
The dice roll is a separate step: given distribution P and a roll value derived
from moth quantum (recorded, not generated, by the ledger — the architecture
doc's S3 replay contract: the ledger records the roll *value* and the outcome,
never manufactures entropy), select one candidate. Same ledger head + same
recorded roll → same selection, replayable.

**Determinism law.** Same ledger head → same distribution, bit-for-bit. This is
the exoj `UnitTable` law transplanted: fnv1a-derived masses, no RNG in the
projection. All entropy enters as ticks from the world (outcomes) or as one
recorded roll per turn (moth quantum). JEV never calls random.

**Decay keeps the distribution alive.** Lane 1's `lam` decay on counts means an
agent that used to fire and stopped succeeding bleeds odds back toward the
floor — the distribution tracks a shifting world instead of fossilizing.

**Minimal implementation.** `jev-projection/poc.py` (stdlib only): M agents,
each with a turn-cell; a deterministic world where the "best" agent for the
task drifts over phases (world ticks via `fnv1a`, no `random` import); JEV
projects each turn; moth-quantum stand-in = `fnv1a("roll:"+t)` bucketed into
the distribution. Baseline comparison: greedy argmax (no dice) vs. dice-roll.
Measure: task success rate, time-to-adapt after phase shift, minimum share any
agent retains.

### Success criterion

1. Σ P(A) = 1.0 exactly (rational arithmetic or normalized counts — not float
   apology), stable across repeated projection from the same head.
2. Zero-history agent retains odds ≥ the prior floor (dice can always land on
   the new mutant — this is what makes D2's mutations meaningful).
3. After a phase shift, the distribution re-concentrates on the new best
   agent within K ticks (pick K honestly in the poc; record it).
4. Dice-roll selection beats greedy argmax on at least one multimodal world —
   i.e., stochasticity earns its keep, demonstrated not asserted.
5. Receipt: projection inputs, distribution, roll, outcome — all content-
   addressed and chained (exoj `'ledger'` policy).

### Risks / failure modes

- **Rich-get-richer collapse.** Success → ticks → higher odds → more firings →
  more ticks. If decay λ is too weak, one agent hits ~100% and the "literal
  odds" vision degenerates into argmax with extra steps. Mitigation to test:
  habituation (Lane 2's θ-tightening applied to turn-cells — firing a lot makes
  the next firing *harder to earn*), stronger decay, or a hard odds ceiling.
  **This is the expected failure.** The poc should provoke it on purpose and
  measure the λ that avoids it.
- **JEV becomes a judge.** Anywhere JEV "weighs in" (e.g., hand-tuned bonuses)
  it stops being a projector and becomes unauditable opinion. Rule: JEV's code
  contains exactly one arithmetic pattern (normalize-with-floor) and nothing
  else. If a change adds judgment, it goes in a cell where it earns ticks.
- **Shared-cell vs per-agent-cell ambiguity.** One cell with answers = agent
   roster (multinomial) vs. N binary cells (one per agent) are *different
   compositions* — they disagree on how competing evidence lands. The poc must
   pick one and defend it; this is the lane's real research content.
- **Double-counting with gates.** If outcome gates and turn-cells both write
  ticks for the same event, beliefs inflate. One event → one tick, exactly one
  ledger row, enforced by construction.

---

## LANE D2 — Agent Mutation: "a new unique agent" as a data structure

### Question

When an agent mid-process "tries to think of at least one new unique agent that
might be better for the next step" — what IS that artifact, as data? What
minimal delta distinguishes a genuine mutation from a re-description of self?
And how is it born with odds (it must, or D1's dice can never pick it)?

### Proposed approach

**An agent, in ZeroClaw terms, is already three things:** a spec
(`zeroclaw-reflex-spec/v1` — the pincher seam parses it TODAY), the cells it
owns (Lane 1 objects), and the gates it installs (Lane 2 objects). So a
**child design** is exactly:

```
AgentDesign {
  spec   : zeroclaw-reflex-spec/v1     # id, intent, trigger, payload (DATA),
                                       # cites[], provenance.parentOrder
  cells  : [Cell seeds]                # question + answer set (+ prior counts
                                       #  inherited or fresh — open question)
  gates  : [Gate configs]              # edges, θ, R, λ
}
```

**Mutation = a typed delta, not free text.** The child must differ from the
parent in at least one *named* dimension — the mutation grammar, deliberately
small to start:

1. **cell-mut:** different `question` or different `answers` set (a new
   question the parent never asked);
2. **gate-mut:** different θ / R / λ or a new edge (a different reflex);
3. **trigger-mut:** different trigger in the spec (fires on different
   occasions);
4. **context-mut:** different `context_sha256` (stands on different cited
   documentation — this is where D3 feeds back in).

**Uniqueness predicate (measurable, not vibes).** Child is unique iff
`canonicalJSON(child) != canonicalJSON(parent)` AND the delta is in the grammar
above (whitespace/ordering changes don't count — canonical JSON already kills
those) AND `output_sha256` of the child differs. Copies are rejected by
construction.

**Inheritance via the existing grammar.** `cites[]` carries the parent's spec
hash; `provenance.parentOrder` records birth order. The lineage is the exoj
sha256-chain pattern applied to *agents* instead of ticks. This is critical for
D3: a compressed parent is a *link* the child already carries.

**Birth odds for free.** The child enters the D1 candidate pool with an empty
turn-cell — the Laplace floor gives it nonzero firing odds automatically. But
its *pre-seeding* comes from MicroMoth (Lane D4): sim ticks in a separate
namespace give it honest provisional odds before it ever touches the real
ledger.

**The claim requirement (anti-novelty-theater).** Every child must carry a
falsifiable claim: *which situation* it handles better, expressed as its
mutated cell's question. "I am agent v2" is not a mutation; "I fire when the
task mentions X, which parent's question never covered" is.

**Minimal implementation.** `agent-mutation/poc.py`: take a parent design +
its tick history, emit one child per mutation type, verify (a) uniqueness
predicate passes for each, (b) `parseZeroclawSpec` (or its python
re-implementation pinned to the same grammar) accepts each child spec, (c) a
deliberate copy fails the predicate. No LLM in the poc — mutation *grammar*
first; generative mutation (an LLM proposing the delta) is a later layer that
must still emit grammar-conformant children.

### Success criterion

1. All four mutation types produce valid, parseable specs; copies and
   whitespace-variants are rejected. Receipt per child: parent hash, child
   hash, delta type.
2. At least one deterministic simulated world exists where a specific child
   measurably outperforms its parent on the child's claimed situation
   (mutation is *meaningful*, not just different).
3. Child enters the D1 pool with odds exactly at the floor — no free boost,
   no zero (the D1/D2 contract).
4. Lineage is walkable: child → cites → parent → cites → grandparent, hashes
   verifying at each hop (exoj chain law).

### Risks / failure modes

- **Population bloat.** Every routine spawns ≥1 child → combinatorial swarm
  growth. The counterweight IS Casey's compression law (D3): children that
  never win a roll get compressed and archived — death by irrelevance, not
  deletion. Also test a spawn-budget (e.g., mutation only when the agent's own
  outcome ticks trend negative — mutate on struggle, not on success).
- **Drift / losing the parent's competence.** A child with a fresh cell set
  forgets everything the parent learned. Mitigation to test: inherit parent
  counts for unmutated cells (cheap — counts+n is copyable state).
- **Novelty theater.** Mutants that are different but never better, forever.
  The claim requirement + sim gate (D4) is the defense; if it fails, the swarm
  becomes a mutation fountain with no selection pressure — detect by measuring
  mean lineage depth of actual *winners* over time.
- **Grammar ossification.** If the 4-delta grammar can't express useful
  mutations, agents will strain to emit legal children that mean nothing. The
  grammar must grow *from* observed sim results (D4), not from imagination.

---

## LANE D3 — Compression: full experience → linkable documentation

### Question

When an agent doesn't fire, it "gets reduced in size, summarized into
documentation others link to." What exactly is preserved, what is archived, and
what is *lost*? How does the summary stay useful to OTHER agents (not just a
diagnostic for us), and how does a compressed agent come back?

### Proposed approach

**Start from the gift Lane 1 already gave us: counts+n is a sufficient
statistic.** The posterior distribution is *fully determined* by counts and n —
the entire tick ledger is proof, not state. So the agent's belief-state is
already compressed by construction. Compression is therefore three layers:

```
HOT  (live agent)   : full tick ledger + cells + gates + spec — firing odds
COLD (summary doc)  : counts+n per cell, gate θ/R/λ final values, spec hash,
                      top-K surprising ticks, outcome stats, the agent's claim
ARCHIVE (vault)     : the full ledger chain, content-addressed, never deleted
                      (archive-by-rename law; the "gold" for later study)
```

**The summary doc** (this is the "documentation others link to"):

```
AgentSummary {
  id            : sha256(canonical(summary))     # the linkable ID
  spec_hash     : cites parent lineage head
  cells         : [{question, answers, counts, n}]   # posterior restorable
  gates         : [{edge, theta_final, R, lam}]
  surprises     : top-K ticks ranked by posterior shift they caused
  outcomes      : fired N times, succeeded M, best/worst situations
  claim         : the situation it believed it was for (from D2)
}
```

**The linking mechanism already exists in the grammar.** `zeroclaw-reflex-spec/v1`
has `context_sha256` and `cites[]`. A new agent's spec can cite a compressed
agent's summary ID as context — the compressed agent's experience becomes
*input* to a successor's trigger. Compression isn't disposal; it's publication.

**What "surprises" means (the essential-experience heuristic).** Rank each
tick in the ledger by how much it moved the posterior (KL or simple |Δp|).
Top-K retained verbatim in the summary; the rest aggregate into counts. This
is the honest, computable version of "essential insights" — the ticks that
*changed the agent's mind* are the ones worth reading, and they're exactly the
boundary cases a successor needs to see.

**Revival (cold → hot).** Restoring the agent = rebuilding cells from counts+n
(exact — same posterior, no ledger replay needed for *behavior*), reloading
gate configs, and pointing at the archived chain for *proof* when audit is
required. The ledger is re-verified, not re-lived. (Watch the trap: gate
*refractory/adaptation transients* are not in counts — a revived agent's
first moments may differ from the original's last moments. Decide explicitly
whether θ revives at `theta_final` or `theta_base`.)

**Minimal implementation.** `compression/poc.py`: build an agent with a long
synthetic ledger (fnv1a world), compress, then verify the three contracts:
(1) **revival fidelity** — posterior from summary == posterior from ledger
(exact for counts+n by sufficiency — if it's not exact, the poc has a bug);
(2) **linkability** — summary ID is deterministic, and a mock successor spec
carries it in `context_sha256`/`cites`; (3) **compression ratio** — report
bytes(ledger) : bytes(summary) honestly, surprises included.

### Success criterion

1. Revival reproduces every cell posterior *exactly* (sufficiency proof in
   action — this is the lane's crown jewel and its test).
2. Summary ID is deterministic from content (same agent → same ID, forever —
   sha256 canonical, exoj law).
3. A successor agent can and *does* cite the summary (mock in poc; real cite
   once D2's context-mut exists).
4. Ratio reported, not promised — with surprises included in the denominator.
5. Archive intact: full chain still under the vault path, renamed not deleted.

### Risks / failure modes

- **The surprise tail is wrong.** Top-K by posterior shift may drop rare-but-
  critical evidence (the once-in-a-thousand tick that would have saved a
  successor). No clean fix — mitigation is keeping K honest and measuring
  revival decision-quality, not just belief fidelity.
- **Write-only docs.** Summaries nobody links to are entropy, not memory
  (ANTI-ENTROPY-LOG law). Defense: D2's context-mut gives agents a *reason*
  to cite (inheriting context through cites is cheaper than re-learning), and
  link-count per summary is measurable — a summary with zero citations after
  N swarm turns is a smell, and can itself be compressed further.
- **Over-compression at the wrong moment.** Compressing an agent the phase
  shift was about to make relevant. Mitigation: D1's decay means relevance
  fades slowly — compress only agents below an odds threshold for a sustained
  window, and revival must be cheap (it is: counts+n).
- **Fidelity theater.** Passing posterior-equality while losing the *claim*
  and surprises (the parts that make the doc useful to others). Both
  contracts must be tested, not just the math.

---

## LANE D4 (supporting) — MicroMoth: simulation before execution

### Question

Casey: cells "play with new agent designs before execution." What is the
sandbox contract — how do sim ticks give a mutant honest provisional odds
without contaminating the real ledger?

### Proposed approach

Two ledgers, one grammar: sim ticks live in a **separate namespace**
(`sim:` prefix on the chain, or a distinct head per agent) and use the exact
Lane 1 structures. A mutant fresh from D2 runs in MicroMoth (existing frames:
`micromoth-quilt`, `pr-wave-micromoth`) against a fnv1a-deterministic replay
of the world; its sim turn-cell posterior seeds a **provisional weight** that
blends with the Laplace floor — e.g., weight = max(score_sim, floor), capped,
so sim can *lower* birth-to-realtime cost but can never vault a mutant to
dominance on simulation alone. Sim never writes to real ledgers; the moth-
quantum dice pool only ever reads real + provisional-marked weights, and the
mark is visible in every receipt.

### Success criterion

1. A mutant that fails in sim enters the real pool at-or-below floor (or is
   rejected — pick one rule and defend it).
2. Sim runs are bit-reproducible (fnv1a world, no RNG import).
3. Zero sim ticks appear in any real ledger head (verifiable by namespace
   audit).

### Risks / failure modes

- **Sim-real gap / overfitting the simulator.** Mutants evolve to beat
  MicroMoth, not the world ("simulation collapse"). Defense: sim world must
  be *sampled from real recorded history* (replayed real ticks), not synthetic
 -only; and D1's real ticks eventually dominate any provisional weight by
  decay.
- **Namespace leakage.** One careless tick write corrupts real beliefs — the
  worst failure class here (silent). The audit in success criterion 3 is not
  optional.

---

## Build order (what the builder should tackle first)

Grounded in CHARTER.md's "one increment per run, thinnest slice first" law:

1. **Lane D1's floor first — it's nearly free.** Lane 1 cells already emit
   Laplace-smoothed posteriors; a turn-cell + normalize-with-floor projection
   is a small poc on top of existing, green code. And *everything else in the
   swarm depends on the dice pool existing*: D2 children need birth odds, D3
   needs the odds threshold that triggers compression, D4 needs a pool to
   seed. **D1 is the keystone increment.**
2. **Then D3's sufficiency receipt (revival fidelity).** Also nearly free —
   it's a property Lane 1 already guarantees, and receipting it early makes
   every later compression decision safe by construction.
3. **Then D2's mutation grammar** (4 typed deltas, uniqueness predicate) — it
   consumes D1's pool and D3's citations, so building it after both avoids
   stubs.
4. **Then D4 MicroMoth namespacing**, last, because it needs real recorded
   history to replay (which only exists after the loop has run for a while).
5. S5 (quilted relationships) re-opens once D3 summaries exist to be pushed
   and pulled.

## Verification law (unchanged, inherited)

Every future poc in these lanes: runs on this box (python3 stdlib), no RNG
imports (fnv1a world), deterministic receipts, append-only ledgers, archive-
by-rename, NO VERIFIED SHA NO BELIEF.
