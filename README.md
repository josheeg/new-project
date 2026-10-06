# new-project-ai
# 1. Initialize Repository & Environment
git init
uv init --no-workspace
uv venv

# 2. Development, Quality & Testing
uv add --dev `
  ruff `
  mypy `
  pytest `
  pytest-cov `
  pytest-asyncio `
  pytest-mock `
  pytest-xdist `
  coverage `
  pyinstaller `
  pre-commit `
  towncrier `
  mkdocs `
  mkdocs-material

# 6. LLMs, RAG & LLM Tooling
uv add `
  anthropic `
  guidance

# 1. Add Spec Validation, Structuring & Schema Engines
uv add `
  pydantic `
  pydantic-settings `
  jinja2 `
  yaml

# 2. Add ADR / Spec Tooling (CLI, Diagramming & Docs)
uv add --dev `
  mkdocs-kroki-plugin `
  mkdocs-gen-files `
  mkdocstrings[python] `
  adr-tools-python

