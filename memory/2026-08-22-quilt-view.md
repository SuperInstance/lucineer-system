# 2026-08-22 — MIST Quilt View built & deployed (flagship teaching feature)

**Worker:** https://mist-quilt.casey-digennaro.workers.dev (repo SuperInstance/mist-quilt, master @ 6770b7f)
**Game:** https://fleet-static-host.casey-digennaro.workers.dev/mist/ — 🔮 HUD button opens overlay (mist-game @ aa1fb2c, fleet-static-host @ 11de912)

Architecture: game posts 2 Hz ticks → GameRoom DO cascades formulas (centroid/spread/speed/mood/score) → WS broadcast + D1 tape + DO-storage snapshot (eviction-proofed). /chat = pincher cache (KV + D1 ledger, deepseek-v4-flash-0731; MISS 3s → HIT 4ms verified). /predict = velocity-based forward-sim + formula re-run.

Gotchas learned:
- Cloudflare Workers block `eval`/`new Function` (no unsafe_eval flag available) → formulas are native TS fns; expr strings display-only. quilt-cloudflare's `with`-pattern would 500 in prod.
- Workers AI model names drift: llama-3.1 deprecated 2026-05 → deepseek-v4-flash-0731 works, returns OpenAI-style choices[0].message.content.
- DO in-memory state dies on eviction in seconds when idle → snapshot+tape to ctx.storage every 2nd tick.
- A parallel agent session was rebuilding mist-game page.tsx (GUI overhaul) mid-task → built my commit via `git archive | tar` + hardlinked node_modules (same-fs only; /tmp is cross-device).
- claude -p needs --dangerously-skip-permissions for file writes; otherwise it just plans.

Standalone web build: 🔮 button iframes worker /view + vanilla 2 Hz ticker (web/app.js, committed).
Spec: memory/mist-quilt-view-spec-2026-08-22.md · Contract: mist-quilt/CONTRACT.md
