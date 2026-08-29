[0m
> build · glm-5.3
[0m
[0m→ [0mRead r4a-prompt.md
[0m→ [0mRead /home/eileen/.openclaw/workspace/scratch/tit-quilt/seed.md
**Q1 — MCP ERGONOMICS**

**1st — kimi.** The most implementable-tomorrow answer of the three. The `oneOf: [literal, {$ref}]` input schema is the only form that's both JSON-Schema-valid for MCP discovery and unambiguous against hostile data; `#json-pointer` is the standard, not a homebrew dot-path; and "deref at EFFECT time" is the one resolution rule nobody else stated — it's what makes replay and concurrent pipes deterministic. Add the witness-union formula, a concrete dangling-ref error shape, and `route: []` when native (two bytes — cheaper than any clever encoding), and a contractor can open an editor and start on tool #1. Flaw: ~2x over the 400-word cap; that's spec-discipline debt.

**2nd — opencode (GLM-5.3).** The best cost analysis of `route` ("you pay for route only when health did") and the best failure semantic — unresolved refs produce *error cells*, so provenance survives even the failure path, which kimi treats as a plain error. But it ships self-inflicted wounds: `$c:<4hex>` hard-caps a session at 65,536 cells (says cold triggers at >10k — so the cap is 6x the working set, cute until it isn't); it claims "(12)" tools and lists 11; `tit.a64_encode` is a name only its author loves; and the answer opens with terminal noise from the session, which in a spec round is sloppy. Ranked on merit, mine sits here.

**3rd — claude (Haiku).** Two build-killers. `tit.pipe.jwt→b64→sha` implies dynamically-composed tool names, but MCP tool lists are statically declared and discovered — that tool is unbuildable without a codegen layer nobody budgeted. And `@cell://...` string-prefix refs are indistinguishable from a literal value that starts with `@` — the exact injection bug the `$ref` object form exists to prevent; `.FIELD` access also can't reach nested arrays. The envelope itself is fine and latency-per-hop is honest, but `latency_ms` on every native call contradicts its own "route stays cheap" claim. Concrete, wrong where it counts.

---

**Q2 — THE SESSION DAEMON**

**1st — opencode (GLM-5.3).** By a hair, and on one line: "the daemon is a cache, not the store." That single framing makes every downstream answer fall out — WAL with fsync per op (the only answer that actually claims durability; an append without fsync is a page-cache lie), compaction per 1k edges, boot_id on the pidfile (kills the PID-reuse-after-reboot bug class that plain flock schemes eat), and an ensure-daemon connect sequence that resolves the two-clients-spawn race explicitly ("first flock winner becomes daemon; losers just connect"). Retention triggers are the most concrete of the three, tombstones keep `blake3(witness)` so claims stay verifiable forever. Defects it should fix before build: steal kimi's in-band `"recovered"` marker — my "notices within 50ms" is a latency claim, not an observability mechanism — and steal lazy cold reload so eviction is invisible to ref resolution. Also over word cap.

**2nd — kimi.** Correct transport choice with the sharpest rejection line ("locks give mutual exclusion but no request/reply"), append-before-reply ordering, journal-tail replay, and the best answer to the judges' literal "who notices" question: the retried call carries `route:["recovered"]` — in-band, zero-cost, undeniable. Lazy reload of cold cells is a real semantic guarantee the others don't offer. It loses 1st only on durability rigor: no fsync, no compaction cadence, no stale-pidfile story — three operational holes a 2 a.m. outage will find. The MCP shim paragraph ("~50-line adapter, spawn/kill freely") is the cleanest statement of why disposability works.

**3rd — claude (Haiku).** Incoherent at the foundation: it *rejects* sockets because they "require the daemon to stay running" — then designs a daemon anyway, spoken to via 500ms lock-file polling. That's a socket rebuilt badly, minus streaming: `attach` needs pushed deltas and this protocol cannot push; its own attach step ("waits for daemon to drop exclusive lock") hand-waves the one requirement that drove the question. Worse, its stated justification — WSL/network mounts — is exactly where flock is least trustworthy (NFS/9p lock semantics are a graveyard). Credit: concrete retention thresholds and the simplest on-disk crash story; files-survive-daemon is right. But the transport decision is the question, and it chose wrong for its own stated reasons.

---

**THE BUILD-CRITICAL DECISION**

**Decide where truth lives: the append-only WAL on disk is the store; the daemon is a disposable, replayable cache; CLI and MCP shim are thin socket clients — before a single tool, envelope, or schema is written.** Why this one: it's the decision that *forces* every other answer into place. It forces the transport to a Unix socket (a cache that must answer requests and stream attach deltas must be able to talk back — this single clause deletes Haiku's file-lock design). It forces MCP-shim disposability (clients spawn/kill freely because no truth lives in the process — the exact fault the judges caught in Design B). It forces crash recovery into replay, not rescue, and makes "who notices" answerable in-band. And it's the only decision that is *ruinous to reverse late*: tool names, envelopes, retention thresholds, even the ref syntax can all evolve after ship — moving truth out of a live daemon's memory once three MCP clients depend on its resident state is a rewrite wearing a migration's clothes. Note also that it's the one decision invisible in the deliverables everyone rushed to write: you can ship all 30 MCP tool definitions and still never have made it. That's precisely why it gets made first, on paper, by the owner.

— GLM-5.3 (Z.ai)
