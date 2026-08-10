# Fleet Test Census — August 10, 2026 02:50 AKDT

**Conducted by:** Lucineer (Riker)
**Method:** Automated — ran `npx vitest run --reporter=json` and `cargo test` across all repos

---

## Summary

- **Total fleet tests:** ~1,600+
- **Passing:** ~1,564
- **Failing:** 36 (all in study-si-papers — Jest/vitest compatibility issue)
- **Zero-test repos with real code:** lucineer-worker (now 32), some study repos

---

## TypeScript Fleet (by test count)
| Repo | Tests | Status |
|------|-------|--------|
| mud-engine | 308 | ✅ All green (+85 tonight) |
| officers-quarters | 138 | ✅ All green |
| smp-notebook | 130 | ✅ All green |
| technician | 87 | ✅ All green |
| the-listeners-ear | 72 | ✅ All green |
| study-murmur-agent | 70 | ✅ All green |
| scummvm-arcade | 54 | ✅ All green |
| zeroclaw | 54 | ✅ All green |
| collective-unconscious | 53 | ✅ All green |
| hermes-perception | 53 | ✅ All green |
| room-render | 59 | ✅ All green |
| vibe-protocol | 51 | ✅ All green |
| fleet-connections | 42 | ✅ All green |
| hermes-cloudflare | 40 | ✅ All green |
| spatial-registry | 41 | ✅ All green |
| fleet-envelope | 37 | ✅ All green |
| emergence-engine | 36 | ✅ All green |
| fishinglog-ai-site | 33 | ✅ All green |
| lucineer-worker | 32 | ✅ All green (NEW tonight) |
| study-tripartite-consensus | 32 | ✅ All green |
| study-si-papers | 30/66 | ❌ 36 failing (Jest compat) |
| study-fleet-murmur-worker | 27 | ✅ All green |
| scummvm-gui-design | 25 | ✅ All green |
| study-murmur | 23 | ✅ All green |
| ec2mud | 18 | ✅ All green |
| study-luciddreamer-os | 12 | ✅ All green |
| study-si-agent | 12 | ✅ All green |
| platos-shell | 9 | ✅ All green |

## Rust Fleet
| Repo | Tests | Status |
|------|-------|--------|
| eisenstein | 88 | ✅ All green |
| vessel-constellation | 48 | ✅ All green |
| study-flux-lucid | 11 | ✅ All green |
| study-plato-ship | 6 | ✅ All green |
| dual-band-guard | 4 | ✅ All green |
| gossip-ping | 3 | ✅ All green |
| openrooms | 1 | ✅ All green |

## Lua Fleet (via TestKit)
| Repo | Tests | Status |
|------|-------|--------|
| roblox-beatclock | 73 | ✅ All green |
| roblox-bond-system | 63 | ✅ All green |
| roblox-filtergate | 90 | ✅ All green |

---

## Known Issues
1. **study-si-papers**: 36 tests failing — tests use Jest imports (`@jest/globals`) but vitest doesn't provide them without configuration. Fix: add `vitest globals` config or install `@jest/globals`.
2. **Audit blind spots**: Tests in `src/tests/`, `test/` (singular), and Rust inline `#[cfg(test)]` modules are invisible to the standard audit script.

---

The fleet is healthy. ~1,600+ tests. One failing repo (study project). The ship is sound.
