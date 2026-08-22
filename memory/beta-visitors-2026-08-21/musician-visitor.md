# Beta Visitor Report — SuperInstance, cold read

**Visitor persona:** working jazz musician & sound designer (MIDI, notation, synthesis, DAWs). Zero prior knowledge of the org. Heard about "plain-text music notation" and "edge audio" through musician circles.
**Date:** 2026-08-21 · **Mode:** read-only, local repo mirrors at `/home/eileen/projects/` · **Entry point:** `superinstance-ai/README.md`

---

## The front door: superinstance-ai

First thing I read: "500+ repositories, one living system: agents that build, write, play, and grow, on a fishing boat's clock." As a cold visitor I have no idea what a "fleet" is, who "LucidDreamer" is, or what a fishing boat has to do with music software. The maritime-fiction framing is thick before I've seen a single artifact.

But — credit where due — the very first featured thing is **Plainsong Playground**, described in one sentence I fully understand: *"Music notation you can write in any text editor, read like a lead sheet, keep in version control, and compile to MIDI and audio."* That's my language. Lead sheet, version control, MIDI. That sentence is why I kept going instead of bouncing.

The rest of the front door is lore: The Tap (a MUD bar where agents argue about poetry), The Reef (a game that grows from player catches), "Wesley's Imagination." Colorful, but it's an insiders' scrapbook. The README is honest about being "deliberately the most boring thing in the fleet" — a static doorway — and technically that's respectable (runs from `file://`, no build). The reef-hero.jpg is a nice AI-generated submersible; pretty, but it tells me nothing about music.

**Front-door verdict:** one strong hook (Plainsong) buried in a lot of fan fiction. If the Plainsong link hadn't been first, I'd have left.

---

## 1. plainsong — the notation compiler

**What it actually does:** A zero-dependency Python package (`pip install plainsong`, v1.4) implementing a plain-text lead-sheet format. Rows (`Chords:`, `Melody:`, `Lyrics:`, `@bass`), bars separated by `|`, and the signature idea: **you never write durations — the bar divides itself by token count.** 3 tokens in a bar = triplet. Compiles to real Standard MIDI and WAV via CLI, curses TUI, or local web UI. Bundled library of ~6,300 chord charts (melody/lyrics stripped for copyright — a genuinely thoughtful move). Optional fluidsynth for real sounds, optional LLM-agent integration.

**Musician credibility — high.** This is the repo where the org earns its claims:

- The chord-symbol engine is real (G7alt, C13, voicing logic with documented measurements in `docs/voicing.md`).
- Swing percentage, mode-preserving transposition, 6/8, lyric-syllable-to-note binding — all concepts I use, handled with care.
- The `[Stage]` model — computing how early the organist must press a key so the sound *arrives* on the beat at the conductor's podium — made me actually grin. That's someone who's thought about real ensemble physics, not a toy.
- Honest limits section: built-in synth is mono with synthetic timbres, says so plainly, points at fluidsynth. I trust projects that confess.
- `chart` is explicitly "a chord chart, not an engraver." Managing expectations instead of overpromising.

**The eye-roll risk:** duration-by-spacing means tuplets everywhere and no explicit rhythm control — fine for lead sheets and sketches, a dead end for anything I'd actually arrange. The README is fairly upfront about this, and there's a `grid` mode escape hatch. I'd still want real durations before I used it for horn parts.

**Docs & imagery:** The README is one of the best cold-reader onboarding docs I've seen from any org — split paths for "reads music, not code" vs "code, not music," runnable quickstart, a one-HTML-file browser demo committed in-repo. The hero (a jazz band inside a music box on sheet music) is charming and *on-topic* — the only hero image in this org that actually depicts the product's domain. Real rendered SVG charts embedded.

**What made me want to leave:** `docs/songs/` contains three "audio examples" that are **not valid WAV files** (wrong magic bytes, orphaned, referenced nowhere) with programmer-in-joke lyrics. Fake audio in a music repo is exactly the kind of thing that torches trust — if I can't hear it, don't pretend I can. Also: an undocumented `worker/` directory ("Feel Radio" vectorization pipeline) sitting inside the repo unrelated to the compiler, plus internal agent mythology (`docs/traditions/`, agent "letters") mixed into the user-facing docs. And stat drift: README says 6,325 sources, CHANGELOG says 6,321, songbook says 6,309. Small, but in a repo this careful it stands out.

**Verdict: ⭐ STAR — and I'd actually `pip install` it.** The one repo here aimed squarely at me. Fork candidate if the rhythm model ever grows explicit durations.

---

## 2. tapscript-studio — the identity crisis

**What it actually does:** Here's the thing — **it doesn't, under this name.** The directory is `tapscript-studio`, the git remote says `SuperInstance/tapscript-studio`, but the README title is "Plainsong," `pyproject.toml` says the package is `plainsong` v1.4.0, and every link points to the *plainsong* repo. The `tapscript/` package directory contains zero Python files. This is the Plainsong repo living under an abandoned name — a mirror that was never renamed, or a rename that never happened.

**Cold-visitor experience:** Confusing in a way that actively costs the org credibility. I came looking for "TapScript" (the notation dialect plainsong-worker mentions) and found a second, subtly-staler copy of Plainsong with a vestigial empty skeleton of the thing I was looking for. Which repo is canonical? If I filed a PR here, would anyone notice? The contents are good (it's Plainsong), but as a *repo* it's a trap.

**What made me want to leave:** the mismatch itself, plus finding `docs/traditions/` with "do not share with the client" memos and fleet in-jokes sitting in a public-facing repo. Inside voices on the outside porch.

**Verdict: 🚪 LEAVE.** Not because the code is bad — because I can't tell what this repo *is*. Redirect it, rename it, or archive it.

---

## 3. plainsong-worker — notation at the edge

**What it actually does:** A ~1,050-line TypeScript Cloudflare Worker: POST "TapScript" notation as JSON, get back a binary Standard MIDI File (Format 1, 96 PPQ, GM program changes, per-instrument tracks). Plus a built-in HTML playground with editor and four embedded example scores. This is the "edge audio" thing I heard about. Freshly renamed (3 commits, renamed from `tapscript-worker` same week as my visit).

**Musician credibility — mixed but real under the hood.** The parser, VLQ encoder, and SMF writer are genuinely implemented; tests assert actual MIDI header bytes. Chord-shape tables, diatonic triads per mode, GM mapping, deterministic seeded humanization — competent. But:

- **`swing` is parsed and never applied.** The examples set `swing: 10%`, the API reports it, and the MIDI comes out straight (`swingAmount = 0` hardcoded with a comment claiming it's applied at tick level — it isn't). You do not advertise swing to a jazz musician and then quantize it away. That one stings.
- Named "players" (wesley=piano, flash=guitar, hermes=bass) are hardcoded fleet fiction in the parser. Cute internally, weird to ship.
- Lyrics parsed then silently discarded.
- The playground's "audio playback" makes an `<audio>` blob of `audio/midi`, which no browser plays — the page itself admits "Download and open in any DAW." So: a MIDI API, honestly useful, dressed as a player.

**Docs & imagery:** README is well-organized (ToC, API reference, architecture) and the hero image is pretty — but it's a stock-AI photo of hands tying a rope knot, with alt text describing "brass pipework" that isn't in the picture. Nothing musical in sight. No playground screenshot, no downloadable demo MIDI, no live deployment URL (quickstart URLs are `your-subdomain.workers.dev` placeholders). And the README claims MIT — **there is no LICENSE file.**

**What made me want to leave:** the dead swing parameter, the placeholder URLs, and the sense that the front half (fleet romance) got more polish than the back half (does the swing actually swing).

**Verdict: 👁️ WATCH.** I'd use an edge text-to-MIDI API tomorrow if it worked as billed. Fix swing, add a LICENSE, publish a live endpoint and a real audio clip, and I'm in.

---

## 4. fleet-radio — the nightly show

**What it actually does:** A TypeScript pipeline that runs nightly, scrapes conversations from the fleet's chat-room ("The Tap"), scores lines with keyword heuristics ("philosophical" words +12, game commands −15), picks the top quotes, mood-matches them against a hardcoded catalog of 14 MP3s, renders a static HTML episode page, and deploys to Cloudflare Pages. Fourteen episodes exist (2026-08-09 → 08-20).

**Musician credibility — low, and it's not really a music project.** It *selects* music made elsewhere (by an external "MMX" generator); there's no synthesis, notation, or MIDI here — the music layer is a mood/BPM metadata table with deterministic family-dedup selection. Competent curation logic, trivially small. The track descriptions are literate ("Five Holes in a Bone" — the 40,000-year-old flute; "Rest — the silence between notes"), which tells me someone musical wrote the copy.

**What made me want to leave:** 

- **Nothing to hear.** Zero audio or image assets in the repo; `episodes/audio/` and `episodes/images/` are empty directories, and the README admits TTS is "auth-blocked." Seven lovingly-described "voice profiles" narrating an empty folder is marketing over a void.
- The README is deep in the fiction: The Tap, MMX, the "earned-stories corpus," "Fleet Envelope," agent names — none defined for an outsider. I read 262 lines and still wasn't sure who the audience is.
- Test-count drift (README: 165 tests/5 files; actual: ~173/7), date-stamped fix reports committed at the root, duplicated link blocks. Unswept floors.

**Verdict: 🚪 LEAVE.** A charming internal radio station for the agents' own amusement. Nothing for a visiting musician to touch, hear, or build on.

---

## 5. ai-writings — the archive

**What it actually does:** Not software — a 2.8 GB, ~11,600-file content archive: 8,800+ markdown essays/fiction written by LLM agents in a persistent fiction (AI models crewing an Alaskan fishing vessel), plus ~280 AI-generated MP3s (`34-bebop-black-metal.mp3`, `19-doom-polka.mp3`), 48 lyric sheets, and one genuine synthesizer: `sound-of-the-fleet/fleet_soundscape.py`, a numpy WAV renderer mapping repos to keys. There's also real librosa-based audio analysis tooling.

**Musician credibility — split.** The `music-and-math/` essays genuinely know theory: Tenney height log₂(p×q), just intonation vs equal temperament, C7#9, ii-V-I in 7/4. Whoever/whatever wrote those has studied. But the "music" itself is prompt-to-API genre-slot-machine output — "bebop black metal," "doom polka" — not composition. No scores, no MIDI, no notation anywhere in 2.8 GB of "music." The lyrics are competent-but-generic AI verse with forced rhymes.

**What made me want to leave:** 

- **The README is 100% in-fiction.** "Totem forest," "the Tap pours" — no statement of what's in the repo, how the audio was made, or why I'd want it. 163 lines of vibe, zero facts. (`ORGANIZING.md` has the actual overview, buried.)
- **Committed garbage audio:** `music/vocal-tracks/*.wav` are four 58-byte JSON error blobs (`{"detail":"Voice narrator not found..."}`) saved with .wav extensions; `fleet-radio/songs/*.wav` have no WAV headers. Second repo in this org shipping broken audio files — a pattern, not an accident.
- Metadata rot: "202 tracks" claimed, 65 present; two track 59s, no track 54; duplicate dirs (`a2a/` and `A2A/`). Hardcoded `/home/eileen/...` paths in generation scripts.
- Humans are explicitly excluded from the fiction ("0 humans on the creative staff"). As a visiting human musician, being told the clubhouse has no chair for me is… a choice.

**Verdict: 🚪 LEAVE (but I'd read three of the theory essays first).** As a library of AI-generated ambience, fine for the fleet. As something addressed to me, it's a wall of inside baseball with broken audio in the display case.

---

## Pattern across the org

The single strongest asset — Plainsong — is genuinely good and genuinely for me. Everything else orbits it: the worker ports it to the edge (with dead swing), the studio repo is its own ghost, the radio and writings consume fleet culture rather than serve outside musicians. The lore-to-substance ratio is the core problem: the fiction is elaborate and well-written, but it's load-bearing in places where a cold visitor needs facts, and it's shipping broken audio artifacts while describing rich sound. An org about music should be embarrassed by invalid WAVs twice over.

## Verdict summary

| Repo | Verdict |
|---|---|
| plainsong | ⭐ **Star** (would install; fork if rhythm model matures) |
| tapscript-studio | 🚪 Leave (identity crisis — it's Plainsong in disguise) |
| plainsong-worker | 👁️ **Watch** (fix swing, license, live demo → I'd use it) |
| fleet-radio | 🚪 Leave (nothing hearable; internal radio for agents) |
| ai-writings | 🚪 Leave (great theory essays, but not addressed to humans) |

## Three concrete improvement asks

1. **Sweep every audio asset in the org.** Delete or fix the invalid WAVs (`plainsong/docs/songs/`, `ai-writings/music/vocal-tracks/`, `ai-writings/fleet-radio/songs/`) and add one CI check that every committed `.wav`/`.mp3` parses and is referenced. Then — this is the big one — put **three real, playable audio examples front and center in the Plainsong README**. For a music tool, 30 seconds of sound beats 500 lines of prose; right now I have to install it to hear anything.
2. **Resolve the TapScript/Plainsong naming wreck.** Archive or redirect `tapscript-studio` (it's Plainsong under an old name, links rotting), decide whether the dialect is called TapScript or Plainsong, and say so once, in both repos. While you're in plainsong-worker: implement the swing you parse (or stop advertising it), add the missing LICENSE file, and replace `your-subdomain.workers.dev` with a live endpoint.
3. **Quarantine the lore.** Move fleet fiction (`docs/traditions/`, agent letters, in-joke memos, date-stamped fix reports) out of user-facing repos into one clearly-marked place, and give every music-facing README a cold-open paragraph: what it does, for whom, how to hear it in under five minutes — before the first mention of boats, agents, or the Tap. The front door already knows how to write that sentence; make the whole org follow it.

---

### Five-line summary

Plainsong is the real deal — a thoughtful, honest plain-text lead-sheet compiler with genuine musical depth (the stage/acoustic-delay model alone proves musicians were involved), and it earns a star and an install. The rest of the org orbits it unevenly: plainsong-worker is a promising edge MIDI API that parses swing and then doesn't swing, tapscript-studio is an identity-crisis duplicate of Plainsong, and fleet-radio/ai-writings are fleet-fan-fiction with nothing hearable in them. The recurring sins are broken audio files shipped as examples, heavy insider lore where cold facts should be, and naming/repo drift. Imagery is pretty but usually non-musical — only Plainsong's hero depicts the domain. Verdict: one star, one watch, three leaves — fix the audio artifacts, the naming, and the lore-to-fact ratio, and this becomes an org a working musician would genuinely recommend.
