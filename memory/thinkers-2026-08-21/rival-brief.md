# RIVAL — Audit Position Brief (SuperInstance merge wave)

Skeptic's cost/benefit of every open decision. Read-only. Doctrine under audit: "newer wins, nothing deleted, ideas retire to archives."

## 1. UNSTABLE pile (103 red-CI) — real defects vs. doctrine theater

The `pr-states.jsonl` payloads let me separate signal from noise. Three genuine defect classes worth fixing, one theater class.

**Real defects (fix, small cost):**
- **gap-hunt round 2** — `Edge-Native#5` (COBS off-by-one), `spectral-music-v2#2` (Pitch::name wrong octave), `flux-cross-assembler#3` (LDI/MOVI emits 4 bytes, desyncs labels), `vessel-bridge#3` (truncated ESP32 frame), `openconstruct-esp32#3` (named GPIO drives pins LOW), `kintsugi-math-c#2` (heap-buffer-overflow in find_golden_joints), `holodeck-c#4` (cmd_gossip signature mismatch), `persona-engine#3` (XML escaping in SSML). All 1-line-to-small, all cite a concrete bug, all worth fixing now.
- **ternary-* "Production hardening" family** (22 PRs, `ternary-critical/depth/dice/scoring/memory/loss/...`) — real numerics bugs (Binder cumulant, magnetization overflow, Huffman avg-bits, WSPT ordering, index-OOB panics, capacity-0) caught via sabotage, each paired with "fake-green test" removal. These are the honest core: mostly 1-line fixes, some small. **Fix all.** Cost: a few mechanical-agent hours, near-zero regression risk because they're test-harness changes.

**Doctrine theater (cheap but hollow — do last, or skip):**
- The `fix(ci): remove failure masking` wave (~40 repos, `ci.yml`/`ci-python.yml`). Unmasking `|| true` is mechanically trivial, but it converts "green lie" → "red truth" without fixing anything. It's correct *process*, not *progress*. Absorb only where a fix-agent is already assigned to the exposed failures; otherwise it just inflates the red count.

## 2. dependabot majors — safe / landmine / close-with-note

**Safe (patch/minor):** serde 1.0.228→.229, ws 8.21.0→.1, ts-jest, prettier 3.8→3.9, pdfkit 0.18→.19.1, ioredis 5.10→5.11, yjs, markdown-it-deflist, `@types/node` 25.9→26.1 (same-major). Absorb.

**Landmines (close with doc note, do NOT absorb silently):**
- **typescript 5.9.3 → 7.0.2** across quilt-{nomad,swarm,pincher,elf,rag,fleet}, PersonalLog, fabric-mcp, CognitiveEngine, webgpu-profiler. TS 7 is the native-port rewrite — a different compiler, not a bump. Absorbing "because newer" is exactly the doctrine failure I'm paid to catch. Pin or close.
- **eslint 8→10** (flat-config breaking), **@typescript-eslint 7→8**, **@types/node 20→26**, **vitest 1→4**, **dockerode 4→5**, **commander 12→15**, **ioredis 5→6**, **next 15→16**, **jsdom 29→30**, **@types/express 4→5** — all true migrations, not bumps.
- **quilt-rust majors** (axum 0.7→0.8, thiserror 1→2, rmcp 0.2→3.1, tower-http 0.5→0.7) — Rust ecosystem majors, each a real code change; the rmcp 0.2→3.1 gap is enormous. Close-with-note.
- **actions/* majors** (checkout 4→7, setup-node 4→7, upload-artifact 4→7, download-artifact 4→8): move to Node 24 runners and change artifact semantics. Landmine unless the runner is verified; don't absorb into pinned-old-ubuntu workflows.

**Note:** the `FAILED ... workflow scope` quilt-jetson#1/#3 and `head not up to date` constraint-theory-py#1/plato-types#1 are **not red-CI** — they're OAuth-token-scope and stale-branch failures. The 14 `merge conflicts` are rebase work, not fix-agent work. Route them to rebase, not rewrite.

## 3. Verify-skepticism — pushback on visitor reports

- **crab-traps count: I push back on the visitor's "~378" as authoritative.** The edge-engineer said "~378 across 13 .test.ts files." Wrong on the file count — there are **10**, not 13. My grep: **385** `test(`/`it(` occurrences (naive, includes `.each` expansion). README now reads **341**. So the "corrected 152→341" is directionally right, but the visitor's "~378" is *also* an overcount — no single number is authoritative without a vitest run. **Recommendation: stop hand-maintaining counts; badge from CI output only.**
- **elephant counts: the visitors contradict each other** — statistician says "275 fns / ~26 files," edge-engineer "275 / 10 files," marine-ops "25 files," README "49 passed," front door "243+." Three reporters, three file counts. This *proves* the number is unmaintainable-by-hand, not that any visitor is right. Escalate the *mechanism* (CI badge), not a new number.
- **"500+ repositories" — I flag this as the single most falsifiable public claim.** Repo-gaps scout counted **250** local mirrors. Either the front door is counting historical/archived, or it's lore. Needs a factual fix, not a tone pass.
- **JEPA overclaim (statistician + edge-engineer) — I endorse it fully, no pushback.** `elephant/jepa.py` empty stub; `collective-unconscious/src/jepa.ts` is momentum extrapolation. Reproducible in five minutes. This is the org's biggest credibility leak and it is *earned* criticism.
- **Shared-art claim (marine-ops: reef-hero.jpg byte-identical to crab-traps hero) — I trust it** (md5sum-class check); no pushback.

## 4. Archived-clones — shared-remote risk (real)

`git remote -v` shows **two local dirs pointing at ONE remote**: `plainsong-worker` and `tapscript-worker` both → `SuperInstance/plainsong-worker.git`. `tapscript-worker` is the stale pre-rename mirror. If any fix-agent works in `tapscript-worker/` and pushes, it collides with `plainsong-worker` on the same remote. **Rule: archive-by-rename must be a local `mv`, never a git push.** The Captain's "archive by rename, don't delete" is fine; the shared-remote is the trap.

## 5. plainsong / tapscript-studio dedupe

Different remotes (`plainsong.git` vs `tapscript-studio.git`), same content. `tapscript-studio` README title = "Plainsong", pyproject = plainsong v1.4.0, `tapscript/` dir empty. Musician visitor: "identity crisis." **Keep `plainsong` canonical; archive `tapscript-studio` (redirect README + GitHub description).** Risk if not deduped: PRs filed on the ghost, number drift between two copies, the empty `tapscript/` dir as a fork-trap.

## 6. Casey decisions vs. panel-settled

**→ Casey (irreversible / public identity / security):** repo renames/archives (tapscript-studio, tapscript-worker); the "500+ repos" front-door claim; raw home-boat IP `147.224.38.131` in crab-traps README/lures/vars (touching lure text changes live behavior); crab-traps `database_id` real-vs-placeholder (only Casey knows which state is true); JEPA rename-vs-implement (org research identity).

**→ Panel can settle (reversible/mechanical):** dependabot patch/minor absorption; LICENSE-file additions (READMEs already claim MIT — adding the file matches claim to reality); the ternary + gap-hunt real-bug fixes; CI-badge-as-source-of-truth for test counts.

## 7. Dissent list (where "newer wins" is wrong)

1. **typescript 7.0.2 and friends:** newer compiler ≠ better. "Newer wins" must not mean blind major-bump; these are migrations, close-with-note.
2. **plainsong is the *older* name and the *canonical* repo; tapscript-studio is the newer name and the ghost.** Newer should not win here — dedupe keeps canonical, not newest.
3. **`remove failure masking` without a fix-agent is process theater, not progress** — "newer/cleaner CI" that only turns green→red buys nothing unless someone fixes the red.
4. **vitest 1→4 / eslint 8→10:** I'd let these wait — they're test-only and safe, but absorbing them now competes with real defect fixes for the same mechanical-agent hours. Sequence real bugs first.

*Bottom line: the honest gradient is real (fleetmath, zeroclaw pre-registration, crab-traps degradation design), but the org leaks credibility through exactly two channels — borrowed ML vocabulary ("JEPA") and unmaintainable hand-written numbers. Both are fixable cheaply. Don't let dependabot's "newer" doctrine trade away the one asset that actually works.*
