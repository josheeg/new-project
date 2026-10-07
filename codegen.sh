#!/usr/bin/env bash
# Regenerate API models from openapi/openapi.yaml. Fail fast on each step.
# Output (src/driven_dev/api_models.py) is GENERATED — never hand-edit it.
# Usage:  ./codegen.sh          regenerate in place
#         ./codegen.sh --check  verify committed file matches the spec (no writes)
set -euo pipefail

target=src/driven_dev/api_models.py
out=$target
if [ "${1:-}" = "--check" ]; then
  out=$(mktemp)
  trap 'rm -f "$out"' EXIT
fi

echo "==> validate spec"
uv run openapi-spec-validator openapi/openapi.yaml
echo "==> generate models"
uv run datamodel-codegen \
  --input openapi/openapi.yaml \
  --output "$out" \
  --output-model-type pydantic_v2.BaseModel \
  --target-python-version 3.14 \
  --disable-timestamp
echo "==> ruff check --fix generated"
uv run ruff check --fix --config pyproject.toml "$out"
echo "==> ruff format generated"
uv run ruff format --config pyproject.toml "$out"

if [ "$out" != "$target" ]; then
  if ! git diff --no-index -- "$target" "$out"; then
    echo "FAILED: $target is stale — run ./codegen.sh and commit" >&2
    exit 1
  fi
  echo "$target matches openapi/openapi.yaml"
else
  echo "Generated $target"
fi
