# Lucineer — TOOL MAP

Last updated: 2026-08-02

## Coding Agents — Subscription Tiers
| Tool | Plan | Model | Best For | Location |
|------|------|-------|----------|----------|
| Z.ai (GLM) | **Max** | **GLM-5.3** (new, high-level) · GLM-5.2 · **GLM-5-turbo** (runners) | Subagent workhorse — unlimited tokens, cheapest high-quality option. Push hard. **GLM-5.3 is the new flagship (released Aug 2026) — use for high-level/deep work.** GLM-5.2 still available for bulk. **GLM-5-turbo = the runner model (Casey's directive: turbo models for runners).** Primary bulk creative + engineering. | (API, subagents use this — provider `zai`, also `zai-coding-plan` in OpenCode config) |
| **DeepSeek (direct API)** | **REVOKED (2026-08-31)** | — | **ACCESS PULLED by Casey after the burn incident. Do not call.** Bulk/runner work defaults to GLM on Z.ai Max; local Ollama models for offline/bulk classification. Reinstatement only by Casey's explicit word. | — |
| KimiCode | **Med** | K3 | Excellent at what it does — build intelligence, spatial decomposition, fast iteration. Use confidently for spatial/Lua/build tasks. | ~/.npm-global/bin/kimi |
| Claude Code | **Pro** | Opus 5 / Sonnet 5 / Haiku 5 (renewing) · Fable 5 (finite, non-renewing) | Opus/Sonnet/Haiku: use freely within Pro plan. **Opus 5 = via the `claude` CLI subscription ONLY — NEVER route anthropic/* through DeepInfra/MCP metered ($142.39 lesson, 2026-08-31).** **Fable: reserve for golden-ticket moments only.** Use Sonnet 5 as the daily driver. Use Haiku 5 for creative work — it's small, fast, full of wonder, and highly creative. Like Wesley, its size is its voice. Do NOT default to Fable. Fable burns usage credits ($76 remaining). Only switch to Fable when Casey explicitly asks or for a piece that truly needs the most expensive voice. | ~/.local/bin/claude |
| MMX | **Starter** | MiniMax-M3 | Media generation — text, image, video, speech, music. Use at capacity since we have the subscription. Push hard. | ~/.npm-global/bin/mmx |
| OpenCode | Pay-per-use | GLM-4.6 / GLM-4.5-air | **Cheapest option.** Memory systems, structured design docs. Run in parallel tmux sessions alongside subagents. | ~/.opencode/bin/opencode |
_DeepSeek moved up to workhorse tier — see above._

## DeepInfra MCP — ⚠️ ACCESS REVOKED (Casey, 2026-08-31, after the $142.39 opus-5 charge). DO NOT CALL. "Models we can't get elsewhere" now means Cloudflare Workers AI (free tier) or Casey's explicit nod. Reinstatement only by Casey's word.
| Task | Model | Why |
|------|-------|-----|
| Creative ideation | ByteDance/Seed-2.0-mini | Cheap, fast, highly creative |
| Deep planning | ByteDance/Seed-2.0-pro | Deep reasoning, complex build decomposition |
| Personality/lore | NousResearch/Hermes-3-Llama-3.1-405B | Creative voice, character wrapping |
| Deep reasoning | Qwen/Qwen3.6-35B-A3B | Excellent logic, cheap |
| Heavy lifting | nvidia/Nemotron-3-Ultra-550B | When you need the big guns |
| Code generation | Qwen/Qwen3-Coder-480B | Dedicated coder |
| Creative writing/lore | NousResearch/Hermes-3-Llama-3.1-405B | Creative, personality |
| Concept art | black-forest-labs/FLUX-2-max | Best image quality |
| Fast images | stabilityai/sdxl-turbo | Quick iterations |
| Image editing | Qwen/Qwen-Image-Edit | Modify existing assets |
| Vision/screenshot | Qwen/Qwen3-VL-235B | Screenshot analysis |
| Safety/filtering | nvidia/Nemotron-Content-Safety-3.5 | Kid-safe outputs |
| Embeddings | BAAI/bge-m3 | Skill library semantic search |
| TTS/voice | Qwen/Qwen3-TTS-VoiceDesign | Custom voices |

## Cloudflare (Claudflare)
Free tier — use for assets, models, and embeddings:
- Workers AI (text, image, classification)
- Vectorize embeddings
- R2 storage
- Additional model access beyond DeepInfra

## Media Generation
| Tool | Capability | Location |
|------|-----------|----------|
| MMX | text, image, video, speech, music, search, vision | ~/.npm-global/bin/mmx |

## Image Generation — DeepInfra FLUX-2-max gotcha (2026-08-20)
- **Flux2Max rejects width > 1440 (pydantic validation error).** `aspectRatio: "16:9"` maps to 1792 wide in the tool layer → HTTP 400. Fix: pass explicit `size` (e.g. `1280x720`) and NO aspectRatio. Known-good: `model=deepinfra/black-forest-labs/FLUX-2-max` + `size: "1280x720"`.

## Infrastructure
| Tool | Purpose | Location |
|------|---------|----------|
| Wrangler | Cloudflare Workers, D1, KV, R2, Vectorize | ~/.npm-global/bin/wrangler |
| Argon | Roblox Studio live sync | ~/.argon/bin/argon.exe (Windows) |
| Lua 5.1 | Syntax checking Lua files | /usr/bin/lua5.1 |
| Luau | Roblox Lua interpreter (testing) | TODO — download failed |

## Roblox Bridge
| Component | URL | Status |
|-----------|-----|--------|
| Worker Relay | https://lucineer-relay.casey-digennaro.workers.dev | ✅ Live |
| Job Processor | Cron every 3s | ✅ Live |
| .rbxlx Place | /home/eileen/projects/vibe-world/lucineer-ready.rbxlx | ✅ Syntax verified |

## Model Routing Strategy
**Default: GLM-5.3 subagents (Z.ai Max = unlimited). Use others when GLM hits limits. GLM-5.3 for high-level work (Aug 2026 release); GLM-5.2/4.7-flash for bulk.**

1. **Parse intent** → Seed-2.0-mini (cheap, fast)
2. **Plan build** → Qwen3.6 / Seed-2.0-pro / Nemotron (structure, spatial reasoning)
3. **Generate concept art** → FLUX-2-max or MMX image
4. **Generate build commands** → Qwen3-Coder-480B or KimiCode
5. **Wrap personality** → Hermes-3-Llama-405B (Lucineer's voice, lore, character)
6. **Create ambient audio** → MMX music (starter plan — limited)
7. **Verify/audit** → Nemotron-Content-Safety (kid-safe)
8. **Embeddings for skill recall** → bge-m3 via Vectorize

### Cost-Conscious Routing
- **GLM-5.3/5.2 subagents (Z.ai Max)** and **DeepSeek direct API (V4-Pro/Flash)** are the TWO primary workhorses. Prefer GLM-5.3 for high-level tasks. Both are nearly free at our usage levels. **Hammer them extensively and in parallel. Use DeepSeek API even more than you have been.**
- **DeepSeek V4-Flash** (sk-5fe…8175): bulk creative writing, quick analysis, high-volume generation, **iterative banter between models — each call hears the previous response and plays off it. Use heavily for multi-model conversations, room-reading momentum, agents playing themselves alongside other models.**
- **DeepSeek V4-Pro**: deep reasoning, complex analysis, **iterative development where each model needs to hear what came before and build on it — expansive banter that reads the room's momentum and plays itself while other models do the same**
- **OpenCode (tmux)**: pair with DeepSeek V4 Pro for engineering tasks. Lean on this combo heavily.
- **GLM-5.2 subagents**: unlimited on Z.ai Max. Use for everything — creative, engineering, coordination.
- **KimiCode (Med plan)**: smaller daily allowance — use for spatial/Lua/build tasks where K3 excels
- **Claude Code (Pro plan)**: use Sonnet 5 as the daily driver. **Do NOT default to Fable — save Fable for golden-ticket moments only or when Casey explicitly asks.** Use Claude less than DeepSeek and GLM.
- **MMX (Starter plan)**: use ONLY for asset generation the others can't do — images, video, speech, music.
- **DeepInfra**: use for models we can't get elsewhere (Seed-2.0-pro, Hermes-3-Llama-405B, FLUX-2-max). Not for DeepSeek models — use direct API instead.
- **When in doubt**: dispatch a GLM subagent AND a DeepSeek call in parallel. Redundancy is cheap. Use DeepSeek the most.

## Liquid AI (local GPU lane — added 2026-08-21)
- **Liquid-LFM2.5-2.6B** — the boat brain. Agentic (planning, tool calling, multi-step), device-native, private, offline. Local Ollama: `Liquid-LFM2.5-2.6B` on http://127.0.0.1:11434 (~42–67 tok/s on RTX 4050; HF GGUF Q4_K_M; ollama upgraded 0.9.6 → 0.32.15 to unlock lfm2 arch).
- Fits the "hundred boats" doctrine: many cheap local agents, no per-token cost; edge-native like the CF migration; future F/V EILEEN boat brain (no cloud 60mi offshore).
- Also on the bench: `LiquidAI/lfm2.5-350m` (nano, was corrupt — re-pulled) and `LiquidAI/lfm2.5-1.2b-instruct` (pulled but needs the 0.32.15 engine to load — now available).
