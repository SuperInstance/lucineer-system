You are the piano chair in a lab that studies what makes a take sound like Duke Ellington. You are writing ROUND 3. Output ONLY a plainsong score — no commentary before or after, nothing else.

THE PIECE: "Unheard Duke II" — solo piano, C, 112 bpm, 4/4, 16 bars, key of C. The header is already set (swing 66% is handled by the session; do not write a header).

THE ROUND-2 TAKE (the starting point — keep this harmonic skeleton, these pitches, these register answers; you are UPGRADING it, not rewriting it):
@piano | C3-G3-D4 . E4 G4 (rest) C5 . . | vel: 88
@piano | Db3-Ab3-Eb4 . F5 Ab5 Db6 G5 . | vel: 58
@piano | A2-E3-G3-D4 . . G4 . F4 E4 . | vel: 66
@piano | G2-F3-B3-E4 . A4 . B4 (rest) D4 E4 | vel: 74
@piano | (rest) C3-G3-D4 . E4 G4 (rest) C5 . | vel: 88
@piano | (rest) (rest) Eb6 . D6 B5 . (rest) . | vel: 56
@piano | F3-Ab3-C4-E4 . Gb3-B3-Db4-F4 . G3-B3-D4-F4 . A5 . | vel: 82
@piano | G2-F3-Ab3-B3 (rest) (rest) D5 (rest) (rest) (rest) (rest) | vel: 95
@piano | Db4-F4-Ab4-C5 . . . Eb6 Db6 C6 Ab5 | vel: 54
@piano | E3-G#3-B3-D5 . . D5 C6 . B5 . | vel: 58
@piano | A2-G3-B3-E4 . . C#4-E4-G4-B4 . A4 . . | vel: 70
@piano | D3-F3-C4-E4 . Db3-F3-Ab3-B3 . B4 (rest) G3-B3 . | vel: 76
@piano | C2-G2-D3 . E3 G3 (rest) C3 . . | vel: 92
@piano | Db3-Ab3-Eb4 (rest) (rest) G3-B3-F4 (rest) (rest) (rest) (rest) | vel: 62
@piano | C3-G3-Eb4 . D4 . Eb6 D6 B4 (rest) | vel: 68
@piano | C2-G2 . . B3-D4-E4-A4 . . C6 . | vel: 50

WHAT THE CRITIC SAID SURVIVED ROUND 2 (fix ALL of these):
1. "inside each bar the arm is one weight" — each bar had ONE velocity number. The arm never rose or fell WITHIN a bar.
2. "bars 7 and 12 land square" — the planing in bar 7 sits on the beat, and bar 12's pickup (G3-B3) comes a slot early.
3. "this render cannot swing" — the render was pinned at swing 0%. (The session header now carries swing 66%; the render will swing — but your rhythms must still FEEL swung: off-beats placed late, pickups that lean.)

YOUR NEW POWERS (plainsong now supports per-note dynamics):
- A "Vel:" row goes directly under a @piano row. The k-th Vel: token shapes the k-th note-token; "." holds its column (the note keeps the dynamic in hand).
- Vel: marks may be: a number 1-127; pp p mp mf f ff (32/48/64/80/96/112); +N / -N (a change riding on what came before); "!" (twenty louder); "cresc" / "dim" (ramp to the next explicit value in the row, or to ±24 by the row's last note).
- Inline marks also work on the note itself: "C4!" accents by twenty, "C4@99" exact velocity, works on stacks ("G3-B3@84") — marks go BEFORE sustains ("C4!~~~", never "C4~~~!").

ROUND-3 REQUIREMENTS:
- One @piano row per bar, 16 bars, same skeleton as R2 (you may nudge single attacks by ONE slot where the fix demands it — see bars 7 and 12 — but keep the chords, the register answers, the b5 late entry, the b4/b12 pickups).
- Under EVERY @piano row, a Vel: row that shapes dynamics INSIDE the bar: the arm must change weight mid-bar — cresc into a bar's peak, dim away from it, off-beat answers softer or accented darker than downbeats. Do NOT write a single constant per bar; that was round 2's failure. Keep the bar's overall level from R2 (88/58/66/...) as the BASE the marks shape around (a plain number token sets absolute; use it as the anchor).
- Bar 7: displace the planing — the second chord (Gb3-B3-Db4-F4) and the A5 answer should lean LATE (and-of-2 feel): shift the planing chord one slot later than R2 so it lands off the beat, and let the Vel: row accent the displacement.
- Bar 12: the pickup G3-B3 moves to the LAST slot of the bar (a true and-of-4 pickup into bar 13), accented just under the downbeat that follows.
- Bars 15-16: dim the top answers into the lone C6 — the ending exhales.

FORMAT RULES:
- Tokens divide the bar; "." holds, "(rest)" silences, "a-b-c" stacks a chord. Keep token counts per bar equal to R2 unless you shift a slot (then shift, don't add).
- Vel: rows use the same bar-internal token count as their @piano row, aligned token-for-token. "." holds the column.
- Output EXACTLY 16 pairs of lines: a @piano line, then its Vel: line. No header, no section markers, no prose.
