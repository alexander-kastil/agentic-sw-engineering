#!/usr/bin/env bash
# Execute a folder-renumbering plan with history-preserving git mv.
# Cycle-safe (A->B while B->C), Windows build-lock tolerant, and it proves
# afterwards that no file content was lost.
#
# usage: renumber-tree.sh --plan <file> [--root <dir>] [--dry-run] [--retries N]
#
# plan file: one move per line, "<old path><TAB or spaces><new path>", both
# relative to --root. Blank lines and lines starting with # are ignored.

set -u

ROOT="$(pwd)"
PLAN=""
DRY=0
RETRIES=5

while [ $# -gt 0 ]; do
  case "$1" in
    --plan) PLAN="$2"; shift 2 ;;
    --root) ROOT="$2"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --retries) RETRIES="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

[ -n "$PLAN" ] || { echo "--plan is required" >&2; exit 2; }
[ -f "$PLAN" ] || { echo "plan not found: $PLAN" >&2; exit 2; }
cd "$ROOT" || exit 2
git rev-parse --git-dir >/dev/null 2>&1 || { echo "not a git repo: $ROOT" >&2; exit 2; }

OLDS=(); NEWS=()
while IFS= read -r line || [ -n "$line" ]; do
  case "$line" in ''|\#*) continue ;; esac
  old="$(printf '%s' "$line" | awk '{print $1}')"
  new="$(printf '%s' "$line" | awk '{print $2}')"
  [ -n "$old" ] && [ -n "$new" ] || { echo "malformed plan line: $line" >&2; exit 2; }
  OLDS+=("${old%/}"); NEWS+=("${new%/}")
done < "$PLAN"

N=${#OLDS[@]}
[ "$N" -gt 0 ] || { echo "plan is empty" >&2; exit 2; }

# --- validate before touching anything -------------------------------------
fail=0
for i in $(seq 0 $((N-1))); do
  [ -e "${OLDS[$i]}" ] || { echo "MISSING source: ${OLDS[$i]}" >&2; fail=1; }
done
dupes="$(printf '%s\n' "${NEWS[@]}" | sort | uniq -d)"
[ -z "$dupes" ] || { echo "duplicate destinations:" >&2; echo "$dupes" >&2; fail=1; }
for i in $(seq 0 $((N-1))); do
  dest="${NEWS[$i]}"
  if [ -e "$dest" ]; then
    is_source=0
    for j in $(seq 0 $((N-1))); do [ "${OLDS[$j]}" = "$dest" ] && is_source=1; done
    [ "$is_source" -eq 1 ] || { echo "destination already exists and is not itself moving: $dest" >&2; fail=1; }
  fi
done
[ "$fail" -eq 0 ] || { echo "PLAN INVALID, nothing moved" >&2; exit 1; }

before_count="$(git ls-files | wc -l | tr -d ' ')"
before_blobs="$(git ls-files -s | awk '{print $2}' | sort | git hash-object --stdin)"

if [ "$DRY" -eq 1 ]; then
  for i in $(seq 0 $((N-1))); do echo "would move: ${OLDS[$i]} -> ${NEWS[$i]}"; done
  echo "planned=$N tracked_before=$before_count (dry run, nothing moved)"
  exit 0
fi

# --- the move, with Windows build-lock recovery -----------------------------
shutdown_done=0
retries_used=0

unlock() {
  # A gitignored bin/obj under the source is the usual holder of the handle on
  # Windows. Clearing it is safe: nothing there is tracked, and a build rebuilds it.
  local src="$1" d
  while IFS= read -r d; do
    [ -n "$d" ] || continue
    [ "$(git ls-files "$d" | wc -l | tr -d ' ')" = "0" ] && rm -rf "$d" 2>/dev/null
  done < <(find "$src" -type d \( -name bin -o -name obj \) 2>/dev/null)
  if [ "$shutdown_done" -eq 0 ] && command -v dotnet >/dev/null 2>&1; then
    dotnet build-server shutdown >/dev/null 2>&1
    shutdown_done=1
  fi
}

move() {
  local src="$1" dst="$2" i
  mkdir -p "$(dirname "$dst")"
  for i in $(seq 1 "$RETRIES"); do
    if git mv "$src" "$dst" 2>/dev/null; then return 0; fi
    retries_used=$((retries_used+1))
    unlock "$src"
    sleep 1
  done
  echo "FAILED: $src -> $dst" >&2
  return 1
}

# Pass 1: everything to a unique temp name, so a cycle cannot collide.
TMPS=()
for i in $(seq 0 $((N-1))); do
  tmp="$(dirname "${NEWS[$i]}")/.__renumber_$i"
  TMPS+=("$tmp")
  move "${OLDS[$i]}" "$tmp" || exit 1
done

# Pass 2: temp to final.
moved=0
for i in $(seq 0 $((N-1))); do
  move "${TMPS[$i]}" "${NEWS[$i]}" || exit 1
  moved=$((moved+1))
done

# Prune directories the plan emptied out. Never touches a directory with content.
for i in $(seq 0 $((N-1))); do
  d="$(dirname "${OLDS[$i]}")"
  while [ "$d" != "." ] && [ "$d" != "/" ] && [ -d "$d" ]; do
    rmdir "$d" 2>/dev/null || break
    d="$(dirname "$d")"
  done
done

# --- the receipt: same files, same content, only different paths ------------
after_count="$(git ls-files | wc -l | tr -d ' ')"
after_blobs="$(git ls-files -s | awk '{print $2}' | sort | git hash-object --stdin)"
deleted="$(git status --porcelain | grep -c '^ D\|^D ' || true)"

verdict=PASS
[ "$before_count" = "$after_count" ] || verdict=FAIL
[ "$before_blobs" = "$after_blobs" ] || verdict=FAIL
[ "$deleted" = "0" ] || verdict=FAIL

echo "moved=$moved retries=$retries_used tracked_before=$before_count tracked_after=$after_count deletions=$deleted content=$verdict"
[ "$verdict" = "PASS" ] || exit 1
