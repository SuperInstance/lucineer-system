# Push-Pull Medium Access for Digital Twin Alignment and Low-Latency Anomaly Reporting

**Date:** 2026-09-02 · **Scouted by:** eco-scout
**URL:** https://arxiv.org/abs/2508.21516 (v3 Jul 2026, submitted to IEEE JSAC)
**Authors:** Chiariotti, Saggese, Munari, Badia, Popovski (Aalborg / Padova line)

## What
A medium-access framework for wireless digital twins that splits traffic in two
lanes: **pull** (central, goal-oriented scheduled periodic status updates that
keep the twin aligned) and **push** (sensor-decided urgent transmissions for
anomalies/faults). A push-pull scheduler (PPS) balances the alignment-vs-anomaly
trade-off: reduces DT drift 20–30% at equal anomaly-detection guarantees, or
cuts worst-case anomaly detection time 30–70% at equal alignment. Key insight:
**the sensor itself decides when something is anomalous enough to interrupt the
schedule** — anomaly detection is pushed to the edge, alignment stays central.

## Why it matters to us
- **The Boat lane is exactly this shape.** F/V EILEEN's twin (engine monitoring,
  AIS, log detection) needs periodic telemetry (alignment) AND low-latency
  alarms (logs in the water, engine fault) over a constrained offshore link.
  The pull/push split with sensor-side urgency decisions is the architecture
  our edge devices (ESP32 quilt cells, Wesley-precursor watch stations) should
  grow into — no central round-trip for the alarm that matters.
- **Divergence framing matches our cosim problem.** quiltdeck just measured RTL
  vs Python twin divergence at frame #36; "DT drift" here is the same quantity
  with a scheduling knob. Their metrics (drift under constrained updates,
  worst-case detection time) are the right vocabulary for our treaty lane's
  divergence reporting.
- Popovski group's goal-oriented communication line (AoII, VoI scheduling) is a
  mature theoretical stack we can import for cellular-quilt tick scheduling —
  which updates a room/boat twin actually needs vs. which are redundant.

## Pointer
Abstract v3: https://arxiv.org/abs/2508.21516 · related: arXiv:2508.19141
(distributed bandit goal-oriented MAC), arXiv:2603.01781 (ISAC-enabled DTs,
EUSIPCO 2026).
