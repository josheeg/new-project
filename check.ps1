# Full verification chain: ruff -> mypy -> spec contract -> pytest.
# Fails fast on first error. Mirrors what a hosted CI would run; use this
# before considering work done.
$ErrorActionPreference = 'Stop'

$steps = @(
    @('ruff check', { uv run ruff check . }),
    @('ruff format --check', { uv run ruff format --check . }),
    @('mypy', { uv run mypy }),
    @('architecture (import-linter)', { uv run lint-imports }),
    @('spec contract (validate + drift)', { & (Join-Path $PSScriptRoot 'codegen.ps1') -Check }),
    @('docstring coverage (interrogate)', { uv run interrogate src }),
    @('docs build (strict)', { uv run mkdocs build }),
    @('pytest (cov gate 90)', { uv run pytest --cov-fail-under=90 })
)

foreach ($s in $steps) {
    Write-Host "==> $($s[0])" -ForegroundColor Cyan
    & $s[1]
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $($s[0]) (exit $LASTEXITCODE)" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

Write-Host "All checks passed." -ForegroundColor Green
