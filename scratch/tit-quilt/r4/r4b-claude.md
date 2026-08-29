## JUDGMENT — ROUND 4b

### Q1 — MCP ERGONOMICS RANKING

**1st: Answer 3 (OpenCode/GLM-5.3)**
Cell reference syntax `$c:9f2` is unambiguously buildable—it's session-scoped, terse (8 chars), and JSONPath-native (`$c:9f2.claims`). The atomic tool list is concrete (12 named), not abstract aspirational. Route optimization (6-byte default string, expand only when interesting) is pragmatic—you don't pay for path metadata when it's "native." Witness format `["w($c:9f2)","t:a64_encode@2"]` is clean. Zero spec ambiguity; a junior engineer could implement this envelope tomorrow.

**2nd: Answer 2 (Kimi)**
Compact pointer syntax `s9f2:c014#field` is nearly as buildable, and the distinction between "resolve at EFFECT time" vs. "push on wire" is clear. Dangling ref detection returning error *cells* (preserving provenance on failure) is sophisticated. But the envelope spec is less concrete—when does `route` expand from `[]` to an array? When does a tool "hop"? The design is strong; the spec is still being formed.

**3rd: Answer 1 (Haiku/mine)**
Full URI syntax `cell://s:session-id/c:ulid[.FIELD]` is over-engineered—the `cell://` protocol adds no semantic value and costs bytes on every reference. The `@ref` input syntax is less standard than `$ref`. Witness as array of cell_refs creates implicit typing (which cell refs are "providers" vs. "inputs"?). Route metadata as objects with `provider` + `latency_ms` is fine, but no optimization for the hot path. Buildable, but requires more clarification work.

---

### Q2 — SESSION DAEMON RANKING

**1st: Answer 2 (Kimi)**
Unix socket + NDJSON + append-only journal is the battle-tested pattern. Fsync per effect before reply is the correct durability guarantee. Auto-spawn on EPIPE with transparent retry is the right automation—failures don't leak to the user. Memory pressure → lazy reload of values is production-grade thinking (you don't fail when hot memory fills; you demote gracefully). "route":["recovered"] makes crashes observable in-band without special logging. The design survives the messy reality of networks and process death.

**2nd: Answer 3 (OpenCode/GLM-5.3)**
WAL + compaction per 1k edges is solid. The boot_id in the pidfile is excellent—it catches reboots without stale PID ambiguity. Tombstone design with blake3(witness digest) is clever (you can verify a claim's provenance without rehydrating the payload). But the daemon lacks streaming semantics—`tit attach` in Kimi's design gives you deltas; Answer 3's version isn't clear on how a long-lived session gets incremental updates. Crash recovery is correct but less explicit than socket-based push.

**3rd: Answer 1 (Haiku/mine)**
File-lock protocol is a clever attempt to avoid socket complexity, but it's a polling pattern disguised as synchronization. The 500ms refresh loop is not event-driven—it has latency floors. "Daemon sees lock → reloads graph" is hand-wavy about *how* the daemon is woken. The critical gap: when the daemon itself crashes and restarts, how does it know which `.lock` files are stale vs. in-use? You'd need the CLI to re-touch its lock, but that's not specified. The `.cold/` directory structure is reasonable, but file-lock schemes don't compose well with remote mounts or WSL edge cases (locking semantics vary). More engineering work needed before buildability.

---

### THE BUILD-CRITICAL DECISION

**Cell reference syntax. This is non-negotiable and locks everything else.**

The three options:
- **URI**: `cell://s:session-id/c:ulid.field` (Haiku)
- **Pointer**: `s9f2:c014#field` (Kimi)  
- **Short form**: `$c:9f2.field` (OpenCode)

This is the decision because:
1. It appears in *every* tool response envelope—defined once, baked into billions of cells
2. Witness chains are immutable; wrong ref syntax means migration hell later
3. It determines the serialization cost of chaining (30 bytes vs. 2KB matters)
4. Client code for resolving refs, caching strategies, and tooling all flow from this choice

**Verdict: Go with OpenCode's `$c:` syntax.**
- Session-scoped (correct—refs should not leak across sessions)
- Shortest (8 chars; Kimi's is 13+; URI is 50+)
- JSONPath native (`$c:9f2.claims` is intuitive for nested access)
- First-time readable (doesn't look like a URL or binary hash)

Once that anchor is set, the rest follows naturally: **socket + journal daemon** (Kimi's model wins here; OpenCode's boot_id idea gets incorporated). The envelope is determined, the wire protocol is determined, and the build can proceed without revisiting this layer.

---

**Claude Haiku 4.5**
