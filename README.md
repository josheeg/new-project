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

