<#
.SYNOPSIS
Health check script for deployed services.

.DESCRIPTION
Performs comprehensive health checks on deployed CodeFlow services.

.PARAMETER HealthCheckUrl
Base URL for health check endpoint.

.PARAMETER Timeout
Timeout in seconds for health checks. Default: 60

.PARAMETER Retries
Number of retry attempts. Default: 3

.PARAMETER RetryDelay
Delay between retries in seconds. Default: 5

.EXAMPLE
.\health-check.ps1 -HealthCheckUrl "https://api.codeflow.example.com"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$HealthCheckUrl,
    
    [int]$Timeout = 60,
    
    [int]$Retries = 3,
    
    [int]$RetryDelay = 5
)

$ErrorActionPreference = 'Stop'

# ============================================================================
# Health Check Functions
# ============================================================================

function Test-HealthEndpoint {
    param(
        [string]$Url,
        [int]$TimeoutSeconds
    )
    
    try {
        $response = Invoke-WebRequest -Uri $Url -Method Get -TimeoutSec $TimeoutSeconds -UseBasicParsing -ErrorAction Stop
        
        if ($response.StatusCode -eq 200) {
            $body = $response.Content | ConvertFrom-Json -ErrorAction SilentlyContinue
            return @{
                Success = $true
                StatusCode = $response.StatusCode
                Status = $body.status
                Details = $body
            }
        } else {
            return @{
                Success = $false
                StatusCode = $response.StatusCode
                Error = "Unexpected status code: $($response.StatusCode)"
            }
        }
    } catch {
        return @{
            Success = $false
            Error = $_.Exception.Message
        }
    }
}

function Test-DetailedHealth {
    param(
        [string]$BaseUrl
    )
    
    $detailedUrl = "$BaseUrl/health?detailed=true"
    return Test-HealthEndpoint -Url $detailedUrl -TimeoutSeconds 30
}

# ============================================================================
# Main Health Check
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Health Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target: $HealthCheckUrl" -ForegroundColor White
Write-Host ""

$allChecksPassed = $true
$attempt = 0

while ($attempt -lt $Retries) {
    $attempt++
    Write-Host "Health Check Attempt $attempt of $Retries..." -ForegroundColor Yellow
    
    # Basic health check
    $healthCheck = Test-HealthEndpoint -Url "$HealthCheckUrl/health" -TimeoutSeconds $Timeout
    
    if ($healthCheck.Success) {
        Write-Host "  ✓ Basic health check passed" -ForegroundColor Green
        Write-Host "    Status: $($healthCheck.Status)" -ForegroundColor Gray
        
        # Detailed health check
        $detailedCheck = Test-DetailedHealth -BaseUrl $HealthCheckUrl
        
        if ($detailedCheck.Success) {
            Write-Host "  ✓ Detailed health check passed" -ForegroundColor Green
            
            # Display component status
            if ($detailedCheck.Details) {
                Write-Host "    Components:" -ForegroundColor Gray
                if ($detailedCheck.Details.database) {
                    $dbStatus = if ($detailedCheck.Details.database.healthy) { "✓" } else { "✗" }
                    Write-Host "      $dbStatus Database" -ForegroundColor $(if ($detailedCheck.Details.database.healthy) { "Green" } else { "Red" })
                }
                if ($detailedCheck.Details.redis) {
                    $redisStatus = if ($detailedCheck.Details.redis.healthy) { "✓" } else { "✗" }
                    Write-Host "      $redisStatus Redis" -ForegroundColor $(if ($detailedCheck.Details.redis.healthy) { "Green" } else { "Red" })
                }
            }
            
            $allChecksPassed = $true
            break
        } else {
            Write-Host "  ✗ Detailed health check failed: $($detailedCheck.Error)" -ForegroundColor Red
            $allChecksPassed = $false
        }
    } else {
        Write-Host "  ✗ Health check failed: $($healthCheck.Error)" -ForegroundColor Red
        $allChecksPassed = $false
        
        if ($attempt -lt $Retries) {
            Write-Host "  Waiting $RetryDelay seconds before retry..." -ForegroundColor Yellow
            Start-Sleep -Seconds $RetryDelay
        }
    }
    
    Write-Host ""
}

# ============================================================================
# Summary
# ============================================================================

Write-Host "========================================" -ForegroundColor $(if ($allChecksPassed) { "Green" } else { "Red" })
if ($allChecksPassed) {
    Write-Host "Health Check: PASSED" -ForegroundColor Green
    exit 0
} else {
    Write-Host "Health Check: FAILED" -ForegroundColor Red
    exit 1
}

