#!/usr/bin/env bash

# Ensure we're in project root
if [[ ! -d "backend" ]]; then
  echo "Run this script from the project root"
  exit 1
fi

# Build -F arguments for each PDF
args=()
for f in backend/tests/fixtures/*.pdf; do
  args+=(-F "files=@$f")
done

# server has to already be running for this to work
curl -w '\n' "http://localhost:8000/upload_batch?collection=architecture" \
  "${args[@]}"

curl -w '\n' "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Which resume is most qualified for a architecture job?", "collection": "architecture"}' | jq
