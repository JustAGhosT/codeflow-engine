<#
.SYNOPSIS
Analyzes and provides recommendations for Docker image optimization.

.DESCRIPTION
Analyzes Dockerfile and provides optimization recommendations.

.PARAMETER DockerfilePath
Path to the Dockerfile.

.PARAMETER ImageName
Docker image name to analyze (if already built).

.EXAMPLE
.\optimize-docker-image.ps1 -DockerfilePath ".\Dockerfile"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$DockerfilePath,
    
    [string]$ImageName = ""
)

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker Image Optimization Analysis" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $DockerfilePath)) {
    Write-Host "✗ Dockerfile not found: $DockerfilePath" -ForegroundColor Red
    exit 1
}

# ============================================================================
# Analyze Dockerfile
# ============================================================================

Write-Host "Analyzing Dockerfile..." -ForegroundColor Yellow

$dockerfileContent = Get-Content $DockerfilePath -Raw
$lines = Get-Content $DockerfilePath
$recommendations = @()
$issues = @()
$warnings = @()

# Check for base image
if ($dockerfileContent -match "FROM\s+(\S+)") {
    $baseImage = $matches[1]
    Write-Host "  Base image: $baseImage" -ForegroundColor Gray
    
    if ($baseImage -notmatch "alpine|slim|distroless") {
        $recommendations += "Consider using a smaller base image (alpine, slim, or distroless)"
    }
} else {
    $issues += "No FROM instruction found"
}

# Check for multi-stage build
if ($dockerfileContent -notmatch "FROM.*AS|FROM.*as") {
    $recommendations += "Consider using multi-stage builds to reduce final image size"
}

# Check for .dockerignore
$dockerfileDir = Split-Path $DockerfilePath -Parent
$dockerignorePath = Join-Path $dockerfileDir ".dockerignore"
if (-not (Test-Path $dockerignorePath)) {
    $warnings += ".dockerignore file not found - may include unnecessary files in build context"
}

# Check for layer optimization
$copyCount = ([regex]::Matches($dockerfileContent, "COPY|ADD")).Count
if ($copyCount -gt 5) {
    $recommendations += "Consider combining COPY commands to reduce layers"
}

# Check for RUN command optimization
$runCount = ([regex]::Matches($dockerfileContent, "RUN\s+")).Count
if ($runCount -gt 3) {
    $recommendations += "Consider combining RUN commands to reduce layers"
}

# Check for cleanup in RUN commands
if ($dockerfileContent -match "RUN.*apt-get.*install" -and $dockerfileContent -notmatch "apt-get.*clean|rm.*/var/lib/apt") {
    $recommendations += "Clean up apt cache in RUN commands to reduce image size"
}

# Check for unnecessary packages
if ($dockerfileContent -match "apt-get.*install" -and $dockerfileContent -notmatch "--no-install-recommends") {
    $recommendations += "Use --no-install-recommends in apt-get install to reduce package size"
}

# Check for user specification
if ($dockerfileContent -notmatch "USER\s+") {
    $warnings += "Consider running as non-root user for security"
}

# Check for WORKDIR
if ($dockerfileContent -notmatch "WORKDIR\s+") {
    $warnings += "Consider using WORKDIR instead of cd commands"
}

# Check for EXPOSE
if ($dockerfileContent -notmatch "EXPOSE\s+") {
    $warnings += "Consider adding EXPOSE instruction for documentation"
}

Write-Host "  ✓ Analysis complete" -ForegroundColor Green
Write-Host ""

# ============================================================================
# Analyze Image Size (if image name provided)
# ============================================================================

if (-not [string]::IsNullOrEmpty($ImageName)) {
    Write-Host "Analyzing image size..." -ForegroundColor Yellow
    
    try {
        $imageInfo = docker image inspect $ImageName 2>&1 | ConvertFrom-Json
        if ($imageInfo) {
            $size = $imageInfo[0].Size
            $sizeMB = [math]::Round($size / 1MB, 2)
            $sizeGB = [math]::Round($size / 1GB, 2)
            
            Write-Host "  Image size: $sizeMB MB ($sizeGB GB)" -ForegroundColor Gray
            
            if ($sizeMB -gt 500) {
                $recommendations += "Image size is large ($sizeMB MB) - consider optimization"
            }
        }
    } catch {
        Write-Host "  ⚠ Could not analyze image size (image may not be built)" -ForegroundColor Yellow
    }
    
    Write-Host ""
}

# ============================================================================
# Display Results
# ============================================================================

Write-Host "========================================" -ForegroundColor $(if ($issues.Count -eq 0) { "Green" } else { "Red" })
Write-Host "Dockerfile Analysis Results" -ForegroundColor $(if ($issues.Count -eq 0) { "Green" } else { "Red" })
Write-Host "========================================" -ForegroundColor $(if ($issues.Count -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($issues.Count -gt 0) {
    Write-Host "Issues:" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "  ✗ $issue" -ForegroundColor Red
    }
    Write-Host ""
}

if ($warnings.Count -gt 0) {
    Write-Host "Warnings:" -ForegroundColor Yellow
    foreach ($warning in $warnings) {
        Write-Host "  ⚠ $warning" -ForegroundColor Yellow
    }
    Write-Host ""
}

if ($recommendations.Count -gt 0) {
    Write-Host "Recommendations:" -ForegroundColor Cyan
    foreach ($rec in $recommendations) {
        Write-Host "  • $rec" -ForegroundColor Gray
    }
    Write-Host ""
}

if ($issues.Count -eq 0 -and $warnings.Count -eq 0 -and $recommendations.Count -eq 0) {
    Write-Host "✓ Dockerfile looks good!" -ForegroundColor Green
    Write-Host ""
}

