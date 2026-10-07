#!/usr/bin/env bash
# Generate a typed Python client from openapi/openapi.yaml.
# Output lands in clients/ (gitignored - it is a build artifact).
set -euo pipefail

uv run openapi-python-client generate \
  --path openapi/openapi.yaml \
  --output-path clients/driven-dev-client \
  --meta none \
  --overwrite
echo "Generated clients/driven-dev-client"
