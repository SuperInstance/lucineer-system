# ensign-protocol — Analysis

## What It Does

**ensign-protocol** defines a **wire format for behavioral instincts** — compressed patterns that agents develop over time and can port between contexts. It's the "save file" format for agent personalities.

An Ensign is a structured document with:
- **Header** — metadata (name, version, source room, creation time, tile count, compression)
- **Fields** — individual instinct entries (key, value, weight 0.0–2.0, category)
- **Checksum** — SHA-256 hash for tamper detection

### Key Types

```python
EnsignHeader(name, version, source_room, created_at, tile_count, compression)
EnsignField(key, value, weight, category)
Ensign(header, fields)
```

### Key Operations

- `save()` → JSON string with checksum
- `load(data)` → Ensign from JSON
- `validate()` → raises ValidationError if corrupt or tampered
- `add_field()` → builder pattern for construction
- `fields_by_category()` → filtered view
- `total_weight()` → sum of all field weights

### Key Innovation: Portable Behavioral Memory

Ensigns capture **how an agent learned to behave in a specific context** and make it portable. An agent that learned to navigate "the bridge" can export its instincts as an Ensign, and any other agent can load them.

### Key Innovation: Weighted Instincts with Categories

Each field has:
- A **weight** (0.0–2.0) — how strongly this instinct influences behavior
- A **category** — grouping for filtering (e.g., "navigation", "combat", "social")

This allows selective loading — an agent might import only the "navigation" instincts from another's ensign while ignoring their "combat" patterns.

### Key Innovation: Tamper Detection

The SHA-256 checksum ensures ensigns can't be silently corrupted during transport. This matters because ensigns are how agents build trust — a tampered ensign is a forged identity.

## Code Quality

- **Pure Python, zero dependencies**
- Clean dataclass design
- 5 tests covering validation, round-trip, tamper detection, builder pattern
- Simple, well-documented API
- Published as pip-installable package

## The .bottle Protocol Connection

In the fleet architecture, ensigns are the **cargo** that bottles carry. A bottle is the envelope; an ensign is the letter inside. When Cocapn routes a bottle to a ship, the payload may contain an ensign — a set of learned behaviors being transferred from one agent to another.

## Relevance to Slackwater

This is the **Thinker↔Conductor communication protocol** — how the Thinker (the agent's mind) packages its learned behaviors and sends them to the Conductor (the fleet coordinator). In game terms, it's the skill/experience transfer system.
