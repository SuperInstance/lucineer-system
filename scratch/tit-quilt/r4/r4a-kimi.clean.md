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
