# Pincher — Integration Plan for Slackwater Cognition Architecture

> **Goal:** Adopt Pincher's reflex engine as the Layer 1 memory backbone for the Conductor and Local Thinker.

---

## Phase 0: Evaluation (Complete)

- [x] Clone and study the full codebase
- [x] Document architecture, innovations, and code quality
- [x] Identify integration points with Slackwater components
- [x] Assess complementarity with Cloudflare Vectorize
- [x] Write analysis (`analysis.md`)

---

## Phase 1: Core Adoption (Week 1–2)

### 1.1 Vendor the Reflex Engine

**Do NOT add Pincher as a Git dependency.** Instead, extract the core patterns into the Slackwater codebase:

```
lucineer-system/
├── crates/
│   └── reflex-engine/         # Extracted from pincher-core
│       ├── src/
│       │   ├── lib.rs
│       │   ├── engine.rs      # ReflexEngine (teach, match, execute)
│       │   ├── matcher.rs     # Vector similarity matching
│       │   ├── confidence.rs  # Confidence model
│       │   ├── embed.rs       # Embedding abstraction (ONNX + hash)
│       │   ├── db.rs          # SQLite + sqlite-vec storage
│       │   ├── veto.rs        # Security veto engine
│       │   └── nail.rs        # .nail portable format
│       └── Cargo.toml
```

**Why vendor:** Pincher is a single-maintainer project with experimental components. We want the proven core (reflex engine, matching, storage, veto) without the experimental edges (hybrid-bridge, ternary routing, WASM compilation).

### 1.2 Adapt the Schema

Extend Pincher's schema for cognition-specific use:

```sql
-- Pincher's original reflexes table (unchanged)
CREATE TABLE reflexes (
    id TEXT PRIMARY KEY,
    intent TEXT NOT NULL,
    action TEXT NOT NULL,
    embedding BLOB NOT NULL,
    confidence REAL NOT NULL DEFAULT 0.5,
    invoke_count INTEGER NOT NULL DEFAULT 0,
    last_invoked TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Slackwater extension: thought types
ALTER TABLE reflexes ADD COLUMN category TEXT DEFAULT 'reflex';
-- Categories: 'reflex', 'observation', 'preference', 'routing', 'decision'

-- Slackwater extension: source tracking
ALTER TABLE reflexes ADD COLUMN source TEXT DEFAULT 'system';
-- Sources: 'system', 'local-thinker', 'conductor', 'user', 'external'
```

### 1.3 Wire the Conductor

The Conductor queries the reflex engine before making routing decisions:

```rust
// In the Conductor's request handler:
fn route_request(&mut self, request: &str) -> RoutingDecision {
    // 1. Check reflex engine for fast path
    let match_result = self.reflex_engine.do_command(request);
    
    match match_result.match_type {
        MatchType::Exact => {
            // High-confidence reflex — bypass LLM entirely
            RoutingDecision::Direct(match_result)
        }
        MatchType::Similar => {
            // Medium confidence — use reflex but log for review
            RoutingDecision::Assisted(match_result)
        }
        MatchType::Novel => {
            // Novel intent — full Conductor deliberation
            // After resolution, store the decision as a new reflex
            let decision = self.deliberate(request);
            self.reflex_engine.teach(request, &decision.action);
            decision
        }
        MatchType::Builtin => {
            RoutingDecision::System(match_result)
        }
    }
}
```

### 1.4 Wire the Local Thinker

The Local Thinker stores observations and preferences as reflexes:

```rust
// When the Thinker observes a pattern:
thinker.reflex_engine.teach(
    "user prefers concise responses during coding sessions",
    "respond with code blocks, minimal prose"
);

// When checking how to respond:
let match_result = thinker.reflex_engine.do_command("how should I format this response?");
// If Exact: use the stored preference directly
// If Novel: default behavior, learn from the interaction
```

---

## Phase 2: Embedding Pipeline (Week 3)

### 2.1 Hash Fallback First

Start with Pincher's hash-based embedding. Zero dependencies, instant setup. Good enough for:
- Exact intent matching
- Near-exact paraphrasing
- System commands and structured requests

### 2.2 Add ONNX When Needed

When semantic matching across diverse phrasings becomes important:

```bash
# Download the model
curl -L -o ~/.pincher/models/all-MiniLM-L6-v2-int8.onnx \
  https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/onnx/model_int8.onnx

# Build with ONNX support
cargo build --release --features onnx
```

### 2.3 Consider BGE-M3

The TOOLS.md mentions `BAAI/bge-m3` for skill library semantic search. If we're already running an embedding model, we could:
- Use BGE-M3 for both Pincher reflexes and Vectorize (consistency)
- Or keep MiniLM-L6-v2 for Pincher (smaller, faster, sufficient for short intents)
- Or use Cloudflare Workers AI for embeddings (no local model needed)

**Recommendation:** Start with MiniLM-L6-v2 (Pincher's default). It's 384-dim, fast, and well-calibrated for the matching thresholds (0.80/0.55). Switch to BGE-M3 only if matching quality is insufficient.

---

## Phase 3: Safety and Autonomy (Week 4)

### 3.1 Adopt the Veto Engine

Pincher's veto engine is essential for autonomous operation. Integrate it as a pre-execution gate:

```rust
// Before ANY tool execution:
fn execute_safely(&self, command: &str) -> Result<Output> {
    let veto_engine = VetoEngine::with_defaults();
    let context = ExecutionContext::for_command(command);
    
    match veto_engine.check(command, &context)? {
        VetoDecision::Allow => self.execute(command),
        VetoDecision::RequireConfirmation(reason) => {
            // Ask the user or log for review
            self.request_confirmation(reason)
        }
        VetoDecision::Deny(reason) => {
            // Hard block
            Err(SafetyError::Vetoed(reason))
        }
    }
}
```

### 3.2 Custom Veto Rules for Slackwater

Extend the default rules with Slackwater-specific patterns:

```toml
# slackwater-veto-rules.toml

[[rules]]
type = "forbidden_pattern"
pattern = "openclaw gateway"
reason = "Gateway configuration changes require explicit user approval"

[[rules]]
type = "forbidden_pattern"
pattern = "crontab -r"
reason = "Crontab removal is destructive — use crontab -e to modify"

[[rules]]
type = "forbidden_command"
pattern = "openclaw restart"
# This should be RequireConfirmation, not Deny — but that requires custom rule type
```

### 3.3 Immunology for Prompt Injection Defense

Pincher's immunology system maps directly to defending against prompt injection:

```rust
// Store antibodies for known attack patterns
let antibody = Antibody::new(
    AntigenKind::PromptInjection,
    r"(?i)ignore\s+(all\s+)?previous\s+instructions",
    "Blocks instruction override attempts",
);
immune_memory.store_antibody(&antibody)?;

// Check incoming messages
if immune_memory.is_blocked(user_input)? {
    return Response::rejected("Potential prompt injection detected");
}
```

---

## Phase 4: Portability (Week 5+)

### 4.1 Agent State Bundles

Use the `.nail` format to make Lucineer's learned state portable:

```bash
# Pack Lucineer's current state
lucineer memory pack --output lucineer-2026-08-03.nail

# Unpack on a new machine
lucineer memory unpack --bundle lucineer-2026-08-03.nail
```

The bundle includes:
- All learned reflexes and confidence scores
- Behavioral preferences
- Veto rules and immune antibodies
- Hardware fingerprint for compatibility scoring

### 4.2 Cross-Machine Sync

Future: Use the registry pattern for multi-machine reflex sharing:

```
Machine A teaches: "deploy to staging" → reflex
Machine B queries: "push to test environment" → matches via vector similarity
```

This requires either:
- A central registry server (Pincher's `publish` command)
- Or peer-to-peer sync via `.nail` exchange

---

## Phase 5: Advanced Integration (Future)

### 5.1 Reflex-Based Skill Routing

Store skill embeddings in the reflex database:

```rust
// When a skill is registered:
for skill in available_skills {
    let embedding = embed(&skill.description);
    reflex_engine.teach(&skill.description, &skill.location)?;
}

// When routing:
let match = reflex_engine.do_command("I need to debug a Python script");
// Matches to the python-debugpy skill via semantic similarity
```

This replaces manual skill selection with learned, confidence-weighted routing.

### 5.2 Heartbeat Integration

During heartbeat checks, the agent can:
- Review recently-failed reflexes (low confidence)
- Prune stale reflexes that haven't been invoked
- Check immune memory for new threats
- Run the resource controller for self-monitoring

```rust
fn heartbeat(&mut self) {
    let state = self.resource_controller.tick();
    if state == ResourceState::Critical {
        // Enter low-power mode: reflex-only, no LLM
        self.mode = AgentMode::ReflexOnly;
    }
    
    // Prune reflexes below 0.10 confidence
    self.reflex_engine.prune_low_confidence(0.10);
    
    // Check immune memory for decay candidates
    self.immune_memory.prune_older_than(&one_week_ago());
}
```

### 5.3 Multi-Agent Reflex Sharing

In a multi-agent fleet (e.g., Lucineer instances on different machines):
- Export reflexes as `.nail` bundles
- Import on peer machines
- Use compatibility scoring to handle environment differences
- Build a shared "reflex library" via the registry

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| sqlite-vec extension breaks on platform | Low | High | Hash fallback works without it |
| ONNX model unavailable | Medium | Low | Hash fallback is functional |
| Reflex pollution (bad patterns learned) | Medium | Medium | Confidence decay + veto engine + pruning |
| Single-maintainer upstream | High | Medium | Vendor the core, don't depend on upstream |
| Schema migration conflicts | Low | Medium | Pincher's migration system is idempotent |
| Performance at scale (>10k reflexes) | Low | Medium | Partition by category, archive old reflexes |

---

## Success Criteria

- [ ] Reflex engine integrated as `crates/reflex-engine` in lucineer-system
- [ ] Conductor queries reflex engine before LLM calls
- [ ] Local Thinker stores observations as reflexes
- [ ] Veto engine gates all tool executions
- [ ] `.nail` bundles enable agent state portability
- [ ] Hash fallback works zero-dependency
- [ ] Reflex count >100 within first week of use
- [ ] LLM call reduction measurable (>30% of intents handled by reflexes)

---

## Decision Record

**2026-08-03:** Evaluated Pincher for integration into Slackwater Cognition Architecture. Decision: **Adopt as Layer 1 reflex memory.** Vendor the core patterns (reflex engine, matcher, confidence, DB, veto) rather than depending on upstream. Complement with Cloudflare Vectorize for large-scale search.
