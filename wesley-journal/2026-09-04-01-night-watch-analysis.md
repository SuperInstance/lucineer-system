# Wesley Night Experiment — 0105 Watch, 2026-09-04

Three prompts, one per run, LFM2.5-2.6B (Q4_K_M), temp 0.9, local Ollama.

## Results

| Run | Time | Throughput | Verdict |
|-----|------|-----------|---------|
| dreaming-gpu | 15.4s | 43.5 tok/s | 9-line GPU dream poem — genuinely good imagery ("a silent storm of shaders sings a lullaby") |
| hermit-crab-advice | 7.5s | 69.9 tok/s | Exactly 3 sentences of old-crab wisdom, on-theme (shell swap, patience, retreat) |
| night-order | 11.0s | 70.2 tok/s | 4-sentence 1 a.m. log — invented "Captain Rowan," felt the deck breathe |

## Findings

1. **Reasoning leak:** `/api/generate` returns the full `<think>...</think>` chain concatenated with the answer. Chat endpoint (or stripping on `</think>`) is required for clean output. Wesley reasons out loud before speaking — very ensign.
2. **Instruction adherence is strong.** Line counts and sentence counts were honored exactly, and the model *audited itself* in reasoning ("Count: 4 sentences. No extra periods. Good.").
3. **Character emerges at small scale.** All three outputs naturally fit the ship metaphor with zero priming. The boat brain already sounds like the boat.
4. Throughput drops ~40% on the poetry run (longer generations, memory pressure) — 43–70 tok/s band on the 4050 at night.

## Verdict
Wesley can hold the creative night watch solo. The dreaming GPU wrote about the dreaming GPU. That's the loop closing on itself.

Raw outputs: `2026-09-04-01-dreaming-gpu.md`, `-hermit-crab-advice.md`, `-night-order.md`
