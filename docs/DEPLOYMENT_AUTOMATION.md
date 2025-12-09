# Deployment Automation Guide

**Phase:** Wave 4, Phase 9.1  
**Status:** Implementation Complete  
**Purpose:** Guide for using enhanced deployment automation

---

## Overview

This guide documents the enhanced deployment automation features added to CodeFlow, including rollback capabilities, health checks, and smoke tests.

---

## Enhanced Deployment Scripts

### `deploy-with-rollback.ps1`

A wrapper script that enhances any deployment script with:
- Automatic rollback on failure
- Health check validation
- Smoke test execution
- Comprehensive error handling

#### Features

1. **Pre-Deployment Validation**
   - Validates deployment script exists
   - Validates Azure CLI availability
   - Validates resource group exists

2. **State Backup**
   - Exports current resource group state
   - Creates backup file for rollback
   - Stores backup in temp directory

3. **Deployment Execution**
   - Executes deployment script
   - Captures deployment errors
   - Tracks deployment duration

4. **Health Check Integration**
   - Performs health checks after deployment
   - Retry logic with configurable attempts
   - Timeout handling

5. **Smoke Test Integration**
   - Runs smoke tests after deployment
   - Validates critical paths
   - Reports test results

6. **Automatic Rollback**
   - Triggers on deployment failure
   - Triggers on health check failure
   - Triggers on smoke test failure
   - Attempts to restore from backup

#### Usage

```powershell
.\scripts\deployment\deploy-with-rollback.ps1 `
    -DeploymentScript ".\deploy-codeflow-engine.ps1" `
    -ResourceGroup "nl-prod-codeflow-rg-san" `
    -RollbackEnabled $true `
    -HealthCheckUrl "https://api.codeflow.example.com/health" `
    -HealthCheckTimeout 300 `
    -SmokeTestScript ".\scripts\deployment\smoke-tests.ps1"
```

#### Parameters

- `DeploymentScript` (Required): Path to deployment script
- `ResourceGroup` (Required): Azure Resource Group name
- `RollbackEnabled` (Optional): Enable rollback (default: $true)
- `HealthCheckUrl` (Optional): Health check endpoint URL
- `HealthCheckTimeout` (Optional): Health check timeout in seconds (default: 300)
- `SmokeTestScript` (Optional): Path to smoke test script

---

## Health Check Script

### `health-check.ps1`

Comprehensive health check script for deployed services.

#### Features

1. **Basic Health Check**
   - Tests `/health` endpoint
   - Validates HTTP 200 response
   - Checks response status

2. **Detailed Health Check**
   - Tests `/health?detailed=true` endpoint
   - Validates component health
   - Reports database status
   - Reports Redis status

3. **Retry Logic**
   - Configurable retry attempts
   - Configurable retry delay
   - Exponential backoff support

#### Usage

```powershell
.\scripts\deployment\health-check.ps1 `
    -HealthCheckUrl "https://api.codeflow.example.com" `
    -Timeout 60 `
    -Retries 5 `
    -RetryDelay 10
```

#### Parameters

- `HealthCheckUrl` (Required): Base URL for health checks
- `Timeout` (Optional): Timeout in seconds (default: 60)
- `Retries` (Optional): Number of retry attempts (default: 3)
- `RetryDelay` (Optional): Delay between retries in seconds (default: 5)

---

## Smoke Test Script

### `smoke-tests.ps1`

Critical path smoke tests for deployed services.

#### Test Coverage

1. **Root Endpoint**
   - Tests base URL accessibility
   - Validates HTTP response

2. **Health Endpoint**
   - Tests `/health` endpoint
   - Validates health status

3. **Version Endpoint**
   - Tests `/version` endpoint
   - Validates version information

4. **Dashboard Endpoint**
   - Tests `/api/dashboard` endpoint
   - Validates dashboard accessibility

5. **API Response Format**
   - Validates JSON response format
   - Checks required fields
   - Validates response structure

#### Usage

```powershell
.\scripts\deployment\smoke-tests.ps1 `
    -BaseUrl "https://api.codeflow.example.com" `
    -Timeout 30
```

#### Parameters

- `BaseUrl` (Required): Base URL for smoke tests
- `Timeout` (Optional): Timeout in seconds (default: 30)

---

## Integration Examples

### Example 1: Basic Deployment with Health Check

```powershell
.\scripts\deployment\deploy-with-rollback.ps1 `
    -DeploymentScript ".\deploy-codeflow-engine.ps1" `
    -ResourceGroup "nl-dev-codeflow-rg-san" `
    -HealthCheckUrl "https://dev-api.codeflow.example.com/health"
```

### Example 2: Full Deployment with All Features

```powershell
.\scripts\deployment\deploy-with-rollback.ps1 `
    -DeploymentScript ".\deploy-codeflow-engine.ps1" `
    -ResourceGroup "nl-prod-codeflow-rg-san" `
    -RollbackEnabled $true `
    -HealthCheckUrl "https://api.codeflow.example.com/health" `
    -HealthCheckTimeout 600 `
    -SmokeTestScript ".\scripts\deployment\smoke-tests.ps1"
```

### Example 3: Standalone Health Check

```powershell
.\scripts\deployment\health-check.ps1 `
    -HealthCheckUrl "https://api.codeflow.example.com" `
    -Retries 10 `
    -RetryDelay 5
```

### Example 4: Standalone Smoke Tests

```powershell
.\scripts\deployment\smoke-tests.ps1 `
    -BaseUrl "https://api.codeflow.example.com"
```

---

## Rollback Strategy

### Current Implementation

The rollback script currently:
1. Creates backup of resource group state
2. Detects deployment failures
3. Attempts to restore from backup
4. Provides manual rollback instructions

### Future Enhancements

1. **Full Rollback Implementation**
   - Automatic resource deletion
   - Previous version restoration
   - Configuration rollback

2. **Blue-Green Deployment**
   - Zero-downtime deployments
   - Traffic switching
   - Instant rollback

3. **Canary Deployment**
   - Gradual rollout
   - Traffic percentage control
   - Automatic promotion/rollback

---

## Best Practices

### Pre-Deployment

1. **Validate Environment**
   - Check Azure CLI is installed
   - Verify resource group exists
   - Validate deployment script

2. **Backup State**
   - Always enable rollback in production
   - Verify backup creation
   - Store backups securely

### During Deployment

1. **Monitor Progress**
   - Watch deployment logs
   - Monitor resource creation
   - Track deployment duration

2. **Handle Errors**
   - Capture all errors
   - Log error details
   - Trigger rollback on failure

### Post-Deployment

1. **Health Checks**
   - Wait for service startup
   - Verify all components healthy
   - Check database connectivity

2. **Smoke Tests**
   - Run critical path tests
   - Validate API responses
   - Verify functionality

---

## Troubleshooting

### Deployment Failures

**Issue:** Deployment script fails
- **Solution:** Check deployment logs
- **Solution:** Verify Azure permissions
- **Solution:** Check resource quotas

### Health Check Failures

**Issue:** Health check times out
- **Solution:** Increase timeout value
- **Solution:** Check service startup time
- **Solution:** Verify network connectivity

### Smoke Test Failures

**Issue:** Smoke tests fail
- **Solution:** Check endpoint URLs
- **Solution:** Verify service is running
- **Solution:** Check API response format

---

## Next Steps

1. ✅ **Deployment automation scripts created**
2. **Integrate into CI/CD workflows**
3. **Add more comprehensive smoke tests**
4. **Implement full rollback logic**
5. **Add deployment metrics tracking**

---

**Last Updated:** 2025-01-XX

