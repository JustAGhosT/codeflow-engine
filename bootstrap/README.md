# CodeFlow AI – Azure Setup Scripts

This package contains az CLI–only PowerShell scripts to bootstrap new repositories into Azure using your org-env-project-type-region naming convention.

## 📁 Scripts

### 1. `New-AzRepoEnvironment.ps1`

Creates core infrastructure for a repo:
- Resource group
- Storage account
- Log Analytics workspace
- Application Insights (linked to the workspace)
- Optional Key Vault

Emits a JSON summary file you can feed into other tooling.

**Example:**

```powershell
.\scripts\New-AzRepoEnvironment.ps1 `
  -OrgCode nl `
  -Environment dev `
  -Project codeflow `
  -RegionShort san `
  -Location southafricanorth `
  -SubscriptionId 00000000-0000-0000-0000-000000000000 `
  -CreateKeyVault `
  -OutputJsonPath ./az-env-dev-codeflow.json
```

### 2. `Set-GitHubSecretsFromJson.ps1`

Reads the JSON summary file and creates GitHub Actions repository secrets using the GitHub CLI (`gh secret set`).

You must be authenticated with `gh` and have access to the target repo.

**Example:**

```powershell
.\scripts\Set-GitHubSecretsFromJson.ps1 `
  -JsonPath ./az-env-dev-codeflow.json `
  -Repo JustAGHosT/codeflow-engine `
  -Prefix DEV_
```

**Secrets created (example):**
- `DEV_AZURE_SUBSCRIPTION_ID`
- `DEV_AZURE_RESOURCE_GROUP`
- `DEV_AZURE_LOCATION`
- `DEV_AZURE_STORAGE_ACCOUNT`
- `DEV_AZURE_STORAGE_CONNECTION`
- `DEV_AZURE_LOG_ANALYTICS_WORKSPACE`
- `DEV_AZURE_LOG_ANALYTICS_WORKSPACE_ID`
- `DEV_AZURE_LOG_ANALYTICS_KEY`
- `DEV_AZURE_APPINSIGHTS_NAME`
- `DEV_AZURE_APPINSIGHTS_KEY`
- `DEV_AZURE_KEYVAULT_NAME` (if KV was created)

### 3. `New-AzRepoFullEnvironment.ps1`

Creates the full environment for a repo:
- Everything from `New-AzRepoEnvironment.ps1`
- App Service plan (Linux)
- Web App for the UI
- Container App Environment
- Container App for the engine
- User-assigned managed identity
- Assigns identity to Web App + Container App
- Optionally grants Key Vault roles to the identity

**Example:**

```powershell
.\scripts\New-AzRepoFullEnvironment.ps1 `
  -OrgCode nl `
  -Environment dev `
  -Project codeflow `
  -RegionShort san `
  -Location southafricanorth `
  -SubscriptionId 00000000-0000-0000-0000-000000000000 `
  -UiRuntime "NODE:20-lts" `
  -EngineImage "ghcr.io/justaghost/codeflow-engine:latest" `
  -CreateKeyVault
```

## 📋 Requirements

- **PowerShell 7+**
- **az CLI** logged in and targeting the correct tenant/subscription
- **gh CLI** for GitHub secrets helper (`Set-GitHubSecretsFromJson.ps1`)
- **az extension** `containerapp` for the full environment script:
  ```powershell
  az extension add --name containerapp
  ```

## 🚀 Quick Start

### Step 1: Create Core Infrastructure

```powershell
.\scripts\New-AzRepoEnvironment.ps1 `
  -OrgCode nl `
  -Environment dev `
  -Project codeflow `
  -RegionShort san `
  -Location southafricanorth `
  -SubscriptionId <your-subscription-id> `
  -CreateKeyVault `
  -OutputJsonPath ./az-env-dev-codeflow.json
```

### Step 2: Set GitHub Secrets

```powershell
# Authenticate with GitHub CLI first
gh auth login

# Set secrets from the JSON file
.\scripts\Set-GitHubSecretsFromJson.ps1 `
  -JsonPath ./az-env-dev-codeflow.json `
  -Repo your-org/your-repo `
  -Prefix DEV_
```

### Step 3: Create Full Environment (Optional)

```powershell
.\scripts\New-AzRepoFullEnvironment.ps1 `
  -OrgCode nl `
  -Environment dev `
  -Project codeflow `
  -RegionShort san `
  -Location southafricanorth `
  -SubscriptionId <your-subscription-id> `
  -UiRuntime "NODE:20-lts" `
  -EngineImage "ghcr.io/your-org/your-image:latest" `
  -CreateKeyVault
```

## 📝 Naming Convention

All resources follow the pattern: `org-env-project-type-region`

**Examples:**
- Resource Group: `nl-dev-codeflow-rg-san`
- Storage Account: `stnldevcodeflowsan` (sanitized, max 24 chars)
- Log Analytics: `nl-dev-codeflow-law-san`
- App Insights: `nl-dev-codeflow-ai-san`
- Key Vault: `kv-nl-dev-codeflow-san` (sanitized, max 24 chars)
- Web App: `nl-dev-codeflow-ui-san` (sanitized, max 60 chars)
- Container App: `nl-dev-codeflow-engine-san` (sanitized, max 32 chars)

## 🔧 Parameters

### Common Parameters (All Scripts)

| Parameter         | Description                                                      | Required |
| ----------------- | ---------------------------------------------------------------- | -------- |
| `-OrgCode`        | Short org code (e.g. nl, tws, mys)                               | ✅ Yes    |
| `-Environment`    | Environment name (dev, test, uat, prod)                          | ✅ Yes    |
| `-Project`        | Project/repo name (e.g. codeflow)                                | ✅ Yes    |
| `-RegionShort`    | Short region code (e.g. san, euw, wus)                           | ✅ Yes    |
| `-Location`       | Azure location (e.g. southafricanorth, westeurope)               | ✅ Yes    |
| `-SubscriptionId` | Azure subscription GUID                                          | ✅ Yes    |
| `-CreateKeyVault` | Switch to create Key Vault                                       | ❌ No     |
| `-OutputJsonPath` | Path for JSON summary (default: `./az-environment-summary.json`) | ❌ No     |

### Additional Parameters (`New-AzRepoFullEnvironment.ps1`)

| Parameter      | Description                                                    | Required |
| -------------- | -------------------------------------------------------------- | -------- |
| `-UiRuntime`   | Runtime stack for Web App (e.g., "NODE:20-lts", "PYTHON:3.11") | ✅ Yes    |
| `-EngineImage` | Container image for engine (e.g., "ghcr.io/org/repo:tag")      | ✅ Yes    |

### Parameters (`Set-GitHubSecretsFromJson.ps1`)

| Parameter   | Description                                        | Required |
| ----------- | -------------------------------------------------- | -------- |
| `-JsonPath` | Path to JSON file from `New-AzRepoEnvironment.ps1` | ✅ Yes    |
| `-Repo`     | GitHub repo in format "owner/repo"                 | ✅ Yes    |
| `-Prefix`   | Prefix for secret names (e.g., "DEV_", "PROD_")    | ❌ No     |

## 📊 JSON Output Structure

The scripts emit a JSON file with the following structure:

```json
{
  "SubscriptionId": "00000000-0000-0000-0000-000000000000",
  "OrgCode": "nl",
  "Environment": "dev",
  "Project": "codeflow",
  "RegionShort": "san",
  "Location": "southafricanorth",
  "ResourceGroup": "nl-dev-codeflow-rg-san",
  "StorageAccountName": "stnldevcodeflowsan",
  "StorageConnectionString": "DefaultEndpointsProtocol=https;...",
  "LogAnalyticsWorkspace": "nl-dev-codeflow-law-san",
  "LogAnalyticsWorkspaceId": "/subscriptions/.../workspaces/...",
  "LogAnalyticsKey": "...",
  "AppInsightsName": "nl-dev-codeflow-ai-san",
  "AppInsightsKey": "...",
  "KeyVaultName": "kvnldevcodeflowsan"  // Only if -CreateKeyVault was used
}
```

For full environment, additional fields:
```json
{
  "AppServicePlanName": "nl-dev-codeflow-asp-san",
  "WebAppName": "nl-dev-codeflow-ui-san",
  "WebAppUrl": "https://nl-dev-codeflow-ui-san.azurewebsites.net",
  "ContainerAppEnvName": "nl-dev-codeflow-cae-san",
  "ContainerAppName": "nl-dev-codeflow-engine-san",
  "ContainerAppUrl": "https://...azurecontainerapps.io",
  "ManagedIdentityName": "nl-dev-codeflow-identity-san",
  "ManagedIdentityId": "/subscriptions/.../identities/...",
  "ManagedIdentityPrincipalId": "..."
}
```

## 🔐 Authentication

### Azure CLI

```powershell
# Login to Azure
az login

# Set subscription
az account set --subscription <subscription-id>

# Verify
az account show
```

### GitHub CLI

```powershell
# Login to GitHub
gh auth login

# Verify
gh auth status
```

## ✅ Verification

After running the scripts:

1. **Check Azure Portal**:
   - Navigate to your resource group
   - Verify all resources are created
   - Check resource names match the naming convention

2. **Check GitHub Secrets**:
   - Go to repository → Settings → Secrets and variables → Actions
   - Verify secrets are created with the correct prefix

3. **Test Deployments**:
   - Verify Web App is accessible
   - Check Container App is running
   - Review Application Insights for telemetry

## 🛠️ Troubleshooting

### Common Issues

1. **"az: command not found"**
   - Install Azure CLI: https://aka.ms/InstallAzureCLI
   - Verify installation: `az --version`

2. **"gh: command not found"**
   - Install GitHub CLI: https://cli.github.com/
   - Verify installation: `gh --version`

3. **"Storage account name already exists"**
   - Storage account names must be globally unique
   - Try a different `-RegionShort` or `-Project` value

4. **"Failed to create Key Vault"**
   - Ensure you have permissions to create Key Vaults
   - Check if Key Vault name is available (globally unique)

5. **"Container App extension not found"**
   ```powershell
   az extension add --name containerapp
   az extension update --name containerapp
   ```

6. **"GitHub secret set failed"**
   - Verify you're authenticated: `gh auth status`
   - Check repository access permissions
   - Ensure you have admin rights to the repository

## 📚 Related Documentation

- [Azure CLI Documentation](https://docs.microsoft.com/cli/azure/)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Azure Container Apps](https://docs.microsoft.com/azure/container-apps/)
- [Azure App Service](https://docs.microsoft.com/azure/app-service/)

## 💡 Usage Tips

1. **Idempotency**: The scripts can be run multiple times safely. Existing resources are detected and reused.

2. **JSON Reuse**: Save the JSON output files for each environment. You can use them later to update secrets or feed into other automation.

3. **Environment Separation**: Use different prefixes (`DEV_`, `PROD_`) when setting GitHub secrets to avoid conflicts.

4. **Resource Cleanup**: To remove all resources, delete the resource group:
   ```powershell
   az group delete --name <resource-group-name> --yes --no-wait
   ```

