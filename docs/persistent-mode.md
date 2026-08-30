# PERSISTENT MODE — local thinking, cloud nudges

*Casey, 2026-08-29 19:13: "think about persistent mode in codex. we can keep thinking about this locally and use cloud models to nudge it."*

## The idea, distilled

Cloud agents are episodic: session opens, context loads, work happens, session dies.
Walk-state evaporates. Codex-style "persistent mode" inverts the residency:

**The thinker lives locally and never dies. The cloud is a visitor, not the resident.**

- Local model (Ollama silicon: Liquid-LFM2.5-2.6B / mistral:7b / deepseek-r1:8b on the 4050)
  runs a continuous think loop — cheap, private, offline-capable, no per-token meter.
- Its **state persists across ticks** in a journal + working cell (QUF-shaped: bounded, warm-loadable,
  fold-covered by construction).
- Cloud models (GLM-5.3, DeepSeek) never hold the session. They receive a *compact digest*
  of current state and return a **nudge** — direction, correction, a question — which is folded
  back into local state as an event, not as a replacement of context.

This is literally the elephant architecture (nudge.py: dial → attention prior; JEPA
correlates, never replaces) and the doctor/nurse JEPA reading: local = nurse/patient/room,
cloud = doctor/reader of the delta. Cloud reads the *step*, not the whole stream.

## Why "codex persistent mode" resonates

Codex CLI's local agent has filesystem + shell residency: state is the repo, not the context window.
Persistent mode generalizes it: **the context window is a cache, the journal is the memory,
the tick loop is the mind.** A boat can lose connectivity for three days; the thinking doesn't stop,
and when the cloud returns it reads the log deltas, not the ocean.

## Architecture (the hundred-boats shape)

```
┌─ LOCAL (always on, free) ──────────────┐   ┌─ CLOUD (visitor, metered) ─┐
│ tick loop (cron/daemon, 5–15 min)      │   │                            │
│   1. read journal head + working cell  │   │  nudge endpoint:           │
│   2. local model thinks one tick:      │   │   in: digest ≤2KB          │
│      observe → update cell → 1 thought │   │   out: ≤3 nudges + 1 Q     │
│   3. append journal (append-only)      │◄──┤   folded in as events      │
│   4. every N ticks or on stuck-ness:   │──►│  stuck-ness signals:       │
│      emit digest → request nudge       │   │   loop-detected, no drift, │
│   5. fold nudge in (timestamped,       │   │   contradiction w/ cell,   │
│      source-tagged CLOUD/LOCAL)        │   │   repeated question        │
└────────────────────────────────────────┘   └────────────────────────────┘
```

House rules the loop inherits:

- **Fail-static**: a failed nudge fetch changes nothing; local keeps ticking (Q4).
- **Ticked**: logical local time; cloud nudges are *events in the log*, never a rewrite (Q5).
- **Balanced books**: every cloud claim that alters the cell must be booked (credit where the
  nudge changed a conclusion — conservation of provenance).
- **Fold-covered**: the journal folds; the digest is a fold, and its round-trip is checked.
- **Bounded**: cell has a max size; overflow = fold, not truncate.

## What the cloud nudge is and is not

IS: direction ("you're circling; try X"), correction ("§3 contradicts your cell's line 12"),
a question ("what breaks at n-ary?"), a pointer ("read GENERAL-CALCULUS GC-C2").
IS NOT: the thinker. The cloud never writes conclusions into the cell directly — it writes
*nudges*, and the local model must act on them in its own voice, on its own tick. If the local
model can't re-derive why a nudge was folded in, the nudge expires (staleness window — the
ρ·F floor applies to the thinking loop itself: the local mind cannot see through its own
staleness; the cloud auditor's freshness is bounded the same way).

## Prototype plan (small, tonight-shaped)

`tools/foreman-think/` in the workspace:
1. `cell.json` — the working cell (bounded, QUF-exportable).
2. `journal.jsonl` — append-only, source-tagged.
3. `tick.py` — one tick: read cell → prompt local model → append thought → maybe update cell.
4. `digest.py` — build the ≤2KB fold-digest (cell + last-k thoughts + stuck signals).
5. `nudge.py` — cron'd: call cloud (GLM-5.3 flash tier or DeepSeek Flash) with the digest,
   fold response as CLOUD events; rate: hourly is plenty.
6. First standing topic for the loop: **the corpus itself** — let it read one paper per day locally
   and think; cloud nudges point at connections. Wesley's growth path, generalized.

Upgrade path: this is the F/V EILEEN wheelhouse brain's exact skeleton. Same code, boat hardware,
satellite-window nudges instead of always-on cloud.

## Open questions (to think on, locally, fittingly)

1. What's the right tick interval vs. thermal cost on the 4050 (idles at ~60 tok/s on LFM2.5)?
2. Should nudges be *scheduled* (hourly) or *drift-triggered* (stuck-ness detector)? — the DRIFT-AS-PREFILTER answer says: drift-triggered, tolerance r+Σρᵢ.
3. Who audits the auditor when the cloud nudge is wrong? → the local model must be able to
   reject a nudge with a booked reason; rejection rate is itself a dial worth tracking.
4. Does codex CLI itself fit in (as a local tool the thinker can invoke), or do we build the loop
   bare on Ollama first? Recommendation: bare Ollama first; codex is one reachable tool later.
