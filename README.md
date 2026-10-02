# new-project-ml-ai
# 1. Initialize Repository & Environment
git init
uv init --app
uv venv

# Add PyTorch CPU index to pyproject.toml
@"

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cpu" }
torchvision = { index = "pytorch-cpu" }
torchaudio = { index = "pytorch-cpu" }
"@ | Out-File -FilePath pyproject.toml -Append -Encoding utf8

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

# 3. Core Data Science, Storage & Utilities
uv add `
  pandas `
  polars `
  scipy `
  matplotlib `
  httpx `
  python-dotenv `
  papermill `
  pydantic

# 4. Classical ML & Time Series
uv add `
  scikit-learn `
  xgboost `
  catboost `
  statsmodels `
  sktime `
  pmdarima `
  prophet

# 5. Deep Learning Frameworks (CPU-Optimized)
uv add torch torchvision torchaudio
uv add tensorflow jax jaxlib

# 6. LLMs, RAG & LLM Tooling
uv add `
  anthropic `
  guidance

# 7. Gitignore & BMAD Method Setup
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore" -OutFile ".gitignore"

Write-Host "Setup complete. Run 'npx bmad-method init' interactively to finish setting up BMAD Method."

npx skills add bmad-code-org/BMAD-METHOD
