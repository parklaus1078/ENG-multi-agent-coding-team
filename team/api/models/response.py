"""Response Models"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    """Pipeline status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentRunResponse(BaseModel):
    """agent execution response"""
    success: bool = Field(..., description="Success status")
    agent: str = Field(..., description="Agent name")
    ticket: str = Field(..., description="Ticket number")
    session_id: str = Field(..., description="Session ID")
    message_count: int = Field(..., description="Message count")
    duration_seconds: float = Field(..., description="execution time (seconds)")
    output: Optional[str] = Field(None, description="Output message")
    error: Optional[str] = Field(None, description="Error message")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "agent": "pm",
                "ticket": "PLAN-001",
                "session_id": "abc123",
                "message_count": 5,
                "duration_seconds": 45.2,
                "output": "Specification generation completed",
                "error": None
            }
        }


class SkillRunResponse(BaseModel):
    """Skill execution response"""
    success: bool = Field(..., description="Success status")
    skill: str = Field(..., description="Skill name")
    duration_seconds: float = Field(..., description="execution time (seconds)")
    result: Dict[str, Any] = Field(..., description="execution result")
    error: Optional[str] = Field(None, description="Error message")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "skill": "validate-spec",
                "duration_seconds": 2.1,
                "result": {
                    "passed": True,
                    "errors": 0,
                    "warnings": 1
                },
                "error": None
            }
        }


class PipelineStatusResponse(BaseModel):
    """Pipeline status response"""
    ticket: str = Field(..., description="Ticket number")
    status: StatusEnum = Field(..., description="Status")
    current_step: Optional[str] = Field(None, description="Current step")
    progress: int = Field(..., description="Progress (0-100)")
    started_at: Optional[datetime] = Field(None, description="Start time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    duration_seconds: Optional[float] = Field(None, description="Duration")
    steps: List[Dict[str, Any]] = Field(..., description="Step list")
    error: Optional[str] = Field(None, description="Error message")

    class Config:
        schema_extra = {
            "example": {
                "ticket": "PLAN-001",
                "status": "running",
                "current_step": "coding",
                "progress": 60,
                "started_at": "2026-03-19T10:00:00Z",
                "completed_at": None,
                "duration_seconds": None,
                "steps": [
                    {"name": "pm", "status": "success", "duration": 45.2},
                    {"name": "validate-spec", "status": "success", "duration": 2.1},
                    {"name": "coding", "status": "running", "duration": None}
                ],
                "error": None
            }
        }


class PipelineListResponse(BaseModel):
    """pipeline list response"""
    total: int = Field(..., description="Total count")
    pipelines: List[PipelineStatusResponse] = Field(..., description="pipeline list")


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Version")


class WebhookResponse(BaseModel):
    """Webhook response"""
    received: bool = Field(True, description="Received")
    event: str = Field(..., description="Event type")
    action: str = Field(..., description="Action")
    queued: bool = Field(..., description="Queued")
    message: str = Field(..., description="Response message")
