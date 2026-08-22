#!/bin/bash
GH="/usr/bin/gh"
SHA="/usr/bin/sha256sum"
STATE="/home/eileen/.openclaw/workspace/memory/quilt-synergy-state.sha"
CUR="$("/usr/bin/gh" issue list --repo SuperInstance/quilt --label synergy --state open --json number,updatedAt 2>/dev/null | "/usr/bin/sha256sum" | cut -d' ' -f1)"
CUR2="$("/usr/bin/gh" issue list --repo SuperInstance/quilt-rust --label synergy --state open --json number,updatedAt 2>/dev/null | "/usr/bin/sha256sum" | cut -d' ' -f1)"
HASH="$(printf '%s|%s' "$CUR" "$CUR2")"
if [ -f "$STATE" ] && [ "$(cat "$STATE")" = "$HASH" ]; then
  echo '{"fire": false}'
else
  printf '%s' "$HASH" > "$STATE"
  echo '{"fire": true}'
fi
