# Scout digest — PuddnHead (SuperInstance) — 2026-09-29

Source: https://github.com/SuperInstance/PuddnHead (69 KB, narrative only, no code).
Local clone (read-only): /home/eileen/scratch/PuddnHead. Files: README + thought1..thought7.md.

## 1. The story (short)

Twain's *Pudd'nhead Wilson*. Wilson arrives in Dawson's Landing, makes one misunderstood
joke, is labelled a fool for twenty years, and quietly collects labelled fingerprints on
glass slides. Roxy (enslaved, 1/16 Black) switches her son (Valet de Chambre, later "Tom
Driscoll") with her master's son in the cradle so her boy grows up white and free. Twenty
years on, debt-ridden "Tom" murders his uncle Judge Driscoll and sells Roxy's freed family
back into slavery to fund it. At the trial the Italian twins are about to be lynched.
Wilson holds up two slides: they match. The reveal is not "who did it" but that *the whole
social order rests on a switched child* — the "heir" is the "servant." Wilson is
celebrated; the truth is instantly co-opted to reinforce race hierarchy rather than expose
it. **The Fool was the ground truth all along.**

## 2. Narrative → primitive mapping (verbatim receipts)

| Narrative beat | Quoted line | Our primitive |
|---|---|---|
| Slide = one unit of evidence | "Each slide is a **Quilt cell** containing an immutable, hashed fingerprint pattern." (t3) | tiles / cells (`tile_file`,`tile_get`) |
| Cell has content-derived name | "**Address**: A unique, content-derived identifier (like a hash of the fingerprint)." (t3) | content address / digest |
| Exact identity proof | "I have two fingerprints that match—this is the truth" (t1) | FNV-1a digest (cheap, exact) |
| Identity as embedding | "His fingerprints are **vector embeddings of identity**." (t3) | bge-m3 → Vectorize (`near`) |
| Ternary timbre = dial | "6 bits of spatial amplitude, 2 bits of timbre (**Ground, Attract, Repel, Abstain**)" (t5) | γ/η field, γ+η ≤ 1585, log₂3 |
| Ledger, append-only | "This layer must be **append-only**. No performance-plane component can mutate it; it can only append." (t6) | bookings + receipts (`book`) |
| Receipts are the honesty surface | "**No verification without receipt.**" / "hash-chained receipts (`fnv1a-64` chained, replayable, tamper-evident)" (t6, t5) | `witness_get`, FNV-1a chain, `verify.mjs` |
| Reflex / trigger | "`pincher` does not decide truth. It decides **when truth needs a courtroom**." (t6) | `pinch` → FIRE / CONFIRM / ESCALATE |
| Escalate + compile back | "unknown → escalate to caller ... compiled back as a new reflex" (api README) | `pinch` ESCALATE + compile-back |
| Courtroom reveal = projection | "His courtroom reveal is a **projection of the cell graph's truth into the system's decision space**." (t3) | qthe projection; **UNBUILT as a moment** |
| Witness / testimony | "He is the system's **orthogonal witness** — and the system will try to weaponize his truth." (t6) | `witness_get` (honesty surface) |
| Re-executable by a stranger | "no claim is verified unless its verification is **re-executable by an adversarial stranger**." (t7) | `verify.mjs`, `coev audit` |
| Fail-loud falsifier | "`coev audit` already says REFUTED. It already exits 1. ... **fail-closed**, seeded, deterministic, re-executable by a stranger." (t7) | coev audit / honest FAIL |
| Co-option ledger | "Every verdict cell should spawn a **consequence cell**." (t6) — "Effects are appended later, never at verdict time." (t7) | **GAP** (no effects ledger) |
| Dissent is a column | "**Dissent is a first-class field, not an exception.**" (t7) | **GAP** (no dissent field) |
| Slide fixed, reading versioned | "The slide is immutable; the reading is versioned." (t7) | **GAP** (versions the artifact, not the reading) |

## 3. Gaps (either direction)
1. **No reveal renderer.** Truth lives in receipts and `tile_history` versions, but nothing
   renders *the moment* — claim → method → matched cells → verdict → dissent — into a
   decision space. `witness_get` is a lookup, not a projection. That is the story's
   punchline ("The evidence was always there. I just needed to hold up the slides.")
   and our biggest narrative→mechanism hole.
2. **No effects/co-option ledger.** We append receipts, not *what happened after the
   verdict* against its stated intent — the whole point per t6: "Wilson's tragedy is not
   that he fails to verify; it is that his verified truth is co-opted."
3. **No dissent column, no named-rule version on the reading.** CONFIRMED/FAIL only; no
   minority report, no `constitution:{id,version,rule}` citation.
4. **Identity is scored, not proved.** `pinch` returns a similarity (CONFIRM 0.892), so a
   lookalike can CONFIRM. The story's law is objective identity.

## 4. Top-3 ideas (smallest testable version each)

**(a) Reveal mode — `reveal_get(verdict_id)`.** Walk the citation chain, emit a transcript
of the moment: claim, method, matched cells with digests, verdict, dissent. Smallest test:
one verdict row → one rendered 10-line transcript from `witness_get` + `tile_history` +
the dependency column. No new storage.

**(b) Fingerprints: digest *proves*, embedding *proposes*.** Keep bge-m3/Vectorize for
candidate search; make the verdict a digest-equality test, not a cosine threshold.
Similar-but-not-identical → `ESCALATE`, never `CONFIRM`. Smallest test: replay the existing
paraphrase pinch with a hash gate; a lookalike (different digest) should flip CONFIRM →
ESCALATE while the true repeat still FIRES.

**(c) Split the ledger in two.** Add `effects` (append-only, later, mechanizable) and
`dissent` (first-class column). Smallest test: book one verdict, append one effect after,
record one dissent; assert the verdict row is immutably unchanged.

## 5. Strongest recommendation

**Ship (b) + (a) as one move: make the reflex path prove identity, then show the proof.**
The digest gate is the doctrine (a scored match is not ground truth — it is the exact bug
the story opens with), and the reveal renderer is the product ("hold up the slides").
Both are additive to `pinch`/`witness_get`, need no new store, and are falsifiable this
week. Order: gate first (correctness), reveal second (legibility). Park (c) — t7 already
says the normative half belongs to a constitution, not the mechanism, and we have no
constitution version to cite yet.

*Naming, from t7: the quilt is the body, the constitution is the law, Pudd'nhead is the
**office** — held by many, re-executable, "you cannot become sovereign by occupying a
re-executable procedure." Good name for a role, not a repo.*
