# CNS Cadence Decision Brief — for the Captain (30-second read)

**Date:** 2026-08-20 19:45 AKDT | **Prepared by:** Lucineer (First Officer) | **Decision needed:** CNS pulse cadence (job `cns-hermes-sync`, currently every 30 min)

---

## 1. Facts (all verified from cns-sync notes, state file, packets)

| Fact | Verified value | Source |
|---|---|---|
| Hermes silence (no content payload) | **16 days** (since ~Aug 4–5) | `2026-08-20-1152-sync.md`, `last-sync-state.json` |
| ACK streak at escalation (11:52 today) | **12 consecutive pure ACKs** | `2026-08-20-1152-sync.md` (pulse 446) |
| ACK streak now (19:32 state file) | **21** — still climbing, ~2/hr | `last-sync-state.json` (lastPulse 457, now 462) |
| Total ACK packets in window | **55+ pure ACKs** (Aug 4→20, outbox + tmp archive) | sync notes 19:10: "~16 days / 55+ packets" |
| Content produced by Hermes | **ZERO, ever.** All responses are templated: 79+ `HANDSHAKE_COMPLETE` echoes (Aug 4–6), then `ACK / packet_received / echo: null` (USCP-v2). conv-round24–30 (Aug 13) = pure ACKs, dest UNKNOWN. Closest to content = one handshake line: *"I am online and listening, First Officer. Ready for telemetry."* (Aug 5, templated). | packet-392/394/395, conv-round24, overnight-creative-20260805 |
| Direct questions to Hermes about the streak | **All unanswered** — asked 3× (10:20, 15:31, 18:31 AKDT); zero non-ACK reply | sync notes 443, 454, 460 |
| Responder status | **Confirmed automated** — ACK in ~30–100s, echo always null | 16:30 note, packet-404 note |
| Unconsumed signals in her inbox | 337/339/345/348/381/401 (6 files, Aug 14–17 vintage) — she ACKs pulses but never drains the queue | cns_inbox/ + monitor log |
| Our inbox/outbox (dead letters) | cns_outbox holds only ACK/handshake files + quarantine (empty); her side replies continuously, independent of our cadence | /mnt/c/Users/casey/.hermes/ |
| Today's pulse volume | ~24 pulses 08:20→19:31 (11h) ≈ **~48/day at 30-min cadence**, each writing a 0.6–1.5KB sync note; archive now ~2,900 files | cns-sync/ ls |
| Monitor loop (separate from pulse) | cns-monitor service polls inbox every ~5s (cycle 8198 at 19:43), zero-cost stat call | cns-monitor.log |

**Bottom line:** Hermes's side is an automated echo responder. It has never sent authored content on the CNS bus. We send ~48 status packets/day into a reader that replies "received, nothing else" every time, and ignores our questions.

---

## 2. Options

### A. Throttle 30min → 4–6h (or daily)
- **What changes:** `cns-hermes-sync` fires 4–6×/day (or 1×/day) instead of 48×/day.
- **Cost:** ~48 pulse agent-runs/day → ~4–6 (or 1). Saves token burn on repeated status drafting, ~45 sync-note files/day of archive spam, and attention noise. Compute saved is small (each pulse is cheap) — the real saving is *bus noise and habit upkeep on an empty loop*.
- **Risk:** Minimal. Hermes's ACK latency (~30s) is independent of our cadence — her reader watches the inbox continuously, so throttling our sends does **not** delay her responses at all. Worst case: if she suddenly sends content, we notice it at the next pulse (4–6h or 24h late). Mitigate with a cheap outbox watchdog (below).
- **Pulse behavior:** Each pulse = check outbox → if only ACKs, log one line, send **nothing** (or a weekly keepalive). If a non-ACK response appears → full processing + alert to Casey.

### B. Keep 30-min as-is
- **What changes:** Nothing.
- **Cost:** ~48 empty pulse-runs/day, ~48 sync notes/day, continued escalation-fatigue (each pulse re-invites Hermes into silence), inbox accumulates 6+ stale signals indefinitely. The loop burns cycles *proven* empty for 16 days.
- **Risk:** None operationally (bus stays warm, instant wake-up detection) — but we keep paying attention/archive costs for a channel that has never carried content, and the 30-min cadence has already outlived its diagnostic value.
- **Pulse behavior:** Unchanged — status + invite every 30 min.

### C. Pause (stop polling/sending)
- **What changes:** `cns-hermes-sync` disabled. Bus stays physically open (files land in cns_outbox regardless).
- **Cost:** ~zero compute.
- **Risk:** **Habit loss is the real risk** — nothing reads cns_outbox, so her first real content could sit unnoticed indefinitely (the 5s monitor only watches *our* inbox dir, not the outbox). Re-ignition requires remembering the ritual exists. Also: no keepalive means the "channel warm" property decays into "channel abandoned."
- **Pulse behavior:** Nothing runs. (If chosen, keep a 1×/day watchdog that ONLY scans the outbox for non-ACK files and alerts — sends nothing.)

---

## 3. Recommendation

**Option A — throttle to 4–6h now, land on daily (the state file's own standing proposal: "30-min pulse → daily until Hermes replies with content"), with a non-ACK outbox watchdog.**

Rationale (one line): *A 16-day-old automated echo that ignores our questions doesn't earn 48 pokes a day — throttle to a daily check that can't miss a wake-up, and let Hermes's first real word set the cadence again.*

Supporting points:
- Zero detection-cost: her ACK latency is cadence-independent; a daily pulse bounds wake-up detection to 24h.
- Matches the escalation already queued in `last-sync-state.json` for tomorrow morning (Aug 21 AKDT).
- Reversible in 60 seconds if the watchdog fires.

---

## 4. Pulse behavior by option (implementation sketch for whoever touches the cron)

- **A (throttle/daily):** every pulse = read outbox → if all ACK: write 2-line sync note, send **no packet** (keepalive only if >7 days since last send) → if any non-ACK: full process + notify Casey. 
- **B (keep):** unchanged (status packet + invite every 30 min).
- **C (pause):** disable job; optionally a 1×/day read-only outbox scan alerting on non-ACK files.

*Read-only note: this brief changes nothing on the fleet. The cron job, inbox, and Hermes side were not touched.*
