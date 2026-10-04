#!/usr/bin/env bash
# quilc referee experiment: models author QUIL programs blind; quilc scores.
# Usage: bash exp_quilc_referee.sh <model-label> <generate-command...>
# The generate command receives the prompt on stdin and must print ONLY the .quil program.
set -u
LABEL="$1"; shift
PROMPT_FILE="$(dirname "$0")/exp_prompt.txt"
OUT_DIR="$(dirname "$0")/exp-out/$LABEL"
mkdir -p "$OUT_DIR"
declare -A TASKS=( [counter]="a single cell 'ticks' of width 16 that increments once per tick, plus a view 'even' returning 1 when it is even" \
 [fanout3]="one source cell 'src' (width 8, self-incrementing) bound to three sink cells s1 s2 s3 of width 8, with fan-out 3 declared" \
 [propose]="a helm cell 'acc' (width 32) fed by a propose input port named 'pred' — the port proposes, the tick consumes it into the journal" )
PASS=0; TOTAL=0
for t in counter fanout3 propose; do
  P="$(cat "$PROMPT_FILE")

TASK: write a complete QUIL program for: ${TASKS[$t]}
Output ONLY the program text, no markdown fences, no commentary."
  "$@" <<< "$P" > "$OUT_DIR/$t.quil" 2>"$OUT_DIR/$t.err"
  if python3 /home/eileen/projects/quilt-verilog/tools/quilc.py check "$OUT_DIR/$t.quil" >"$OUT_DIR/$t.check" 2>&1; then
    R=PASS; PASS=$((PASS+1))
  else R=FAIL; fi
  TOTAL=$((TOTAL+1))
  echo "$LABEL/$t: $R ($(grep -c 'error' "$OUT_DIR/$t.check" 2>/dev/null || echo 0) errors)"
done
echo "RESULT $LABEL: $PASS/$TOTAL valid"
