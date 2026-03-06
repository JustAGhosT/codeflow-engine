<#
.SYNOPSIS
Sets up Azure monitoring for CodeFlow Engine.

.DESCRIPTION
Configures Application Insights, Log Analytics, and alerting for CodeFlow.

.PARAMETER ResourceGroup
Azure Resource Group name.

.PARAMETER Location
Azure location. Default: southafricanorth

.PARAMETER AppName
Application name. Default: codeflow-engine

.EXAMPLE
.\setup-azure-monitoring.ps1 -ResourceGroup "nl-prod-codeflow-rg-san" -AppName "codeflow-engine"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,
    
    [string]$Location = "southafricanorth",
    
    [string]$AppName = "codeflow-engine"
)

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Azure Monitoring Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Validate Azure CLI
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "✗ Azure CLI is not installed" -ForegroundColor Red
    exit 1
}

# ============================================================================
# Create Application Insights
# ============================================================================

Write-Host "Creating Application Insights..." -ForegroundColor Yellow

$appInsightsName = "$AppName-insights"
$appInsightsExists = az monitor app-insights component show `
    --app $appInsightsName `
    --resource-group $ResourceGroup `
    --query "name" `
    --output tsv 2>$null

if ($appInsightsExists) {
    Write-Host "  ✓ Application Insights already exists" -ForegroundColor Green
    $appInsightsId = az monitor app-insights component show `
        --app $appInsightsName `
        --resource-group $ResourceGroup `
        --query "appId" `
        --output tsv
    $instrumentationKey = az monitor app-insights component show `
        --app $appInsightsName `
        --resource-group $ResourceGroup `
        --query "instrumentationKey" `
        --output tsv
} else {
    Write-Host "  Creating Application Insights..." -ForegroundColor Gray
    $appInsights = az monitor app-insights component create `
        --app $appInsightsName `
        --location $Location `
        --resource-group $ResourceGroup `
        --application-type web `
        --output json 2>&1 | ConvertFrom-Json
    
    if ($LASTEXITCODE -eq 0) {
        $appInsightsId = $appInsights.appId
        $instrumentationKey = $appInsights.instrumentationKey
        Write-Host "  ✓ Application Insights created" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to create Application Insights" -ForegroundColor Red
        exit 1
    }
}

Write-Host "  Application Insights ID: $appInsightsId" -ForegroundColor Gray
Write-Host "  Instrumentation Key: $instrumentationKey" -ForegroundColor Gray
Write-Host ""

# ============================================================================
# Create Log Analytics Workspace
# ============================================================================

Write-Host "Creating Log Analytics Workspace..." -ForegroundColor Yellow

$workspaceName = "$AppName-logs"
$workspaceExists = az monitor log-analytics workspace show `
    --workspace-name $workspaceName `
    --resource-group $ResourceGroup `
    --query "name" `
    --output tsv 2>$null

if ($workspaceExists) {
    Write-Host "  ✓ Log Analytics Workspace already exists" -ForegroundColor Green
    $workspaceId = az monitor log-analytics workspace show `
        --workspace-name $workspaceName `
        --resource-group $ResourceGroup `
        --query "customerId" `
        --output tsv
    $workspaceKey = az monitor log-analytics workspace get-shared-keys `
        --workspace-name $workspaceName `
        --resource-group $ResourceGroup `
        --query "primarySharedKey" `
        --output tsv
} else {
    Write-Host "  Creating Log Analytics Workspace..." -ForegroundColor Gray
    $workspace = az monitor log-analytics workspace create `
        --workspace-name $workspaceName `
        --location $Location `
        --resource-group $ResourceGroup `
        --output json 2>&1 | ConvertFrom-Json
    
    if ($LASTEXITCODE -eq 0) {
        $workspaceId = $workspace.customerId
        $workspaceKey = az monitor log-analytics workspace get-shared-keys `
            --workspace-name $workspaceName `
            --resource-group $ResourceGroup `
            --query "primarySharedKey" `
            --output tsv
        Write-Host "  ✓ Log Analytics Workspace created" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to create Log Analytics Workspace" -ForegroundColor Red
        exit 1
    }
}

Write-Host "  Workspace ID: $workspaceId" -ForegroundColor Gray
Write-Host ""

# ============================================================================
# Create Action Group for Alerts
# ============================================================================

Write-Host "Creating Action Group for alerts..." -ForegroundColor Yellow

$actionGroupName = "$AppName-alerts"
$actionGroupExists = az monitor action-group show `
    --name $actionGroupName `
    --resource-group $ResourceGroup `
    --query "name" `
    --output tsv 2>$null

if ($actionGroupExists) {
    Write-Host "  ✓ Action Group already exists" -ForegroundColor Green
} else {
    Write-Host "  Creating Action Group..." -ForegroundColor Gray
    Write-Host "  ⚠ Action Group requires email. Update manually in Azure Portal." -ForegroundColor Yellow
    Write-Host "  Action Group name: $actionGroupName" -ForegroundColor Gray
}

Write-Host ""

# ============================================================================
# Display Configuration
# ============================================================================

Write-Host "========================================" -ForegroundColor Green
Write-Host "Monitoring Setup Complete" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Application Insights:" -ForegroundColor White
Write-Host "    Name: $appInsightsName" -ForegroundColor Gray
Write-Host "    ID: $appInsightsId" -ForegroundColor Gray
Write-Host "    Instrumentation Key: $instrumentationKey" -ForegroundColor Gray
Write-Host ""
Write-Host "  Log Analytics:" -ForegroundColor White
Write-Host "    Name: $workspaceName" -ForegroundColor Gray
Write-Host "    Workspace ID: $workspaceId" -ForegroundColor Gray
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Add instrumentation key to application settings:" -ForegroundColor White
Write-Host "   APPINSIGHTS_INSTRUMENTATIONKEY=$instrumentationKey" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Add Log Analytics configuration:" -ForegroundColor White
Write-Host "   LOG_ANALYTICS_WORKSPACE_ID=$workspaceId" -ForegroundColor Gray
Write-Host "   LOG_ANALYTICS_WORKSPACE_KEY=$workspaceKey" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Configure alert rules in Azure Portal" -ForegroundColor White
Write-Host "4. Set up action groups with email/SMS notifications" -ForegroundColor White
Write-Host ""

