# Generate a typed Python client from openapi/openapi.yaml.
# Output lands in clients/ (gitignored - it is a build artifact).
$ErrorActionPreference = 'Stop'

uv run openapi-python-client generate `
    --path openapi/openapi.yaml `
    --output-path clients/driven-dev-client `
    --meta none `
    --overwrite
if ($LASTEXITCODE -ne 0) {
    Write-Host "FAILED: client generation (exit $LASTEXITCODE)" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "Generated clients/driven-dev-client" -ForegroundColor Green
