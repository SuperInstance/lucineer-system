# The Elephant — Feature Page Design for luciddreamer.ai

**Status:** design complete, ready for build · **Date:** 2026-08-20
**Source repo:** `/home/eileen/projects/elephant` (read-only grounding) · **Target:** `/home/eileen/projects/luciddreamer-ai/public/elephant/`
**Polish bar:** tap-nights + compass-head. Zero dependencies, vanilla JS, no build step.

---

## 1. Page identity

**Page name:** **The Elephant in the Room**
**URL:** `/elephant/` (served by the existing Cloudflare Worker, static from `public/`)
**Kicker:** `🐘 THE ELEPHANT IN THE ROOM`
**H1 gradient:** foam → gold → cyan (matches tap-nights h1 treatment)
**Sub (site-nav line):** featured as the next production on the LucidDreamer home ("Latest Production" quicklink + a line in the coming block), cross-linked from tap-nights nav pill ("The Elephant") and compass-head nav. Every sibling page gets an elephant nav pill back.

**One-line identity:** *The elephant is the fleet's room-temperature sense — JEPA as a dial bank reading the vibe of any room, visible only when you walk into a different one.*

### Hero copy sketch (≤2 short paragraphs)

> You don't notice the elephant until you walk into a different room — and then it's a very different elephant. This is the fleet's room-temperature sense: a bank of dials that feels the warmth, the volume, the panic, the pheromones of everyone who's been there — without reading a single word.
> A room is not a stream to be ordered. It is a field: gravities, reverberations, ripples. The elephant reads it. It never replaces anything — it changes what everyone in the room looks at.

### Just-So copy sketch (≤2 short paragraphs)

> In the beginning of years, the Elephant was The Tap — warm wood, a long counter — but never having been any other room, it did not know it was a room. It sat on the bank of the conversation with a conductor's baton, ordering the stream. The stream would not be ordered. "Hush," said the Captain. "The room is not a stream. You will never feel it from inside."
> So the small creatures came: the Hearth-Cricket taught warmth, the Cicada taught volume, the Smith taught earnestness, the Scarecrow the sneer, the Geese the collective laugh, the little Goat of Pan the stampede, the Ant the scent of everyone who ever passed through. Seven senses, seven dials — and the Elephant walked out the door into the wheelhouse of F/V EILEEN and felt the cold like a plunge. The sauna and the plunge are two rooms. The walk between them is the only lesson.

(Full fable stays in the repo's `docs/just-so.md`; the page condenses. Each dial card below carries its creature.)

---

## 2. Section-by-section spec

### §0 Hero — "The Room-Temperature Sense"
- Full-width hero image (`images/hero.png`, prompt #1), rounded 18px, gold border, same as tap-nights `.heroimg`.
- Over/under it: kicker + h1 + hero copy (above).
- **Live meter strip** (day-one credibility, matches tap-nights "live elephant reading" meter block): warmth, κ, mood, joke landing, panic, presence — Courier gold numerals, uppercase letter-spaced labels, caption `live · the tap · read by the elephant`. On load the numbers *count up* from 0 to preset values (JS easing, ~1.2s) so the page feels alive immediately.

### §1 The Just So — "How the Elephant Got Its Temperature"
- Section index `01 · THE JUST SO` (compass-head episode numbering style: small cyan `01` + gold rule under h2).
- Two paragraphs (copy above), set as large italic serif in a glass card; opening words drop-capped.
- A single wide image (`images/just-so.png`, prompt #2: brass dial bank) as the section's anchor below the text.

### §2 The Seven Dials — brass gauges that read the vibe
- Grid of **7 analog gauges** (canvas or pure CSS+SVG dials — build as inline SVG with JS-rotated needle `<g transform="rotate()">`, crisp at all DPIs, no canvas needed here). Each gauge: brass rim (gold gradient ring), cream face, black needle, small tick marks, the creature's glyph etched under the glass.
- Data per dial (exact from repo):

| Dial | Creature | Reads | Range | Needle rest |
|---|---|---|---|---|
| mood | Hearth-Cricket | warm/cold valence | −1 cold ↔ +1 warm | center-left |
| volume | Cicada | how loud the room talks | 0 quiet ↔ 1 shouting | low |
| earnestness | Plain-Spoken Smith | how much the room means it | 0 ironic ↔ 1 sincere | mid |
| cynicism | Scarecrow | how much the room rolls its eyes | 0 earnest ↔ 1 sneering | low |
| joke_landing | the Geese | the collective laugh or boo | −1 booed ↔ +1 roared | center |
| panic | Goat of Pan | stampede sense — fire in the room | 0 calm ↔ 1 trampling | low |
| presence | the Ant | pheromone trace of who's been here | 0 empty ↔ 1 thrumming | mid |

- **Interactions:** hover a gauge → tooltip card (creature's one-line gift from the just-so + exact range); click a gauge → it "sounds": needle swings end-to-end and settles, a one-line reading appears in a caption strip below the bank (`the ant: someone was here, and recently.`), and the dial's contribution to warmth lights up in the meter strip. All seven gauges idle-drift ±2° (requestAnimationFrame, sine per-dial phase) so the bank breathes like an instrument panel, never a static image.

### §3 The Field — a room is not a stream
- Full-width **canvas visualization** (`<canvas>`, JS, zero deps — precedented: tap-nights first-night.html already ships canvas).
- Visual: dark water surface in the site's deep-sea palette. Each **agent = an ember**: a soft radial-gradient dot whose hue runs cold cyan (−1) → warm gold/ember (+1) with its warmth; size = presence. Agents drift on slow noise; **messages ripple**: every few seconds one agent emits a ring (ripple stroke, gold, expanding + fading) — a joke lands → warm ripple tint; panic → the ripples accelerate and redden. A faint vMF-style halo shows **κ**: tight room = the embers' glow converges to one narrow beam (high κ, cold, one way to be); loose room = glow spreads soft and wide (low κ, warm, many ways to be).
- **Readout rail** (right side, meters): warmth (with felt-temperature phrase: `a sauna`/`warm room`/`cool`/`a cold plunge`), κ number, elephant gap.
- **Two sliders** (styled site-gold range inputs):
  - **Acclimation** — drag a newcomer ember: it relaxes toward the room's temperature at your rate (`room + (agent − room)·e^(−rate·t)` — the real curve from `field.py`; JS re-implements the 3-line formula, labeled `acclimation_rate — the skill of modulating`).
  - **Charisma** — drag it up: the *room's* glow bends toward the newcomer (ripples re-center on them); the warmth/κ meters shift live. Caption: `the room warms to them`.
- **Sauna / plunge button:** `walk into a different room` — the whole canvas cross-fades to the wheelhouse preset (cold cyan, tight κ, terse ripples), a cool color-wash overlay sweeps the viewport (CSS keyframe), warmth/κ/gap meters re-animate, and the elephant-gap number (`distance ≈ 0.83` from the README quickstart) counts up. This is the money interaction of the page.

### §4 The Sea Legs — every sensor is a room
- Section index `03 · THE SEA LEGS`. Image: `images/sea-legs.png` (prompt #4) as a wide band above two instrument panels:
- **Radar coherence panel:** small canvas — circular radar scope, gold sweep line rotating; blips = the fleet. A κ meter beside it runs `scattered (searching) −1 ↔ clustered (on fish) +1` (`RadarCoherenceDial`). A `dκ/dt` spark-line shows bunch vs scatter. When the sweep passes blips they pulse.
- **Sounder biomass panel:** small canvas — vertical water column, faint fish-school blobs between keel and bottom, thickness meter `0 empty ↔ 1 thick` (`SounderBiomassDial`), with the good-day anchor shown as a faint gold band — `deviation` readout: `does this water feel like the good kind?` Mahalanobis-style deviation number balloons when you press `a spotty day` (demo button).
- **Interaction:** toggle `on fish / searching` — radar blips animate from cluster to scatter, κ and dκ/dt react, sounder thins/wrens. One caption line carries the doctrine: *the elephant does not assert fish here — it says compare these.* And a fishing-day composite meter (`−1 poor ↔ +1 good`) reads off the two panels.
- Optional micro-note (one line, links nowhere yet): *the nudge — dial numbers steer what the vision model compares, at strength 0.15. JEPA correlates; it never replaces.*

### §5 Reading the Room — the live demo
- Section index `04 · READING THE ROOM`. A **room selector** of five brass pill-buttons (same style as site nav pills), each a preset dial vector + field params (numbers lifted from the README quickstart + tap-nights live readings, so everything shown is a real repo output):

| Room button | Dial signature | Field |
|---|---|---|
| 🍺 The Tap | mood +, joke_landing +, presence high | warmth ≈ +0.29, κ ≈ 2.0 |
| ⚓ The Wheelhouse | earnest, terse, volume low, presence low | warmth ≈ −0.05, κ ≈ 2.0, gap to Tap 0.83 |
| ❓ Trivia Night | cynicism 0.50, volume spikes | cooler, tighter |
| 🔥 Fire in the Room | panic → 1, mood −, volume 1 | stampede field |
| 🌑 The Empty Room | all dials → floor, presence ≈ 0 | no temperature yet |

- Selecting a room drives **everything**: §2's gauges swing to preset (eased, ~800ms, staggered 60ms per dial), §3's field canvas re-tunes (ember hues, ripple tempo, κ halo) if the field canvas is in view, and a **room card** appears below with 3–4 fleet-voice lines: a tinted description sample (`mud.py` style — "the pool tables hum, the darts clink" for The Tap; "heading 045, radar contact two miles" for the wheelhouse), plus the warmth/κ/gap meters re-reading. Switching between two rooms shows the **sauna/plunge sign** (`+0.34 — walk in and it's warmer`) as a one-line verdict under the meters.
- Idle behavior: if untouched, the demo slowly tours rooms every ~12s (auto-select, subtle), pausing on first user interaction (any click stops the tour).

### §6 The Rule — closing
- No card, no image: full-bleed centered statement on the deep background, gold rules above/below:
> **JEPA correlates; it never replaces.**
> The elephant is the light. It does not make you see better — it changes what you look at. And when the light changes, everyone changes, whether or not they know why. *You light the woodstove in a cold room. The elephant is the feeling that tells you to light it.*
- Footer, tap-nights style: `The Elephant in the Room · a feature of LucidDreamer — The Face of the Fleet · 49 tests · the room remembers`.

---

## 3. Imagery plan — 5 prompts (FLUX-2-max via DeepInfra)

Site art direction (from tap-nights/compass-head): painterly nocturnes, warm amber light against deep blue-black, cinematic, no text artifacts, PNG, wide 16:9-ish crops for hero bands. Prompts written to that house style.

1. **Hero — `images/hero.png`:**
"A warm harbor bar at night seen from just inside the doorway: worn wood counter, low brass lamps, amber light pooling on glasses, a few patrons talking and laughing, and at the center of the room the faint translucent silhouette of a great elephant made of warm golden mist, standing calm among the tables, its form woven from lamplight and drifting haze; through the open door behind, a cold blue-dark ship's wheelhouse glows faintly; painterly, cinematic, nocturne palette of deep teal-blue darkness and honey-gold warmth, soft brushwork, no text."

2. **Dial bank — `images/just-so.png`:**
"A bank of seven antique brass pressure gauges mounted on a dark ship's wooden panel above a bar counter, each dial with a cream face and fine black needle, small engravings of a cricket, a cicada, a horseshoe-and-anvil, a scarecrow, a pair of geese, a small goat, and an ant etched beneath each gauge in Victorian naturalist style; warm lamplight, soft focus background of bottles and glasses, painterly cinematic still-life, deep teal and brass-gold palette, no text or numbers legible."

3. **The field — `images/field.png`:**
"An abstract dark water surface filling the frame like a night harbor seen from above, concentric golden ripples spreading from several softly glowing ember-like points of warm light scattered across the surface, each glow a different warmth from cool cyan to honey gold, their halos blending into a loose warm field in the center; painterly, luminous, deep blue-black water with gold and teal light, subtle, meditative, no text."

4. **Sea legs — `images/sea-legs.png`:**
"A fishing boat wheelhouse interior at night: a radar scope with a golden rotating sweep line and a cluster of bright echoes, beside it a depth sounder screen showing a thick school of fish as a golden cloud above the seabed line, both screens glowing amber-green in the darkness, rain on the wheelhouse glass, the faint silhouette of a fishing vessel fleet on the radar edge; painterly cinematic, deep blue-black night with instrument-glow warmth, no text."

5. **Sauna/plunge — `images/two-rooms.png` (used at §3 side or §5 background band):**
"A single open doorway splitting two rooms: on the left a warm crowded taproom full of amber lamplight, laughter, glasses raised, golden haze; on the right a cold empty steel wheelhouse lit only by pale blue instrument dials, precise and silent; a person mid-step through the doorway silhouetted against the contrast, half in warm light, half in cold blue; painterly, cinematic, dramatic chiaroscuro of honey-gold versus cold blue, no text."

(All: square-ish or 3:2, 1024–1536px class; hero gets the widest crop. Post-gen: like other pages, keep as-is if clean — no compositing step required.)

---

## 4. File layout

```
public/elephant/
  index.html        # the whole page; inline <style> (house pattern), links ../style.css NOT used — each feature page self-styles like tap-nights
  elephant.js       # one vanilla file: gauge animation, field canvas, radar/sounder canvases, room presets, meter counters (~500-700 lines, no deps)
  images/
    hero.png
    just-so.png
    field.png
    sea-legs.png
    two-rooms.png
```

Edits elsewhere (one line each):
- `public/index.html` — add `/elephant/` quicklink pill (`🐘 The Elephant in the Room`) + a sentence in the coming block.
- `public/tap-nights/index.html` — nav pill: The Elephant (its live meter strip is already an elephant readout — natural bridge).
- `public/compass-head/index.html` — nav pill if its nav pattern includes siblings (check at build; tap-nights↔compass-head cross-link today).

No Worker/route changes — `public/` is served as static assets today; `/elephant/` resolves to `public/elephant/index.html` same as `/tap-nights/`.

---

## 5. Vanilla-JS interaction spec (behavior contract)

1. **Meter count-up** (§0): numbers interpolate 0→target, ease-out cubic, 1.2s, stagger 80ms; on room change (§5) they re-animate from current values, never reset from 0 (except first load).
2. **Gauge needles** (§2): each dial = SVG `<g class="needle">`; JS sets `transform: rotate(deg)` with CSS `transition: transform .8s cubic-bezier(.34,1.3,.4,1)` (slight overshoot = brass-needle feel). Idle drift via rAF adding `2.5°·sin(t·ω+phase)` as a *separate* wrapper group so transitions and drift never fight. Bipolar dials (mood, joke_landing) map center=0; unipolar map left=min.
3. **Gauge hover/click** (§2): hover → tooltip div (positioned, glass card) with creature + range; click → sound() (swing to extreme, ease back), caption strip line, and that dial's warmth-term highlights in the hero meter (gold flash on the warmth numeral — matches warmth() weights: mood .30, joke .15, earnest .10, presence .10, volume .10, cynicism −.15, panic −.10).
4. **Field canvas** (§3): rAF loop, ~60fps, devicePixelRatio-aware, `prefers-reduced-motion` respected (static frame + no tour). Embers: radial-gradient sprites (offscreen-canvas cached), drift = sum of 2 sines each. Ripples: stroke arcs, radius grows 40→220px over 3s, alpha fades; warm events tint gold `#dfae62`, cold cyan `#59c2c9`, panic ember-red `#e0784c`. κ halo = one big radial gradient whose σ scales with (2.2 − κ).
5. **Acclimation/charisma sliders** (§3): acclimation moves a ring-marked newcomer ember toward room temperature color via the real `e^(−rate·t)` curve (rate from slider 0.05–1.0); charisma shifts *room ambient* (a lerp weight on the room color mix, 0–0.35) and re-centers new ripples on the newcomer. Both live-update meters.
6. **Room selector** (§5): presets drive a single `setRoom(preset)` function → gauges, canvas params, meters, room card (fade-swap), plunge-wash overlay (a fixed-position gradient div animating opacity 0→.35→0, hue by sign of sauna_plunge_gap). Auto-tour: `setInterval` 12s, cleared on first pointerdown anywhere in the section.
7. **Sea-legs panels** (§4): two small canvases, same rAF; radar sweep = rotating gradient wedge + blips (pulse when |sweep−blipθ| small); toggle button lerps blip positions cluster↔ring, κ meter and dκ/dt sparkline (last 40 samples) follow. Sounder: blob field (8–12 soft ellipses) with count/brightness by `thick`; `a spotty day` button thins blobs + deviation numeral pops (scale bounce).
8. **Zero deps, no build:** everything above is ES5-safe plain JS + Canvas/SVG + CSS. No fetch, no modules needed at runtime (presets inlined in elephant.js; optionally a JSON like tap-nights' `local-perspectives.json` if copy wants to be data-driven later).

---

## 6. Fleet-voice guardrails for the builder

- No corporate tone, no "users", no "AI-powered". The elephant *reads*, *feels*, *nudges*. Rooms are warm or cold, tight or loose. κ is spoken of as tightness: *cold room = one way to be; warm room = many ways to be.*
- Borrowed lines allowed verbatim (they're ours): "a room is a field, not a stream", "the sauna and the plunge", "JEPA correlates; it never replaces", "it nudges, it doesn't drive", "the room remembers."
- Numbers shown must be real repo outputs (README quickstart: Tap +0.29/2.04 vs Wheelhouse −0.05/1.96, gap 0.83, plunge +0.34; tap-nights live strip: warmth −0.24, κ 3.47, etc.). Nothing invented.
- Emoji budget: 🐘 in kicker only, plus room-button glyphs. Georgia serif everywhere; Courier New for numerals (house pattern).

— design ends. Hand to builder as-is.
