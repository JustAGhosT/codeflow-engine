<#
.SYNOPSIS
Analyzes bundle sizes for JavaScript/TypeScript projects.

.DESCRIPTION
Analyzes bundle sizes and provides optimization recommendations.

.PARAMETER ProjectPath
Path to the project directory.

.PARAMETER OutputFile
Output file for the analysis report.

.EXAMPLE
.\analyze-bundle-size.ps1 -ProjectPath "C:\repos\codeflow-desktop" -OutputFile "bundle-analysis.json"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath,
    
    [string]$OutputFile = "bundle-analysis.json"
)

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Bundle Size Analysis" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $ProjectPath)) {
    Write-Host "✗ Project path not found: $ProjectPath" -ForegroundColor Red
    exit 1
}

$packageJsonPath = Join-Path $ProjectPath "package.json"
if (-not (Test-Path $packageJsonPath)) {
    Write-Host "✗ package.json not found in project" -ForegroundColor Red
    exit 1
}

# ============================================================================
# Analyze Dependencies
# ============================================================================

Write-Host "Analyzing dependencies..." -ForegroundColor Yellow

$packageJson = Get-Content $packageJsonPath | ConvertFrom-Json
$dependencies = @{}

if ($packageJson.dependencies) {
    foreach ($dep in $packageJson.dependencies.PSObject.Properties) {
        $dependencies[$dep.Name] = @{
            Version = $dep.Value
            Type = "dependency"
        }
    }
}

if ($packageJson.devDependencies) {
    foreach ($dep in $packageJson.devDependencies.PSObject.Properties) {
        if (-not $dependencies.ContainsKey($dep.Name)) {
            $dependencies[$dep.Name] = @{
                Version = $dep.Value
                Type = "devDependency"
            }
        }
    }
}

Write-Host "  ✓ Found $($dependencies.Count) dependencies" -ForegroundColor Green
Write-Host ""

# ============================================================================
# Analyze Build Output
# ============================================================================

Write-Host "Analyzing build output..." -ForegroundColor Yellow

$buildDirs = @("dist", "build", "out", ".next")
$buildFiles = @()

foreach ($dir in $buildDirs) {
    $buildPath = Join-Path $ProjectPath $dir
    if (Test-Path $buildPath) {
        $files = Get-ChildItem -Path $buildPath -Recurse -File | Where-Object { 
            $_.Extension -in @(".js", ".css", ".html", ".json")
        }
        
        foreach ($file in $files) {
            $size = (Get-Item $file.FullName).Length
            $buildFiles += @{
                Path = $file.FullName.Replace($ProjectPath, ".")
                Size = $size
                SizeKB = [math]::Round($size / 1KB, 2)
                SizeMB = [math]::Round($size / 1MB, 2)
                Extension = $file.Extension
            }
        }
    }
}

$totalSize = ($buildFiles | Measure-Object -Property Size -Sum).Sum
$totalSizeKB = [math]::Round($totalSize / 1KB, 2)
$totalSizeMB = [math]::Round($totalSize / 1MB, 2)

Write-Host "  ✓ Found $($buildFiles.Count) build files" -ForegroundColor Green
Write-Host "  Total size: $totalSizeMB MB ($totalSizeKB KB)" -ForegroundColor White
Write-Host ""

# ============================================================================
# Generate Recommendations
# ============================================================================

Write-Host "Generating recommendations..." -ForegroundColor Yellow

$recommendations = @()

# Check for large dependencies
$largeDeps = @("react", "react-dom", "@mui/material", "lodash", "moment")
foreach ($dep in $largeDeps) {
    if ($dependencies.ContainsKey($dep)) {
        $recommendations += "Consider using lighter alternatives for $dep"
    }
}

# Check for duplicate dependencies
$duplicatePatterns = @{
    "lodash" = "lodash-es"
    "moment" = "date-fns"
}

foreach ($pattern in $duplicatePatterns.Keys) {
    if ($dependencies.ContainsKey($pattern) -and $dependencies.ContainsKey($duplicatePatterns[$pattern])) {
        $recommendations += "Both $pattern and $($duplicatePatterns[$pattern]) are installed - consider using only one"
    }
}

# Check for large build files
$largeFiles = $buildFiles | Where-Object { $_.SizeMB -gt 1 } | Sort-Object -Property Size -Descending | Select-Object -First 5
if ($largeFiles) {
    $recommendations += "Large build files detected - consider code splitting"
    foreach ($file in $largeFiles) {
        $recommendations += "  - $($file.Path): $($file.SizeMB) MB"
    }
}

# Check total bundle size
if ($totalSizeMB -gt 5) {
    $recommendations += "Total bundle size is large ($totalSizeMB MB) - consider optimization"
}

Write-Host "  ✓ Generated $($recommendations.Count) recommendations" -ForegroundColor Green
Write-Host ""

# ============================================================================
# Generate Report
# ============================================================================

$report = @{
    ProjectPath = $ProjectPath
    AnalyzedAt = (Get-Date -Format "o")
    Dependencies = @{
        Total = $dependencies.Count
        List = $dependencies
    }
    BuildOutput = @{
        TotalFiles = $buildFiles.Count
        TotalSize = $totalSize
        TotalSizeKB = $totalSizeKB
        TotalSizeMB = $totalSizeMB
        Files = $buildFiles | Sort-Object -Property Size -Descending
    }
    Recommendations = $recommendations
}

$reportJson = $report | ConvertTo-Json -Depth 10
$reportJson | Out-File -FilePath $OutputFile -Encoding utf8

Write-Host "========================================" -ForegroundColor Green
Write-Host "Analysis Complete" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Report saved to: $OutputFile" -ForegroundColor White
Write-Host ""
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  Dependencies: $($dependencies.Count)" -ForegroundColor White
Write-Host "  Build Files: $($buildFiles.Count)" -ForegroundColor White
Write-Host "  Total Size: $totalSizeMB MB" -ForegroundColor White
Write-Host "  Recommendations: $($recommendations.Count)" -ForegroundColor White
Write-Host ""

if ($recommendations.Count -gt 0) {
    Write-Host "Top Recommendations:" -ForegroundColor Yellow
    foreach ($rec in $recommendations[0..4]) {
        Write-Host "  • $rec" -ForegroundColor Gray
    }
    Write-Host ""
}

