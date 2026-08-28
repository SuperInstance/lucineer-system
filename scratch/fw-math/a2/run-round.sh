#!/bin/bash
# angle round: TUTOR (claude) / TURING (kimi) / TURTLE (deepseek)
cd ~/.openclaw/workspace/scratch/fw-math/a2 || exit 1

claude -p "$(cat seed2-TUTOR.md)" > a2-claude.md 2>&1 &
CPID=$!

kimi -p "$(cat seed2-TURING.md)" > a2-kimi.md 2>&1 &
KPID=$!

KEY=$(grep -oP 'DEEPSEEK_API_KEY="?\K[^"]+' ~/.bashrc | head -1)
curl -s https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $KEY" \
  -d "$(jq -n --arg s "$(cat seed2-TURTLE.md)" '{model:"deepseek-chat",messages:[{role:"user",content:$s}],max_tokens:700}')" \
  -o ds-a2.json
jq -r '.choices[0].message.content // .error.message // .' ds-a2.json > a2-deepseek.md &
DPID=$!

wait $CPID $KPID $DPID
wc -w a2-*.md
