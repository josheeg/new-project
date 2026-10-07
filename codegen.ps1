# Regenerate API models from openapi/openapi.yaml. Fail fast on each step.
# Output (src/driven_dev/api_models.py) is GENERATED; never hand-edit it.
# Usage:  .\codegen.ps1          regenerate in place
#         .\codegen.ps1 -Check   verify committed file matches the spec (no writes)
param([switch]$Check)

$ErrorActionPreference = 'Stop'
$target = 'src/driven_dev/api_models.py'
$out = if ($Check) { Join-Path ([System.IO.Path]::GetTempPath()) 'driven-dev-api_models.gen.py' } else { $target }

$steps = @(
    @('validate spec', @('run', 'openapi-spec-validator', 'openapi/openapi.yaml')),
    @('generate models', @('run', 'datamodel-codegen',
        '--input', 'openapi/openapi.yaml',
        '--output', $out,
        '--output-model-type', 'pydantic_v2.BaseModel',
        '--target-python-version', '3.14',
        '--disable-timestamp')),
    @('ruff check --fix generated', @('run', 'ruff', 'check', '--fix', '--config', 'pyproject.toml', $out)),
    @('ruff format generated', @('run', 'ruff', 'format', '--config', 'pyproject.toml', $out))
)

foreach ($s in $steps) {
    Write-Host "==> $($s[0])" -ForegroundColor Cyan
    & uv @($s[1])
    if ($LASTEXITCODE -ne 0) {
        if ($Check) { Remove-Item $out -ErrorAction SilentlyContinue }
        Write-Host "FAILED: $($s[0]) (exit $LASTEXITCODE)" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

if ($Check) {
    git diff --no-index -- $target $out
    $diffCode = $LASTEXITCODE
    Remove-Item $out -ErrorAction SilentlyContinue
    if ($diffCode -ne 0) {
        Write-Host "FAILED: $target is stale - run .\codegen.ps1 and commit" -ForegroundColor Red
        exit 1
    }
    Write-Host "$target matches openapi/openapi.yaml" -ForegroundColor Green
} else {
    Write-Host "Generated $target" -ForegroundColor Green
}
