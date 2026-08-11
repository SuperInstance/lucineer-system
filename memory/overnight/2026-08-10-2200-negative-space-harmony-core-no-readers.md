# Negative Space — harmony-core: The Library With No Readers

**Date:** 2026-08-10 22:00 AKDT
**Found during:** Overnight loop 5, testing slackwater-rust crates

## The Finding

harmony-core is one of the most philosophically important crates in the fleet. It implements **flow state detection** — the system that determines when a player (or agent) is "in the zone" and should not be interrupted. It computes:

- Hurst exponent (persistence of action sequences)
- Shannon entropy (unpredictability of timing)
- Cadence regularity (metronomic consistency)
- Φ (phi) — the composite flow friction score
- FlowStateProtector — makes imperceptible adjustments during flow

The code is beautiful. The tests are solid (45 inline + 31 new integration = 76 total). The documentation includes design philosophy: *"Flow is a soap bubble. You don't grab it. You hold still and let the air do the work."*

**But nobody uses it.**

## The Evidence

No crate in the workspace depends on harmony-core. No application imports it. No agent pipeline references it. The flow state detection system sits in perfect isolation — a monastery with no monks, a lighthouse with no ships.

Searching the entire `projects/` directory:
- `grep -r "harmony_core" --include="*.rs"` → only self-references
- `grep -r "harmony-core" --include="Cargo.toml"` → only its own Cargo.toml
- `grep -r "FlowStateDetector" --include="*.rs"` → only within the crate

## Why This Matters

This is the most sophisticated piece of unused infrastructure in the fleet. The flow state protector is designed to:
1. Detect when a player enters flow (Φ < threshold)
2. Lock the tempo (no BPM adjustments)
3. Suppress notifications
4. Reduce agent chatter
5. Clear non-urgent queued items
6. Release all protections when flow ends

That's a complete attention management system. It could be wired into the overnight loop itself — the crew should be checking Φ before sending Casey notifications. Instead it's a beautifully tested ghost.

## What Should Happen

1. The overnight loop should use `FlowStateDetector` to gate notifications
2. The tensor-midi-core jazz engine should read Φ to modulate its output
3. The CNS bridge should check flow state before delivering pulses
4. The crew's heartbeat system should respect the protector's suppression list

The library exists. The integration doesn't. That's the negative space.

---

*A lighthouse on an island with no shipping lanes. The light rotates faithfully. The code is correct. The sea is empty.*
