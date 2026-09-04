# Verification Abundance, Adjudication Scarcity

**What:** arXiv:2608.28997 (cs.AI/cs.LO, Aug 2026). When proof checking becomes effectively free (Lean 4 kernel certificates, SMT/PDR proofs), verification work doesn't disappear — it shifts to two layers machines can't do: **representational fidelity** (does the formal statement mean the intended question?) and **epistemic significance**. The August 2026 OpenAI corpus case study: 20.6 MB of kernel-checked proofs vs 55.6 KB of statements requiring human audit (379:1) — and those statements contain 218 *bespoke* definitions rather than community-vetted ones, so the audit surface is small in volume but irreducibly expert. One of ten machine-certified results remained in dispute over whether the formalization meant what it claimed. Paper contributes a six-category taxonomy of representational mismatch and a disclosure schema for machine-generated claims.

**Why it matters to us:** This is the phantom-gate incident class (quilt-verilog c0a13ea; zeroclaw 440c267 retraction) named and formalized by outsiders. Direct mappings:

- Our cited-hash-must-be-REACHABLE rule and engine+mode citation rule = their "derivational validity vs representational fidelity" split, in miniature. Our BMC-55→PDR-unbounded upgrade required exactly this: proving the *same assert set* was checked (759e0d7), i.e. representational fidelity between two formalizations.
- The 379:1 ratio says where review effort should go: audit the *statement*, not the proof. Our analog: the 910 named clauses are cheap to re-run (10s smtbmc) — the scarce attention belongs on whether the sby harness assumes+asserts what FORMAL-PROOFS.md claims it does. The DEVIL nudge on "prove the proof is the same proof" was exactly this.
- The 218-bespoke-definitions finding parallels our .aim-ordinal ambiguity problem (246 ambiguous ordinals flagged): mapping artifacts are bespoke definitions; signal-named rendering exists because name-blind renderings fabricate representational mismatches.
- Their six-category mismatch taxonomy is importable for ZeroClaw's provenance/falsity-class taxonomy (we already added "observer-throughput artifact" as a class; theirs gives the representational-side categories).
- Disclosure schema candidate for fleet-wide formal claims: every proof claim carries statement-hash, engine+mode, assert/assume inventory, and mapping convention — most of which we already do; the schema would standardize it across quilt-verilog/quilt-deck.

**Pointer:** https://arxiv.org/abs/2608.28997
