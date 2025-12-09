# CodeFlow Engine - Azure Deployment Guide

This guide covers deploying CodeFlow Engine to Azure using Azure Container Apps, Azure Database for PostgreSQL, and Azure Cache for Redis.

---

## Prerequisites

- Azure subscription with contributor access
- Azure CLI installed and logged in
- Bicep CLI installed (optional, for infrastructure as code)
- GitHub repository with CodeFlow Engine code

---

## Architecture

``` text
┌─────────────────┐
│  Azure Container│
│      Apps       │  ← CodeFlow Engine
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼───┐
│PostgreSQL│ │ Redis │
└─────────┘ └───────┘
```

---

## Quick Deployment (30 minutes)

### Step 1: Clone Infrastructure Repository

```bash
git clone https://github.com/JustAGhosT/codeflow-infrastructure.git
cd codeflow-infrastructure/bicep
```

### Step 2: Set Up Azure Resources

```bash
# Login to Azure
az login

# Set variables
RESOURCE_GROUP="codeflow-rg"
LOCATION="eastus"
ENVIRONMENT="production"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Deploy infrastructure
az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file main.bicep \
  --parameters @codeflow-engine-parameters.json
```

### Step 3: Build and Push Docker Image

```bash
# Set variables
ACR_NAME="codeflowacr"
IMAGE_NAME="codeflow-engine"
VERSION="1.0.1"

# Login to ACR
az acr login --name $ACR_NAME

# Build and push
docker build -t $ACR_NAME.azurecr.io/$IMAGE_NAME:$VERSION .
docker push $ACR_NAME.azurecr.io/$IMAGE_NAME:$VERSION
```

### Step 4: Deploy to Container Apps

```bash
# Deploy using the deployment script
.\deploy-codeflow-engine.ps1 \
  -ResourceGroupName $RESOURCE_GROUP \
  -Environment $ENVIRONMENT \
  -ImageTag $VERSION
```

---

## Detailed Deployment Steps

### 1. Infrastructure Setup

#### Option A: Using Bicep (Recommended)

```bash
cd codeflow-infrastructure/bicep

# Review parameters
cat codeflow-engine-parameters.json

# Deploy
az deployment group create \
  --resource-group codeflow-rg \
  --template-file main.bicep \
  --parameters @codeflow-engine-parameters.json
```

#### Option B: Using Azure Portal

1. Navigate to Azure Portal
2. Create Resource Group: `codeflow-rg`
3. Create Azure Database for PostgreSQL
4. Create Azure Cache for Redis
5. Create Azure Container Registry
6. Create Azure Container Apps Environment

### 2. Database Configuration

```bash
# Get database connection string
az postgres flexible-server show-connection-string \
  --server-name codeflow-postgres \
  --database-name codeflow \
  --admin-user codeflow \
  --admin-password YourPassword123!
```

### 3. Environment Variables

Set these in Azure Container Apps:

```env
# Database
DATABASE_URL=postgresql://codeflow:password@codeflow-postgres.postgres.database.azure.com:5432/codeflow

# Redis
REDIS_URL=rediss://codeflow-redis.redis.cache.windows.net:6380?ssl=true

# GitHub
GITHUB_TOKEN=your_github_token

# AI Providers (optional)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Application
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### 4. Secrets Management

Store secrets in Azure Key Vault:

```bash
# Create Key Vault
az keyvault create \
  --name codeflow-kv \
  --resource-group codeflow-rg \
  --location eastus

# Store secrets
az keyvault secret set \
  --vault-name codeflow-kv \
  --name github-token \
  --value "your_github_token"

az keyvault secret set \
  --vault-name codeflow-kv \
  --name openai-api-key \
  --value "your_openai_key"
```

Reference in Container Apps:

```yaml
env:
  - name: GITHUB_TOKEN
    secretRef: github-token
  - name: OPENAI_API_KEY
    secretRef: openai-api-key
```

---

## Deployment Scripts

### PowerShell Script

```powershell
.\deploy-codeflow-engine.ps1 `
  -ResourceGroupName "codeflow-rg" `
  -Environment "production" `
  -ImageTag "1.0.1" `
  -GitHubToken (Get-AzKeyVaultSecret -VaultName "codeflow-kv" -Name "github-token").SecretValueText
```

### Bash Script

```bash
./deploy-codeflow-engine.sh \
  --resource-group codeflow-rg \
  --environment production \
  --image-tag 1.0.1 \
  --github-token $(az keyvault secret show --vault-name codeflow-kv --name github-token --query value -o tsv)
```

---

## Health Checks

After deployment, verify:

```bash
# Get Container App URL
APP_URL=$(az containerapp show \
  --name codeflow-engine \
  --resource-group codeflow-rg \
  --query properties.configuration.ingress.fqdn -o tsv)

# Check health
curl https://$APP_URL/health
```

---

## Scaling

### Manual Scaling

```bash
az containerapp update \
  --name codeflow-engine \
  --resource-group codeflow-rg \
  --min-replicas 2 \
  --max-replicas 10
```

### Auto-scaling

Configure in `main.bicep`:

```bicep
scale: {
  minReplicas: 2
  maxReplicas: 10
  rules: [
    {
      name: 'http-rule'
      http: {
        metadata: {
          concurrentRequests: '100'
        }
      }
    }
  ]
}
```

---

## Monitoring

### Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app codeflow-insights \
  --location eastus \
  --resource-group codeflow-rg

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app codeflow-insights \
  --resource-group codeflow-rg \
  --query instrumentationKey -o tsv)

# Add to Container App
az containerapp update \
  --name codeflow-engine \
  --resource-group codeflow-rg \
  --set-env-vars "APPINSIGHTS_INSTRUMENTATION_KEY=$INSTRUMENTATION_KEY"
```

### Logs

```bash
# View logs
az containerapp logs show \
  --name codeflow-engine \
  --resource-group codeflow-rg \
  --follow
```

---

## Troubleshooting

### Container Won't Start

1 Check logs:

```bash
az containerapp logs show --name codeflow-engine --resource-group codeflow-rg
```

2 Verify environment variables

```bash
az containerapp show --name codeflow-engine --resource-group codeflow-rg --query properties.template.containers[0].env
```

3 Check database connectivity

```bash
az postgres flexible-server show --name codeflow-postgres --resource-group codeflow-rg
```

### Database Connection Issues

1 Verify firewall rules allow Container Apps:

```bash
az postgres flexible-server firewall-rule create \
  --server-name codeflow-postgres \
  --resource-group codeflow-rg \
  --name AllowContainerApps \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

2 Check connection string format
3 Verify credentials in Key Vault

### High Costs

1. Review scaling configuration
2. Use consumption plan for Container Apps
3. Consider reserved capacity for database
4. Monitor costs in Azure Cost Management

---

## Rollback

### Rollback to Previous Version

```bash
# List revisions
az containerapp revision list \
  --name codeflow-engine \
  --resource-group codeflow-rg

# Activate previous revision
az containerapp revision activate \
  --name codeflow-engine \
  --resource-group codeflow-rg \
  --revision <previous-revision-name>
```

---

## Next Steps

- Set up CI/CD pipeline (see [CI/CD Guide](../ci-cd/CI_CD.md))
- Configure custom domain
- Set up monitoring alerts
- Review [Security Best Practices](../security/SECURITY.md)

---

## Additional Resources

- [Azure Container Apps Documentation](https://docs.microsoft.com/azure/container-apps/)
- [Bicep Documentation](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)
- [Full Deployment Guide](./DEPLOYMENT_GUIDE.md)
