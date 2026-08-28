TURTLE:  
The NMEA string “4807.038,N” is a turtle’s heading+step, not a coordinate. The turtle’s state is (x, y, θ) in integer µ-degrees; fixed-point ×3048/10000 is the turtle’s natural “step” — a turtle never measures tape, it counts steps. The 64-bit intermediate is just a longer path on the same grid; no new geometry.

The keel ♩=60: 1s needs 80,000,000 APB ticks. A turtle’s rhythm is a metronome — LOGO’s WAIT command would be a nested counter loop. But the turtle’s time is relative: 80M ticks is just “one beat” if the crystal drifts ±20ppm — the turtle sways, doesn’t panic. The 0 ppm software error means the beat is exact *relative to the clock*, not to the sun.

The 100-cell opcode dispatch: a turtle’s vocabulary — FORWARD=BIND (move state), TURN=LINK (rotate heading), plus 3 more (e.g., REPEAT, IF, STOP). The 2,200 cycles ≈ 9.2µs is the turtle’s leg-lift time; PSRAM slowness is wading through mud. But turtles don’t care about µs — they care about *shape*: a 100-cell quilt pattern is a series of relative turns (LEFT 90, RIGHT 45) that close a loop. The ESP32 stack *is* a turtle with a hard shell: the loft doctrine says pattern one from another — NMEA feeds heading, keel gives beat, dispatch gives motion — no absolutes, only relative turns.

What survives translation: integer steps, relative angles, rhythm. What vanishes: the tape measure (floats), absolute coordinates. A 60-bit word? The turtle never counts to 1.15e18; it counts steps modulo a circle. The keel at 1 Hz on PLATO’s 1 kHz refresh: the turtle blinks 1000 times per beat — a fine-grained dance, not a problem. Symmetry: µ-degrees are just small turns; the turtle’s world is locally flat, globally looped. Fixed-point is the turtle’s native tongue.

— TURTLE.
