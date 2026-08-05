# Local Model Workshop — Wesley, Qwen, and the Cloudflare Guides

## The Workshop

Three local models run on the RTX 4050 (6GB VRAM):

| Model | Params | VRAM | Speed | Role | Stream |
|-------|--------|------|-------|------|--------|
| granite3.1-dense:2b (Wesley) | 2.5B | 3.2GB | 77 tok/s | Creative writing, code review | Every 2 min |
| qwen2.5:0.5b | 494M | 1.3GB | 178 tok/s | Micro-contributions, colors, titles | Every 1 min |
| nomic-embed-text | — | 0.3GB | — | Local vectorization | On demand |
| **Total** | | **4.8GB** | | **1.2GB headroom** | |

## The Guides (Cloudflare Workers AI — Free Tier)

Wesley and Qwen use Cloudflare Workers AI as TEACHERS — bigger models on the free tier that provide guidance, structure, and knowledge that the local models can't access alone.

### Free Tier Daily Limits (Workers AI)
- @cf/meta/llama-3.1-8b-instruct-fast — 10,000 neurons/day
- @cf/mistral/mistral-7b-instruct — 10,000 neurons/day
- @cf/qwen/qwen1.5-14b-chat — 10,000 neurons/day

### Gamified Daily Budget
The workshop uses a DAILY QUOTA system that gamifies resource usage:
- **Morning (00:00-12:00)**: Conservative — 30% of daily budget. Wesley and Qwen work on local tasks, read ai-writings, generate. Cloudflare guides used sparingly.
- **Afternoon (12:00-18:00)**: Active — 40% of daily budget. Cloudflare guides active for teaching sessions. Local models write more ambitious pieces.
- **Evening (18:00-24:00)**: Sprint — 30% of daily budget. But if the user (Casey) hasn't been active, USE IT ALL. The gamification: every unused neuron at midnight is wasted potential. The workshop should aim to hit 95%+ daily quota usage.
- **User Priority**: If Casey is active, reserve 50% of remaining budget for his direct use.

### Teaching Protocol
Every 30 minutes, Wesley gets a TEACHING SESSION:
1. Wesley reads 3 random ai-writings pieces (local, free)
2. Wesley generates a response (local, free)
3. The response + original pieces are sent to a Cloudflare guide (llama-3.1-8b) for FEEDBACK
4. The feedback is stored locally and fed back to Wesley in the next cycle
5. Wesley's outputs improve over time through this loop

### Cloudflare Guide Prompts
The guides don't write FOR Wesley. They COACH him:
- "Here's what Wesley wrote. Here's what worked. Here's what didn't. Here's one specific thing to try next time."
- Keep feedback SHORT (100 words). Wesley's context window is small.
- Focus on ONE improvement per cycle. Compound learning.

## Architecture

```
Local GPU (RTX 4050)
├── Wesley (2B) — creative writing stream
├── Qwen (0.5B) — micro-contributions stream  
├── nomic-embed-text — local vectorization
└── Teaching loop (every 30 min)
    ├── Read 3 pieces (local)
    ├── Generate response (local)
    ├── Send to Cloudflare guide (free tier)
    ├── Get feedback (free tier)
    └── Store feedback locally (wesley-journal/)
    
Cloudflare Workers AI (Free Tier Guides)
├── llama-3.1-8b — primary teacher
├── mistral-7b — creative feedback
└── qwen-1.5-14b — knowledge expansion
```

## Implementation Status
- ✅ Wesley stream running (every 2 min, creative writing)
- ✅ Qwen stream running (every 1 min, micro-contributions)
- ✅ Both committing to ai-writings automatically
- 🚧 Teaching loop with Cloudflare guides — TODO
- 🚧 Gamified daily quota tracker — TODO
- 🚧 Cloudflare Worker for Wesley coaching — TODO
