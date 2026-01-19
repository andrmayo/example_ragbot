#!/usr/bin/env bash

# Ensure we're in project root
if [[ ! -d "backend" ]]; then
  echo "Run this script from the project root"
  exit 1
fi

# server has to already be running for this to work
curl -w '\n' http://localhost:8000/upload \
  -F "file=@${1:-backend/tests/fixtures/engineering_resume25.docx}"
