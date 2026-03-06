<#
.SYNOPSIS
Identifies potentially unused Azure resources.

.DESCRIPTION
Analyzes Azure resources to identify potentially unused or underutilized resources.

.PARAMETER ResourceGroup
Azure Resource Group name (optional).

.PARAMETER DaysUnused
Number of days to consider a resource unused. Default: 30

.EXAMPLE
.\identify-unused-resources.ps1 -ResourceGroup "nl-dev-codeflow-rg-san" -DaysUnused 30
#>

[CmdletBinding()]
param(
    [string]$ResourceGroup = "",
    
    [int]$DaysUnused = 30
)

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Unused Resource Identification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Validate Azure CLI
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "✗ Azure CLI is not installed" -ForegroundColor Red
    exit 1
}

# ============================================================================
# Identify Unused Resources
# ============================================================================

Write-Host "Identifying unused resources..." -ForegroundColor Yellow

$unusedResources = @()
$cutoffDate = (Get-Date).AddDays(-$DaysUnused)

if ([string]::IsNullOrEmpty($ResourceGroup)) {
    $resourceGroups = az group list --query "[].name" --output tsv 2>$null
    
    if ($resourceGroups) {
        foreach ($rg in $resourceGroups) {
            Write-Host "  Checking resource group: $rg" -ForegroundColor Gray
            
            # Get resources
            $resources = az resource list --resource-group $rg --query "[].{Name:name, Type:type, Location:location}" --output json 2>$null | ConvertFrom-Json
            
            foreach ($resource in $resources) {
                # Check for activity (simplified - would need actual usage metrics)
                $resourceInfo = @{
                    ResourceGroup = $rg
                    Name = $resource.Name
                    Type = $resource.Type
                    Location = $resource.Location
                    Status = "Unknown"
                    Recommendation = "Review resource usage"
                }
                
                # Check for common unused resource patterns
                if ($resource.Name -match "test|demo|temp|old|backup") {
                    $resourceInfo.Status = "Potentially Unused"
                    $resourceInfo.Recommendation = "Review and delete if not needed"
                    $unusedResources += $resourceInfo
                }
            }
        }
    }
} else {
    Write-Host "  Checking resource group: $ResourceGroup" -ForegroundColor Gray
    
    $resources = az resource list --resource-group $ResourceGroup --query "[].{Name:name, Type:type, Location:location}" --output json 2>$null | ConvertFrom-Json
    
    foreach ($resource in $resources) {
        $resourceInfo = @{
            ResourceGroup = $ResourceGroup
            Name = $resource.Name
            Type = $resource.Type
            Location = $resource.Location
            Status = "Unknown"
            Recommendation = "Review resource usage"
        }
        
        if ($resource.Name -match "test|demo|temp|old|backup") {
            $resourceInfo.Status = "Potentially Unused"
            $resourceInfo.Recommendation = "Review and delete if not needed"
            $unusedResources += $resourceInfo
        }
    }
}

Write-Host "  ✓ Analysis complete" -ForegroundColor Green
Write-Host ""

# ============================================================================
# Display Results
# ============================================================================

Write-Host "========================================" -ForegroundColor $(if ($unusedResources.Count -eq 0) { "Green" } else { "Yellow" })
Write-Host "Unused Resource Analysis" -ForegroundColor $(if ($unusedResources.Count -eq 0) { "Green" } else { "Yellow" })
Write-Host "========================================" -ForegroundColor $(if ($unusedResources.Count -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

if ($unusedResources.Count -eq 0) {
    Write-Host "✓ No obviously unused resources found" -ForegroundColor Green
    Write-Host ""
    Write-Host "Note: This is a basic analysis. For comprehensive analysis:" -ForegroundColor Yellow
    Write-Host "  - Review Azure Cost Management usage reports" -ForegroundColor Gray
    Write-Host "  - Check resource metrics and activity logs" -ForegroundColor Gray
    Write-Host "  - Review resource tags and naming conventions" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "Found $($unusedResources.Count) potentially unused resources:" -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($resource in $unusedResources) {
        Write-Host "Resource: $($resource.Name)" -ForegroundColor White
        Write-Host "  Type: $($resource.Type)" -ForegroundColor Gray
        Write-Host "  Resource Group: $($resource.ResourceGroup)" -ForegroundColor Gray
        Write-Host "  Status: $($resource.Status)" -ForegroundColor Yellow
        Write-Host "  Recommendation: $($resource.Recommendation)" -ForegroundColor Cyan
        Write-Host ""
    }
    
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Review each resource manually" -ForegroundColor Gray
    Write-Host "  2. Check resource usage metrics" -ForegroundColor Gray
    Write-Host "  3. Verify resource is not needed" -ForegroundColor Gray
    Write-Host "  4. Delete unused resources to reduce costs" -ForegroundColor Gray
    Write-Host ""
}

