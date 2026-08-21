#!/usr/bin/env bash
# org-wide link repair — scout phase 2 follow-up
# usage: link-repair.sh [dry|apply]
set -u
ROOT=/home/eileen/projects
MODE=${1:-dry}
SKIP_REPOS=" ai-writings researchlocal-backup "
EXCL_RE='(^|/)(node_modules|\.git|target|dist|build|vendor)/'

RULES=$(mktemp /tmp/link-repair-rules.XXXXXX.sed)
cat > "$RULES" <<'SEDEOF'
# --- protections: domains, filenames, local clone paths (marker LKRPR breaks literal match) ---
s@fleet-wiki\.@fleet-LKRPR-wiki.@g
s@mud-arena\.(cu|md)\b@mud-LKRPR-arena.\1@g
s@(/home/[A-Za-z0-9._/-]+/projects/)hermes-perception@\1hermes-LKRPR-perception@g
s@(/home/[A-Za-z0-9._/-]+/projects/)lucineer-brain@\1lucineer-LKRPR-brain@g
s@(/home/[A-Za-z0-9._/-]+/projects/)log-tensor@\1log-LKRPR-tensor@g
s@(/home/[A-Za-z0-9._/-]+/projects/)tensor-midi@\1tensor-LKRPR-midi@g
s@(/home/[A-Za-z0-9._/-]+/projects/)ternary-tenforward@\1ternary-LKRPR-tenforward@g
s@(/home/[A-Za-z0-9._/-]+/projects/)mud-arena@\1mud-LKRPR-arena@g
# --- master->main: only plato-training (verified: remote default=main) ---
s@(github\.com/SuperInstance/plato-training/(blob|tree))/master/@\1/main/@g
# --- repo renames ---
s@\bhermes-perception\b@hermes-avatar@g
s@\bofficers-quarters\b@elephant@g
s@\bopenconstruct-kernel\b@OpenConstruct@g
s@\blucineer-brain\b@lucineer-system@g
s@\bternary-tenforward\b@confidence-cascade@g
s@\blog-tensor\b@murmur@g
s@\btensor-midi\b@fleet-jepa-midi@g
s@\bmud-arena\b@mud-engine@g
s@\bluciddreamer-vision\b@lucid-dreamer@g
s@(^|[^A-Za-z0-9_-])fleet-wiki\b@\1lucineer-fleet-wiki@g
s@(github\.com/SuperInstance/)EXOCORTEX\b@\1exocortex-core@g
s@(github\.com/SuperInstance/)zeroclaw\b@\1zeroclaw-dissertation@g
# --- dead-repo annotation (idempotent: strip then re-add) ---
s@\]\(([^)]*SuperInstance/(the-living-minds|wesley-journal|forgemaster|compaction-teacher|flow-state)\b[^)]*)\) \(dead\)@](\1)@g
s@(SuperInstance/(the-living-minds|wesley-journal|forgemaster|compaction-teacher|flow-state)\b[A-Za-z0-9._/~#-]*) \(dead\)@\1@g
/^[[:space:]]*\[[^]]*\]:/!s@([^("'])(https?://github\.com/SuperInstance/(the-living-minds|wesley-journal|forgemaster|compaction-teacher|flow-state)\b[A-Za-z0-9._/~#-]*)@\1\2 (dead)@g
s@\]\(([^)]*SuperInstance/(the-living-minds|wesley-journal|forgemaster|compaction-teacher|flow-state)\b[^)]*)\)@](\1) (dead)@g
# --- restore protections ---
s@-LKRPR-@-@g
SEDEOF

# grep patterns for per-category dry-run counts (order matches report columns)
CAT_NAMES=(
  "master->main"
  "hermes-perception" "officers-quarters" "openconstruct-kernel" "lucineer-brain"
  "ternary-tenforward" "log-tensor" "tensor-midi" "mud-arena"
  "luciddreamer-vision" "fleet-wiki" "EXOCORTEX" "zeroclaw"
  "dead-annotate"
)
CAT_PATTERNS=(
  'github\.com/SuperInstance/plato-training/(blob|tree)/master/'
  '\bhermes-perception\b'
  '\bofficers-quarters\b'
  '\bopenconstruct-kernel\b'
  '\blucineer-brain\b'
  '\bternary-tenforward\b'
  '\blog-tensor\b'
  '\btensor-midi\b'
  '\bmud-arena\b'
  '\bluciddreamer-vision\b'
  '(^|[^A-Za-z0-9_-])fleet-wiki\b'
  'github\.com/SuperInstance/EXOCORTEX\b'
  'github\.com/SuperInstance/zeroclaw\b'
  'github\.com/SuperInstance/(the-living-minds|wesley-journal|forgemaster|compaction-teacher|flow-state)\b'
)
COMBINED=$(IFS='|'; echo "${CAT_PATTERNS[*]}")

COMMIT_MSG="docs: org-wide link repair — repo renames + master→main (scout phase 2)"

for dir in "$ROOT"/*/; do
  repo=${dir%/}; name=${repo##*/}
  [ -d "$repo/.git" ] || continue
  case "$SKIP_REPOS" in *" $name "*) continue;; esac

  # tracked *.md files, minus excluded dirs and symlinks
  mapfile -t files < <(git -C "$repo" ls-files '*.md' | grep -vE "$EXCL_RE" | while IFS= read -r f; do [ -L "$repo/$f" ] || printf '%s\n' "$f"; done)
  [ ${#files[@]} -eq 0 ] && continue

  # fast path: any rule match at all?
  rel_matches=$(grep -lE "$COMBINED" -- "${files[@]/#/$repo/}" 2>/dev/null | sed "s|^$repo/||" || true)
  [ -z "$rel_matches" ] && continue

  if [ "$MODE" = dry ]; then
    counts=(); total=0
    for p in "${CAT_PATTERNS[@]}"; do
      c=$(printf '%s\n' "$rel_matches" | sed "s|^|$repo/|" | tr '\n' '\0' | xargs -0 grep -ohE "$p" 2>/dev/null | wc -l)
      counts+=("$c"); total=$((total+c))
    done
    nfiles=$(echo "$rel_matches" | wc -l)
    printf '%s\t%s\t%s' "$name" "$nfiles" "$total"
    for c in "${counts[@]}"; do printf '\t%s' "$c"; done
    printf '\n'
  else
    # apply
    changed=()
    while IFS= read -r f; do
      before=$(md5sum "$repo/$f" | cut -d' ' -f1)
      sed -E -i -f "$RULES" "$repo/$f"
      after=$(md5sum "$repo/$f" | cut -d' ' -f1)
      [ "$before" != "$after" ] && changed+=("$f")
    done <<< "$rel_matches"
    if [ ${#changed[@]} -gt 0 ]; then
      git -C "$repo" add -- "${changed[@]}" 2>/dev/null
      if git -C "$repo" commit -q -m "$COMMIT_MSG" 2>/dev/null; then
        hash=$(git -C "$repo" rev-parse --short HEAD)
        printf 'COMMITTED\t%s\t%s files\t%s\n' "$name" "${#changed[@]}" "$hash"
        printf '%s\n' "${changed[@]}" | sed "s|^|  FILE\t$name\t|"
      else
        printf 'COMMIT_FAILED\t%s\t%s files staged\n' "$name" "${#changed[@]}"
      fi
    fi
  fi
done

rm -f "$RULES"
