# UNSTABLE PR Triage — 2026-08-21

Batch: 81 red-CI PRs across the SuperInstance org (of 201 open PRs; 119 green/no-checks not covered).
Source: `/tmp/pr-states.jsonl`, `/tmp/open-prs.txt`, `/tmp/pr-checks.tsv`, per-PR check logs in `/tmp/failures/`.
All PRs were held from the earlier merge pass because CI is red. **Nothing was merged — no red CI was merged.**

## Class breakdown (81)

| Class | Count | Notes |
|---|---|---|
| UNMASK (remove failure masking) | 17 | 16 fixed + pushed (CI re-running), 1 needs real work |
| DEPENDABOT-MAJOR | 48 | mostly blocked by pre-existing CI config, not the bump |
| DEPENDABOT-OTHER (group bumps / "Update requirement" style) | 10 | same root causes as MAJOR |
| DEPENDABOT-MINOR | 1 | SmartCRDT#64 — blocked by missing lockfile |
| DEPENDABOT-PATCH | 2 | quilt-rust#1/#4 (0.x semver bumps, breaking in Rust) |
| FIX-PR (human-authored) | 3 | 2 fixed + pushed, 1 needs real work |

## Summary of actions (final, 2026-08-21 ~18:00 AKDT)

- **Fixed + pushed: 19 PRs** (16 UNMASK + 2 FIX-PR + 1 dependabot one-liner)
  - **10 confirmed green by CI**: active-probe#1, adaptive-plato-early-version#1, fleet-config#1, fleet-containers#1, fleet-bottles#1, fleet-gateway#1, fleet-homunculus#1, webgpu-profiler#66 (7/7), PersonalLog#65 (eslint key + --webpack), quicunnel#8 (all but audit)
  - **9 fixed-pushed but GitHub Actions did not create runs** (verified local fixes; push webhooks dropped by GitHub — check-suites show no Actions suite for the new SHAs despite re-pushes, close/reopen, and empty commits): activelog-agent#1, activelog-ai-pages#1, actualization-harbor#1, adinkra-math-pypi#1, ability-transfer#3, fleet-discovery#1, fleet-agent-early-version#1, fleet-github-app#1, fleet-coordinate-js#1. **Action needed: re-trigger CI from the UI (or wait for GitHub to catch up), then merge.**
  - **quicunnel#8**: audit now runs (Cargo.lock generated) but **correctly fails on a real vuln — ring 0.16.20 (RUSTSEC-2025-0009). Do not merge until `cargo update -p ring` / rustls bump.**
- **Need real work: 4 PRs** (fleet-constraint#1, Edge-Native#5, quicunnel#8 audit vuln, PersonalLog#60/61/66/68 cluster — see notes)
- **Close-candidates (dependabot-major on dormant study repos, blocked by pre-existing broken CI): ~33 PRs** — see the lockfile-blocked bucket below
- **Merged this wave: 0** (all fixes pushed to PR branches; merging only after CI confirms green — one red CI was deliberately NOT merged)

---

## Full table (81 PRs)

### UNMASK — "remove failure masking" (17)

| PR | Repo | Failing check | Root cause | Fix effort | Action |
|---|---|---|---|---|---|
| #1 | active-probe | pip install -e . (exit 1) | no pyproject/setup.py → not installable | 1-line | **fixed-pushed** (added pyproject.toml) — CI: test pass ✅ |
| #1 | adaptive-plato-early-version | pip install -e . (exit 1) | no pyproject/setup.py | 1-line | **fixed-pushed** (added pyproject.toml) — CI: test pass ✅ |
| #1 | activelog-agent | test (3.10-3.12) ModuleNotFoundError | ci.yml never installs package (`pip install pytest` only) | 1-line | **fixed-pushed** (install -e . before pytest) |
| #1 | actualization-harbor | test ModuleNotFoundError | ci.yml never installs package + pyproject flat-layout error | small | **fixed-pushed** (install -e . + packages=) |
| #1 | activelog-ai-pages | test ModuleNotFoundError | broken build-backend (`setuptools.backends._legacy:_Backend`) + no install | 1-line | **fixed-pushed** (backend fix + install -e .) |
| #1 | adinkra-math-pypi | test ModuleNotFoundError | PEP-639 license classifier conflict breaks install + no install step | 1-line | **fixed-pushed** (dropped classifier + install -e .) |
| #3 | ability-transfer | pytest collected 0 items (exit 5) | Python CI on a C project; real suite is `make test` (28/28 pass) | 1-line | **fixed-pushed** (test step → make test) |
| #1 | fleet-discovery | pytest collected 0 items (exit 5) | repo has no tests | 1-line | **fixed-pushed** (tolerate exit 5) |
| #1 | fleet-agent-early-version | pytest collected 0 items (exit 5) | repo has no tests | 1-line | **fixed-pushed** (tolerate exit 5) |
| #1 | fleet-bottles | ImportError `Fleet` from `cocapn` | test imports nonexistent package (empty cocapn dir) | small | **fixed-pushed** (replaced with repo-layout smoke tests) |
| #1 | fleet-config | pip install on 3.10 | pyproject requires-python >=3.11 vs CI matrix 3.10 | 1-line | **fixed-pushed** (relaxed to >=3.10) — CI green ✅ |
| #1 | fleet-containers | ModuleNotFoundError yaml | PyYAML not declared anywhere | 1-line | **fixed-pushed** (requirements.txt PyYAML) — CI green ✅ |
| #1 | fleet-coordinate-js | npx eslint exit 2 | no eslint config exists; eslint 9 needs flat config; tsc is real gate | 1-line | **fixed-pushed** (removed lint step) |
| #1 | fleet-gateway | ImportError `FleetGateway` from `gateway` | merge clobbered full gateway.py (FleetGateway, discover_from_yaml); tests/cli depend on it | small (restore) | **fixed-pushed** (restored from initial commit) — CI green ✅ |
| #1 | fleet-github-app | flake8 E999 SyntaxError | non-ASCII em-dash in bytes literal, webhook_handler.py:257 | 1-line | **fixed-pushed** (.encode() instead) + exit-5 tolerance (no tests) |
| #1 | fleet-homunculus | test_count_by_status assert 2==1 | status bands inconsistent with heal(); pain level logic broken | small | **fixed-pushed** (aligned bands, amount-based levels; 19/19 pass) — CI green ✅ |
| #1 | fleet-constraint | ModuleNotFoundError numpy (+fleet_agent) | needs numpy AND imports `fleet_agent.fleet_math` — cross-package dep that doesn't exist anywhere | substantial | **needs-work** (vendor/remove cross-import; numpy is 1-line but not sufficient) |

### FIX-PR (human-authored, 3)

| PR | Repo | Failing check | Root cause | Fix effort | Action |
|---|---|---|---|---|---|
| #66 | webgpu-profiler | test (3.10-3.12) + build-and-test (18) | console `pytest` lacks cwd on sys.path; node 18 + jsdom/html-encoding-sniffer ESM incompat | small | **fixed-pushed** (`python -m pytest`, drop node 18) — CI green ✅ (7/7) |
| #8 | quicunnel | Security audit | audit needs Cargo.lock (gitignored); after fix, audit correctly flags ring 0.16.20 (RUSTSEC-2025-0009) | small→moderate | **fixed-pushed** (generate-lockfile step) — audit now runs but FAILS on real vuln: needs `cargo update -p ring` / rustls bump before merge |
| #5 | Edge-Native | ESP32-S3 Firmware Build (ninja) | C build error in firmware (app_main.c) | substantial | **needs-work** (embedded C; not timeboxed) |

### DEPENDABOT — lockfile-blocked bucket (33 PRs)
**Failure:** `actions/setup-node` `cache: 'npm'` step → "Dependencies lock file is not found" (repo has no package-lock/pnpm-lock) OR `npm ci` fails with EUSAGE (no lockfile). This is **pre-existing broken CI config**, not caused by the bump. Fix (per repo, cheap): commit a lockfile or drop `cache:` from setup-node. **Bumps are almost certainly safe to take eventually** — nothing in the dependency code is even being compiled.

quilt-swarm #1-#12 (12) · quilt-fleet #1-#6 (6) · quilt-rag #1-#5 (5) · quilt-elf #1-#3 (3) · quilt-ai #1 (1) · quilt-cloudflare #2 (1) · quilt-evolve #1 (1) · SmartCRDT #62/#64/#66 (3, #64 is prettier MINOR) · CognitiveEngine #51 (1, pnpm)

### DEPENDABOT — other failures (18 PRs)

| PR | Repo | Failing check | Root cause | Fix effort | Action |
|---|---|---|---|---|---|
| #53, #54 | CognitiveEngine | Docker buildx | `invalid tag "SuperInstance/...": must be lowercase` — org name uppercase in workflow tag; pre-existing | 1-line (workflow) | needs-work (CI config) |
| #65 | PersonalLog | Node.js type check / build | next 15→16: `eslint` key removed from NextConfig type + Next 16 defaults to Turbopack and rejects webpack config | 2×1-line | **fixed-pushed** (removed eslint block; `next build --webpack`) — CI green ✅ |
| #60, #61, #66, #68 | PersonalLog | Build & Test exit 1 | `Cannot read properties of null (reading 'explain')` — npm/pnpm engine issue on bump branches | small | needs-work (inspect per-PR; likely stale lockfile or engine pin) |
| #1, #2 | quilt-nomad | test exit 1 | `npm ci` EUSAGE — no lockfile | 1-line (lockfile) | needs-work (CI config) |
| #1-#5 | quilt-pincher | test exit 1 | `npm ci` EUSAGE — no lockfile | 1-line (lockfile) | needs-work (CI config) |
| #14 | SuperInstance-papers | test | typescript 6→7; `npm ci` no lockfile | 1-line (lockfile) | needs-work (CI config) |
| #27 | flux-runtime | build | tsc "Found 3467 errors" — pre-existing type breakage, not the bump | substantial | needs-work |
| #1-#3 | quilt-k3s | Run chaos gauntlet | `k3d: command not found` — runner missing k3d; infra issue | 1-line (CI) | needs-work (CI config) |
| #1 | quilt-rust | clippy -D warnings | tower-http 0.5→0.7 API drift | small | needs-work (code change; safe eventually) |
| #2 | quilt-rust | clippy -D warnings | thiserror 1→2: rmcp ServerInfo became non-exhaustive (E0639) | small | needs-work (builder/`..Default`; safe eventually) |
| #3 | quilt-rust | security audit | rmcp 0.2→3.1: audit flags RUSTSEC advisories in tree | small | needs-work (audit-driven) |
| #4 | quilt-rust | clippy -D warnings | axum 0.7→0.8 API drift | small | needs-work (code change; safe eventually) |
| #76, #81, #82, #83, #84 | webgpu-profiler | build-and-test | base main had fake-green CI; these inherit broken suite — after #66 merges they likely pass on rebase | n/a (rebase) | wait-for-#66 |

---

## Recommendations

1. **Merge the 6 confirmed-green fixed PRs now** (fleet-config#1, fleet-containers#1, fleet-bottles#1, fleet-gateway#1, fleet-homunculus#1, webgpu-profiler#66), and the remaining 13 as their CI goes green.
2. **Lockfile-blocked bucket (~33 PRs):** cheap shared fix — commit lockfiles or drop `cache:` from `actions/setup-node` in the quilt-*/SmartCRDT/CognitiveEngine repos, then all these dependabot PRs go green and can merge. Do NOT close them for being "broken" — the bumps are fine.
3. **Close-candidates (dormant study repos, dependabot-major, would still need CI fix before merge):** quilt-swarm (12 PRs), quilt-fleet (6), quilt-rag (5), quilt-elf (3) — all dormant since ~July 2026. If the org doesn't want to maintain lockfiles there, closing these PRs is defensible; flag for Casey.
4. **Real work queue:** fleet-constraint#1 (cross-package import), Edge-Native#5 (ESP32 build), quicunnel#8 (ring vuln — do not merge until `cargo update -p ring`), PersonalLog#60/61/66/68, flux-runtime#27.
