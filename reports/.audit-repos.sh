#!/bin/bash
# Read-only repo audit. Collects remote, dirty count, branch/upstream, ahead count,
# last commit date, and size (excluding node_modules and .git) for each dir.
OUT=/tmp/repo-audit.tsv
: > "$OUT"

audit() {
  local d="$1"
  local name="${d#/home/eileen/}"
  name="${name%/}"
  if ! git -C "$d" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$d" "no-git" "-" "-" "-" "-" "-" "-" "-" >> "$OUT"
    return
  fi
  local remote rfirst
  remote=$(git -C "$d" remote get-url origin 2>/dev/null)
  if [ -z "$remote" ]; then
    rfirst=$(git -C "$d" remote 2>/dev/null | head -1)
    [ -n "$rfirst" ] && remote=$(git -C "$d" remote get-url "$rfirst" 2>/dev/null)
  fi
  local dirty branch up ahead last size
  dirty=$(git -C "$d" status --porcelain 2>/dev/null | wc -l)
  branch=$(git -C "$d" branch --show-current 2>/dev/null)
  [ -z "$branch" ] && branch="DETACHED:$(git -C "$d" rev-parse --short HEAD 2>/dev/null)"
  up=$(git -C "$d" rev-parse --abbrev-ref '@{u}' 2>/dev/null)
  if [ -n "$up" ]; then
    ahead=$(git -C "$d" rev-list --count '@{u}..HEAD' 2>/dev/null)
  else
    ahead="no-upstream"
  fi
  last=$(git -C "$d" log -1 --format=%cs 2>/dev/null)
  [ -z "$last" ] && last="no-commits"
  size=$(du -sh --exclude=node_modules --exclude=.git "$d" 2>/dev/null | cut -f1)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$name" "$d" "git" "${remote:-NONE}" "$dirty" "$branch" "${up:-none}" "$ahead" "$last" "$size" >> "$OUT"
}
export -f audit
export OUT

dirs=(/home/eileen/projects/*/ /home/eileen/ai-writings /home/eileen/plainsong /home/eileen/plainsong-mcp /home/eileen/the-tap /home/eileen/fleet-static-host)
printf '%s\n' "${dirs[@]}" | xargs -P 8 -I{} bash -c 'audit "$@"' _ {}
echo "AUDIT_DONE lines=$(wc -l < "$OUT")"
