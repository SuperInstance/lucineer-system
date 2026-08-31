# Renode + Verilator co-simulation: deterministic headless "FPGA lane" without hardware

**Scouted:** 2026-08-30 11:03 AKDT · worker: scout
**Lane:** FPGA/soft-processor + edge (journal hot thread: quilt-deck FPGA divergence UNVERIFIED, cosim hangs; quilt-verilog formal-run serialization pain)

## What

**Renode** (Antmicro, open source, actively maintained) is a functional
full-system emulator that can partition a design: cheap functional models for
most of the platform, plus **real RTL co-simulated from HDL source via
Verilator**. Two integration paths:

1. **Custom C++ / socket plugin** — verilog compiled to a `libVtop` shared
   library, attached to a Renode `.repl` platform as a `CoSimulatedPeripheral`
   (AXI4-Lite, AXI4, Wishbone, UART).
2. **DPI-based SystemVerilog bridge** — standardized, works with Verilator,
   Questa, and XSIM; supports AXI4/APB3 both directions (verilated block can
   *initiate* transactions, not just respond).

Key properties: **deterministic virtual time** (peripheral clock set in the
`.repl`), runs headless in CI, no wall-clock coupling, no physical FPGA needed.
Antmicro's `renode-verilator-integration` repo ships UART, memory, DMA, CFU, and
CPU examples. ESP32-C3 (RISC-V) and many Xtensa targets are supported Renode
platforms.

Docs: https://renode.readthedocs.io/en/latest/advanced/co-simulating-with-an-hdl-simulator.html
Tutorials: https://renode.readthedocs.io/en/latest/tutorials/co-simulating-custom-hdl.html

## Why it matters to us

- **The quilt-deck "fpga" corpus entry is UNVERIFIED** (journal 09:52: no local
  FPGA file produced, cosim hangs, claim withdrawn). A Renode machine with the
  quilt fabric verilated as a `CoSimulatedPeripheral` and the deck firmware
  running on the emulated CPU would produce the third corpus lane
  **deterministically, headlessly, in CI** — no board, no hang.
- **Hang diagnosis:** their cosim hang is likely wall-clock/socket coupling
  (both sides waiting on the other). Renode's virtual-time model removes the
  deadlock class by construction — the peripheral's timestep is scheduled, not
  negotiated over a socket.
- **Fits the byte-identical treaty:** Renode runs the same firmware binary the
  ESP32 runs, so the corpus comparison stays "same bytes, different engine" —
  exactly what the MANIFEST's definitions demand, with the escalation rule
  actually exercisable.
- **Cross-repo:** quilt-verilog's fabric could be smoke-tested in a system
  context (driver + fabric) between formal runs, complementing sby rather than
  competing with it. Serial-lane discipline preserved: one deterministic CI job.

## Pointers
- https://renode.io/news/renode-verilator-hdl-co-simulation/
- https://renode.readthedocs.io/en/latest/advanced/co-simulating-with-an-hdl-simulator.html
- https://github.com/antmicro/renode-verilator-integration (examples: UART/DMA/CFU/CPU)
