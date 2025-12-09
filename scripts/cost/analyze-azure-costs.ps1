<#
.SYNOPSIS
Analyzes Azure resource costs and provides optimization recommendations.

.DESCRIPTION
Analyzes Azure resources and provides cost optimization recommendations.

.PARAMETER ResourceGroup
Azure Resource Group name (optional, analyzes all if not specified).

.PARAMETER SubscriptionId
Azure Subscription ID (optional, uses default if not specified).

.PARAMETER OutputFile
Output file for the cost analysis report.

.EXAMPLE
.\analyze-azure-costs.ps1 -ResourceGroup "nl-prod-codeflow-rg-san" -OutputFile "cost-analysis.json"
#>

[CmdletBinding()]
param(
    [string]$ResourceGroup = "",
    
    [string]$SubscriptionId = "",
    
    [string]$OutputFile = "cost-analysis.json"
)

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Azure Cost Analysis" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Validate Azure CLI
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "✗ Azure CLI is not installed" -ForegroundColor Red
    exit 1
}

# Set subscription if provided
if (-not [string]::IsNullOrEmpty($SubscriptionId)) {
    Write-Host "Setting subscription to: $SubscriptionId" -ForegroundColor Yellow
    az account set --subscription $SubscriptionId
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to set subscription" -ForegroundColor Red
        exit 1
    }
}

# ============================================================================
# Analyze Resources
# ============================================================================

Write-Host "Analyzing Azure resources..." -ForegroundColor Yellow

$resources = @()

if ([string]::IsNullOrEmpty($ResourceGroup)) {
    Write-Host "  Analyzing all resource groups..." -ForegroundColor Gray
    $resourceGroups = az group list --query "[].name" --output tsv 2>$null
    
    if ($resourceGroups) {
        foreach ($rg in $resourceGroups) {
            Write-Host "    Analyzing resource group: $rg" -ForegroundColor Gray
            $rgResources = az resource list --resource-group $rg --query "[].{Name:name, Type:type, Location:location}" --output json 2>$null | ConvertFrom-Json
            
            foreach ($resource in $rgResources) {
                $resources += @{
                    ResourceGroup = $rg
                    Name = $resource.Name
                    Type = $resource.Type
                    Location = $resource.Location
                }
            }
        }
    }
} else {
    Write-Host "  Analyzing resource group: $ResourceGroup" -ForegroundColor Gray
    $rgResources = az resource list --resource-group $ResourceGroup --query "[].{Name:name, Type:type, Location:location}" --output json 2>$null | ConvertFrom-Json
    
    foreach ($resource in $rgResources) {
        $resources += @{
            ResourceGroup = $ResourceGroup
            Name = $resource.Name
            Type = $resource.Type
            Location = $resource.Location
        }
    }
}

Write-Host "  ✓ Found $($resources.Count) resources" -ForegroundColor Green
Write-Host ""

# ============================================================================
# Categorize Resources
# ============================================================================

Write-Host "Categorizing resources..." -ForegroundColor Yellow

$resourceCategories = @{
    Compute = @()
    Database = @()
    Storage = @()
    Network = @()
    Monitoring = @()
    Other = @()
}

foreach ($resource in $resources) {
    $type = $resource.Type
    
    if ($type -match "ContainerApps|ContainerService|VirtualMachine|AppService") {
        $resourceCategories.Compute += $resource
    } elseif ($type -match "PostgreSQL|MySQL|CosmosDB|Database") {
        $resourceCategories.Database += $resource
    } elseif ($type -match "Storage|StorageAccount|Blob") {
        $resourceCategories.Storage += $resource
    } elseif ($type -match "Network|LoadBalancer|ApplicationGateway|VirtualNetwork") {
        $resourceCategories.Network += $resource
    } elseif ($type -match "LogAnalytics|ApplicationInsights|Monitor") {
        $resourceCategories.Monitoring += $resource
    } else {
        $resourceCategories.Other += $resource
    }
}

Write-Host "  ✓ Categorized resources" -ForegroundColor Green
Write-Host ""

# ============================================================================
# Generate Recommendations
# ============================================================================

Write-Host "Generating cost optimization recommendations..." -ForegroundColor Yellow

$recommendations = @()

# Check for unused resources
$unusedThreshold = (Get-Date).AddDays(-30)
$recommendations += "Review resources unused for 30+ days"

# Check for over-provisioned resources
if ($resourceCategories.Compute.Count -gt 0) {
    $recommendations += "Review compute resource sizing - consider right-sizing"
    $recommendations += "Consider auto-scaling for compute resources"
}

# Check for database resources
if ($resourceCategories.Database.Count -gt 0) {
    $recommendations += "Review database tier and sizing"
    $recommendations += "Consider reserved capacity for production databases"
    $recommendations += "Review database backup retention policies"
}

# Check for storage resources
if ($resourceCategories.Storage.Count -gt 0) {
    $recommendations += "Review storage tier (hot/cool/archive)"
    $recommendations += "Implement data lifecycle management"
    $recommendations += "Review and delete unused storage accounts"
}

# Check for monitoring resources
if ($resourceCategories.Monitoring.Count -gt 0) {
    $recommendations += "Review log retention policies"
    $recommendations += "Optimize log queries to reduce data ingestion"
}

# General recommendations
$recommendations += "Use Azure Cost Management to track spending"
$recommendations += "Set up budget alerts"
$recommendations += "Review and apply Azure reservations where applicable"
$recommendations += "Consider spot instances for non-critical workloads"

Write-Host "  ✓ Generated $($recommendations.Count) recommendations" -ForegroundColor Green
Write-Host ""

# ============================================================================
# Generate Report
# ============================================================================

$report = @{
    AnalyzedAt = (Get-Date -Format "o")
    SubscriptionId = if ([string]::IsNullOrEmpty($SubscriptionId)) { (az account show --query id -o tsv) } else { $SubscriptionId }
    ResourceGroup = if ([string]::IsNullOrEmpty($ResourceGroup)) { "All" } else { $ResourceGroup }
    Summary = @{
        TotalResources = $resources.Count
        Compute = $resourceCategories.Compute.Count
        Database = $resourceCategories.Database.Count
        Storage = $resourceCategories.Storage.Count
        Network = $resourceCategories.Network.Count
        Monitoring = $resourceCategories.Monitoring.Count
        Other = $resourceCategories.Other.Count
    }
    Resources = $resources
    ResourceCategories = @{
        Compute = $resourceCategories.Compute
        Database = $resourceCategories.Database
        Storage = $resourceCategories.Storage
        Network = $resourceCategories.Network
        Monitoring = $resourceCategories.Monitoring
        Other = $resourceCategories.Other
    }
    Recommendations = $recommendations
}

$reportJson = $report | ConvertTo-Json -Depth 10
$reportJson | Out-File -FilePath $OutputFile -Encoding utf8

# ============================================================================
# Display Summary
# ============================================================================

Write-Host "========================================" -ForegroundColor Green
Write-Host "Cost Analysis Complete" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Report saved to: $OutputFile" -ForegroundColor White
Write-Host ""
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  Total Resources: $($resources.Count)" -ForegroundColor White
Write-Host "  Compute: $($resourceCategories.Compute.Count)" -ForegroundColor White
Write-Host "  Database: $($resourceCategories.Database.Count)" -ForegroundColor White
Write-Host "  Storage: $($resourceCategories.Storage.Count)" -ForegroundColor White
Write-Host "  Network: $($resourceCategories.Network.Count)" -ForegroundColor White
Write-Host "  Monitoring: $($resourceCategories.Monitoring.Count)" -ForegroundColor White
Write-Host "  Other: $($resourceCategories.Other.Count)" -ForegroundColor White
Write-Host ""
Write-Host "Top Recommendations:" -ForegroundColor Yellow
foreach ($rec in $recommendations[0..4]) {
    Write-Host "  • $rec" -ForegroundColor Gray
}
Write-Host ""

