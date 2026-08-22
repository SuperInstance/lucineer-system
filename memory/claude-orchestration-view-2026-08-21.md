---
name: claude-orchestration-view-2026-08-21
description: Claude's strategic orchestration recommendations — sequencing, token routing, decision gates
metadata:
  type: project
---

# Claude Orchestration View — 2026-08-21

**The thesis:** The fleet is architecture-complete and bottlenecked by two decisions and one wiring task, not new math. Sequence credibility moves fast, unblock the demo, clear Casey's gate decisions, and ship the agent-collectives narrative this quarter.

## 1. Sequencing: The Sequence Within This Week

**Collapse objectives 1 & 2 into one **foundation sprint** (parallel, <24 hrs total):**

- **Objective 1 (Honest foundation):** Apply the five truthfulness edits — drift numbers, narrative qualifiers, E2/E3 tests-or-caveat [2026-08-21 digest 5]. These are mechanical. Assign to DeepSeek, merge Friday morning.
- **Objective 2 (Calibrated instrument):** Run the κ(t)-around-entry-steps check on existing corpus [digest item 10②]. It's read-only, hours-long, highest-value design experiment. Parallel-path: DeepSeek runs the check; Claude reads the verdict Monday. **Gate decision:** If κ(t) confirms entry-steps *are* concentration events (not mean-direction), then wave-3 is a power design — ship it now, no generator rewrite. If κ(t) fails, the K leg becomes the primary path. Either way, you have a decision.

**Why collapse them?** Both are <1 day, both feed credibility, and the κ(t) verdict is the last unknown before the instrument-maker sprint (objective 2b, riverbed harness). Burning 24 hours here buys clarity for 2 weeks of downstream work.

**Objective 3 (Live demo loop) is the real work:** reading → visible output → policy [digest 3]. The architecture is done [digest 8, 9]. This is pure engineering: wire `roomd :4073 GET /field` → sensor cell / sim-worker → crab-traps D1 ledger → Pages dial-dashboard. Assign to OpenCode + Kimi subagents (they have the X1–X15 cross-link tasks ready [digest 9]). **Target:** Visible output by end of week. This is the agent-collectives thesis made concrete and the highest-leverage visibility move.

**Objective 4 (CF migration phase 3)** is parallel infrastructure work: fleet-radio → Queues + the-tap DO build [digest 4]. Fully specified [digest 8]. Assign to OpenCode + Kimi. Start now, land by Sept 3 (supports phase 5). Does not gate narrative.

**Objective 5 (Fleet credibility)** hinges on one Casey call: retry P0 quilt-jetson #1/#3 merges and ratify the one-day coordinated dependabot wave [digest 5]. Blocking decision: OAuth scope fix. Once Casey greenlight, this is a 1-day coordinated push (47 PRs). Do not start until oauth-fixed merges pass.

## 2. Token Economy: Routing

**DeepSeek (free-ish):** Run the κ(t) check (read-only experiment); apply the five truthfulness edits. ~8–12 hrs. Lock it in Friday morning; verdict Monday.

**GLM (cheap):** Already worked the consensus + migration design. Stand by for CF phase 3 tweak-pass if OpenCode surfaces edge cases in the Queues/DO conversion.

**OpenCode (plenty):** **Primary orchestration lane this week:**
  - Choreograph the demo wiring (X1–X15 tasks, ledger consumer, Pages dashboard).
  - CF phase 3 → Queues/DO conversion (spec → code).
  - Digest cadence: Move to **event-gated model, never polling** [digest 4.2]. Gate on: κ(t) verdict, wiring MVP completion, Casey decisions, PR merge milestones. Propose: Monday verdict brief, Wednesday sprint sync, Friday completion memo.

**Kimi (medium):** Subagent overflow for OpenCode (demo wiring + CF). **Ratify KimiCode-under-systemd now** [digest 4.8] — it's the persistent engine for phases 3–5 and unblocks the "one-command deploy" developer story [digest 8].

**Claude (scarce, this hour):** This memo + arbitration on one pivot: **Calibration vs wiring.**

## 3. The One Decision That Might Require Claude Arbitration

[Digest 4.1] asks: If capacity forces a choice, which gets the next deep-compute block — the riverbed harness (instrument-maker, complex) or the wiring (zero new math, high visibility)?

**Recommendation: Defer the riverbed harness until the κ(t) check lands.** Here's why:

- The κ(t) check directly answers whether the instrument needs a full rewrite or just a K-leg addition [digest 10②]. If κ(t) confirms entry-steps are concentration events, the existing riverbed can ship wave-3 this quarter with cosmetic updates.
- If κ(t) fails, **then** you need the instrument-maker sprint (α-sweep, persona simulator, coordinate firewall, decoy audit). But you'll know this by Monday; then the riverbed harness becomes the clear priority.
- The wiring (objective 3) is unblocke—it doesn't wait on calibration. It's architectural choreography, pure engineering. Assign it to OpenCode now.

**Outcome:** By end of week, you know whether the instrument needs a full rebuild or a fix, and the demo is wired and visible. The instrument-maker sprint is either a confirmed priority or downranked to Q4.

## 4. What Casey Decides This Week (Not Next Week)

**Gate decisions — block execution if not decided:**
1. **OAuth scope fix merge retry** [digest 5]. Pass: yes/no? (Outcome: quilt-jetson #1/#3 and the 47-PR dependabot wave unblock.)
2. **CF gates** [digest 3.8]: Oracle decommission timing, $5/mo Workers Paid tier for DOs/Queues, shared D1 `fleet-spine` vs per-example DBs. (Outcome: CF phase 3 scope + cost clarity.)

**Batched decision memo for post-iceberg** (do not surface weekly):
- Landmine-migration wave timing (lean: weekend).
- Front-door "500+ repos" claim verification (lean: yes).
- Boat IP 147.224.38.131 DDNS / CF Tunnel (infrastructure, low narrative impact).
- JEPA naming rename (lean: yes, credibility win).
- Tap demo gating: hold or ship degraded (recommend: ship degraded on crab-traps format alone; quilt-side cell kinds can follow).
- Hero display 149KB vs 213KB.
- Raw-boat `database_id` truth.

**Human tasks** (Casey's parallel track):
- Fine-grained PAT (contents + workflows write).
- Tapscript-studio repo rename.
- Four push authorizations + dependabot standing-rule + remote-detach approval.

## 5. The Three Highest-Leverage Moves

1. **κ(t) check verdict by Monday:** Kills the last design unknown, clarifies whether wave-3 ships or riverbed needs a rebuild. <24 hrs, decisive outcome. DeepSeek.

2. **Demo wired by Friday:** Visible agent-collectives narrative — reading → ledger → display. Shows the quilt-seam + elephant symbiosis live. This is the pitch-deck moment. OpenCode + Kimi.

3. **OAuth scope fix merge + coordinated 47-PR dependabot push:** Closes 150 PRs, proves the fixes hold, establishes the cadence for phase 5. One Casey call (retry greenlight), then one coordinated day. Highest-velocity visibility.

**Why these three?** They buy credibility (1), narrative (2), and closure (3) in 72 hours, with no new math and mostly assigned work. The rest of the quarter becomes building, not proving.

---

**Tone for Casey:** Two gate decisions unlock everything else. Get those Friday, and the fleet ships the agent-collectives thesis + a live demo by Sept 3.
