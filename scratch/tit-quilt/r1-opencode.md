[0m
> build · glm-5.3
[0m
**TIT/QUILT — every tool a cell, every conversion a derivation.**

**1. INTEGRATE — opcode mapping**

- Converters / hashes / generators → pure FUNCTION cells. `BIND` declares the tool cell (in/out schema, tool id, version); a conversion is `LINK(input_cell → tool_cell)`; `VIEW` renders the derived slot. No `EFFECT` — pure cells only write their own output.
- Headless CLI (`tit convert x`) → `EFFECT` runner: bind argv as a cell, evaluate the subgraph, emit cell-graph JSON, `FORGET` the ephemerals.
- Live-as-you-type → `TICK`: each keystroke ticks the input cell; downstream cells re-derive. Ratatui's reactive loop becomes TICK-driven graph evaluation.
- TUI → one `VIEW` over the graph. Fuzzy tool search = a VIEW filter over the BIND registry. Clipboard = `EFFECT` (it touches the world).

**2. ABSTRACT HIGHER**

- **Composability:** TIT's tools are islands; quilt chains them — `json.fmt → yaml → sha256` is three LINKs evaluated as one subgraph.
- **Provenance:** `w(sha256(x)) = w(x) ∪ {sha256_cell@v}`. A converted value without witness marks is a claim.
- **Routing:** a tool id becomes an interface; implementations are providers — native Rust cell, or MHS `cli`/`http`/`mcp` transport cells. LINK resolves via health-aware weights, ascending dispatch: native first, escalate on failure or health decay. Routing IS linking.
- **Statefulness:** regex/cron tester buffers become persistent cells with telemetry, not TUI-local state.

**3. ENHANCE — provenance pipelines (impossible in terminal TIT)**

```
$ tit pipe 'base64.dec | yaml.load | sha256' --emit graph
{ "value":   "9f2a…",
  "witness": ["stdin@ts", "b64dec@native@1.4",
              "yaml.load@mock@0.9", "sha256@native"],
  "route":   [{"edge":"sha256","tried":["native"],"used":"native"}],
  "graph":   { …cell-graph JSON… } }
```

The output is a rerunnable, auditable derivation: replay it in any render layer (web VIEW, Godot engine VIEW, another host); re-dispatch only edges whose witness versions changed. Terminal TIT returns an answer; quilt-native TIT returns a fact with its receipts.

— glm-5.3
