# Audit Round 9 — tap-frontend

Repo: SuperInstance/tap-frontend · default branch: **master** (verified via `git symbolic-ref refs/remotes/origin/HEAD`) · Audit date: 2026-09-03 · Commit: **6f609d7**

## 1. Link check (~25 links)

- All README relative/external links resolved via curl/gh api: the-tap, platos-shell, scummvm-prototype, elephant, spatial-registry, fleet-radio, fleet-envelope, cns-bridge, dual-band-guard, collective-unconscious, confidence-cascade, vibe-protocol, lucineer-fleet-wiki — all 200.
- `AI-Writings/tree/main/prose` → 200 (already uses the post-move prose/ path — the-tap's round-5 root→prose/ breakage class does **not** occur here; this README was already correct).
- `pages.cloudflare.com` → 200.
- **Two links 404 for anonymous visitors but are live PRIVATE repos** (verified via `gh api`, not deleted): `mud-engine` (private, pushed 2026-08-21), `wesley-journal` (private, pushed 2026-08-21). Not dead — noted as "(private repo)" in README rather than treated as broken. No dead deploy badge here (README has no badge; the-tap's round-5 badge issue class absent).

## 2. Claims verified by re-run / recount

- **Tests re-run:** `npm test` → **121/121 pass** (1 suite). Fresh verification-by-rerun, not reading old output.
- **8-second glow pulse:** `index.html:65` — `animation: glow-pulse 8s ease-in-out infinite` ✓
- **Palette hex codes** (#d4a24c, #0a0908, #ffd700, #f5f0e8, #e8d5a0, #4a4a4a): all present as CSS vars ✓
- **Rooms** bar-rail / galley / wheelhouse / radio: present in code (radio only as icon map entry — minor, not a claim) ✓
- **Bearer auth via `character.api_key`:** `index.html:982` `'Authorization': 'Bearer ' + character.api_key` ✓
- **"Fleet Wiki — 700+ pages":** GitHub wiki (not repo tree) shows **762 pages** ✓ — claim holds (repo tree itself only has ~20 files; pages live in the wiki).
- **STALE — "the-tap … 1313 files":** the-tap @ master (01a01de, post-round-5) has **170 git-tracked files / 205 tree entries**. Checked the-tap's full history — file count never reached 1313 at any commit (max 170). Claim unreproducible → corrected with dated note.
- **STALE — `/api/tide` endpoint row:** the backend gateway (`the-tap/workers/tap-gateway/src/index.ts`) has no `/api/tide`; it exposes `/api/tide-cycle` (mod-key gated). And the frontend **never calls a tide endpoint** — `loadTideBadge()` infers tide from conversation stats ("last voice · N voices · N lines"). Fixed table with dated note.
- **STALE — wesley-journal "(dead)":** repo exists and is private, not dead (pushed 2026-08-21). Corrected to "(private repo, active as of 2026-08-21 — not deleted)".
- CI: `.github/workflows/ci.yml` exists in-tree, targets main+master, runs jest ✓ (no dead CI refs).

## 3. Cross-pollination applied

- **Honest-boundary booking** (lucineer-system r1 / quilt-verilog r3 style): all three corrections are dated 2026-09-03 notes alongside corrected text; no history rewritten, no deletions.
- **Verification-by-rerun** (r3/r6/r7/r8 discipline): tests re-run, counts recounted, backend endpoints cross-checked in the-tap source, wiki page count checked live.
- Checked the-tap r5 findings (AI-Writings prose/ move, dead badge, LIVING-HISTORY owner) for the same classes — none present here.

## 4. Result

Commit **6f609d7** pushed to master (ff, no force). 3 stale claims fixed + 1 private-repo label added; everything else verified clean.
