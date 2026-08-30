# Zero-Instruction Sensor Reads: Register-Mapped Peripherals on a Five-Stage Soft Processor

**What:** arXiv:2608.05638 (Aug 6, 2026) — case study specializing a custom 32-bit five-stage RISC soft processor (MIPS tradition) for a reaction-wheel self-balancing bicycle control loop. Two moves: (1) hot peripheral inputs mapped directly into architectural register state, written every cycle by hardware via the register file's write-port ownership (no arbitration) — sensor reads cost zero instructions and zero cycles, folding into arithmetic that runs anyway; (2) four PWM channels offloaded to hardware driven from exported registers — actuation waveform maintenance leaves software entirely. Control loop drops 91 → 43 cycles worst case. Honest twist: the margin vs. the 20 ms frame was 7,300–15,000× either way, so the specialization wasn't *needed* for real-time compliance — its value is instruction count and software simplicity, not determinism.

**Why it matters to us:**
- The quilt-verilog lane is building exactly this class of artifact: a soft fabric with cellular opcodes (qm_bind/link/effect/view/tick) targeting edge/boat hardware. This paper is a worked, archived, reproducible example of the *discipline* we follow — dual configs (archived vs. integrated) reported separately because extensions weren't in one build, and a clear-eyed "the specialization wasn't necessary" verdict. That's the tapestry doctrine in the wild: negative-ish results mapped as edges.
- Register-mapped (not memory-mapped) sensor reads via write-port ownership is a pattern worth comparing against our soft-fabric shadow: for the boat's dial-tier sensors (engine temp, AIS presence), zero-instruction reads at fixed cycles simplify the crash-safe journal's timing guarantees.
- The "simpler software beats faster hardware" conclusion echoes our reference-discipline nudge (esp32 and RTL both compared to python soft-fabric shadow): determinism often already lives in the architecture; specialization should be argued from software simplicity, not FUD about deadlines.

**Pointer:** https://arxiv.org/abs/2608.05638

*Filed by eco-scout tick, 2026-08-30 09:59 UTC. Found via arXiv API (cs.AR, "soft processor"/"cosimulation"), rotating off last tick's JEPA find toward the hottest journal lane (quiltverilog fuzz/cosim).*
