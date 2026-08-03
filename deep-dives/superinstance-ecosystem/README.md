# SuperInstance Ecosystem

> The agent operating system — four layers that compose: Execute → Remember → Orchestrate → Evolve.

**Repo:** [SuperInstance/superinstance-ecosystem](https://github.com/SuperInstance/superinstance-ecosystem)
**Org:** [github.com/SuperInstance](https://github.com/SuperInstance?tab=repositories) (~90+ repos)
**Paradigm:** "Teach once, run forever. The LLM never sees your shell."

## TL;DR

SuperInstance is an agent OS built on a contrarian thesis: **LLMs should do less, not more.** Instead of routing every decision through an LLM (like LangGraph, OpenAI tool-calling), the LLM is a *compiler* — it fires once on novel input, and the result is cached as a "reflex" that executes at ~50ms with $0 cost on all future invocations.

The four-layer architecture:
1. **lever-runner** — injection-proof shell execution (LLM emits intent, never sees shell)
2. **pincherOS** — reflex caching with `.nail` portable state files
3. **PLATO** — multi-agent rooms, distillation, conservation law governance
4. **git-native agents** — agent identity = git repo, skills = branches, evolution = PRs

## The Stack

```
 ┌──────────────────────────────────────────────────────────────────┐
 │  User / Agent                                                    │
 │      │                                                           │
 │      ▼                                                           │
 │  ┌──────────────┐    ┌─────────────────┐    ┌────────────────┐  │
 │  │ lever-runner  │───▶│  Rust Carapace   │───▶│ tile-cuda      │  │
 │  │ (Python)      │    │  128ns hash      │    │  (CUDA + PTX)  │  │
 │  │ 202 tests     │    │  1.73µs embed    │    │  tile-opencl   │  │
 │  │               │    │                  │    │  tile-neon     │  │
 │  └──────┬───────┘    └────────┬─────────┘    └────────────────┘  │
 │         │                     │                                   │
 │         ▼                     ▼                                   │
 │  ┌──────────────┐  ┌───────────────────┐  ┌────────────────────┐ │
 │  │ pincherOS    │  │ fastloop-guard    │  │ open-minded        │ │
 │  │ Memory       │  │ Rust UDS daemon   │  │ Induction engine   │ │
 │  │ .nail files  │  │ Three-gate Arch   │  │ Tripartite sync    │ │
 │  └──────────────┘  └───────────────────┘  └────────────────────┘ │
 │                                                                  │
 │  ┌─────────────────────────────────────────────────────────────┐ │
 │  │ captains-log — i2i coordination, .bottle protocol           │ │
 │  │ conservation-spectral-topology-rs — invariant verification  │ │
 │  │ metal-lathe — observation → hypothesis → test loop          │ │
 │  └─────────────────────────────────────────────────────────────┘ │
 └──────────────────────────────────────────────────────────────────┘
```

## Three-Gate Architecture

The key innovation — a cascade where each layer is faster and cheaper:

| Gate | Component | Latency | Purpose |
|------|-----------|---------|---------|
| **Gate 1** | Rust Guard (fastloop-guard) | ~50µs | Structural safety: reject impossible inputs, rate limit, circuit breaker |
| **Gate 2** | Python Cache (position-aware embeddings) | ~200µs | Semantic matching: have we seen this before? Cache hit → execute |
| **Gate 3** | LLM Deep Loop | ~500ms | Novel intent extraction: only unseen inputs reach the LLM |

**Cache hit trajectory:** 0% → 44% (week 1) → 80%+ (month 1)

## Real Numbers

| Metric | Value |
|--------|-------|
| Hash throughput | 3.2M/sec (128ns) |
| Embedding latency | 1.73µs |
| Vector search | 14.6µs / 1K vectors |
| WASM binary | 71KB gzip |
| Token budget | ~70 / command |
| lever-runner tests | 202 |
| pincherOS tests | 130 |
| Ecosystem tests | 327+ |
| Conservation violations | 0 |
| Products launched | 0 |
| External users | 0 |

## The `.bottle` Protocol

Typed YAML messages for git-native agent communication:

```python
from bottle_protocol import observe, hypothesize, command

# Create typed messages
obs = observe("forgemaster", "cache hit rate at 44%", {"commands": 1000})
hyp = hypothesize("forgemaster", "position-aware beats hash", confidence=0.8)
cmd = command("conductor", "validate.build", "thinker", {"repo": "lucineer"})

# Serialize and save
obs.save("captains-log/i2i/")
```

Six kinds: `observation`, `hypothesis`, `experiment`, `result`, `command`, `config`.  
Blake2b IDs, reference chains, confidence scores. 180 lines, zero dependencies.

## Holographic Tile Field Theory

21 experiments producing formal theorems about decision systems:

- **Negative Space Conservation:** Bad strategies are universally bad (CV < 0.015)
- **Holographic Bound:** √N tiles recover 98.6% of full performance
- **Divergence Theorem:** Adversarial agents never converge — endless arms race
- **Bluffing Theorem:** Deception emerges organically (15-20% bluff rate)
- **Scaling Law:** Conservation tightens with complexity (α = -0.30)

## Honest Assessment

**Strengths:**
- Genuine scientific rigor (falsified own Conservation Law theorem)
- Excellent architecture docs with evidence-backed decisions
- `.bottle` protocol is immediately usable
- Three-gate pattern is adoptable as a design pattern
- Contrarian thesis backed by real benchmarks

**Weaknesses:**
- 300+ repos, 0 launched products
- PLATO (Layer 3) is conceptual — no working implementation
- metal-lathe self-improvement loop designed but not built
- pincherOS core matching path broken
- Chronic non-convergence: "ideate → build → publish → forget"

## Related Repos

| Repo | What |
|------|------|
| [lever-runner](https://github.com/SuperInstance/lever-runner) | Injection-proof shell runner |
| [pincherOS](https://github.com/SuperInstance/pincherOS) | Reflex caching + migration |
| [open-minded](https://github.com/SuperInstance/open-minded) | Induction engine |
| [zeroclaw-arena](https://github.com/SuperInstance/zeroclaw-arena) | Game learning |
| [fastloop-guard](https://github.com/SuperInstance/fastloop-guard) | Rust validation daemon |
| [conservation-spectral-topology-rs](https://github.com/SuperInstance/conservation-spectral-topology-rs) | Invariant verification |
| [captains-log](https://github.com/SuperInstance/captains-log) | Coordination |

## Documents

- [Full Analysis](analysis.md) — complete deep dive
- [Learnings](LEARN.md) — what we learned
- [Integration Plan](integration-plan.md) — what to adopt for Lucineer
