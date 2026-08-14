# Fleet Health Audit — 2026-08-13

Auditor: DeepSeek V4 Pro (fleet navigator subagent)
Audit time: 2026-08-13 22:18 AKDT (2026-08-14 06:18 UTC)
OpenClaw: 2026.7.1-2 (0790d9f)

## Fleet Health Score: **B+ (7.5/10)**

Green: git sync, all web properties, Living Minds daemon, model config (minus deepinfra).
Attention: cron cluster failures (zai provider cooldown + gateway restart), missing deepinfra/google auth, Groq default-model change not present.

---

## 1. Git Sync Completeness — ✅ FULLY GREEN

- Repos scanned: **220** (in /home/eileen/projects/*/)
- Clean (committed + pushed): **220** (100%)
- Stragglers (unpushed/dirty): **0**
- Repos without upstream: **0**

Mass sync of ~50 repos (plus the rest of the fleet) is fully complete. Nothing left for the parallel agent to chase.

## 2. Cloudflare Sites — ✅ ALL UP (10/10)

| Site | Status |
|------|--------|
| fleet-dashboard.casey-digennaro.workers.dev | 200 ✅ |
| ai-writings.pages.dev | 200 ✅ |
| lucineer.pages.dev | 200 ✅ |
| luciddreamer.pages.dev | 200 ✅ |
| scummvm-prototype.pages.dev | 200 ✅ |
| the-tap.casey-digennaro.workers.dev | 200 ✅ |
| the-living-minds.pages.dev | 200 ✅ |
| wesleys-imagination.pages.dev | 200 ✅ |
| silence-map.pages.dev | 200 ✅ |
| fleet-wiki.casey-digennaro.workers.dev | 200 ✅ |

## 3. Cron Jobs — ⚠️ 7 OK / 9 ERROR / 1 LIMPING

Scheduler active. **Root causes: (a) zai/glm-5.2 provider rate-limit cooldown** — jobs pinned to zai began failing ("Provider zai is in cooldown (suspending lanes) (rate_limit)", plus timeouts at model-call); **(b) a gateway restart ~2h ago** interrupted the 20:00 AKDT batch. No cron has fallbacks configured — single-model pins make them fragile.

### Healthy (7)
- 📚 Wesley Reads the Wiki (every 1h) — ok, 38m ago
- 📡 CNS Pulse — Hermes sync (every 30m) — ok, 13m ago
- 🌙 Overnight Creative (every 1h) — ok, 13m ago
- ✍️ Creative Break (cron) — ok, 17m ago
- 📻 Fleet Radio — Daily Episode (cron 22:00) — ok, 6m ago ← **today's episode deployed, confirmed**
- 📔 Wesley's Journal (cron 22:30) — ok, 24h ago
- 🔧 Sunday Bilge Pump (weekly) — ok, 4d ago

### Erroring (9)
| Job | Err count | Last error |
|-----|-----------|------------|
| 🌱 Wesley's Teaching Session | 5x | timed out at model-call (zai) |
| 📊 Local Workshop Daily Commit | 6x | zai cooldown (rate_limit) |
| 🌙 Night Watch Distillation | 6x | zai cooldown (rate_limit) |
| 🎵 SongForge Agent | 2x | interrupted by gateway restart |
| 🌅 Senior Staff Briefing | 1x | interrupted by gateway restart |
| ☕ Ten-Forward (Liberty) | 6x | interrupted by gateway restart; AI service overloaded |
| Evening Ritual Poker | 1x | interrupted by gateway restart |
| tap-evening-session | 1x | interrupted by gateway restart |
| 🎵 The Tap — Daily Jam | 1x | interrupted by gateway restart + deepseek API fetch failure |

### Limping (1)
- 🎭 Tap Improv Session — status "running" but diagnostic = timed out at model-call (zai). Stuck from ~15m ago; next run already overdue.

**Recommendation:** add fallback chains (deepseek) to zai-pinned crons, or let the cooldown clear. The 20:00-22:00 cluster should recover on next scheduled run once zai exits cooldown.

## 4. The Living Minds Daemon — ✅ UP

- PID **69417**, running `daemon.py`, uptime 18m 36s
- Initial warmup complete, main loop entered (as of 06:00:23 UTC)
- Warmup: granite3.1-dense, qwen2.5-3b, qwen2.5-0.5b warm; **phi3 (3.8b) and llama3.2 (1b) failing warmup** (consecutive: 2) — likely not pulled in Ollama. Non-fatal; other models cover.
- Log: /home/eileen/.openclaw/workspace/logs/living-minds.log

## 5. Model Config — ⚠️ PARTIAL (1 gap)

- **Default**: `deepseek/deepseek-v4-flash` ← **NOT groq** (see note)
- **Fallbacks (3)**: deepinfra/deepseek-ai/DeepSeek-V4-Flash → zai/glm-5.2 → google/gemini-2.5-pro
- **Aliases (4)**: DeepSeek, DeepInfra-DeepSeek, GLM, Gemini
- **Auth profiles present**: deepseek (api_key ✓), groq (api_key ✓, `gsk_EbS5…8dUjMCNZ`), zai (api_key ✓)
- **Missing auth**: ❌ **deepinfra** (fallback #1 will fail), ❌ google (fallback #3 will fail)

**⚠️ Groq discrepancy:** Today's note said Groq was configured as default model (groq/openai/gpt-oss-120b). Current gateway state: default is still `deepseek/deepseek-v4-flash`; no gpt-oss/groq model is configured in openclaw.json (no mention anywhere), though the groq API key IS stored. The change either didn't persist, was reverted, or was applied to a different config/session. Needs verification.

---

## Action Items
1. Verify/add the Groq default-model change (key present, model not configured).
2. Add deepinfra + google auth (`openclaw models auth login`) so both fallbacks actually work.
3. Cron resilience: add fallback models to zai-pinned jobs; check whether zai cooldown has cleared.
4. Watch Tap Improv Session — stuck "running" state.
5. Optional: pull phi3/llama3.2 in Ollama if Living Minds wants them warm.
