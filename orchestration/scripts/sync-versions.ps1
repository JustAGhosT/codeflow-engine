#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Synchronize versions across all CodeFlow repositories.

.DESCRIPTION
    This script synchronizes the version across all CodeFlow repositories
    to ensure consistency for coordinated releases.

.PARAMETER Version
    Version to set (e.g., "1.2.3"). If not specified, uses the version
    from codeflow-engine as the source of truth.

.PARAMETER RepoPath
    Base path to CodeFlow repositories. Defaults to parent directory.

.PARAMETER DryRun
    Show what would be changed without making changes.

.EXAMPLE
    .\sync-versions.ps1 -Version "1.2.0"

.EXAMPLE
    .\sync-versions.ps1 -DryRun

.EXAMPLE
    .\sync-versions.ps1 -Version "1.2.0" -RepoPath "C:\repos"
#>

param(
    [string]$Version,
    [string]$RepoPath = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent),
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Get-VersionFromFile {
    param(
        [string]$FilePath,
        [string]$Pattern
    )

    if (-not (Test-Path $FilePath)) {
        return $null
    }

    $content = Get-Content $FilePath -Raw
    if ($content -match $Pattern) {
        return $matches[1]
    }

    return $null
}

function Set-VersionInFile {
    param(
        [string]$FilePath,
        [string]$OldVersion,
        [string]$NewVersion,
        [string]$Pattern
    )

    if (-not (Test-Path $FilePath)) {
        return $false
    }

    $content = Get-Content $FilePath -Raw
    $newContent = $content -replace $Pattern, $NewVersion

    if ($content -ne $newContent) {
        if (-not $DryRun) {
            Set-Content -Path $FilePath -Value $newContent -NoNewline
        }
        return $true
    }

    return $false
}

Write-Host "CodeFlow Version Synchronization" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Determine target version
if (-not $Version) {
    $enginePath = Join-Path $RepoPath "codeflow-engine"
    $pyprojectPath = Join-Path $enginePath "pyproject.toml"
    
    $Version = Get-VersionFromFile -FilePath $pyprojectPath -Pattern 'version\s*=\s*"([^"]+)"'
    
    if (-not $Version) {
        Write-Host "❌ Could not determine version from codeflow-engine" -ForegroundColor Red
        Write-Host "   Please specify -Version parameter" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "Using version from codeflow-engine: $Version" -ForegroundColor Yellow
} else {
    Write-Host "Using specified version: $Version" -ForegroundColor Yellow
}

# Validate version format
if (-not ($Version -match '^\d+\.\d+\.\d+')) {
    Write-Host "❌ Invalid version format: $Version" -ForegroundColor Red
    Write-Host "   Expected format: MAJOR.MINOR.PATCH (e.g., 1.2.3)" -ForegroundColor Yellow
    exit 1
}

if ($DryRun) {
    Write-Host ""
    Write-Host "🔍 Dry run mode - no changes will be made" -ForegroundColor Yellow
}

Write-Host ""

# Define repositories to update
$repos = @(
    @{
        Name = "codeflow-engine"
        File = "pyproject.toml"
        Pattern = 'version\s*=\s*"([^"]+)"'
        Replacement = "version = `"$Version`""
    },
    @{
        Name = "codeflow-desktop"
        File = "package.json"
        Pattern = '"version"\s*:\s*"([^"]+)"'
        Replacement = "`"version`": `"$Version`""
    },
    @{
        Name = "codeflow-vscode-extension"
        File = "package.json"
        Pattern = '"version"\s*:\s*"([^"]+)"'
        Replacement = "`"version`": `"$Version`""
    },
    @{
        Name = "codeflow-website"
        File = "package.json"
        Pattern = '"version"\s*:\s*"([^"]+)"'
        Replacement = "`"version`": `"$Version`""
    }
)

$updated = 0
$skipped = 0
$errors = 0

foreach ($repo in $repos) {
    $repoPath = Join-Path $RepoPath $repo.Name
    $filePath = Join-Path $repoPath $repo.File

    if (-not (Test-Path $filePath)) {
        Write-Host "⚠️  $($repo.Name): File not found ($($repo.File))" -ForegroundColor Yellow
        $skipped++
        continue
    }

    $currentVersion = Get-VersionFromFile -FilePath $filePath -Pattern $repo.Pattern

    if (-not $currentVersion) {
        Write-Host "⚠️  $($repo.Name): Could not read current version" -ForegroundColor Yellow
        $skipped++
        continue
    }

    if ($currentVersion -eq $Version) {
        Write-Host "✅ $($repo.Name): Already at version $Version" -ForegroundColor Green
        continue
    }

    Write-Host "📝 $($repo.Name): $currentVersion → $Version" -ForegroundColor Cyan

    $success = Set-VersionInFile -FilePath $filePath `
        -OldVersion $currentVersion `
        -NewVersion $Version `
        -Pattern $repo.Pattern

    if ($success) {
        if ($DryRun) {
            Write-Host "   (Would update)" -ForegroundColor Gray
        } else {
            Write-Host "   ✅ Updated" -ForegroundColor Green
        }
        $updated++
    } else {
        Write-Host "   ⚠️  Update failed" -ForegroundColor Yellow
        $errors++
    }
}

Write-Host ""
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "=======" -ForegroundColor Cyan
Write-Host "Target version: $Version" -ForegroundColor Yellow
Write-Host "Updated: $updated" -ForegroundColor Green
Write-Host "Skipped: $skipped" -ForegroundColor Gray
Write-Host "Errors: $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Gray" })

if (-not $DryRun -and $updated -gt 0) {
    Write-Host ""
    Write-Host "✅ Version synchronization complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Review changes: git diff" -ForegroundColor Gray
    Write-Host "2. Commit changes: git commit -am 'chore: sync versions to $Version'" -ForegroundColor Gray
    Write-Host "3. Update CHANGELOG.md files" -ForegroundColor Gray
} elseif ($DryRun) {
    Write-Host ""
    Write-Host "🔍 Dry run complete - no changes made" -ForegroundColor Yellow
}

Write-Host ""

