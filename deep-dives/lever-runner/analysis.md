# Lever Runner — Deep Dive Analysis

> **Repository:** [SuperInstance/lever-runner](https://github.com/SuperInstance/lever-runner)
> **Version studied:** v1.0.0 (pyproject) / v0.4.0 (package)
> **License:** MIT
> **Date:** 2026-08-03
> **Analyst:** Slackwater Cognition Architecture research

---

## 1. What It Does

**Post-inference command executor.** A token-lean AI operator that runs pre-approved shell commands by intent, not by tool schemas.

Lever Runner inverts the standard AI-shell-assistant pattern. Instead of sending your terminal context to a cloud LLM and letting it synthesize shell commands, Lever Runner asks the LLM to do one cheap thing — compress a user request into a 3-8 word intent phrase — then matches that phrase against a local vector database of pre-approved commands. The LLM never sees your filesystem, environment variables, or shell history.

**The core loop:**

```
User types:  "check disk usage on the server"
     ↓
LLM compresses to:  "show disk usage"         (~70 tokens total)
     ↓
Vector search finds:  "df -h"                 (local, zero tokens)
     ↓
Sandbox executes:  df -h                     (pre-approved, trust-scored)
```

**Key metric:** ~70 tokens per query (vs. 2,000-5,000 for Copilot CLI / Warp / Cursor). In passthrough mode: 0 tokens.

---

## 2. Architecture — How Intent-Based Execution Works

### 2.1 The Three-Gate Pipeline

The defining architectural choice. Every user request passes through three sequential gates, each cheaper than the last. Most queries never reach the expensive LLM gate.

```
┌──────────────────────────────────────────────────────┐
│                    USER REQUEST                       │
│              "check disk usage on server"             │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│  GATE 1: Rust Fastloop Guard (~50µs)                 │
│  Unix domain socket → Rust daemon                    │
│  - Rate limiting (per sandbox)                        │
│  - Shell metacharacter detection                      │
│  - Failure cache (known-bad inputs blocked instantly) │
│  Falls back to Python FastLoopInterceptor (~200µs)   │
│  if Rust daemon unavailable                          │
└──────────────────┬───────────────────────────────────┘
                   ↓ (if passes)
┌──────────────────────────────────────────────────────┐
│  GATE 2: Python Cache + Embedding (~200µs - 7.6ms)   │
│  - Embedding cache (44% hit rate in production)      │
│  - LanceDB cosine similarity search                  │
│  - Trust score gating (min threshold = 40)           │
│  - Similarity floor check (default 0.55)             │
└──────────────────┬───────────────────────────────────┘
                   ↓ (if cache miss)
┌──────────────────────────────────────────────────────┐
│  GATE 3: LLM Intent Extraction (~500ms)              │
│  System prompt: ~58 tokens                           │
│  User message: ~10 tokens                            │
│  LLM output: ~8 tokens (the intent phrase)           │
│  The LLM sees ONLY the phrase — no shell, no files   │
│  Backend chain: primary → fallback → passthrough     │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│  VECTOR SEARCH + SANDBOX EXECUTION                    │
│  LanceDB cosine top-k → best match                   │
│  Per-session sandbox (/tmp/lever-runner/<id>/)       │
│  Restricted env (whitelisted vars only)               │
│  Resource limits (CPU, memory, timeout=30s)           │
│  Process-group kill on timeout                        │
│  Trust score update (±Δ based on success/failure)    │
└──────────────────────────────────────────────────────┘
```

### 2.2 Core Components

| Component | File | Responsibility |
|-----------|------|----------------|
| **Orchestrator** | `orchestrator.py` | Single dispatcher: `do()`, `teach()`, `status()`, `list_commands()`. Called by CLI, bot, and HTTP API. |
| **Intent Extractor** | `intent_extractor.py` | LLM-based phrase compression + arg extraction. Supports 5 backends (passthrough, ollama, openai, deepinfra, minimax) with automatic fallback chain. |
| **Command Store** | `store.py` | LanceDB-backed vector store. Per-chat isolation. Three embedding methods (sentence-transformers, position-aware hash, pure hash). Trust scoring with success/failure tracking. |
| **Executor** | `executor.py` | Sandboxed command execution. Per-session dirs, restricted PATH, resource limits, process-group kill, metacharacter validation. |
| **Fastloop Bridge** | `fastloop_bridge.py` | Rust UDS daemon bridge with Python fallback. Sub-ms validation: rate limiting, structural checks, failure cache. |
| **HTTP API** | `http_api.py` | `POST /run`, `POST /teach`, `GET /status`, `GET /healthz`. Loopback-only by default. Bearer auth support. Rate limited. |
| **Telegram Bot** | `bot.py` | Full conversational interface: `/do`, `/teach`, `/status`, `/commands`, `/stats`. Per-chat isolation. User allowlist. |
| **Auto-Promote** | `auto_promote.py` | Hourly cron: promote high-success commands, rewrite failing ones via remote LLM. Self-improvement loop. |
| **CUDA Backend** | `cuda_backend.py`, `cuda_kernels.py` | GPU-accelerated vector search (torch/cupy/pycuda/ctypes fallback chain). 2.6x faster embedding on RTX 4050. |
| **Export/Import** | `seed_export.py`, `seed_import.py`, `export_nail.py` | JSONL skill packs, shell aliases, pincherOS `.nail` format. Portable command libraries. |

### 2.3 Data Flow

```
                   ┌─────────┐
                   │  User   │
                   │ request │
                   └────┬────┘
                        │
           ┌────────────┼────────────┐
           ↓            ↓            ↓
      ┌─────┐     ┌─────┐     ┌─────┐
      │ CLI │     │ Bot │     │ HTTP│
      └──┬──┘     └──┬──┘     └──┬──┘
         │            │            │
         └────────────┼────────────┘
                      ↓
              ┌───────────────┐
              │ Orchestrator  │
              │   do()        │
              └───────┬───────┘
                      │
         ┌────────────┼────────────┐
         ↓            ↓            ↓
   ┌──────────┐ ┌───────────┐ ┌──────────┐
   │ FastLoop │ │ Intent    │ │ Command  │
   │ Bridge   │ │ Extractor │ │ Store    │
   │ (Gate 1) │ │ (Gate 3)  │ │ (Gate 2) │
   └──────────┘ └───────────┘ └──────────┘
                      │            │
                      ↓            ↓
              ┌───────────────────────┐
              │  Executor (sandbox)   │
              │  + trust update       │
              └───────────────────────┘
```

### 2.4 Embedding Strategy

Three methods, configurable via `EMBEDDING_METHOD`:

| Method | Dimensions | Latency | Accuracy | Dependencies |
|--------|-----------|---------|----------|-------------|
| `sentence_transformers` | 384 | 6.7ms (CPU) / 2.6ms (GPU) | Best (semantic) | `sentence-transformers`, HuggingFace model (~80MB) |
| `position_aware` | 64 | ~1µs | 44% top-1 | None (hashlib only) |
| `hash` | 64 | ~6µs | 0% top-1 (baseline) | None (hashlib only) |

The position-aware hash embedding is a notable innovation — it achieves 44% accuracy with zero dependencies and sub-microsecond latency, making it viable for embedded/edge deployments where even sentence-transformers is too heavy.

### 2.5 LLM Backend Chain

```
Primary backend (e.g. "ollama")
  ↓ on retryable error (timeout, 429, 5xx)
Fallback 1 (e.g. "deepinfra")
  ↓ on retryable error
Fallback 2 (e.g. "openai")
  ↓ on any error
Passthrough (raw request = intent phrase, 0 tokens)
```

The chain **always terminates at passthrough** — a complete provider outage degrades gracefully rather than hanging.

### 2.6 Trust Scoring System

```
New command:     trust = 50 (TRUST_NEW)
Success:         trust += 1.5 (TRUST_BUMP)
Failure:         trust -= 4.0 (TRUST_PENALTY)
Auto-promote:    if success_count > 20 and trust < 90: trust += 10
Rewrite:         if trust < 30 and failures >= 5: ask LLM for fix
Minimum to run:  trust >= 40 (min_trust floor)
Maximum:         100 (hard cap)
```

The asymmetry (±1.5 success vs. -4.0 failure) means a command needs ~3 successes to recover from one failure — conservative, favoring safety.

---

## 3. Key Innovation — Why This Is Better Than Tool-Calling Schemas

### 3.1 The Token Economics Problem

Standard AI shell tools (Copilot CLI, Warp, Cursor, OpenInterpreter) ship the **entire tool schema** in every prompt:

```
Typical tool-calling prompt:
  - System prompt with role instructions      ~200 tokens
  - Tool schemas (20-50 tools × ~50 tokens)   ~1,500 tokens
  - Conversation history                       ~300 tokens
  - User message                               ~20 tokens
  ─────────────────────────────────────────────
  Total per query                              ~2,000-5,000 tokens
```

Lever Runner's prompt:

```
  - System prompt (compress to phrase)         ~58 tokens
  - User message                               ~10 tokens
  - LLM output                                 ~8 tokens
  ─────────────────────────────────────────────
  Total per query                              ~76 tokens
```

**28× fewer tokens.** At 1,000 commands/day on gpt-4o, that's $675/month vs. ~$0.05/month.

### 3.2 The Security Model

The fundamental insight: **the LLM cannot inject commands because it never produces commands.** It produces a 3-8 word phrase. The command is looked up from a pre-approved table by cosine similarity. Even if the LLM is completely compromised via prompt injection:

- It can only output a phrase (validated: lowercase, alphanumeric + spaces, max 8 words)
- The phrase must match a pre-approved command above the similarity floor (0.55)
- The matched command must be above the trust floor (40)
- The command runs in a sandbox with restricted env, resource limits, and hard timeout
- Arguments are validated against `^[a-zA-Z0-9._-]+$` — shell metacharacters are impossible

This is a **structural** security property, not a policy. No amount of prompt engineering can bypass it because the LLM's output channel is too narrow to encode a shell injection.

### 3.3 The Compilation Analogy

Lever Runner treats LLM understanding as a **compile-time** concern, not a **runtime** concern:

```
Traditional agent:    LLM → tool call → execute → hope
Copilot agent:        LLM → suggestion → approve → pray
Lever Runner:         teach once → compile (embed) → verify → run forever
```

- **Compile time** (`teach`): LLM helps map intent → command. Human approves. Embedding is computed and stored.
- **Runtime** (`do`): Vector search finds the nearest pre-approved command. Zero LLM cost.

This is directly analogous to how a compiler works: the expensive type-checking and optimization happen once at compile time; runtime execution is deterministic and fast.

### 3.4 Self-Improvement Without Neural Networks

The `auto_promote.py` cron implements a learning loop without any model training:

1. **Promote winners**: Commands with 20+ successes get trust boosts (+10)
2. **Surface failures**: Low-trust failing commands get flagged
3. **Rewrite** (opt-in): Remote LLM proposes corrected commands for failures

This is reinforcement learning via database operations — the vector store accumulates experiential knowledge without gradient updates.

---

## 4. Integration Opportunities for Slackwater Cognition Architecture

### 4.1 Local Thinker → Lever Runner for Lightweight Action Execution

**High fit.** The Local Thinker's role is fast, cheap cognitive processing close to the data. Lever Runner's three-gate architecture is purpose-built for exactly this:

| Local Thinker Need | Lever Runner Capability |
|---|---|
| Minimal token expenditure | ~70 tokens/query (or 0 in passthrough) |
| Fast response time | Gate 1: 50µs, Gate 2: 7.6ms, Gate 3: 500ms |
| Safe action execution | Sandboxed, trust-scored, metacharacter-validated |
| Learns from experience | Trust scoring auto-promotes successful commands |
| Works offline | Passthrough mode requires zero API keys |
| Multiple surfaces | CLI, HTTP API, Telegram bot — all calling same orchestrator |

**Recommendation:** Embed Lever Runner's orchestrator pattern (not the full server) directly into the Local Thinker. The `orchestrator.py` module is 150 lines and has zero hard dependencies beyond the store and executor. The FastLoopBridge can be reused as-is for the Local Thinker's input validation layer.

### 4.2 Algorithmic Action Layer → Lever Runner Intent Mapping

**Strong structural parallel.** The cognition architecture's "lean → action selection" pipeline maps directly onto Lever Runner's intent → command pipeline:

```
Cognition Architecture          Lever Runner
─────────────────────          ────────────
Perception (input)       →     User request
Lean processing          →     FastLoop validation (Gate 1)
Intent classification    →     LLM phrase extraction (Gate 3)
Action selection         →     Vector search + trust gating (Gate 2)
Action execution         →     Sandbox executor
Feedback                 →     Trust score update
```

**The action policy table** in the cognition architecture is isomorphic to Lever Runner's command table:

| Cognition Architecture | Lever Runner Equivalent |
|---|---|
| Action policy table | `commands` LanceDB table |
| Action confidence threshold | Trust score floor (40) |
| Action success/failure tracking | `success_count`, `failure_count` |
| Action promotion/demotion | `auto_promote.py` trust dynamics |
| Pre-approved action set | Seed pack (67 commands) |
| Parameterized actions | `{{param}}` template substitution |

**Recommendation:** Use Lever Runner's store schema as the template for the cognition architecture's action policy table. The trust dynamics (asymmetric ±, auto-promote thresholds) are well-tuned through production use.

### 4.3 Does This Replace the Current Worker API Call Pattern?

**Partial replacement, not full.**

**What it can replace:**
- Shell command execution from the Local Thinker (the `exec` tool path)
- System administration actions (disk, processes, docker, git, networking)
- Any deterministic, repeatable action that can be pre-approved

**What it cannot replace:**
- Complex multi-step reasoning that requires full LLM context
- Actions that need to synthesize novel commands not in the table
- Actions requiring deep context awareness (file contents, code semantics)
- The main agent's tool-calling for dynamic, stateful operations

**Recommendation:** Deploy Lever Runner as a **complementary action layer** alongside the existing Worker API pattern. The Local Thinker routes to Lever Runner for known-safe operations and falls back to the full tool-calling path for novel ones. Over time, successful novel operations get `taught` to Lever Runner, expanding its pre-approved repertoire.

### 4.4 Integration Architecture

```
┌─────────────────────────────────────────────────────┐
│              Slackwater Cognition                    │
│                                                     │
│  ┌─────────────┐         ┌─────────────────────┐   │
│  │ Local        │ intent  │ Lever Runner        │   │
│  │ Thinker      │───────►│ Embedded Instance   │   │
│  │              │         │                     │   │
│  │ - FastLoop   │         │ - Command Store     │   │
│  │   validation │         │ - Trust Scoring     │   │
│  │ - Lean       │         │ - Sandbox Exec      │   │
│  │   processing │         │ - Auto-Promote      │   │
│  └──────┬──────┘         └─────────┬───────────┘   │
│         │                          │                │
│         │    ┌─────────────────────┘                │
│         ↓    ↓                                      │
│  ┌──────────────────┐                              │
│  │  Algorithmic     │     ┌──────────────────┐     │
│  │  Action Layer    │◄───►│  Cloud Thinker   │     │
│  │                  │     │  (Worker API)    │     │
│  │ - Policy table   │     │  - Complex ops   │     │
│  │ - Trust scores   │     │  - Novel actions │     │
│  │ - Intent → cmd   │     │  - Deep context  │     │
│  └──────────────────┘     └──────────────────┘     │
└─────────────────────────────────────────────────────┘
```

---

## 5. Code Quality Assessment

### 5.1 Verdict: Production-Ready with Caveats

**Strengths:**

- **Clean separation of concerns.** Each module has a single, well-documented responsibility. The orchestrator is a thin dispatcher; the store handles only data; the executor handles only sandboxing.
- **Comprehensive test coverage.** 160 tests covering three-gate cascade, parameterized commands, trust dynamics, auto-promote, bot handlers, HTTP API, fallback chains, and injection prevention. The smoke test is a 600-line end-to-end integration test.
- **Defensive security.** Shell metacharacter validation at two layers (FastLoop + executor). Restricted environment variables. Resource limits. Per-session sandboxes. Process-group kill. Argument validation for templates. The security model is structural, not advisory.
- **Graceful degradation.** LLM backend chain always terminates at passthrough. Rust fastloop falls back to Python. GPU falls back to CPU. Every dependency has a zero-cost fallback.
- **Excellent documentation.** README, BENCHMARKS, INSIGHT essay, doctor health check, quickstart guide, future integration doc, contributing guide. The INSIGHT.md essay alone is worth reading for its architectural analysis.
- **Type annotations throughout.** `from __future__ import annotations` everywhere. Dataclasses for all return types. Ruff with strict rules including `S` (security).

**Caveats:**

- **`shell=True` in executor.** The `subprocess.Popen(command, shell=True, ...)` is intentional (the design is to run shell commands) but is a code smell in security-critical contexts. The metacharacter validation mitigates this, but a future version should consider `shlex.split()` + `shell=False` for non-pipeline commands.
- **LanceDB as the sole vector store.** LanceDB is relatively new and has rough edges (pagination semantics vary by version, rename not supported, read-after-write races). The `read_consistency_interval=0` workaround works but is fragile.
- **Python only.** The Rust fastloop-guard is a thin validation layer. For true sub-ms latency in the cognition architecture, the full pipeline (embed + search + execute) would need a Rust port.
- **Single-user assumption.** The bot uses a single Telegram bot token with user allowlist. No multi-tenant auth, no per-user rate limiting at the bot layer (though per-chat isolation exists).
- **`init_db.py` at repo root.** The seed file is outside the package, making wheel installs skip the seed pack. The store has a `_seed_from_init_db()` fallback that silently no-ops if `init_db` isn't importable.

### 5.2 Metrics

| Metric | Value |
|---|---|
| Source files (src/) | 16 Python modules |
| Total LOC (src/) | ~3,200 |
| Test files | 8 test modules |
| Test LOC | ~1,800 |
| Smoke test | 600+ LOC, 50+ assertions |
| Dependencies (core) | 7 (lancedb, sentence-transformers, pyarrow, python-dotenv, python-telegram-bot, httpx, requests) |
| Dependencies (dev) | 6 (pytest, pytest-asyncio, ruff, requests, build, twine) |
| Ruff rules enabled | 10 categories (E, F, W, I, B, UP, N, S, C4, RET) |
| Seed commands | 67 (system, docker, git, networking, file ops) |
| Skill packs | 5 (system, devops, git, security, python) |

---

## 6. Specific Patterns for Cognition

### 6.1 Intent → Action Mapping

**Pattern:** Natural language → compressed phrase → vector search → ranked candidates → trust-gated selection → execution.

**Cognition parallel:** The "lean" processing step in the cognition architecture. The Local Thinker perceives input, classifies intent via fast heuristics (FastLoop), then selects an action from the policy table via similarity matching.

**Key insight:** The LLM is used for **compression**, not generation. It reduces a variable-length natural language input to a fixed-format, validated output (3-8 word lowercase phrase). This is the cheapest possible use of an LLM — and it's the only use.

**For the cognition architecture:** The Local Thinker should use the same pattern. LLM calls should be limited to intent compression (mapping rich input to a standardized action key). The actual action selection should be a local operation (vector search or hash lookup).

### 6.2 Pre-Approved Commands as Action Policy

**Pattern:** A database of `(intent_phrase, command, trust_score)` tuples. Commands are added by `teach()` (human or LLM-assisted). Commands are selected by cosine similarity. Commands are filtered by trust score. Commands are updated by execution feedback.

**Cognition parallel:** The action policy table in the cognition architecture. Actions are pre-defined with associated confidence values. The policy is not a neural network — it's a lookup table with experiential feedback.

**Key insight:** Trust scoring creates a **natural curriculum**. New actions start at trust=50 (uncertain). Successful executions promote them. Failures demote them aggressively (asymmetric penalty: +1.5/-4.0). The system naturally converges toward high-trust, reliable actions without any model training.

**For the cognition architecture:**
```
Action table schema (proposed):
  action_id: UUID
  trigger_pattern: str          # the "intent phrase"
  action_spec: JSON             # the "command" (generic action, not just shell)
  confidence: float (0-100)     # the "trust score"
  success_count: int
  failure_count: int
  embedding: float[dim]         # for similarity search
  last_invoked: timestamp
  created_at: timestamp
```

### 6.3 Token-Lean Operation

**Pattern:** The entire LLM budget per action is ~76 tokens (58 system + 10 user + 8 output). In passthrough mode: 0 tokens. The system is designed to minimize LLM calls, not just minimize per-call tokens.

**The three-gate cascade** ensures most queries never reach the LLM:
- Gate 1 (template match): exact-match queries → 0 tokens
- Gate 2 (embedding cache): 44% of remaining → 0 tokens
- Gate 3 (LLM): only novel queries → 76 tokens

Combined: ~56% of queries cost zero tokens, the rest cost ~76 tokens each.

**Cognition parallel:** The Local Thinker must operate under strict token budgets. The three-gate pattern is directly applicable:

```
Gate 1: Pattern match (exact triggers, cached responses)     — 0 tokens
Gate 2: Embedding cache (similar past situations)             — 0 tokens
Gate 3: LLM compression (novel situations only)               — ~76 tokens
```

**For the cognition architecture:** Implement a three-gate cascade for every Local Thinker decision point. Track cache hit rates. Set a target of >50% of decisions resolved at Gate 1 or 2.

### 6.4 The FastLoop Pattern — Sub-ms Validation

**Pattern:** Before any expensive operation (LLM call, vector search), validate the input cheaply. The FastLoop checks rate limits, structural validity, and failure cache in under 1ms.

**Key insight:** The failure cache is the most valuable component. After seeing a bad input once, the system never processes it again. This is **negative learning** — the system gets faster as it accumulates knowledge of what doesn't work.

**For the cognition architecture:** The Local Thinker should maintain a failure cache for actions that produced errors. When the same (or similar) trigger occurs, the failure cache short-circuits the evaluation, saving both tokens and latency.

### 6.5 The `.nail` Export Pattern — Portable Cognition

**Pattern:** Export the entire action table (intent phrases, commands, embeddings, trust scores) as a portable archive. Import on another device. Same muscle memory, different hardware.

**Key insight:** Cognition is portable. If the Local Thinker has learned effective actions on one deployment, that knowledge should transfer to another. The embedding vectors + trust scores are the distilled experience.

**For the cognition architecture:** Implement export/import for the action policy table. The `.nail` format (tar.zst with SQLite + manifest + embeddings) is a good template. This enables:
- Deploying a pre-trained Local Thinker to new nodes
- Sharing learned policies between instances
- Version-controlling cognition state

---

## 7. Risks and Limitations

### 7.1 Embedding Quality Ceiling

The default `all-MiniLM-L6-v2` model (384 dims, 80MB) achieves good accuracy for English command phrases but struggles with:
- Multi-language input (would need `paraphrase-multilingual-MiniLM-L12-v2`, 470MB)
- Domain-specific jargon (specialized terms may not embed well)
- Very short queries (1-2 words may not have enough signal)

**Mitigation:** The position-aware hash embedding (64 dims, 0 dependencies, 44% accuracy) is a viable fallback for edge deployments where even MiniLM is too heavy.

### 7.2 LanceDB Maturity

LanceDB is the sole vector store. It's relatively new (v0.20+):
- No rename operation (requires create-copy-drop)
- Pagination semantics vary by version
- Read-after-write races (mitigated by `read_consistency_interval=0`)
- `to_pandas()` requires pyarrow's pandas shim

**Mitigation:** The store interface is thin enough (~200 LOC) that swapping to Qdrant, ChromaDB, or a custom SQLite+numpy implementation would be feasible.

### 7.3 Single-Action Granularity

Lever Runner executes one command per request. It cannot:
- Chain commands (run A, then B if A succeeds)
- Conditionally branch (if disk > 80%, do X, else do Y)
- Maintain state between commands
- Compose multi-step workflows

**For the cognition architecture:** This is acceptable for the action execution layer (one action per decision), but the Local Thinker's planning layer needs its own composition mechanism above Lever Runner.

### 7.4 No Native Multi-User Support

Per-chat isolation exists but shares a single bot token and a single process. True multi-tenancy (multiple users, separate auth, separate rate limits) would require:
- Per-user authentication (not just per-chat)
- Per-user vector stores (or partitioned tables)
- Per-user trust policies

---

## 8. Recommendation Summary

| Question | Answer | Confidence |
|---|---|---|
| Can the Local Thinker use Lever Runner for lightweight action execution? | **Yes** — embed orchestrator pattern directly | High |
| Can the algorithmic action layer map to Lever Runner intents? | **Yes** — direct isomorphism to action policy table | High |
| Does this replace the current Worker API call pattern? | **Partially** — complements, not replaces | Medium |
| Is the code production-ready? | **Yes, with caveats** — security-solid, well-tested, LanceDB dependency is the main risk | High |
| Should we use the code directly or re-implement the pattern? | **Hybrid** — use the pattern, vendor the orchestrator + store, swap the executor | Medium |

---

## 9. Files Studied

### Source (`src/lever_runner/`)
- `__init__.py`, `__main__.py` — package + entry point
- `cli.py` — full CLI with subcommands (do, teach, status, doctor, stats, export, import)
- `orchestrator.py` — central dispatcher: `do()`, `teach()`, `status()`, `list_commands()`
- `intent_extractor.py` — LLM phrase compression with 5 backends + fallback chain
- `store.py` — LanceDB command store with 3 embedding methods + parameterized commands
- `executor.py` — sandboxed command execution with resource limits + metacharacter validation
- `fastloop.py` — Python FastLoop interceptor (rate limit, failure cache, structural validation)
- `fastloop_bridge.py` — Rust UDS daemon bridge with Python fallback
- `bot.py` — Telegram bot with /do, /teach, /status, /commands, /stats
- `http_api.py` — HTTP API with /run, /teach, /status, /healthz + rate limiting + auth
- `auto_promote.py` — hourly cron for trust promotion + LLM-assisted command rewriting
- `doctor.py` — pre-flight health check (11 checks)
- `token_logger.py` — append-only JSONL token accounting with rotation
- `benchmark.py` — 20-task benchmark suite (target: <200 tokens/command)
- `cuda_backend.py` — GPU vector search (torch/cupy/pycuda/ctypes/CPU fallback chain)
- `cuda_kernels.py` — CUDA C kernel source strings + hand-written PTX
- `export_nail.py` — pincherOS .nail format export (tar.zst + SQLite + embeddings)
- `seed_export.py` — JSONL skill pack export
- `seed_import.py` — JSONL skill pack import

### Tests (`tests/`)
- `conftest.py` — shared fixtures (mock Telegram, env cleanup)
- `test_three_gate.py` — end-to-end three-gate cascade tests
- `test_fastloop.py` — FastLoop interceptor unit tests
- `test_params.py` — parameterized command tests (placeholder detection, arg validation, substitution)
- `smoke.py` — 600+ LOC end-to-end integration test (20 test sections, 50+ assertions)
- `helpers.py`, `test_bot.py`, `test_embeddings.py`, `test_export_nail.py`, `test_cuda_backend.py`, `test_cli_subcommands.py`, `test_fastloop_bridge.py`

### Configuration
- `pyproject.toml` — hatchling build, ruff (10 rule categories), pytest config
- `init_db.py` — 67-command seed pack
- `packs/` — 5 skill packs (system, devops, git, security, python)
- `.env.example`, `.env.minimal` — environment configuration
- `Dockerfile`, `Dockerfile.web`, `docker-compose.yml` — containerization
- `fly.toml` — Fly.io deployment
- `systemd/` — hardened systemd units (NoNewPrivileges, ProtectSystem=strict)

### Documentation
- `README.md` — comprehensive (3,000+ words, architecture diagrams, comparison tables)
- `BENCHMARKS.md` — token economics, latency benchmarks, cost projections
- `CHANGELOG.md` — full version history (v0.1.0 → v1.0.0)
- `TODO.md` — candid v0.5 roadmap with "things I will NOT add" section
- `INSIGHT.md` — two research essays (~12,000 words total) on GPU execution safety
- `docs/QUICKSTART.md`, `docs/FUTURE-INTEGRATION.md`, `docs/BROWSER-STRATEGY.md`
- `CONTRIBUTING.md`, `AGENT.md`, `AGENTS.md`

---

*Analysis complete. See `integration-plan.md` for the concrete integration roadmap and `LEARN.md` for extracted patterns.*
