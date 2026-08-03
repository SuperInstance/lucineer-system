# Pincher — Learning Notes

## Core Mental Model

Think of Pincher as a **spinal cord** for AI agents. When you touch something hot, your hand pulls back before your brain processes the pain. Pincher does this for AI:

1. Intent arrives → embedded into a vector
2. Vector is matched against stored reflexes (semantic, not exact)
3. If the match is strong enough → execute directly (~50ms, $0)
4. If it's novel → the LLM "compiles" a new reflex and stores it

The LLM is not in the hot path. It's a **compiler** that runs once per novel intent and produces a reusable artifact.

## The Three Tiers

| Tier | Similarity | Latency | Cost | What Happens |
|------|-----------|---------|------|--------------|
| Exact | ≥0.80 | ~50ms | $0 | Execute reflex directly |
| Similar | 0.55–0.80 | ~3s | ~$0.001 | Execute with confirmation flag |
| Novel | <0.55 | ~10s | ~$0.01 | LLM compiles new reflex |

## Embedding Strategy

**Two backends, same interface:**

1. **ONNX** (feature flag `onnx`): Real all-MiniLM-L6-v2 model. 384-dim. Semantic understanding.
2. **Hash fallback** (default): SHA-256 trigram + word + global hashing into 384-dim. Deterministic. Zero dependencies. Works offline.

The hash fallback is genuinely clever:
- **Trigrams** capture local character structure
- **Whole words** capture semantic units
- **Global hash** captures overall text identity
- All L2-normalized

It won't match "show running processes" to "list active processes" as well as MiniLM, but for exact and near-exact matches, it works.

## Confidence Model

```
Success: confidence += 0.05 × (1.0 - confidence)  → asymptotic toward 1.0
Failure: confidence -= 0.10 × confidence           → proportional decay
Clamped: [0.05, 0.95]
```

This is a bounded learning signal. A reflex at 0.95 confidence needs ~0 failures to drop to 0.85 (about 2-3 failures). A reflex at 0.50 needs ~5 successes to reach 0.60. The asymmetry (5% up, 10% down) makes the system appropriately cautious.

## The .nail Format

```
crab.nail (tar.zst archive)
├── manifest.json     # Version, fingerprint, checksums
├── reflexes.db       # Complete SQLite database
├── identity.json     # Agent name + preferences
└── config.toml       # Resource thresholds, paths
```

All files verified via BLAKE3. Hardware compatibility scored 0.0–1.0 based on OS, CPU, RAM, GPU, MAC hash.

This is **portable agent identity**. The "crab" (agent state) can move between "shells" (machines).

## Security Layers

1. **Veto engine** (pre-execution): Pattern-based blocking of dangerous commands
   - Blocks: `rm -rf /`, `mkfs`, `dd if=`, `base64 -d | sh`, `eval`, `python -c`, etc.
   - Protects: `/etc`, `/sys`, `/proc`, `/boot`, `/dev`
   - Customizable via TOML

2. **Sandbox** (execution): Bubblewrap isolation with capability tokens
   - Falls back to restricted `Command::new` with `env_clear()`

3. **Immunology** (adaptive): Learns rejection patterns
   - Antigens: PromptInjection, MaliciousAction, ResourceAbuse, StaleReflex
   - Antibodies stored in SQLite, activated on match, decay when inactive

## Key Code Paths

### Teach
```
ReflexEngine::teach(intent, action)
  → embed(intent) → 384-dim vector
  → INSERT INTO reflexes + vec_reflexes
  → confidence starts at 0.5
```

### Do (execute)
```
ReflexEngine::do_command(intent)
  → embed(intent)
  → match_reflex() → Exact/Similar/Novel
  → If Exact: veto check → execute → update confidence → log
  → If Novel: return "no match" (LLM sidecar handles elsewhere)
```

### Match
```
match_reflex(conn, embedder, intent)
  → embed(intent) → query_vec
  → Exact string match check (fast path)
  → sqlite-vec KNN search (top-5)
  → Re-rank with cosine similarity
  → Classify by thresholds
```

## Resource Management

PID controller with 3 states:
- **Normal**: RAM <70%, CPU <60% → full LLM, 4096 tokens
- **Light**: RAM 70-85% or CPU 60-80% → reduced context, skip LLM for high-confidence
- **Critical**: RAM >85% or CPU >80% → reflex-only, no LLM

3-tick hysteresis prevents flapping.

## Graph Routing (Bonus)

The `route/mod.rs` module is a full ternary-weighted graph library:
- Edges carry `+1` (trusted), `0` (neutral), `-1` (adversarial)
- Bellman-Ford, Floyd-Warshall, label propagation, spectral clustering
- Signed modularity scoring
- `RoomGraph` for multi-agent routing

This is fleet-level infrastructure for trust-aware agent networks.

## What's Stubbed

- `pincher compile` — prints messages, doesn't actually compile WASM
- `pincher mature` — prints messages, doesn't actually do adversarial fuzzing
- `pincher publish` — depends on a registry server that doesn't exist
- `wasmtime` feature — declared but no WASM execution implemented

## What Works

- ✅ Reflex engine (teach, match, execute, confidence)
- ✅ SQLite vector storage (sqlite-vec)
- ✅ Hash fallback embeddings (zero-dependency)
- ✅ ONNX embeddings (with `--features onnx`)
- ✅ CLI (status, doctor, teach, do, reflexes, pack, unpack, run, bench)
- ✅ .nail pack/unpack with BLAKE3 verification
- ✅ Veto engine (20+ default rules)
- ✅ JSON-RPC server (Unix domain socket)
- ✅ Built-in reflexes (system.info, file.read, process.list, git.status, etc.)
- ✅ Immune memory (antibody storage and matching)
- ✅ Resource controller (PID + 3-state degradation)
- ✅ Graph routing algorithms
- ✅ Python inference sidecar (OpenAI, Ollama, llama.cpp backends)

## Lessons for Slackwater

1. **The compilation metaphor is powerful.** Don't cache LLM responses — compile them into reusable artifacts with parameterized templates.

2. **Hash embeddings are good enough for MVP.** Start without ONNX; add it when semantic matching matters.

3. **SQLite + sqlite-vec is a legitimate vector database.** No server, no infrastructure, single file. Perfect for agent-local memory.

4. **Confidence scoring creates a natural learning curve.** The system gets measurably better with use, and the confidence numbers are meaningful for routing decisions.

5. **The .nail format is a model for agent portability.** Agent state should be a single file you can move between machines.

6. **The veto engine pattern is essential for autonomous operation.** Deterministic safety rules before every execution, period.
