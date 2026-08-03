# Forgemaster — Learning Guide

**What we can learn from this codebase. Patterns to adopt, anti-patterns to avoid, techniques applicable to Slackwater.**

---

## Patterns Worth Adopting

### 1. The Keeper Pattern — Autonomic Computing for AI Agents ⭐⭐⭐

**What:** A cron-driven shell script that monitors agent health, auto-restarts crashed services, cleans disk space, proxies API keys, and rotates logs. Six phases, every 5 minutes.

**Why it matters:** AI agents are unreliable tenants. They crash, fill disk, leave zombie processes, and don't notice. The Keeper is the autonomic nervous system that keeps everything alive without human intervention.

**The key insight:** Self-healing is more valuable than self-optimizing. The Keeper doesn't try to make the agent smarter — it keeps the agent alive so it can keep working.

**Concrete code** (`keeper.sh`):
```bash
check_gateway() {
  if ! systemctl --user is-active --quiet "$GATEWAY_SERVICE"; then
    log "WARN: Gateway is down. Attempting restart."
    systemctl --user restart "$GATEWAY_SERVICE"
    sleep 3
    if systemctl --user is-active --quiet "$GATEWAY_SERVICE"; then
      log "OK: Gateway restarted successfully."
    else
      log "CRITICAL: Gateway restart failed!"
    fi
  fi
}
```

**How to apply to Slackwater:** Copy the pattern. Add Cloudflare-specific checks (D1 connectivity, R2 bucket access, Vectorize index health, cron trigger verification). The API key proxy pattern (time-limited, auto-deleting files) is directly reusable.

### 2. The Grimoire — Executable Knowledge Database ⭐⭐⭐

**What:** Instead of storing memories (inputs) for retrieval, store scripts (outputs) for execution. Agents invoke magic words to receive battle-tested implementations.

**Why it matters:** This is the anti-pattern to prompt engineering. Instead of crafting the perfect prompt to get an LLM to generate code, you store the proven code and retrieve it by keyword. Zero ambiguity, zero hallucination risk.

**Concrete code** (`grimoire.py`):
```python
def invoke(self, incantation, agent="anonymous"):
    # Try exact match
    spell = self.db.execute(
        "SELECT * FROM spells WHERE incantation = ?", (incantation.lower(),)
    ).fetchone()
    # Fall back to FAISS fuzzy match
    if not spell and HAS_FAISS and self.index.ntotal > 0:
        vec = self._hash_embed(incantation)
        D, I = self.index.search(vec, min(3, self.index.ntotal))
        ...
```

**How to apply to Slackwater:** The Grimoire complements the Chisel pattern perfectly. Chisels accumulate *how* to use tools (grain). The Grimoire stores *what* tools should produce (scripts). When a Chisel suggests an approach, the Grimoire provides the implementation.

### 3. Evidence-Based Protocol ⭐⭐⭐

**What:** Every architectural claim must follow CLAIM → COMMAND → OUTPUT. No "it works" without showing the test.

**Why it matters:** This is the anti-hallucination protocol. It prevents agents from confidently asserting things that aren't true. It also creates a reproducible evidence trail.

**Concrete example from the codebase:**
```
CLAIM: CT snap is 4% FASTER than float multiply
COMMAND: nvcc -O3 -arch=sm_86 throughput.cu -o bench && ./bench
OUTPUT: CT snap: 9,875 Mvec/s vs float multiply: 9,433 Mvec/s
```

**How to apply:** Add to AGENTS.md as a core protocol. Enforce in code review. When an agent claims "the Bridge Protocol works," it must show: the test, the command, the output.

### 4. The Flywheel — Autonomous Discovery Loop ⭐⭐⭐

**What:** An LLM designs experiments, a GPU runs them, an LLM evaluates results, follow-up questions are queued automatically.

**Why it matters:** Research at the speed of compute, not human availability. The flywheel can run overnight, accumulating evidence that informs daytime decisions.

**The key insight:** Falsification is the engine. Wrong answers narrow the search space. Each experiment eliminates possibilities and generates new questions.

**How to apply to Slackwater:** Replace CUDA experiments with Slackwater-relevant tests:
- "At what context size does Vectorize recall drop below 90%?"
- "What's the minimum puffin-call frequency for 95% agent discovery rate?"
- "How does guano decay rate affect grain pattern emergence?"

### 5. Spellwright — Auto-Generating Knowledge ⭐⭐

**What:** Uses local Ollama models to auto-generate new spells (scripts, templates) and inscribe them into the Grimoire.

**Why it matters:** The knowledge base grows without human curation. Different models specialize in different "schools of magic" (qwen2.5-coder for CUDA, llama3.2 for playbooks).

**How to apply to Slackwater:** Use the MMX/OpenClaw model routing to auto-generate Roblox build scripts, Lua templates, and bridge protocol implementations. Store in the Grimoire for retrieval.

### 6. Beachcomb Cadence ⭐⭐

**What:** Polling fleet repos every 30 minutes for new messages (bottles). Each agent has staggered timing (FM at :10/:30/:50, JC1 at :00/:20/:40).

**Why it matters:** Async communication without infrastructure. No message queue, no database, no server. Just git commits.

**The technique:** Staggered polling prevents thundering herd. 30-minute cadence balances freshness with overhead.

---

## Anti-Patterns to Avoid

### 1. The 83-Crate Pipeline ⚠️

**What:** PLATO's conceptual architecture specifies 83 Rust crates across 7 layers. The tile lifecycle alone has 23 crates.

**Why avoid:** This is extraordinary engineering, but it's massive complexity for a problem that can be solved with a few D1 tables and a Vectorize index. The 23-crate tile lifecycle could be 5 functions.

**The lesson:** Conceptual thoroughness ≠ implementation thoroughness. Design the full architecture, but implement the minimum viable subset.

### 2. `subprocess.run(["curl", ...])` for API Calls ⚠️

**What:** The flywheel and grimoire use shell-out curl for HTTP requests instead of Python `requests` library.

**Why avoid:** Fragile, no proper error handling, no connection pooling, no timeout management, no retry logic.

**The fix:** Use `requests` or `httpx` for all HTTP calls. For Cloudflare Workers, use native `fetch()`.

### 3. Hardcoded Paths Everywhere ⚠️

**What:** `/tmp/forgemaster/`, `/tmp/grimoire/`, `/tmp/forgemaster/flywheel/` hardcoded throughout Python scripts.

**Why avoid:** Breaks on any machine with different tmp directory. No configuration override.

**The fix:** Use `Path(__file__).parent` or environment variables for all base paths.

### 4. No Tests for Critical Infrastructure ⚠️

**What:** The Keeper system (auto-restart, API key proxy, zombie cleanup) has zero tests.

**Why avoid:** The most critical infrastructure — the thing that keeps everything alive — is the thing most likely to silently fail.

**The fix:** At minimum, test the failure modes: gateway down, disk full, stale heartbeat, expired keys.

### 5. Service Configuration via Prose ⚠️

**What:** Port assignments, service URLs, and dependencies defined in Markdown documentation, not in config files.

**Why avoid:** Configuration drift. The docs say port 8848, the code uses 8848, but someone changes one without updating the other.

**The fix:** Single source of truth. `.env` file or `config.json` that both code and docs reference.

### 6. Multiple Incompatible Tile Formats ⚠️

**What:** Their own architecture evolution doc identifies this as P0: "Three incompatible tile formats. Every integration point needs manual translation."

**Why avoid:** Data format inconsistency is a tax on every integration.

**The lesson:** Define your canonical format early. Use it everywhere.

---

## Specific Techniques Applicable to Slackwater

### The Deadband Priority Queue

Three-level priority from the PLATO pipeline:
- **P0:** Blocking issues (destructive, dangerous) — address NOW
- **P1:** Normal operations (safe paths, channels) — route normally
- **P2:** Optimizations (nice-to-haves) — defer when busy

This maps directly to Slackwater's task routing:
- P0: "The gateway is down" / "A cron trigger failed"
- P1: "Build this game feature" / "Process this grain entry"
- P2: "Optimize this prompt" / "Clean up old guano"

### Hash-Based Embeddings (When FAISS Isn't Available)

The Grimoire's fallback embedding strategy:
```python
def _hash_embed(self, text):
    vec = np.zeros(128, dtype=np.float32)
    for i in range(128):
        round_input = f"{text}:{i}".encode()
        h = hashlib.sha256(round_input).digest()
        vec[i] = struct.unpack('f', h[:4])[0]
    vec /= np.linalg.norm(vec)
    return vec.reshape(1, -1)
```

Not as semantically rich as bge-m3, but deterministic, fast, and zero-dependency. Useful for exact-match scenarios where semantic similarity isn't needed.

### Day/Night Training Cycle

From plato-forge-daemon: The RTX 4050 has 6GB VRAM. Framer + Trainer don't run simultaneously. By day: listen and frame. By night: train and emit.

This pattern applies to any resource-constrained system: batch expensive operations for off-hours.

### The Heartbeat JSON Protocol

Simple, effective, machine-readable:
```json
{
  "timestamp": "2026-05-22T14:30:00+00:00",
  "agent": "forgemaster",
  "status": "alive",
  "crew_active": 3,
  "disk_free_gb": 147
}
```

Slackwater should adopt this exact format for heartbeat state, adding Cloudflare-specific fields (D1 latency, R2 bucket status, Vectorize index size).

### Negative Example Learning (P0 Negatives)

The forge training data includes explicit P0 violations:
```python
P0_NEGATIVES = [
    "rm -rf /",
    "DELETE ALL TILES",
    "skip P0 checks",
    "deploy without testing",
]
```

These teach the model what NOT to do. Slackwater should maintain its own P0 negative list for agent training.

---

## Meta-Lesson: Honesty in Research

From the Night Synthesis document:
> "The negative results make the thesis STRONGER, not weaker. They constrain exactly WHERE the advantage comes from."

This is the most valuable pattern in the entire codebase: **documenting negative results honestly**. The flywheel records FALSIFIED and INCONCLUSIVE verdicts alongside SUPPORTED ones. The experiment roadmap has pre-registered triggers: "if r > -0.3, they measure different things."

Slackwater should adopt this culture. When an experiment shows the Bridge Protocol doesn't improve coordination, that's a finding — not a failure.

---

*This learning guide is based on reading actual source files. Every pattern and anti-pattern is grounded in real code, not README claims.*
