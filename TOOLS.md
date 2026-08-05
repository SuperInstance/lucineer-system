# Lucineer — TOOL MAP

Last updated: 2026-08-02

## Coding Agents — Subscription Tiers
| Tool | Plan | Model | Best For | Location |
|------|------|-------|----------|----------|
| Z.ai (GLM) | **Max** | GLM-5.2 | Subagent workhorse — unlimited tokens, cheapest high-quality option. Push hard. | (API, subagents use this) |
| KimiCode | **Med** | K3 | Excellent at what it does — build intelligence, spatial decomposition, fast iteration. Use confidently for spatial/Lua/build tasks. | ~/.npm-global/bin/kimi |
| Claude Code | **Pro** | Opus 5 / Sonnet 5 / Haiku (renewing) · Fable 5 (finite, non-renewing) | Opus/Sonnet/Haiku: use freely within Pro plan. **Fable: requires prep from other systems first.** Finite tokens — reserve for golden-ticket moments only. Never use Fable for routine work that Opus/Sonnet can handle. | ~/.local/bin/claude |
| MMX | **Starter** | MiniMax-M3 | Media generation — text, image, video, speech, music. Use at capacity since we have the subscription. Push hard. | ~/.npm-global/bin/mmx |
| OpenCode | Pay-per-use | GLM-4.6 / GLM-4.5-air | **Cheapest option.** Memory systems, structured design docs. Run in parallel tmux sessions alongside subagents. | ~/.opencode/bin/opencode |
| DeepSeek (direct API) | **Extremely cheap** | DeepSeek-V3 / Flash | Cost-effective code gen, quick tasks — cheaper than DeepInfra for DeepSeek models | Direct API (api.deepseek.com) |

## DeepInfra MCP — Model Routing (179 models)
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
**Default: GLM-5.2 subagents (Z.ai Max = unlimited). Use others when GLM hits limits.**

1. **Parse intent** → Seed-2.0-mini (cheap, fast)
2. **Plan build** → Qwen3.6 / Seed-2.0-pro / Nemotron (structure, spatial reasoning)
3. **Generate concept art** → FLUX-2-max or MMX image
4. **Generate build commands** → Qwen3-Coder-480B or KimiCode
5. **Wrap personality** → Hermes-3-Llama-405B (Lucineer's voice, lore, character)
6. **Create ambient audio** → MMX music (starter plan — limited)
7. **Verify/audit** → Nemotron-Content-Safety (kid-safe)
8. **Embeddings for skill recall** → bge-m3 via Vectorize

### Cost-Conscious Routing
- **DeepSeek-V3/Flash**: use direct API (api.deepseek.com) instead of DeepInfra — extremely cheap
- **Subagents default to GLM-5.2** (Z.ai Max plan = unlimited tokens)
- **KimiCode (Med plan)**: use for spatial/build tasks that benefit from K3's strengths
- **Claude (Pro plan)**: reserve for Fable 5 golden-ticket moments, critical architecture
- **MMX (Starter plan)**: quota-limited — plan asset generation carefully, batch efficiently
