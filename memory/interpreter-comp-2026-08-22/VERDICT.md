# INTERPRETER COMPETITION — JUDGE'S SYNTHESIS
*Riker adjudicating, 2026-08-22 11:00 AKDT. Entries: arch-kimi.md (208L), arch-opencode.md (397L), arch-claude.md (558L). Naming workshop: names-deepseek.md, names-deepseek-r2.md, names-hermes.md.*

## Convergences (the fleet has already decided these, whoever builds)
1. **Separate repo, sibling to elephant** — all three: elephant stays numpy-pure; interpreter tails `data/production-log.jsonl`. The seam already exists.
2. **Interpretation = structured JSON first, prose second** — numeric per-dial deltas + direction/magnitude/horizon predictions + a step-back synthesis. Comparability is enforced by schema (fixed enums, quantized bands), not asserted.
3. **Mechanical judge first, model judge second, human anchor third** — deterministic replay of predictions against subsequent readings is unbribeable arithmetic; the LLM judge handles nuance; humans anchor calibration.
4. **Chain-sealed interpretation ledger** — sha256 chain per the cell-ledger pattern (Ammann bars: locally decodable global phase). Interpretations accumulate as first-class fleet artifacts.
5. **Best-of-n sampling at generation → free preference pairs → DPO flywheel** (both Kimi and OpenCode independently). SFT cold-start (~50-100 gold interpretations) before DPO.

## The one real disagreement: base model
- **Kimi:** Qwen3-4B-Instruct-2507 (4-bit QLoRA, r=16, ctx 2048) — "2B is a toy, 8B is a lie, 4B is the horse." Diversity argument: don't reuse Granite/Liquid (judge-split hygiene).
- **OpenCode (mahout):** Qwen3-4B too (unsloth), with honest VRAM math; 8B named as inference-only oracle; Granite 2B "trains fine but analytical ceiling too low."
- **Claude:** Granite 3.1 2B (Wesley-adjacent stack reuse, fastest train cycle, most headroom for iteration count).
**Ruling: 2-to-1 for Qwen3-4B, and the diversity argument is sound — Wesley's Granite body stays Wesley's; the interpreter gets its own inductive bias. Casey gets the final call with the VRAM caveat (6GB = tight; unsloth 4-bit verified by two entries).**

## Second disagreement: the Wesley merge
- Kimi: NO merge — different cognitive roles; Wesley consumes interpretations.
- OpenCode: NO on weights/role, YES as a tool Wesley consults — "an interpreter embedded in the agent cannot certificate its own phason" (the Penrose argument, the deepest line in the competition).
- Claude: NO — conversationalist vs retrospective reader.
**Ruling: unanimous NO on merging weights. Wesley grows BY CONSULTING the interpreter, never BY BECOMING it. OpenCode's phason-certificate framing is the doctrine.**

## Naming — the workshop's yield
Round 1 (10), Round 2 (kill/add), Hermes round (3). Standouts:
- **MAHOUT** (the elephant's keeper — OpenCode led with it; instantly graspable, role-true: "the elephant reads the room; the mahout reads the elephant")
- **TIDE** (Hermes's pick — "short, true, and it moves"; reads the field as currents; conflicts with nothing)
- **TUSK** (the sensing organ; pokes into per-delta meaning)
- **WESLEY, THE GROWN** (if merge ever revisited — it isn't, per above)
- **UMBRA** (tracks the shadow of what's unsaid — poetic, maybe too dark for a deck call-out)
**Shortlist for Casey: MAHOUT (structural truth, fleet-intuitive) vs TIDE (Hermes's voice, boat-true). Both survive a deck call-out. Recommendation: MAHOUT — it names the RELATION (keeper↔elephant), not just the reading.**

## Build order (synthesized; ready for a GO)
1. Repo `SuperInstance/mahout` (pending name), package tailing production-log.jsonl; interpretation schema v1 (JSON+prose, predictions, enums); chain seal.
2. interp-infer systemd service + best-of-2 sampling off local llama-server (Qwen3-4B base until LoRA v1).
3. interp-score.timer — deterministic judge (predictions vs realized readings).
4. 50-100 gold interpretations (SFT cold start; judge-scored, human-spot-checked).
5. First DPO cycle → LoRA v1 → champion/challenger A/B on held-out week.
6. Wesley integration: consults, never merges.

## Provenance
All three architectures + three naming rounds on file in this directory. No repo created yet; awaiting Casey's GO + name pick.
