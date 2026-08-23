#!/usr/bin/env bash
# Fleet Feedback Digest — do the other agents USE my work?
# Lucineer's audience is the fleet. This scan answers: what landed, what got
# consumed, what got cited, what's ignored. Run daily; digest to memory.
set -u
PROJECTS=/home/eileen/projects
OUT=/home/eileen/.openclaw/workspace/memory/fleet-feedback-$(date +%Y-%m-%d).md
TODAY=$(date +%Y-%m-%d)

{
echo "# Fleet Feedback Digest — $TODAY"
echo
echo "*The other agents are the audience. What did they consume?*"
echo

# 1) CROSS-REPO CONSUMPTION: who references our live artifacts?
echo "## 1. Cross-repo consumption (code/docs referencing elephant artifacts)"
for pat in "vibe_state" "cell_ledger" "room.field" "record_with" "enable_ledger"; do
  hits=$(grep -rln "$pat" $PROJECTS/{quilt,quilt-cell-bridges,quilt-rust,superinstance-website,crab-traps,collective-unconscious,flux-runtime} \
    --include="*.py" --include="*.ts" --include="*.js" --include="*.md" 2>/dev/null | grep -v node_modules | grep -v ".git/" | head -5)
  if [ -n "$hits" ]; then
    echo "- **$pat**: $(echo "$hits" | wc -l | tr -d ' ') file(s) — $(echo "$hits" | sed 's|.*/projects/||' | tr '\n' ' ' | cut -c1-160)"
  else
    echo "- **$pat**: no cross-repo references yet"
  fi
done
echo

# 2) ADOPTION: did the spearhead pick up our handoffs?
echo "## 2. Handoff adoption (v* / COH / fascia / REG-1 in other agents' work)"
for pat in "v\*" "vstar" "cohesion" "COH" "fascia" "REG-1" "volume.*presence"; do
  hits=$(grep -rln -E "$pat" $PROJECTS/{quilt,quilt-cell-bridges,quilt-rust,superinstance-website,collective-unconscious} \
    --include="*.py" --include="*.ts" --include="*.md" 2>/dev/null | grep -v node_modules | grep -v ".git/" | head -5)
  if [ -n "$hits" ]; then
    echo "- **$pat**: $(echo "$hits" | sed 's|.*/projects/||' | tr '\n' ' ' | cut -c1-160)"
  else
    echo "- **$pat**: not adopted yet"
  fi
done
echo

# 3) LIVE WIRE: is /vibe_state actually serving data?
echo "## 3. Live wire (vibe_state endpoint)"
vibe=$(curl -s --max-time 8 "https://crab-trap-funnel.casey-digennaro.workers.dev/vibe_state" 2>/dev/null | head -c 200)
if [ -n "$vibe" ]; then
  echo "- /vibe_state: LIVE — $(echo "$vibe" | grep -oE '"[a-z]+"' | head -5 | tr '\n' ' ')"
else
  echo "- /vibe_state: DOWN"
fi
dials=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 "https://crab-trap-funnel.casey-digennaro.workers.dev/dials" 2>/dev/null)
echo "- /dials dashboard: HTTP $dials"
echo

# 4) PR REVIEWS: are our PRs being reviewed/merged by others?
echo "## 4. PR state (our lanes)"
for pr in "flux-runtime:28"; do
  repo="${pr%:*}"; n="${pr#*:}"
  state=$(gh pr view "$n" --repo "SuperInstance/$repo" --json state,reviewDecision,mergeable -q '.state+" / reviews:"+(.reviewDecision//"none")+" / "+.mergeable' 2>/dev/null)
  echo "- $repo #$n: $state"
done
echo

# 5) NEW WRITES: did other agents write new content into our shared spaces?
echo "## 5. Shared-space growth (last 24h)"
for d in tap-sessions fragments fleet-radio/songs; do
  cnt=$(find $PROJECTS/ai-writings/$d -newermt "-24 hours" -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "- ai-writings/$d: $cnt new file(s) in 24h"
done
echo

echo "## 6. Signals"
echo "- Interpret: consumption > citation > mention. No references = invisible work."
} > "$OUT"
echo "digest written: $OUT"
cat "$OUT"
