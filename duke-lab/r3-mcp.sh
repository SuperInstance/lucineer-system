#!/bin/bash
# usage: mcp.sh TOOL JSON_ARGS [id]
ID=${3:-$RANDOM}
curl -s --max-time 120 http://127.0.0.1:8765/ -X POST -H 'Content-Type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"id\":$ID,\"method\":\"tools/call\",\"params\":{\"name\":\"$1\",\"arguments\":$2}}"
