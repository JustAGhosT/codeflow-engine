# CodeFlow Engine - Logging Guide

This guide describes how to implement structured logging in CodeFlow Engine.

---

## Overview

CodeFlow Engine uses structured logging with JSON format for centralized log collection and analysis.

---

## Logging Configuration

### Environment Variables

```bash
# Log level
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Log format
LOG_FORMAT=json  # json, text

# Log output
LOG_OUTPUT=stdout  # stdout, file, both

# Log file (if using file output)
LOG_FILE=/app/logs/codeflow.log

# Azure Log Analytics (optional)
LOG_ANALYTICS_WORKSPACE_ID=your-workspace-id
LOG_ANALYTICS_WORKSPACE_KEY=your-workspace-key
```

### Python Logging Configuration

```python
import logging
import json
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": "codeflow-engine",
            "component": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

# Configure logger
logger = logging.getLogger("codeflow_engine")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(StructuredFormatter())
logger.addHandler(handler)
```

---

## Logging Best Practices

### Use Appropriate Log Levels

```python
# DEBUG: Detailed diagnostic information
logger.debug("Processing request", extra={"request_id": request_id})

# INFO: General informational messages
logger.info("Request processed successfully", extra={
    "request_id": request_id,
    "duration_ms": duration
})

# WARNING: Warning messages
logger.warning("Rate limit approaching", extra={
    "request_id": request_id,
    "rate_limit": 90
})

# ERROR: Error messages
logger.error("Failed to process request", extra={
    "request_id": request_id,
    "error": str(error)
}, exc_info=True)

# CRITICAL: Critical errors
logger.critical("Service unavailable", extra={
    "error": str(error)
}, exc_info=True)
```

### Include Context

```python
# Good: Include context
logger.info("PR processed", extra={
    "request_id": request_id,
    "pr_number": pr_number,
    "repository": repository,
    "duration_ms": duration
})

# Bad: Missing context
logger.info("PR processed")
```

### Use Correlation IDs

```python
import uuid

# Generate correlation ID at request start
request_id = str(uuid.uuid4())

# Include in all log messages
logger.info("Processing request", extra={"request_id": request_id})
logger.info("Calling external API", extra={"request_id": request_id})
logger.info("Request completed", extra={"request_id": request_id})
```

### Don't Log Sensitive Information

```python
# Bad: Logging sensitive data
logger.info("User logged in", extra={
    "username": username,
    "password": password  # NEVER log passwords!
})

# Good: Logging safe information
logger.info("User logged in", extra={
    "user_id": user_id,
    "username": username  # Safe to log
})
```

---

## Logging Examples

### API Request Logging

```python
import time
from fastapi import Request
from fastapi.logger import logger

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    logger.info("Request started", extra={
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host
    })
    
    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        
        logger.info("Request completed", extra={
            "request_id": request_id,
            "status_code": response.status_code,
            "duration_ms": duration_ms
        })
        
        return response
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error("Request failed", extra={
            "request_id": request_id,
            "error": str(e),
            "duration_ms": duration_ms
        }, exc_info=True)
        raise
```

### Database Query Logging

```python
logger.debug("Executing database query", extra={
    "request_id": request_id,
    "query": query,
    "parameters": parameters
})

try:
    result = await db.execute(query, parameters)
    logger.debug("Query executed successfully", extra={
        "request_id": request_id,
        "rows_affected": result.rowcount
    })
except Exception as e:
    logger.error("Query failed", extra={
        "request_id": request_id,
        "query": query,
        "error": str(e)
    }, exc_info=True)
    raise
```

### External API Call Logging

```python
logger.info("Calling external API", extra={
    "request_id": request_id,
    "api": "github",
    "endpoint": endpoint
})

start_time = time.time()
try:
    response = await github_client.get(endpoint)
    duration_ms = (time.time() - start_time) * 1000
    
    logger.info("External API call successful", extra={
        "request_id": request_id,
        "api": "github",
        "endpoint": endpoint,
        "status_code": response.status_code,
        "duration_ms": duration_ms
    })
except Exception as e:
    duration_ms = (time.time() - start_time) * 1000
    logger.error("External API call failed", extra={
        "request_id": request_id,
        "api": "github",
        "endpoint": endpoint,
        "error": str(e),
        "duration_ms": duration_ms
    }, exc_info=True)
    raise
```

---

## Log Aggregation

### Azure Log Analytics

#### Send Logs to Log Analytics

```python
from azure.monitor.opencensus import AzureLogHandler

# Configure Azure Log Analytics handler
log_handler = AzureLogHandler(
    connection_string=f"InstrumentationKey={workspace_key}"
)
logger.addHandler(log_handler)
```

### Application Insights

#### Send Logs to Application Insights

```python
from opencensus.ext.azure.log_exporter import AzureLogHandler

# Configure Application Insights handler
log_handler = AzureLogHandler(
    connection_string=f"InstrumentationKey={app_insights_key}"
)
logger.addHandler(log_handler)
```

---

## Log Queries

### Azure Log Analytics Queries

#### Find Errors
```kusto
codeflow_engine_CL
| where Level == "ERROR"
| project Timestamp, Message, RequestId, Exception
| order by Timestamp desc
```

#### Request Performance
```kusto
codeflow_engine_CL
| where Message contains "Request completed"
| extend Duration = todouble(DurationMs)
| summarize avg(Duration), p95(Duration), p99(Duration) by bin(Timestamp, 1h)
```

#### Error Rate
```kusto
codeflow_engine_CL
| where Level == "ERROR"
| summarize ErrorCount = count() by bin(Timestamp, 1h)
```

---

## Additional Resources

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Azure Log Analytics Documentation](https://docs.microsoft.com/azure/azure-monitor/logs/)
- [Application Insights Documentation](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)

---

## Support

For logging questions:
- GitHub Issues: [codeflow-engine/issues](https://github.com/JustAGhosT/codeflow-engine/issues)
- Documentation: This guide

