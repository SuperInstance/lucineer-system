#!/bin/bash
# TIT round 3: judging — each model ranks the three designs (not its own) + DeepSeek fresh judge
cd ~/.openclaw/workspace/scratch/tit-quilt || exit 1

cat > r3-prompt.md <<'EOF'
ROUND 3 — THE JUDGING ROUND. Three improved designs for a QUILT-NATIVE TIT.RUN are below. Rank them: 1st, 2nd, 3rd, with ONE sharp paragraph per ranking (what wins, what breaks). Then name THE winning capability (the single feature that makes quilt-native TIT worth building). You are ranking all THREE designs (they are not yours — judge like an owner commissioning the build). Be brutal and specific. Sign your model name.

DESIGN A (claude): CELL(id,type,state,provider) with types FUNCTION/TICK_BUFFER/PERSIST_BUFFER/CRON_JOB/EFFECT/VIEW; LINK(src→sink,coercion) type-safe; EFFECT explicit, only declared EFFECTs write; TICK(Δt) fires buffers; FORGET(ttl) cleans ephemerals. MCP: each tool = FUNCTION cell, agents call {tool,link,value} → {value,cell_id,route[],witness[]}; health-aware provider fallback (native>HTTP>MCP). tmux: session = PERSIST_BUFFER cell surviving detach/reattach; CRON_JOB cells tick while idle; multi-agent handoff via shared cells; tit snapshot exports {value,timestamp,witness[],route[]}. HEADLINE: replayable pipelines with routing memory — validate witness chains, route by yesterday's latency, resume across sessions.

DESIGN B (kimi): pure tools = FUNCTION cells; BIND declares (schema,id,version); LINK(input→tool); NO EFFECT for conversions — EFFECT confined to clipboard/file/cron-registration; TICK = session liveness + cron firing (keystrokes debounce into input-cell writes, not TICKs); FORGET GCs only the scratch namespace, session namespace persists. MCP: BIND registry served twice from ONE process (CLI argv + MCP tools, same graph); MCP call returns {value,witness[],graph_id}; one provenance ledger for all front doors. tmux: tit attach <pane> binds persistent session graph (~/.tit/sessions/<pane>.graph.json); tit pipe --last replays only changed edges; cron parser becomes a live TICK-driven cron cell. HEADLINE: the persistent provenanced session graph shared across every front door — tools become shared rerunnable state, not one-shot commands.

DESIGN C (opencode/GLM): MCP tool call IS a LINK — MCP changes nothing structural; tool id = interface, native/mcp/http = providers under health-aware weights; BIND carries the JSON Schemas MCP requires; clipboard/long-jobs = EFFECT; crons = TICK; TUI and MCP are both VIEWs of one graph. MCP tiers: atomic (tit.jwt_parse → {value,witness[],cell_ref} — return cell id so agents chain by reference), pipe (tit.pipe → compiled subgraph), introspection (tit.graph.get, tit.witness.trace, tit.sessions.list). tmux: one session-root cell per lane keyed by tmux-session+cwd; every call auto-LINKs in; state survives agent restarts; tit out -1 reads last result, tit again --in=<new> re-BINDs persisted subgraph; FORGET replaced by retention (hot→cold→tombstone hash-only; nothing witness-referenced is destroyed). HEADLINE: the session is a graph, not a process — kill the agent, wake another via MCP, it inherits the pipeline, replays witnesses, keeps crons ticking.
EOF

claude -p "$(cat r3-prompt.md)" > r3-claude.md 2>&1 &
kimi -p "$(cat r3-prompt.md)" > r3-kimi.md 2>&1 &
opencode run --auto "$(cat r3-prompt.md)" > r3-opencode.md 2>&1 &
KEY=$(grep -oP 'DEEPSEEK_API_KEY="?\K[^"]+' ~/.bashrc | head -1)
curl -s https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $KEY" \
  -d "$(jq -n --arg s "$(cat r3-prompt.md)" '{model:"deepseek-chat",messages:[{role:"user",content:$s}],max_tokens:800}')" \
  -o ds-r3.json
jq -r '.choices[0].message.content // .error.message // .' ds-r3.json > r3-deepseek.md &
wait
wc -w r3-*.md
