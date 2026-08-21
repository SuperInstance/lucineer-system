# Post-Sweep Verification Checklist — kimi org-wide link repair (2026-08-20)

Context: kimi's org-wide sweep (~90 repos) repairs links broken by repo renames.
Commits land **LOCALLY ONLY — NO PUSH** until the Captain approves. This is the
checklist for when the sweep lands.

---

## 0. Preflight — confirm the sweep actually landed, unpushed

```bash
# For a sample of repos (or a manifest if kimi logged one):
cd <repo>
git log --oneline -3          # sweep commit should be HEAD
git status -sb                # expect: ## main...origin/main [ahead N]
```
- `[ahead N]` = commits are local-only = **correct**. `[behind]` or no marker =
  something got pushed or rebased — flag it.
- If kimi left a manifest/log of repos touched, verify count (~90) and that every
  listed repo has a HEAD commit matching the sweep convention
  (e.g. `fix: link repair` / `chore: rename references`).

## 1. Per-repo commit verification

```bash
git show --stat HEAD          # files touched — docs only?
git show HEAD --name-only
```
- **Allowed:** `README.md`, `*.md`, `docs/**`, link/path references.
- **Red flag:** `.lua`/`.luau`, `.ts`, `.py`, `.rs`, `.toml`, `.json`, `.env*`,
  `.rbxlx`, lockfiles — source/config files should be untouched by a link sweep.
- Commit message should match the sweep convention (no `Merge`, no giant blob).
- Do this on **all repos that touch code** + a random sample of the rest
  (every 10th repo minimum).

## 2. Spot catastrophic matches (renames leaking into code identifiers)

The catastrophic failure mode: the rename regex matched the repo name **inside
code identifiers**, not just URLs/link text — e.g. `mud_arena` → `mud_engine` in
variable names, `OfficersQuarters` in class names, `EXOCORTEX` in env var names.

```bash
git show HEAD | grep '^[-+]' | grep -v '^[-+][-+]'   # changed lines only
# then hunt for identifier-context replacements:
git show HEAD | grep -iE 'perception|officers|fleet_wiki|tensor_midi|mud_arena|zeroclaw|exocortex'
```
- Look for changes where the old name is embedded in a **word** (snake_case,
  camelCase, SCREAMING_CASE) rather than a URL path or prose sentence.
- Any change to a non-markdown file = STOP, flag, that repo does not ship.
- Spot-check ≥10 diffs, weighted toward code-heavy repos.

## 3. Known-good target mapping — spot-check these

Old name should be **gone from link context**; new repo must **resolve**.

| Old | New | Check |
|---|---|---|
| hermes-perception | hermes-avatar | grep old → 0 or prose-only |
| officers-quarters | elephant | grep old → 0 or prose-only |
| fleet-wiki | lucineer-fleet-wiki | grep old → 0 or prose-only |
| tensor-midi | fleet-jepa-midi | grep old → 0 or prose-only |
| mud-arena | mud-engine | grep old → 0 or prose-only |
| zeroclaw | zeroclaw-dissertation | grep old → 0 or prose-only |
| EXOCORTEX | exocortex-core | grep old → 0 or prose-only |

```bash
for r in <repo>; do grep -rn 'hermes-perception\|officers-quarters\|fleet-wiki\|tensor-midi\|mud-arena\|zeroclaw\|EXOCORTEX' --include='*.md' "$r" | head; done
# resolve the new repos:
curl -s -o /dev/null -w '%{http_code}\n' https://github.com/SuperInstance/hermes-avatar   # expect 200
git ls-remote https://github.com/SuperInstance/elephant HEAD                               # expect a sha
```
- `curl`/`ls-remote` each of the 7 new names once → all must resolve (200 / sha).
- Old names may remain in prose ("formerly hermes-perception") — that's fine;
  old names inside `](...)` link targets are not.

## 4. superinstance-profile URL-fix queue — FIRST fix after the sweep

File: `/home/eileen/projects/superinstance-profile/README.md`
Malformed pattern: `https://github.com/SuperInstance/https://github.com/SuperInstance/<target>`
→ fix to `https://github.com/SuperInstance/<target>`

**Verified: 9 malformed URLs across 8 lines** (not the 5 previously known):

| Line | Target (after fix) | Occurrences |
|---|---|---|
| 58 | `casting-call` | 1 |
| 135 | `elephant` | 1 |
| 143 | `elephant` | 1 |
| 166 | `fleet-yaw` | 1 |
| 168 | `fleet-yaw` | 1 |
| **170** | **`fleet-yaw` AND `elephant`** — **two links on one line, easy to miss** | 2 |
| 238 | `casting-call` | 1 |
| 312 | `mud-engine/blob/main/docs/TOWFISH-SUBMARINE.md` | 1 |

Mechanical fix (one-liner, then eyeball):
```bash
sed -i 's|github.com/SuperInstance/https://github.com/SuperInstance/|github.com/SuperInstance/|g' README.md
grep -c 'SuperInstance/https' README.md   # must be 0 after
```
Additional flag from the same README:
- **L506:** display label `zeroclaw` links to `SuperInstance/zeroclaw` — per the
  mapping that repo is now `zeroclaw-dissertation`, so this href is likely a
  404. Confirm and update href (label is fine as-is or update both).
- L492 `git clone https://github.com/SuperInstance/SuperInstance.git` is the
  org-profile repo itself — **legit, leave it**.
- L506/510/511 use old display labels (hermes-perception, officers-quarters,
  log-tensor, tensor-midi) with already-corrected hrefs — cosmetic only,
  optional follow-up, not blocking.

## 5. Ship gate — 5 items the Captain needs before approving the wide push

1. **Catastrophic-match audit clean** — no source/config files changed in any
   swept repo; sampled diffs (≥10 repos) show no renames inside code
   identifiers.
2. **Known-good mapping resolves** — all 7 new repo names return 200/sha via
   curl or ls-remote; old names absent from link targets in sampled repos.
3. **No repo left broken** — every swept repo is clean apart from its sweep
   commit; no doubled URLs, no bare old repo names, READMEs render.
4. **superinstance-profile URL queue fixed** — the 9 malformed URLs (8 lines)
   + L506 zeroclaw href corrected, committed locally.
5. **Push plan explicit** — manifest of repo → sweep commit sha (`git rev-parse
   HEAD` per repo before pushing), push order (docs-first, code-heavy last or
   subset), and rollback path (`git revert <sweep-sha>` per repo if anything
   misbehaves after push).

---

### Knowns / risks carried into the checklist
- Known-5 line count was wrong → 8 lines / **9 URLs** (L170 has two).
- L506 zeroclaw href may already be dead post-rename.
- Sweep may have touched superinstance-profile too — if so, apply the URL queue
  **on top of** the sweep commit so both land in one reviewable commit.
