# Metrics and Alerting Setup Guide

**Phase:** Wave 3, Phase 7  
**Status:** Implementation Guide  
**Purpose:** Guide for setting up metrics and alerting in Azure

---

## Overview

This guide provides step-by-step instructions for setting up Application Insights metrics and alerting for CodeFlow Engine.

---

## Prerequisites

- Azure subscription
- Azure CLI installed and configured
- Resource group created
- Application Insights created (or use setup script)

---

## Quick Setup

### Option 1: Automated Setup

```powershell
# Set up monitoring infrastructure
.\scripts\monitoring\setup-azure-monitoring.ps1 `
    -ResourceGroup "nl-prod-codeflow-rg-san" `
    -AppName "codeflow-engine"

# Create alert rules
.\scripts\monitoring\create-alert-rules.ps1 `
    -ResourceGroup "nl-prod-codeflow-rg-san" `
    -AppInsightsName "codeflow-engine-insights" `
    -ActionGroupName "codeflow-engine-alerts"
```

### Option 2: Manual Setup

Follow the detailed steps below.

---

## Step 1: Create Application Insights

### Using Azure CLI

```bash
az monitor app-insights component create \
  --app codeflow-engine-insights \
  --location southafricanorth \
  --resource-group nl-prod-codeflow-rg-san \
  --application-type web
```

### Using Azure Portal

1. Navigate to Azure Portal
2. Create new resource → Application Insights
3. Configure:
   - Name: `codeflow-engine-insights`
   - Resource Group: Your resource group
   - Location: Your region
   - Application Type: Web
4. Create and note the Instrumentation Key

---

## Step 2: Configure Application

### Environment Variables

Add to your Container App or environment:

```bash
APPINSIGHTS_INSTRUMENTATIONKEY=<your-instrumentation-key>
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=<your-instrumentation-key>
```

### Python Integration

The structured logging implementation already supports Application Insights. Ensure:

1. Install dependencies:
   ```bash
   pip install opencensus-ext-azure
   ```

2. Configure in settings:
   ```python
   settings.monitoring.log_analytics_workspace_id = "<workspace-id>"
   settings.monitoring.log_analytics_workspace_key = "<workspace-key>"
   ```

---

## Step 3: Create Action Group

### Using Azure CLI

```bash
az monitor action-group create \
  --name codeflow-engine-alerts \
  --resource-group nl-prod-codeflow-rg-san \
  --short-name codeflow \
  --email-receivers name=team-email email=team@example.com
```

### Using Azure Portal

1. Navigate to Monitor → Alerts → Action groups
2. Create action group
3. Configure:
   - Name: `codeflow-engine-alerts`
   - Short name: `codeflow`
   - Email notifications
   - SMS notifications (optional)
   - Webhook (optional)

---

## Step 4: Create Alert Rules

### Common Alert Rules

#### 1. High Error Rate

**Condition:** Error rate > 5%  
**Window:** 5 minutes  
**Frequency:** 1 minute

```bash
az monitor metrics alert create \
  --name codeflow-engine-high-error-rate \
  --resource-group nl-prod-codeflow-rg-san \
  --scopes <app-insights-resource-id> \
  --condition "avg requests/failed > 0.05" \
  --window-size PT5M \
  --evaluation-frequency PT1M \
  --action <action-group-id>
```

#### 2. High Response Time

**Condition:** Average response time > 2 seconds  
**Window:** 5 minutes  
**Frequency:** 1 minute

```bash
az monitor metrics alert create \
  --name codeflow-engine-high-response-time \
  --resource-group nl-prod-codeflow-rg-san \
  --scopes <app-insights-resource-id> \
  --condition "avg requests/duration > 2000" \
  --window-size PT5M \
  --evaluation-frequency PT1M \
  --action <action-group-id>
```

#### 3. Server Exceptions

**Condition:** Server exceptions > 0  
**Window:** 5 minutes  
**Frequency:** 1 minute

```bash
az monitor metrics alert create \
  --name codeflow-engine-server-exceptions \
  --resource-group nl-prod-codeflow-rg-san \
  --scopes <app-insights-resource-id> \
  --condition "count exceptions/server > 0" \
  --window-size PT5M \
  --evaluation-frequency PT1M \
  --action <action-group-id>
```

#### 4. Low Availability

**Condition:** Availability < 99%  
**Window:** 15 minutes  
**Frequency:** 5 minutes

```bash
az monitor metrics alert create \
  --name codeflow-engine-availability-low \
  --resource-group nl-prod-codeflow-rg-san \
  --scopes <app-insights-resource-id> \
  --condition "avg availabilityResults/availabilityPercentage < 99" \
  --window-size PT15M \
  --evaluation-frequency PT5M \
  --action <action-group-id>
```

---

## Step 5: Create Custom Metrics (Optional)

### Track Custom Metrics

```python
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import stats

# Create metrics exporter
exporter = metrics_exporter.new_metrics_exporter(
    connection_string=f"InstrumentationKey={instrumentation_key}"
)

# Track custom metric
stats_recorder = stats.stats.stats_recorder
measure = stats.stats.stats_recorder.new_measure_int("custom_metric")
view = stats.stats.view_manager.register_view(
    stats.stats.view.View(
        "custom_metric_view",
        measure,
        stats.stats.aggregation.CountAggregation()
    )
)
```

---

## Step 6: Configure Log Analytics (Optional)

### Create Log Analytics Workspace

```bash
az monitor log-analytics workspace create \
  --workspace-name codeflow-engine-logs \
  --location southafricanorth \
  --resource-group nl-prod-codeflow-rg-san
```

### Link to Application Insights

```bash
az monitor app-insights component update \
  --app codeflow-engine-insights \
  --resource-group nl-prod-codeflow-rg-san \
  --workspace <log-analytics-workspace-id>
```

---

## Monitoring Dashboards

### Create Dashboard

1. Navigate to Azure Portal → Dashboards
2. Create new dashboard
3. Add tiles:
   - Request rate
   - Response time
   - Error rate
   - Availability
   - Custom metrics

### KQL Queries

#### Request Performance

```kusto
requests
| where timestamp > ago(1h)
| summarize 
    avg(duration),
    p95(duration),
    p99(duration)
    by bin(timestamp, 5m)
```

#### Error Analysis

```kusto
exceptions
| where timestamp > ago(1h)
| summarize count() by type, bin(timestamp, 5m)
| order by count_ desc
```

#### Top Slow Requests

```kusto
requests
| where timestamp > ago(1h)
| where duration > 2000
| project timestamp, name, duration, url
| order by duration desc
| take 20
```

---

## Best Practices

### Alert Thresholds

1. **Start Conservative**
   - Set higher thresholds initially
   - Adjust based on actual behavior
   - Avoid alert fatigue

2. **Use Multiple Windows**
   - Short windows (5 min) for critical alerts
   - Longer windows (15 min) for availability

3. **Group Related Alerts**
   - Use action groups effectively
   - Route to appropriate teams

### Metric Collection

1. **Track Key Metrics**
   - Request rate
   - Response time
   - Error rate
   - Availability

2. **Custom Metrics**
   - Business metrics
   - Performance indicators
   - Resource usage

3. **Log Aggregation**
   - Structured logging
   - Correlation IDs
   - Context information

---

## Troubleshooting

### Alerts Not Firing

**Issue:** Alerts configured but not triggering

**Solutions:**
- Verify action group is configured
- Check alert rule conditions
- Verify metrics are being collected
- Check alert rule status in Azure Portal

### Metrics Not Appearing

**Issue:** Metrics not showing in Application Insights

**Solutions:**
- Verify instrumentation key is set
- Check application is sending telemetry
- Verify network connectivity
- Check Application Insights status

### High Alert Volume

**Issue:** Too many alerts firing

**Solutions:**
- Adjust thresholds
- Increase evaluation frequency
- Use alert suppression
- Group related alerts

---

## Next Steps

1. ✅ **Monitoring infrastructure set up**
2. ✅ **Alert rules configured**
3. **Monitor and adjust thresholds**
4. **Create custom dashboards**
5. **Set up log queries**
6. **Review and optimize alerts**

---

**Last Updated:** 2025-01-XX

