# CodeFlow Engine - Architecture Documentation

This document describes the architecture of the CodeFlow Engine, including system design, component interactions, and data flows.

---

## Table of Contents

- [System Overview](#system-overview)
- [High-Level Architecture](#high-level-architecture)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Deployment Architecture](#deployment-architecture)
- [Technology Stack](#technology-stack)

---

## System Overview

CodeFlow Engine is an AI-powered automation platform that analyzes GitHub pull requests, creates issues, and manages code quality through intelligent workflows.

### Core Capabilities

- **PR Analysis**: Multi-agent code review and quality analysis
- **Issue Management**: Automated issue creation in GitHub and Linear
- **Workflow Automation**: 20+ pre-built workflows for common tasks
- **AI Integration**: Support for multiple LLM providers (OpenAI, Anthropic, etc.)
- **Platform Detection**: Automatic detection of 25+ development platforms
- **Quality Gates**: Automated validation before merge

---

## High-Level Architecture

``` text
┌─────────────────────────────────────────────────────────────────┐
│                        External Systems                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ GitHub   │  │  Linear  │  │  Slack   │  │  Axolo   │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       │              │              │              │            │
│       └──────────────┴──────────────┴──────────────┘            │
│                          │                                        │
└──────────────────────────┼────────────────────────────────────────┘
                           │
                  ┌────────▼────────┐
                  │  CodeFlow Engine │
                  │   (FastAPI)     │
                  └────────┬────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐  ┌────────▼────────┐  ┌─────▼──────┐
│  PostgreSQL  │  │      Redis       │  │   Workers  │
│  (Database)  │  │     (Cache)      │  │ (Background)│
└──────────────┘  └──────────────────┘  └────────────┘
```

### Components

1. **API Server** (FastAPI): REST API and WebSocket server
2. **Engine Core**: Business logic and workflow orchestration
3. **Actions**: Modular action system for PR analysis, issue creation, etc.
4. **Integrations**: GitHub, Linear, Slack, Axolo connectors
5. **AI System**: LLM provider abstraction and multi-agent support
6. **Database**: PostgreSQL for persistent data
7. **Cache**: Redis for session data and temporary storage
8. **Workers**: Background task processors

---

## Component Architecture

### CodeFlow Engine Internal Structure

``` text
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Server     │  │  Dashboard   │  │ GitHub App   │     │
│  │   (Main)     │  │   Router      │  │  Routers     │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                  │
│                  ┌─────────▼─────────┐                        │
│                  │  CodeFlow Engine  │                        │
│                  │    (Core)         │                        │
│                  └─────────┬─────────┘                        │
└────────────────────────────┼──────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼──────┐  ┌──────────▼──────────┐  ┌─────▼──────┐
│   Actions    │  │   Integrations     │  │    AI      │
│  Registry    │  │    Registry        │  │  System     │
└───────┬──────┘  └──────────┬──────────┘  └─────┬──────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                  ┌──────────▼──────────┐
                  │   Data Layer         │
                  │  ┌──────┐ ┌──────┐ │
                  │  │  DB  │ │Redis │ │
                  │  └──────┘ └──────┘ │
                  └─────────────────────┘
```

### Core Components

#### 1. Server Layer

- **FastAPI Application**: Main HTTP/WebSocket server
- **Dashboard Router**: UI and dashboard API endpoints
- **GitHub App Routers**: Installation, webhooks, callbacks
- **Health Checker**: System health monitoring

#### 2. Engine Core

- **CodeFlowEngine**: Main orchestration class
- **Workflow System**: Workflow execution engine
- **Action Registry**: Action discovery and execution
- **Trigger System**: Event-driven triggers

#### 3. Actions System

Actions are modular, reusable components:

- **Quality Engine**: Code quality analysis
- **Issue Creator**: Automated issue creation
- **PR Analyzer**: Pull request analysis
- **Platform Detector**: Technology stack detection
- **AI Linting Fixer**: AI-powered code fixes
- **And 50+ more actions**

#### 4. Integration Layer

- **GitHub Integration**: GitHub API client, webhooks, app installation
- **Linear Integration**: Linear API client for issue management
- **Slack Integration**: Slack notifications via webhooks/bot
- **Axolo Integration**: Axolo workspace integration

#### 5. AI System

- **LLM Provider Abstraction**: Support for multiple providers
- **Multi-Agent System**: CrewAI and AutoGen integration
- **AI Learning System**: Memory and learning capabilities
- **Configurable Providers**: OpenAI, Anthropic, Mistral, Groq, etc.

---

## Data Flow

### GitHub Webhook Flow

``` text
GitHub
  │
  │ Webhook Event (PR opened, comment, etc.)
  ▼
CodeFlow Engine (Webhook Handler)
  │
  │ Parse event
  ▼
Trigger System
  │
  │ Match triggers
  ▼
Workflow Engine
  │
  │ Execute workflow
  ▼
Actions (PR Analysis, Issue Creation, etc.)
  │
  │ Results
  ▼
Database (Store results)
  │
  │ Notifications
  ▼
Integrations (Slack, Linear, etc.)
```

### PR Processing Flow

``` text
1. PR Opened/Updated
   │
   ▼
2. Webhook Received
   │
   ▼
3. Trigger Matched
   │
   ▼
4. Workflow Executed
   │
   ├─► Platform Detection
   ├─► Code Quality Analysis
   ├─► AI Review
   └─► Issue Creation (if needed)
   │
   ▼
5. Results Stored
   │
   ├─► Database (PostgreSQL)
   └─► Cache (Redis)
   │
   ▼
6. Notifications Sent
   │
   ├─► GitHub Comment
   ├─► Slack Notification
   └─► Linear Issue (if created)
```

### Issue Creation Flow

``` text
Quality Analysis
  │
  │ Issues Found
  ▼
Issue Classification
  │
  ├─► Security Issues → High Priority
  ├─► Performance Issues → Medium Priority
  └─► Code Style Issues → Low Priority
  │
  ▼
Issue Creation
  │
  ├─► GitHub Issues
  └─► Linear Tickets
  │
  ▼
Notifications
  │
  ├─► Slack
  └─► Axolo
```

---

## Deployment Architecture

### Production Deployment (Azure)

``` text
┌─────────────────────────────────────────────────────────┐
│                    Azure Cloud                           │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Azure Container Apps Environment         │  │
│  │                                                  │  │
│  │  ┌──────────────┐      ┌──────────────┐        │  │
│  │  │   Engine     │      │   Workers    │        │  │
│  │  │  (Primary)   │      │ (Background)  │        │  │
│  │  └──────┬──────┘      └──────┬───────┘        │  │
│  │         │                     │                 │  │
│  └─────────┼─────────────────────┼─────────────────┘  │
│            │                     │                      │
│  ┌─────────▼─────────┐  ┌───────▼────────┐           │
│  │  Azure Database   │  │  Azure Cache   │           │
│  │   for PostgreSQL   │  │   for Redis    │           │
│  └────────────────────┘  └────────────────┘           │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Azure Key Vault (Secrets)                 │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Application Insights (Monitoring)           │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Local Development

``` text
Developer Machine
  │
  ├─► VS Code Extension
  ├─► Desktop App
  └─► Website (Next.js)
        │
        │ API Calls
        ▼
  Docker Compose Stack
    │
    ├─► CodeFlow Engine (port 8000)
    ├─► PostgreSQL (port 5432)
    └─► Redis (port 6379)
```

---

## Technology Stack

### Backend

- **Python 3.12+**: Core language
- **FastAPI**: Web framework and API server
- **SQLAlchemy**: ORM for database access
- **Alembic**: Database migrations
- **Pydantic**: Data validation and settings
- **Poetry**: Dependency management

### AI & ML

- **OpenAI API**: GPT models
- **Anthropic API**: Claude models
- **CrewAI**: Multi-agent framework
- **AutoGen**: Agent orchestration
- **LangChain**: LLM abstraction (optional)

### Integrations

- **PyGithub**: GitHub API client
- **Linear API**: Linear issue management
- **Slack SDK**: Slack integration
- **Axolo SDK**: Axolo integration

### Infrastructure

- **PostgreSQL**: Primary database
- **Redis**: Caching and session storage
- **Docker**: Containerization
- **Azure Container Apps**: Production hosting
- **Azure Database**: Managed PostgreSQL
- **Azure Cache**: Managed Redis

### Frontend (Related Components)

- **VS Code Extension**: TypeScript/React
- **Desktop App**: Tauri (Rust + React)
- **Website**: Next.js (React + TypeScript)

---

## Component Interaction Diagrams

### Extension ↔ Engine Communication

``` text
VS Code Extension
  │
  │ HTTP/WebSocket
  ▼
CodeFlow Engine API
  │
  ├─► /api/v1/check (Quality Check)
  ├─► /api/v1/metrics (Get Metrics)
  ├─► /api/v1/history (Get History)
  └─► /ws (WebSocket for real-time updates)
  │
  ▼
Results Returned
  │
  ▼
Extension UI Updates
```

### Desktop ↔ Engine Communication

``` text
Desktop App (Tauri)
  │
  │ HTTP API
  ▼
CodeFlow Engine API
  │
  ├─► /api/v1/status
  ├─► /api/v1/check
  └─► /api/v1/config
  │
  ▼
Results Displayed in Desktop UI
```

### Website Integration

``` text
Website (Next.js)
  │
  │ API Calls (Server-side)
  ▼
CodeFlow Engine API
  │
  ├─► /api/v1/status (Public status)
  └─► /api/v1/docs (Documentation)
  │
  ▼
Content Rendered in Website
```

---

## Database Schema Overview

### Core Tables

- **workflows**: Workflow definitions
- **workflow_executions**: Execution history
- **issues**: Created issues tracking
- **quality_checks**: Quality check results
- **metrics**: Performance metrics
- **learning_memory**: AI learning data

### Relationships

```
Workflow ──┬──> WorkflowExecution
           │
           └──> Action

WorkflowExecution ──> QualityCheck ──> Issue

QualityCheck ──> Metrics
```

---

## Security Architecture

### Authentication & Authorization

- **GitHub App**: OAuth-based authentication
- **API Keys**: For programmatic access
- **JWT Tokens**: For session management
- **Rate Limiting**: Per-IP and per-user limits

### Secret Management

- **Azure Key Vault**: Production secrets
- **Environment Variables**: Development
- **No Hardcoded Secrets**: All secrets externalized

### Network Security

- **HTTPS Only**: All external communication
- **CORS Configuration**: Restricted origins
- **Firewall Rules**: Database access restrictions
- **SSL/TLS**: Database and Redis connections

---

## Scalability Considerations

### Horizontal Scaling

- **Stateless API**: Engine instances can scale horizontally
- **Load Balancing**: Azure Load Balancer
- **Auto-scaling**: Based on CPU/memory metrics
- **Worker Scaling**: Independent worker scaling

### Vertical Scaling

- **Database Scaling**: Azure Database scaling options
- **Redis Scaling**: Azure Cache scaling
- **Resource Limits**: Configurable per instance

### Caching Strategy

- **Redis Cache**: Session data, temporary results
- **Database Query Cache**: Frequently accessed data
- **CDN**: Static assets (if applicable)

---

## Monitoring & Observability

### Metrics

- **Application Insights**: Azure monitoring
- **Prometheus**: Custom metrics endpoint
- **Health Checks**: `/health` endpoint
- **Performance Metrics**: Processing times, success rates

### Logging

- **Structured Logging**: JSON format
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Centralized Logging**: Azure Log Analytics
- **Error Tracking**: Sentry integration

### Tracing

- **Distributed Tracing**: OpenTelemetry (optional)
- **Request Tracing**: Correlation IDs
- **Performance Profiling**: Built-in profiling

---

## Additional Resources

- [API Documentation](./API.md)
- [Deployment Guide](../deployment/DEPLOYMENT_GUIDE.md)
- [Configuration Guide](../config/CONFIGURATION.md)
- [Development Guide](../../README.md)

---

## Support

For questions or clarifications:
- GitHub Issues: [codeflow-engine/issues](https://github.com/JustAGhosT/codeflow-engine/issues)
- Documentation: [README.md](../../README.md)

