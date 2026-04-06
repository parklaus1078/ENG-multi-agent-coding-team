# Multi-Agent Coding Team API

FastAPI-based REST API + Discord integration + Web dashboard

---

## 🚀 Quick Start

### 1. Installation

```bash
# Install requirements
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file to set DISCORD_WEBHOOK_URL, etc.
```

### 2. Run API Server

```bash
# Development mode (auto-reload)
uvicorn api.main:app --reload --port 8000

# Or run directly
python -m api.main
```

### 3. Access Web Dashboard

```
http://localhost:8000
```

### 4. Check API Documentation

```
Swagger UI: http://localhost:8000/api/docs
ReDoc: http://localhost:8000/api/redoc
```

---

## 📡 API Endpoints

### Agents

#### Project Planner Agent
```bash
curl -X POST http://localhost:8000/api/agents/project-planner \
  -H "Content-Type: application/json" \
  -d '{
    "project": "my-todo-app",
    "requirements_text": "Develop a web-based TODO app..."
  }'
```

#### PM Agent
```bash
curl -X POST http://localhost:8000/api/agents/pm \
  -H "Content-Type: application/json" \
  -d '{
    "project": "my-todo-app",
    "ticket": "TODO-001"
  }'
```

####Coding Agent
```bash
curl -X POST http://localhost:8000/api/agents/coding \
  -H "Content-Type: application/json" \
  -d '{
    "project": "my-todo-app",
    "ticket": "TODO-001"
  }'
```

#### QA Agent
```bash
curl -X POST http://localhost:8000/api/agents/qa \
  -H "Content-Type: application/json" \
  -d '{
    "project": "my-todo-app",
    "ticket": "TODO-001"
  }'
```

#### Stack Initializer Agent
```bash
curl -X POST http://localhost:8000/api/agents/stack-initializer \
  -H "Content-Type: application/json" \
  -d '{
    "project": "my-todo-app"
  }'
```

#### List Agents
```bash
curl http://localhost:8000/api/agents/list
```

### Skills

```bash
# Run validate-spec skill
curl -X POST http://localhost:8000/api/skills/validate-spec \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "PLAN-001",
    "project": "my-cli-tool",
    "auto_fix": true
  }'

# Run commit skill
curl -X POST http://localhost:8000/api/skills/commit \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "PLAN-001",
    "project": "my-cli-tool"
  }'

# Run test-runner skill
curl -X POST http://localhost:8000/api/skills/test-runner \
  -H "Content-Type: application/json" \
  -d '{
    "project": "my-cli-tool",
    "args": {"coverage": true}
  }'

# List skills
curl http://localhost:8000/api/skills/list
```

### Pipeline

```bash
# Run full pipeline
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "PLAN-001",
    "project": "my-cli-tool",
    "resume": false
  }'

# Get pipeline status
curl http://localhost:8000/api/pipeline/status/PLAN-001

# List pipelines
curl http://localhost:8000/api/pipeline/list

# Cancel pipeline
curl -X POST http://localhost:8000/api/pipeline/cancel/PLAN-001

# Get logs
curl http://localhost:8000/api/pipeline/logs/PLAN-001

# Get statistics
curl http://localhost:8000/api/pipeline/stats
```

### Webhooks

```bash
# GitHub Webhook (automatically called by GitHub)
POST /api/webhooks/github
Headers:
  X-GitHub-Event: pull_request
  X-Hub-Signature-256: sha256=...

# Discord Command (called by Discord Bot)
POST /api/webhooks/discord
{
  "command": "run",
  "args": ["PLAN-001"],
  "user_id": "123456789",
  "channel_id": "987654321"
}
```

---

## 🔵 Discord Integration

### 1. Create Webhook URL

1. Discord Server Settings → Integrations → Webhooks
2. Create new webhook
3. Copy webhook URL

### 2. Set Environment Variable

```bash
export DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
```

### 3. Receive Notifications

Automatic Discord notifications when pipeline runs:

- 🚀 Pipeline Started
- 🤖 Agent Started/Completed
- ✅ Tests Passed / ❌ Tests Failed
- 🚀 Deployed to Production
- ⚠️ PR Review Issues

### Discord Notification Example

```
🚀 Pipeline Started
━━━━━━━━━━━━━━━━━━━━
Ticket: PLAN-001
Project: my-cli-tool
━━━━━━━━━━━━━━━━━━━━
Mode: New | Status: 🟢 Running
```

---

## 🔗 GitHub Webhook Setup

### 1. Repository Settings

1. GitHub Repository → Settings → Webhooks
2. Add webhook
3. Payload URL: `https://your-domain.com/api/webhooks/github`
4. Content type: `application/json`
5. Secret: (your SECRET)
6. Events: Pull requests, Issues

### 2. Set Environment Variable

```bash
export GITHUB_WEBHOOK_SECRET=your-secret
```

### 3. Automatic Actions

- **PR created/updated** → review-pr skill automatically runs
- **Issue created** → Ticket automatically created (to be implemented)

---

## 🏗️ Architecture

```
api/
├── main.py                 # FastAPI app
├── config.py               # Configuration
├── models/
│   ├── request.py          # Request models
│   └── response.py         # Response models
├── routers/
│   ├── agents.py           # /api/agents/*
│   ├── skills.py           # /api/skills/*
│   ├── pipeline.py         # /api/pipeline/*
│   └── webhooks.py         # /api/webhooks/*
└── services/
    ├── agent_service.py    # Agent execution
    ├── skill_service.py    # Skill execution
    ├── pipeline_service.py # Pipeline management
    ├── discord_service.py  # Discord integration
    └── webhook_service.py  # Webhook handling
```

---

## 📊 Response Examples

### Agent Run Response

```json
{
  "success": true,
  "agent": "pm",
  "ticket": "PLAN-001",
  "session_id": "abc123",
  "message_count": 5,
  "duration_seconds": 45.2,
  "output": "Specification generation completed",
  "error": null
}
```

### Pipeline Status Response

```json
{
  "ticket": "PLAN-001",
  "status": "running",
  "current_step": "coding",
  "progress": 60,
  "started_at": "2026-03-19T10:00:00Z",
  "completed_at": null,
  "steps": [
    {"name": "pm", "status": "success", "duration": 45.2},
    {"name": "validate-spec", "status": "success", "duration": 2.1},
    {"name": "coding", "status": "running", "duration": null}
  ],
  "error": null
}
```

---

## 🔧 Development

### Running Tests

```bash
pytest api/tests/
```

### Code Style

```bash
# Format
black api/

# Lint
pylint api/
```

---

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_WEBHOOK_URL` | Yes | Discord webhook URL |
| `GITHUB_WEBHOOK_SECRET` | No | GitHub webhook secret |
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key |
| `API_HOST` | No | API host (default: 0.0.0.0) |
| `API_PORT` | No | API port (default: 8000) |

---

## 🚨 Error Handling

All endpoints return errors in the following format:

```json
{
  "detail": "Error message"
}
```

HTTP Status Codes:
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Discord Webhooks Guide](https://discord.com/developers/docs/resources/webhook)
- [GitHub Webhooks Guide](https://docs.github.com/en/webhooks)
