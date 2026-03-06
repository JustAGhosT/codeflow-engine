<#
.SYNOPSIS
Automates security scanning across CodeFlow repositories.

.DESCRIPTION
Runs security scans for vulnerabilities in dependencies and code.

.PARAMETER Repository
Repository path to scan.

.PARAMETER ScanType
Type of scan to run (dependencies, code, all). Default: all

.PARAMETER OutputFile
Output file for scan results.

.EXAMPLE
.\security-scan.ps1 -Repository "C:\repos\codeflow-engine" -ScanType "dependencies"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Repository,
    
    [ValidateSet("dependencies", "code", "all")]
    [string]$ScanType = "all",
    
    [string]$OutputFile = "security-scan-results.json"
)

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Security Scan" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $Repository)) {
    Write-Host "✗ Repository not found: $Repository" -ForegroundColor Red
    exit 1
}

Push-Location $Repository

$scanResults = @{
    Repository = $Repository
    ScannedAt = (Get-Date -Format "o")
    ScanType = $ScanType
    Vulnerabilities = @()
    Warnings = @()
    Info = @()
}

# ============================================================================
# Dependency Scanning
# ============================================================================

if ($ScanType -in @("dependencies", "all")) {
    Write-Host "Scanning dependencies..." -ForegroundColor Yellow
    
    # Check for package.json (npm)
    if (Test-Path "package.json") {
        Write-Host "  Scanning npm dependencies..." -ForegroundColor Gray
        
        # Check if npm audit is available
        if (Get-Command npm -ErrorAction SilentlyContinue) {
            try {
                $auditResult = npm audit --json 2>&1 | ConvertFrom-Json
                
                if ($auditResult.vulnerabilities) {
                    foreach ($vuln in $auditResult.vulnerabilities.PSObject.Properties) {
                        $scanResults.Vulnerabilities += @{
                            Type = "npm"
                            Package = $vuln.Name
                            Severity = $vuln.Value.severity
                            Title = $vuln.Value.title
                            Recommendation = "Run: npm audit fix"
                        }
                    }
                }
                
                Write-Host "    ✓ npm audit complete" -ForegroundColor Green
            } catch {
                Write-Host "    ⚠ npm audit failed: $_" -ForegroundColor Yellow
                $scanResults.Warnings += "npm audit failed: $_"
            }
        }
    }
    
    # Check for pyproject.toml (Poetry)
    if (Test-Path "pyproject.toml") {
        Write-Host "  Scanning Poetry dependencies..." -ForegroundColor Gray
        
        if (Get-Command poetry -ErrorAction SilentlyContinue) {
            try {
                # Poetry doesn't have built-in security scanning
                # Would need to use safety or pip-audit
                Write-Host "    ⚠ Poetry security scanning requires safety or pip-audit" -ForegroundColor Yellow
                $scanResults.Info += "Poetry dependencies detected - install safety or pip-audit for scanning"
            } catch {
                Write-Host "    ⚠ Poetry scan failed: $_" -ForegroundColor Yellow
            }
        }
    }
    
    # Check for requirements.txt (pip)
    if (Test-Path "requirements.txt") {
        Write-Host "  Scanning pip dependencies..." -ForegroundColor Gray
        
        if (Get-Command pip -ErrorAction SilentlyContinue) {
            try {
                # Use pip-audit if available
                $pipAudit = Get-Command pip-audit -ErrorAction SilentlyContinue
                if ($pipAudit) {
                    $auditOutput = pip-audit --format json 2>&1
                    # Parse results
                    Write-Host "    ✓ pip-audit complete" -ForegroundColor Green
                } else {
                    Write-Host "    ⚠ pip-audit not installed. Install with: pip install pip-audit" -ForegroundColor Yellow
                    $scanResults.Info += "pip-audit not installed for dependency scanning"
                }
            } catch {
                Write-Host "    ⚠ pip scan failed: $_" -ForegroundColor Yellow
            }
        }
    }
}

# ============================================================================
# Code Scanning
# ============================================================================

if ($ScanType -in @("code", "all")) {
    Write-Host "Scanning code..." -ForegroundColor Yellow
    
    # Check for secrets
    Write-Host "  Checking for secrets..." -ForegroundColor Gray
    
    $secretPatterns = @(
        "password\s*=\s*['`"]([^'`"]+)['`"]",
        "api[_-]?key\s*=\s*['`"]([^'`"]+)['`"]",
        "secret\s*=\s*['`"]([^'`"]+)['`"]",
        "token\s*=\s*['`"]([^'`"]+)['`"]",
        "BEGIN\s+(RSA\s+)?PRIVATE\s+KEY"
    )
    
    $codeFiles = Get-ChildItem -Path . -Recurse -Include *.py,*.js,*.ts,*.json,*.yml,*.yaml -File | 
        Where-Object { $_.FullName -notmatch "node_modules|\.git|__pycache__|\.venv|dist|build" }
    
    foreach ($file in $codeFiles) {
        $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
        if ($content) {
            foreach ($pattern in $secretPatterns) {
                if ($content -match $pattern) {
                    $scanResults.Warnings += @{
                        Type = "Potential Secret"
                        File = $file.FullName.Replace($Repository, ".")
                        Pattern = $pattern
                        Recommendation = "Review and remove hardcoded secrets"
                    }
                }
            }
        }
    }
    
    Write-Host "    ✓ Code scan complete" -ForegroundColor Green
}

Pop-Location

# ============================================================================
# Generate Report
# ============================================================================

$scanResults.VulnerabilityCount = $scanResults.Vulnerabilities.Count
$scanResults.WarningCount = $scanResults.Warnings.Count

$reportJson = $scanResults | ConvertTo-Json -Depth 10
$reportJson | Out-File -FilePath $OutputFile -Encoding utf8

# ============================================================================
# Display Summary
# ============================================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor $(if ($scanResults.VulnerabilityCount -eq 0) { "Green" } else { "Red" })
Write-Host "Security Scan Summary" -ForegroundColor $(if ($scanResults.VulnerabilityCount -eq 0) { "Green" } else { "Red" })
Write-Host "========================================" -ForegroundColor $(if ($scanResults.VulnerabilityCount -eq 0) { "Green" } else { "Red" })
Write-Host ""

Write-Host "Vulnerabilities: $($scanResults.VulnerabilityCount)" -ForegroundColor $(if ($scanResults.VulnerabilityCount -eq 0) { "Green" } else { "Red" })
Write-Host "Warnings: $($scanResults.WarningCount)" -ForegroundColor $(if ($scanResults.WarningCount -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

if ($scanResults.VulnerabilityCount -gt 0) {
    Write-Host "Top Vulnerabilities:" -ForegroundColor Red
    foreach ($vuln in $scanResults.Vulnerabilities[0..4]) {
        Write-Host "  • $($vuln.Package): $($vuln.Severity) - $($vuln.Title)" -ForegroundColor Yellow
    }
    Write-Host ""
}

Write-Host "Report saved to: $OutputFile" -ForegroundColor White
Write-Host ""

if ($scanResults.VulnerabilityCount -gt 0) {
    exit 1
} else {
    exit 0
}

