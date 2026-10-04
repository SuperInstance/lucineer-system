# eco-quiltverilog — SPIN-49/50 record recovered from unwritten WHEEL-LOG (2026-09-04 07:2x AKDT)

The quilt-verilog working tree is being concurrently mutated by a second actor
(branch switches master↔g3-kinduction, resets onto eco-quiltverilog's commits,
a mid-merge conflict in flight at time of writing). The wheel/ working log could
not be safely edited, so this holds the entries that belong in
spikes/225-e1-interference-tick/wheel/WHEEL-LOG.md once the tree stabilizes.

## SPIN-49-ADVERSARY — verdict (verified against spin49-adversary-output.txt)
- Attempt 1: LOST ("lost active execution context", 7m50s, zero output) — INCONCLUSIVE, scar booked (3rd silent lane death; detached-runner fix recommended).
- Attempt 2: COMPLETED. **H1 VALIDATED / H2 FALSIFIED / H3 VALIDATED.**
  - H1: D6 per-cell monotone emission counter at ingress catches the spoof storm — 0/~142k spoofed flits accepted, honest FPR 0 (5/5 seeds × 4/4 cells), residency returns to honest null. SPIN-47's spoofing crack CLOSED.
  - H2: self-attributed flood vs envelope-calibrated quota (Q=39–52) — FALSIFIED: ~63% of flood admitted, honest residency −18.2 to −89.4pp. Ledger prices drops correctly to the liar (0 honest drops), but at those quotas it prices RATE, not provenance (exploratory: Q=1 holds ≤1.2pp, Q=2 holds 3/4).
  - H3: coalition spoof+declare hybrid caught 5/5 seeds (D6 drop-ledger + per-cell D5), honest cells clean.
  - Headline: attribution solved; volume denial by an honestly-attesting flooder is unsolved — attribution ≠ congestion pricing.
  - Boundaries: D6 catch is structural (counter-state asymmetry, not key compromise); H2 partly a pre-registered-design artifact; honResΔ inflated by ~99%-saturated baseline.
  - Canaries ALL PASS. Files: SPIN-49-adversary.md + spin49_adversary.py + spin49-adversary-output.txt (all on disk, untracked).
- LCG state after SPIN-49: 1860847622 → next 1448521415, mod 10 = 5 (CONSERVATION).

## SPIN-50-CONSERVATION — brief (NOT dispatched; tree unstable)
- Lane would be wheel_spin50_conservation (zai/glm-5.3, run mode) — SPIN-49's booked law-candidate (Q-operating curve).
- Brief: Q ∈ {1,2,4,8,16,32,envelope} × flood rate {0.5×,1×,2×} × grammars {zero, ladder@15, kcoh5@15} × K ∈ {1,2}. H1: honest-residency protection collapses to one curve of price-to-flood ratio across grammars (band ε); FALSIFY on grammar departure >ε. H2: ledger price exactly conserved (Σ liar-priced drops == Σ flood excess over Q) on every arm — SPIN-15 identity for the quota channel; FALSIFY on any unpriced drop. Canaries: spin49_adversary.py byte-identity replays, anchors 77.3/187834/8756 + 71.5/5792/106378, gate=never ≡ mc=0, SPIN-15 asserts live, double-run determinism. Seeds 1/7/42/1999/20260902. Deliverable wheel/SPIN-50-conservation.md.

## Incident escalation (needs Casey's call)
Two workers shared /home/eileen/projects/quilt-verilog today: eco-quiltverilog
(wheel spike) and an O4/round-4 actor (dev-rounds, g3-kinduction). Effects:
pull --rebase orphaned unpushed rounds (recovered via reflog, dd2a148 — which
the other lane then built on), working-tree rewrites mid-lane, and now an
unresolved merge conflict. Recommendation: one git worktree per lane, or a
serialization rule on the shared checkout. Nothing was destroyed — every commit
survives as an object.
