# Org README Canonicalization — Proposal (2026-08-20)

Three local repos all carry the SuperInstance org-profile README and all
point at the same remote: `github.com/SuperInstance/SuperInstance` (the
special org-profile repo). Nothing here has been deleted or renamed —
this is a proposal only.

## The three variants

| Repo | Last commit | Lines | Links | Live? |
|---|---|---|---|---|
| `si-main` | 2026-08-14 (`0044d23`) | 414 | 111 | no — stale clone |
| `si-readme` | 2026-08-18 (`15aacd0`) | 540 | 119 | no — stale clone |
| `superinstance-profile` | 2026-08-20 (`5d31a35`) | 553 | 126 | **yes — matches `origin/main`** |

`git ls-remote` confirms the live `origin/main` is `5d31a35`, exactly
`superinstance-profile`'s HEAD. The other two are older local clones
whose tracking refs were never updated, so their "in sync" status is an
illusion.

## What each has that the others lack

- **si-main** (oldest): nothing unique. It is a strict ancestor in
  content — older stats badges (200 repos / 6,500+ corpus), no imagery
  header, no "Reef Grows a Room", no "Plainsong", and its links still
  use `blob/master` paths and pre-rename repo names
  (`hermes-perception`, `officers-quarters`, `lucineer-brain`,
  `tensor-midi`, `log-tensor`, `monologue-pro`) that the Aug 20
  dead-link surgery fixed. Its last commit (Compass Head Radio Hour
  additions) is fully contained in both later variants.
- **si-readme** (middle): added the imagery header (the flagship's
  seven + the debug-duck porthole image), "The Reef Grows a Room"
  section, and "Plainsong — The Jukebox Takes Requests". All of this is
  also present in superinstance-profile. It still carries the
  pre-surgery dead links and mid stats (500+ repos / 6,500+ corpus).
- **superinstance-profile** (newest, live): everything in si-readme,
  plus the Aug 20 dead-link surgery (0 remaining `blob/master` refs;
  AI-Writings master→main and `prose/` moves; mud-engine package
  renames to `agent-runtime`/`envelope`/`core`/`channels`/`event-bus`;
  `hermes-perception`→`hermes-avatar`, `officers-quarters`→
  `elephant`/`fleet-yaw`, `openconstruct-*`→`OpenConstruct`,
  `lucineer-brain`→`lucineer-system`, `ternary-tenforward`→
  `confidence-cascade`, `log-tensor`→`murmur`, `tensor-midi`→
  `fleet-jepa-midi`, `monologue-pro`→`drunk-02-pro`), refreshed stats
  (1,000+ repos, 946 public, 6,000+ tests, 8,800+ corpus pieces), the
  13-wings Map pointer, and a new "The Best of the Wall" section.
  Caveat: the surgery introduced two malformed doubled URLs —
  `https://github.com/SuperInstance/https://github.com/SuperInstance/casting-call`
  (in the Crab and the Shell "models" link) and the same pattern for
  `elephant` (in the Tile and the Deadband "fisherman learns" link).
  Those two should be fixed in the canonical copy before or right after
  collapsing.

## Recommendation

Collapse to **superinstance-profile as the single canonical working
copy**: it is the freshest, it is a strict content superset of the
other two, it carries the dead-link surgery, and — decisively — it is
already the commit live on `origin/main`, so choosing it changes
nothing the world sees. Fix the two doubled-URL links there first.
Then retire the other two *in place, no deletions*: rename the local
directories to `si-main-archive-20260814` and `si-readme-archive-20260818`
(or drop an `ARCHIVED.md` pointer file at each root saying "canonical
org README lives in ../superinstance-profile"), and leave their git
history untouched. If the captain wants belt-and-suspenders, tag each
archived clone's HEAD (`org-readme-pre-canonical`) before renaming so
any future archaeology is one `git log` away. From then on, all org
README edits happen in superinstance-profile only — one door, one sign.
