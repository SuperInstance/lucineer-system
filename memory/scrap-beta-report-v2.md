# SCRAPCRAFT — Regression Rig v2 Report
**Target:** https://fleet-static-host.casey-digennaro.workers.dev/scrap/ (live deploy)
**Date:** 2026-08-23 (AKDT) · **Rig:** headless Chromium 151 (CDP, swiftshader WebGL), synthetic input, no audio, no vision models
**Bundles analyzed:** `assets/index-BOFxm0Qt.js` (607 KB, minified — code-level verification used where observation was impossible)
**Sessions:** 7 browser sessions; localStorage persisted across all restarts

---

## Executive Summary

The merge is **fundamentally healthy**: cold start, splash removal, yard render, mining, Earl's gate, quest spine, NEXT-step verbs, rare-find delight, BrainGallery, challenge rotation, a11y closed-panel hygiene, resize, and freeze/thaw resilience all verified clean with **zero console errors** across every session.

One reproducible hard-freeze blocks all panel-close paths in this harness (6/6) — evidence says environment-specific, but it needs ONE manual headed confirmation before sign-off because the tutorial forces a workshop close. Two a11y/UX issues and a save-semantics question round out the list. No confirmed P0.

---

## P1 — Fix before beta sign-off

### P1-1 · Workshop close hard-freezes the tab (6/6 headless) — needs one headed confirm
**Severity rationale:** If it reproduces with real trusted input, it's a P0 (tutorial requires closing the Workshop). All evidence says headless-only, hence P1 pending manual check.

**Repro (100% deterministic in this rig, 6/6):**
1. Load page → CLOCK IN → dismiss WELCOME BACK.
2. Press `E` → Workshop opens (verified `#inv-panel` display:flex, contents render).
3. Press `E` again (toggle-close) **or** `Escape` → **entire page main thread freezes synchronously.**

**Frozen state characteristics:**
- `Runtime.evaluate` never returns (raw CDP and tool driver both).
- Renderer CPU drops to ~2% (not a spin — a block).
- `Page.reload` is accepted but never executes (navigation deadlocks too).
- Only killing the tab recovers; browser process stays healthy.
- **Zero console output** before/during the freeze.

**Root-cause evidence (code-level):**
- `closeInventory()` ends with the bundle's only **unguarded** `requestPointerLock()`:
  ```js
  closeInventory(){this._overlayOpen=!1,this._overlay.classList.remove("open"),...,
    document.getElementById("game-canvas").requestPointerLock()}
  ```
- Every other call site uses the guarded form: `document.pointerLockElement||X.requestPointerLock()`.
- Patching a guard over `HTMLCanvasElement.prototype.requestPointerLock` (no-op when already locked) did **not** prevent the freeze (session 6) → the deadlock sits in Chromium headless pointer-lock internals, not the game's JS.
- Open paths never freeze (0/6); freeze is exclusively the close path.
- Related: native `prompt()` (Earl F-chat) also freezes all page JS while open — same family of "page blocked, CDP helpless" states in this environment.

**Recommended action:** one manual headed-Chrome pass: open workshop, close with E and ESC ×5. If clean → close as environment artifact (and still apply the P3 guard fix below for hygiene). If it freezes headed → P0, ship-blocker.

---

## P2 — Fix for beta

### P2-1 · Achievement toast rests "visible + empty" from page load (a11y)
**Repro (2/2 fresh sessions):**
1. Hard-load the page (before even pressing CLOCK IN).
2. Inspect `#achieve-toast`: computed `opacity: 1`, `display: block`; `#ach-toast-name` and `#ach-toast-desc` are **empty strings**; positioned offscreen-right (x≈viewport+24px).
3. It stays in this state indefinitely (observed >2 min; still there at session end) until a real achievement populates it (Lucky Strike populated it correctly later).

**Impact:** the element is exposed in the accessibility tree at all times with empty content (screen-reader noise; violates the "closed panels absent from a11y tree" bar the merge set for panels). Visually invisible only because it's parked offscreen.
**Fix shape:** idle state should be `display:none`/`aria-hidden` and only mount/reveal on fire.

### P2-2 · No mid-session save of core progression (hard refresh loses the shift)
**Repro:**
1. Play ~5 min: reach Lv.1 TINKERER, hotbar gains 🔩 Iron Scrap ×2 + ⚙️ Small Gear, iron quest 2/5, Earl gate advanced through "Open the Workshop".
2. Kill browser (or hard refresh) mid-shift → CLOCK IN again.

**Result:** Lv.0, empty hotbar, quest 0/5, Earl gate reset to step 1. Full localStorage dump contains **no player/world save keys at all**.
**What DOES persist (all correct):** delight flags (`scrapcraft_delight_first_lucky_find`), companion memory (Bolt counters: blocksMined 2, rareLoot 1, nudgesFollowed 1; greet_return events), codex/spine/nightshift/onboarding state, companions met/active.
**Action:** if session-scoped yards are intended (the CLOCK IN / "the yard kept your spot" shift metaphor suggests yes), make that explicit to players (e.g., CLOCK OUT saves or a "shift ends on refresh" notice). Otherwise this is data loss.

### P2-3 · Maker Bench: RUN with no deployed bot is a silent no-op (first-hour UX)
**Repro:**
1. `T` → Maker Bench → load "Line Follower" preset via the EXAMPLES `<select>` (workspace populates; dropzone placeholder gone — verified).
2. Click `▶ RUN`.

**Result:** DRIVE/TURN sensors stay `0.0`, BOT SERIAL log stays empty, Daily Contract "Run a bot program for 2 minutes total" stays `0s / 120s`. No toast, no serial message, no hint about the missing prerequisite (built/deployed bot).
**Secondary:** the `⚡ BUILD IT` firmware receipt (`#flash-receipt`) rendered perfectly (A+ grade, generated Arduino firmware) but **both its Close buttons (`✕` and "Close") failed to dismiss it** (remained `display:flex` after 2 clicks + waits) — possibly the same rAF-throttled-transition environment artifact, but worth a headed check.
**Fix shape:** RUN with no bot in the yard should toast "No bot deployed — BUILD IT first" (the NEXT-step HUD already teaches physical verbs; this is the one silent dead-end found).

### P2-4 · Ambient chatter / AmbientLife not observably firing in hour one (verify it talks)
**Observed:** across all sessions: exactly **one** companion line all day (Bolt: "Ok, big moment: press T…" — fired at the workshop gate step, i.e. event-driven), plus greet_return at load. Session 7 soak: **0 unsolicited lines in 4–6 min** mixing active mining and idle, day cycling Morning→Midday. No immediate repeats (trivially — nothing repeated because almost nothing spoke).
**Code-verified (bundle):**
- ChatterGuard exists and matches spec exactly: `minGapS 20, windowS 600, maxUnsolicited 6` with commit/prune of `_unsolicited` timestamps → cap ≤6/10min **by construction**.
- Ambient scheduler exists: `_ambientS += dt` vs `_ambientGap` (base + rng), gated on ChatterGuard.
- AmbientLife: `ambientLife = new fo(...)`, `.tick(dt)` in the main loop; crane `Creak()` audio; yard-cat lines present in companion banks.
**Verdict:** cap compliance ✓ (0 ≤ 6). But "hour-one presence" (yard cat, creaks, ambient lines) could not be confirmed observationally in this harness (no audio; visual-only cues in WebGL; possibly gated on companion bond/first-meet or suppressed while panels open). **Needs a manual 10-min listen/watch pass.**

---

## P3 — Hygiene / notes

- **P3-1** `closeInventory()` unguarded `requestPointerLock()` — inconsistent with the guarded pattern at every other call site; add the `document.pointerLockElement ||` guard regardless of P1-1 outcome (defense against lock-state races for real users too).
- **P3-2** Earl chat via native `prompt()` pauses the entire game loop while open (world/rAF halt). Quirky-by-design and the merge's "Earl prompt fixes" work (`_earlBusy` + `?? ""` seen in code, no-stack verified live), but a custom input row would keep the world alive.
- **P3-3** Harness artifacts (not game bugs): swiftshader deprecation warning + `GPU stall due to ReadPixels` (from screenshot probes); rAF throttled to ~1.5fps in this headless; pointer lock granted on only 2/5 cold boots (when absent, all lock-gated keys correctly no-op with no errors).

---

## Verified PASS (no regression)

| Area | Result | Evidence |
|---|---|---|
| Cold start E2E | ✅ | CLOCK IN click lands instantly (splash removal real — no overlay interception); WebGL yard renders (composited frame 99.7% non-blank, 136 coarse colors @780×437; 99.0% @1100×700); rAF loop running; **0 console errors all day** |
| Movement | ✅ | W-hold → 24.3% pixel delta between screenshots (camera moved) |
| Mining | ✅ | mine-arc progress ring (dashoffset 80.1, opacity 1); iron 0→3/5 across sweeps; hotbar gains items; Earl gate advances on mining. Note: aiming requires pitch above horizon (y=0 ground targets auto-cancel — correct) |
| Earl's gate | ✅ | Full stepwise advance observed: Welcome/WASD → Mine Some Scrap → Open the Workshop → Open the Maker Lab (with "Earl pre-loaded a starter program") |
| Quest HUD / spine | ✅ | SALVAGE RUN + DAILY CONTRACT live and **rotating** between sessions (Collect 3 Small Gears → Run a bot program ≥1 variable); QUESTS log + [L] logbook present |
| NEXT step HUD | ✅ | Physical verbs confirmed: "➜ NEXT: Mine 5 iron scrap (0/5) ↳ hold left-click on the scrap heaps"; "Press W A S D…"; "Press E…"; "Press T…" |
| First-mine rare find + confetti | ✅ | 🍀 **Lucky Strike** achievement fired mid-mining ("Find a hidden rare item buried in scrap…"); code path: notify + `particles.burst(...,"confetti",14)` + `audio.pickup` + `foreman.onEvent("lucky_find")`; delight flag persisted to localStorage |
| First-program delight (partial) | ✅/⚠️ | Bolt's "big moment: press T" nudge fired at the right beat; Maker Bench + presets + firmware BUILD all work; the RUN→2-min-daily leg blocked by P2-3 |
| Level-up | ✅ | Lv.0 → **Lv.1 TINKERER** with title in HUD |
| WELCOME BACK | ✅ | Returning-player panel ("the yard kept your spot") + BACK TO WORK; companion greet_return events recorded |
| BrainGallery | ✅ | Opens from Maker Bench (🧠 GALLERY): community programs list loads over network (entry seen: "Drove straight into the forge wall at full speed… failure · by a yard kid · ⬇1"), categories (Wall Avoiders…Custom), Publish My Brain, LOAD PROGRAM |
| Maker Bench | ✅ | Full VPL: tile palette (MOTION/OUTPUT/TIMING/FLOW/MACROS/VARIABLES/SUBROUTINES), examples, brain tiers (TIN/SPARK/VISION), BOT 1/2, SPARK, SHARE, MODS, BOT, CODE export (Arduino .ino / MicroPython / Wokwi) |
| ClassRoom | ⚠️ present | `classroom-panel` + join prompt (`showJoinPromptIfNeeded()` at boot) + class-code prompt/confirm in code; flows not exercised (prompt-gated → freeze risk in harness). No regression evidence |
| Races / ghosts | ⚠️ present | Race-board panel, lap/ghost counters, "first_autonomous_lap" delight ceremony, "👻 GHOST: BEST LAP" HUD all present in code+HUD; end-to-end lap not exercised (proximity-gated + no pointer lock this session). No regression evidence |
| Challenge rotation | ✅ | Different challenge per session (daily seed) |
| Day/night | ✅ | Morning → Midday → darker scene across sessions (nightshift key persisted) |
| A11y: closed panels | ✅ | codex/pause/help `display:none`; flash-receipt `visibility:hidden`+`opacity:0`; classroom/race-board/tower panels **removed from DOM** when closed (best practice). Exception: P2-1 achieve-toast |
| Chaos: F-mash | ✅ | 10 rapid F keydowns → exactly **1** Earl prompt (no stacking); `_earlBusy` + `!repeat` guards verified live and in code |
| Chaos: rapid C | ⚠️ coverage gap | `KeyC`→`_cycleCompanion()` requires pointerLockElement (granted 2/5 boots). When unlocked: correct silent no-op, no errors. Companions state machine (met/activeId/recruited) persisted correctly |
| Chaos: resize | ✅ | 780×437 → 1100×700: canvas + HUD reflow, scene re-renders (99% non-blank), no errors |
| Chaos: tab-switch / freeze | ✅ | `Page.setWebLifecycleState: frozen` 2.5s mid-mining-macro → resumed clean, macro completed, page responsive, no errors |
| Chaos: hard refresh save | ✅/⚠️ | Meta-progression survives (see P2-2 for what doesn't) |
| Console | ✅ | **Zero errors** across 7 sessions (only swiftshader warnings from harness probes) |

---

## Test-env caveats
- Headless CDP + swiftshader software WebGL; rAF throttled ~1.5fps (frame-accurate gameplay timing untestable).
- Synthetic (untrusted) input events — game has no `isTrusted` checks, so they're accepted; pointer lock grant was inconsistent.
- No audio (creaks/meows/beeps unverifiable); vision models 429'd all session (pixel-statistics + DOM used instead).
- Native `prompt()`/`confirm()` freeze the page in this harness — all prompt-gated flows (Earl chat, ClassRoom join/leave, bot rename, save wipe) were code-verified only.

## Suggested next rig additions
1. `--enable-unsafe-swiftshader` + `Emulation.setVirtualTimePolicy` or headed run for close-path retest.
2. Expose a `window.__SCRAP_DEBUG` hook (chatter log, ambient schedule, ChatterGuard state) — the rig had to reverse-engineer everything from the minified bundle.
3. One instrumented `?debug=chatter` query param would have converted P2-4 from "verify manually" to pass/fail.
