# Substrate Deep-Scout — SUBSTRATE lane, 2026-09-29

Scout: lucineer-scout-substrate. Sources: 14 repos cloned shallow to /tmp/scan-substrate/, + local canon bundle /home/eileen/projects/quilt-research-canons (read deeply: README, SPRINT-LINEAGE, novel-problems-report, moth-fidelity-matrix, jev-gate-experiments, active-ledger, HANDOFF, jev-velocity). Constraints honored: read-only + file writes + ledger bookings.

## What the current sprint protocol IS (quilt-research-canons)

**Sprint-lineage protocol**: each API agent's run leaves a Python run for the next sprint; every `sprint-XXX-NNN.py` embeds a `NEXT-SPRINT SPEC (XXX-(NNN+1))` header specific enough to implement without asking; the roadmap is the chain of files in the directory, not memory; each artifact is a runnable witness that declares its successor. Substrate-walker pattern surviving wipes by writing itself into the filesystem.

Newest state (pushed 2026-09-29/30): HANDOFF brief (don't re-derive measured results: quilt-c v0.1.0 signed+published crates.io/npm; open PRs quilt-c#5 A2A cell API, fleet-seeds#2 externalisability gate 0/10, AI-Writings#70 Bell-witness verifier); wave-66 PR-sweep integration (21 open PRs → 0 unhandled); JEV gate experiments REPLACED the p>0.7 composite gate.

## Per-repo digest (14 repos)

| repo | core idea (1 line) | status | contributes to active doctrine |
|---|---|---|---|
| **substrate-foundation** | Core runtime: 11 opcodes + FNV-1a canary `0x024a555471370b18d` ("café Δ 日本語") + `DRIFT_TOLERANCE_MEAN_P=0.7` (the JEV gate constant) | npm `@superinstance/substrate-foundation`, tests ship | Judgment gates CM1: the 0.7 threshold literal lives here; architecture diagram names it "JEV gate threshold" |
| **opcode-canon** | The 11-opcode canon: BIND/LINK/EFFECT/VIEW/TICK (cell-graph algebra) + ATTEST/DELEGATE/CONTEST/MERGER/REVOKE/WITHDRAW (observation algebra) | npm, .d.ts | Vocabulary for ActiveLedger operations (every ledger hop = opcode application) |
| **substrate-witness-log** | Immutable prev_hash-chained witness records; structural defense vs memory-poisoning (cites arXiv 2605.08442) | npm | ActiveLedger's append-only-by-construction guarantee — the exact clause that fires the canon gate (~0.93) |
| **cell-doctrine** | Three tenets: `cell_is_system` (cell is the system, not the data), `watch_oscillates` (universal↔particular), `address_is_data` (cell at hash H fully determined by H) | npm 0.1.0, `isCell`/`watchMode`/`toggleWatch` | cells-are-dedicated grounding: operations act on the cell; data is what the cell points at |
| **three-forms-of-evidence** | Evidence = DIRECT/WITNESS/PATTERN, weights 1.0/0.7/0.4, `classifyEvidence`+`trustScore` | npm, .d.ts | CM1 inputs; **CONFLICTS with substrate-foundation's witness/receipt/memory — canon drift, see finds** |
| **three-forms-of-forgetting** | Forgetting = bundle (keep summary), traversal (drop path), evidence (stop anchoring) — never deletion; scar remains, recoverable | npm | Witness-chain semantics: scars persist under JEPA prediction |
| **observation-primitive** | The atom: `{subject,predicate,object,issuer,time,evidence,signature}` + fnv1a64 + `int16Dials` (live-canon /api/cell submission) | npm, **no README** | Observation shape feeding witness logs + gate claims |
| **observation-primitive-rs** | Rust port of the atom; typed Opcode enum (11), Evidence {Direct,Witness,Pattern}, forgetting kinds; same canary assert | crates, src complete | Cross-language parity leg (TS/Rust/Python/C99 byte-exact) |
| **witness-is-prediction** | Rosetta theorem: the witness log IS a predictive model — each scar is the cell's hypothesis of future damage; JEV (writes log) ≡ JEPA (predicts masked context), one operator two directions; holds for ledgers/memory/social | npm | **Verbatim grounding of witness-as-prediction JEPA** |
| **substrate-quantum** | Classical sim ≤14 qubits: Bell/GHZ/W, QFT, Grover, Deutsch-Jozsa, entanglement entropy; own fleet-canary check | npm 0.1.0 dev | Substrate leg of the MOTH quantum-audio lane (fidelity matrix: QSM best continuous r≈1.0, QPAM all-rounder) |
| **substrate-merger** | MERGER opcode: combine two observations into one, idempotent | npm | Chorale chord-witness composition (N-way emission → composed witness) |
| **substrate-revoke** | REVOKE opcode: remove an observation's authority; permanent entry, hash-chained (revoke ≠ delete) | npm | Authority lifecycle on the ledger |
| **substrate-attest** | ATTEST opcode: add trust score to an observation, witness-typed | npm (README grammar bug: "is irrevocable") | Trust math feeding gate confidence |
| **substrate-membership** | Pure set-membership test: is a cell in a set | npm | Cell-set routing primitives |

All 14 share the same fleet boilerplate (canary, 4-language parity claim, stress-fuzz test ref). The distinct content is in index.js headers + foundation README.

## Doctrine-grade finds (booked to ledger)

1. **JEV canon gate characterized + replaced** (quilt-research-canons, jev-gate-experiments 2026-09-29, ~90 API calls): the gate is a structural-completeness STEP, not a quality scale — mechanism+explicit-guarantee fires ~0.93-0.97; everything past the guarantee (byte-prefix proof, fail-closed, second impl, even Lean 4 proof) is INERT to the instrument; bare "append-only" wording alone scores 0.98 (tautology tester). Replacement: two-axis gate `min(MECHANISM, EXTERNALITY) > 0.7`, shipped `jev_gate.py` self-test 7/7 with circularity pre-filter; ±0.10 phrasing swing → use for ranking/diagnosis, not binary. Slot-2-in-batch always highest, slot-4 lowest but identical across claims → only compare within one call. This is the CM1 judgment-gate doctrine, current as of today.

2. **Evidence-forms canon drift inside the fleet**: substrate-foundation exports FORMS = witness/receipt/memory; three-forms-of-evidence ships DIRECT/WITNESS/PATTERN with weights 1.0/0.7/0.4, and observation-primitive-rs repeats the latter — both claim "R10 canonical". The byte-exact FNV canary holds while the semantic taxonomy forked. ActiveLedger evidence-class routing + CM1 weights depend on which version wins; needs a canon decision.

3. **witness-is-prediction Rosetta theorem**: witness log = predictive model; scar = hypothesis of future damage; JEV and JEPA = same operator from two directions where time and space collapse. Verbatim, testable (`witnessAsPrediction` returns predictive_scar with trust-derived strength).

Also notable (not booked): ActiveLedger is grounded in the canons bundle itself (`research/active-ledger.md`, 2026-09-29, 12/12 selftest incl. 4 negative controls): double-entry tensor routing — every hop recorded on both sides in each book-keeper's units, translation table = routing code; planes need not be orthogonal (47 Hz hull vibration = FAULT/structural, nothing/acoustic, low-vib/comfort — all correct); the pre-STT filter is a real cell posting verdicts to the same ledger, and a blocked signal sends NOTHING across the gate (distinct from zero). JEV velocity: most claims stable at trial 1 → no need to average repeat calls.

## Ledger bookings

- book 1: JEV gate replacement → receipt quilt-research-canons
- book 2: evidence-forms drift → receipt three-forms-of-evidence
- book 3: Rosetta theorem → receipt witness-is-prediction
