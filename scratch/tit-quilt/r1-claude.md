# Quilt-Native TIT: Design Submission

## 1. INTEGRATE: TIT Tools → Quilt Opcodes

**Tool → Cell Mapping:**
- **Converters & Crypto** (base64, SHA-256, date-time, etc.): FUNCTION cells with VIEW (input form/clipboard) → EFFECT (output result). State-free, pure transformations.
- **Stateful Tools** (regex tester, JSON formatter): VIEW cells hosting input + output side-by-side; internal state cell tracks current pattern/config via TICK.
- **Tool Picker (fuzzy search)**: BIND opcode at startup — all tool cells indexed by keyword, symbol, category. Live search rewrites BIND weights as you type.
- **TUI Layer**: A VIEW cell observing the cell graph. Routes user keystrokes as EFFECT requests to tool cells; streams EFFECT outputs back as live results. Multiple VIEWs can coexist (CLI is a headless VIEW that chains tool cells via LINK edges).
- **CLI Layer**: EFFECT runner. Composes tool cells as a cell-graph LINK pipeline (e.g., `tit-native base64-decode | url-decode | sha256`); executes headless, no TUI overhead.

## 2. ABSTRACT HIGHER: Quilt's Gain

**TIT Today:** Tool switcher. Each tool is isolated; no chaining, no intermediate inspection, no provenance.

**Quilt Gives TIT:**
- **Composable Pipelines (LINK)**: Chain converters as directed acyclic cell graphs. `base64 → url-decode → sha256` is a single routable graph, not three separate CLI invocations.
- **Witness-Trit Provenance**: Every converted value carries marks: *"this SHA result was computed from this base64-decoded input at 2026-08-27T14:33Z, sourced from clipboard, via browser VIEW."* Auditable, repeatable, linkable back to source.
- **Health-Aware Routing**: Swap local MD5 for a remote hash service without changing the graph structure. LINK health weights let the system choose the cheapest-first path.
- **State as First-Class**: Live tool state (current regex, formatter settings) becomes a cell, observable by other cells. TUI reflects state changes in real-time without polling.

## 3. ENHANCE: One Concrete New Capability

**Multi-View Live Tool-Chain Designer:**

Build a tool pipeline visually in a web VIEW. It becomes a LINK-based cell graph. Type into the web form; the TUI (separate VIEW) streams live intermediate results for each step. Each step is inspectable—click "base64 output" to see the intermediate. Save the chain as a reusable cell template.

**The Difference:** TIT chains are one-shot CLI. Quilt chains are: composable, inspectable at each step, provenanced (which tool, which input, which timestamp, which device), and swappable (replace the local hasher with a routed remote one by health weight). The web VIEW + TUI VIEW both see the same cell graph. No duplicate logic.

---

**Model:** Claude Haiku 4.5
