# JUDGING ROUND 4b — Rankings and Decision

## Q1 Rankings: MCP Ergonomics

**1st — kimi.** Three tiers, one envelope, and the syntax is compact and unambiguous. `s9f2:c014#payload`, `@last`, and `{"$ref":...}` inside `oneOf` are clear, minimal primitives. Best insight: `route` is *empty* when native — route encoding cost scales with actual routing, not protocol overhead. `w(out) = w(in) ∪ {tool@ver}` is a clean compositional rule. `tit.pipe` with edges count is pragmatic. This design can be implemented in a weekend without corner-case surprises.

**2nd — claude.**
`@cell://s:SESSION/c:ULID[.FIELD]` is explicit but verbose; the mechanics are sound but the syntax will bloat every chained call. Response envelope's `cell_ref`, `value`, `witness`, `route` is solid, and the chain pattern is correct. But the `@ref` syntax introduces a new dereference semantic that competes with JSON pointers — two mechanisms, one job. Slightly overweight.

**3rd — opencode.** The JSONPath suffix `.claims` and `$c:last` are fine, but the envelope's `"route":"native"` as a *string* is a design smell — a scalar where the others use a list (or empty list). Any future multi-hop routing path will require migrating from string to array, breaking the contract. `$c:<4hex>` is too short; collision risk at scale with a 16-bit namespace. The design is buildable but has landmines, and your example chaining `a64_encode({b:{"$ref":"$c:9f2.claims"}})` composes poorly with tools that take multiple args.

## Q2 Rankings: The Session Daemon

**1st — kimi.** This is the production-grade answer. Unix socket + NDJSON gives streaming `attach`, one-shot `out`, crash detection, and clean request/reply. Journal-before-reply for durability is the correct write-ahead pattern. `titd` as auto-spawn on connect failure with journal tail replay is textbook recovery. The `"route":["recovered"]` in-band flag is the touch of a systems engineer who's actually debugged distributed state. Calling file-locks "a socket rebuilt badly" is the brutal truth. This survives the "demo at 3am" test and the "two clients, one daemon" test.

**2nd — opencode.** Same socket architecture, solid WAL + compaction design. The `ensure-daemon` pattern (connect → fail → flock → fork → replay → serve) is efficient and correct. But it's the *spec* of a daemon, not the *protocol* of a daemon. The JSONL op framing is thin — no request IDs, no correlation between a `call` and its `result` when multiple clients multiplex. The `attach` call returns cell names but not the replacement `route` metadata. It's a good skeleton, but the muscular system is incomplete. Also, waking a daemon on the first client call — a cold-start latency hit — needs a heartbeat or keepalive that's unspecified.

**3rd — claude.** File-lock protocol is the wrong choice for the stated goals. File-based coordination is brittle: 500ms refresh loops guarantee missed pushes, stale locks require PID checks, and "try to acquire exclusive lock by writing to `~/.tit/sessions/<key>.lock`" is a recipe for race conditions when two clients attach simultaneously. The "reload graph if stale" logic is fuzzy. And the cold/tombstone lifecycle (hot → cold → tombstone, 1000 ops/10min/24h thresholds) is plausible but the daemon never actually streams deltas to clients — `attach` is a one-shot graph read, not a subscription. This is reconstructing state, not a daemon. The "NEVER DIES" for witness chain is right, but the whole thing is a bit-file system, not a session service.

## THE BUILD-CRITICAL DECISION

**The single decision: the session store's durability model — specifically, the point at which a cell's data and witness are committed to stable storage before a client is acknowledged.**

Everything else — the tool tiering, the socket vs. file-lock, chaining syntax — is refinable. But if the store acknowledges an EFFECT and then loses it (or worse, corrupts it), the entire provenance layer collapses into a feature that cannot be trusted in production. The builder must decide *now*: is the journal fsync'd per op (kimi's `journal.jsonl` + checkpoint at N edges, pick N) or is the graph in-memory with lazy compaction (opencode's WAL + `graph.json` compact at 1k edges)? This decision drives the wire protocol (streaming vs. one-shot), the crash recovery code path, the client's retry semantics, and the entire testing strategy for the daemon. Get it wrong and the "witness chain" becomes a ceremonial artifact — the daemon will lose the very facts it was built to preserve, and no amount of clever `@cell://` syntax or `$c:last` sugar will save a toolchain whose history is fiction.

If I'm commissioning this build: I demand kimi's commitment to journal-then-reply, socket transport, and auto-spawn recovery. And I require opencode's `ensure-daemon` pattern plus kimi's `"route":["recovered"]` in-band recovery marker. Claude's file-lock is the prototype; kimi's is the product. The decision that gates it all: **the durability contract of the session journal, decided before a single line of protocol code.**

— GLM-5.3 (Z.ai)
