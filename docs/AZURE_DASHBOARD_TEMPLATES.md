# Azure Dashboard Templates

**Phase:** Wave 3, Phase 7  
**Status:** Implementation Guide  
**Purpose:** Dashboard templates and configuration for CodeFlow monitoring

---

## Overview

This guide provides dashboard templates and KQL queries for monitoring CodeFlow Engine in Azure Application Insights.

---

## Dashboard Templates

### Template 1: Application Overview

**Purpose:** High-level application health and performance

**Metrics to Include:**
- Request rate (requests/second)
- Response time (P50, P95, P99)
- Error rate (%)
- Availability (%)
- Active users

**KQL Queries:**

#### Request Rate
```kusto
requests
| where timestamp > ago(1h)
| summarize RequestRate = count() / 3600.0 by bin(timestamp, 1m)
| render timechart
```

#### Response Time
```kusto
requests
| where timestamp > ago(1h)
| summarize 
    P50 = percentile(duration, 50),
    P95 = percentile(duration, 95),
    P99 = percentile(duration, 99)
    by bin(timestamp, 5m)
| render timechart
```

#### Error Rate
```kusto
requests
| where timestamp > ago(1h)
| summarize 
    Total = count(),
    Errors = countif(success == false)
    by bin(timestamp, 5m)
| extend ErrorRate = (Errors * 100.0) / Total
| project timestamp, ErrorRate
| render timechart
```

---

### Template 2: Performance Monitoring

**Purpose:** Detailed performance metrics

**Metrics to Include:**
- Slow requests (>2s)
- Top slow endpoints
- Database query performance
- External API call performance
- Cache hit rates

**KQL Queries:**

#### Slow Requests
```kusto
requests
| where timestamp > ago(1h)
| where duration > 2000
| project timestamp, name, duration, url, user_Id
| order by duration desc
| take 20
```

#### Top Slow Endpoints
```kusto
requests
| where timestamp > ago(24h)
| where duration > 1000
| summarize 
    Count = count(),
    AvgDuration = avg(duration),
    MaxDuration = max(duration)
    by name
| order by AvgDuration desc
| take 10
```

#### Database Query Performance
```kusto
dependencies
| where timestamp > ago(1h)
| where type == "SQL"
| summarize 
    AvgDuration = avg(duration),
    Count = count()
    by name
| order by AvgDuration desc
```

---

### Template 3: Error Analysis

**Purpose:** Error tracking and analysis

**Metrics to Include:**
- Error count by type
- Exception stack traces
- Failed requests
- Error trends

**KQL Queries:**

#### Errors by Type
```kusto
exceptions
| where timestamp > ago(24h)
| summarize Count = count() by type
| order by Count desc
| take 10
```

#### Exception Details
```kusto
exceptions
| where timestamp > ago(1h)
| project timestamp, type, message, outerMessage, details
| order by timestamp desc
| take 50
```

#### Failed Requests
```kusto
requests
| where timestamp > ago(1h)
| where success == false
| project timestamp, name, url, resultCode, duration
| order by timestamp desc
```

---

### Template 4: Business Metrics

**Purpose:** CodeFlow-specific business metrics

**Metrics to Include:**
- PRs processed
- Issues created
- Workflows executed
- API calls made

**KQL Queries:**

#### PRs Processed
```kusto
customEvents
| where timestamp > ago(24h)
| where name == "PRProcessed"
| summarize Count = count() by bin(timestamp, 1h)
| render timechart
```

#### Workflows Executed
```kusto
customEvents
| where timestamp > ago(24h)
| where name == "WorkflowExecuted"
| summarize Count = count() by bin(timestamp, 1h)
| render timechart
```

---

## Dashboard Configuration Steps

### Step 1: Create Dashboard

1. Navigate to Azure Portal
2. Go to Application Insights → Dashboards
3. Click "New Dashboard"
4. Name: "CodeFlow Engine - Overview"

### Step 2: Add Tiles

1. Click "Edit"
2. Click "Add Tile"
3. Select "Custom" → "Query"
4. Paste KQL query
5. Configure visualization (timechart, table, etc.)
6. Set refresh interval

### Step 3: Organize Layout

1. Drag tiles to organize
2. Resize tiles as needed
3. Group related metrics
4. Save dashboard

---

## Alert Rule Templates

### High Error Rate Alert

```kusto
requests
| where timestamp > ago(5m)
| summarize 
    Total = count(),
    Errors = countif(success == false)
| extend ErrorRate = (Errors * 100.0) / Total
| where ErrorRate > 5
```

**Alert Condition:** ErrorRate > 5%  
**Window:** 5 minutes  
**Frequency:** 1 minute

### High Response Time Alert

```kusto
requests
| where timestamp > ago(5m)
| summarize AvgDuration = avg(duration)
| where AvgDuration > 2000
```

**Alert Condition:** Average duration > 2000ms  
**Window:** 5 minutes  
**Frequency:** 1 minute

### Low Availability Alert

```kusto
availabilityResults
| where timestamp > ago(15m)
| summarize Availability = avg(availabilityPercentage)
| where Availability < 99
```

**Alert Condition:** Availability < 99%  
**Window:** 15 minutes  
**Frequency:** 5 minutes

---

## Custom Metrics

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
measure = stats.stats.stats_recorder.new_measure_int("prs_processed")
view = stats.stats.view_manager.register_view(
    stats.stats.view.View(
        "prs_processed_view",
        measure,
        stats.stats.aggregation.CountAggregation()
    )
)

# Record metric
stats_recorder.new_measurement_map().measure_int_put(measure, 1).record()
```

---

## Dashboard Best Practices

### Organization

1. **Group Related Metrics**
   - Performance metrics together
   - Error metrics together
   - Business metrics together

2. **Use Consistent Time Ranges**
   - Standard: Last 24 hours
   - Detailed: Last 1 hour
   - Historical: Last 7 days

3. **Visualization Types**
   - Timecharts for trends
   - Tables for detailed data
   - Gauges for current values

### Performance

1. **Optimize Queries**
   - Use time filters
   - Limit result sets
   - Use aggregations

2. **Refresh Intervals**
   - Real-time: 1 minute (for critical metrics)
   - Standard: 5 minutes
   - Historical: 15 minutes

---

## Pre-built Dashboard JSON

### Export Dashboard

```bash
az portal dashboard export \
  --name "CodeFlow Engine - Overview" \
  --resource-group nl-prod-codeflow-rg-san \
  --output-file dashboard.json
```

### Import Dashboard

```bash
az portal dashboard import \
  --name "CodeFlow Engine - Overview" \
  --resource-group nl-prod-codeflow-rg-san \
  --input-file dashboard.json
```

---

## Next Steps

1. ✅ **Dashboard templates created**
2. **Create dashboards in Azure Portal**
3. **Configure alert rules**
4. **Set up custom metrics**
5. **Monitor and adjust**

---

**Last Updated:** 2025-01-XX

