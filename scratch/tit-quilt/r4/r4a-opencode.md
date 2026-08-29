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
