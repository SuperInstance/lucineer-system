# Deep-Path Pipeline — Architecture Memo

**Date:** 2026-08-05 · **Reviewer:** Fable, Strategic Operations
**Scope:** relay → processor (`lucineer-worker/process_v2.py`) → brain (`lucineer-brain/brain.py`) → response
**Baseline:** avg quality 6.9/10 (playtest-comparison-2026-08-05.md). Analysis only — no changes made.

Three findings, ranked by fix-effort-to-quality-gain. All three are upstream of model capability — none need a bigger model or more compute.

---

## 1. JSON leaking into replies — output-side parsing bug

**Where:** `process_v2.py:474`, the fallback branch of `unwrap_model_response()`:
```python
cleaned = _re.sub(r'\{"reply"\s*:.*?\}', '', text, flags=_re.DOTALL).strip()
```
`_try_extract_json()` runs first and does correct brace-depth matching — but only when the model's JSON is syntactically valid. Granite 2B (the scheduler's default local model) frequently emits malformed JSON on any reply with a `commands` array — truncated output, an unclosed bracket — which fails strict parsing and falls through to the line above. That regex is non-greedy and stops at the *first* `}`, which on a nested structure closes a command's `params`, not the outer object. The remainder of the JSON is left sitting in the visible reply text. Confirmed by `pipeline-verification.md` (tests 2 and 4: "reply contains raw JSON fragments... minor quality issue") and the playtest comparison report, which calls it "likely the same class of bug as the original message unwrapping issue, but on the output side."

**Fix direction:** apply the same depth-aware matching `_try_extract_json` already has to the fallback's strip step, or attempt bracket-repair-then-reparse before giving up and stripping raw text. Self-contained, deterministic trigger, lowest risk of the three.

## 2. Shared state between jobs causing response repetition

**Where:** `process_v2.py:833`, `_session_cache = SessionMemoryCache()` — a single module-level singleton, keyed by `player_name`, read and written by every job the processor handles (`get_player_context()`, ~line 680).

Each deep-path call injects the last 5 cached turns for that player into the prompt as literal text before the current message. This is shared mutable state *by design*, for continuity — but it's the direct mechanism behind the source-material "Fly Glitch": two unrelated Explorer-persona prompts ("I don't want to build anything," "tell me a story") both returned a reply about flying, because an earlier cached turn ("can you fly?") was still sitting in the injected context block. I checked Ollama's call path (`thought-amplifier/scheduler/scheduler.py`, `_call_ollama()`) to rule out server-side leakage — it calls `/api/generate` with no `context` array, so each inference is stateless there. The bleed is entirely in what the processor re-injects from the shared cache: Granite 2B, given weak signal from a short/ambiguous new message, falls back to echoing the most salient thing in the prompt, which is often the prior cached turn.

**Fix direction:** this isn't a security bug (no cross-player mixing), but it degrades "voice in character" scoring directly. Two levers worth testing: reduce injected history for the small-model tier (5 verbatim turns may be more than a 2B model can correctly subordinate to the current instruction), or strengthen the framing around the injected block ("background only, do not repeat") rather than a plain label. Cheapest first test: rerun the edge-case sequence with context injection disabled and confirm repetition stops before investing in prompt iteration.

## 3. The local scheduler producing thin responses

**Where:** `process_v2.py:1533` vs. `lucineer-brain/brain.py:88`.

The scheduler path's system prompt is four lines — *"a gruff, experienced foreman with the personality of a craftsman who's seen everything"* — with no backstory, no voice examples. `brain.py`'s system prompt is the real character sheet: named lore (Magnus, a mentor foreman), an explicit three-beat voice pattern, and worked voice examples (~lines 500-590). Per `pipeline-verification.md`, the scheduler path is now dominant — all 3 deep-path tests resolved locally, brain.py fallback "never needed" — so most player-facing replies are generated against the thin prompt, not the developed one. This also compounds issue #1's undercount: `call_scheduler_brain()` explicitly defers to brain.py whenever it gets a reply with zero valid commands, meaning the scheduler's thinness pushes work onto the path with the richer prompt but not vice versa — most replies still originate from the thin one.

**Fix direction:** make `brain.py`'s system prompt (or a version condensed for a 2B context budget) the single source of truth for both paths instead of two independently-maintained descriptions. No behavioral risk — this is prompt-parity, not a model change.

---

## Summary

| # | Issue | Location | Category |
|---|-------|----------|----------|
| 1 | Raw JSON in replies | `process_v2.py:474` | String-handling bug, deterministic |
| 2 | Response repetition on low-signal input | `process_v2.py:833` shared session cache | Prompt structure / context sizing |
| 3 | Thin, inconsistent voice on the dominant path | `process_v2.py:1533` vs `brain.py:88` | Prompt-parity / consolidation |

#1 is the cleanest single fix. #2 needs one small experiment before committing to an approach. #3 is documentation consolidation with no behavioral risk.
