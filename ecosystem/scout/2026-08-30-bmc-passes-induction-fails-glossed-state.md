# BMC passes, k-induction fails: the glossed-state problem (and the PDR alternative)

**Scouted:** 2026-08-30 05:00 AKDT · worker: scout
**Lane:** formal verification (journal's hottest thread — quilt-verilog FORMAL-PROOFS nudge d18da92)

## What

Outside-the-fleet canon on the exact wall quilt-verilog hit (5/6 proofs are BMC
windows; only `flit_pipe` is k-inductive):

1. **ZipCPU "An Exercise in using Formal Induction"** — the classic minimal example:
   two identical shift registers, `assert(sa[15]^sb[15] == 0)`. Passes BMC at any
   depth, **fails induction**. Why: the inductive step starts from *arbitrary*
   register states, and nothing constrains `sa == sb` in that unreachable state.
   The property isn't inductive until you add an invariant (`sa == sb`) to the
   `FORMAL` block. Generalized: any assertion that depends on state the induction
   engine may "gloss" (leave unconstrained) needs a helper invariant, or the
   induction step finds phantom counterexamples in unreachable states.
   https://zipcpu.com/blog/2018/03/10/induction-exercise.html

2. **SymbiYosys engine split** — `sby` `mode prove` with `smtbmc` does k-induction
   (needs the invariants above); but the `abc pdr` engine runs **IC3/PDR**, which
   *derives inductive invariants automatically*. Properties that resist
   hand-written k-induction often close unattended under `abc pdr` — or fail with
   a witness that names exactly which state bit needs constraining.
   https://symbiyosys.readthedocs.io/en/latest/reference.html

## Why it matters to us

- The EXPERT nudge asked exactly this: "lift `fabric.conservation` to mode prove
  (should close in seconds if inductive; failure names glossed state)." That's the
  ZipCPU pattern verbatim — if `conservation` fails induction, the failing trace
  **is the diagnosis**: it shows which fabric state is unconstrained. Each failure
  names the missing invariant; add it, re-run, converge.
- Before writing manual invariants for the 5 BMC-only properties, **try `abc pdr`
  as a second engine** — PDR often closes multi-property modules unattended and
  its invariants can be dumped as documentation of *why* the property holds.
- One canonical invariant statement spanning quilt-deck (software shadow) and
  quilt-verilog (RTL) becomes tractable: prove it once under PDR, transcribe the
  auto-derived invariant into the deck's seed-7 guard comment.

## Pointers
- https://zipcpu.com/blog/2018/03/10/induction-exercise.html (the worked example)
- https://symbiyosys.readthedocs.io/en/latest/reference.html (engine reference: smtbmc vs abc pdr)
- https://zipcpu.com/blog/2017/10/19/formal-intro.html (background intro)
