<#
.SYNOPSIS
Creates alert rules for CodeFlow Engine monitoring.

.DESCRIPTION
Creates common alert rules for Application Insights metrics.

.PARAMETER ResourceGroup
Azure Resource Group name.

.PARAMETER AppInsightsName
Application Insights name.

.PARAMETER ActionGroupName
Action Group name for notifications.

.EXAMPLE
.\create-alert-rules.ps1 -ResourceGroup "nl-prod-codeflow-rg-san" -AppInsightsName "codeflow-engine-insights"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,
    
    [Parameter(Mandatory = $true)]
    [string]$AppInsightsName,
    
    [string]$ActionGroupName = "codeflow-engine-alerts"
)

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Creating Alert Rules" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Validate Azure CLI
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "✗ Azure CLI is not installed" -ForegroundColor Red
    exit 1
}

# Get Application Insights resource ID
$appInsightsId = az monitor app-insights component show `
    --app $AppInsightsName `
    --resource-group $ResourceGroup `
    --query "id" `
    --output tsv

if (-not $appInsightsId) {
    Write-Host "✗ Application Insights not found: $AppInsightsName" -ForegroundColor Red
    exit 1
}

# Get Action Group resource ID
$actionGroupId = az monitor action-group show `
    --name $ActionGroupName `
    --resource-group $ResourceGroup `
    --query "id" `
    --output tsv

if (-not $actionGroupId) {
    Write-Host "⚠ Action Group not found: $ActionGroupName" -ForegroundColor Yellow
    Write-Host "  Creating alert rules without action group..." -ForegroundColor Gray
}

# ============================================================================
# Alert Rule Definitions
# ============================================================================

$alertRules = @(
    @{
        Name = "codeflow-engine-high-error-rate"
        DisplayName = "High Error Rate"
        Description = "Alert when error rate exceeds 5%"
        Metric = "requests/failed"
        Threshold = 0.05
        Aggregation = "count"
        Window = "PT5M"
    },
    @{
        Name = "codeflow-engine-high-response-time"
        DisplayName = "High Response Time"
        Description = "Alert when average response time exceeds 2 seconds"
        Metric = "requests/duration"
        Threshold = 2000
        Aggregation = "avg"
        Window = "PT5M"
    },
    @{
        Name = "codeflow-engine-server-exceptions"
        DisplayName = "Server Exceptions"
        Description = "Alert when server exceptions occur"
        Metric = "exceptions/server"
        Threshold = 1
        Aggregation = "count"
        Window = "PT5M"
    },
    @{
        Name = "codeflow-engine-availability-low"
        DisplayName = "Low Availability"
        Description = "Alert when availability drops below 99%"
        Metric = "availabilityResults/availabilityPercentage"
        Threshold = 99
        Aggregation = "avg"
        Window = "PT15M"
        Operator = "LessThan"
    }
)

# ============================================================================
# Create Alert Rules
# ============================================================================

$created = 0
$skipped = 0

foreach ($rule in $alertRules) {
    Write-Host "Creating alert: $($rule.DisplayName)..." -ForegroundColor Yellow
    
    # Check if rule already exists
    $existing = az monitor metrics alert show `
        --name $rule.Name `
        --resource-group $ResourceGroup `
        --query "name" `
        --output tsv 2>$null
    
    if ($existing) {
        Write-Host "  ⚠ Alert rule already exists, skipping" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    # Build condition
    $operator = if ($rule.Operator) { $rule.Operator } else { "GreaterThan" }
    
    # Create alert rule
    $alertParams = @{
        name = $rule.Name
        resource-group = $ResourceGroup
        scopes = $appInsightsId
        condition = "avg $($rule.Metric) $operator $($rule.Threshold)"
        window-size = $rule.Window
        evaluation-frequency = "PT1M"
        description = $rule.Description
    }
    
    if ($actionGroupId) {
        $alertParams["action"] = $actionGroupId
    }
    
    try {
        az monitor metrics alert create @alertParams --output none 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Alert rule created" -ForegroundColor Green
            $created++
        } else {
            Write-Host "  ✗ Failed to create alert rule" -ForegroundColor Red
        }
    } catch {
        Write-Host "  ✗ Error: $_" -ForegroundColor Red
    }
    
    Write-Host ""
}

# ============================================================================
# Summary
# ============================================================================

Write-Host "========================================" -ForegroundColor Green
Write-Host "Alert Rules Summary" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Created: $created" -ForegroundColor Green
Write-Host "Skipped: $skipped" -ForegroundColor Yellow
Write-Host "Total: $($alertRules.Count)" -ForegroundColor White
Write-Host ""
Write-Host "Note: Alert rules may need manual configuration in Azure Portal" -ForegroundColor Yellow
Write-Host "      for complex conditions and multiple action groups." -ForegroundColor Gray
Write-Host ""

