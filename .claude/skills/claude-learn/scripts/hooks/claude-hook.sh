#!/bin/bash
set -euo pipefail

HOOK_NAME="${1:-}"
REPO_ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || echo ".")}"
[ -f "$REPO_ROOT/.conversations-claude/hooks/node-path.sh" ] || exit 0
. "$REPO_ROOT/.conversations-claude/hooks/node-path.sh"

if ! NODE_BIN="$(resolve_node)"; then exit 0; fi

SCRIPT_PATH="$(resolve_node_script_path "$NODE_BIN" "$REPO_ROOT/.conversations-claude/hooks/claude-hook.js")"
exec "$NODE_BIN" "$SCRIPT_PATH" "$HOOK_NAME"
