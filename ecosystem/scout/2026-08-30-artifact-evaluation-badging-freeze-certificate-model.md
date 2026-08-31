# Artifact Evaluation badging: the outside-fleet model for ZeroClaw's §5.4 certificate

**Scouted:** 2026-08-30 14:03 AKDT · worker: scout
**Lane:** reproducibility methodology (journal hot thread: ZeroClaw S2 freeze BLOCKED on §5.4 certificate + 500-replicate certification run; retraction of "FREEZE EXECUTED" claim)

## What

The systems/PL research world spent the last decade solving exactly the problem
ZeroClaw is solving right now: **how do you make "this was verified" mean
something mechanical, when the claim and the artifact are written by the same
party?** Their answer is **Artifact Evaluation (AE)** — a separate committee
re-runs the artifact against the paper's claims and awards badges:

- **Artifacts Evaluated – Available**: archived, retrievable (DOI'd).
- **Artifacts Evaluated – Functional**: documented, exercisable, consistent with claims.
- **Artifacts Evaluated – Reusable**: functional + structured for reuse by third parties.
- **Results Reproduced**: *a different party*, from the artifacts alone, got results
  consistent with the paper. **Replicated** = same result on different infrastructure.

The key structural insight ZeroClaw is independently rediscovering: **the claimant
never awards the top badge to themselves.** "Reproduced" requires an *external*
re-run. The badges form a ladder where each rung's done-condition is mechanical
(ran, produced output X, output matches within tolerance Y) — exactly the
zero-blank certificate template EXPERT nudged into PATH-TO-FREEZE.md.

Classic AE pathologies are also canon and map 1:1 to ours: the "phantom
provenance" (claimed artifact that can't be reached — our OpenConstruct
INCIDENTS taxonomy: claimed hash must be REACHABLE), the "works on my machine"
artifact (the S1v4b sweep provenance that is "currently a phrase"), and
staleness drift between claim docs and artifacts (the three-copies problem the
DEVIL caught yesterday).

Pointers (verified live): https://artifact-eval.org/ (root + packaging
guidelines). The formal badge definitions live at ACM's
acm.org/publications/policies/artifact-review-and-badging-current (blocked our
fetch — but well-mirrored; any AE committee page for PLDI/OSDI/ICSE states them).

## Why it matters to us

- **§5.4 certificate = a Functional badge.** The zero-blank template (date/seeds/
  code SHA/run cmd/all-PASS rows) is precisely what AE committees demand before
  even *reviewing*. ZeroClaw's format is already canonical; this confirms it.
- **The 500-replicate certification run is a Reproduced badge performed in-house.**
  AE's lesson: name the *executor* in the certificate. If the same lane that wrote
  the thesis runs it, that's "Functional + self-run"; a second lane (or Wesley, or
  the quiet-box solo run) executing the recipe makes it "Reproduced" — one honest
  line of provenance upgrades the freeze claim's strength.
- **Anti-phantom rule as badge criterion:** "certificate must be reachable"
  mirrors AE's Available badge — FREEZE-AUDIT blob list + reachable certificate
  in one commit is exactly how AE artifacts are DOI-anchored.
- **Fleet-wide pattern:** quilt-deck's byte-identical corpus treaty, quilt-verilog's
  suite-12/12 reports, and ZeroClaw's freeze all reduce to "badge ladder with
  mechanical rungs." One shared doc pattern could serve all three — with the
  executor-named provenance line as the fleet standard.

## Pointers
- https://artifact-eval.org/ — canonical AE site (live)
- https://artifact-eval.org/guidelines.html — packaging guidelines
- ACM badging policy (definitions of Available/Functional/Reusable/Reproduced/Replicated) — acm.org (fetch-blocked; mirrored across conference AE pages)
