<#
.SYNOPSIS
Smoke tests for deployed CodeFlow services.

.DESCRIPTION
Runs critical path smoke tests to verify deployment.

.PARAMETER BaseUrl
Base URL for the deployed service.

.PARAMETER Timeout
Timeout in seconds for each test. Default: 30

.EXAMPLE
.\smoke-tests.ps1 -BaseUrl "https://api.codeflow.example.com"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$BaseUrl,
    
    [int]$Timeout = 30
)

$ErrorActionPreference = 'Stop'

# ============================================================================
# Test Functions
# ============================================================================

function Test-Endpoint {
    param(
        [string]$Url,
        [string]$Method = "GET",
        [hashtable]$Headers = @{},
        [int]$TimeoutSeconds = 30
    )
    
    try {
        $params = @{
            Uri = $Url
            Method = $Method
            TimeoutSec = $TimeoutSeconds
            UseBasicParsing = $true
            ErrorAction = "Stop"
        }
        
        if ($Headers.Count -gt 0) {
            $params.Headers = $Headers
        }
        
        $response = Invoke-WebRequest @params
        
        return @{
            Success = $true
            StatusCode = $response.StatusCode
            Content = $response.Content
        }
    } catch {
        return @{
            Success = $false
            Error = $_.Exception.Message
            StatusCode = $_.Exception.Response.StatusCode.value__
        }
    }
}

# ============================================================================
# Smoke Tests
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Smoke Tests" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target: $BaseUrl" -ForegroundColor White
Write-Host ""

$testsPassed = 0
$testsFailed = 0
$tests = @()

# Test 1: Root endpoint
Write-Host "Test 1: Root endpoint..." -ForegroundColor Yellow
$result = Test-Endpoint -Url $BaseUrl -TimeoutSeconds $Timeout
if ($result.Success) {
    Write-Host "  ✓ Root endpoint accessible" -ForegroundColor Green
    $testsPassed++
    $tests += @{ Name = "Root Endpoint"; Status = "PASSED" }
} else {
    Write-Host "  ✗ Root endpoint failed: $($result.Error)" -ForegroundColor Red
    $testsFailed++
    $tests += @{ Name = "Root Endpoint"; Status = "FAILED"; Error = $result.Error }
}
Write-Host ""

# Test 2: Health endpoint
Write-Host "Test 2: Health endpoint..." -ForegroundColor Yellow
$result = Test-Endpoint -Url "$BaseUrl/health" -TimeoutSeconds $Timeout
if ($result.Success -and $result.StatusCode -eq 200) {
    Write-Host "  ✓ Health endpoint accessible" -ForegroundColor Green
    $testsPassed++
    $tests += @{ Name = "Health Endpoint"; Status = "PASSED" }
} else {
    Write-Host "  ✗ Health endpoint failed: $($result.Error)" -ForegroundColor Red
    $testsFailed++
    $tests += @{ Name = "Health Endpoint"; Status = "FAILED"; Error = $result.Error }
}
Write-Host ""

# Test 3: Version endpoint
Write-Host "Test 3: Version endpoint..." -ForegroundColor Yellow
$result = Test-Endpoint -Url "$BaseUrl/version" -TimeoutSeconds $Timeout
if ($result.Success -and $result.StatusCode -eq 200) {
    Write-Host "  ✓ Version endpoint accessible" -ForegroundColor Green
    $testsPassed++
    $tests += @{ Name = "Version Endpoint"; Status = "PASSED" }
} else {
    Write-Host "  ⚠ Version endpoint not available (non-critical)" -ForegroundColor Yellow
    $tests += @{ Name = "Version Endpoint"; Status = "SKIPPED" }
}
Write-Host ""

# Test 4: Dashboard endpoint (if available)
Write-Host "Test 4: Dashboard endpoint..." -ForegroundColor Yellow
$result = Test-Endpoint -Url "$BaseUrl/api/dashboard" -TimeoutSeconds $Timeout
if ($result.Success -and $result.StatusCode -eq 200) {
    Write-Host "  ✓ Dashboard endpoint accessible" -ForegroundColor Green
    $testsPassed++
    $tests += @{ Name = "Dashboard Endpoint"; Status = "PASSED" }
} else {
    Write-Host "  ⚠ Dashboard endpoint not available (non-critical)" -ForegroundColor Yellow
    $tests += @{ Name = "Dashboard Endpoint"; Status = "SKIPPED" }
}
Write-Host ""

# Test 5: API response format
Write-Host "Test 5: API response format..." -ForegroundColor Yellow
$result = Test-Endpoint -Url "$BaseUrl/health" -TimeoutSeconds $Timeout
if ($result.Success) {
    try {
        $json = $result.Content | ConvertFrom-Json -ErrorAction Stop
        if ($json.status) {
            Write-Host "  ✓ API returns valid JSON" -ForegroundColor Green
            $testsPassed++
            $tests += @{ Name = "API Response Format"; Status = "PASSED" }
        } else {
            Write-Host "  ⚠ API returns JSON but missing expected fields" -ForegroundColor Yellow
            $tests += @{ Name = "API Response Format"; Status = "WARNING" }
        }
    } catch {
        Write-Host "  ✗ API response is not valid JSON" -ForegroundColor Red
        $testsFailed++
        $tests += @{ Name = "API Response Format"; Status = "FAILED"; Error = $_.Exception.Message }
    }
} else {
    Write-Host "  ✗ Cannot test API response format" -ForegroundColor Red
    $testsFailed++
    $tests += @{ Name = "API Response Format"; Status = "FAILED"; Error = $result.Error }
}
Write-Host ""

# ============================================================================
# Summary
# ============================================================================

Write-Host "========================================" -ForegroundColor $(if ($testsFailed -eq 0) { "Green" } else { "Red" })
Write-Host "Smoke Test Summary" -ForegroundColor $(if ($testsFailed -eq 0) { "Green" } else { "Red" })
Write-Host "========================================" -ForegroundColor $(if ($testsFailed -eq 0) { "Green" } else { "Red" })
Write-Host ""

foreach ($test in $tests) {
    $statusColor = switch ($test.Status) {
        "PASSED" { "Green" }
        "FAILED" { "Red" }
        "WARNING" { "Yellow" }
        default { "Gray" }
    }
    
    Write-Host "  $($test.Status): $($test.Name)" -ForegroundColor $statusColor
    if ($test.Error) {
        Write-Host "    Error: $($test.Error)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Total: $($tests.Count) tests" -ForegroundColor White
Write-Host "Passed: $testsPassed" -ForegroundColor Green
Write-Host "Failed: $testsFailed" -ForegroundColor $(if ($testsFailed -eq 0) { "Gray" } else { "Red" })
Write-Host ""

if ($testsFailed -eq 0) {
    Write-Host "✓ All critical smoke tests passed" -ForegroundColor Green
    exit 0
} else {
    Write-Host "✗ Some smoke tests failed" -ForegroundColor Red
    exit 1
}

