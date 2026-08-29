ROUND 4b — JUDGING ROUND. The three yards below answered the two fault-line questions (Q1 MCP ergonomics; Q2 the session daemon). Rank the answers PER QUESTION — 1st, 2nd, 3rd, one sharp paragraph per ranking (two ranking lists total). Then name THE build-critical decision — the single decision this build must get right before any code is written, and why. Judge like an owner commissioning the build: brutal, specific, buildability over cleverness. One of these answers may be your own — rank it on merit or lose credibility. Sign your model name.

=== ANSWER 1 — claude (Haiku 4.5) ===
## Q1 — MCP ERGONOMICS

**Tool tier naming:**
```
tit.jwt.parse         (atomic)
tit.pipe.jwt→b64→sha  (pipe)
tit.introspect.tools  (introspection)
```

**Response envelope:**
```json
{
  "cell_ref": "cell://s:session-id/c:ulid",
  "value": {...},
  "witness": ["cell://s:session-id/c:input-ulid"],
  "route": [{"provider": "native", "latency_ms": 2}]
}
```

**jwt_parse example:**
```json
{
  "cell_ref": "cell://s:abc123/c:jwt42",
  "value": {
    "header": {"alg": "HS256", "typ": "JWT"},
    "payload": {"sub": "user", "exp": 1234567890},
    "signature_b64": "SflKxw..."
  },
  "witness": ["cell://s:abc123/c:token_input"],
  "route": [{"provider": "native", "latency_ms": 1}]
}
```

**Chaining by reference — `cell_ref` resolution:**
Instead of re-sending payload, next call uses `@ref` syntax:
```json
{
  "tool": "tit.base64.encode",
  "input": {
    "data": "@cell://s:abc123/c:jwt42.payload"
  }
}
```

Daemon resolves `@cell://...` to actual value locally; agent never sees it. This is **cell reference resolution** (the mechanism). Rule: `@cell://s:SESSION/c:ULID[.FIELD]` resolves to value or field by local graph lookup. Route stays cheap—it's metadata only, never includes payload.

---

## Q2 — SESSION DAEMON

**Architecture: file-lock protocol** (simpler than socket; works across WSL/network mounts; survives reconnect without state sync).

**Socket alternative rejected:** Requires daemon to stay running; WSL/container edge cases; harder crash recovery.

**File structure:**
```
~/.tit/sessions/
  abc123.graph.json    (hot: full cell graph)
  abc123.lock          (PID + epoch; stale if unrefreshed)
  abc123.cold/         (cold: value tombstones only)
    c:ulid.json        ({"witness": [...], "route": [...], "ts": ...})
```

**Wire protocol — tit attach:**
```bash
tit attach <key>
```
1. CLI writes ~/.tit/sessions/<key>.lock: `{pid: $, epoch: now, op: "attach"}`
2. Waits for daemon to drop exclusive lock (or refreshes own every 500ms)
3. Reads ~/<key>.graph.json, gets current cell_ref pointers
4. Daemon sees lock → reloads graph if stale

**tit out -1:**
```bash
tit out -1  # query last output cell
```
```json
→ daemon returns: {"cell_ref": "cell://abc123/c:ULID", "value": {...}, "from": "hot"}
```

**Crash recovery:**
- Daemon dies → .graph.json + .cold/ survive on disk
- Next `tit attach` sees stale .lock (PID not running)
- CLI refreshes graph from disk, resumes
- Daemon on restart re-reads .lock timestamps; drops locks >5m old

**Tombstone lifecycle:**
- **Hot → Cold:** Cell unreferenced for 1000 ops OR 10min → move value to .cold/, keep cell_ref index
- **Cold → Tombstone:** After 24h cold → delete .cold/c:ulid.json, keep witness + route metadata in .graph.json
- **Never dies:** Witness chain (lineage), route metadata, session key

---

**Claude Haiku 4.5**

=== ANSWER 2 — kimi ===
# ROUND 4 — kimi

## Q1 — MCP ERGONOMICS

**Tiers.** Atomic: `tit.jwt_parse`, `tit.base64_encode`, `tit.sha256`, … (~30 thin tools). Pipe: `tit.pipe` (batch edges, one call). Introspection: `tit.cells`, `tit.witness`, `tit.refs`.

**Envelope** (every atomic call):

```json
{
  "cell_ref": "s9f2:c014",
  "value": {"header": {"alg": "HS256", "typ": "JWT"},
            "payload": {"sub": "1234", "exp": 1893456000},
            "signature": "SflKxw…", "valid_exp": false},
  "witness": ["native:jwt-parse@1.4.0"],
  "route": []
}
```

`route` is **empty when native** — the default path costs zero bytes. Each provider hop appends one short code: `["mcp:fs"]`. Never objects, never payloads.

**Input schema** — every input param accepts a literal or a ref:

```json
{"input": {"oneOf": [{"type": "string"},
                     {"type": "object", "required": ["$ref"]}]}}
```

**cell_ref syntax:** `<session>:<cell>[#json-pointer]` — `s9f2:c014#payload`. `@last` = newest cell in session.

**Chaining** — refs resolve daemon-side; values never cross the wire:

```
tit.jwt_parse      {token:"eyJ…"}                       → s9f2:c014
tit.base64_encode  {input:{"$ref":"s9f2:c014#payload"}} → s9f2:c015
tit.sha256         {input:{"$ref":"s9f2:c015"}}         → s9f2:c016
```

Resolution rules: deref at EFFECT time only; `w(out) = w(in) ∪ {tool@ver}`; dangling ref → `{"error":"dangling_ref","ref":"s9f2:c099"}`. `tit.pipe` submits all three edges in one call, returns `{"cell_ref":"s9f2:c016","edges":3}`.

## Q2 — THE UNSTATED DAEMON

**Unix socket, not file-lock.** Locks give mutual exclusion but no request/reply, no push for `attach`, no crash detection. `~/.tit/titd.sock` + `flock` on `titd.lock` guarantees exactly one daemon. CLI and MCP shim are thin clients speaking NDJSON:

```json
→ {"op":"attach","session":"s9f2","since_edge":12}
← {"op":"edge","edge":13,"cell":"c015","diff":{…}}        (streamed)
→ {"op":"out","session":"s9f2","ref":"@last"}
← {"value":"9f86d081…","witness":["native:sha256@1.4.0"],"route":[]}
```

`tit attach` = the streaming op; `tit out -1` = one-shot. MCP server = ~50-line stdio↔socket adapter: spawn/kill freely — three clients, one daemon, one graph.

**Durability:** every EFFECT is appended to `~/.tit/sessions/<key>.journal.jsonl` *before* the reply is sent; `graph.json` is a checkpoint every N edges.

**Crash recovery:** connect fails → client auto-spawns `titd` → daemon loads `graph.json`, replays the journal tail, re-binds the socket; client retries once. Who notices: the retried response carries `"route":["recovered"]` — cheap, explicit, in-band.

**Retention:** hot = resident in daemon memory. Cold = idle 10 min or memory pressure → flushed to `graph.json`, evicted; refs still resolve via lazy reload (transparent). Tombstone = `tit forget <ref>` or TTL → value dropped, keeps `{cell_ref, sha256, witness[], route[], ts}` — enough to verify a claim without the data. **Never dies:** witness chains and tombstone headers — provenance is the audit trail; deleting it would make facts indistinguishable from claims.

— Kimi

<!-- === END ANSWER — session transcript may follow below === -->

=== ANSWER 3 — opencode (GLM-5.3) ===
[0m
> build · glm-5.3
[0m
[0m$ [0mls -la; ls ../ 2>/dev/null | head -20
total 28
drwxrwxr-x 2 eileen eileen 4096 Aug 27 21:40 .
drwxrwxr-x 3 eileen eileen 4096 Aug 27 21:40 ..
-rw-rw-r-- 1 eileen eileen 2837 Aug 27 21:40 r4a-claude.md
-rw-rw-r-- 1 eileen eileen 3571 Aug 27 21:41 r4a-kimi.md
-rw-rw-r-- 1 eileen eileen   29 Aug 27 21:40 r4a-opencode.md
-rw-rw-r-- 1 eileen eileen 2554 Aug 27 21:40 r4a-prompt.md
-rw-rw-r-- 1 eileen eileen 3014 Aug 27 21:40 run-r4a.sh
ds-r3.json
r1-claude.md
r1-kimi.md
r1-opencode.md
r2-claude.md
r2-kimi.md
r2-opencode.md
r2-prompt.md
r3-claude.md
r3-deepseek.md
r3-kimi.md
r3-opencode.md
r3-prompt.md
r4
run-r2.sh
run-r3.sh
seed.md
[0m
[0m→ [0mRead run-r4a.sh
[0m→ [0mRead r4a-opencode.md
**Q1 — MCP ERGONOMICS**

Three tiers, one envelope. **atomic** (12): `tit.jwt_parse`, `tit.sha256`, `tit.md5`, `tit.a64_encode/decode`, `tit.json_to_yaml`, `tit.yaml_to_json`, `tit.cron_parse`, `tit.regex_parse`, `tit.subnet_calc`, `tit.uuid_v4`, `tit.passgen` — plain-arg schemas; every arg accepts a literal **or** `{"$ref":...}`. **pipe**: `tit.pipe({steps:[{tool,args}]})`. **introspection**: `tit.cells({since,q})`, `tit.witness({cell})`, `tit.health()`.

`tit.jwt_parse({token})` returns exactly:

```json
{"cell":"$c:9f2","tool":"tit.jwt_parse@1",
 "value":{"header":{"alg":"HS256","typ":"JWT"},
          "claims":{"sub":"u1","exp":1798761600},"sig":"verified:HS256"},
 "witness":["w($c:9e1)","t:jwt_parse@1"],
 "route":"native"}
```

**Chaining = refs, not values.** cell_ref syntax `$c:<4hex>` (session-scoped), `$c:last` = newest cell, `$c:9f2.claims` = JSONPath into value. The chain ships 30 bytes, not 2KB:

```json
tit.a64_encode({b:{"$ref":"$c:9f2.claims"}})  → cell $c:9f3
tit.sha256({d:{"$ref":"$c:9f3"}})             → witness ["w($c:9f2)","t:a64_encode@2","t:sha256@3"]
```

Daemon resolves refs server-side; unresolved ref → error *cell* (provenance survives failure). Witness union composes free — the digest is a fact.

**route stays cheap:** default is the 6-byte string `"native"`. It expands to an array only when routing was interesting: `"route":[{"try":"native","err":"no impl"},{"try":"mcp","ok":1,"ms":41}]`. You pay for route only when health did.

**Q2 — THE DAEMON**

**Unix socket** `$XDG_RUNTIME_DIR/tit.sock`, JSONL frames. File-lock rejected: locks give exclusion, not messaging — `attach` needs streaming deltas; lockfile+spool is a socket rebuilt badly. One `flock`'d `~/.tit/daemon.pid` (pid+boot_id) elects the singleton.

```json
→ {"op":"call","tool":"tit.a64_encode","args":{"b":{"$ref":"$c:9f2.claims"}}}
← {"ok":1,"cell":"$c:9f3","value":"eyJzdWIi...","witness":["w($c:9f2)","t:a64_encode@2"],"route":"native"}
→ {"op":"attach","session":"proj/r4","since":9}
← {"op":"delta","cells":[["$c:9f3","tit.a64_encode"]]}
→ {"op":"out","n":-1}
← {"op":"result","cell":"$c:9f3","value":"eyJzdWIi..."}
```

CLI and MCP servers are the same thin client: `tit <cmd>` ≡ `{"op":"call",...}`.

**Crash recovery:** the daemon is a cache, not the store. Each session = append-only `sessions/<key>.wal`, fsync per op, compacted to `<key>.graph.json` per 1k edges. Daemon dies → clients see EPIPE. Every connect runs ensure-daemon: connect → fail → flock pidfile → stale (pid dead / boot_id mismatch) → fork → replay WALs → serve. First flock winner becomes daemon; losers just connect. Sessions lost nothing — the next client notices within its first 50ms.

**Retention:** hot (memory+WAL) while held or touched <24h → cold (compacted graph.json, values inline, telemetry→counters) at 24h idle or >10k cells → tombstone (drop value+args; keep `cell`, `tool`, `edges`, `blake3(witness)`) on `tit forget`, ephemeral cells at detach, or cold+unreferenced 30d. **Never dies:** cell ids, edges, tool names, witness digests. Payloads rot; the quilt doesn't.

— GLM-5.3 (Z.ai)
