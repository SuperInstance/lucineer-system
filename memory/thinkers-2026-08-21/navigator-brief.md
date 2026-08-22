# NAVIGATOR — Strategy Position Brief: The Held Pile & Open Decisions

**Date:** 2026-08-21 (Friday) · **Panel:** SuperInstance decision panel · **Doctrine applied:** (a) newer ideas usually win; (b) ideas are preserved, not deleted (archive-by-rename, never destroy)
**Evidence base:** /tmp/pr-states.jsonl (237 PRs, 111 merged, 126 held), /tmp/merge-results.log, repo-gaps-2026-08-21.md, beta-visitors-2026-08-21/*, phase3-roadmap-2026-08-20.md, direct git inspection of plainsong-worker / tapscript-worker / si-*.archived clones / luciddreamer-ai. Read-only; no repo modified.

---

## 0. Headline finding — the held pile is NOT on the iceberg's critical path

I ran the held 126 against the iceberg map (The Tap → the boat, Wesley toward the wheelhouse, the elephant as temperature sense, fleet radio, skills-compiled-once). Result: **the iceberg organs are already green.** The Tap / crab-traps / the-tap / tap-frontend — zero held PRs. Wesley — zero. elephant — zero (corpus 666459e landed this morning; stage-2 verified). fleet-radio — zero (variety decision is separate, §6). The boat's marine-gpu-edge PRs merged clean.

The held pile decomposes as: **84 dependabot** (65 of them MAJOR) + **42 fleet-authored**, and the fleet-authored mass is (i) ~18 `fix(ci): remove failure masking` one-liners on fleet-body and study repos, (ii) ~13 older-edge-family PRs now conflicting *because newer PRs already won* on those repos, (iii) a dozen one-offs. This is shipkeeping, not shipbuilding.

**Strategic call:** run the held pile with the mechanical agents (merge-fixwave, unstable-triage) in parallel and let the iceberg roadmap (phase-3 items: unconscious P1, Wesley's Ollama return, sea-legs demo) proceed today. Never gate a phase-3 item on quilt-swarm's eslint version.

---

## 1. Priority order for the UNSTABLE pile (103 red-CI)

**P0 — tonight, zero effort:** quilt-jetson #1/#3 (the BLOCKED workflow-scope pair). Captain fixed the OAuth scope — re-attempt both merges immediately; clears the whole BLOCKED class and finishes the jetson set.

**P1 — iceberg organs (the fleet's nervous system):**
1. **fleet-gateway#1** (masking fix) — gateway is *live deployed*, got the gallery push overnight (581102d); a live organ with lying CI is canary risk. Fix first, alone if needed.
2. **The fleet body-plan batch:** fleet-config, fleet-discovery, fleet-containers, fleet-bottles, fleet-github-app, fleet-homunculus, fleet-constraint, fleet-agent-early-version, fleet-stitch, fleet-scribe, fleet-coordinate-js — all the same masking-fix shape. Batch them in one runner wave. **Newer-idea move:** where the repo is Python, migrate to the fleet shared python-ci workflow (the sunset-ecosystem#33 pattern, matching agent-operations#3's merged CI/CD strategy) instead of patching 11 bespoke YAMLs — fix the masking *once, centrally*.
3. **quilt-rust's 4 dependabot** (incl. thiserror 1→2) — this is the golden-vector/edge-ledger contract repo (G3). It's the reference other projects cite; it must be green *first* so the contract stays authoritative. Rust deps are low-risk to absorb.
4. **sunset-ecosystem #33 + #32** — #33 (migrate to shared CI) is the newer idea; merge it FIRST, then rebase #32 (resolve all test failures) on top. If #32's fixes are absorbed by the migration, close-as-superseded with a pointer. Do not merge them in the listed order.

**P2 — conflict chains (newer PRs already won):** edge-compiler#1, nexus-edge-runtime#1, holodeck-c#1, edge-relay-agent#1/#3, flux-cross-assembler#1/#2, fleet-midi#2, fleet-conductor#1, edge-native-paper#1/#2, codespace-edge-rd#1. Each of these repos has 2–4 *newer* PRs already merged on top. Doctrine (a) is unambiguous: the merged newer architecture is canonical. For each old PR: **diff against current main, fold any unique fix forward into a fresh small PR, then close-as-superseded** with a comment recording what was folded. Do NOT rebase two-generations-old work over three newer merged waves — that resurrects legacy behavior the org already voted against.

**P3 — the quilt-grid dependency wave (47 dependabot PRs):** quilt-swarm (12), quilt-fleet (6), quilt-pincher (5), quilt-rag (5), quilt-k3s (3), quilt-elf (3), quilt-nomad (2), quilt-cloudflare/evolve/ai (1 each), plus quicunnel (3, incl. the critical rustls/quinn build fix #8 — do that one FIRST, it's a real breakage not a bump) and flux-runtime (2). **Key mechanism note:** merge all *GitHub-Actions* bumps (setup-python 5→7, upload-artifact 4→7, cache 5→6) first, org-wide — deprecated actions are plausibly *causing* a chunk of the red-CI pile, so these merges are medicine, not churn. Then run the TS/eslint 8→10 / vitest 1→4 / typescript 5.9→7 family bump as ONE coordinated wave (one crew, one day, same versions everywhere) — 12 staggered quilt-swarm PRs will conflict pairwise forever; that's why they're held. The grid is the first-person-ledger zoom of the iceberg's same-edge-at-three-zooms — it matters, but as a *family green*, not repo-by-repo dribble.

**P4 — ballast & study (fix last, or absorb cheaply):** PersonalLog (11), SmartCRDT (10), polln (10), CognitiveEngine (5), webgpu-profiler (8 + #66, which is a real fake-green CI fix — pull it forward out of this tier), SuperInstance-papers (2), forgemaster#6, bplus-tree#1 (README-only), vessel-room-navigator#1 (loading bug — small real fix, do it), plato-engine-block-c#2, adinkra/adaptive-plato/actualization-harbor/activelog-*/active-probe/ability-transfer masking one-liners. Head-behind pair (constraint-theory-py#1, plato-types#1): update branch + re-merge — pure mechanics for the fixwave agent. None of this tier advances the iceberg this week; it advances *credibility*, which the beta visitors just told us is our weakest hull plate.

**Explicit noise list:** quilt-swarm's eslint/ts dev-dep majors on un-deployed scaffolding, SmartCRDT/polln/CognitiveEngine majors, PersonalLog dev-deps. Green-keep them cheaply; don't engineer them.

---

## 2. Dependabot major bumps — merge-and-absorb vs close, per repo class

- **Contract/live repos (quilt-rust, quilt-jetson, flux-runtime, fabric-mcp, quicunnel, SuperInstance-papers):** MERGE-AND-ABSORB. Newer versions are the newer idea; the repo's job is to stay a trustworthy reference. Absorb actions bumps instantly, library majors after one green CI run.
- **Active TS family (quilt-swarm, quilt-fleet, quilt-pincher, quilt-rag, quilt-k3s, quilt-elf, quilt-nomad):** MERGE, but only as the single coordinated family wave (§1 P3). Never as staggered independent PRs — they are mechanically mutually conflicting.
- **Study / experimental / early-version (SmartCRDT, polln, CognitiveEngine, webgpu-profiler, *-early-version, adaptive-plato, study-tier):** CLOSE majors that require code migration, with a dated comment ("superseded — repo scaffolds fresh on current versions when next touched"); absorb minors/patches in one batch. Closing an upgrade *offer* destroys no idea — the offer is regenerable on demand; the doctrine protects ideas, not inboxes. When the repo is next genuinely touched, scaffold on current versions (newer ideas win).
- **PersonalLog:** absorb ONCE as a single lockfile+CI batch, then set dependabot ignore rules for majors. It's the ship's log — a journal, not a product; it should be green and boring forever.
- **Org-wide standing rule I'd codify:** actions/* bumps always merge (CI health); runtime deps absorb on active repos, close-with-comment on study repos; dev-dep majors follow the family-wave cadence, monthly at most.

---

## 3. The archived clones (si-main.archived-20260820, si-readme.archived-20260820)

**Recommendation: push as archive branches to SuperInstance/SuperInstance, then fold unique ideas into the canonical — do NOT create new repos, do NOT leave local-only.**

Verified state: both are stale clones of the org repo carrying *unique commits not guaranteed anywhere else* — the de-IP pass (5391b28 / 1aa9eb2: replaced raw boat IP 147.224.38.131 with `<BOAT_IP>`), org-wide link repair (5dd3d27 / 33f3363), plus their own front-door imagery/sections (Compass Head Radio Hour in si-main; flagship-seven imagery in si-readme). The canonical front door is now superinstance-profile (pushed, live, 466bd42).

- **Why archive branches, not archived repos:** we spent yesterday collapsing three org front doors into one; minting two new public repos re-clutters the gangplank the beta visitors just told us is our credibility bottleneck. Branches preserve every byte in the cloud, discoverable, zero front-page cost: `archive/si-main-20260820`, `archive/si-readme-20260820`.
- **Why not local-only:** one disk failure from losing the de-IP and imagery work. Preservation means in the cloud.
- **Mandatory follow-through:** diff each archive branch against superinstance-profile; fold anything unique (especially the de-IP pass — confirm the canonical profile carries it; and the Compass Head Radio Hour section if still wanted) into the canonical with attribution. Ideas preserved AND live — that's the doctrine's second half.

---

## 4. plainsong vs tapscript-studio dedupe

**Canonical: plainsong. Full stop.** Evidence: the PyPI package *is* `plainsong` (v1.4.0); org-wide links already point at plainsong; the repo-gaps scan rates plainsong P2-clean vs tapscript-studio P1-stale (H1 literally says `# Plainsong`, badge points at the plainsong PyPI, embedded chart hotlinks the plainsong repo); and the musician beta visitor independently verdicted tapscript-studio "identity crisis — Plainsong in disguise… as a repo it's a trap."

**Sequence (archive, never delete):**
1. Diff tapscript-studio → plainsong; fold any unique delta (chiefly the in-repo `docs/img/creatures-of-interval.svg`, so the README stops hotlinking the old raw.githubusercontent path) into plainsong.
2. Rename the GitHub repo `tapscript-studio` → `tapscript-studio-archived` (GitHub auto-redirects old links — the address keeps working, so nothing that points here rots). Tombstone the README head: "This project is now **Plainsong** → link. The notation dialect formerly here is called TapScript; its live compiler is plainsong-worker."
3. Rename the local dir `tapscript-studio.archived-20260821`.
4. **Keep the name "TapScript" alive as the *dialect*** — plainsong-worker parses TapScript notation; that's where the term earns its keep. Say the naming once, in both READMEs, exactly as the musician visitor prescribed: *Plainsong* = the project; *TapScript* = the notation it eats. (Also closes the repo-gaps P1 stale-branding item for free.)

Newer idea wins: Plainsong is the newer name and the newer branding; TapScript-the-repo retires with honors and a redirect.

---

## 5. tapscript-worker hero commit 96d669a

**Verified fact that changes the default answer: 96d669a exists ONLY locally.** The remote (plainsong-worker.git) history does *not* contain it — the rename lineage carries a *different* hero commit (5651164, a 149,658-byte image) where tapscript-worker's 96d669a added a **213,932-byte** hero (md5 73c2c6de ≠ 5cbfc70d). Same idea, two different assets; the bigger original exists nowhere in the cloud.

**Recommendation: preserve, don't recreate, don't orphan.**
1. Push 96d669a to the remote as `archive/tapscript-worker-hero-96d669a` (one push, permanent preservation, zero repo sprawl). **Do NOT recreate a tapscript-worker repo** — that resurrects a retired name against doctrine (a).
2. Rename the local dir to `tapscript-worker.archived-20260821` per archive-by-rename.
3. One-line Captain's choice, not a panel item: which hero image *displays* on plainsong-worker's README — the live 149KB one or the original 213KB one? Either way the other stays in history. I'd keep the current one (it shipped with the rename; newer wins) unless the Captain wants the original art back.

---

## 6. Sweep push (elephant page → luciddreamer.ai) & variety-show cron (Friday 21:00)

**Sweep push: GO. Now.** d74a5b2 (The Elephant in the Room feature page) sits under two already-stacked commits (58159ba hero+gallery — which wires the 20 orphaned image files the repo-gaps scan flagged; 24d815c honest Quick Start) — pushing ships a coherent, visitor-hardened set. This is the iceberg *directly*: the elephant is the fleet's temperature sense and luciddreamer.ai is the autonomous-publisher flagship; a public /elephant/ page is the first time the temperature sense has a face a stranger can see. The beta visitors' loudest complaint about luciddreamer-ai was "20 images, none wired" — 58159ba answers it. Nothing is held behind it except the repo being 65+ commits ahead; every day unpushed is drift risk. (Standing note: confirm the front-door "500+ repositories" and test-count claims get their sanity pass on the *deployed* site after push — the statistician flagged them.)

**Variety-show cron: GO for tonight's episode, HOLD the automation until proven.** It's Friday; the slot is real; the pilot script already exists in full (fleet-radio-variety-pilot-2026-08-21.md — complete rundown, cold open through sign-off, real numbers from the logs). But the sibling tap-improv cron failed last night with an exec error, and the variety cron shares pipeline DNA. A first episode born at 21:05 as a stack trace poisons the format's debut; a newer idea deserves a clean berth.
- **If** the tap-improv exec bug is fixed and verified by ~20:30: enable the cron, let it run.
- **Else:** ship the existing pilot manually tonight (it's written!), enable the cron only after one observed clean cycle, aim the automation at episode 2.
The Variety Hour is the newer framing of fleet radio (arranged truth > generated filler — its own cold open says so); it should win the slot — the question is only *which pipe* delivers episode 1.

---

## 7. Where the doctrine points on the held pile overall

- **Newer ideas usually win, applied:** the merged production-hardening/honesty wave is the newest idea in the org's history — every held PR that *extends* it (masking fixes, fact-checks, shared-CI migration) should land; every held PR that *predates and conflicts with* it (the old edge-family #1s) should be folded-forward and closed-as-superseded, not reborn. Dependabot's newest versions win *on active repos*; on study repos the newest idea is the repo's own retirement to a clean scaffold, so majors close there. Plainsong wins the name; TapScript survives as the dialect. The 21:00 Variety Hour wins the Friday slot over the older daily-only format.
- **Ideas preserved, applied:** archived clones → cloud archive branches + fold-through to canonical. tapscript-studio → renamed-with-redirect + tombstone, unique SVG folded into plainsong. 96d669a → archive branch before the local dir is renamed away. Closed dependabot majors → dated comments recording why (the idea of the upgrade is preserved in writing; the diff is regenerable). The quilt family's legacy versions → the family-wave commit itself is the historical record.
- **The one place I'd police the doctrine:** "newer wins" must never become "delete the older." Every close-as-superseded needs its fold-forward or its written epitaph. I'd ask the panel to treat a close-without-comment as a doctrine violation worth flagging.

---

## 8. Where I want the panel's disagreement

1. **Close-as-superseded vs full rebase for the old conflict PRs.** A Historian instinct will want the old PRs' full diffs preserved as merged history. My position: fold unique fixes forward + epitaph comment preserves the *ideas* without resurrecting superseded architecture — but this is the panel's call because it sets precedent for every future conflict wave.
2. **Green-first vs migrate-first on CI.** I split it (green-first for live organs like fleet-gateway; migrate-to-shared-CI-first for the rest). An Ops position could argue green-first everywhere is safer today and migration is a project, not a triage. Legitimate; I'd hold my line only for gateway.
3. **Archive branches vs a proper archive repo for si-main/si-readme.** If the Captain wants the org's archaeology *visible* (the "gold preserved for later study" instinct), one public `SuperInstance/archive` repo with branch-per-era might serve better than buried branches on the org repo. I chose low-clutter; the advocate may choose low-obscurity. Panel should pick.
4. **PersonalLog dependency policy.** I recommend absorb-once-then-ignore. If anyone argues the log repo should be frozen read-only instead (no deps churn at all), I'd hear it — freezing is also doctrine-clean.
5. **The 213KB vs 149KB hero** — deferred to the Captain, but if a panelist feels strongly about original art, now's the moment.

**Bottom line:** Re-merge jetson tonight (P0), fix fleet-gateway and the fleet body-plan this weekend (P1), let the fixwave eat the conflicts as fold-forward-closes (P2), run one coordinated quilt dependency day (P3), batch the ballast (P4) — and in parallel, GO the sweep push, GO the Variety Hour pilot (manual if the cron isn't proven), and let the iceberg sail. The held pile never touches the bow.

— Navigator, 2026-08-21
