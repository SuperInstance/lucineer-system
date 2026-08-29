Understood—this is design debugging, not code debugging. I'll apply systematic analysis: understand each design's failure modes, identify root causes, then synthesize an integrated solution.

---

## PHASE 1: ROOT CAUSE INVESTIGATION — Each Design's Flaw

**CLAUDE Design Flaw: Race Condition Between VIEW State and EFFECT Runners**

The design separates VIEW cells (stateful, updated via TICK) from EFFECT runners (headless CLI composing cells via LINK). When a TICK fires mid-execution—e.g., a tool's state changes while an EFFECT runner is mid-pipeline—the graph is inconsistent. A SHA256 computed from a base64-decoded value becomes stale if the input cell's VIEW changes during the hash. Real symptom: "why does my pipeline output differ when I re-run it 1 second later?" No way to declare a cell's snapshot-in-time identity.

**KIMI Design Flaw: No Session Persistence Layer (Breaks Constraint B)**

The design specifies "TICK per keystroke, FORGET for ephemerals" but omits how state survives agent context switches. With Constraint B (tmux long-running agents), an agent's pipeline state must outlive its tmux window detach/reattach cycle. KIMI has no PERSIST_BUFFER equivalent. Symptom: "Agent worked for 3 hours, detached, reattached, state vanished."

**OpenCode/GLM Design Flaw: "No EFFECT" Violates Practical Workflows**

"Pure cells write only their own output" + "no EFFECT" forbids side effects. But real TIT workflows need them: `tit pipe 'fetch-url | write-file'`, `tit watch regex-buffer --cron 5m`, deployment chains. The design restricts TIT to read-only analysis. Worse, "health-aware routing at LINK layer" is undefined—what happens if a cell's provider fails mid-execution? Does the whole graph retry, or does it fall through silently? Symptom: "I need to upload the SHA to S3, but the design forbids EFFECTs."

---

## PHASE 2–3: INTEGRATED DESIGN (Constraints A + B)

**Opcode Core:**
- `CELL(id, type, state, provider)` where type ∈ {FUNCTION, TICK_BUFFER, PERSIST_BUFFER, CRON_JOB, EFFECT, VIEW}
- `LINK(src→sink, coercion)` with type-safe routing (base64.dec as coercion rule)
- `EFFECT(target)` explicit; only declared EFFECTs write (files, APIs, shell)
- `TICK(Δt)` fires TICK_BUFFER and dependents; `FORGET(ttl)` cleans ephemerals

**MCP Tool Surface (Constraint A):**
- Each tool = FUNCTION cell; MCP agents call `{"tool": "tit_cells", "link": "base64.enc", "value": "hello"}` → `{value, cell_id, route[], witness[]}`
- Health-aware dispatch: LINK resolves provider fallback chain (local native > HTTP > MCP) automatically
- Provenance chain emitted: `witness[]` = hash chain, `route[]` = provider resolution log

**Tmux Session Behavior (Constraint B):**
- Agent session = PERSIST_BUFFER cell; state survives detach/reattach
- CRON_JOB cells tick even when agent is idle (e.g., `check-tasks --cron 5m`)
- Multi-agent handoff: agent A's output = agent B's input (same cell, reused LINK)
- `tit snapshot --session $ID --cells base64,sha256` exports {value, timestamp, witness[], route[]} for resumption

---

## THE SINGLE MOST VALUABLE NEW CAPABILITY

**Replayable Pipelines with Routing Memory:** Emit `{value, witness[], route[], graph[]}` where each cell carries its provider-resolution history. Tomorrow's agent can:
1. **Validate witness chain** – confirm SHA of intermediate YAML matches cached witness
2. **Route intelligently** – if MCP was slow yesterday, use local native sha256 today
3. **Resume across session boundaries** – PERSIST_BUFFER restores pipeline state after agent restart

**Impossible in terminal TIT** (no routing layer, no witness chain). **Novel in quilt designs** because it merges Claude's composability + OpenCode's provenance + Kimi's persistence (inferred) + MCP's provider pluggability + tmux's session-as-first-class.

---

**Haiku 4.5**
