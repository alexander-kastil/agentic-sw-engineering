#!/usr/bin/env bash

set -uo pipefail

URL=""; KEY=""; EXPECT=""; CALLS=(); HEALTH=0; UNAUTH=0; CONTAINER=0
while [ $# -gt 0 ]; do
  case "$1" in
    --url) URL="$2"; shift 2 ;;
    --key) KEY="$2"; shift 2 ;;
    --expect) EXPECT="$2"; shift 2 ;;
    --call) CALLS+=("$2"); shift 2 ;;
    --health) HEALTH=1; shift ;;
    --unauth-401) UNAUTH=1; shift ;;
    --container) CONTAINER=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
[ -n "$URL" ] || { echo "usage: verify-mcp-server.sh --url <mcp-url> [--key K] [--expect a,b] [--call name]... [--health] [--unauth-401] [--container]" >&2; exit 2; }
ORIGIN="${URL%/mcp}"
PRE=0

if [ "$CONTAINER" = "1" ]; then
  PORT="${ORIGIN##*:}"
  NAME="$(docker ps --filter "publish=$PORT" --format '{{.Names}}' 2>/dev/null | head -1)"
  if [ -z "$NAME" ]; then
    echo "container: NONE published on $PORT"; PRE=1
  else
    ST="$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}no healthcheck{{end}}' "$NAME" 2>/dev/null)"
    echo "container: $NAME ($ST)"
    case "$ST" in healthy|"no healthcheck") ;; *) PRE=1 ;; esac
  fi
fi

if [ "$HEALTH" = "1" ]; then
  H=$(curl -sk -m 10 -o /dev/null -w '%{http_code}' "$ORIGIN/health")
  echo "GET /health (no credentials) HTTP $H"
  [ "$H" = "200" ] || { echo "  want 200: an orchestrator probes this without a token"; PRE=1; }
fi

if [ "$UNAUTH" = "1" ]; then
  U=$(curl -sk -m 10 -o /dev/null -w '%{http_code}' -X POST "$URL"       -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream"       -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')
  echo "POST /mcp (no credentials) HTTP $U"
  [ "$U" = "401" ] || { echo "  want 401: the endpoint is not protected"; PRE=1; }
fi

[ "$PRE" = "0" ] || { echo "RESULT fail: pre-checks"; exit 1; }

HDR=(-H "Content-Type: application/json" -H "Accept: application/json, text/event-stream")
[ -n "$KEY" ] && HDR+=(-H "X-API-Key: $KEY")

rpc() { curl -sk -m 20 -X POST "$URL" "${HDR[@]}" -d "$1" | sed -n 's/^data: //p;/^{/p' | tail -1; }

STATUS=$(curl -sk -m 20 -o /dev/null -w '%{http_code}' -X POST "$URL" "${HDR[@]}" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')
echo "tools/list HTTP $STATUS"
[ "$STATUS" = "200" ] || { echo "RESULT fail: expected 200"; exit 1; }

LIST=$(rpc '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')
NAMES=$(printf '%s' "$LIST" | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const t=JSON.parse(s).result.tools;console.log(t.map(x=>x.name).sort().join(","))})') || {
  echo "RESULT fail: tools/list did not parse"; exit 1; }
COUNT=$(printf '%s' "$NAMES" | tr ',' '\n' | grep -c .)
echo "tools ($COUNT): $NAMES"

FAIL=0
if [ -n "$EXPECT" ]; then
  WANT=$(printf '%s' "$EXPECT" | tr ',' '\n' | sort | paste -sd, -)
  if [ "$NAMES" = "$WANT" ]; then echo "expect: match"; else echo "expect: MISMATCH want=$WANT"; FAIL=1; fi
fi

for t in ${CALLS+"${CALLS[@]}"}; do
  R=$(rpc "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/call\",\"params\":{\"name\":\"$t\",\"arguments\":{}}}")
  N=$(printf '%s' "$R" | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{try{const r=JSON.parse(s).result;const c=r.structuredContent||JSON.parse(r.content[0].text);const a=Array.isArray(c)?c:(Object.values(c).find(Array.isArray)||[]);console.log(a.length)}catch(e){console.log("ERR")}})')
  echo "call $t -> $N item(s)"
  { [ "$N" = "ERR" ] || [ "$N" = "0" ]; } && FAIL=1
done

[ "$FAIL" = "0" ] && echo "RESULT pass: $COUNT tools" || echo "RESULT fail"
exit "$FAIL"
