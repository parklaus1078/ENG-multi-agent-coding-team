"""Request Models"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class AgentRunRequest(BaseModel):
    """Agent execution request (generic)"""
    ticket: Optional[str] = Field(None, description="Ticket number (Examples: PLAN-001)")
    project: str = Field(..., description="Project name")
    prompt: Optional[str] = Field(None, description="Additional prompt")
    auto_mode: bool = Field(True, description="Auto mode (no questions)")

    class Config:
        schema_extra = {
            "example": {
                "ticket": "PLAN-001",
                "project": "my-cli-tool",
                "prompt": None,
                "auto_mode": True
            }
        }


class ProjectPlannerRequest(BaseModel):
    """Project Planner Agent execution request"""
    project: str = Field(..., description="Project name")
    requirements_text: str = Field(..., description="Requirements text")

    class Config:
        schema_extra = {
            "example": {
                "project": "my-todo-app",
                "requirements_text": "Develop a web-based TODO app..."
            }
        }


class StandardAgentRequest(BaseModel):
    """PM/Coding/QA Agent execution request"""
    project: str = Field(..., description="Project name")
    ticket: str = Field(..., description="Ticket number (Examples: PLAN-001)")

    class Config:
        schema_extra = {
            "example": {
                "project": "my-todo-app",
                "ticket": "PLAN-001"
            }
        }


class StackInitializerRequest(BaseModel):
    """Stack Initializer Agent execution request"""
    project: str = Field(..., description="Project name")

    class Config:
        schema_extra = {
            "example": {
                "project": "my-todo-app"
            }
        }


class SkillRunRequest(BaseModel):
    """Skill execution request"""
    ticket: Optional[str] = Field(None, description="Ticket number")
    project: str = Field(..., description="Project name")
    args: Optional[Dict[str, Any]] = Field(None, description="Additional argumentss")
    auto_fix: bool = Field(False, description="auto-fix apply")

    class Config:
        schema_extra = {
            "example": {
                "ticket": "PLAN-001",
                "project": "my-cli-tool",
                "args": {},
                "auto_fix": False
            }
        }


class PipelineRunRequest(BaseModel):
    """Run pipeline request"""
    ticket: str = Field(..., description="Ticket number")
    project: str = Field(..., description="Project name")
    Resume: bool = Field(False, description="interrupted pipeline resume")
    skip_steps: Optional[list[str]] = Field(None, description="to skip steps")

    class Config:
        schema_extra = {
            "example": {
                "ticket": "PLAN-001",
                "project": "my-cli-tool",
                "Resume": False,
                "skip_steps": None
            }
        }


class GitHubWebhookRequest(BaseModel):
    """GitHub Webhook request"""
    action: str = Field(..., description="Event Action")
    pull_request: Optional[Dict[str, Any]] = Field(None, description="PR information")
    issue: Optional[Dict[str, Any]] = Field(None, description="Issue information")
    repository: Dict[str, Any] = Field(..., description="Repository information")
    sender: Dict[str, Any] = Field(..., description="Sender information")


class DiscordCommandRequest(BaseModel):
    """Discord Command request"""
    command: str = Field(..., description="Command name")
    args: Optional[list[str]] = Field(None, description="Command arguments")
    user_id: str = Field(..., description="Discord user ID")
    channel_id: str = Field(..., description="Discord channel ID")

    class Config:
        schema_extra = {
            "example": {
                "command": "run",
                "args": ["PLAN-001"],
                "user_id": "123456789",
                "channel_id": "987654321"
            }
        }
