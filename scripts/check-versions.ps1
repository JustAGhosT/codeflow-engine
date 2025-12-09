#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Check versions across all CodeFlow repositories.

.DESCRIPTION
    This script checks the current version in all CodeFlow repositories and
    displays a summary of version consistency.

.PARAMETER RepoPath
    Base path to CodeFlow repositories. Defaults to parent directory.

.EXAMPLE
    .\check-versions.ps1

.EXAMPLE
    .\check-versions.ps1 -RepoPath "C:\repos"
#>

param(
    [string]$RepoPath = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
)

$ErrorActionPreference = "Stop"

Write-Host "CodeFlow Version Check" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

$repos = @(
    @{ Name = "codeflow-engine"; File = "pyproject.toml"; Pattern = 'version\s*=\s*"([^"]+)"' },
    @{ Name = "codeflow-desktop"; File = "package.json"; Pattern = '"version"\s*:\s*"([^"]+)"' },
    @{ Name = "codeflow-vscode-extension"; File = "package.json"; Pattern = '"version"\s*:\s*"([^"]+)"' },
    @{ Name = "codeflow-website"; File = "package.json"; Pattern = '"version"\s*:\s*"([^"]+)"' }
)

$versions = @{}

foreach ($repo in $repos) {
    $repoPath = Join-Path $RepoPath $repo.Name
    $filePath = Join-Path $repoPath $repo.File

    if (-not (Test-Path $filePath)) {
        Write-Host "⚠️  $($repo.Name): File not found ($($repo.File))" -ForegroundColor Yellow
        continue
    }

    $content = Get-Content $filePath -Raw
    if ($content -match $repo.Pattern) {
        $version = $matches[1]
        $versions[$repo.Name] = $version
        Write-Host "✅ $($repo.Name): $version" -ForegroundColor Green
    } else {
        Write-Host "⚠️  $($repo.Name): Version not found" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Version Summary" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan

if ($versions.Count -eq 0) {
    Write-Host "No versions found." -ForegroundColor Red
    exit 1
}

# Group by version
$versionGroups = $versions.GetEnumerator() | Group-Object Value

foreach ($group in $versionGroups) {
    Write-Host ""
    Write-Host "Version: $($group.Name)" -ForegroundColor Yellow
    foreach ($item in $group.Group) {
        Write-Host "  - $($item.Key)" -ForegroundColor Gray
    }
}

# Check for consistency
$uniqueVersions = $versions.Values | Select-Object -Unique
if ($uniqueVersions.Count -gt 1) {
    Write-Host ""
    Write-Host "⚠️  Warning: Versions are not synchronized across repositories" -ForegroundColor Yellow
    Write-Host "   Consider using sync-versions.ps1 to synchronize versions" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "✅ All repositories use the same version: $($uniqueVersions[0])" -ForegroundColor Green
}

Write-Host ""

