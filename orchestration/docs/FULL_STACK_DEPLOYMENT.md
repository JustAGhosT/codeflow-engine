# CodeFlow Full Stack Deployment Guide

This guide covers deploying the complete CodeFlow stack, including all components and their integration.

---

## Architecture Overview

``` text
┌─────────────────────────────────────────────────────────────┐
│                        Internet                              │
└───────────────┬─────────────────────────────────────────────┘
                │
        ┌───────▼────────┐
        │  Load Balancer │
        │   (Azure)      │
        └───────┬────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───▼───┐  ┌───▼───┐  ┌───▼────┐
│Website│  │Engine │  │Extension│
│(Static│  │(API)  │  │(VS Code)│
│ Web)  │  │       │  │         │
└───────┘  └───┬───┘  └─────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│Postgres│ │Redis │ │Desktop│
│        │ │      │ │  App  │
└────────┘ └──────┘ └───────┘
```

**Components:**

- **Website**: Next.js static site (Azure Static Web Apps)
- **Engine**: Python API server (Azure Container Apps)
- **Extension**: VS Code extension (VS Code Marketplace)
- **Desktop**: Tauri desktop app (distributed via releases)
- **Database**: PostgreSQL (Azure Database)
- **Cache**: Redis (Azure Cache)

---

## Prerequisites

### Required

- Azure subscription with contributor access
- GitHub account with all repositories
- Domain name (optional but recommended)
- SSL certificates (auto-provisioned by Azure)

### Tools

- Azure CLI
- Docker
- Node.js 20+
- Python 3.12+
- Git

---

## Deployment Order

Deploy components in this order:

1. **Infrastructure** (Database, Cache, Container Registry)
2. **Engine** (API server)
3. **Website** (Static site)
4. **Extension** (VS Code Marketplace - manual)
5. **Desktop** (Build and distribute - manual)

---

## Step 1: Infrastructure Setup

### 1.1 Create Resource Group

```bash
RESOURCE_GROUP="codeflow-rg"
LOCATION="eastus"

az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION
```

### 1.2 Deploy Infrastructure

```bash
cd codeflow-infrastructure/bicep

# Deploy core infrastructure
az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file main.bicep \
  --parameters @codeflow-engine-parameters.json
```

This creates:

- Azure Container Apps Environment
- Azure Database for PostgreSQL
- Azure Cache for Redis
- Azure Container Registry
- Log Analytics Workspace

### 1.3 Get Connection Strings

```bash
# Database connection string
DB_CONNECTION=$(az postgres flexible-server show-connection-string \
  --server-name codeflow-postgres \
  --database-name codeflow \
  --admin-user codeflow \
  --query connectionStrings.psql -o tsv)

# Redis connection string
REDIS_URL=$(az redis list-keys \
  --name codeflow-redis \
  --resource-group $RESOURCE_GROUP \
  --query primaryKey -o tsv)
```

---

## Step 2: Deploy CodeFlow Engine

### 2.1 Build and Push Docker Image

```bash
cd codeflow-engine

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

### 2.2 Deploy to Container Apps

```bash
cd codeflow-infrastructure/bicep

.\deploy-codeflow-engine.ps1 \
  -ResourceGroupName $RESOURCE_GROUP \
  -Environment production \
  -ImageTag $VERSION
```

### 2.3 Configure Environment Variables

Set in Azure Container Apps:

```env
DATABASE_URL=$DB_CONNECTION
REDIS_URL=rediss://codeflow-redis.redis.cache.windows.net:6380?ssl=true&password=$REDIS_KEY
GITHUB_TOKEN=your_github_token
OPENAI_API_KEY=your_openai_key
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### 2.4 Verify Engine Deployment

```bash
# Get Container App URL
ENGINE_URL=$(az containerapp show \
  --name codeflow-engine \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn -o tsv)

# Check health
curl https://$ENGINE_URL/health
```

---

## Step 3: Deploy Website

### 3.1 Create Static Web App

```bash
az staticwebapp create \
  --name codeflow-website \
  --resource-group $RESOURCE_GROUP \
  --location eastus2 \
  --sku Standard
```

### 3.2 Configure GitHub Actions

#### 1. Get deployment token

```bash
DEPLOY_TOKEN=$(az staticwebapp secrets list \
  --name codeflow-website \
  --resource-group $RESOURCE_GROUP \
  --query properties.apiKey -o tsv)
```

#### 2. Add to GitHub Secrets

- Repository: `codeflow-website`
- Secret: `AZURE_STATIC_WEB_APPS_API_TOKEN`
- Value: `$DEPLOY_TOKEN`

#### 3. Push to main branch (deploys automatically)

### 3.3 Configure Custom Domain

```bash
az staticwebapp hostname set \
  --name codeflow-website \
  --resource-group $RESOURCE_GROUP \
  --hostname www.codeflow.io
```

Add DNS CNAME:

``` text
www.codeflow.io → codeflow-website.azurestaticapps.net
```

---

## Step 4: Integration Configuration

### 4.1 Configure Website → Engine

Update website environment variables:

```env
NEXT_PUBLIC_API_URL=https://$ENGINE_URL
NEXT_PUBLIC_WS_URL=wss://$ENGINE_URL/ws
```

### 4.2 Configure Extension → Engine

Extension connects to Engine via configuration:

1. Open VS Code Settings
2. Search for "CodeFlow"
3. Set `codeflow.apiUrl` to `https://$ENGINE_URL`
4. Set `codeflow.apiKey` (if using API key auth)

### 4.3 Configure Desktop → Engine

Desktop app configuration:

1. Open Desktop app settings
2. Set API URL: `https://$ENGINE_URL`
3. Configure authentication

---

## Step 5: Health Checks and Monitoring

### 5.1 Health Check Endpoints

**Engine:**

```bash
curl https://$ENGINE_URL/health
```

**Website:**

```bash
curl https://www.codeflow.io/health
```

### 5.2 Set Up Monitoring

```bash
# Create Application Insights
az monitor app-insights component create \
  --app codeflow-insights \
  --location eastus2 \
  --resource-group $RESOURCE_GROUP

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app codeflow-insights \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

# Add to Engine
az containerapp update \
  --name codeflow-engine \
  --resource-group $RESOURCE_GROUP \
  --set-env-vars "APPINSIGHTS_INSTRUMENTATION_KEY=$INSTRUMENTATION_KEY"
```

### 5.3 Set Up Alerts

```bash
# Create alert for Engine downtime
az monitor metrics alert create \
  --name codeflow-engine-down \
  --resource-group $RESOURCE_GROUP \
  --scopes /subscriptions/{sub-id}/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.App/containerApps/codeflow-engine \
  --condition "avg HttpRequests < 1" \
  --window-size 5m \
  --evaluation-frequency 1m
```

---

## Step 6: Scaling Configuration

### 6.1 Engine Scaling

```bash
az containerapp update \
  --name codeflow-engine \
  --resource-group $RESOURCE_GROUP \
  --min-replicas 2 \
  --max-replicas 10
```

### 6.2 Database Scaling

```bash
az postgres flexible-server update \
  --name codeflow-postgres \
  --resource-group $RESOURCE_GROUP \
  --sku-name Standard_D2s_v3 \
  --tier GeneralPurpose
```

### 6.3 Redis Scaling

```bash
az redis update \
  --name codeflow-redis \
  --resource-group $RESOURCE_GROUP \
  --sku Standard \
  --vm-size c1
```

---

## Integration Testing

### Test Full Stack

#### 1. **Website → Engine:**

```bash
# Test API call from website
curl -X GET https://www.codeflow.io/api/status \
  -H "Origin: https://www.codeflow.io"
```

#### 2. **Extension → Engine:**

- Open VS Code
- Install CodeFlow extension
- Run "CodeFlow: Check Current File"
- Verify API call succeeds

#### 3. **Desktop → Engine:**

- Open Desktop app
- Connect to Engine
- Verify connection status

---

## Rollback Procedures

### Rollback Engine

```bash
# List revisions
az containerapp revision list \
  --name codeflow-engine \
  --resource-group $RESOURCE_GROUP

# Activate previous revision
az containerapp revision activate \
  --name codeflow-engine \
  --resource-group $RESOURCE_GROUP \
  --revision <previous-revision>
```

### Rollback Website

1. Go to Azure Portal
2. Navigate to Static Web App → Deployment history
3. Select previous deployment
4. Click "Redeploy"

---

## Troubleshooting

### Engine Not Responding

#### 1. Check Container App logs

```bash
az containerapp logs show \
  --name codeflow-engine \
  --resource-group $RESOURCE_GROUP \
  --follow
```

#### 2. Verify database connectivity

#### 3. Check environment variables

#### 4. Verify image is correct version

### Website Not Loading

1. Check build logs in GitHub Actions
2. Verify static files in `out` directory
3. Check routing rules in `staticwebapp.config.json`
4. Verify custom domain DNS

### Integration Issues

1. Check CORS configuration in Engine
2. Verify API URLs in clients
3. Check authentication tokens
4. Review network logs

---

## Cost Optimization

### Estimated Monthly Costs (Small Scale)

- Container Apps: ~$50/month
- PostgreSQL: ~$100/month
- Redis: ~$50/month
- Static Web Apps: Free tier
- **Total: ~$200/month**

### Optimization Tips

1. Use consumption plan for Container Apps
2. Scale down during off-hours
3. Use Basic tier for development
4. Enable auto-shutdown for dev environments
5. Monitor costs in Azure Cost Management

---

## Security Checklist

- [ ] All secrets in Azure Key Vault
- [ ] HTTPS enabled for all endpoints
- [ ] CORS configured correctly
- [ ] Database firewall rules set
- [ ] Redis SSL enabled
- [ ] API authentication configured
- [ ] Rate limiting enabled
- [ ] Security scanning in CI/CD
- [ ] Logs reviewed regularly

---

## Next Steps

1. Set up CI/CD pipelines (see [CI/CD Guide](../ci-cd/CI_CD.md))
2. Configure custom domains
3. Set up monitoring alerts
4. Review security best practices
5. Plan for scaling

---

## Additional Resources

- [Engine Deployment Guide](../../codeflow-engine/docs/deployment/DEPLOYMENT_GUIDE.md)
- [Website Deployment Guide](../../codeflow-website/docs/DEPLOYMENT.md)
- [Infrastructure Documentation](../../codeflow-infrastructure/README.md)
- [Azure Documentation](https://docs.microsoft.com/azure/)

---

## Support

For issues or questions:

- GitHub Issues: [codeflow-orchestration/issues](https://github.com/JustAGhosT/codeflow-orchestration/issues)
- Documentation: See individual component guides
