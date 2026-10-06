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

# Core Dependencies for Spec-First API Routing & Runtime Validation
uv add connexion[flask] pydantic uvicorn fastapi

# Development Dependencies for Spec Linting, Code Generation, Mocking, and Contract Testing
uv add --dev openapi-spec-validator openapi-python-client schemathesis pytest pytest-cov ruff mypy

# Core Runtime Dependencies: Dependency Injection, Configuration, and Domain Modeling
uv add dependency-injector pydantic pydantic-settings

# Development Dependencies: Architectural Governance, Diagramming, Performance Benchmarking, and Quality Enforcement
uv add --dev import-linter diagrams pytest pytest-benchmark ruff mypy


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

