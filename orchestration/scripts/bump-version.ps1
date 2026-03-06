#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Bump version in a CodeFlow repository.

.DESCRIPTION
    This script bumps the version in a CodeFlow repository according to
    semantic versioning rules.

.PARAMETER RepoPath
    Path to the repository. Defaults to current directory.

.PARAMETER Type
    Type of version bump: major, minor, or patch.

.PARAMETER Version
    Specific version to set (e.g., "1.2.3").

.PARAMETER DryRun
    Show what would be changed without making changes.

.EXAMPLE
    .\bump-version.ps1 -Type patch

.EXAMPLE
    .\bump-version.ps1 -Type minor -RepoPath "C:\repos\codeflow-engine"

.EXAMPLE
    .\bump-version.ps1 -Version "1.2.3" -DryRun
#>

param(
    [string]$RepoPath = (Get-Location).Path,
    [ValidateSet("major", "minor", "patch")]
    [string]$Type,
    [string]$Version,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Get-CurrentVersion {
    param([string]$Path)

    $pyprojectPath = Join-Path $Path "pyproject.toml"
    $packageJsonPath = Join-Path $Path "package.json"

    if (Test-Path $pyprojectPath) {
        $content = Get-Content $pyprojectPath -Raw
        if ($content -match 'version\s*=\s*"([^"]+)"') {
            return $matches[1]
        }
    }

    if (Test-Path $packageJsonPath) {
        $content = Get-Content $packageJsonPath -Raw
        if ($content -match '"version"\s*:\s*"([^"]+)"') {
            return $matches[1]
        }
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

function Bump-Version {
    param(
        [string]$CurrentVersion,
        [string]$Type
    )

    if (-not ($CurrentVersion -match '^(\d+)\.(\d+)\.(\d+)')) {
        throw "Invalid version format: $CurrentVersion"
    }

    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    $patch = [int]$matches[3]

    switch ($Type) {
        "major" {
            $major++
            $minor = 0
            $patch = 0
        }
        "minor" {
            $minor++
            $patch = 0
        }
        "patch" {
            $patch++
        }
    }

    return "$major.$minor.$patch"
}

Write-Host "CodeFlow Version Bump" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
Write-Host ""

$currentVersion = Get-CurrentVersion -Path $RepoPath

if (-not $currentVersion) {
    Write-Host "❌ Could not determine current version" -ForegroundColor Red
    exit 1
}

Write-Host "Current version: $currentVersion" -ForegroundColor Yellow

if ($Version) {
    $newVersion = $Version
} elseif ($Type) {
    $newVersion = Bump-Version -CurrentVersion $currentVersion -Type $Type
} else {
    Write-Host "❌ Either -Type or -Version must be specified" -ForegroundColor Red
    exit 1
}

Write-Host "New version: $newVersion" -ForegroundColor Green

if ($DryRun) {
    Write-Host ""
    Write-Host "🔍 Dry run mode - no changes will be made" -ForegroundColor Yellow
}

Write-Host ""

# Update pyproject.toml
$pyprojectPath = Join-Path $RepoPath "pyproject.toml"
if (Test-Path $pyprojectPath) {
    $updated = Set-VersionInFile -FilePath $pyprojectPath `
        -OldVersion $currentVersion `
        -NewVersion $newVersion `
        -Pattern "version\s*=\s*`"$([regex]::Escape($currentVersion))`""
    
    if ($updated) {
        Write-Host "✅ Updated pyproject.toml" -ForegroundColor Green
    } elseif ($DryRun) {
        Write-Host "📝 Would update pyproject.toml" -ForegroundColor Gray
    }
}

# Update package.json
$packageJsonPath = Join-Path $RepoPath "package.json"
if (Test-Path $packageJsonPath) {
    $updated = Set-VersionInFile -FilePath $packageJsonPath `
        -OldVersion $currentVersion `
        -NewVersion $newVersion `
        -Pattern "`"version`"\s*:\s*`"$([regex]::Escape($currentVersion))`""
    
    if ($updated) {
        Write-Host "✅ Updated package.json" -ForegroundColor Green
    } elseif ($DryRun) {
        Write-Host "📝 Would update package.json" -ForegroundColor Gray
    }
}

if (-not $DryRun) {
    Write-Host ""
    Write-Host "✅ Version bumped successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Update CHANGELOG.md" -ForegroundColor Gray
    Write-Host "2. Commit changes: git commit -am 'chore: bump version to $newVersion'" -ForegroundColor Gray
    Write-Host "3. Create tag: git tag -a v$newVersion -m 'Release version $newVersion'" -ForegroundColor Gray
    Write-Host "4. Push tag: git push origin v$newVersion" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "🔍 Dry run complete - no changes made" -ForegroundColor Yellow
}

Write-Host ""

