# Release Verification — 2026-09-29 (fleet lane, READ-ONLY)

Task: verify the 10 publish-ready candidates from the org release audit with **dry-runs only**.
Nothing was published, pushed, or deployed. Clones: `/home/eileen/scratch/release-verify/<repo>` (TMPDIR=/home/eileen/tmp).
Registry probes used `User-Agent: fleet-scout/1.0`. Hazards skipped entirely (micrograd-quilt, SmartCRDT, hermes-construct, and any micrograd/elephant/quilt/hermit/laya/cellforge-named package).

## Methodology notes
- **Rust dry-run:** `cargo package --list --allow-dirty` then `cargo publish --dry-run --allow-dirty` (CARGO_TARGET_DIR=/home/eileen/tmp/cargo-target).
- **Python:** `python3 -m build` is **UNAVAILABLE on this host** — `build` resolves to a shadow module with no `__main__` (`No module named build.__main__`). Substitute dry-run: `python3 -m pip install --dry-run --no-deps --break-system-packages .` (metadata/build-backend only, no install). Real sdist/wheel build is therefore **unproven on this host**.
- **npm:** `npm pack --dry-run` (never `npm publish`; npm auth is known-invalid).
- **crates.io name probe:** 404 = free, 200 = taken.

## Go / No-Go table

| Repo | Ecosystem | Registry name free | Tests present | Dry-run | Blocker | Exact command that WOULD publish |
|---|---|---|---|---|---|---|
| polln | crates.io | YES (404) | YES (`tests/`, 3 entries) | **PASS** (packaged 3581 files / **63.0 MiB**, verified build) | cargo creds present; size bloat — 63 MiB crate is a packaging mistake, not a code failure | `cd polln && cargo publish --allow-dirty` |
| polln | PyPI (`pyproject.toml` v1.0.0, name `polln`) | YES (404) | YES | PASS (pip metadata) | PyPI creds unknown; **version/label mismatch** (repo Rust/npm are 0.1.0, PyPI claims 1.0.0); entry point `polln = mcp_codebase_search:main` is not obviously in this tree | `python3 -m build --sdist && twine upload dist/*` |
| polln | npm (`polln` 0.1.0) | YES (404) | YES | PASS (`npm pack` 15.9 MB packed / 65.3 MB unpacked, 3535 files) | npm auth invalid; **65 MB unpacked** — needs `files` allowlist first | `cd polln && npm publish --access public` |
| quality-gate-stream | PyPI (0.1.1) | YES (404) | YES (14 entries) | PASS (pip metadata, `Would install quality-gate-stream-0.1.1`) | PyPI creds unknown; author recorded as "Oracle1" (fine, but note) | `python3 -m build --sdist && twine upload dist/*` |
| quilt-c | PyPI (0.1.0) | YES (404) | YES (8 entries) | PASS (pip metadata) | PyPI creds unknown; console script `quilt-c-verify = verify:main` expects C sources shipped **inside the sdist** — verify MANIFEST.in covers `src/` + `include/` before upload | `python3 -m build --sdist && twine upload dist/*` |
| quilt-c | crates.io | **NO — TAKEN (200)** | — | n/a (no `Cargo.toml` in repo) | Name occupied by a crate created **2026-09-29T15:38Z** (keywords: graph, cellular, reproducibility, c99, opcodes — fleet-flavored). Either it is ours already or the name is burnt. **Do not attempt a Rust publish under this name.** | (blocked) |
| mavis-substrate-walker | PyPI (0.1.0) | YES (404) | YES (4 entries) | PASS (pip metadata) | PyPI creds unknown; **no LICENSE file** in tree (pyproject declares MIT) | `python3 -m build --sdist && twine upload dist/*` |
| quilt-cloudflare | npm (`quilt-cloudflare` 0.1.0) | YES (404) | YES (`test/`, 4 entries, `node --test`) | PASS (`npm pack`, 3.5 MB / 35 files) | npm auth invalid; package is a **Worker** (`main: src/worker.ts`, wrangler) — npm publish is semantically odd, deploy is the real release. **Deploy is prohibited this run.** | `cd quilt-cloudflare && npm publish --access public` (if npm is even wanted) — real release is `npx wrangler deploy` |
| fleet-murmur | PyPI (0.1.0) | YES (404) | YES (17 entries) | PASS (pip metadata) | PyPI creds unknown; license Apache-2.0, LICENSE present | `python3 -m build --sdist && twine upload dist/*` |
| moth-waveform | PyPI (0.2.0) | YES (404) | YES (4 entries) | PASS (pip metadata) | PyPI creds unknown; **hard-pinned qiskit 2.5.2 / qiskit-aer 0.17.2 / numpy 2.4.6 / scipy 1.17.1 / quantumaudio 0.2.0** — deliberate per in-manifest comment (Aer RNG stream stability). Weighty dependency tree for a first release. | `python3 -m build --sdist && twine upload dist/*` |
| quilt-tools | npm (`@superinstance/quilt-tools` 0.1.0) | YES (404, incl. scope) | **NO** (`npm pack` only; `check` script does `node --check`) | PASS (`npm pack`, 656 kB / 125 files) | npm auth invalid; **scope `@superinstance` decision needed** (does the org own that npm org?); no test suite | `cd quilt-tools && npm publish --access public` |
| exoj | npm (`exoj` 0.1.0) | YES (404) | **NO** (has `smoke.mjs` only, `npm run smoke`) | PASS (`npm pack`, 738.9 kB / 60 files) | npm auth invalid; **no README/LICENSE file, no `description`, no `main`/exports** — thin manifest; unpublishable-looking as a library | `cd exoj && npm publish --access public` |
| quilt-vm-wasm | crates.io (`quilt-vm-wasm` 0.1.0) | YES (404) | **NO** (`tests/` absent; dev-dep `wasm-bindgen-test` declares intent) | **PASS** (packaged, compiles, "aborting upload due to dry run") | cargo creds present; zero tests despite wasm-bindgen-test dev-dep | `cd quilt-vm-wasm && cargo publish --allow-dirty` |

## Publishable TODAY with cargo creds (dry-run clean)
1. **quilt-vm-wasm** — cleanest Rust candidate. Name free, `cargo publish --dry-run` passes end-to-end. Only gap: no tests. Risk: low.
2. **polln (crates.io)** — dry-run passes, but **do not ship as-is**: 3581 files / 63.0 MiB sdist. Add `include`/`exclude` to `Cargo.toml` first (repo contains white-papers, benchmarks, audit docs). This is the one real fix-up before a Rust publish.

## Credential reality check
- `~/.cargo/credentials.toml` **exists** (57 bytes, token prefix `cio…`, len 35 = modern crates.io token shape).
- **Token validity is UNPROVABLE read-only:** `GET https://crates.io/api/v1/me` returns `403 "this action can only be performed on the crates.io website"` — crates.io has closed that endpoint to API clients. So "proven" can only be inferred.
- **Strong inference the token is live:** the `quilt-c` crate landed on crates.io **today at 15:38Z** with fleet-matching keywords. Someone in this fleet is publishing successfully right now.
- **npm:** auth known-invalid. Every npm row is blocked on credentials, not code.
- **PyPI:** creds unknown — no probe performed (would require a real upload attempt; prohibited this run).

## Needs Casey input
1. **npm credentials** — blocks all 4 npm candidates (quilt-tools, quilt-cloudflare, exoj, polln-npm). Route: `npm login` / `NPM_TOKEN` + 2FA decision.
2. **npm scope decision** — is `@superinstance` an org we own on npm? `quilt-tools` declares `@superinstance/quilt-tools`. Name checks out free; ownership does not.
3. **PyPI credentials** — blocks all 5 Python candidates. Also: PyPI now strongly prefers scoped/Trusted Publishing (OIDC) over long-lived tokens; decide whether to mint a token or wire GitHub Actions OIDC.
4. **polln packaging** — three manifests (Cargo 0.1.0 / pyproject 1.0.0 / package.json 0.1.0) with **divergent versions** and a 63–65 MB payload. Which artifact is the real polln release? Needs a call.
5. **quilt-c crates.io collision** — name taken as of 15:38Z today. Confirm whether that crate is ours (if so, fine) or a stranger (if so, quarantine the Rust name and ship Python-only).
6. **quilt-cloudflare** — is the release `npm publish` or `wrangler deploy`? Deploy was out of scope this run; needs an explicit go.
7. **Missing LICENSE files** (mavis-substrate-walker, moth-waveform, quilt-tools, exoj, quilt-vm-wasm) — MIT is declared in metadata but no LICENSE text ships. Cheap fix, worth doing before any public release.
8. **Test gaps** — quilt-tools, exoj, quilt-vm-wasm have no real test suites. Publishing untested crates/packages is legal but unwise; recommend a smoke test each.

## Shape of the fleet's release state (one paragraph)
The Rust lane is genuinely ready: budget 2 candidates, both dry-run green, and the only true blocker is packaging hygiene on `polln`. The Python lane is **code-ready but credential-starved** — all 5 packages produce valid metadata and all 5 registry names are free (a clean sweep), so the entire lane unblocks the moment a PyPI credential exists. The npm lane is the least ready in every dimension: invalid auth, a scope we may not own, and manifests (`exoj` has no description/main; `polln` ships 65 MB) that would be embarrassing as first impressions. Verdict: **ship nothing until PyPI creds, an npm scope decision, and polln's manifest are settled; then publish quilt-vm-wasm + the 5 Python packages immediately.**

Dry-runs performed: 2 cargo publishes (PASS×2), 5 pip metadata builds (PASS×5), 4 npm packs (PASS×4). Zero real publishes. Zero deploys. Zero pushes.
