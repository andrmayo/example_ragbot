#!/usr/bin/env bash

# server has to already be running for this to work
curl -w '\n' -X DELETE http://localhost:8000/clear_all
