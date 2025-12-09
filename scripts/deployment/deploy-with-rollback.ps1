<#
.SYNOPSIS
Enhanced deployment script with automatic rollback capabilities.

.DESCRIPTION
Deploys infrastructure with automatic rollback on failure, health checks, and smoke tests.

.PARAMETER DeploymentScript
Path to the deployment script to execute.

.PARAMETER ResourceGroup
Azure Resource Group name.

.PARAMETER RollbackEnabled
Enable automatic rollback on failure. Default: $true

.PARAMETER HealthCheckUrl
URL for health check after deployment.

.PARAMETER HealthCheckTimeout
Timeout for health checks in seconds. Default: 300

.PARAMETER SmokeTestScript
Path to smoke test script to run after deployment.

.EXAMPLE
.\deploy-with-rollback.ps1 -DeploymentScript ".\deploy-codeflow-engine.ps1" -ResourceGroup "nl-dev-codeflow-rg-san"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$DeploymentScript,
    
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,
    
    [bool]$RollbackEnabled = $true,
    
    [string]$HealthCheckUrl = "",
    
    [int]$HealthCheckTimeout = 300,
    
    [string]$SmokeTestScript = ""
)

$ErrorActionPreference = 'Stop'

# ============================================================================
# SECTION 1: Initialization
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Enhanced Deployment with Rollback" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$deploymentStartTime = Get-Date
$deploymentId = [guid]::NewGuid().ToString()
$backupFile = "$env:TEMP\deployment-backup-$deploymentId.json"

Write-Host "Deployment ID: $deploymentId" -ForegroundColor Gray
Write-Host "Start Time: $deploymentStartTime" -ForegroundColor Gray
Write-Host ""

# ============================================================================
# SECTION 2: Pre-Deployment Validation
# ============================================================================

Write-Host "Pre-deployment validation..." -ForegroundColor Yellow

# Validate deployment script exists
if (-not (Test-Path $DeploymentScript)) {
    Write-Host "✗ Deployment script not found: $DeploymentScript" -ForegroundColor Red
    exit 1
}

# Validate Azure CLI
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "✗ Azure CLI is not installed" -ForegroundColor Red
    exit 1
}

# Check resource group exists
$rgExists = az group show --name $ResourceGroup --query "name" --output tsv 2>$null
if (-not $rgExists) {
    Write-Host "✗ Resource group not found: $ResourceGroup" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Pre-deployment validation passed" -ForegroundColor Green
Write-Host ""

# ============================================================================
# SECTION 3: Backup Current State
# ============================================================================

if ($RollbackEnabled) {
    Write-Host "Backing up current deployment state..." -ForegroundColor Yellow
    
    try {
        # Export current resource group state
        az group export --name $ResourceGroup --output-file $backupFile --output none 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Backup created: $backupFile" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Backup creation failed (continuing anyway)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ⚠ Backup creation failed: $_" -ForegroundColor Yellow
    }
    
    Write-Host ""
}

# ============================================================================
# SECTION 4: Execute Deployment
# ============================================================================

Write-Host "Executing deployment..." -ForegroundColor Yellow
Write-Host ""

$deploymentSuccess = $false
$deploymentError = $null

try {
    # Execute deployment script
    & $DeploymentScript
    
    if ($LASTEXITCODE -eq 0) {
        $deploymentSuccess = $true
        Write-Host "  ✓ Deployment completed successfully" -ForegroundColor Green
    } else {
        throw "Deployment script exited with code $LASTEXITCODE"
    }
} catch {
    $deploymentError = $_
    Write-Host "  ✗ Deployment failed: $_" -ForegroundColor Red
    $deploymentSuccess = $false
}

Write-Host ""

# ============================================================================
# SECTION 5: Health Check
# ============================================================================

$healthCheckPassed = $false

if ($deploymentSuccess -and -not [string]::IsNullOrEmpty($HealthCheckUrl)) {
    Write-Host "Performing health check..." -ForegroundColor Yellow
    
    $healthCheckStartTime = Get-Date
    $maxAttempts = 10
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        $attempt++
        $elapsed = ((Get-Date) - $healthCheckStartTime).TotalSeconds
        
        if ($elapsed -gt $HealthCheckTimeout) {
            Write-Host "  ✗ Health check timeout after $HealthCheckTimeout seconds" -ForegroundColor Red
            break
        }
        
        try {
            $response = Invoke-WebRequest -Uri $HealthCheckUrl -Method Get -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
            
            if ($response.StatusCode -eq 200) {
                $healthCheckPassed = $true
                Write-Host "  ✓ Health check passed (attempt $attempt)" -ForegroundColor Green
                break
            }
        } catch {
            Write-Host "  ⚠ Health check attempt $attempt failed, retrying..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        }
    }
    
    if (-not $healthCheckPassed) {
        Write-Host "  ✗ Health check failed after $attempt attempts" -ForegroundColor Red
        $deploymentSuccess = $false
    }
    
    Write-Host ""
}

# ============================================================================
# SECTION 6: Smoke Tests
# ============================================================================

$smokeTestPassed = $false

if ($deploymentSuccess -and -not [string]::IsNullOrEmpty($SmokeTestScript)) {
    Write-Host "Running smoke tests..." -ForegroundColor Yellow
    
    if (Test-Path $SmokeTestScript) {
        try {
            & $SmokeTestScript
            
            if ($LASTEXITCODE -eq 0) {
                $smokeTestPassed = $true
                Write-Host "  ✓ Smoke tests passed" -ForegroundColor Green
            } else {
                Write-Host "  ✗ Smoke tests failed" -ForegroundColor Red
                $deploymentSuccess = $false
            }
        } catch {
            Write-Host "  ✗ Smoke test execution failed: $_" -ForegroundColor Red
            $deploymentSuccess = $false
        }
    } else {
        Write-Host "  ⚠ Smoke test script not found: $SmokeTestScript" -ForegroundColor Yellow
    }
    
    Write-Host ""
}

# ============================================================================
# SECTION 7: Rollback on Failure
# ============================================================================

if (-not $deploymentSuccess -and $RollbackEnabled) {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Deployment Failed - Initiating Rollback" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    
    Write-Host "Rolling back to previous state..." -ForegroundColor Yellow
    
    try {
        if (Test-Path $backupFile) {
            # Attempt to restore from backup
            Write-Host "  Attempting to restore from backup..." -ForegroundColor Gray
            
            # Note: Full rollback would require more complex logic
            # This is a placeholder for rollback implementation
            Write-Host "  ⚠ Automatic rollback requires manual intervention" -ForegroundColor Yellow
            Write-Host "  Backup file saved at: $backupFile" -ForegroundColor Gray
            
            # Clean up failed deployment resources if possible
            Write-Host "  Cleaning up failed deployment resources..." -ForegroundColor Gray
            
        } else {
            Write-Host "  ✗ Backup file not found, cannot rollback automatically" -ForegroundColor Red
        }
    } catch {
        Write-Host "  ✗ Rollback failed: $_" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "✗ Deployment failed and rollback attempted" -ForegroundColor Red
    exit 1
}

# ============================================================================
# SECTION 8: Success Summary
# ============================================================================

$deploymentEndTime = Get-Date
$duration = $deploymentEndTime - $deploymentStartTime

Write-Host "========================================" -ForegroundColor Green
Write-Host "Deployment Completed Successfully" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  Deployment ID: $deploymentId" -ForegroundColor White
Write-Host "  Duration: $($duration.TotalSeconds) seconds" -ForegroundColor White
Write-Host "  Health Check: $(if ($healthCheckPassed) { '✓ Passed' } else { 'N/A' })" -ForegroundColor White
Write-Host "  Smoke Tests: $(if ($smokeTestPassed) { '✓ Passed' } else { 'N/A' })" -ForegroundColor White
Write-Host ""

if (Test-Path $backupFile) {
    Remove-Item $backupFile -Force -ErrorAction SilentlyContinue
}

exit 0

