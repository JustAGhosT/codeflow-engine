<#
.SYNOPSIS
Migrates all "CODEFLOW" references to "codeflow" across the codebase.

.DESCRIPTION
This script performs a comprehensive search and replace operation to migrate
all "CODEFLOW" and "CODEFLOW" references to "codeflow" and "CodeFlow" respectively.

.PARAMETER RepoPath
Path to the repository root to process. If not specified, processes all repos.

.PARAMETER DryRun
If specified, shows what would be changed without making changes.

.PARAMETER ExcludePatterns
Array of file patterns to exclude from migration (e.g., "*.lock", "*.json.bak")

.EXAMPLE
.\migrate-codeflow-to-codeflow.ps1 -DryRun
Shows what would be changed without making changes.

.EXAMPLE
.\migrate-codeflow-to-codeflow.ps1 -RepoPath "C:\Users\smitj\repos\codeflow-engine"
Processes only the codeflow-engine repository.
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$RepoPath = "",
    [switch]$DryRun = $false,
    [string[]]$ExcludePatterns = @(
        "*.lock", "*.log", "*.bak", 
        "node_modules", ".git", "dist", "build", "__pycache__", ".venv", "venv",
        "*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll", "*.exe",
        "*.png", "*.jpg", "*.jpeg", "*.gif", "*.ico", "*.pdf",
        "*.zip", "*.tar", "*.gz", "*.whl", "*.egg",
        "htmlcov", "coverage", ".coverage", "*.egg-info",
        "*.vsix", "*.vsix.bak", ".next", "out", ".vercel"
    )
)

$ErrorActionPreference = 'Stop'

# Migration mappings - using arrays to handle case-sensitive replacements
$mappings = @(
    # Case-sensitive replacements (order matters - more specific first)
    @{ Pattern = 'app.codeflow.io'; Replacement = 'app.codeflow.io' },
    @{ Pattern = 'codeflow.io'; Replacement = 'codeflow.io' },
    @{ Pattern = 'codeflow-repo-migration'; Replacement = 'codeflow-repo-migration' },
    @{ Pattern = 'codeflow-workflow'; Replacement = 'codeflow-workflow' },
    @{ Pattern = 'codeflow-minimal'; Replacement = 'codeflow-minimal' },
    @{ Pattern = 'codeflow-advanced'; Replacement = 'codeflow-advanced' },
    @{ Pattern = 'codeflow-overview'; Replacement = 'codeflow-overview' },
    @{ Pattern = 'codeflow-saas'; Replacement = 'codeflow-saas' },
    @{ Pattern = 'codeflow-engine'; Replacement = 'codeflow-engine' },
    @{ Pattern = 'codeflow-io'; Replacement = 'codeflow-io' },
    @{ Pattern = 'codeflow-'; Replacement = 'codeflow-' },
    @{ Pattern = '-codeflow'; Replacement = '-codeflow' },
    @{ Pattern = 'codeflow_'; Replacement = 'codeflow_' },
    @{ Pattern = '_codeflow'; Replacement = '_codeflow' },
    @{ Pattern = 'codeflow.'; Replacement = 'codeflow.' },
    @{ Pattern = '.codeflow'; Replacement = '.codeflow' },
    @{ Pattern = 'CODEFLOW'; Replacement = 'CODEFLOW' },
    @{ Pattern = 'CODEFLOW'; Replacement = 'CodeFlow' },
    @{ Pattern = 'CODEFLOW'; Replacement = 'codeflow' }
)

# Get all repository paths
$repos = @()
if ($RepoPath) {
    $repos = @($RepoPath)
} else {
    $basePath = Split-Path $PSScriptRoot -Parent
    $repos = @(
        "$basePath\..\codeflow-engine",
        "$basePath\..\codeflow-desktop",
        "$basePath\..\codeflow-vscode-extension",
        "$basePath\..\codeflow-website",
        "$basePath\..\codeflow-infrastructure",
        "$basePath\..\codeflow-azure-setup",
        "$basePath\..\codeflow-orchestration"
    )
}

$totalFiles = 0
$totalReplacements = 0
$skippedFiles = 0

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CODEFLOW to CodeFlow Migration Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
if ($DryRun) {
    Write-Host "DRY RUN MODE - No files will be modified" -ForegroundColor Yellow
    Write-Host ""
}

foreach ($repo in $repos) {
    if (-not (Test-Path $repo)) {
        Write-Host "âš ï¸  Repository not found: $repo" -ForegroundColor Yellow
        continue
    }
    
    Write-Host "Processing: $repo" -ForegroundColor Green
    Write-Host "----------------------------------------" -ForegroundColor Gray
    
    # Get all files recursively, excluding patterns
    $files = Get-ChildItem -Path $repo -Recurse -File | Where-Object {
        $shouldInclude = $true
        $fullPath = $_.FullName
        
        # Skip if in excluded directories
        foreach ($pattern in $ExcludePatterns) {
            if ($fullPath -like "*\$pattern\*" -or $fullPath -like "*\$pattern" -or $_.Name -like $pattern) {
                $shouldInclude = $false
                break
            }
        }
        
        # Skip if in common build/exclude directories
        if ($fullPath -like "*\node_modules\*" -or 
            $fullPath -like "*\__pycache__\*" -or 
            $fullPath -like "*\.git\*" -or
            $fullPath -like "*\dist\*" -or
            $fullPath -like "*\build\*" -or
            $fullPath -like "*\htmlcov\*" -or
            $fullPath -like "*\.next\*" -or
            $fullPath -like "*\out\*" -or
            $fullPath -like "*\.venv\*" -or
            $fullPath -like "*\venv\*") {
            $shouldInclude = $false
        }
        
        $shouldInclude
    }
    
    $repoFiles = 0
    $repoReplacements = 0
    
    foreach ($file in $files) {
        try {
            # Skip binary and compiled files
            $ext = $file.Extension.ToLower()
            $name = $file.Name.ToLower()
            $binaryExts = @('.exe', '.dll', '.so', '.dylib', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.tar', '.gz', '.whl', '.egg', '.pyc', '.pyo', '.pyd', '.vsix', '.min.js', '.min.css')
            if ($binaryExts -contains $ext -or $name -like '*.min.*' -or $name -like '*.bundle.*') {
                continue
            }
            
            # Skip if file path contains excluded patterns
            $fullPath = $file.FullName
            if ($fullPath -like "*\node_modules\*" -or 
                $fullPath -like "*\__pycache__\*" -or 
                $fullPath -like "*\htmlcov\*" -or
                $fullPath -like "*\.next\*" -or
                $fullPath -like "*\dist\*" -or
                $fullPath -like "*\build\*") {
                continue
            }
            
            # Read file content
            $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
            if ($null -eq $content) {
                continue
            }
            
            $originalContent = $content
            $fileReplacements = 0
            
            # Apply all mappings (order matters - more specific patterns first)
            foreach ($mapping in $mappings) {
                $pattern = $mapping.Pattern
                $replacement = $mapping.Replacement
                $count = ([regex]::Matches($content, [regex]::Escape($pattern))).Count
                if ($count -gt 0) {
                    $content = $content -replace [regex]::Escape($pattern), $replacement
                    $fileReplacements += $count
                }
            }
            
            # Only process if changes were made
            if ($content -ne $originalContent) {
                $repoFiles++
                $totalFiles++
                $repoReplacements += $fileReplacements
                $totalReplacements += $fileReplacements
                
                $relativePath = $file.FullName.Replace($repo, '').TrimStart('\')
                Write-Host "  $relativePath ($fileReplacements replacements)" -ForegroundColor Gray
                
                if (-not $DryRun) {
                    # Backup original file
                    $backupPath = "$($file.FullName).codeflow-backup"
                    Copy-Item -Path $file.FullName -Destination $backupPath -Force
                    
                    # Write updated content
                    [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
                }
            }
        }
        catch {
            Write-Host "  âš ï¸  Error processing $($file.Name): $_" -ForegroundColor Yellow
            $skippedFiles++
        }
    }
    
    Write-Host ""
    Write-Host "  Files modified: $repoFiles" -ForegroundColor Cyan
    Write-Host "  Total replacements: $repoReplacements" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Migration Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total files modified: $totalFiles" -ForegroundColor Green
Write-Host "Total replacements: $totalReplacements" -ForegroundColor Green
Write-Host "Files skipped: $skippedFiles" -ForegroundColor Yellow
Write-Host ""

if ($DryRun) {
    Write-Host "This was a dry run. Run without -DryRun to apply changes." -ForegroundColor Yellow
} else {
    Write-Host "Migration complete! Backup files created with .codeflow-backup extension." -ForegroundColor Green
    Write-Host "Review changes and remove backup files when satisfied." -ForegroundColor Gray
}

