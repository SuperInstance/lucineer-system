ROUND-TABLE SEED — the math of the ESP32 framework synergy, from the assembly up.

FACTS (verified):
1. rspurlock/framework-arduinoespressif32 = repackaged Arduino-ESP32 core v4.4 (PlatformIO package; 7 commits; default config; no custom patches visible in cores/).
2. quilt-esp32 builds 5 PlatformIO envs (esp32dev, esp32s3, reflex_arc, nmea, eileen) on framework=arduino, compiling C files: qm_opcodes.c (the 5+1 opcodes BIND/LINK/EFFECT/VIEW/TICK/FORGET), qm_serve.c, NMEA 0183 byte-at-a-time parser, eileen_main.cpp (keel blinks ♩=60).
3. Targets: ESP32 (Xtensa LX6) and ESP32-S3 (Xtensa LX7, 240MHz, 512KB SRAM, no FPU).

THE QUESTION, TO BE ANSWERED ITERATIVELY — round 1 (each model answers fresh, no peeking):
"From the assembly up: what is the actual mathematical content of the quilt-on-ESP32 stack? Take ONE layer — qm_opcodes.c compiling to Xtensa LX7 instructions (which instruction sequences implement BIND/LINK/EFFECT/VIEW/TICK/FORGET? what does the compiler actually emit?), OR the NMEA byte-parser's arithmetic (micro-degrees integer math, no floats — what are the overflow bounds? how do you do lat/lon in 32-bit ints without FPU?), OR the keel-timing math (♩=60 blink = 1s period on a 240MHz core — timer math, clock divider exactness, drift per hour). Give the REAL equations and instruction-level reasoning. Then state ONE synergy claim: what does repackaged-vs-custom change about this stack's math, if anything?"
Answer in ≤300 words, equations in plaintext. Sign your model name.
