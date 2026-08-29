#!/bin/bash
# TIT round 2: cross-pollination + critique + improve, with MCP + tmux angles
cd ~/.openclaw/workspace/scratch/tit-quilt || exit 1

cat > r2-prompt.md <<'EOF'
ROUND 2 — you now read the three round-1 designs (below) for a QUILT-NATIVE TIT.RUN, plus TWO NEW CONSTRAINTS from the captain:

NEW CONSTRAINT A (the MCPs): the fleet runs MCP servers (quilt MCP, AgentCompute "agent-facing CLI over the quilt MCP server", harness mcp_tool_use). TIT's headless tools could be exposed as MCP TOOLS — so any MCP-capable agent (Claude Desktop, OpenClaw, any) can call base64/JSON/cron/JWT as tool calls. How does that change the quilt-native design? (Tools as MCP tools = the agent-native surface; cells = the internal substrate; both views of the same graph.)

NEW CONSTRAINT B (tmux long-running agents): the fleet's coding agents run in long-lived tmux sessions (claude -p, kimi, opencode, coding-agent lanes). A terminal toolbox for THOSE agents is not a TUI a human stares at — it's a headless companion they call from inside their session, plus their workspace state persists across hours/days. How does quilt-native TIT serve a long-running agent's session? (Persistent tool state as cells that survive the session? Cron/job cells that keep ticking while the agent works? A tool chain that remembers its last pipeline?)

THE THREE ROUND-1 DESIGNS:
[CLAUDE] Tools→FUNCTION cells (VIEW in, EFFECT out); stateful tools = VIEW cells + internal state via TICK; fuzzy picker = BIND re-weighting; TUI = VIEW over the graph; CLI = headless EFFECT runner composing cells via LINK pipelines (base64→url-decode→sha256 as one graph); quilt gives: composability, witness-trit provenance ("this SHA came from this input at this time via clipboard"), health-aware routing (swap local MD5 for remote), state as first-class. ENHANCE: multi-view live tool-chain designer (web VIEW + TUI VIEW, one graph).
[KIMI] (transcript truncated — infer: opcode mapping, cells for each tool, TICK for live typing, FORGET for ephemerals.)
[OPENCODE/GLM] Pure tools = FUNCTION cells: BIND declares tool cell, LINK(input→tool), VIEW renders derived slot, no EFFECT (pure cells write only their own output); headless CLI = EFFECT runner binding argv as a cell, evaluating subgraph, emitting cell-graph JSON, FORGETting ephemerals; live-as-you-type = TICK per keystroke; TUI = one VIEW, fuzzy search = VIEW filter over BIND registry; clipboard = EFFECT. Abstraction: composability (json.fmt→yaml→sha256 = 3 LINKs one subgraph), provenance w(sha256(x)) = w(x) ∪ {sha256_cell@v}, routing (tool id = interface, providers = native/MHS cli/http/mcp transports, LINK resolves via health-aware weights, ascending dispatch), statefulness (regex/cron buffers as persistent cells). ENHANCE: provenance pipelines — `tit pipe 'base64.dec | yaml.load | sha256' --emit graph` outputs {value, witness[], route[], graph[]} — a rerunnable auditable derivation replayable in any render layer.

YOUR TASK (≤400 words, concrete):
1. QUESTION: find the sharpest flaw in EACH rival design (what breaks in practice?).
2. RESEARCH-AND-IMPROVE: given constraints A (MCP tools) and B (tmux long-running agents), propose the IMPROVED integrated design — the opcode mapping, the MCP tool surface, and the tmux companion behavior. Name the single most valuable NEW capability a quilt-native TIT has over terminal TIT, now with MCP+tmux in view.
3. Sign your model name. This is still a competition.
EOF

claude -p "$(cat r2-prompt.md)" > r2-claude.md 2>&1 &
kimi -p "$(cat r2-prompt.md)" > r2-kimi.md 2>&1 &
opencode run --auto "$(cat r2-prompt.md)" > r2-opencode.md 2>&1 &
wait
wc -w r2-*.md
