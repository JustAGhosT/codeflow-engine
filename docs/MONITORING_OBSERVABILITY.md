# CodeFlow Monitoring & Observability

This document describes the monitoring and observability strategy for CodeFlow.

---

## Overview

CodeFlow uses a comprehensive monitoring and observability stack:
- **Logging:** Azure Log Analytics (centralized)
- **Metrics:** Azure Monitor, Prometheus
- **Tracing:** OpenTelemetry (distributed tracing)
- **Alerting:** Azure Monitor Alerts
- **Dashboards:** Azure Monitor Dashboards, Grafana (optional)

---

## Logging Strategy

### Centralized Logging

#### Azure Log Analytics
- **Workspace:** Centralized log collection
- **Retention:** 90 days (configurable)
- **Archival:** Long-term storage for compliance

#### Log Collection
- **Application Logs:** Structured JSON logs
- **System Logs:** Container/system logs
- **Access Logs:** API access logs
- **Error Logs:** Error and exception logs

### Structured Logging

#### Log Format
```json
{
  "timestamp": "2025-01-XXT00:00:00Z",
  "level": "INFO",
  "service": "codeflow-engine",
  "component": "api",
  "message": "Request processed",
  "request_id": "abc123",
  "user_id": "user-123",
  "duration_ms": 150,
  "status_code": 200
}
```

#### Log Levels
- **DEBUG:** Detailed diagnostic information
- **INFO:** General informational messages
- **WARNING:** Warning messages
- **ERROR:** Error messages
- **CRITICAL:** Critical errors requiring immediate attention

### Log Aggregation

#### Collection Points
1. **Application Logs**
   - Direct to Log Analytics
   - Via Application Insights
   - Via log forwarder

2. **Container Logs**
   - Docker container logs
   - Kubernetes pod logs
   - Azure Container Apps logs

3. **Infrastructure Logs**
   - Azure resource logs
   - Network logs
   - Security logs

---

## Metrics & Monitoring

### Application Metrics

#### Key Metrics
- **Request Rate:** Requests per second
- **Response Time:** P50, P95, P99 latencies
- **Error Rate:** Errors per second
- **Throughput:** Requests processed per second
- **Active Connections:** Current active connections

#### Business Metrics
- **PRs Processed:** Pull requests processed
- **Issues Created:** Issues created
- **Workflows Executed:** Workflows executed
- **API Calls:** API calls made
- **User Activity:** Active users

### Infrastructure Metrics

#### System Metrics
- **CPU Usage:** CPU utilization
- **Memory Usage:** Memory consumption
- **Disk I/O:** Disk read/write operations
- **Network I/O:** Network traffic
- **Container Metrics:** Container resource usage

#### Azure Metrics
- **Container App Metrics:** Replicas, CPU, memory
- **Database Metrics:** Connections, queries, latency
- **Redis Metrics:** Cache hits, memory usage
- **Storage Metrics:** Storage usage, I/O

### Monitoring Dashboards

#### Azure Monitor Dashboards
- **System Overview:** Overall system health
- **Service Health:** Per-service metrics
- **Performance:** Performance metrics
- **Errors:** Error tracking
- **Business Metrics:** Business KPIs

#### Grafana Dashboards (Optional)
- **Application Metrics:** Detailed application metrics
- **Infrastructure Metrics:** System metrics
- **Custom Dashboards:** Custom visualizations

---

## Distributed Tracing

### OpenTelemetry Integration

#### Trace Collection
- **Instrumentation:** Automatic and manual
- **Trace Export:** To Azure Application Insights
- **Trace Correlation:** Request correlation IDs

#### Trace Components
- **Spans:** Individual operations
- **Traces:** Complete request flows
- **Context Propagation:** Trace context across services

### Trace Visualization

#### Application Insights
- **Transaction Search:** Search traces
- **Performance Analysis:** Performance insights
- **Dependency Map:** Service dependencies

---

## Alerting

### Alert Rules

#### Critical Alerts
- **Service Down:** Service unavailable
- **High Error Rate:** Error rate > 5%
- **High Latency:** P95 latency > 5s
- **Resource Exhaustion:** CPU/Memory > 90%

#### Warning Alerts
- **Elevated Error Rate:** Error rate > 1%
- **Increased Latency:** P95 latency > 2s
- **Resource Usage:** CPU/Memory > 70%

### Notification Channels

#### Email
- **Critical Alerts:** Immediate email
- **Warning Alerts:** Daily digest

#### Slack
- **Critical Alerts:** Immediate notification
- **Warning Alerts:** Channel notification

#### PagerDuty (Optional)
- **Critical Alerts:** On-call escalation
- **Incident Management:** Incident tracking

### Alert Escalation

#### Escalation Policy
1. **Level 1:** Primary on-call (5 minutes)
2. **Level 2:** Secondary on-call (15 minutes)
3. **Level 3:** Team lead (30 minutes)
4. **Level 4:** Management (1 hour)

---

## Health Checks

### Health Check Endpoints

#### Application Health
```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.2.0",
  "uptime_seconds": 3600,
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "external_apis": "healthy"
  }
}
```

#### Readiness Check
```
GET /health/ready
```

#### Liveness Check
```
GET /health/live
```

### Health Check Monitoring

#### Uptime Monitoring
- **Check Frequency:** Every 30 seconds
- **Timeout:** 5 seconds
- **Retries:** 3 attempts
- **Alert:** If unhealthy for > 2 minutes

---

## Error Tracking

### Sentry Integration

#### Error Collection
- **Automatic:** Unhandled exceptions
- **Manual:** Custom error reporting
- **Context:** Request context, user info

#### Error Analysis
- **Error Grouping:** Similar errors grouped
- **Error Trends:** Error frequency over time
- **Error Details:** Stack traces, context

---

## Performance Monitoring

### Application Performance Monitoring (APM)

#### Performance Metrics
- **Response Time:** End-to-end response time
- **Throughput:** Requests per second
- **Error Rate:** Percentage of errors
- **Availability:** Uptime percentage

#### Performance Analysis
- **Slow Queries:** Database query analysis
- **Bottleneck Identification:** Performance bottlenecks
- **Resource Usage:** Resource consumption

---

## Log Retention Policies

### Retention Periods

#### Application Logs
- **Hot Storage:** 30 days
- **Warm Storage:** 90 days
- **Cold Storage:** 1 year (archived)

#### Audit Logs
- **Retention:** 7 years (compliance)

#### Access Logs
- **Retention:** 90 days

### Log Archival

#### Archival Process
- **Automated:** Daily archival
- **Storage:** Azure Blob Storage
- **Format:** Compressed JSON
- **Retrieval:** On-demand retrieval

---

## Observability Best Practices

### Do's

✅ **Do:**
- Use structured logging
- Include correlation IDs
- Log at appropriate levels
- Monitor key metrics
- Set up meaningful alerts
- Create useful dashboards
- Track business metrics

### Don'ts

❌ **Don't:**
- Log sensitive information
- Over-log (too verbose)
- Under-log (missing critical info)
- Ignore alerts
- Create alert fatigue
- Skip health checks

---

## Implementation Guide

### Step 1: Set Up Logging

1. **Create Log Analytics Workspace**
   ```bash
   az monitor log-analytics workspace create \
     --resource-group codeflow-rg \
     --workspace-name codeflow-logs
   ```

2. **Configure Application Logging**
   - Add logging configuration
   - Set up log forwarding
   - Configure log levels

### Step 2: Set Up Metrics

1. **Enable Application Insights**
   ```bash
   az monitor app-insights component create \
     --app codeflow-engine \
     --location eastus \
     --resource-group codeflow-rg
   ```

2. **Configure Metrics Collection**
   - Add metrics instrumentation
   - Set up custom metrics
   - Configure metric export

### Step 3: Set Up Alerting

1. **Create Alert Rules**
   - Define alert conditions
   - Set thresholds
   - Configure notifications

2. **Set Up Notification Channels**
   - Configure email
   - Configure Slack
   - Set up escalation

### Step 4: Create Dashboards

1. **Create Azure Monitor Dashboards**
   - Add key metrics
   - Create visualizations
   - Set up refresh intervals

2. **Create Grafana Dashboards** (Optional)
   - Import dashboards
   - Customize visualizations
   - Set up alerts

---

## Additional Resources

- [Azure Monitor Documentation](https://docs.microsoft.com/azure/azure-monitor/)
- [Application Insights Documentation](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Sentry Documentation](https://docs.sentry.io/)

---

## Support

For monitoring questions:
- GitHub Issues: [codeflow-orchestration/issues](https://github.com/JustAGhosT/codeflow-orchestration/issues)
- Documentation: This document

