# Negative Space: fleet-cns-v3 Has Zero Tests — The Nervous System Is Unverified

**Discovered:** 2026-08-13, 17:55 AKDT (Loop 2)
**Severity:** HIGH — this is critical infrastructure
**Repo:** `/home/eileen/projects/fleet-cns-v3/`

## The Finding

The CNS v3 bus is the typed Rust message bus that the entire fleet communicates through. Every agent — Hermes, Lucineer, Wesley, the living-minds daemon, the tapscript workers — sends messages through this bus. It has:

- **6 typed channels** (Pulse, Status, Creative, Decision, FeelTilt, IntentBroadcast)
- **Priority queuing** (Low, Normal, High, Critical)
- **SQLite persistence** with WAL mode and 7-day retention
- **USCP packet conversion** (bidirectional Hermes compatibility)
- **Broadcast pub/sub** with subscriber tracking
- **HTTP API** via axum

And it has **zero tests.**

Not a single `#[test]` in any source file. The `tempfile` dev-dependency is declared but never used. This is the system that carries every creative piece, every decision record, every pulse between agents. If the USCP conversion has a bug, messages silently corrupt. If the store has a race condition, messages disappear.

## What Could Go Wrong

1. **USCP `from_uscp` round-trip** — if serialization isn't symmetric, Hermes messages lose data in transit
2. **Priority ordering** — if `PartialOrd` is wrong, CRITICAL messages queue behind NORMAL
3. **Store cleanup** — if the timestamp comparison is wrong, recent messages get deleted
4. **Bus publish with no subscribers** — silent message loss (by design, but untested)
5. **Channel parsing** — if `FEEL_TILT` vs `FEELTILT` handling diverges, messages route to wrong channels
6. **SQLite WAL recovery** — crash during write could corrupt the bus state

## The Fix

Write comprehensive tests covering:
- Channel/Priority parsing (round-trip all variants)
- CnsMessage construction and USCP round-trip
- Bus pub/sub (subscribe, publish, receive, subscriber counting)
- Store operations (open, store, replay, since, cleanup, stats)
- Edge cases (empty channels, unknown intents, malformed USCP)

## Why This Matters

The fleet trusts the CNS bus. Every creative piece flows through it. Every Hermes packet is converted by it. Every decision is logged by it. Trust without verification is faith. The nervous system needs a checkup.
