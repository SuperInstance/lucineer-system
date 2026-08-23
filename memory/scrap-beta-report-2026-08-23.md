# SCRAPCRAFT — Beta Test Rig Report
**Date:** 2026-08-23 (07:12–07:55 AKDT) · **Rig:** headless Chromium 151 via CDP, live deploy only
**Live deploy tested:** `https://fleet-static-host.casey-digennaro.workers.dev/scrap/` (serves `dist` build `index-DJTQGWgL.js`, built 2026-08-22 21:53 — matches repo HEAD af7e692)
**Repo:** `/home/eileen/projects/Scrapcraft` @ af7e692 (read-only reference; nothing modified, nothing deployed)

---

## ⛔ HEADLINE: THE LIVE SITE IS CURRENTLY UNPLAYABLE (P0)

Every single boot — fresh profile or returning — crashes during `Game.init()`. The game
loop never starts. The kid sees: CLOCK IN → Earl's 2-step welcome → the Yard Gate
questions → then a **frozen yard**: no movement, no mining, no day/night, no Spark
hello, no autosave, no Earl greet, no logbook, no races. HUD chrome renders around a
blank viewport. **Nothing in the playable game functions.**

### P0-1 — `Uncaught ReferenceError: Wakes is not defined` kills every boot
- **Stack (captured live, 2× clean repro + 1× across browser restart = 3/3):**
  ```
  ReferenceError: Wakes is not defined
    at vr._checkSpine   (assets/index-DJTQGWgL.js:889)   ← QuestSystem._checkSpine
    at new vr           (assets/index-DJTQGWgL.js:889)   ← new QuestSystem(...)
    at xr.init          (assets/index-DJTQGWgL.js:889)   ← Game.init
    at Cr               (assets/index-DJTQGWgL.js:987)   ← boot()
  ```
- **Repro (exact):**
  1. Open `https://fleet-static-host.casey-digennaro.workers.dev/scrap/` (any browser, any profile, incognito fine).
  2. Click **CLOCK IN**.
  3. Console shows `Uncaught ReferenceError: Wakes is not defined` (index-DJTQGWgL.js:889).
  4. Finish the wizard + gate (both still work — pure DOM).
  5. Expected: playable yard. **Actual:** frozen world. WASD does nothing, hold-left-click mines
     nothing (mine arc never engages — raycast/update loop dead), no block labels, no
     crosshair spread, ~0 game rAF frames (verified by wrapping `requestAnimationFrame`:
     only my own probe ticks; the game registers none after the throw).
- **Root cause (repo, read-only verification):** commit `7d14f6a` ("feat(story): the yard
  wakes", 2026-08-22 21:53) added to `src/quests/QuestSystem.js`:
  ```js
  _checkSpine() {
    this.wakes ??= new Wakes({ storage: this.game?.storage ?? null });  // ← no import!
    this.wakes.sync(this.spine);
  ```
  `QuestSystem.js` imports (lines 19–24) do **not** include
  `import { Wakes } from '../story/Wakes.js'`. `new QuestSystem(...)` runs `_checkSpine()`
  in its constructor (line ~46) → throws → `Game.init()` dies at line 370 →
  `game.start()` (in `main.js` boot) never runs → no `_loop()`.
- **Cascade of dead systems (all after init line 370):** PrestigeSystem/Back Room,
  night-shift payout, `beforeunload`/`visibilitychange` exit-saves (so `scrapcraft_save_v6`
  is **never written** — no saves at all), daily-contract chip, hotbar update, classroom
  prompt, Earl cold-start greet on returning boot, `this.quests` assignment (so `[L]`
  logbook is a silent no-op via `?.`).
- **Why 856 green tests didn't catch it:** the suite tests `Spine`, `Wakes`, `Tracker` in
  isolation — **no test constructs `QuestSystem`** (`node -e "new QuestSystem({}, CAMPAIGN)"`
  in the repo crashes identically). Fix is one import line; the *systemic* fix is an
  integration test that boots QuestSystem (and ideally a smoke test that runs `main.js`
  boot in a DOM shim).

**Per task instructions: no fix attempted. Documented precisely.**

---

## P1 — degrades play

### P1-1 — Companion-cycle hotkey C is dead code (nesting bug)
`src/Game.js` ~line 688 (in `_bindInput` keydown handler):
```js
if (e.code === 'KeyV' && !e.repeat && !this.ui.isOpen && !this.tileEditor.isOpen) {
  this._startRivetTalk();
  //  — swap active companion (party members take the shoulder)
  if (e.code === 'KeyC' && document.pointerLockElement && ...) {   // ← nested inside KeyV!
    this._cycleCompanion();
  }
}
```
`e.code` can't be both `KeyV` and `KeyC` → **C never swaps companions.**
- **Repro:** befriend 2+ companions (e.g. Rivet delivered + Bolt chosen at gate — exactly the
  default first-run state), press **C** in the yard. Expected: active companion swaps.
  Actual: nothing. (Verified in source + bundled JS; untestable live only because of P0-1.)

### P1-2 — Native `prompt()` for Earl chat (F key) hard-wedges the tab under kid-chaos
- **Repro (live):** press **F** (Talk to Earl). A native `prompt()` opens and freezes the
  whole game. While it's open, mash other keys (E/T/H/C…): the page's JS thread stays
  blocked; dismissing left the renderer wedged in my rig twice (CDP evaluate permanently
  timed out; only killing the tab recovered). A kid key-mashing around the F prompt can
  land in an unresponsive tab.
- **Expected:** in-game input UI (like the gate questions / Spark chat use). Native
  `prompt()` also can't be styled, can't be dismissed by ESC on all platforms, and blocks
  the loop. (Partially environment-amplified in headless; the blocking itself is inherent
  to `prompt()`.)

---

## P2 — polish

1. **P2-1 · favicon 404.** `https://fleet-static-host.casey-digennaro.workers.dev/favicon.ico`
   → 404 on every load. Trivial: inline SVG favicon in index.html or deploy one to /scrap/.
2. **P2-2 · Invisible-but-present panels pollute the accessibility tree.** `#welcome-back`
   ("WELCOME BACK / THE YARD KEPT YOUR SPOT"), the Maker "READY TO BUILD" panel and the
   Wokwi "TIN BRAIN" panel sit at `opacity:0`/`display:block` and still surface in
   role/aria snapshots. Fresh profiles see "WELCOME BACK" text in the tree — confusing for
   screen readers and for DOM-based tools. Use `display:none`/`aria-hidden` when inactive.
3. **P2-3 · Stranger-tier companion idle lines: 3 lines, no repeat-memory.** 15 simulated
   reloads → same line up to **4× in a row** (first_meet bank: 3 lines; observations
   tier-0 slice: 3 lines). A kid restarting often hears the identical "FRAGILE crate"
   joke back-to-back. Suggestion: keep a "recently-said" ring buffer (last 3) per bank in
   `scrapcraft_rivet` state; pick from `pool − recent`.
4. **P2-4 · No debug/fast-forward hooks in the live build.** Nothing like
   `window.__scrapcraft` / `?chapter=N` exists; the spine can't be QA'd in-browser
   without hours of real play. Suggestion: a `?debug=1` gate exposing `game` +
   `spine.completeThrough(n)` (dev-only), or a Playwright smoke that boots to
   first-frame (would have caught P0-1).
5. **P2-5 · "Mo's Ledger" — couldn't locate as a named surface.** The task asked to verify
   "Mo's Ledger mentions"; repo has `BotLedger.js` (bot service log), quest Logbook
   transcript, and Mo references in spine ch11/12 + finale brief. If "Mo's Ledger" is a
   planned/renamed feature it isn't in this build — worth confirming the name.

---

## Dimension-by-dimension results

| # | Dimension | Verdict |
|---|-----------|---------|
| 1 | **Cold start / first-run** | Wizard (2 steps) ✅ → Yard-Gate questions ✅ → companion delivered+persisted ✅ → **game dead at boot (P0-1)**. Zero console errors *besides* P0-1; WebGL init clean (software-render warnings are my rig's artifact). |
| 2 | **The spine** | Live: unreachable past the quest-HUD paint (constructor renders HUD, then throws). **Headless vs source: PASS** — ch1→pos2; ch2 done → East Road Light wakes; ch4 → Fence Whistle; ch6 → Smelter's Flame; monotonic under progress regression; ceremonies once-ever; Back Room catalog = 8 perks + Earl board lines present (PrestigeSystem). 12 chapters validated. |
| 3 | **Geography** | **Headless World gen, 4 seeds (1337, 42, 777, 20260823): PASS** — 12/12 named landmarks every seed; 0 floating solid blocks (yesterday's beacon-bury/float fix holds); 5 beacons, 0 buried; oval = 196 track blocks; Ghost Track landmark present with silhouette build + empty letter boards + "never gated" tease. Note: seed is **hardcoded 1337** in Game.js (RELEASE_NOTES still says fixed 42) — seeds only reachable via module API, not UI. |
| 4 | **Companions** | Entry scoring: all 16 answer-pairs → bolt 5 / rivet 6 / magma 4 / juno 1 (juno needs both "far piles"+"explore" — fine, but only 1/16 paths reach the most distinctive persona); skip-skip defaults Rivet ✅; free-pick offered ✅; state persists (bond/traits/counters JSON) ✅. Banter: tier discipline + reach-down-only rules verified in data; repeat-rate issue → P2-3. |
| 5 | **Maker loop** | Blocked by P0-1 (needs live boot). Repo's 36 maker unit tests pass; Wokwi export panel + share-link button render in DOM; `?brain=` share codes parse in `main.js` boot — but boot dies before parsing (P0-1 swallows even bad-code handling). |
| 6 | **Save/load** | Onboarding-done, gate answers, companion roster, rivet/bolt state, spine key: all persist across hard refresh **and** browser restart ✅. Game save itself: **never written** (exit-save handlers registered after the P0 crash point) — no `scrapcraft_save_v6` ever appears. WelcomeBack builder (headless): correct rows (bot+quest+streak), empty snapshot → no card ✅ — but see P2-2 (inert card text in DOM on fresh profiles). |
| 7 | **Kid's chaos pass** | DOM layer survives rapid overlay toggling (E/ESC/T/H) without JS errors. Two hard wedges both traced to native `prompt()` (P1-2). Resize to 320×400: no new errors before the wedge. Tab-switch: n/a beyond save-on-hide (dead via P0-1). |

---

## Feel report

**Three things that already feel great:**
1. **The cold-open voice.** Earl's conscription copy ("the junk's been piling up waiting
   for someone with thumbs") + the two-question gate is *instantly* characterful — a kid
   knows who runs this yard and who they are within 60 seconds. The wizard→gate→first
   quest-HUD handoff (when it ran) was smooth and un-patronizing.
2. **The spine as data.** 12 chapters with per-band delight beats, pull-vectors per
   companion, ceremonies once-ever, wakes as *ambient* (never text-dumped) — verified
   headlessly, this is a genuinely strong retention skeleton. The Logbook "what woke"
   list is a lovely idea (Earl never explains).
3. **The teaching payload.** Every quest carries a real concept + kidPhrase + a memory
   line in Earl's voice ("A robot is just scrap with a job"). PWM/PID/hysteresis/failure
   analysis at middle-school register, and the plaque trail as curriculum — this is the
   rare edu-game where the engineering is the personality.

**Three things that feel flat (with concrete suggestions):**
1. **The blank first frame.** Right now the yard never renders (P0-1) — but even
   structurally, CLOCK IN → wizard → gate means ~90 seconds of menus before a kid sees
   voxels. Suggestion: render one static hero frame of the yard *behind* the wizard
   (camera already exists post-init); let the conscription line land over the world it
   describes.
2. **Companion silence at the exact moment of maximum wonder.** Stranger tier has 3 idle
   lines and no reactive banks for the *first hour* events kids actually hit (first
   craft, first station visit, first night) — biome_first exists but low_battery/flash
   tiers beyond 0 are thin. Suggestion: 2–3 tier-0 lines each for `first_craft`,
   `first_night`, `first_station` + the repeat-memory from P2-3; Rivet should feel
   *present* in minute five, not just at first_meet.
3. **The yard doesn't answer back.** With the loop dead it's literal, but even in the
   data: the only ambient feedback loops are Wakes (5 total, chapter-gated hours apart)
   and zone toasts. Between them, minutes pass with zero yard response to the kid.
   Suggestion: cheap ambient chirps on the existing event bus (crane creaks when entering
   Industrial Corridor, the cat crosses the road near the gate every ~10 min, distant
   lap-siren when a personal best is close) — one-shot audio/DOM, no new systems.

---

## Rig artifacts
- Frozen-yard screenshot: `/home/eileen/.openclaw/media/outbound/0e5c2f81-5333-4be3-83ba-a6a92517a4dc---d4c650e1-86b0-44c2-9b45-5e555193317a.png`
- Cold-start screenshot: `/home/eileen/.openclaw/media/outbound/6303c19a-605a-4c4a-b774-6ef5ba50a9a7---dde33000-34b2-4155-baf5-b66dc508e4ae.png`
- Headless verification scripts run against repo source (read-only): world-gen invariants ×4 seeds; spine/wake cascade; entry-scoring matrix; banter draw statistics; `new QuestSystem` crash repro; `npm test` (856 ✅ 0 ❌).

## Bottom line
One missing import line (`Wakes`) shipped in last night's "yard wakes" merge and took the
whole live site down; the suite stayed green because nothing constructs QuestSystem.
Everything else I could verify — geography, spine logic, persistence, companion data —
is in genuinely good shape. Fix the import, add a boot-smoke test, redeploy, and this
report's remaining items are all P1/P2 polish.
