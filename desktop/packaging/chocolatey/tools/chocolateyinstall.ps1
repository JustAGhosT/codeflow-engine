# Chocolatey install script for CodeFlow Engine

$ErrorActionPreference = 'Stop'

$packageName = 'codeflow-engine'
$toolsDir = "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"

# Check Python installation
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "Python not found. Installing Python 3.12..."
    choco install python3 --version=3.12 -y
    refreshenv
}

# Verify Python version
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python (\d+)\.(\d+)") {
    $major = [int]$Matches[1]
    $minor = [int]$Matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 12)) {
        throw "Python 3.12+ required. Found: $pythonVersion"
    }
}

Write-Host "Installing CodeFlow Engine via pip..."
pip install codeflow-engine

if ($LASTEXITCODE -ne 0) {
    throw "Failed to install CodeFlow Engine"
}

Write-Host ""
Write-Host "CodeFlow Engine installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Set up your API keys:"
Write-Host '     $env:GITHUB_TOKEN = "ghp_your_token"'
Write-Host '     $env:OPENAI_API_KEY = "sk-your_key"'
Write-Host ""
Write-Host "  2. Run CodeFlow:"
Write-Host "     CodeFlow --help"
Write-Host ""
