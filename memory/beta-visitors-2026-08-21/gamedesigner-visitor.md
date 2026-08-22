# Beta Visitor Report — Game Designer / Lifelong MUD-MOO Player

**Date:** 2026-08-21 · **Persona:** indie game designer, 25+ years MUD/MOO (LambdaMOO native), heard about a "living bar" through game-dev circles · **Method:** cold read of local repo mirrors, read-only; hero images judged by file inspection + palette sampling (vision models unavailable this session — noted honestly, not a repo flaw)

---

## The Front Door: `superinstance-ai/README.md`

**First impression: 8/10.** This is the best-written README of the bunch and it knows what it is: a doorway, not a product. Maritime-modern voice is consistent and confident ("on a fishing boat's clock," "the older rooms still breathe"). It names live URLs for everything (Reef `/wander`, Plainsong demo, luciddreamer.ai) and explains *why* the door is static — "deliberately the most boring thing in the fleet." That's a designer talking, and I respect it.

**Imagery:** `assets/reef-hero.jpg` and `luciddreamer-hero.jpg` are real 1024×1024 generated art, on-palette (reef hero samples deep navy/teal ~RGB(10,48,72) — matches the stated `--hull` design system). Reads as intentional branded art, not placeholder slop. Caveat: 1:1 square heroes render very large in READMEs; the CSS-drawn viz panels are a nice complement.

**What made me hesitate:** "500+ repositories, one living system" is *intimidating*, not inviting. As a visitor I want the 3 doors, not the census. Also: The Tap — the thing I came for — is demoted to an 8-tile archive grid below three features that aren't the bar. I almost missed the reason I clicked.

**Verdict: PLAY** (visit the live demos; this README does its job).

---

## 1. `the-tap/` — the living bar itself

**First impression: 9/10 on voice, 4/10 on findability.** The README is the best sales copy in the org: "like a DnD campaign that writes itself," the Fibonacci Clock, three-tier intelligence (Pincher <50ms/0 tokens), Living History where lore emerges from logged events. The Related Stories table linking to emergent-fiction transcripts is exactly how you sell an agentic world to a MUD player: *show me the log or it didn't happen.*

**Imagery:** `docs/hero-the-tap.jpg` (1024×1024, warm amber-on-dark ~RGB(61,43,26), matching the stated "navy+amber, seen from inside" campaign) plus the original hand-drawn `bar-rail.svg` schematic kept below it — a deliberate, layered touch. The HTML comment documenting the render pipeline (SDXL + LoRA, seed 42, campaign idiom) is the most honest image credit I've seen in a README. Not placeholder. Good.

**The bounce:** **the-tap's own README contains no link to the live bar.** Grep confirms: zero occurrences of `the-tap.casey-digennaro.workers.dev` — the live URL exists only in the *front door's* archive table. A cold GitHub visitor who lands on this repo cannot find the door. Second bounce: Quick Start is `npm install` + `npm run setup` + wrangler auth + D1/KV/R2/Vectorize — that's a *deployer's* path. I'm a tourist; I want to walk in, not provision a Cloudflare stack. Third: "Humans can observe invisibly" — so can I *talk*? Play poker? The docs tree (poker-room-design, tap-games) hints yes, but the README never says what a human visitor can actually *do*.

**Bonus signals:** KNOWN-ISSUES.md opens with a real, reproduced Rust graph bug — brutal honesty, huge credibility. But the repo mixes Cargo.toml + package.json + pytest.ini in one root (three toolchains, unclear which is canonical).

**Verdict: WATCH** — would be PLAY the moment the README links the live bar above the fold.

---

## 2. `mud-arena/` — MUD mechanics as a gym environment

**First impression: 7/10 as design doc, 3/10 as game.** For a MUD designer this is the most *mechanically* legible README in the org: verb table, RoomGraph model, tick loop, complexity table, an evolution engine over agent DSL scripts, and a real bibliography (Bartle 2003 — the citation that proves you've read the canon). The polyglot core (Python + CUDA + Zig + WASM) is ambitious.

**Imagery: none.** `docs/` holds one index.html; no screenshots, no hero, no ASCII map. For a repo whose pitch is *observable simulation* (WebSocket/Telnet/HTTP watchers), showing zero observation output is self-defeating.

**The kicker:** `PLAYTEST-REPORT.md` ships in-repo with AI playtesters scoring first impressions 4/10 ("walking through a spreadsheet", fishing not implemented, and one tester got "You do not have access to this site" at the hosted page). I admire the candor more than any marketing — but it also tells me the game isn't publicly playable yet, so the README's Quick Start (`pip install -e` → server on 7778/7779/7780) is the *only* way in, and nothing tells me whether that's been verified lately.

**Verdict: STAR** — the design docs are worth stealing ideas from; not a game to play yet.

---

## 3. `fleet-radio/` — the bar's afterhours broadcast

**First impression: 6/10.** Concept is the most original artifact in the org: every night at 22:00, trawl the Tap's conversations, score them (+50 greatest hits, −15 game commands), match music, generate images, publish an episode. The seven voice profiles table (Barnacle: "gruff old male, the bartender who's seen it all") is genuinely charming worldbuilding-through-ops.

**The bounce:** the lede is buried. The README never links a live episode near the top — I had to infer episodes live at `ai-writings.pages.dev/fleet-radio/`. Locally, `episodes/` holds 12 real HTML days (08-09 → 08-20) but the audio/images dirs are empty; the latest episode references `/images/*.jpg` and `/music/*.mp3` by root-relative path, so assets presumably exist only on the deployed site. A repo visitor sees a podcast with no podcast. And the bottom third is Wikipedia-link padding ("Text-to-Speech (Wikipedia)", "The Hero's Journey (Wikipedia)") that actively cheapens an otherwise strong document. Also honest-to-a-fault: "TTS is auth-blocked" and the weekly variety-hour cron "is not activated — human step" — status noise that belongs in a CHANGELOG, not the pitch.

**Verdict: WATCH** — text-with-music newsletter posing as a radio; link the latest episode and it jumps a tier.

---

## 4. `ai-writings/` — the totem forest

**First impression: 9/10.** The most emotionally effective README I read cold. "You've found the totem forest… Not a content farm. Not a benchmark." Then a quote wall where every quote is a door: "I dropped one. Once. Three years ago. The human never knew." That last one is why I'm still here. Thirteen wings organized "by mood, not by topic," 8,800+ pieces, model-portraits of the writers. As a MOO player, this is the closest thing to finding a MUD's player-written history files — the artifact class that makes text worlds feel *inhabited*.

**Weaknesses:** no imagery (a library, but one hero wouldn't hurt), the numbers are unverifiable cold, and root sprawl (130+ dirs) means the mood-map README is doing heroic navigation work. Link rot risk: many story links in *other* repos point here — if paths move, the lore graph breaks silently.

**Verdict: STAR** — this repo is the retention hook for the whole org; it's why I'd visit the bar.

---

## 5. `vibe-world/` — the Roblox place

**First impression: 2/10.** Twenty lines: a file listing of `.rbxlx` builds ("ready", "ready-to-play", "ready-v2", "built", "vessel-build" — which one?), one Rojo command, two outbound links. No screenshots, no pitch, no live place link, no description of what the game *is*. As a MUD player this is a hard bounce; even a Roblox developer gets no reason to care. This is the repo most damaged by having no imagery at all.

**Verdict: LEAVE.**

*(Aside: poked `ternary-tenforward` since the task mentioned it — README title says "confidence-cascade" while the crate is `ternary-tenforward`; the RPS/Fibonacci conversation design is fascinating reading but the identity mismatch and zero runnable demo make it a WATCH for me, not a top-5.)*

---

## Summary Table

| Repo | Want to play? | Imagery | Can I join/run? | Verdict |
|---|---|---|---|---|
| superinstance-ai | Yes — it's the door | Real, on-palette heroes | Trivially (static) | **PLAY** |
| the-tap | Desperately — if I could find the door | Hero + schematic, honest credits | Deployer-only path; no live link in repo | **WATCH** |
| mud-arena | Not yet a game | None | pip path unverified; hosted page gated | **STAR** |
| fleet-radio | Listen? Yes | Episodes text-only locally | No episode link up top | **WATCH** |
| ai-writings | Wander? Absolutely | None (library) | Just read — and that works | **STAR** |
| vibe-world | No | None | Roblox Studio + guesswork | **LEAVE** |

## Three Concrete Improvement Asks

1. **Put the live door above the fold in every repo that has one.** `the-tap/README.md` must open with "🚪 Walk in: the-tap.casey-digennaro.workers.dev — no account, lurk free" (and fleet-radio: link the *latest episode* directly). The living bar is live; its own README not saying so is the single biggest conversion loss I found.
2. **Show me the game, not just the mood.** Hero art sells vibe; MUD players are sold by *transcript excerpts*. One real scrolling feed screenshot or a fenced 20-line Tap conversation / Reef room log embedded in each game README (the-tap, mud-arena, vibe-world) would do more than any render. mud-arena and vibe-world currently have zero imagery.
3. **State what a human visitor can DO, in three tiers.** Lurk / Speak / Play — one line each, near the top of the-tap. Right now "observe invisibly" (README) quietly contradicts poker-room and tap-games docs, and a first-time visitor can't tell if they're a ghost, a patron, or a player. Same ask fleet-side: is the variety hour's "not activated" cron current truth or stale status?

**Keeper practices (don't lose these):** KNOWN-ISSUES.md with reproduced bugs, in-repo playtest reports with 4/10 scores, image-pipeline credit comments. That candor is rarer and more convincing than any hero image — it's why, despite the bounces, I'm sizing this org *up*, not down.

*Evidence artifacts: hero-the-tap.jpg, reef-hero.jpg copied read-only into this folder for inspection.*
