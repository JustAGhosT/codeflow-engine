<#
.SYNOPSIS
Creates GitHub repository secrets from an Azure environment JSON file.

.DESCRIPTION
Takes the JSON summary emitted by New-AzRepoEnvironment.ps1 and creates GitHub Actions repo secrets using the GitHub CLI (gh).

You must be authenticated with gh (gh auth login) and have access to the target repository.

.PARAMETER JsonPath
Path to the JSON file emitted by New-AzRepoEnvironment.ps1.

.PARAMETER Repo
GitHub repository in format "owner/repo" (e.g., "JustAGHosT/codeflow-engine").

.PARAMETER Prefix
Optional prefix for secret names (e.g., "DEV_", "PROD_"). If omitted, no prefix is used.

.EXAMPLE
.\Set-GitHubSecretsFromJson.ps1 -JsonPath ./az-env-dev-codeflow.json -Repo JustAGHosT/codeflow-engine -Prefix DEV_
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$JsonPath,

    [Parameter(Mandatory = $true)]
    [string]$Repo,

    [string]$Prefix = ""
)

function Write-Section {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message
    )
    Write-Host ""
    Write-Host "=== $Message ===" -ForegroundColor Cyan
}

function Test-GitHubCLI {
    try {
        $null = gh --version
        return $true
    }
    catch {
        return $false
    }
}

function Set-GitHubSecret {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        [Parameter(Mandatory = $true)]
        [string]$Value,
        [Parameter(Mandatory = $true)]
        [string]$Repository
    )

    Write-Host "Setting secret: $Name" -ForegroundColor Yellow
    $secretName = if ($Prefix) { "${Prefix}$Name" } else { $Name }
    
    $value | gh secret set $secretName --repo $Repository
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Secret '$secretName' set successfully" -ForegroundColor Green
    }
    else {
        Write-Host "  ✗ Failed to set secret '$secretName'" -ForegroundColor Red
        return $false
    }
    return $true
}

Write-Section "Checking prerequisites"

if (-not (Test-GitHubCLI)) {
    Write-Host "Error: GitHub CLI (gh) is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Install it from: https://cli.github.com/" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ GitHub CLI found" -ForegroundColor Green

if (-not (Test-Path $JsonPath)) {
    Write-Host "Error: JSON file not found: $JsonPath" -ForegroundColor Red
    exit 1
}

Write-Host "✓ JSON file found: $JsonPath" -ForegroundColor Green

Write-Section "Reading JSON summary"
$jsonContent = Get-Content -Path $JsonPath -Raw | ConvertFrom-Json

Write-Section "Setting GitHub repository secrets"

$secrets = @{
    "AZURE_SUBSCRIPTION_ID"        = $jsonContent.SubscriptionId
    "AZURE_RESOURCE_GROUP"         = $jsonContent.ResourceGroup
    "AZURE_LOCATION"               = $jsonContent.Location
    "AZURE_STORAGE_ACCOUNT"        = $jsonContent.StorageAccountName
    "AZURE_STORAGE_CONNECTION"     = $jsonContent.StorageConnectionString
    "AZURE_LOG_ANALYTICS_WORKSPACE" = $jsonContent.LogAnalyticsWorkspace
    "AZURE_LOG_ANALYTICS_WORKSPACE_ID" = $jsonContent.LogAnalyticsWorkspaceId
    "AZURE_LOG_ANALYTICS_KEY"      = $jsonContent.LogAnalyticsKey
    "AZURE_APPINSIGHTS_NAME"       = $jsonContent.AppInsightsName
    "AZURE_APPINSIGHTS_KEY"        = $jsonContent.AppInsightsKey
}

if ($jsonContent.PSObject.Properties.Name -contains "KeyVaultName") {
    $secrets["AZURE_KEYVAULT_NAME"] = $jsonContent.KeyVaultName
}

$successCount = 0
$failCount = 0

foreach ($secret in $secrets.GetEnumerator()) {
    if (Set-GitHubSecret -Name $secret.Key -Value $secret.Value -Repository $Repo) {
        $successCount++
    }
    else {
        $failCount++
    }
}

Write-Section "Summary"
Write-Host "Successfully set: $successCount secrets" -ForegroundColor Green
if ($failCount -gt 0) {
    Write-Host "Failed to set: $failCount secrets" -ForegroundColor Red
}

Write-Host ""
Write-Host "Secrets created with prefix: $(if ($Prefix) { $Prefix } else { '(none)' })" -ForegroundColor Cyan
Write-Host "Repository: $Repo" -ForegroundColor Cyan

