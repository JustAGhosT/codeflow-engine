# Check test coverage and enforce quality gates

param(
    [int]$CoverageThreshold = 70
)

$ErrorActionPreference = 'Stop'

$CoverageFile = "coverage.xml"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CodeFlow Engine - Coverage Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if coverage file exists
if (-not (Test-Path $CoverageFile)) {
    Write-Host "⚠️  Coverage file not found. Running tests with coverage..." -ForegroundColor Yellow
    poetry run pytest --cov=codeflow_engine --cov-report=xml --cov-report=term
}

# Get current coverage percentage
$CoverageOutput = poetry run coverage report | Select-String "TOTAL"
$Coverage = [regex]::Match($CoverageOutput, '(\d+(?:\.\d+)?)%').Groups[1].Value
$CoverageValue = [double]$Coverage

Write-Host "Current coverage: ${Coverage}%"
Write-Host "Target coverage: ${CoverageThreshold}%"
Write-Host ""

# Check if coverage meets threshold
if ($CoverageValue -lt $CoverageThreshold) {
    Write-Host "❌ Coverage ${Coverage}% is below threshold of ${CoverageThreshold}%" -ForegroundColor Red
    Write-Host ""
    Write-Host "Coverage by module:" -ForegroundColor Yellow
    poetry run coverage report --show-missing | Select-String "codeflow_engine" | Select-Object -First 20
    exit 1
}
else {
    Write-Host "✅ Coverage ${Coverage}% meets threshold of ${CoverageThreshold}%" -ForegroundColor Green
    exit 0
}

