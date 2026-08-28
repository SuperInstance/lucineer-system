# The Seam: Sampling Rate as Design Primitive

**What only the control-theory angle sees:**

TURING and TURTLE describe the same phenomenon in different languages—tape vs. geometry, O(log N) vs. "no new grid"—but both assume the word size is *given*. TUTOR makes it chosen. Yet none of them notice that **60-bit is not a compression of 64-bit, it's a *resonance*.**

The µ-degree overflow trap vanishes not because PLATO had infinite tape (TURING) or didn't need precision (TURTLE), but because **at 1 kHz refresh, the time constant of drift is shorter than the control loop**. Parsing NMEA every frame means your heading estimate resets 1,000 times per second. You cannot accumulate error faster than you erase it. The 60-bit word is not a limit—it's a tuning dial. Smaller precision, faster feedback; they cancel. TUTOR glimpsed this (interactivity > drift), but phrased it as pedagogy. TURING's O(log N) binary counter is *faster*, but the keel still swings ±20ppm because *the counter runs once per 80M ticks*, not once per millisecond.

**The convergence:**

TURING's information-theoretic floor (11 cycles/edge), TURTLE's steady-state sway (±20ppm metronome), and TUTOR's 1 kHz parse together prove that **in any closed-loop system, bandwidth of measurement beats precision of storage**—the stack's ceiling is not arithmetic width or state space, but how often the world is allowed to correct itself.

***— Control angle*
