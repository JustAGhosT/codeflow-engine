<#
.SYNOPSIS
Creates a full Azure environment for a new repo using az CLI.

.DESCRIPTION
Creates everything from New-AzRepoEnvironment.ps1 plus:
- App Service plan (Linux)
- Web App for the UI
- Container App Environment
- Container App for the engine
- User-assigned managed identity
- Assigns identity to Web App + Container App
- Optionally grants Key Vault roles to the identity

Naming convention: org-env-project-type-region
Example: nl-dev-codeflow-rg-san

.PARAMETER OrgCode
Short org code (e.g. nl, tws, mys).

.PARAMETER Environment
Environment name (dev, test, uat, prod).

.PARAMETER Project
Project/repo name (e.g. codeflow).

.PARAMETER RegionShort
Short region code used in names (e.g. san, euw, wus).

.PARAMETER Location
Azure location (e.g. southafricanorth, westeurope).

.PARAMETER SubscriptionId
Azure subscription GUID.

.PARAMETER UiRuntime
Runtime stack for the Web App (e.g., "NODE:20-lts", "PYTHON:3.11").

.PARAMETER EngineImage
Container image for the engine Container App (e.g., "ghcr.io/justaghost/codeflow-engine:latest").

.PARAMETER CreateKeyVault
Switch to also create a Key Vault and grant the managed identity access to it.

.PARAMETER OutputJsonPath
Optional path to write the JSON summary. If omitted, JSON is written to ./az-environment-summary.json in the current directory.

.EXAMPLE
.\New-AzRepoFullEnvironment.ps1 -OrgCode nl -Environment dev -Project codeflow -RegionShort san -Location southafricanorth -SubscriptionId 00000000-0000-0000-0000-000000000000 -UiRuntime "NODE:20-lts" -EngineImage "ghcr.io/justaghost/codeflow-engine:latest" -CreateKeyVault
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$OrgCode,

    [Parameter(Mandatory = $true)]
    [ValidateSet('dev', 'test', 'uat', 'prod')]
    [string]$Environment,

    [Parameter(Mandatory = $true)]
    [string]$Project,

    [Parameter(Mandatory = $true)]
    [string]$RegionShort,

    [Parameter(Mandatory = $true)]
    [string]$Location,

    [Parameter(Mandatory = $true)]
    [string]$SubscriptionId,

    [Parameter(Mandatory = $true)]
    [string]$UiRuntime,

    [Parameter(Mandatory = $true)]
    [string]$EngineImage,

    [switch]$CreateKeyVault,

    [string]$OutputJsonPath = "./az-environment-summary.json"
)

function Write-Section {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message
    )
    Write-Host ""
    Write-Host "=== $Message ===" -ForegroundColor Cyan
}

function Get-SafeName {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Base,
        [int]$MaxLength = 24,
        [switch]$LowercaseOnly
    )

    $clean = ($Base -replace '[^a-zA-Z0-9]', '')
    if ($LowercaseOnly) {
        $clean = $clean.ToLowerInvariant()
    }

    if ($clean.Length -gt $MaxLength) {
        $clean = $clean.Substring(0, $MaxLength)
    }

    if ([string]::IsNullOrWhiteSpace($clean)) {
        throw "Cannot generate safe name from '$Base'."
    }

    return $clean
}

Write-Section "Setting Azure subscription"
az account set --subscription $SubscriptionId | Out-Null

Write-Section "Building resource names (org-env-project-type-region)"

$rgName = "$OrgCode-$Environment-$Project-rg-$RegionShort"
$stRaw = "st$OrgCode$Environment$Project$RegionShort"
$stName = Get-SafeName -Base $stRaw -MaxLength 24 -LowercaseOnly

$lawName = "$OrgCode-$Environment-$Project-law-$RegionShort"
$aiName = "$OrgCode-$Environment-$Project-ai-$RegionShort"

$aspName = "$OrgCode-$Environment-$Project-asp-$RegionShort"
$webAppRaw = "$OrgCode-$Environment-$Project-ui-$RegionShort"
$webAppName = Get-SafeName -Base $webAppRaw -MaxLength 60 -LowercaseOnly

$caeName = "$OrgCode-$Environment-$Project-cae-$RegionShort"
$caRaw = "$OrgCode-$Environment-$Project-engine-$RegionShort"
$caName = Get-SafeName -Base $caRaw -MaxLength 32 -LowercaseOnly

$identityName = "$OrgCode-$Environment-$Project-identity-$RegionShort"

if ($CreateKeyVault) {
    $kvRaw = "kv-$OrgCode-$Environment-$Project-$RegionShort"
    $kvName = Get-SafeName -Base $kvRaw -MaxLength 24 -LowercaseOnly
}

Write-Host "Resource group: $rgName"
Write-Host "Storage account: $stName"
Write-Host "Log Analytics: $lawName"
Write-Host "App Insights: $aiName"
Write-Host "App Service Plan: $aspName"
Write-Host "Web App: $webAppName"
Write-Host "Container App Environment: $caeName"
Write-Host "Container App: $caName"
Write-Host "Managed Identity: $identityName"
if ($CreateKeyVault) {
    Write-Host "Key Vault: $kvName"
}

Write-Section "Creating resource group"
az group create --name $rgName --location $Location `
    --output table

Write-Section "Creating storage account"
az storage account create --name $stName --resource-group $rgName --location $Location --sku Standard_LRS --kind StorageV2 --min-tls-version TLS1_2 --https-only true --allow-blob-public-access false `
    --output table

Write-Section "Creating Log Analytics workspace"
az monitor log-analytics workspace create --resource-group $rgName --workspace-name $lawName --location $Location --sku PerGB2018 `
    --output table

$lawId = az monitor log-analytics workspace show --resource-group $rgName --workspace-name $lawName --query id --output tsv

Write-Section "Creating Application Insights (connected to workspace)"
az monitor app-insights component create --app $aiName --location $Location --resource-group $rgName --workspace $lawId --application-type web --output table

if ($CreateKeyVault) {
    Write-Section "Creating Key Vault"
    az keyvault create --name $kvName --resource-group $rgName --location $Location --enable-rbac-authorization true `
        --output table
}

Write-Section "Creating user-assigned managed identity"
$identityId = az identity create --name $identityName --resource-group $rgName --location $Location --query id --output tsv
$identityPrincipalId = az identity show --name $identityName --resource-group $rgName --query principalId --output tsv

Write-Host "Identity created: $identityId" -ForegroundColor Green
Write-Host "Principal ID: $identityPrincipalId" -ForegroundColor Green

Write-Section "Creating App Service Plan (Linux)"
az appservice plan create --name $aspName --resource-group $rgName --location $Location --is-linux --sku B1 `
    --output table

Write-Section "Creating Web App"
az webapp create --name $webAppName --resource-group $rgName --plan $aspName --runtime $UiRuntime `
    --output table

Write-Section "Assigning managed identity to Web App"
az webapp identity assign --name $webAppName --resource-group $rgName --identities $identityId `
    --output table

Write-Section "Creating Container App Environment"
az containerapp env create --name $caeName --resource-group $rgName --location $Location `
    --output table

Write-Section "Creating Container App"
az containerapp create --name $caName --resource-group $rgName --environment $caeName `
    --image $EngineImage --target-port 8000 --ingress external --min-replicas 1 --max-replicas 3 `
    --output table

Write-Section "Assigning managed identity to Container App"
az containerapp identity assign --name $caName --resource-group $rgName --system-assigned false --user-assigned $identityId `
    --output table

if ($CreateKeyVault) {
    Write-Section "Granting Key Vault access to managed identity"
    $subscriptionId = az account show --query id --output tsv
    $kvScope = "/subscriptions/$subscriptionId/resourceGroups/$rgName/providers/Microsoft.KeyVault/vaults/$kvName"
    
    az role assignment create --assignee $identityPrincipalId --role "Key Vault Secrets User" --scope $kvScope `
        --output table
    Write-Host "✓ Key Vault access granted" -ForegroundColor Green
}

Write-Section "Fetching connection details"

$stConn = az storage account show-connection-string --name $stName --resource-group $rgName --query connectionString --output tsv

$lawKey = az monitor log-analytics workspace get-shared-keys --resource-group $rgName --workspace-name $lawName --query primarySharedKey --output tsv

$aiKey = az monitor app-insights component show --app $aiName --resource-group $rgName --query instrumentationKey --output tsv

$webAppUrl = az webapp show --name $webAppName --resource-group $rgName --query defaultHostName --output tsv

$caUrl = az containerapp show --name $caName --resource-group $rgName --query properties.configuration.ingress.fqdn --output tsv

Write-Section "Summary (for GitHub/Azure DevOps secrets)"

$summary = [PSCustomObject]@{
    SubscriptionId             = $SubscriptionId
    OrgCode                    = $OrgCode
    Environment                = $Environment
    Project                    = $Project
    RegionShort                = $RegionShort
    Location                   = $Location
    ResourceGroup              = $rgName
    StorageAccountName         = $stName
    StorageConnectionString    = $stConn
    LogAnalyticsWorkspace      = $lawName
    LogAnalyticsWorkspaceId    = $lawId
    LogAnalyticsKey            = $lawKey
    AppInsightsName            = $aiName
    AppInsightsKey             = $aiKey
    AppServicePlanName         = $aspName
    WebAppName                 = $webAppName
    WebAppUrl                  = "https://$webAppUrl"
    ContainerAppEnvName        = $caeName
    ContainerAppName           = $caName
    ContainerAppUrl            = "https://$caUrl"
    ManagedIdentityName        = $identityName
    ManagedIdentityId          = $identityId
    ManagedIdentityPrincipalId = $identityPrincipalId
}

if ($CreateKeyVault) {
    $summary | Add-Member -NotePropertyName "KeyVaultName" -NotePropertyValue $kvName
}

$summary | Format-List

$summaryJson = $summary | ConvertTo-Json -Depth 3

Write-Section "Writing JSON summary to $OutputJsonPath"
$OutputJsonPath = [System.IO.Path]::GetFullPath($OutputJsonPath)
$summaryJson | Out-File -FilePath $OutputJsonPath -Encoding utf8

Write-Host ""
Write-Host "JSON summary written to: $OutputJsonPath" -ForegroundColor Green
Write-Host ""
Write-Host $summaryJson

