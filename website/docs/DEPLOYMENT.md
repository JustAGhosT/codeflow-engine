# CodeFlow Website - Deployment Guide

This guide covers deploying the CodeFlow website to Azure Static Web Apps.

---

## Prerequisites

- Node.js 20+
- Azure subscription
- Azure Static Web Apps resource
- GitHub repository with website code

---

## Local Development

### Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

The site will be available at `http://localhost:3000`

### Build Locally

```bash
# Build for production
npm run build

# Start production server
npm start
```

---

## Azure Static Web Apps Deployment

### Option 1: GitHub Actions (Automatic)

The website includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that automatically deploys on push to `main` branch.

**Setup:**

#### 1. Create Azure Static Web App resource

```bash
az staticwebapp create \
  --name codeflow-website \
  --resource-group codeflow-rg \
  --location eastus2 \
  --sku Free
```

#### 2. Get deployment toke

```bash
az staticwebapp secrets list \
  --name codeflow-website \
  --resource-group codeflow-rg \
  --query properties.apiKey -o tsv
```

#### 3. Add to GitHub Secrets

- Go to repository Settings → Secrets
- Add secret: `AZURE_STATIC_WEB_APPS_API_TOKEN`
- Paste the deployment token

#### 24. Push to main branch

```bash
git push origin main
```

Deployment will start automatically.

### Option 2: Azure CLI (Manual)

```bash
# Build the site
npm run build

# Deploy using Azure CLI
az staticwebapp deploy \
  --name codeflow-website \
  --resource-group codeflow-rg \
  --app-location "/" \
  --output-location "out" \
  --login
```

### Option 3: VS Code Extension

1. Install "Azure Static Web Apps" extension
2. Right-click on `out` folder
3. Select "Deploy to Static Web App"
4. Choose your Static Web App resource

---

## Environment Configuration

### Environment Variables

Create `.env.production` for production:

```env
NEXT_PUBLIC_API_URL=https://api.codeflow.io
NEXT_PUBLIC_ANALYTICS_ID=your_analytics_id
```

### Configuration Files

- `next.config.js` - Next.js configuration
- `staticwebapp.config.json` - Azure Static Web Apps routing

---

## Custom Domain Setup

### 1. Add Custom Domain in Azure

```bash
az staticwebapp hostname set \
  --name codeflow-website \
  --resource-group codeflow-rg \
  --hostname www.codeflow.io
```

### 2. Configure DNS

Add CNAME record:

``` text
Type: CNAME
Name: www
Value: <your-static-web-app>.azurestaticapps.net
```

### 3. SSL Certificate

Azure automatically provisions SSL certificates for custom domains. Wait 5-10 minutes for provisioning.

### 4. Verify

```bash
# Check domain status
az staticwebapp hostname show \
  --name codeflow-website \
  --resource-group codeflow-rg \
  --hostname www.codeflow.io
```

---

## CDN Configuration

### Azure CDN Integration

#### 1. Create CDN profile

```bash
az cdn profile create \
  --name codeflow-cdn \
  --resource-group codeflow-rg \
  --sku Standard_Microsoft
```

#### 2. Create CDN endpoint

```bash
az cdn endpoint create \
  --name codeflow-website-cdn \
  --profile-name codeflow-cdn \
  --resource-group codeflow-rg \
  --origin www.codeflow.io
```

#### 3. Configure caching rules in Azure Portal

---

## Build Configuration

### Next.js Build Settings

The site uses static export for Azure Static Web Apps:

```javascript
// next.config.js
module.exports = {
  output: "export",
  images: {
    unoptimized: true,
  },
};
```

### Build Optimization

- Image optimization: Use `next/image` with `unoptimized: true` for static export
- Code splitting: Automatic with Next.js
- Minification: Enabled by default
- Tree shaking: Automatic

---

## Monitoring

### Application Insights

#### 1. Create Application Insights

```bash
az monitor app-insights component create \
  --app codeflow-website-insights \
  --location eastus2 \
  --resource-group codeflow-rg
```

#### 2. Add to Next.js

```javascript
// Add to _app.js or _app.tsx
import { Analytics } from "@vercel/analytics/react";
```

### Logs

View logs in Azure Portal:

- Navigate to Static Web App → Monitoring → Logs
- Or use Azure CLI:

```bash
az staticwebapp logs show \
  --name codeflow-website \
  --resource-group codeflow-rg
```

---

## Troubleshooting

### Build Failures

**TypeScript errors:**

```bash
# Check TypeScript
npm run type-check

# Fix errors
npm run lint -- --fix
```

**Build timeout:**

- Increase build timeout in GitHub Actions
- Optimize build process
- Remove unused dependencies

### Deployment Issues

**404 errors:**

- Check `staticwebapp.config.json` routing rules
- Verify `output` directory in `next.config.js`
- Check build output location

**Environment variables not working:**

- Verify `.env.production` is committed (if needed)
- Check Azure Static Web Apps configuration
- Use `NEXT_PUBLIC_` prefix for client-side variables

### Performance Issues

**Slow page loads:**

- Enable CDN
- Optimize images
- Reduce bundle size
- Enable compression

---

## Rollback

### Rollback to Previous Deployment

1. Go to Azure Portal
2. Navigate to Static Web App → Deployment history
3. Select previous deployment
4. Click "Redeploy"

Or use Azure CLI:

```bash
az staticwebapp deployment show \
  --name codeflow-website \
  --resource-group codeflow-rg \
  --deployment-id <previous-deployment-id>
```

---

## Best Practices

1. **Test locally** before deploying
2. **Use staging environment** for testing
3. **Monitor performance** with Application Insights
4. **Keep dependencies updated**
5. **Use semantic versioning** for releases
6. **Document breaking changes**
7. **Set up alerts** for deployment failures

---

## Additional Resources

- [Azure Static Web Apps Documentation](https://docs.microsoft.com/azure/static-web-apps/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Static Web Apps Configuration](https://docs.microsoft.com/azure/static-web-apps/configuration)

---

## Support

For issues or questions:

- GitHub Issues: [codeflow-website/issues](https://github.com/JustAGhosT/codeflow-website/issues)
- Azure Support: [Azure Portal](https://portal.azure.com)
