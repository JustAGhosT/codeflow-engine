# CodeFlow Engine - Quick Start Deployment Guide

**Time:** 5 minutes  
**Difficulty:** Beginner

This guide will get you up and running with CodeFlow Engine in 5 minutes using Docker.

---

## Prerequisites

- Docker and Docker Compose installed
- GitHub Personal Access Token (optional, for GitHub integration)
- OpenAI API key (optional, for AI features)

---

## Quick Start (5 Minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/JustAGhosT/codeflow-engine.git
cd codeflow-engine
```

### Step 2: Create Environment File

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Required
GITHUB_TOKEN=your_github_token_here

# Optional - for AI features
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Database (defaults work for local)
DATABASE_URL=postgresql://codeflow:password@localhost:5432/codeflow
REDIS_URL=redis://localhost:6379/0
```

### Step 3: Start with Docker Compose

```bash
docker-compose up -d
```

This will start:
- CodeFlow Engine (port 8000)
- PostgreSQL database (port 5432)
- Redis cache (port 6379)

### Step 4: Verify Installation

Check the health endpoint:

```bash
curl http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "version": "1.0.1",
  "database": "connected",
  "redis": "connected"
}
```

### Step 5: Access the Dashboard

Open your browser to:
```
http://localhost:8000/dashboard
```

---

## Next Steps

- **Full Deployment:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **Azure Deployment:** See [AZURE_DEPLOYMENT.md](./AZURE_DEPLOYMENT.md)
- **Kubernetes Deployment:** See [KUBERNETES_DEPLOYMENT.md](./KUBERNETES_DEPLOYMENT.md)
- **Configuration:** See [CONFIGURATION.md](../config/CONFIGURATION.md)

---

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, change it in `docker-compose.yml`:

```yaml
services:
  codeflow-engine:
    ports:
      - "8001:8000"  # Change 8001 to any available port
```

### Database Connection Error

Make sure PostgreSQL is running:

```bash
docker-compose ps
```

If not running, restart:

```bash
docker-compose restart postgres
```

### Health Check Fails

Check the logs:

```bash
docker-compose logs codeflow-engine
```

Common issues:
- Missing environment variables
- Database not ready (wait 30 seconds)
- Invalid GitHub token

---

## Stopping the Services

```bash
docker-compose down
```

To remove all data:

```bash
docker-compose down -v
```

---

## What's Next?

- Configure GitHub App integration
- Set up Linear/Slack integrations
- Customize workflows
- Deploy to production

See the [full documentation](../README.md) for more details.

