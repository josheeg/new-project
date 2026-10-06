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
  mkdocs-material`
  pytest-watch

# Core Runtime Dependencies: Data validation & API framework
uv add pydantic pydantic-settings fastapi uvicorn

# Development Dependencies: Schema generators, contract testing, and quality tools
uv add --dev datamodel-code-generator schemathesis hypothesis pytest pytest-cov ruff mypy

# Core Dependencies for API & Interactive Docs (if building APIs)
uv add fastapi pydantic uvicorn

# Development Dependencies for Documentation Generation, Testing, and Linting
uv add --dev mkdocs mkdocs-material "mkdocstrings[python]" interrogate pytest ruff mypy


# 6. LLMs, RAG & LLM Tooling
uv add `
  anthropic `
  guidance

# 1. Add Spec Validation, Structuring & Schema Engines
uv add `
  pydantic `
  pydantic-settings `
  jinja2 `
  pyyaml

# 2. Add ADR / Spec Tooling (CLI, Diagramming & Docs)
uv add --dev `
  mkdocs-kroki-plugin `
  mkdocs-gen-files `
  mkdocstrings[python] `
  adr-tools-python

