# Ship plainsong 1.5.0 and plainsong-mcp 1.0.1

You are finishing a release that is fully prepared in code but blocked on steps
that need a browser, a PyPI login and repository settings. Everything below has
been verified locally except where it explicitly says otherwise. Work in order —
step 2 must happen before step 3, or the release run will fail.

Two repositories, and note they have **different default branches**:

| Repo | Default branch | PR to merge | Ships |
|---|---|---|---|
| `SuperInstance/plainsong` | `master` | #19 | 1.5.0 |
| `SuperInstance/plainsong-mcp` | `main` | #5 | 1.0.1 |

---

## 1. Merge both pull requests

Merge `SuperInstance/plainsong#19` into `master`, and
`SuperInstance/plainsong-mcp#5` into `main`.

Check CI is green on each **before** merging, and check it by reading the job
list rather than the summary tick. This repository has had a step marked
`success` while its log ended in `##[error]Process completed with exit code 1`,
because the step carried `continue-on-error: true`. If a job's steps include one
that was skipped when you expected it to run, say so rather than merging.

---

## 2. Configure Trusted Publishers on PyPI — do this BEFORE tagging

**This is the actual blocker and has been for the project's entire history.**
There has never been a Trusted Publisher on either project. All six previous
plainsong release runs died at the same step:

```
invalid-publisher: valid token, but no corresponding publisher
environment: MISSING
```

Every version now on PyPI was uploaded by hand. `test` and `build` pass in those
runs, which is what made the failure easy to keep misreading.

For **each** project, go to PyPI → the project → **Publishing** → add a new
publisher (GitHub Actions), and set:

| Field | plainsong | plainsong-mcp |
|---|---|---|
| Owner | `SuperInstance` | `SuperInstance` |
| Repository | `plainsong` | `plainsong-mcp` |
| Workflow name | `release.yml` | `release.yml` |
| Environment | **leave empty** | **leave empty** |

Two traps:

- Use the **project's own** Publishing page, not "add a *pending* publisher".
  The pending-publisher page is for names that do not exist yet and will refuse
  a name already taken. Both of these names are taken.
- `environment: MISSING` in the error message means the field must be **empty**,
  not that it needs a value. Filling it in is a common wrong fix.

`docs/releasing.md` in the plainsong repo has the long version.

---

## 3. Tag and push

Only after step 2. Both release workflows refuse a tag that disagrees with the
version in the tree, so verify before tagging rather than after.

```bash
# plainsong
git checkout master && git pull
grep __version__ plainsong/version.py        # must print 1.5.0
git tag v1.5.0 && git push origin v1.5.0

# plainsong-mcp
git checkout main && git pull
grep '^version' pyproject.toml               # must print 1.0.1
git tag v1.0.1 && git push origin v1.0.1
```

**Tag the commit that carries the bump**, not whatever the branch was when you
started. `v1.2.0` was once created one commit early, on a tree still saying
1.1.0; the workflow guard caught it, but a local build in the same clone quietly
produced 1.1.0 artifacts that PyPI then rejected as duplicates.

If you need to move a tag: a `--depth 1` clone cannot delete and re-push one.
Fetch properly first.

---

## 4. Watch both release runs to completion

Do not stop at "the workflow started". For each run, confirm the job graph
actually completed: `test → build → publish → release`.

**Read the publish step's log even when it is green.** If it says
`skip-existing` skipped the upload, the files were already on PyPI and nothing
new was published — that is a legitimate outcome for a re-run, but it means the
version you think you shipped may not be the one up there.

Known failure modes, in the order they are likely:

1. **`invalid-publisher`** → step 2 was not done, or a field is wrong. Fix the
   publisher and re-run the workflow; the tag does not need recreating.
2. **Tag/version mismatch** → the guard failed in the first job. Delete the tag,
   fix the version, re-tag on the right commit.
3. **`twine check` failure** (plainsong-mcp only) → metadata PyPI would reject.
   The message names the field.
4. **A re-run of an old tag does nothing useful** → a re-run uses the workflow
   file *as it was at that tag*. `v1.0.1`, `v1.1.0` and `v1.2.0` in plainsong
   predate `skip-existing` and cannot be backfilled this way; they authenticate
   and then abort on files already on PyPI. From `v1.3.0` on, a re-run completes.

---

## 5. Verify the published packages from outside

Once both are on PyPI, from a clean directory **outside any checkout**:

```bash
cd /tmp && python3 -m venv v && ./v/bin/pip install -q plainsong==1.5.0
./v/bin/plainsong --version                       # 1.5.0
./v/bin/plainsong spec                            # must pass, and must not say "no specs found"
./v/bin/plainsong new "Ship Check" -o s.song
./v/bin/plainsong compile s.song -o s.mid         # must produce notes, not silence
./v/bin/plainsong info s.song --json              # must be JSON; the flag position matters, see below
```

That fifth command is new in 1.5.0 — flags after the subcommand used to be
refused outright. If it errors with `unrecognized arguments: --json`, the wheel
on PyPI is not the one that was built from this tag.

`plainsong spec` printing `no specs found` and exiting 0 is the specific bug
1.5.0 fixes; if you see that text at all, the packaged data files are missing.

Then, in a plainsong checkout:

```bash
python3 tools/verify_release.py            # tree, wheel AND the live PyPI package
```

It never imports plainsong — it installs the published artifact into a throwaway
venv outside the source tree and drives the console script. Report its final
counts verbatim.

And for the sibling:

```bash
cd /tmp && ./v/bin/pip install -q plainsong-mcp==1.0.1
./v/bin/python -c "import plainsong_mcp; print('ok')"
```

---

## 6. Two things needing repository settings

**GitHub Pages** — I could not reach `https://superinstance.github.io/plainsong/`
from my sandbox (the request returned no status through the proxy), so I do not
know whether it is already live. **Check first, and only act if it is not.**

If it 404s: `SuperInstance/plainsong` → Settings → Pages → Deploy from a branch
→ branch `master`, folder `/docs`. The README links to that URL, and
`docs/index.html` already redirects the Pages root to the browser demo, so this
is the only missing piece.

Confirm afterwards that the URL serves the demo, not a directory listing.

---

## 7. The one check CI cannot run

CI has no browser, so the browser demo is never tested against the compiler
there. From a plainsong checkout, with a browser available:

```bash
python3 tools/demo_differential.py
```

`docs/demo/index.html` carries its own parser, arranger and MIDI writer in
JavaScript so the landing page runs with nothing installed. It is meant to be a
faithful subset. This script compiles the same notation both ways and compares.
Run it and report the result — 1.5.0 did not change the arranger, so it should
pass, and a failure would be a real finding rather than noise.

---

## How to report back

- Give exact command output for anything you verify, not a summary of it.
- If a step was skipped, say it was skipped. A green tick you did not look
  inside is not evidence, and this project has been bitten by exactly that twice
  — a CI step that could not fail, and a `spec` command that called finding
  nothing a pass.
- If something fails, report the failure with its error text and stop rather
  than working around it. A blocked release is fine; a release that looks
  finished and is not, is not.
- Do not re-record, force, or delete anything to make a check pass.
