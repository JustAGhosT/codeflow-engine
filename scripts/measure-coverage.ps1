# Measure current test coverage and generate detailed report

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CodeFlow Engine - Coverage Measurement" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Run tests with coverage
Write-Host "Running tests with coverage..." -ForegroundColor Yellow
poetry run pytest --cov=codeflow_engine --cov-report=html --cov-report=term --cov-report=xml

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Coverage Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get overall coverage
$CoverageOutput = poetry run coverage report | Select-String "TOTAL"
$Coverage = [regex]::Match($CoverageOutput, '(\d+(?:\.\d+)?)%').Groups[1].Value
Write-Host "Overall Coverage: ${Coverage}%"
Write-Host ""

# Show coverage by module
Write-Host "Coverage by Module:" -ForegroundColor Yellow
Write-Host "----------------------------------------"
poetry run coverage report --show-missing | Select-String "codeflow_engine"
Write-Host ""

# Show files with low coverage
Write-Host "Files with Coverage < 50%:" -ForegroundColor Yellow
Write-Host "----------------------------------------"
$LowCoverage = poetry run coverage report | Select-String "codeflow_engine" | Where-Object {
    if ($_ -match '(\d+(?:\.\d+)?)%') {
        [double]$matches[1] -lt 50
    }
}
if ($LowCoverage) {
    $LowCoverage | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "None"
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Detailed Report" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "HTML report generated: htmlcov/index.html"
Write-Host "XML report generated: coverage.xml"
Write-Host ""
Write-Host "Open HTML report: Start-Process htmlcov/index.html"
Write-Host ""

