"""Agent Router"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.models.request import ProjectPlannerRequest, StandardAgentRequest, StackInitializerRequest
from api.models.response import AgentRunResponse
from api.services.agent_service import AgentService
from api.services.discord_service import DiscordService
import time

router = APIRouter()
agent_service = AgentService()
discord = DiscordService()


@router.post("/project-planner", response_model=AgentRunResponse)
async def run_project_planner(request: ProjectPlannerRequest, background_tasks: BackgroundTasks):
    """Project Planner Agent Run"""

    # Discord notification (start)
    await discord.send_notification(
        title="🗺️ Project Planner Agent Started",
        description=f"Project: {request.project}",
        color=3447003  # Blue
    )

    start_time = time.time()

    try:
        # agent Run
        result = agent_service.run_agent(
            agent_name="project-planner",
            ticket="",
            project=request.project,
            prompt=request.requirements_text,
            auto_mode=True
        )

        duration = time.time() - start_time

        # Discord notification (success)
        background_tasks.add_task(
            discord.send_notification,
            title="✅ Project Planner Agent Completed",
            description=f"Project: {request.project}\nDuration: {duration:.1f}s",
            color=3066993  # Green
        )

        return AgentRunResponse(
            success=True,
            agent="project-planner",
            ticket="",
            session_id=result.get("session_id", ""),
            message_count=result.get("message_count", 0),
            duration_seconds=duration,
            output=result.get("output", ""),
            error=None
        )

    except Exception as e:
        duration = time.time() - start_time

        # Discord notification (failure)
        background_tasks.add_task(
            discord.send_notification,
            title="❌ Project Planner Agent Failed",
            description=f"Project: {request.project}\nError: {str(e)}",
            color=15158332  # Red
        )

        return AgentRunResponse(
            success=False,
            agent="project-planner",
            ticket="",
            session_id="",
            message_count=0,
            duration_seconds=duration,
            output=None,
            error=str(e)
        )


@router.post("/pm", response_model=AgentRunResponse)
async def run_pm_agent(request: StandardAgentRequest, background_tasks: BackgroundTasks):
    """PM Agent Run"""
    return await _run_standard_agent("pm", request, background_tasks)


@router.post("/coding", response_model=AgentRunResponse)
async def run_coding_agent(request: StandardAgentRequest, background_tasks: BackgroundTasks):
    """Coding Agent Run"""
    return await _run_standard_agent("coding", request, background_tasks)


@router.post("/qa", response_model=AgentRunResponse)
async def run_qa_agent(request: StandardAgentRequest, background_tasks: BackgroundTasks):
    """QA Agent Run"""
    return await _run_standard_agent("qa", request, background_tasks)


@router.post("/stack-initializer", response_model=AgentRunResponse)
async def run_stack_initializer(request: StackInitializerRequest, background_tasks: BackgroundTasks):
    """Stack Initializer Agent Run"""

    # Discord notification (start)
    await discord.send_notification(
        title="⚙️ Stack Initializer Agent Started",
        description=f"Project: {request.project}",
        color=3447003  # Blue
    )

    start_time = time.time()

    try:
        # agent Run
        result = agent_service.run_agent(
            agent_name="stack-initializer",
            ticket="",
            project=request.project,
            prompt=None,
            auto_mode=True
        )

        duration = time.time() - start_time

        # Discord notification (success)
        background_tasks.add_task(
            discord.send_notification,
            title="✅ Stack Initializer Agent Completed",
            description=f"Project: {request.project}\nDuration: {duration:.1f}s",
            color=3066993  # Green
        )

        return AgentRunResponse(
            success=True,
            agent="stack-initializer",
            ticket="",
            session_id=result.get("session_id", ""),
            message_count=result.get("message_count", 0),
            duration_seconds=duration,
            output=result.get("output", ""),
            error=None
        )

    except Exception as e:
        duration = time.time() - start_time

        # Discord notification (failure)
        background_tasks.add_task(
            discord.send_notification,
            title="❌ Stack Initializer Agent Failed",
            description=f"Project: {request.project}\nError: {str(e)}",
            color=15158332  # Red
        )

        return AgentRunResponse(
            success=False,
            agent="stack-initializer",
            ticket="",
            session_id="",
            message_count=0,
            duration_seconds=duration,
            output=None,
            error=str(e)
        )


async def _run_standard_agent(
    agent_name: str,
    request: StandardAgentRequest,
    background_tasks: BackgroundTasks
) -> AgentRunResponse:
    """PM, Coding, QA Agent Run (common logic)"""

    # Discord notification (start)
    await discord.send_notification(
        title=f"🤖 {agent_name.upper()} Agent Started",
        description=f"Ticket: {request.ticket}\nProject: {request.project}",
        color=3447003  # Blue
    )

    start_time = time.time()

    try:
        # agent Run
        result = agent_service.run_agent(
            agent_name=agent_name,
            ticket=request.ticket,
            project=request.project,
            prompt=None,
            auto_mode=True
        )

        duration = time.time() - start_time

        # Discord notification (success)
        background_tasks.add_task(
            discord.send_notification,
            title=f"✅ {agent_name.upper()} Agent Completed",
            description=f"Ticket: {request.ticket}\nDuration: {duration:.1f}s",
            color=3066993  # Green
        )

        return AgentRunResponse(
            success=True,
            agent=agent_name,
            ticket=request.ticket,
            session_id=result.get("session_id", ""),
            message_count=result.get("message_count", 0),
            duration_seconds=duration,
            output=result.get("output", ""),
            error=None
        )

    except Exception as e:
        duration = time.time() - start_time

        # Discord notification (failure)
        background_tasks.add_task(
            discord.send_notification,
            title=f"❌ {agent_name.upper()} Agent Failed",
            description=f"Ticket: {request.ticket}\nError: {str(e)}",
            color=15158332  # Red
        )

        return AgentRunResponse(
            success=False,
            agent=agent_name,
            ticket=request.ticket,
            session_id="",
            message_count=0,
            duration_seconds=duration,
            output=None,
            error=str(e)
        )


@router.get("/list")
async def list_agents():
    """List available agents"""
    return {
        "agents": [
            {
                "name": "project-planner",
                "description": "Create and break down entire project tickets",
                "endpoint": "/api/agents/project-planner",
                "input": {
                    "project": "Project name (required)",
                    "requirements_text": "Requirements text (required)"
                }
            },
            {
                "name": "pm",
                "description": "Transform product planning into structured deliverables",
                "endpoint": "/api/agents/pm",
                "input": {
                    "project": "Project name (required)",
                    "ticket": "Ticket number (required)"
                }
            },
            {
                "name": "coding",
                "description": "Implement code according to project type",
                "endpoint": "/api/agents/coding",
                "input": {
                    "project": "Project name (required)",
                    "ticket": "Ticket number (required)"
                }
            },
            {
                "name": "qa",
                "description": "Write tests according to project type",
                "endpoint": "/api/agents/qa",
                "input": {
                    "project": "Project name (required)",
                    "ticket": "Ticket number (required)"
                }
            },
            {
                "name": "stack-initializer",
                "description": "Set up initial stack by project type",
                "endpoint": "/api/agents/stack-initializer",
                "input": {
                    "project": "Project name (required)"
                }
            }
        ]
    }
