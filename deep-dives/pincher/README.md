# Pincher — README

> A reflex engine for AI agents. "Vector database as runtime, LLM as compiler."

## What Is Pincher?

Pincher is a Rust-based reflex engine that sits between an AI agent and the world, intercepting patterns before they reach expensive LLM machinery. It responds in <50ms without an LLM, at zero marginal cost.

**The core loop:** Teach → Match → Execute → Learn

- **Teach**: Store an intent→action mapping as a vector-embedded reflex
- **Match**: Incoming intents are embedded and compared via cosine similarity
- **Execute**: Matched reflexes fire directly; novel intents escalate to the LLM
- **Learn**: Successful reflexes gain confidence; failures degrade

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Reflex** | A learned intent→action mapping stored as a 384-dim vector |
| **Three-tier matching** | Exact (≥0.80), Similar (0.55–0.80), Novel (<0.55) |
| **Confidence scoring** | Multiplicative: +5% of gap on success, -10% on failure |
| **.nail format** | Portable agent state (tar.zst + BLAKE3 checksums) |
| **Veto engine** | Pre-execution safety checks (blocks rm -rf, mkfs, etc.) |
| **Immunology** | Adaptive threat detection with persistent antibody memory |
| **Hash fallback** | Zero-dependency deterministic embeddings when ONNX unavailable |

## Architecture

```
pincher-core/     # Core library (Rust)
  src/reflex/     # Match, execute, confidence
  src/db/         # SQLite + sqlite-vec
  src/embed/      # ONNX (MiniLM-L6-v2) + hash fallback
  src/security/   # Veto engine, sandbox, capabilities
  src/migration/  # .nail portable format
  src/rpc/        # JSON-RPC over Unix sockets
  src/route/      # Ternary-weighted graph routing
  src/immunology/ # Pattern-based immune system
  src/resource/   # PID controller, 3-state degradation

pincher-cli/      # CLI binary (15+ commands)
pincher-infer/    # Python LLM sidecar (distillation)
hybrid-bridge/    # Experimental ternary computing bridge
```

## Quick Start

```bash
git clone https://github.com/SuperInstance/pincher.git
cd pincher
cargo build --release -p pincher-cli
cp target/release/pincher ~/.local/bin/

pincher status
pincher teach
pincher do "list files"
pincher reflexes
pincher pack --output crab.nail
```

## Technology Stack

- **Language**: Rust 2021 (core + CLI), Python (inference sidecar)
- **Storage**: SQLite + sqlite-vec extension
- **Embeddings**: all-MiniLM-L6-v2 (384-dim) via ONNX Runtime
- **Security**: Bubblewrap sandbox, Landlock (optional), veto engine
- **Portability**: .nail format (tar.zst + BLAKE3)
- **License**: MIT OR Apache-2.0

## Relevance to Slackwater Cognition

Pincher provides the **reflex memory layer** — sub-millisecond pattern matching between the Local Thinker's observations and the Conductor's routing decisions. It complements Cloudflare Vectorize (which handles large-scale document search).

See `analysis.md` for the full deep dive and `integration-plan.md` for the adoption roadmap.
