#!/usr/bin/env bash
# Resolve every internal markdown link in a tree and check numbered folders are
# contiguous. The verification pass after any restructure or renumbering.
#
# usage: link-check.sh [--root <dir>] [--scope <subdir>] [--quiet]
#
# Checks:
#   1. every ](target) that is not http(s)/mailto/#anchor resolves to a real path,
#      relative links against the file's own directory, /-anchored against --root
#   2. every numbered sibling set (NN-name) runs 01..NN with no gap and no duplicate
#   3. every directory in a numbered set carries a readme.md
#
# Summary line is assertable: files=N links=N broken=N prefix_defects=N missing_readme=N

set -u

ROOT="$(pwd)"
SCOPE=""
QUIET=0

while [ $# -gt 0 ]; do
  case "$1" in
    --root) ROOT="$2"; shift 2 ;;
    --scope) SCOPE="$2"; shift 2 ;;
    --quiet) QUIET=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

cd "$ROOT" || exit 2
SEARCH="${SCOPE:-.}"
[ -e "$SEARCH" ] || { echo "scope not found: $SEARCH" >&2; exit 2; }

files=0; links=0; broken=0

while IFS= read -r f; do
  files=$((files+1))
  dir="$(dirname "$f")"
  # ](target) with the target ending at the first ) or whitespace
  grep -n -o '](\([^)"[:space:]]*\)' "$f" 2>/dev/null | while IFS= read -r hit; do
    lineno="${hit%%:*}"
    target="${hit#*](}"
    case "$target" in
      http://*|https://*|mailto:*|'#'*|'') continue ;;
    esac
    target="${target%%#*}"; target="${target%%\?*}"
    [ -n "$target" ] || continue
    case "$target" in
      /*) resolved=".${target}" ;;
      *)  resolved="$dir/$target" ;;
    esac
    if [ ! -e "$resolved" ]; then
      echo "BROKEN|$f:$lineno|$target"
    else
      echo "OK|"
    fi
  done
done < <(find "$SEARCH" -name '*.md' -type f \
          -not -path '*/node_modules/*' -not -path '*/.git/*' \
          -not -path '*/bin/*' -not -path '*/obj/*' | sort) > /tmp/.linkcheck.$$

links="$(grep -c '^' /tmp/.linkcheck.$$ || true)"
broken="$(grep -c '^BROKEN' /tmp/.linkcheck.$$ || true)"
if [ "$QUIET" -eq 0 ] && [ "$broken" != "0" ]; then
  echo "--- broken links ---"
  grep '^BROKEN' /tmp/.linkcheck.$$ | while IFS='|' read -r _ where target; do
    echo "  $where -> $target"
  done
fi
rm -f /tmp/.linkcheck.$$

# --- numbered-sibling contiguity and readme presence ------------------------
prefix_defects=0
missing_readme=0
while IFS= read -r parent; do
  set -- $(find "$parent" -mindepth 1 -maxdepth 1 -type d -name '[0-9][0-9]-*' \
            -not -path '*/node_modules/*' | sort)
  [ $# -gt 0 ] || continue
  n=0
  for d in "$@"; do
    n=$((n+1))
    prefix="$(basename "$d" | cut -c1-2)"
    expected="$(printf '%02d' "$n")"
    if [ "$prefix" != "$expected" ]; then
      [ "$QUIET" -eq 0 ] && echo "PREFIX: $d has $prefix, expected $expected"
      prefix_defects=$((prefix_defects+1))
    fi
    if [ ! -f "$d/readme.md" ] && [ ! -f "$d/README.md" ]; then
      [ "$QUIET" -eq 0 ] && echo "NO README: $d"
      missing_readme=$((missing_readme+1))
    fi
  done
done < <(find "$SEARCH" -type d -not -path '*/node_modules/*' -not -path '*/.git/*' \
          -not -path '*/bin/*' -not -path '*/obj/*' | sort)

echo "files=$files links=$links broken=$broken prefix_defects=$prefix_defects missing_readme=$missing_readme"
[ "$broken" = "0" ] && [ "$prefix_defects" = "0" ] || exit 1
exit 0
