# CodeFlow Engine - Documentation Index

Welcome to the CodeFlow Engine documentation! This index helps you find the documentation you need.

---

## Quick Links

### 🚀 Getting Started
- [Quick Start Guide](./deployment/QUICK_START.md) - Get running in 5 minutes
- [Full Deployment Guide](./deployment/DEPLOYMENT_GUIDE.md) - Comprehensive deployment instructions
- [Environment Variables Reference](./deployment/ENVIRONMENT_VARIABLES.md) - All configuration options

### 📚 Deployment Guides

#### Local Development
- [Quick Start (Docker)](./deployment/QUICK_START.md) - 5-minute Docker setup

#### Cloud Deployment
- [Azure Deployment](./deployment/AZURE_DEPLOYMENT.md) - Azure Container Apps
- [Kubernetes Deployment](./deployment/KUBERNETES_DEPLOYMENT.md) - AKS, GKE, EKS

#### Full Stack
- [Full Stack Deployment](../../codeflow-orchestration/docs/FULL_STACK_DEPLOYMENT.md) - Complete system deployment

### 🏗️ Architecture

- [System Architecture](./architecture/ARCHITECTURE.md) - Complete system design
  - High-level architecture
  - Component interactions
  - Data flows
  - Deployment architecture
  - Technology stack

### 🔌 API Reference

- [API Documentation](./api/API.md) - Complete API reference
  - REST API endpoints
  - WebSocket API
  - Authentication
  - Rate limiting
  - Error codes
  - Request/response examples

### 🧪 Testing

- [Testing Strategy](./testing/TESTING_STRATEGY.md) - Testing philosophy and structure
- [Coverage Guide](./testing/COVERAGE_GUIDE.md) - Measuring and improving coverage
- [Coverage Improvement Plan](./testing/COVERAGE_IMPROVEMENT_PLAN.md) - Plan to reach 80%+ coverage
- [Integration Testing](./testing/INTEGRATION_TESTING.md) - Integration test guide
- [E2E Testing](./testing/E2E_TESTING.md) - End-to-end test guide

---

## Documentation by Role

### For Developers

**Getting Started:**
1. [Quick Start Guide](./deployment/QUICK_START.md)
2. [Environment Variables](./deployment/ENVIRONMENT_VARIABLES.md)
3. [Architecture Overview](./architecture/ARCHITECTURE.md)

**Development:**
- [Testing Strategy](./testing/TESTING_STRATEGY.md)
- [Coverage Guide](./testing/COVERAGE_GUIDE.md)
- [API Documentation](./api/API.md)

### For DevOps Engineers

**Deployment:**
1. [Full Deployment Guide](./deployment/DEPLOYMENT_GUIDE.md)
2. [Azure Deployment](./deployment/AZURE_DEPLOYMENT.md)
3. [Kubernetes Deployment](./deployment/KUBERNETES_DEPLOYMENT.md)
4. [Full Stack Deployment](../../codeflow-orchestration/docs/FULL_STACK_DEPLOYMENT.md)

**Configuration:**
- [Environment Variables](./deployment/ENVIRONMENT_VARIABLES.md)

### For Contributors

**Getting Started:**
1. [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contribution guidelines
2. [Testing Strategy](./testing/TESTING_STRATEGY.md)
3. [Coverage Improvement Plan](./testing/COVERAGE_IMPROVEMENT_PLAN.md)

**Writing Tests:**
- [Testing Strategy](./testing/TESTING_STRATEGY.md)
- [Integration Testing](./testing/INTEGRATION_TESTING.md)
- [E2E Testing](./testing/E2E_TESTING.md)

### For API Consumers

**API Reference:**
1. [API Documentation](./api/API.md) - Complete API reference
2. [OpenAPI/Swagger](../docs) - Available at `/docs` endpoint

**Integration:**
- [Architecture](./architecture/ARCHITECTURE.md) - System design
- [Full Stack Deployment](../../codeflow-orchestration/docs/FULL_STACK_DEPLOYMENT.md)

---

## Documentation Structure

```
docs/
├── README.md                    # This file
├── deployment/                  # Deployment guides
│   ├── QUICK_START.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── AZURE_DEPLOYMENT.md
│   ├── KUBERNETES_DEPLOYMENT.md
│   └── ENVIRONMENT_VARIABLES.md
├── architecture/                # Architecture documentation
│   └── ARCHITECTURE.md
├── api/                         # API documentation
│   └── API.md
└── testing/                     # Testing documentation
    ├── TESTING_STRATEGY.md
    ├── COVERAGE_GUIDE.md
    ├── COVERAGE_IMPROVEMENT_PLAN.md
    ├── INTEGRATION_TESTING.md
    └── E2E_TESTING.md
```

---

## Common Tasks

### I want to...

**...deploy CodeFlow Engine:**
→ Start with [Quick Start](./deployment/QUICK_START.md) or [Full Deployment Guide](./deployment/DEPLOYMENT_GUIDE.md)

**...configure environment variables:**
→ See [Environment Variables Reference](./deployment/ENVIRONMENT_VARIABLES.md)

**...understand the architecture:**
→ Read [Architecture Documentation](./architecture/ARCHITECTURE.md)

**...use the API:**
→ See [API Documentation](./api/API.md)

**...write tests:**
→ Start with [Testing Strategy](./testing/TESTING_STRATEGY.md)

**...improve test coverage:**
→ Follow [Coverage Improvement Plan](./testing/COVERAGE_IMPROVEMENT_PLAN.md)

**...deploy to Azure:**
→ See [Azure Deployment Guide](./deployment/AZURE_DEPLOYMENT.md)

**...deploy to Kubernetes:**
→ See [Kubernetes Deployment Guide](./deployment/KUBERNETES_DEPLOYMENT.md)

**...set up local development:**
→ Use [Quick Start](./deployment/QUICK_START.md) with Docker Compose

---

## Additional Resources

- **Main README:** [../../README.md](../../README.md)
- **Contributing:** [../../CONTRIBUTING.md](../../CONTRIBUTING.md)
- **Full Stack Guide:** [../../codeflow-orchestration/docs/FULL_STACK_DEPLOYMENT.md](../../codeflow-orchestration/docs/FULL_STACK_DEPLOYMENT.md)
- **GitHub Issues:** [codeflow-engine/issues](https://github.com/JustAGhosT/codeflow-engine/issues)

---

## Support

For questions or help:
- GitHub Issues: [codeflow-engine/issues](https://github.com/JustAGhosT/codeflow-engine/issues)
- Documentation: This index and linked guides
- API Docs: Available at `/docs` endpoint when server is running

---

**Last Updated:** 2025-01-XX
