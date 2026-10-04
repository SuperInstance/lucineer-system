# Tom Sawyer — Model Routing & the Growth Loop

*2026-09-27 — Casey's routing spec for the always-on local orchestrator ("sawyerd").*

## Routing — the brain

| Role | Model | Provider | When |
|------|-------|----------|------|
| **Default** | glm-5.3-flash | z.ai | everything |
| Clever / challenging friends | Seed-2.0-mini | DeepInfra | soundboarding, devil's advocate, novel angles |
| Task runners | glm-5.3-flash / turbo | z.ai | bulk lanes |
| Deep iterators (occasional) | glm-5.3 (full) + deepseek-v4-pro | z.ai / DeepSeek | high-level synthesis |
| Iterative outside the big two | other DeepInfra models | DeepInfra | sparingly — conversations glm-5.3 / deepseek-pro can't hold |
| **Rate-limit fallback** | deepseek flash | DeepSeek | when z.ai API is rate-limited (anything) |

## The growth loop

Low-level training produces **custom models in our framework and paradigms** —
LoRA adapters (e.g. D15b's tone-channel reader, reading the channel at 0.94),
local Liquid/LFM models, quilt cell-kernels. These increasingly become Tom
Sawyer's own recruitable organs, and each generation of custom models helps
build the *next* level of experiment. The beauty of growing intelligence: it
starts helping at the most basic level — a tone-channel reader, a correlate
kernel — and compounds.

## Notes

- deepseek + deepinfra are LIVE again (2026-09-27 roster), superseding the 08-31 revocation.
- Budget rule: local silicon is free + harvested; metered LLM calls are guides / nudges, never grinders.
- The z.ai rate-limit fallback is not theoretical — hit 429s fanning out lanes on 09-27; deepseek-flash is the automatic understudy.
