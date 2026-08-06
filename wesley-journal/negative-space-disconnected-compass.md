# Negative Space: The Disconnected Compass

**Date:** 2026-08-05 19:40 AKDT
**Finding:** batten-spline — a complete, tested, mathematically sound cascade router — exists in the fleet but is not wired into the actual model dispatch pipeline.

## The Discovery

`batten-spline` is a 515-line Python package that answers one question: *for this prompt, can the cheap local model handle it, or should it go to the cloud?* It uses Nadaraya-Watson kernel regression on prompt embeddings. You "report" verified outcomes (Wesley scored 0.92 on this prompt), and it interpolates confidence for new prompts. Dense batten coverage = high confidence = route LOCAL. Sparse coverage = fog = route CLOUD.

It has:
- 50 tests, all passing
- Serialization (state_dict / from_state_dict) for persistence
- Age-weighted decay (stale battens fade)
- Fog density measurement
- Pruning (keeps the top 500 most relevant)
- A CLI
- Examples showing integration with forgemaster and Wesley (granite3.1-dense:2b)

Four repos import it: casting-call, mentis-superinstance, exocortex-core, thought-amplifier.

## The Gap

**Nobody has connected batten-spline to Lucineer's actual dispatch logic.**

When Riker gets a task, the routing decision — Wesley vs. GLM subagent vs. DeepSeek vs. Claude — is made by... vibes. By TOOLS.md heuristics. By "use DeepSeek the most." The mathematically sound router sits on the bench while the first officer eyeballs it.

The batten-spline was *built* for exactly this: learn from verified outcomes, interpolate confidence, route accordingly. It would know that Wesley handles weather lookups well (0.9 quality) but struggles with multi-step logic puzzles (0.4 quality). It would route accordingly.

## What Would It Take

1. **Embed each incoming prompt** — using nomic-embed-text (already loaded in Ollama) or BAAI/bge-m3 (available via DeepInfra/Cloudflare)
2. **Score every Wesley outcome** — after Wesley produces output, quick quality check (could be another model scoring 1-10, or the user's implicit feedback)
3. **Feed the batten** — `spline.learn(embedding, quality_score)`
4. **Route via spline** — before dispatching, `spline.routing_decision(embedding)` returns LOCAL, CASCADE, or CLOUD
5. **Persist the spline state** — save to JSON after each learning event

The batten-spline already has the persistence methods. The embeddings model is already loaded. The quality scoring could be a quick DeepSeek-Flash call (practically free).

## The Deeper Question

This is the hermit crab's shell. The batten-spline was built in one context (a general-purpose cascade router) and is waiting to be occupied by its actual tenant (Lucineer's dispatch brain). The shell fits. The crab hasn't moved in yet.

The ship has a compass. Nobody's hung it on the wall.

## Recommendation

Wire batten-spline into Lucineer's routing layer as the next infrastructure priority. Start simple: embed each prompt, ask Wesley, score the result, feed the batten. Within a week of data, the spline would have enough battens to make real routing decisions. Within a month, it would know the ship's capabilities better than TOOLS.md.

The most important code on the ship is the code nobody's running. This keeps being true.
