# Oracle → Cloudflare Migration Design — SuperInstance Fleet

**Date:** 2026-08-21 · **Author:** Cloudflare migration planner (GLM-5.3 subagent)
**Directive (Captain, 2026-08-21):** migrate everything off the Oracle instance to a permanently persistent, clever system on Cloudflare; keep the ability for any developer to run their own instance; every public example must be explorable via Cloudflare Pages/Workers, not the Oracle server.
**Inputs:** /home/eileen/projects (309 dirs, ~250 active mirrors), memory/consensus-decision-2026-08-21.md, TOOLS.md, WEBSITE_DEPLOYMENT.md, repo READMEs (crab-traps, quilt-cloudflare, the-tap/ARCHITECTURE-CLOUDFLARE.md, fleet-radio, luciddreamer-ai, elephant, superinstance-ai, fleet-dashboard, study-oracle1).
**Read-only session — no repos modified.**

---

## 0. What "Oracle" means today (finding)

The Oracle footprint is **study-oracle1** (Oracle Cloud ARM64 host, aarch64) — the "Managing Director lighthouse" vessel charter that runs a command hierarchy of agents (JetsonClaw1 edge, OpenManus, Navigator, etc.) plus vessel/workspace repos. It is an **agent host**, not primarily a web host. The public web surfaces already live on Cloudflare (see §1 "Live today"). The migration therefore has two halves:

1. **Public examples & demos** → already largely CF-deployable; finish the job, make every one self-deployable by a stranger (§3).
2. **The Oracle1 vessel runtime** (long-lived agent orchestration) → decompose into CF-native persistence (D1/DO/Cron/Queues) + one **persistent engine** on the WSL2 workstation under systemd (§5), then retire the Oracle box.

---

## 1. Inventory & disposition

**Live on Cloudflare today (already done):** `lucineer-relay` Worker (Roblox bridge, cron every 3s), `ai-writings.pages.dev`, `luciddreamer-ai` Worker (luciddreamer.ai, KV persistence + 2 cron triggers), `crab-trap-funnel` Worker (D1 + reef cron + /wander), `fleet-dashboard` Worker, `superinstance.ai` front door (static), Pages sites: lucineer-com, activelog, fishinglog, activeledger. GitHub Pages: plainsong playground demo.

### Disposition table (family-level; named examples explicit)

| Repo / family | Today | Target CF surface | Disposition |
|---|---|---|---|
| **crab-traps** (+ crab-trap-web) | Worker live w/ D1 + cron | **Reference pattern**: Worker API + D1 (catches/lineage) + Vectorize (lure/reef embeddings, in worker/ already) + Cron (lure breeding) + R2 (lure images) | **MIGRATE-DONE** — promote to fleet reference template; scrub `<BOAT_IP>` → hostname (OPEN #4 in consensus doc) |
| **luciddreamer-ai** | Worker + KV live | Worker + KV (history) + D1 (ranked corpus) + Pages front | **MIGRATE-DONE** — already has honest quickstart convention (wrangler.example.toml, .dev.vars.example, BYOK) — adopt fleet-wide (§3) |
| **ai-writings** (+ vectorizer) | Pages live | Pages static + R2 (audio/artwork) + Vectorize (semantic index) | **MIGRATE-DONE** for static; add Vectorize index |
| **fleet-radio** | Runs from WSL2 via cron-agent (tsx pipeline), deploys to ai-writings Pages | Worker + **Cron Triggers** (replace crons.json agent-crons) + **Queues** (episode pipeline: fetch Tap → score → images → TTS → assemble) + R2 (episode audio/images) | **MIGRATE** — highest-value conversion; Queues fits the multi-step nightly/weekly pipelines (incl. Variety Hour) |
| **the-tap** | ARCHITECTURE-CLOUDFLARE.md spec'd; rooms/local parts on boat/WSL2 | **Durable Objects** (per-room live state, WebSocket rooms) + Tap-Gateway Worker (WS router) + KV (sessions) + D1 (transcripts) + Queues (open-mic async turns) | **MIGRATE (build)** — the spec already names every surface; DO is the live-state layer |
| **tap-frontend / tap-gamenight** | local | Pages (frontend) served by the Tap gateway | **MIGRATE** |
| **plainsong / plainsong-worker / plainsong-mcp / tapscript-studio (→archived)** | GH Pages playground | Pages static (playground) + Worker (compiler API) | **MIGRATE** — playground to superinstance.pages.dev subpath; per consensus A1 tapscript-studio retires into plainsong |
| **quilt-cloudflare** | Deployable runtime (D1+Vectorize+KV+R2, schema.sql, `wrangler init --from`) | Already the exact fleet pattern — Worker + D1 + Vectorize + KV + R2 | **MIGRATE-DONE** — second reference template; use as the D1-as-spine exemplar |
| **quilt family** (swarm/fleet/pincher/rag/k3s/nomad/elf/evolve/ai/rust) | mixed runtimes (k8s/nomad/elf targets stay local) | quilt-cloudflare pattern where interactive; k3s/nomad/elf/rust variants **KEEP-LOCAL** (they target other platforms by design) | **SPLIT** |
| **elephant** | local research, 275 tests, no CI | Pages (dashboard of dials reading a demo feed) + Worker API for scoring endpoints; GPU training runs **KEEP-LOCAL** (WSL2/Jetson) | **SPLIT** — research compute local, explorable demo on CF |
| **elephant-sim-worker** | worker scaffold | Worker + DO (simulated room field state) | **MIGRATE** |
| **fleet-gateway** | Python gateway, live-deployed organ (consensus P1b) | Router stays as organ; add thin CF Worker front (routes→example Workers) once CI honest | **MIGRATE (phase 3)** |
| **fleet-radio, fleet-tts, fleet-midi, fleet-audio, fleet-jepa-midi** | local pipelines | Queues producers/consumers + R2 output + Pages presentation | **MIGRATE (pipelines)** |
| **fleet-dashboard, fleet-embed, fleet-memory, fleet-wiki, fleet-scribe, fleet-discovery, fleet-config, fleet-inventory** | mixed | Each small Worker or DO; fleet-embed → Vectorize writer; fleet-memory → D1+Vectorize read/write API | **MIGRATE (phase 3)** |
| **superinstance-ai** (front door) | static + custom domain | Pages; add **example catalog** section (§3) | **ENHANCE** |
| **lucineer-*** (com-site, worker, brain, memory, vector, creative, roblox, system) | relay Worker live | Keep relay; lucineer-vector → Vectorize; lucineer-memory → D1; site → Pages | **MIGRATE-DONE/partial** |
| ***-ai-site / *-ai-pages** (activelog, fishinglog, activeledger, luciddreamer-content) | Pages live | Pages static | **MIGRATE-DONE** |
| **mud-arena / mud-engine / git-native-mud / ec2mud** | boat/WSL2 | DO (rooms) + D1 (world) — the Tap pattern minus LLMs; or KEEP-LOCAL if boat-coupled | **SPLIT (phase 4)** |
| **hermes-cloudflare** | scaffold | Worker | **MIGRATE** |
| **casting-call, officers-quarters, playtest-journals, wesley-journal, PersonalLog, SmartCRDT, CognitiveEngine, SuperInstance-papers, zeroclaw-dissertation, study-\* (≈90), research repos, pypi/engine repos (adinkra-math, plato-engine-block-c, constraint-theory-py, flux-genome-rs, quicunnel, holodeck-c, nexus-edge-runtime, edge-compiler, ternary-*)** | local | — | **KEEP-LOCAL** (dissertation, research, engines; engines run on WSL2/Jetson where compute/scale needed) |
| **Roblox bridge** (lucineer-ready.rbxlx + relay) | live Worker | unchanged | **DONE** |
| **Boat-facing repos** (sensor-bridge, cns-*, sonar-vision, plato-vessel-*, study-fleet-vessel…) | boat `<BOAT_IP>` | CF **only as proxy/auth front** (Tunnel option, consensus OPEN #4); engines stay on the boat | **KEEP-LOCAL + CF edge** |

**Oracle-hosted today (determinable):** only the study-oracle1 vessel runtime + its workspace/vessel repos' compute. Nothing in the public example set was found served from Oracle (rg for oracle/OCI/152.x across READMEs: no hits) — the public demos already point at workers.dev/pages.dev domains.

---

## 2. The clever architecture — one fleet pattern

**"Crab-trap spine": every example is a Worker with shared bindings; D1 is the persistent spine; DOs are live rooms; Queues are the async crew.**

```
                      superinstance.ai (Pages — catalog + front door)
                                     │ links
        ┌────────────────────────────┼────────────────────────────┐
        ▼                            ▼                            ▼
  example Workers (one per demo)   fleet-gateway Worker         Pages sites (static)
  luciddreamer / crab-traps /     (thin router: /go/:example →   playgrounds, dashboards,
  the-tap / elephant-demo /        its Worker; health checks)    archives, radio episodes
  fleet-radio …
        │                                                            ▲
   ┌────┴───────────────────────────────────────────── D1 (spine) ──┘
   │  catches · episodes · posts · lineage · catalog registry · migrations/
   ├─ Durable Objects — the-tap rooms, mud rooms, elephant room-field sim
   ├─ KV — lures (zero-state bundles), sessions, config, feature flags
   ├─ R2 — episode audio, hero art, music assets, build media
   ├─ Vectorize — one index per corpus (writings, reef, quilt, memory)
   ├─ Queues — radio pipeline, creative loops, open-mic turns, image gen
   └─ Cron Triggers — lure breeding (hourly), luciddreamer (30m), radio (22:00 AKDT / Fri 21:00 variety)
```

Rules of the pattern (extracted from what already works):
1. **One Workers project per example, one shared D1 database** (`fleet-spine`) with per-example schema prefixes + migrations dir — D1 survives everything (crab-traps' "can't fail" doctrine).
2. **Never hang, never 502**: proxied fleet calls carry 5s timeout + degrade-to-record (crab-traps' fleet proxy pattern) — this is how boat/WSL2 backends integrate later without coupling.
3. **Vectorize per corpus, not one mega-index** (dimensions differ per embedder); fleet-embed Worker is the only writer.
4. **Queues for anything multi-step** — radio episode = one queue with staged consumers (fetch/score/images/TTS/assemble/deploy); retries free, cron just enqueues.
5. **DO per live room** — the Tap spec is the canonical DO design; reuse its gateway→room-worker→DO shape.
6. **Static stays static** — Pages, no client JS required (luciddreamer doctrine).

---

## 3. Developer-instance story (the stranger test)

Adopt luciddreamer-ai's already-honest convention as the **fleet template standard**:

```
template-repo/
  wrangler.toml            # real names, no secrets
  wrangler.example.toml    # annotated copy with every placeholder named (account_id, namespace ids)
  .dev.vars.example        # BYOK: LLM_API_KEY, optional BOAT_ENDPOINT
  README.md                # "Deploy your own in 3 commands" + honest timeline ("~10 min, not 60 s")
  schema.sql / migrations/ # d1 schema — `wrangler d1 execute --file`
  scripts/bootstrap.sh     # create d1 + vectorize + kv + r2, print ids to paste
  deploy-one.sh            # bootstrap.sh && wrangler deploy
```

- **One command:** `wrangler init my-x --from SuperInstance/<repo>` (quilt-cloudflare already proves this flow) → fill `wrangler.example.toml` → `./deploy-one.sh`.
- **BYOK secrets:** all model keys via `wrangler secret put`; boat endpoints optional (degrade gracefully without them — every example must work standalone).
- **Example catalog:** new `superinstance.ai/#catalog` section + JSON at `/examples.json` (served from a tiny Worker, D1-backed registry: name, blurb, live URL, repo, template flag, one-command deploy string). Every beta-visitor complaint ("where do I try this?") is answered by one page.
- **CI badge honesty** (consensus C1): catalog shows CI-derived test counts only.

---

## 4. Migration sequencing

| Phase | Work | Status |
|---|---|---|
| **0 — Inventory** | this document; registry skeleton (D1 `examples` table) | this doc |
| **1 — Static/Pages (mostly done)** | lucineer-com, activelog, fishinglog, activeledger, ai-writings, superinstance.ai live; ADD: plainsong playground → Pages, tap-frontend, elephant dial-dashboard, example catalog page | **~80% done** |
| **2 — Live Workers (done + finish)** | DONE: lucineer-relay, luciddreamer-ai, crab-trap-funnel, fleet-dashboard. DO: IP scrub (OPEN #4/5), luciddreamer D1 add, ai-writings vectorize | mostly done |
| **3 — Stateful/async build-out** | the-tap DO build (spec ready) → fleet-radio → Queues conversion (nightly + Variety Hour crons off the WSL2 agent-crons onto CF Cron Triggers) → fleet-* microservices → elephant-sim-worker → mud rooms (optional) | next |
| **4 — Data spine & catalog** | shared D1 migrations, fleet-embed writer, examples registry + catalog page, template-repo sweep across the 7 flagship examples | next |
| **5 — Oracle decommission** | move Oracle1 vessel duties: orchestration → the persistent engine (§5) + CF Queues/Cron; vessel/workspace repos → archive branches (A2/A3 doctrine); DNS/takedown last | gated on Captain |

---

## 5. Persistent-engine recommendation — KimiCode

**Verdict: yes — run KimiCode as the one persistent local engine, under systemd, not tmux.**

- **Why KimiCode:** K3's build-intelligence/spatial strength + Med-plan allowance; TOOLS.md already routes spatial/Lua/build work to it. As a persistent engine it gives the fleet a local reasoning endpoint that (a) assists DeepInfra MCP model routing (179 models need a router brain with memory), (b) absorbs subagent work when GLM/DeepSeek are saturated, (c) pre-compiles/validates Lua + build commands destined for the Roblox bridge.
- **Architecture fit:** it is the *only* tier that shouldn't live on CF — CF gives persistence of **state** (D1/KV/DO), not long-lived **processes**. The engine is the boat-side/WSL2 complement: durable state on CF, durable compute at home. Its outputs (validated builds, routed prompts, embeddings) always land in CF stores via the relay Worker — never held only in memory. AGENTS.md critical-path rules apply: systemd + MemoryMax + Restart=always, no tmux-for-production, memory O(chunk).
- **Oracle1's duties** land here (orchestration brain) + Queues/Cron on CF (timing/scheduling).

**Concrete sketch** (`/etc/systemd/system/kimi-engine.service`, per AGENTS.md: long-lived → systemd, Restart=always, MemoryMax, ext4 paths):

```ini
[Unit]
Description=KimiCode persistent engine (fleet build-intelligence + MCP router assist)
After=network-online.target

[Service]
Type=simple
User=eileen
WorkingDirectory=/home/eileen/projects/CognitiveEngine   # engine harness dir (persistent session/log home)
ExecStart=/home/eileen/.npm-global/bin/kimi --serve --port 8788 --mcp
Restart=always
RestartSec=5
MemoryMax=6G
Environment=KIMI_SESSION_DIR=/home/eileen/.local/share/kimi-engine
StandardOutput=append:/home/eileen/.local/state/kimi-engine/log
StandardError=inherit

[Install]
WantedBy=default.target
```

Ops notes: session checkpoints to disk (O(chunk), never O(corpus)); logs under `~/.local/state` on ext4; tmux only for interactive debugging sessions into the same harness; capability manifest consumed by the gateway so DeepInfra routing prompts stay small.

---

## 6. Risks & open questions

**Can't move to CF:** long-running/GPU compute (elephant training, JEPA encoders — keep on WSL2/Jetson); raw TCP/UDP sockets (quicunnel, fleet-conductor TCP — CF only proxies HTTP/WS); egress-heavy scraping; anything needing >128MB Worker memory or CPU >30s (→ split into Queues chunks or local engine); k3s/nomad/elf quilt variants (different platforms by design); boat sensors (physical).

**Needs the Captain:**
1. **Oracle decommission timing** + what must survive from the Oracle1 vessel/workspace repos (archive branches per A2/A3?).
2. **DNS** — custom domains for catalog/examples (superinstance.ai already his); luciddreamer.ai confirmation.
3. **Paid-plan gates** — DOs need paid plan (Workers Paid $5/mo) for the Tap; Queues similarly. Approve or stage Tap behind free-tier fallback.
4. **crab-traps boat endpoint** (OPEN #4/5: hostname vs Tunnel; database_id truth).
5. **Human tasks 1–7 from consensus doc** (PAT, repo rename, push authorizations) — several gate phase 5.
6. **Shared-D1 decision** — one `fleet-spine` vs per-example DBs (cost/blast-radius tradeoff; recommend shared + prefixes, Captain ratifies).

**Open:** whether mud-family goes CF-DO or stays boat-local; Variety Hour cron ownership (agent-cron vs CF Trigger) until pipeline proven (consensus C5).
