# Deep-Scout: Lane VIBE — audio/music/language-spectral (2026-09-29)

Casey directive: dive into early/archived SuperInstance experiment repos for ideas worth reviving. 13/13 cloned OK to /tmp/scan-vibe. Read-only; no commits/pushes/GPU.

## Per-repo digest

### 1. quantum-audio-honesty ⭐ TOP FIND
- **Core idea:** Sonify agent state → lossy channel → decode → advice whose confidence = channel self-consistency (drift vs clean image).
- **Status:** Extracted 2026-09-28 from pong-quilt `qa.js`; works, tested. Not archived-broken — archived-*clean*.
- **Key machinery:** (a) deterministic labeled stand-in oracle, confidence hard-capped `SIM_MAX_CONF=0.5`, every surface says `source:"qa-sim"`; (b) empty-pot seam: below shot budget → returns silence/null, *refusal not a guess* (`??` not `||` semantics documented); (c) BYO endpoint seam: real oracle confidence NOT sim-capped; any failure → receipt `byo-qpam-fallback`, degrade to labeled sim at same seed/pot.
- **Revive in:** **cell-mesh judgment gates** — adopt wholesale as gate-judge honesty spec: every stub judge labeled + confidence-capped, empty budget = refusal, BYO real judge with fallback receipts, confidence = self-consistency not vibes.

### 2. musician-soul ⭐
- **Core idea:** Persona vector-DBs digest MIDI phrases into 32-dim fingerprints; jams scored on harmony+surprise; working answers reinforced, mutated copies spawn; "soul" = % self-made patterns.
- **Status:** Pure Rust, zero deps, forbid(unsafe), examples + tests work. `src/meta.rs` is the hidden gem: phrase = **trajectory** not point — Catmull-Rom spline through embedding space; arc length, bending energy, twist energy (3rd-order torsion = "the property is in the twist"), planarity; `gesture_distance` is scale/offset-invariant → comparable *across fleet nodes*; soul as trajectory-of-becoming with `vibe_velocity`.
- **Revive in:** cell-mesh — (a) harmony/surprise reinforcement as gate scoring; (b) spline gesture geometry as behavioral fingerprint for cross-node agent drift detection (scale-invariant by design).

### 3. songforge ⭐
- **Core idea:** AI covers of rough recordings (Demucs → Whisper-verify-vs-lyrics → enhance → MMX generate → remix) + relay-round transmission-chain lab.
- **Status:** Full CLI works; experiments/ is the valuable part: `build_relay.py` staircase-vs-relay crossfade builds with **conservation-of-signal tests in dB**; `depth3_relay.py` asks "does the transmission tax asymptote?" (L1 0.735, L2 0.948 at X=1.0 — decay fraction shrinks per layer).
- **Revive in:** **i2i-ledger** — adopt the relay protocol as handoff QA: measure dB decay across agent→agent→agent chains, crossfade conservation checks, depth-N asymptote curves per handoff pair.

### 4. linguistic-spectral
- **Core idea:** Text → bigram/word transition graph → Laplacian spectral fingerprint (conservation ratio, spectral gap, effective dimension) → genre/author/anomaly/language classification at numpy cost.
- **Status:** Single 42KB script, works (genres, 3 authors, code-injection anomaly, 5 languages); depends on sibling `code-conservation` pkg w/ local stubs fallback.
- **Revive in:** judgment gates — near-free deterministic first-pass fingerprint to pre-screen text artifacts (anomaly detection flags gibberish/injection) before spending LLM judge calls; also a cheap receipt fingerprint for ledger entries.

### 5. polyvocoder
- **Core idea:** 350-line universal head: any canon lore → 6-dim JEV features → tiny VAE → shared latent z → decode to prose + 16×16 ASCII image + 4s waveform simultaneously; tri-modal canon anchoring (if all three "feel" canon, it's canon).
- **Status:** Runs; `canon_tagger.py` tags lore w/ doctrine anchors (cells_are_scars, canon_gate_is_chord, etc.); v1+v2 pipelines.
- **Revive in:** quilt canon work — tri-modal canon anchoring as a gate test: same latent rendered to text/image/audio, scored in each modality; canon_tagger doctrine vocabulary reusable for quilt seed tagging.

### 6. polyvocoder-rust
- **Core idea:** Schema-parity Rust port of polyvocoder; pins fleet canary `fnv1a-64('café Δ 日本語') = 0x024a555471370b18d`; JSON dual snake/camelCase wire compat.
- **Status:** Builds, canary binary + test verify.
- **Revive in:** plato-cf rebuild / any TS+Rust split — the canary-pin + schema-parity + dual-alias-JSON pattern as standard port harness. (Fold into #5's revival.)

### 7. tensor-midi
- **Core idea:** Conversation rendered as live 12/8 jazz: messages → SWMIDI-8 events on a 12-pulse engine; **3:4 polyrhythm as architecture** — DMN(3-pulse) × ECN(4-pulse) resolve at beat 12 via CRT.
- **Status:** Built in one 4-agent ensemble session (Aug 8 2026); engine.js/analyzer/audio/persistence all present.
- **Revive in:** cell-mesh — coprime-period agent scheduling rendezvousing at LCM beats (deterministic "flow state" sync points); SWMIDI-8 (8-byte events, 96 PPQ) as a compact event wire format for mesh telemetry.

### 8. cra-analysis
- **Core idea:** Multi-LLM (GLM-5.3 + DeepSeek) CRA-of-Quilt audit dossier.
- **Status:** No README; the .md files ARE the artifact. Findings dated 2026-08-24.
- **Actionable gems for plato-cf rebuild:** (1) conservation law unenforced — single `fascia_ledger: i64` instead of separate gamma/eta registers; fix = split + enforce γ+η=0 in every op + random-perturbation invariant test. (2) Quilt levels 3–4 (topos, 2-cat) aspirational — code is level 1. (3) Missing fable tests (30, 33, 40). (4) Meta: DeepSeek hallucinated plausible file paths when asked to cite — always verify citations.

### 9. music-vibe-experiments
- **Core idea:** 16-dim vibe embedding (dark/bright, dense/sparse, tight/loose…) deterministically maps to MIDI parameters; sweeps, style prototypes (BoC, Daft Punk, Miles), blending, groove-locking.
- **Status:** Pure Rust, 24 tests, zero deps; works.
- **Revive in:** quilt canon / cell generators — the vibe vector as a compact continuous control knob any cell can consume or blend; vibe-space interpolation as generative navigation.

### 10. plainsong
- **Core idea:** Text-native music notation — 4 aligned rows (Chords/Melody/Lyrics/part), self-dividing bars, diffable — compiles to MIDI/audio; PyPI-published, single-file web demo.
- **Status:** **Alive, not archived** (last commit 2026-08-25). Strong agent ergonomics (AGENTS.md of documented agent mistakes).
- **Revive in:** quilt canon audio layer — canon songs as plain-text artifacts LLMs can read/write/diff natively; "bars divide themselves" = no duration math for generators.

### 11. chiaroscuro
- **Core idea:** Real-time webcam→ASCII, five engines, five hosted doors, Director = per-cell aesthetic decision engine, 45 dials, 31 typefaces.
- **Status:** Live at fleet-static-host (mirror/sculptor/studio/director/viewfinder). Not archived — a working tile.
- **Revive in:** quilt canon visual work; Director's auto-dial-setting from intent is the reusable pattern (aesthetic as inference).

### 12. tessera
- **Core idea:** "Video studio where footage is text": clips are chiaroscuro renders arranged as a drag-able mosaic (quilt), spliced via overlap/gap timeline — picture emerges from tiles, never one reel.
- **Status:** Design-stage with docs + fold-in of chiaroscuro evidence; no renderer of its own (by design).
- **Revive in:** quilt canon — mosaic-over-timeline composition pattern; also the "fold sibling repo evidence wholesale" method.

### 13. quilt-quantumaudio-demo
- **Core idea:** MOTH quantumaudio QPAM encoding (9 qubits, depth-2 per 10ms) as a pluggable cell "substrate"; 0.98+ reconstruction Pearson on AerSimulator.
- **Status:** Tiny demo, works; `falsify_shots2000.py` included (falsification-first culture).
- **Revive in:** cell-mesh substrate zoo — quantum-audio substrate as one more swappable backend; include `source`-labeled sim/real distinction (pairs with #1).

## Top 3 revivable (ranked)
1. **Honesty-channel semantics** (quantum-audio-honesty) → cell-mesh judgment gates: labeled+confidence-capped stub judges, empty-pot refusal, BYO seam w/ fallback receipts, confidence = self-consistency.
2. **Transmission-tax relay protocol** (songforge) → i2i-ledger: dB-decay measurement + conservation tests + depth-N asymptote curves for agent→agent handoff chains.
3. **Gesture-spline fingerprints + harmony/surprise reinforcement** (musician-soul meta.rs) → cell-mesh: scale-invariant cross-node behavioral drift detection; reinforcement-scored gate answers.

Runners-up: cra-analysis γ/η split fix (concrete plato-cf worklist item), linguistic-spectral near-free text fingerprints (gate pre-screen), polyvocoder tri-modal canon anchoring (quilt canon gates).

— lucineer scout, 2026-09-29 15:2x AKDT
