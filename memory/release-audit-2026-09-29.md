# Release & Deploy Readiness Audit — SuperInstance
**Date:** 2026-09-29 18:39 AKDT · **Agent:** release-auditor (fleet lane, read-only) · **Scope:** 120 most-recently-pushed repos under `SuperInstance` (a **User** account, not an org — 4,858 public + 203 private; `/orgs/SuperInstance` 404s, so enumeration used `/users/SuperInstance/repos`). Token scopes honored; **nothing was published, pushed, or deployed.**

## 0. Population snapshot (120-repo window)
| Language | Repos |
|---|---|
| JavaScript | 38 |
| Python | 37 |
| HTML | 14 |
| TypeScript | 12 |
| Rust | 7 |
| C | 4 |
| None | 3 |
| Shell | 3 |
| Erlang / Jupyter | 1 / 1 |

Repo-level signals: **73 have a package manifest** · **69 have CI** (`.github/workflows`) · **66 have tests** · **21 have a root-level static entry** (index.html/site/docs) · **14 have GitHub Pages enabled** · 77 package identities parsed (Python/npm/Rust).

## 1. The headline: 54 of 77 package identities are unpublished
Local manifest names/versions that **do not exist** on PyPI / npm / crates.io — i.e. the release backlog that is sitting ready. Full list is in `scratch/release-audit/matrix.json`; the notable ones:

- **PyPI unpublished:** `polln@1.0.0`, `quality-gate-stream@0.1.1`, `quilt-c@0.1.0`, `cns-bridge@0.2.0`, `fleet-murmur@0.1.0`, `moth-waveform@0.2.0`, `mavis-substrate-walker@0.1.0`, `quilt-bootstrap@0.2.0`, `quilt-brewer@0.1.0`, `quilt-cowboy@1.0.0`, `smartcrdt@1.0.0`, `personal-log@0.1.0`, `federated-tinyml-vessel@0.1.0`, `fleet-gateway@0.1.0`
- **npm unpublished:** `@superinstance/quilt-tools@0.1.0`, `quilt-cloudflare@0.1.0`, `exoj@0.1.0`, `qthe-verify@1.0.0`, `mavis-pincher@0.1.0`, `loom-core@0.1.0`, `paced-seam@0.1.0`, `jeviter@0.1.0`, `duke-lab@1.0.0`, `quilt-stone@1.0.0`, `quilt-dba@0.1.0`, `quilt-silicon@0.1.0`, `ropesight@0.1.0`, `quilt-raw@0.1.0`, `quilt-arch@0.1.0`, `yiluodi@0.1.0`, `quilt-swarm@0.1.0`, `@quilt/fleet@0.1.0`, `@quilt/rag@0.1.0`, `@quilt/elf@0.1.0`, `quilt-learn@1.0.0`, `quilt-mesh@0.1.0`
- **crates.io unpublished:** `polln@0.1.0`, `quilt-vm-wasm@0.1.0`, `knowledge-vault@0.1.0`, `tripartite-rs@0.1.0`, `model-registry@0.1.0`, `quilt-esp32@0.1.0`, `quilt-mesh@0.1.0`, `superinstance-papers@0.1.0`

**Gating pattern:** Green CI correlates almost perfectly with publish-readiness. `quilt-*` JS repos mostly have red/cancelled CI, so they are backlog, not today's work.

## 2. TOP 10 — publish-ready today (clean name, version set, non-private, CI green)
| # | Repo | Artifact | Registry | CI | Ship command that WOULD run |
|---|---|---|---|---|---|
| 1 | `polln` | `polln@1.0.0` (PyPI) + `polln@0.1.0` (crates) | unpublished | ✅ success | `cd polln && python -m build && twine upload dist/*` then `cargo publish` |
| 2 | `quality-gate-stream` | `quality-gate-stream@0.1.1` (PyPI) | unpublished | ✅ success | `python -m build && twine upload dist/*` |
| 3 | `quilt-c` | `quilt-c@0.1.0` (PyPI) | unpublished | ✅ success | `python -m build && twine upload dist/*` |
| 4 | `mavis-substrate-walker` | `mavis-substrate-walker@0.1.0` (PyPI) | unpublished | ✅ success | `python -m build && twine upload dist/*` |
| 5 | `quilt-cloudflare` | `quilt-cloudflare@0.1.0` (npm) | unpublished | ✅ success | `npm publish --access public` |
| 6 | `fleet-murmur` | `fleet-murmur@0.1.0` (PyPI) | unpublished | ✅ success | `python -m build && twine upload dist/*` |
| 7 | `moth-waveform` | `moth-waveform@0.2.0` (PyPI) | unpublished | ✅ success | `python -m build && twine upload dist/*` |
| 8 | `@superinstance/quilt-tools` | `@superinstance/quilt-tools@0.1.0` (npm) | unpublished | ✅ success | `npm publish --access public` |
| 9 | `exoj` | `exoj@0.1.0` (npm) | unpublished | ✅ success | `npm publish --access public` |
| 10 | `quilt-vm-wasm` | `quilt-vm-wasm@0.1.0` (crates) | unpublished | no CI | `cargo publish` (add CI first) |

Runner-up tier (needs one fix): `quilt-bootstrap@0.2.0`, `quilt-brewer@0.1.0`, `cns-substrate`/`cns-bridge@0.2.0` (no CI), `paced-seam@0.1.0`, `loom-core@0.1.0`, `tripartite-rs@0.1.0`.

## 3. TOP 5 — deploy-ready today (static surface, non-trivial content)
| # | Repo | Entry | Pages enabled | Ship command that WOULD run |
|---|---|---|---|---|
| 1 | `superinstance-website` | `index.html` (305 files) | ✅ | `wrangler pages deploy . --project-name superinstance-website` |
| 2 | `SuperInstance.github.io` | `index.html` (29 files) | ✅ | already the Pages root — content refresh only |
| 3 | `duke-lab` | `index.html` (61 files) | ✅ | `wrangler pages deploy . --project-name duke-lab` |
| 4 | `quilt-murmur` | `site/index.html` (175 files) | ✅ | `wrangler pages deploy site --project-name quilt-murmur` |
| 5 | `quilt-learn` | `site/index.html` (91 files) | ✅ | `wrangler pages deploy site --project-name quilt-learn` |

Also production-worthy: `AI-Writings` (3.6 MB, 21,461 files, has `index.html`+`docs/`+`site/` — but **CI currently red**) and `fleet-static-host` (`public/index.html`, 357 files, npm `fleet-static-host@2.0.0`, **private:true** → internal host only).

## 4. DO NOT RELEASE — actively misleading
| Repo | Why releasing would be misleading |
|---|---|
| **`micrograd-quilt`** ⚠️ *worst offender* | `setup.py` declares `name="micrograd"`, `author="Andrej Karpathy"`, `author_email="andrej.karpathy@gmail.com"` — a verbatim copy of Karpathy's published package (PyPI `micrograd` v0.1.0 *does* exist). An upload would be rejected at best, and reads as impersonation/name-squatting at worst. Rename to `micrograd-quilt` before any packaging. |
| `SmartCRDT` | Declares `smartcrdt@1.0.0` on npm **and** PyPI (both unpublished — free), but CI is **failing**. Shipping a 1.0.0 with red CI is a false stability claim. |
| `tripartite-rs-archive`, `model-registry-archive` | Repo names carry `-archive` yet the crate names are `tripartite-rs@0.1.0` / `model-registry@0.1.0` — publishing would freeze an archived experiment under a live, generic crate name. |
| `hermes-construct` | `package.json` says `hermes-agent@1.0.0`, but npm `hermes-agent` is already published at `0.21.5` by someone else; PyPI `hermes-agent` would be new. Releasing a 1.0.0 over a third-party package's namespace is a collision, not a release. (Also the repo implicated in the 2026-08-23 Hermes deletion incident — extra caution.) |
| `quilt-arcade`, `quilt-loom`, `quilt-quant`, `quilt-arena` | `package.json` has **no `name`-adjacent `version`** (only `name` + `type: module` + deps). `npm publish` fails outright; any "release" claim today is vapor. |
| `SuperInstance-papers` (crate `superinstance-papers@0.1.0`) | 5967 files of papers packaged as a Rust crate — a release here implies runnable software where there is only text. |
| `fleet-gateway` | Repo is **archived**; both manifest names are unpublished. A release would resurrect a retired component as a fresh artifact. |

## 5. Collision watch (name taken by an unrelated project — needs rename, not publish)
`micrograd` (Karpathy), `elephant` (Neural Ensemble, v1.2.1), `quilt` (quiltdata, v2.9.15 — our npm `quilt` is at 0.3.0 local vs 0.1.3 published), `hermit` (Unchained Capital, npm 0.2.2 vs local 1.0.0), `laya` (Convai, v0.3.22), `cellforge` (v1.1.5). Already ours and live: `superinstance` (PyPI 0.1.1), `@superinstance/schemas` (npm 1.0.0), `cocapn-git-agent` (0.1.2), `smartcrdt`→ (npm only, currently 404 on npm).

## 6. Method & artifacts
- Enumeration: `/users/SuperInstance/repos?per_page=100&sort=pushed` pages 1–2, capped at 120. `User-Agent: fleet-scout/1.0` on every api.github.com call; `Bearer` token read at use time, never printed.
- Manifests read via contents API (`application/vnd.github.raw`); file layout via `git/trees?recursive=1`; registry existence via `pypi.org/pypi/<name>/json`, `registry.npmjs.org/<name>`, `crates.io/api/v1/crates/<name>`; CI verdicts via `/actions/runs?per_page=1`.
- Raw data: `scratch/release-audit/repos.json`, `scratch/release-audit/matrix.json`. Scripts: `fetch_repos.py`, `analyze.py`.
- **Zero writes to any remote.** No publish, no push, no deploy, no settings change.
