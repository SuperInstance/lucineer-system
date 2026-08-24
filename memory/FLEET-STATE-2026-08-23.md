# FLEET STATE — 2026-08-23 (master continuation doc)

*Written by Lucineer for future Lucineer context windows. If you are reading this fresh: this file + LANE-LEDGER.md + CONTINUATION.md are your bootstrap. Trust them over memory of "yesterday".*

## The Ship — repos, URLs, deploy paths

| Repo | Path | Live at | Deploy path |
|------|------|---------|-------------|
| Scrapcraft (web game) | /home/eileen/projects/Scrapcraft | https://fleet-static-host.casey-digennaro.workers.dev/scrap/ | `npm run build` → `cp -r dist /home/eileen/projects/fleet-static-host/public/scrap` → `cd fleet-static-host && npx wrangler deploy`. **Tell users to hard-refresh (Ctrl+Shift+R) after every deploy — no cache busting yet.** |
| fleet-static-host | /home/eileen/projects/fleet-static-host (branch `master`!) | workers.dev root: lobby (tapestry+TRAILS), /papers /writings /mist /ternary | `npx wrangler deploy` |
| scrapcraft cloud saves | Scrapcraft/cloudflare | separate worker `scrapcraft` | `npx wrangler deploy` in cloudflare/ |
| saddle | /home/eileen/projects/saddle | — (library) | npm test = node --test |
| superinstance (org root) | /home/eileen/projects/superinstance | public | Kennel Vol I+II on main |
| scrapcraft-roblox | /home/eileen/projects/scrapcraft-roblox | — | branch `phase1-yard` = yard + MVP loop |
| scrapcraft-roblox-bible | /home/eileen/projects/scrapcraft-roblox-bible | — | extraction data (partial) |
| dsh-assessment | /home/eileen/projects/dsh-assessment | — | ASSESSMENT.md — verdict: SIDESTEP; option = FLUX-as-plugin weekend |

## Scrapcraft main state (evening Aug 23)
- main @ ~4699f5b+: HUD entropy fixes deployed (ab9d84a2). 1891+ tests.
- Merged today: companion roundness, banter variety+ChatterGuard, ambient life, first-hour, chapters 7-9, perf+touch, opening cinematic+Mo's Ledger(J), teaching payload, QC rewrites, coach/VHF radio, cinema+tutorial missions+VETERAN RIDE, save-semantics (full-payload autosave), zone-gate fixes, USCP emitter (opt-in), classroom unit 1, research doc, Rift docs.
- Known live issues: none confirmed open. Casey's E-menu errors = stale cache (repro'd clean).
- **THE loudest gap (research doc): ZERO real kids have playtested. Highest-value next step = one real kid session, then rig v4.**

## Doctrine (Casey directives — standing)
- **Routing:** GLM-5.3 (z.ai)= planning/envisioning/strategy. DeepSeek V4-Flash = runners (spawn model="deepseek/deepseek-v4-flash"). kimi+opencode in tmux = coder passes (kimi 403s → opencode+claude fallback). DeepInfra MCP = wider consults (Seed-2.0-pro, Hermes-405B, Qwen3.6).
- Serial lanes: >6-8 concurrent GLM lanes starve/die. Worktrees + COMMIT EVERY ~10 MIN (checkpoint doctrine) = deaths are recoverable. Lanes merging to main MUST run node --check + npm run build + full suite BEFORE push.
- Tapestry: trails/misses are first-class content (lobby TRAILS section live).
- Archive by rename, never destroy. No secrets in repos (swept before public flip — all SuperInstance repos now PUBLIC).
- Image-gen: local/CF free lanes free; FLUX-2-max needs Casey's nod per campaign.

## Open decisions awaiting Casey
1. DSH: FLUX-as-plugin weekend experiment (recommended by assessment) — Casey said "do it all" 15:05 → treat as approved, keep it seam-harvest only, never migrate.
2. Kid playtest scheduling (needs a real kid — Casey's son).

## Key docs
- Scrapcraft/docs: CURRICULUM.md, RESEARCH-2026-08.md, VHF-DOCTRINE.md, cns/{RIFT-PHASE-1,MAPPING-SPEC-V2,RIFT-MANIFESTO,KINETIC-REPORT}.md, classroom/UNIT-1.md, VOICE-QC.md (in src or docs)
- saddle/docs: ARCHITECTURE, FIELD-TRIAL-1/2, RIDER-TAXONOMY, VESTIGES, HARNESS-VS-SWARM, INVISIBLE-HARNESS
- memory/: daily notes 2026-08-23 (full day log), scrap-beta-report{,-v2,-v3}.md
