#!/bin/bash

resolve_node() {
  if command -v node >/dev/null 2>&1; then command -v node; return 0; fi
  if command -v node.exe >/dev/null 2>&1; then command -v node.exe; return 0; fi
  if command -v where.exe >/dev/null 2>&1; then
    local win_path
    win_path=$(where.exe node 2>/dev/null | head -n 1 | tr -d '\r')
    if [ -n "$win_path" ]; then
      command -v cygpath >/dev/null 2>&1 && cygpath -u "$win_path" || printf '%s\n' "$win_path"
      return 0
    fi
  fi
  return 1
}

resolve_node_script_path() {
  local node_bin="$1" script_path="$2"
  if [[ "$script_path" == /* ]] && command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$script_path"; return 0
  fi
  if [[ "$script_path" =~ ^/mnt/([a-zA-Z])/(.*)$ ]]; then
    local d="${BASH_REMATCH[1]}" r="${BASH_REMATCH[2]}"
    r="${r//\//\\}"; printf '%s:\\%s\n' "$(printf '%s' "$d" | tr '[:lower:]' '[:upper:]')" "$r"; return 0
  fi
  printf '%s\n' "$script_path"
}
