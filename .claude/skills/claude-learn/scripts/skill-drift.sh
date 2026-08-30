#!/bin/bash

set -u

repo=${1:-}
if [ -z "$repo" ] || [ ! -d "$repo" ]; then
  echo "usage: skill-drift.sh <repo-root> [skill-name ...]" >&2
  exit 2
fi
shift || true

L="$repo/.claude/skills"
G="${CLAUDE_GLOBAL_SKILLS:-$HOME/.claude/skills}"

[ -d "$G" ] || { echo "no global skill root at $G" >&2; exit 2; }

is_skill() { [ -f "$1/SKILL.md" ]; }

same_content() {
  diff -q <(tr -d '\r' < "$1") <(tr -d '\r' < "$2") >/dev/null 2>&1
}

tree_status() {
  local g="$1" l="$2" differing=0 onesided=0
  while IFS= read -r rel; do
    if [ -f "$l/$rel" ]; then
      same_content "$g/$rel" "$l/$rel" || differing=$((differing + 1))
    else
      onesided=$((onesided + 1))
    fi
  done < <(cd "$g" && find . -type f ! -path './.*' ! -path '*/__pycache__/*' ! -name '*.pyc' | sed 's|^\./||')
  while IFS= read -r rel; do
    [ -f "$g/$rel" ] || onesided=$((onesided + 1))
  done < <(cd "$l" && find . -type f ! -path './.*' ! -path '*/__pycache__/*' ! -name '*.pyc' | sed 's|^\./||')
  echo "$differing $onesided"
}

if [ "$#" -eq 0 ]; then
  printf '%-34s %-12s %s\n' SKILL STATUS DETAIL
  names=$( { [ -d "$L" ] && ls "$L"; ls "$G"; } 2>/dev/null | sort -u )
  for name in $names; do
    lg="$G/$name"; ll="$L/$name"
    is_skill "$lg" 2>/dev/null || is_skill "$ll" 2>/dev/null || continue
    if [ -d "$lg" ] && [ -d "$ll" ]; then
      read -r differing onesided <<< "$(tree_status "$lg" "$ll")"
      if [ "$differing" -eq 0 ] && [ "$onesided" -eq 0 ]; then
        printf '%-34s %-12s %s\n' "$name" synced ""
      else
        printf '%-34s %-12s %s\n' "$name" diverged "$differing differing, $onesided one-sided"
      fi
    elif [ -d "$lg" ]; then
      printf '%-34s %-12s %s\n' "$name" global-only "pull to share with the team"
    else
      printf '%-34s %-12s %s\n' "$name" local-only "repo-specific, or never pushed"
    fi
  done
  exit 0
fi

for name in "$@"; do
  lg="$G/$name"; ll="$L/$name"
  echo "### $name"
  if [ ! -d "$lg" ]; then echo "  local-only, no global counterpart"; continue; fi
  if [ ! -d "$ll" ]; then echo "  global-only, not pulled into this repo"; continue; fi
  printf '  %-52s %8s %8s\n' FILE 'ONLY-G' 'ONLY-L'
  while IFS= read -r rel; do
    if [ ! -f "$ll/$rel" ]; then
      printf '  %-52s %8s %8s\n' "$rel" "$(wc -l < "$lg/$rel")" "absent"
      continue
    fi
    same_content "$lg/$rel" "$ll/$rel" && continue
    d=$(diff <(tr -d '\r' < "$lg/$rel") <(tr -d '\r' < "$ll/$rel"))
    printf '  %-52s %8s %8s\n' "$rel" "$(printf '%s' "$d" | grep -c '^<')" "$(printf '%s' "$d" | grep -c '^>')"
  done < <(cd "$lg" && find . -type f ! -path './.*' ! -path '*/__pycache__/*' ! -name '*.pyc' | sed 's|^\./||' | sort)
  while IFS= read -r rel; do
    [ -f "$lg/$rel" ] || printf '  %-52s %8s %8s\n' "$rel" "absent" "$(wc -l < "$ll/$rel")"
  done < <(cd "$ll" && find . -type f ! -path './.*' ! -path '*/__pycache__/*' ! -name '*.pyc' | sed 's|^\./||' | sort)
done
