#!/usr/bin/env bash
# fixup: repair misplaced "(dead)" annotations from the first apply pass.
# POSIX sed leftmost-longest let the annotate rule span multiple links on a line.
# Verified: zero pre-existing ") (dead)" in any parent commit, so stripping all
# link-adjacent annotations and re-adding with corrected ([^()]) rules is safe.
set -u
ROOT=/home/eileen/projects
LOG=/home/eileen/.openclaw/workspace/org-sweep/apply.log
EXCL_RE='(^|/)(node_modules|\.git|target|dist|build|vendor)/'

FIX=$(mktemp /tmp/link-repair-fixup.XXXXXX.sed)
cat > "$FIX" <<'SEDEOF'
# strip ALL link-adjacent annotations (ours; none pre-existed)
s@(\]\([^()]*\)) \(dead\)@\1@g
# strip bare-url annotations (ours were correct, but re-added below)
s@(SuperInstance/(the-living-minds|wesley-journal|forgemaster|compaction-teacher|flow-state)([^A-Za-z0-9_-][A-Za-z0-9._/~#-]*)?) \(dead\)@\1@g
# re-add: bare urls (not inside links, not in link definitions)
/^[[:space:]]*\[[^]]*\]:/!s@([^("'])(https?://github\.com/SuperInstance/(the-living-minds|wesley-journal|forgemaster|compaction-teacher|flow-state)([^A-Za-z0-9_-][A-Za-z0-9._/~#-]*)?)@\1\2 (dead)@g
# re-add: inline links (paren-bounded)
s@\]\(([^()]*SuperInstance/(the-living-minds|wesley-journal|forgemaster|compaction-teacher|flow-state)([^A-Za-z0-9_-][^()]*)?)\)@](\1) (dead)@g
SEDEOF

while IFS=$'\t' read -r _ repo _rest; do
  dir="$ROOT/$repo"
  mapfile -t files < <(git -C "$dir" ls-files '*.md' | grep -vE "$EXCL_RE")
  [ ${#files[@]} -eq 0 ] && continue
  rel=$(grep -lE '\(dead\)|SuperInstance/(the-living-minds|wesley-journal|forgemaster|compaction-teacher|flow-state)([^A-Za-z0-9_-]|$)' -- "${files[@]/#/$dir/}" 2>/dev/null | sed "s|^$dir/||" || true)
  [ -z "$rel" ] && continue
  changed=()
  while IFS= read -r f; do
    before=$(md5sum "$dir/$f" | cut -d' ' -f1)
    sed -E -i -f "$FIX" "$dir/$f"
    after=$(md5sum "$dir/$f" | cut -d' ' -f1)
    [ "$before" != "$after" ] && changed+=("$f")
  done <<< "$rel"
  if [ ${#changed[@]} -gt 0 ]; then
    git -C "$dir" add -- "${changed[@]}"
    if git -C "$dir" commit -q --amend --no-edit; then
      printf 'AMENDED\t%s\t%s files\t%s\n' "$repo" "${#changed[@]}" "$(git -C "$dir" rev-parse --short HEAD)"
    else
      printf 'AMEND_FAILED\t%s\n' "$repo"
    fi
  else
    printf 'UNCHANGED\t%s\n' "$repo"
  fi
done < <(grep '^COMMITTED' "$LOG")

rm -f "$FIX"
