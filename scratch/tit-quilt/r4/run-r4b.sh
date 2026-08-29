#!/bin/bash
# TIT round 4b: judging — 3 yards + deepseek rank the three answers per question, name THE build-critical decision
set -e
cd ~/.openclaw/workspace/scratch/tit-quilt/r4 || exit 1

# clean kimi answer at its END ANSWER marker (line number computed dynamically)
MARK=$(grep -n 'END ANSWER' r4a-kimi.md | head -1 | cut -d: -f1)
head -n "$MARK" r4a-kimi.md > r4a-kimi.clean.md

{
cat <<'EOF'
ROUND 4b — JUDGING ROUND. The three yards below answered the two fault-line questions (Q1 MCP ergonomics; Q2 the session daemon). Rank the answers PER QUESTION — 1st, 2nd, 3rd, one sharp paragraph per ranking (two ranking lists total). Then name THE build-critical decision — the single decision this build must get right before any code is written, and why. Judge like an owner commissioning the build: brutal, specific, buildability over cleverness. One of these answers may be your own — rank it on merit or lose credibility. Sign your model name.

=== ANSWER 1 — claude (Haiku 4.5) ===
EOF
cat r4a-claude.md
cat <<'EOF'

=== ANSWER 2 — kimi ===
EOF
cat r4a-kimi.clean.md
cat <<'EOF'

=== ANSWER 3 — opencode (GLM-5.3) ===
EOF
cat r4a-opencode.md
} > r4b-prompt.md

wc -w r4b-prompt.md

claude  -p "$(cat r4b-prompt.md)" > r4b-claude.md  2>&1 &
J1=$!
kimi    -p "$(cat r4b-prompt.md)" > r4b-kimi.md    2>&1 &
J2=$!
opencode run --auto "$(cat r4b-prompt.md)" > r4b-opencode.md 2>&1 &
J3=$!
KEY=$(grep -oP 'DEEPSEEK_API_KEY="?\K[^"]+' ~/.bashrc | head -1)
jq -n --arg s "$(cat r4b-prompt.md)" '{model:"deepseek-chat",messages:[{role:"user",content:$s}],max_tokens:1500}' > ds-r4-req.json
curl -s https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $KEY" \
  -d @ds-r4-req.json -o ds-r4.json &
J4=$!
echo "spawned judges: claude=$J1 kimi=$J2 opencode=$J3 deepseek=$J4"
wait
jq -r '.choices[0].message.content // .error.message // .' ds-r4.json > r4b-deepseek.md
wc -w r4b-*.md
