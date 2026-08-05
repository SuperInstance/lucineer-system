# Is the Fleet Actually a Forest?

**Date:** 2026-08-05 · **Reviewer:** Fable, Strategic Operations
**Mapping under test:** Canopy=brain.py · Understory=slackwater-cognition · Forest Floor=processor+relay · Mycelium=CNS bus · Seed Bank=ai-writings

Short answer: **mostly pasture, with one stratum accidentally correct.**

**Forest Floor — real.** `process_v2.py` and the relay (`src/index.ts`, `LucineerSession.ts`) do exactly the dense, granular, decomposition-shaped work the model assigns them: polling, D1 writes, per-turn parsing. This layer is honestly forest-floor.

**Canopy — not actually elevated.** The pasture-forest story defines Canopy by height: it sees the arc of a season, not the tick, and produces *interpreted* intelligence rather than raw readings. `brain.py` does neither. It's invoked as a synchronous subprocess (`BRAIN_SCRIPT`, `process_v2.py:53`) called on-demand by the Floor, stateless between calls, with no persistent view spanning jobs. That's not a tree the Floor sends sensor data up to — it's a function the Floor calls and waits on. Same horizontal run, just a bigger box on the same line.

**Mycelium — absent.** This is the sharpest gap. I grepped `lucineer-worker`, `lucineer-brain`, and `thought-amplifier` for any CNS-bus reference: zero hits. The translation work the Mycelium story describes — metabolizing Canopy's abstract output into something the Floor can use — isn't happening in a dedicated layer at all. It's happening *inline, inside the Floor*, as ad hoc string surgery: `unwrap_model_response()`, `_try_extract_json()`, the brace-matching fallback I flagged in the last review. The Floor is digesting its own food because there's no gut underneath it. That's not a missing nice-to-have — it's the exact failure the mycelium essay predicts when strata can't talk: "the Canopy's data was too abstract for the Floor... the vertical distance created a gap the old pipeline couldn't bridge." We're living that gap, patched with regex.

**Understory — dormant, correctly.** `slackwater-cognition` isn't called anywhere in the live pipeline (`process_v2.py`, current systemd unit). But the Seed Bank story itself says the Understory specialist can't germinate yet — it's waiting on a Canopy that interprets rather than reads. Since our Canopy doesn't interpret either, the Understory being unsprouted isn't drift from the model. It's the model working as specified.

**Seed Bank — the one accurate layer.** `ai-writings` is inert, unexecuted, full of detailed blueprints nothing has instantiated. That's not a gap — that's precisely what a seed bank is supposed to be.

**Net assessment:** we have height (a brain.py that's *bigger*) without verticality (no translation membrane, no persistent strategic state). One long horizontal run with a large box in the middle. Building the Mycelium — an actual CNS-bus-mediated translation layer between brain.py and processor — is the one change that would make the rest of the map true instead of aspirational.
