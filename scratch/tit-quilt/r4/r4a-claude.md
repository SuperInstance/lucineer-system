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
