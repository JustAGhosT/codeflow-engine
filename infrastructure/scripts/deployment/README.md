# Deployment Automation Scripts

Enhanced deployment scripts with rollback, health checks, and smoke tests.

## Scripts

### `deploy-with-rollback.ps1`

Enhanced deployment wrapper with automatic rollback capabilities.

**Features:**
- Pre-deployment validation
- State backup before deployment
- Automatic rollback on failure
- Health check integration
- Smoke test integration
- Comprehensive error handling

**Usage:**
```powershell
.\deploy-with-rollback.ps1 `
    -DeploymentScript ".\deploy-codeflow-engine.ps1" `
    -ResourceGroup "nl-dev-codeflow-rg-san" `
    -HealthCheckUrl "https://api.codeflow.example.com/health" `
    -SmokeTestScript ".\smoke-tests.ps1"
```

### `health-check.ps1`

Comprehensive health check script for deployed services.

**Features:**
- Basic health check
- Detailed health check with component status
- Retry logic
- Configurable timeout

**Usage:**
```powershell
.\health-check.ps1 `
    -HealthCheckUrl "https://api.codeflow.example.com" `
    -Retries 5 `
    -RetryDelay 10
```

### `smoke-tests.ps1`

Critical path smoke tests for deployed services.

**Features:**
- Root endpoint test
- Health endpoint test
- Version endpoint test
- Dashboard endpoint test
- API response format validation

**Usage:**
```powershell
.\smoke-tests.ps1 `
    -BaseUrl "https://api.codeflow.example.com" `
    -Timeout 30
```

## Integration Example

```powershell
# Enhanced deployment with all features
.\deploy-with-rollback.ps1 `
    -DeploymentScript "..\..\codeflow-infrastructure\bicep\deploy-codeflow-engine.ps1" `
    -ResourceGroup "nl-prod-codeflow-rg-san" `
    -RollbackEnabled $true `
    -HealthCheckUrl "https://api.codeflow.example.com/health" `
    -HealthCheckTimeout 300 `
    -SmokeTestScript ".\smoke-tests.ps1"
```

## Features

### Rollback Capabilities

- Automatic state backup before deployment
- Rollback on deployment failure
- Rollback on health check failure
- Rollback on smoke test failure

### Health Checks

- Basic endpoint health check
- Detailed component health check
- Retry logic with exponential backoff
- Configurable timeouts

### Smoke Tests

- Critical path testing
- API endpoint validation
- Response format validation
- Non-critical endpoint handling

## Error Handling

All scripts include comprehensive error handling:
- Validation errors
- Network errors
- Timeout errors
- Deployment errors

## Next Steps

1. Integrate into existing deployment workflows
2. Add more comprehensive smoke tests
3. Implement full rollback logic
4. Add deployment metrics tracking

