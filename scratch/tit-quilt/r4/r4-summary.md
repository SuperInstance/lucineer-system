# TIT-R4 — Round 4 Results (the two fault lines)

## Q1 — MCP ERGONOMICS (points 3/2/1)

| Judge | 1st | 2nd | 3rd |
|---|---|---|---|
| claude (Haiku 4.5) | opencode/GLM | kimi | claude |
| deepseek (V4-Flash)* | kimi | claude | opencode/GLM |
| kimi | kimi | opencode/GLM | claude |
| opencode (GLM-5.3) | kimi | opencode/GLM | claude |

**Tally: kimi 11 · opencode/GLM 8 · claude 5 → WINNER: kimi (3 of 4 first places)**

Winning mechanism: `<session>:<cell>[#json-pointer]` refs (e.g. `s9f2:c014#payload`), `oneOf` literal-or-`{"$ref":...}` input schema, deref at EFFECT time only, `w(out) = w(in) ∪ {tool@ver}`, `route: []` when native — zero bytes for the default path. Killer critiques that shaped it: kimi + opencode both caught GLM's flagship-example bug (`"sig":"verified:HS256"` — a parse tool cannot verify an HMAC without a key); opencode + claude both caught claude's `tit.pipe.jwt→b64→sha` as unbuildable (MCP tool lists are statically declared) and the `@cell://` string-prefix as an injection bug. GLM's error-cells (provenance survives failure) and "pay for route only when health did" were named best-in-round ideas but sat 2nd.

## Q2 — THE SESSION DAEMON (points 3/2/1)

| Judge | 1st | 2nd | 3rd |
|---|---|---|---|
| claude | kimi | opencode/GLM | claude |
| deepseek | kimi | opencode/GLM | claude |
| kimi | opencode/GLM | kimi | claude |
| opencode | opencode/GLM | kimi | claude |

**Tally: kimi 10 · opencode/GLM 10 · claude 4 → DEAD HEAT on points; WINNER: kimi on tiebreak**
Tiebreak: both neutral judges (claude, deepseek) put kimi 1st; kimi conceded 1st to its rival while opencode took it for itself; among non-self votes kimi 2–1 opencode. Unanimous: claude's file-lock is the round's one wrong answer ("a socket rebuilt badly" — both rivals + deepseek).

Photo-finish synthesis the judges themselves wrote: **kimi's daemon chassis** (Unix socket + NDJSON, append-only journal-before-reply, auto-spawn, `"route":["recovered"]` in-band marker, lazy cold reload) **+ opencode's hardening** (boot_id in pidfile kills PID-reuse-after-reboot; flock election "first flock winner becomes daemon, losers just connect" resolves the two-client spawn race; fsync-per-op; "the daemon is a cache, not the store"; blake3(witness) tombstones).

## THE BUILD-CRITICAL DECISION — split 2–2, composing into one spec-first gate

- **Durability/truth-location (deepseek + opencode):**
  - deepseek: "the durability contract of the session journal, decided before a single line of protocol code" — "Get it wrong and the 'witness chain' becomes a ceremonial artifact… no amount of clever `@cell://` syntax or `$c:last` sugar will save a toolchain whose history is fiction."
  - opencode: "Decide where truth lives: the append-only WAL on disk is the store; the daemon is a disposable, replayable cache; CLI and MCP shim are thin socket clients — before a single tool, envelope, or schema is written… moving truth out of a live daemon's memory once three MCP clients depend on its resident state is a rewrite wearing a migration's clothes."
- **Cell contract (kimi + claude):**
  - kimi: "The cell contract — cell identity, ref syntax, witness composition rule, and tombstone invariants — must be frozen before line one… the cell contract is the constitution."
  - claude: "Cell reference syntax. This is non-negotiable and locks everything else… Witness chains are immutable; wrong ref syntax means migration hell later."

The two camps are two ends of one gate: WHAT is stored/referenced (cell contract) and WHERE truth lives (WAL-is-the-store). Both are irrevocable once journals hit disk and clients integrate; everything else (transport, retention thresholds, tool roster) is revisable behind them.

## Footnotes (integrity)
- *deepseek (V4-Flash, verified via API response `model` field) mis-signed its verdict "— GLM-5.3 (Z.ai)" — identity bleed from prompt content; content is genuinely independent (it ranked GLM's Q1 answer 3rd, last place).
- opencode's r4a transcript shows it listing the r4 directory before answering (these yards have filesystem access); its design remained materially distinct — noted, not disqualifying.
- kimi's and opencode's r4a answers ran over the 400-word cap; both were marked down for it by at least one judge.
