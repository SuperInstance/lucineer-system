# Org Scout Phase 2 — 2026-08-20

**Scope:** 249 git repos scanned under `/home/eileen/projects/`
**Time:** ~15 minutes

---

## 1. Dead-Branch Carriers (blob/master or tree/master links when default=main)

14 repos with stale `blob/master`/`tree/master` references:

| Repo | Files affected |
|------|---------------|
| forgemaster | docs/GETTING-STARTED.md |
| hermes-construct | 5 files (mlops refs, osint) |
| lucineer-system | deep-dives/plato-fflearning/README.md |
| plainsong-mcp | docs/mcp.md, docs/ensemble.md |
| plato-portal | writing/INDEX.md |
| quilt-rust | target/tmp/go/... (build artifact, ignorable) |
| scummvm-arcade | scummvm-web/SETUP.md, docs/ |
| si-main | README.md, writing/INDEX.md, 2 tutorials |
| si-readme | README.md, THE-FLEET-NOW.md, writing/INDEX.md, 2 tutorials |
| study-flagship | docs/COCAPN-ARCHITECTURE.md |
| study-flux-lucid | README.md |
| superinstance-profile | THE-FLEET-NOW.md, writing/INDEX.md, 2 tutorials |

**Total: ~25 files across 13 real repos** (quilt-rust is build artifacts)

---

## 2. Renamed/Vanished Repo References

Massive — ~90+ repos reference old names. Top offenders in READMEs:

| Old name | Current name | Referenced in (README count) |
|----------|-------------|--------------------------|
| `hermes-perception` | `hermes-avatar` | ~25 repos |
| `the-living-minds` | (dead) | ~18 repos |
| `officers-quarters` | `elephant` | ~15 repos |
| `fleet-wiki` | `lucineer-fleet-wiki` | ~15 repos |
| `tensor-midi` | `fleet-jepa-midi` | ~10 repos |
| `wesley-journal` | (dead) | ~12 repos |
| `forgemaster` | (dead) | ~8 repos |
| `compaction-teacher` | (dead) | ~3 repos |
| `flow-state` | (dead) | ~2 repos |
| `EXOCORTEX` | `exocortex-core` | ~5 repos |
| `lucineer-brain` | `lucineer-system` | ~6 repos |
| `ternary-tenforward` | `confidence-cascade` | ~3 repos |
| `log-tensor` | `murmur` | ~3 repos |
| `mud-arena` | `mud-engine` | ~3 repos |
| `openconstruct-kernel` | `OpenConstruct` | ~3 repos |
| `zeroclaw` | `zeroclaw-dissertation` | ~4 repos |

**Note:** `si-main`, `si-readme`, and `superinstance-profile` are the 3 "profile" variants of the org README — fixing those three fixes ~20 broken links in the org's front door.

---

## 3. Unpushed / Uncommitted Work

| Repo | Branch | Ahead | Dirty files |
|------|--------|-------|-------------|
| ai-writings | master | **1,462 commits** | 1 file dirty |
| fleet-dashboard | main | 20 commits | — |
| luciddreamer-ai | master | 65 commits | — |
| zeroclaw | master | 12 commits | — |
| fleet-radio | — | — | 1 file dirty |
| si-readme | — | — | 1 file dirty |

**⚠️ ai-writings is 1,462 commits ahead of origin/master — likely a branch sync issue or massive unpushed work.**

---

## 4. Missing README

**1 repo:** `ideation-games/`

---

## 5. Top 5 Cross-Pollination Gold

1. **superinstance-profile/** (106 fleet links) — the polished org profile; every link should be canonical
2. **si-readme/** (99 links) — org README variant; near-identical to si-main
3. **si-main/** (92 links) — org README variant
4. **tapscript-studio/** (51 links) + **platos-shell/** (38 links) — rich fleet architecture docs with the most detailed cross-repo wiring descriptions
5. **cns-bridge/** (26 links) — the fleet's "spine" repo with the best narrative about how repos connect

---

## 6. Verdict

- **Highest-leverage fix: mass sed rename across all 90+ repos.** A single script doing `hermes-perception→hermes-avatar`, `the-living-minds→lucineer-system` (or mark dead), `officers-quarters→elephant`, `fleet-wiki→lucineer-fleet-wiki`, `tensor-midi→fleet-jepa-midi`, `wesley-journal→` (dead, remove link), `forgemaster→` (dead), etc. would fix hundreds of broken links in one pass.
- **ai-writings is 1,462 commits ahead of origin** — investigate whether this is a stale `master` vs `main` mismatch or genuinely unpushed work.
- **si-main/si-readme/superinstance-profile are 3 copies of the org README** — pick one canonical, delete or redirect the others, then fix that one.
- **Dead-branch refs are concentrated in 4 repos** (si-main, si-readme, superinstance-profile, scummvm-arcade) — trivial sed `s|/master/|/main/|g` fix.
- **Only 1 repo missing a README** — fleet hygiene is good on this front.
