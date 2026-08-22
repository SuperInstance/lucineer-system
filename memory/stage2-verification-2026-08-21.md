# Stage-2 Wave-2 Corpus Verification — 2026-08-21

**Verifier:** subagent (read-only pass; no commits, no writes to the repo)
**Repo:** /home/eileen/projects/elephant (origin: git@github.com:SuperInstance/elephant.git)
**Design spec:** STAGE2-CORPUS-DESIGN-2026-08-20.md (= the `dsf-stage2-corpus-design` referenced in memory/2026-08-20.md line 242, "G4 Stage-2: GO")
**Run report:** STAGE2-RUN-2026-08-20.md
**Dissertation repo:** /home/eileen/projects/zeroclaw-dissertation (research/topic.md addendum)

## 1. What's present (all verified on disk)

| Artifact | Status |
|---|---|
| `STAGE2-CORPUS-DESIGN-2026-08-20.md` (17 KB) | untracked, present |
| `STAGE2-RUN-2026-08-20.md` (13 KB) | untracked, present |
| `data/nights/night-T1..T9.jsonl` (9 wave-2 logs, v:2 schema, 20–46 msgs) | present, **gitignored** |
| `data/e2/e2-nights-manifest-w2.json` (9 nights, sha256+stripped_md5, deterministic=true) | present, **gitignored** |
| `data/e2/e2-personas.json` (14 personas: filed 8 bit-identical + new-1..6; `w2_seed` 20260820; archetypes new-1=drifter, new-2=essayist, new-3=writer, new-4=engineer, new-5=engineer, new-6=writer) | tracked, modified |
| `data/slope/stage2-wave-gate.json` (all_pass=true, 53 checks) | present, **gitignored** |
| `data/slope/slope-regression-w2-results.json` (primary −0.3588 [−0.9354, +0.2817], p=0.2682; tripwire fired; verdict INDETERMINATE-leaning-alignment) | present, **gitignored** |
| `data/slope/slope-regression-results.json` (wave-1, sha256 374bcee9…) | present, **gitignored** |
| `SLOPE-REGRESSION-2026-08-20.md` (wave-1 run doc, 7-reader degenerate run) | tracked, modified |
| `scripts/e2_nights.py` (T-tags + §2 ATTENDANCE, append-only generate) | tracked, modified |
| `scripts/e2_personas.py` (NEW_NAMES + new-1..6) | tracked, modified |
| `scripts/e2_instrument.py` (W2_NIGHTS, FIELD_NIGHTS_W2, COLD_ENTRY_W2; PRIMARY_NIGHTS/FIELD_NIGHTS untouched) | tracked, modified |
| `scripts/slope_regression.py` (wave-1 filed machinery; byte-identical through wave-2 work per run doc) | tracked, modified vs HEAD (wave-1 re-run changes) |
| `scripts/slope_regression_w2.py`, `scripts/stage2_wave_gate.py` | untracked, present |
| `research/topic.md` (zeroclaw-dissertation) — dated addendum appended verbatim from design §3 | uncommitted (annotate-only) |

## 2. Design conformance (independently re-checked)

- **Attendance matrix == design §2 for all 9 nights** (21 readers; T1 9, T2 7, T3 7, T4a 6+staged@12, T4b 8+staged@28, T5 10+staged@24, T5c 9+staged@24, T8 7, T9 7). Drifter measured {T2, T4a, T4b} exactly as designed; staged T5/T5c appearances are warmth-content only.
- **x-side:** 15 distinct x, Sxx = 0.1971 (design 0.1971, exact), x-range 0.2535 (design 0.254), band means cold 0.4792 / mid 0.6384 / warm 0.7094 (±0.02 targets). Per-reader x matches the design's a priori table; the 3 tabled typos (new-2 0.5060→0.5066, singer 0.6399→0.6422, new-4 0.6399→0.6379) are exactly the run doc's deviation #2 — registered aggregates unaffected.
- **Room side:** corpus_sd reproduces 0.2367; per-night warmth reproduces the filed ladder to 4 decimals on all 9 (incl. T3 = A family +0.6551 per deviation #1 — the design's own numbers force T3 ∈ {A, S1}; T8 = S3 +0.7409 confirmed).
- **§3.1 preconditions:** 21/21 unique visited sets, ≥3 distinct x, Sxx ≥ 0.19, no archetype majority per band — ALL PASS.
- **§6 guards:** all 21 readers ≥ 3 nights (attrition); ICC 0.9076 [0.7832, 0.9112] > filed 0.7714 [0.667, 0.810] (baseline stability — FM6 does not fire); class-residual tripwire (FM4) fired and handled per design (both slopes reported, no declaration on primary); determinism green.
- **Frozen wave-1 corpus untouched:** night-S*.jsonl, wave-1 manifest, e2-field/ladder results all unchanged in git; wave-1 slope guards reproduce (drift 0.7483, E-cont spread 0.4556, corpus_sd 0.2367).

## 3. Validation runs executed (temp copy /tmp/stage2-verify — repo untouched, zero writes)

All scripts numpy-only, no network calls (grep-verified). Ran in an rsync'd temp copy; outputs compared byte-for-byte with the filed artifacts:

1. `python3 scripts/e2_nights.py --verify` → **9/9 nights reproduce** (stripped_md5 match).
2. `python3 scripts/stage2_wave_gate.py` → **ALL CHECKS PASS**; output byte-identical (sha256 13d0…).
3. `python3 scripts/slope_regression_w2.py` → verdict + all numbers reproduce; output byte-identical (sha256 d253…).
4. `python3 scripts/slope_regression.py` (wave-1) → guards + primary reproduce; output byte-identical (sha256 374bcee9…, matches the run doc's recorded hash).

## 4. Issues / gaps

1. **MAIN LANDING GAP — wave-2 corpus data is gitignored.** `.gitignore` line 3 is `data/`; `git check-ignore` confirms night-T*.jsonl ×9, e2-nights-manifest-w2.json, stage2-wave-gate.json, slope-regression-w2-results.json are all ignored. `git add -n` shows a plain commit stages only the 10 doc/script files and **silently excludes every wave-2 data artifact**. Repo convention force-adds corpus files (wave-1 S-nights, personas, manifest are tracked), so the landing commit needs `git add -f` on the wave-2 data files (or a .gitignore carve-out like `!data/nights/night-T*.jsonl`). Without this, the corpus is not reproducible from the commit.
2. **Minor internal inconsistency in guard re-file:** stage2-wave-gate.json records drift 0.7955 / cont_spread 0.4883 / ICC 0.9061 [0.7809, 0.9109], while slope-regression-w2-results.json (and the run doc §2) file drift 0.8084 / cont_spread 0.4960 / ICC 0.9076 [0.7832, 0.9112]. Both files self-consistent, likely different windowing (gate at generation vs instrument-final); not a correctness issue, but worth a one-line note in the commit message.
3. **Wave-1 re-run changes ride along:** `scripts/slope_regression.py` and `SLOPE-REGRESSION-2026-08-20.md` are modified vs HEAD (the 7-reader degenerate run that grounds the design). The run doc claims slope_regression.py was byte-identical *through* the wave-2 work (true — the diff vs HEAD predates wave-2), but it is uncommitted and would land in the same commit. Decide: co-commit (defensible — it's the design's grounding run) or split.
4. **Class-residual tripwire adjudication pending** (committee item per run doc §6): primary CI contains 0/excludes 1 (alignment-lean), class-residual CI [−0.2408, −0.0376] excludes 0 by a knife-edge (upper −0.038). The run honors the design's letter: INDETERMINATE-leaning-alignment, no declaration. Not a blocker for landing the corpus; the doc states it explicitly.
5. **No `generalization` branch exists** (local or remote) — only `main`, synced with origin (HEAD = origin/main = 1f2a1c5). The encoder-generalization-upgrade commit **2a520e2 is already landed on main** (followed by 5c8a44f, 3af376b). So "the generalization commit ready to land" = already pushed; the pending uncommitted work is the Stage-2 wave-2 corpus + wave-1 slope re-run + dissertation addendum.
6. Dissertation addendum (research/topic.md) is uncommitted by design (annotate-only doctrine) — expected; nothing to fix.

## 5. Verdict

- **Corpus build: CORRECT and fully reproducible.** Design conformance verified on every registered number; all four validation scripts re-run green in a read-only temp copy with byte-identical outputs to the filed artifacts.
- **Ready to land: YES with one required step** — force-add (or carve out of .gitignore) the 12 wave-2 data artifacts so the commit actually contains the corpus; optionally note the gate-vs-results guard-number difference. The tripwire adjudication is a committee decision documented in the run doc, not a landing blocker.
- Nothing was modified during this pass.
