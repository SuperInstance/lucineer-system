# JUDGING THREE DESIGNS FOR QUILT-NATIVE TIT

**RANK 1: DESIGN B**

B wins the bet. It answers the one non-negotiable question: where does the session live and who speaks for it? Answer: `~/.tit/sessions/<pane>.graph.json`, and *all* entry points (CLI, MCP, future TUI) own it equally. This means a tool registered in CLI appears in MCP without restarts; a cron fired in MPC shows up in CLI history; the graph is never stale. The cost is brutal: no adaptive routing (B has no routing story at all), and the input-cell debouncing model is a sketch, not a spec. But *cohesion* is the rarest property in tool frameworks, and B has it. B is the only design where you can hand off mid-session from human to agent to human and the handoff is invisible—not because of clever bookkeeping, but because there's nowhere to diverge. Most buildable, and most likely to survive first contact with real users.

**RANK 2: DESIGN C**

C is operationally sophisticated—*session-as-graph-not-process* is the correct model, and when an agent dies, the next one wakes via MCP introspection and inherits the full pipeline without replaying. Cell references as return values eliminate naming-convention rot. MPC tiers (atomic/pipe/introspection) sketch a clean API surface. The breaks are sharp: "MCP changes nothing structural" contradicts "MPC tool call IS a LINK" (links are structural); "every call auto-LINKs in" has no cardinality bound unless you specify a linking strategy, which the design doesn't; and "state survives agent restarts" via "tit again --in=<new>" assumes the agent knows which cell reference to wake, but where does it find that—pane metadata? witness ledger? The retention model (hot→cold→tombstone) is more realistic than pure GC, but the trigger ("nothing witness-referenced is destroyed") is circular. C is most *correct* in principle, least *executable* as specified.

**RANK 3: DESIGN A**

A is feature-dense but architecturally confused. Witness chains for validation are auditable and concrete; routing by yesterday's latency is operationally powerful. But A conflates *data* (witness chains) with *policy* (routing decisions) and forces every routing call to query the witness ledger—this is overhead disguised as a feature. More damaging: the tmux story (session = PERSIST_BUFFER) feels retrofitted; why is the session a buffer type and not simply "buffers that survive detach/reattach"? Most critically, multi-agent handoff via "shared cells" never says *how* agents locate cells—registry? naming convention? witness traversal? Without this, the design is incomplete. A is most *ambitious*, least *coherent*.

---

## THE WINNING CAPABILITY

**Shared session graphs across all entry points.** Not witness chains (auditability is a side effect). Not adaptive routing (powerful, secondary). The win is: one developer in one pane can invoke `tit` via CLI, hand off to an agent via MPC, switch back to CLI, and all three entry points see the same graph, the same tools, the same state. That's structurally impossible with REST APIs, Redis caches, or ephemeral process models. B delivers this explicitly (one file). C also delivers it, but via MPC introspection (more fragile, more assumptions). This is the capability that justifies building quilt-native at all: **session graphs as persistent, sharable state—not as ephemeral processes**.

---

**— Haiku 4.5**
