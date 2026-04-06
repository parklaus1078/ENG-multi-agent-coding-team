#!/usr/bin/env python3
"""
Multi-Agent Coding Team API
FastAPI-based REST API

Usage:
    uvicorn api.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
import uvicorn

from api.routers import agents, skills, pipeline, webhooks, projects
from api.services.discord_service import DiscordService

# Initialize Discord service
discord = DiscordService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle (startup/shutdown)"""
    # Startup
    print("🚀 Multi-Agent Coding Team API Started")
    await discord.send_notification(
        title="🚀 API Server Started",
        description="Multi-Agent Coding Team API has started.",
        color=3066993  # Green
    )

    yield

    # Shutdown
    print("👋 Multi-Agent Coding Team API Stopped")
    await discord.send_notification(
        title="👋 API Server Stopped",
        description="Multi-Agent Coding Team API has stopped.",
        color=15158332  # Red
    )


# Create FastAPI app
app = FastAPI(
    title="Multi-Agent Coding Team API",
    description="AI Agent-based Automated Development Platform",
    version="0.0.4",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, allow only specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(pipeline.router, prefix="/api/pipeline", tags=["Pipeline"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])

# Static files (web dashboard)
web_dir = Path(__file__).parent.parent / "web"
if web_dir.exists():
    app.mount("/static", StaticFiles(directory=str(web_dir / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Web dashboard main page"""
    html_file = web_dir / "index.html"

    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()

    # If dashboard HTML doesn't exist, return simple guide page
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multi-Agent Coding Team</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 { color: #333; }
            .status { color: #22c55e; font-weight: bold; }
            .link {
                display: inline-block;
                margin: 10px 10px 10px 0;
                padding: 10px 20px;
                background: #3b82f6;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }
            .link:hover { background: #2563eb; }
            code {
                background: #f3f4f6;
                padding: 2px 6px;
                border-radius: 3px;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Multi-Agent Coding Team</h1>
            <p class="status">✅ API Server execution</p>

            <h2>📚 API Documentation</h2>
            <a href="/api/docs" class="link">Swagger UI</a>
            <a href="/api/redoc" class="link">ReDoc</a>

            <h2>🔗 Quick Start</h2>
            <h3>1. Run Pipeline</h3>
            <pre><code>curl -X POST http://localhost:8000/api/pipeline/run \\
  -H "Content-Type: application/json" \\
  -d '{"ticket": "PLAN-001", "project": "my-project"}'</code></pre>

            <h3>2. Check Status</h3>
            <pre><code>curl http://localhost:8000/api/pipeline/status/PLAN-001</code></pre>

            <h3>3. Run Agent</h3>
            <pre><code>curl -X POST http://localhost:8000/api/agents/pm \\
  -H "Content-Type: application/json" \\
  -d '{"ticket": "PLAN-001", "project": "my-project"}'</code></pre>

            <h2>🎯 Available Endpoints</h2>
            <ul>
                <li><code>POST /api/agents/{agent_name}</code> - Run agent</li>
                <li><code>POST /api/skills/{skill_name}</code> - Run skill</li>
                <li><code>POST /api/pipeline/run</code> - Run full pipeline</li>
                <li><code>GET /api/pipeline/status/{ticket}</code> - Get status</li>
                <li><code>POST /api/webhooks/github</code> - GitHub webhook</li>
                <li><code>POST /api/webhooks/discord</code> - Discord webhook</li>
            </ul>

            <h2>🔧 Configuration</h2>
            <p>Set environment variables:</p>
            <pre><code>DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
GITHUB_WEBHOOK_SECRET=your-secret
API_PORT=8000</code></pre>
        </div>
    </body>
    </html>
    """


@app.get("/api/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "service": "multi-agent-coding-team",
        "version": "0.0.4"
    }


@app.get("/api/information")
async def information():
    """API informationrmation"""
    return {
        "name": "Multi-Agent Coding Team API",
        "version": "0.0.4",
        "agents": ["pm", "coding", "qa", "project-planner", "stack-initializer"],
        "skills": [
            "validate-spec",
            "commit",
            "review-pr",
            "refactor-code",
            "test-runner",
            "deploy",
            "benchmark",
            "docs-generator"
        ],
        "integrations": ["discord", "github"],
        "docs": {
            "swagger": "/api/docs",
            "redoc": "/api/redoc"
        }
    }


if __name__ == "__main__":
    # Run in development mode
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="information"
    )
