# Lever Runner — Lessons Learned

> Patterns and insights extracted for the Slackwater Cognition Architecture.

---

## 1. The Compilation Model: Teach Once, Run Forever

**The most important lesson.** Lever Runner treats LLM understanding as a compile-time concern. You use the LLM once — to understand what a user means and map it to an action. After that, the mapping is fixed in a vector database and executed via cosine similarity. No LLM needed at runtime.

```
Compile time:  intent → LLM → phrase → embed → store in vector DB
Runtime:       request → (optional LLM compress) → vector search → execute
```

**Application to cognition:** The Local Thinker should distinguish between *learning new actions* (expensive, LLM-assisted, infrequent) and *executing known actions* (cheap, deterministic, frequent). The vector DB is the boundary between these two modes.

---

## 2. Three-Gate Cascade: Escalating Cost, Decreasing Frequency

Every request passes through three gates, cheapest first. Most requests never reach the expensive gate.

| Gate | Latency | Cost | Hit Rate |
|------|---------|------|----------|
| 1. Template/rate-limit check | 50µs | $0 | ~20% |
| 2. Embedding cache + vector search | 200µs - 7.6ms | $0 | ~44% |
| 3. LLM intent extraction | 500ms | ~76 tokens | ~36% |

**The design principle:** Always attempt the cheapest resolution first. Cache aggressively. Only escalate to the expensive path when all cheaper paths miss.

**Application to cognition:** The Local Thinker should implement a cascade:
1. **Pattern match** — exact triggers, cached responses (0 tokens, 0 ms)
2. **Embedding search** — similar past situations (0 tokens, ~7ms)
3. **LLM compression** — novel situations only (~76 tokens, ~500ms)

Target: >50% of decisions resolved at gates 1-2.

---

## 3. The Failure Cache: Negative Learning

Lever Runner's FastLoop maintains a `failure_db` — a hash set of inputs that previously caused errors. When the same input arrives again, it's rejected instantly without any processing.

This is **negative learning** — the system gets faster as it accumulates knowledge of what doesn't work. Unlike positive learning (adding new capabilities), negative learning monotonically improves performance.

**Application to cognition:** Maintain a failure cache for:
- Action triggers that consistently produce errors
- Input patterns that lead to dead ends
- LLM prompts that produce unhelpful responses

The failure cache should have a TTL (Lever Runner doesn't, which is a minor weakness — stale failures could block valid inputs after environment changes).

---

## 4. Asymmetric Trust Dynamics

```
Success:  +1.5 trust
Failure:  -4.0 trust
```

The 1:2.67 ratio means a command needs ~3 successes to recover from one failure. This is deliberately conservative — it favors reliability over novelty.

**Why asymmetric?** A command that succeeds once might be lucky. A command that fails once is definitely broken. False positives (trusting a bad command) are more dangerous than false negatives (distrusting a good command) because bad commands can cause real damage.

**Application to cognition:** The action policy table should use asymmetric trust dynamics. The exact ratio depends on the cost of errors in the cognition architecture — if errors are cheap to recover from, a 1:1 ratio might be fine. If errors propagate (like in the GPU execution context from INSIGHT.md), a 1:5 ratio might be appropriate.

---

## 5. Parameterized Actions with Validated Arguments

Lever Runner supports `{{param}}` templates:

```
teach: "show logs for {{container}}" → "docker logs --tail 100 {{container}}"
use:   "show logs for nginx"        → "docker logs --tail 100 nginx"
```

Arguments are validated against `^[a-zA-Z0-9._-]+$` — shell metacharacters are structurally impossible. This allows dynamic parameterization without injection risk.

**Application to cognition:** Actions should support parameterized templates. The validation regex should be action-specific (some actions might allow paths, others only identifiers). The key principle: **the parameter space is bounded and validated before execution**, not after.

---

## 6. Provider Fallback Chain — Always Terminate at Zero Cost

```
primary (ollama) → fallback1 (deepinfra) → fallback2 (openai) → passthrough
```

The chain **always ends at passthrough** — a complete provider outage degrades to using the raw user input as the search key. This is lower quality but never fails.

**The design principle:** Every external dependency should have a zero-cost fallback. The system should be functional (if degraded) even if every external service is down.

**Application to cognition:** The Local Thinker should have a passthrough mode for every LLM-dependent operation. If the cloud thinker is unreachable, the local thinker should still operate using local models, cached responses, or heuristic defaults.

---

## 7. Per-Session Sandboxing as a Trust Boundary

Every command execution gets:
- A fresh `/tmp/lever-runner/<session_id>/` directory
- A restricted environment (only whitelisted vars)
- Resource limits (CPU, memory)
- A hard timeout (30s, process-group kill)
- A restricted PATH (system paths only)

**The principle:** Each execution is isolated. A compromised command cannot affect other executions, cannot read the host filesystem, cannot exfiltrate data (no network access in env), and cannot run forever.

**Application to cognition:** Action execution in the cognition architecture should use per-invocation sandboxes. Even for non-shell actions (API calls, data transformations), the principle of isolation applies: each action gets its own context, resource limits, and timeout.

---

## 8. Skill Packs as Composable Knowledge

Lever Runner's skill packs are JSONL files — each line is `{intent, command, category}`. They're composable (import multiple packs), portable (export and share), and version-controllable (plain text, diffable).

```
system.jsonl:  25 commands (disk, memory, processes, network)
devops.jsonl:  46 commands (docker, systemd, nginx, logs)
git.jsonl:     32 commands (branching, rebasing, stash, cherry-pick)
security.jsonl: 10 commands (ports, firewall, suid, fail2ban)
python.jsonl:  15 commands (pip, venv, pytest, black, mypy)
```

**Application to cognition:** Cognition capabilities should be packaged as composable, portable skill packs. A "skill" is a set of `(trigger_pattern, action_spec, confidence)` tuples that can be imported, exported, shared, and version-controlled. This aligns with the OpenClaw skills model.

---

## 9. The `.nail` Format: Portable Cognition State

The `.nail` export packages:
- `manifest.json` — metadata, checksums, device fingerprint
- `reflexes.db` — SQLite with intent/action/embedding/confidence tuples
- `identity.json` — agent preferences
- `config.toml` — resource thresholds

All compressed as tar.zst. A complete cognitive state, portable across devices.

**Application to cognition:** The cognition architecture should define a similar portable format. A "cognition snapshot" that includes:
- Action policy table (embeddings + trust scores)
- Failure cache
- Configuration
- Version metadata

This enables deploying pre-trained Local Thinkers, sharing cognition state, and rolling back to known-good states.

---

## 10. What NOT to Take from Lever Runner

### 10.1 `shell=True` Is a Security Debt

Lever Runner uses `subprocess.Popen(command, shell=True)`. The metacharacter validation is excellent, but `shell=True` is inherently risky. For the cognition architecture, prefer `shlex.split()` + `shell=False` for non-pipeline commands, or use a proper shell parser for pipelines.

### 10.2 LanceDB as Sole Vector Store

LanceDB works but has rough edges. The cognition architecture should abstract the vector store interface (like Lever Runner's `CommandStore` class but with a proper protocol) and support multiple backends (Qdrant, ChromaDB, SQLite+numpy, FAISS).

### 10.3 Single-Action Granularity

Lever Runner does one command per request. The cognition architecture needs multi-step planning, conditional branching, and stateful composition. Don't try to force all cognition into Lever Runner's single-action model.

### 10.4 No Context Awareness

Lever Runner's LLM sees only the user's phrase — no conversation history, no system state, no environmental context. This is great for security but limiting for cognition. The Local Thinker needs richer context (current goals, recent actions, system state) without sacrificing the token-lean property.

---

## 11. Key Numbers to Remember

| Metric | Value | Why It Matters |
|---|---|---|
| Tokens per query (passthrough) | 0 | Zero-cost operation is achievable |
| Tokens per query (hosted LLM) | ~76 | 28× cheaper than tool-calling |
| Vector search p50 latency | 7.6ms | Fast enough for real-time cognition |
| Template match latency | 1.7µs | Essentially free |
| Cache hit rate | 44% | Nearly half of queries skip the LLM |
| Seed commands | 67 | Starting library that covers common ops |
| Asymmetric penalty ratio | 1:2.67 | Successes need to outnumber failures 3:1 |
| Similarity floor | 0.55 | Below this, no match (forces teaching) |
| Trust floor for auto-run | 40 | Below this, requires confirmation |
| Trust promotion threshold | 20 successes | Earns +10 trust bump |
| Trust demotion threshold | 5 failures at trust <30 | Triggers LLM rewrite |

---

*These lessons feed directly into the integration plan. See `integration-plan.md` for the phased adoption roadmap.*
