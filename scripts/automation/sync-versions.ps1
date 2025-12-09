<#
.SYNOPSIS
Synchronizes versions across CodeFlow repositories.

.DESCRIPTION
Ensures version consistency across multiple repositories and updates version files.

.PARAMETER Repositories
Array of repository paths to sync.

.PARAMETER Version
Version to set (e.g., "1.2.3"). If not provided, reads from first repository.

.PARAMETER DryRun
Show what would be changed without making changes. Default: $false

.EXAMPLE
.\sync-versions.ps1 -Repositories @("C:\repos\codeflow-engine", "C:\repos\codeflow-desktop") -Version "1.2.3"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string[]]$Repositories,
    
    [string]$Version = "",
    
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Version Synchronization" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

# ============================================================================
# Get Current Version
# ============================================================================

if ([string]::IsNullOrEmpty($Version)) {
    Write-Host "Reading version from first repository..." -ForegroundColor Yellow
    
    $firstRepo = $Repositories[0]
    if (-not (Test-Path $firstRepo)) {
        Write-Host "✗ Repository not found: $firstRepo" -ForegroundColor Red
        exit 1
    }
    
    Push-Location $firstRepo
    
    # Try to read version from various files
    if (Test-Path "package.json") {
        $packageJson = Get-Content "package.json" | ConvertFrom-Json
        $Version = $packageJson.version
    } elseif (Test-Path "pyproject.toml") {
        $pyproject = Get-Content "pyproject.toml" -Raw
        if ($pyproject -match 'version\s*=\s*"([^"]+)"') {
            $Version = $matches[1]
        }
    } elseif (Test-Path "version.txt") {
        $Version = Get-Content "version.txt" -Raw
    }
    
    Pop-Location
    
    if ([string]::IsNullOrEmpty($Version)) {
        Write-Host "✗ Could not determine version" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "  Found version: $Version" -ForegroundColor Green
    Write-Host ""
}

# ============================================================================
# Update Versions
# ============================================================================

$results = @()

foreach ($repo in $Repositories) {
    if (-not (Test-Path $repo)) {
        Write-Host "✗ Repository not found: $repo" -ForegroundColor Red
        continue
    }
    
    Write-Host "Processing: $repo" -ForegroundColor Yellow
    Push-Location $repo
    
    $updated = $false
    $oldVersion = ""
    
    # Update package.json
    if (Test-Path "package.json") {
        $packageJson = Get-Content "package.json" | ConvertFrom-Json
        $oldVersion = $packageJson.version
        
        if ($packageJson.version -ne $Version) {
            if (-not $DryRun) {
                $packageJson.version = $Version
                $packageJson | ConvertTo-Json -Depth 10 | Set-Content "package.json" -Encoding utf8
            }
            $updated = $true
            Write-Host "  Updated package.json: $oldVersion -> $Version" -ForegroundColor Green
        } else {
            Write-Host "  package.json already at version $Version" -ForegroundColor Gray
        }
    }
    
    # Update pyproject.toml
    if (Test-Path "pyproject.toml") {
        $pyprojectContent = Get-Content "pyproject.toml" -Raw
        
        if ($pyprojectContent -match 'version\s*=\s*"([^"]+)"') {
            $oldVersion = $matches[1]
            
            if ($oldVersion -ne $Version) {
                if (-not $DryRun) {
                    $pyprojectContent = $pyprojectContent -replace 'version\s*=\s*"[^"]+"', "version = `"$Version`""
                    $pyprojectContent | Set-Content "pyproject.toml" -Encoding utf8
                }
                $updated = $true
                Write-Host "  Updated pyproject.toml: $oldVersion -> $Version" -ForegroundColor Green
            } else {
                Write-Host "  pyproject.toml already at version $Version" -ForegroundColor Gray
            }
        }
    }
    
    # Update version.txt
    if (Test-Path "version.txt") {
        $oldVersion = Get-Content "version.txt" -Raw
        
        if ($oldVersion.Trim() -ne $Version) {
            if (-not $DryRun) {
                $Version | Set-Content "version.txt" -Encoding utf8
            }
            $updated = $true
            Write-Host "  Updated version.txt: $oldVersion -> $Version" -ForegroundColor Green
        } else {
            Write-Host "  version.txt already at version $Version" -ForegroundColor Gray
        }
    }
    
    $results += @{
        Repository = $repo
        OldVersion = $oldVersion
        NewVersion = $Version
        Updated = $updated
    }
    
    Pop-Location
    Write-Host ""
}

# ============================================================================
# Summary
# ============================================================================

Write-Host "========================================" -ForegroundColor Green
Write-Host "Version Sync Summary" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

$updatedCount = ($results | Where-Object { $_.Updated }).Count

Write-Host "Repositories processed: $($results.Count)" -ForegroundColor White
Write-Host "Repositories updated: $updatedCount" -ForegroundColor $(if ($updatedCount -gt 0) { "Green" } else { "Gray" })
Write-Host "Target version: $Version" -ForegroundColor White
Write-Host ""

if ($DryRun) {
    Write-Host "This was a dry run. Use without -DryRun to apply changes." -ForegroundColor Yellow
}

