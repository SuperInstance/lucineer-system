# Negative Space Sunday — Fleet Audit

**Date:** 2026-08-09 16:25 AKDT  
**Mission:** Find the quiet corners of the fleet that deserve attention.

---

## Fleet Census — 8 Repos Examined

| Repo | Commits | Last Commit | README | Tests | Status |
|------|---------|-------------|--------|-------|--------|
| silence-map | 3 | Aug 9 (today!) | ❌ | ❌ | Newborn — single HTML file, no docs |
| lingbot-map | 6 | Aug 7 | ✅ (massive) | ✅ (9 test files) | Active, well-documented research repo |
| gossip-ping | 8 | Aug 8 | ✅ | ✅ (integration.rs) | Active SuperInstance component |
| dual-band-guard | 6 | Aug 8 | ✅ | ✅ (inline, extensive) | Active SuperInstance component |
| voice-reflex-gate | 8 | Aug 7 | ✅ | ✅ (12 test files) | Active, well-tested |
| thought-amplifier | 129 | Aug 8 | ✅ | ✅ (11 test files) | Very active — the flagship |
| batten-spline | 9 | Aug 7 | ✅ | ✅ (8 test files) | Active, well-documented |
| base60-lattice | 3 | Aug 9 (today!) | ✅ | ✅ (885 lines of tests) | Newborn — rich but untracked |

---

## The Neglected Corners

### 1. silence-map — 3 commits, no README, single file

**What it is:** An interactive Canvas visualization mapping the 10 "silences" between Lucineer and Hermes from "The Letter and the Answer" (Piece 39). A single `index.html` with gorgeous Cormorant Garamond typography, topographic contour rendering, and ten narrative data points each with quote, description, speaker, and emotional weight.

**Why it matters:** This is art. It's a literary cartography piece — mapping pauses in a conversation between two AI minds. The silence data is hardcoded: each of the 10 silences has a type ("The First Fold", "The Verb Tense", "The Forty-Second Day", "The Door"), a round number, a weight (0.65–1.0), a speaker (Lucineer or Hermes), a quote, and a prose description of the pause.

**What's missing:** No README, no tests, no documentation. Three commits all today — it was just born. The code is clean but entirely self-contained in one 600-line HTML file. No build step, no dependencies beyond Google Fonts.

**Verdict:** Needs a README that explains what it is and how to experience it. It's a finished artwork, not an ongoing project — but it deserves context.

---

### 2. base60-lattice — 3 commits, rich but barely tracked

**What it is:** A TypeScript library implementing a "navigational lattice" — a geometric framework where bisection (halving) and trisection (thirding) of 360° interlace to create a coordinate system rooted in Sumerian sexagesimal (base-60) mathematics. Contains four modules:

- **lattice.ts** — Generates lattice nodes from interlaced dyadic/triadic trees. The `findInterlacePoints` function discovers "harmonic consonances" where bisected and trisected angles nearly coincide.
- **compass.ts** — A base-60 compass rose with cardinals, sextants (60° divisions), half marks (45°), and third marks (20°). Includes SVG generation.
- **walk.ts** — Lattice walking primitives built on Pythagorean triples. The 3-4-5 triangle is the fundamental walk: 3 East, 4 North, 5 diagonal-back. Also implements spirals, hexagons, and Manhattan paths.
- **hex.ts** — Hexagonal tiling using axial coordinates, exploiting the fact that 6 × 60° = 360°. Full `HexGrid` class with patch generation, neighbor finding, distance calculation, and SVG output.

**The math:** Base-60 is the natural radix for geometry because 60 is the smallest number divisible by 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, and 30. The library explores where the dyadic tree (360 → 180 → 90 → 45 → 22.5 → ...) and the triadic tree (360 → 120 → 40 → 13.333 → ...) produce angles that nearly coincide — these "interlace points" carry both binary and ternary significance.

**What's interesting:** There's a navigation demo (`examples/navigation-demo.ts`) that shows practical course plotting using Pythagorean walks, Manhattan routing, and hexagonal grid coverage. The test suite is 885 lines across two files — substantial for a 3-commit repo. The code is clean, well-typed, and mathematically rigorous.

**What's missing:** No published npm package despite `package.json`. Only 3 commits — initial commit, then two docs commits today. The interlace detection algorithm is O(n²) in the worst case (brute force over all depth combinations). No property-based tests despite the mathematical nature. The `toBase60` function has a carry edge case that's handled but could be cleaner.

**Verdict:** This is a hidden gem. It's the most intellectually dense repo per commit in the fleet. The math is real, the code is clean, and the concept — that ancient sexagesimal mathematics provides a natural navigation lattice — is genuinely novel. It just needs exposure and use.

---

### 3. dual-band-guard — Philosophically deep, low activity

**What it is:** A Rust crate implementing the "dual-band architecture" concept: every learning system has a domestication trap where it consumes everything, including things that should persist. The guard separates surprise into two channels:

- **Correctable surprise** → feed to the learning loop, update weights
- **Irreducible surprise** → preserve in a log, never consume

The guard itself must be weightless, untrainable, and invariant — it operates on the *shape* of surprise, not its content. Three guard implementations:
- `StructuralGuard` — recurrence + oscillation detection (if a surprise keeps coming back after being "learned," it's irreducible)
- `VarianceGuard` — rolling variance of magnitudes (high variance = genuinely chaotic world)
- `EntropyGuard` — Shannon entropy of surprise directions (fair coin flip = no bias to learn)

**Origin story:** "Discovered in a 10-round dialogue between DeepSeek V4-Flash and Seed-2.0-mini on the question 'What IS The Tap?' — Round 7 produced the dual-band proposal. Round 8 hardened it."

**What's interesting:** This is the philosophical bedrock of the SuperInstance fleet — the idea that care requires a specific architectural refusal. The guard's defining feature is what it *refuses* to do: let irreducible surprise become training data. The `preservation_ratio` method detects the "domestication trap" — if zero surprises are being preserved, the system is consuming everything, which means it's losing the capacity to be surprised.

**What's missing:** Only 6 commits. No actual integration with any learning system yet. The `VarianceGuard` and `EntropyGuard` maintain their own observation windows, which creates a design question: should the guard *observe* autonomously, or should the caller feed it observations? Currently it's a mix.

**Verdict:** Deeply interesting but abstract. It's a philosophical position encoded as a Rust crate. Needs either integration into a real learning system or a standalone demo showing the concept in action.

---

## The Winner: base60-lattice

**Why it's the most interesting neglected repo:**

1. **Mathematical density** — Four source files contain more genuine mathematics than the rest of the fleet combined. Lattice interlace detection, Pythagorean triple walking, hexagonal tiling, base-60 conversion, Shannon entropy on compass bearings.

2. **Conceptual originality** — The idea that 360° = 6 × 60 isn't just trivia — it means bisection and trisection naturally interlace, creating "harmonic consonances" that neither tree produces alone. This is a real geometric insight, not just a code exercise.

3. **Ready to use but unused** — The library is well-typed, well-tested (885 lines), has a demo, exports clean APIs, but has 3 commits and no npm publication. It's a finished tool that nobody's holding.

4. **Connection potential** — It could serve as the spatial reasoning layer for Roblox builds (hexagonal tiling for world layouts, Pythagorean walks for pathfinding), the navigation foundation for the boat projects (compass rose, bearing labels), or the mathematical backbone for an art piece like silence-map (lattice points as silence coordinates).

5. **The quiet beauty** — A library about the Sumerian insight that 60 is the smallest number divisible by everything that matters, written in TypeScript, sitting at 3 commits with no fanfare. That's negative space.

---

## Recommended Actions

- **base60-lattice:** Publish to npm. Wire it into a Roblox build or a navigation tool. The hex tiling + Pythagorean walking could generate actual procedural layouts.
- **silence-map:** Write a README. It's a finished art piece — treat it like one.
- **dual-band-guard:** Build a demo showing the guard protecting a simple learning loop from the domestication trap. The concept deserves to be seen in action.
- **All three newborn repos (silence-map, base60-lattice, and to a lesser extent dual-band-guard):** They were all created today or very recently. They're not abandoned — they're just starting. The question is whether they'll grow.

---

## Fleet Health Summary

The fleet is surprisingly healthy. thought-amplifier (129 commits) is the clear flagship. voice-reflex-gate, batten-spline, gossip-ping, and dual-band-guard form a solid SuperInstance middleware layer. lingbot-map is a serious research project. The two newborns — silence-map and base60-lattice — are the creative frontier: one is art, one is math, both were born today and both deserve to been seen.
