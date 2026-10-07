#!/usr/bin/env bash
# Full verification chain: ruff -> mypy -> spec contract -> pytest.
# Fails fast on first error. Mirrors what a hosted CI would run; use this
# before considering work done.
set -euo pipefail

echo "==> ruff check"
uv run ruff check .
echo "==> ruff format --check"
uv run ruff format --check .
echo "==> mypy"
uv run mypy
echo "==> architecture (import-linter)"
uv run lint-imports
echo "==> spec contract (validate + drift)"
bash ./codegen.sh --check
echo "==> docstring coverage (interrogate)"
uv run interrogate src
echo "==> docs build (strict)"
uv run mkdocs build
echo "==> pytest (cov gate 90)"
uv run pytest --cov-fail-under=90
echo "All checks passed."
