#!/usr/bin/env bash
# Sweep push: pushes every repo in final-hashes.tsv (the 88 swept repos).
# Reads repo list, pushes current branch to origin, logs results.
set -u
BASE=/home/eileen/projects
LIST=/home/eileen/.openclaw/workspace/org-sweep/final-hashes.tsv
LOG=/home/eileen/.openclaw/workspace/org-sweep/push.log
: > "$LOG"
ok=0; fail=0
while IFS=$'\t' read -r repo hash; do
  [ -z "$repo" ] && continue
  # skip excluded repos if any appear
  case "$repo" in
    ai-writings|researchlocal-backup|researchlocal|quilt-rust) echo "SKIP $repo (excluded)" | tee -a "$LOG"; continue;;
  esac
  if [ ! -d "$BASE/$repo" ]; then
    echo "MISS $repo (no dir)" | tee -a "$LOG"; fail=$((fail+1)); continue
  fi
  out=$(cd "$BASE/$repo" && git push origin HEAD 2>&1)
  rc=$?
  if [ $rc -eq 0 ]; then
    echo "OK   $repo -> $(cd "$BASE/$repo" && git rev-parse --short HEAD)" | tee -a "$LOG"
    ok=$((ok+1))
  else
    echo "FAIL $repo :: $(echo "$out" | head -2 | tr '\n' ' ')" | tee -a "$LOG"
    fail=$((fail+1))
  fi
done < "$LIST"
echo "=== DONE ok=$ok fail=$fail ===" | tee -a "$LOG"
