#!/usr/bin/env bash

if [[ -z "$1" ]]; then
  echo "Usage: ./test_ask.sh <question>"
  exit 1
fi

curl -w '\n' -s http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"$1\"}" | jq
