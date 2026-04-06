"""Pipeline Service - Run pipeline and management"""

import sys
from pathlib import Path

# auto_pipeline.pyfor importing for importing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from auto_pipeline_v2 import AutoPipelineV2
from typing import Optional, List, Dict, Any
import json
from datetime import datetime


class PipelineService:
    """Pipeline service"""

    def __init__(self):
        self.team_root = Path(__file__).parent.parent.parent
        self.pipelines: Dict[str, Dict[str, Any]] = {}  # In-memory storage

    def run_pipeline(
        self,
        ticket: str,
        project: str,
        resume: bool = False,
        skip_steps: Optional[List[str]] = None
    ):
        """Run pipeline (background)"""

        project_path = self.team_root / "projects" / project

        if not project_path.exists():
            raise Exception(f"Project not found: {project}")

        pipeline = AutoPipelineV2(str(project_path))

        # Initialize status
        self.pipelines[ticket] = {
            "ticket": ticket,
            "status": "running",
            "current_step": "pm",
            "progress": 0,
            "started_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "duration_seconds": None,
            "steps": [],
            "error": None
        }

        try:
            # Run pipeline
            pipeline.run_full_pipeline(resume=resume)

            # success Status update
            self.pipelines[ticket].update({
                "status": "success",
                "progress": 100,
                "completed_at": datetime.utcnow().isoformat()
            })

        except Exception as e:
            # failure Status update
            self.pipelines[ticket].update({
                "status": "failed",
                "completed_at": datetime.utcnow().isoformat(),
                "error": str(e)
            })

    def get_status(self, ticket: str) -> Optional[Dict[str, Any]]:
        """Get pipeline status"""
        return self.pipelines.get(ticket)

    def list_pipelines(
        self,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List pipelines"""

        pipelines = list(self.pipelines.values())

        if status:
            pipelines = [p for p in pipelines if p["status"] == status]

        # Sort by most recent
        pipelines.sort(key=lambda x: x["started_at"], reverse=True)

        return pipelines[:limit]

    def cancel_pipeline(self, ticket: str):
        """Cancel pipeline"""

        if ticket not in self.pipelines:
            raise Exception(f"Pipeline not found: {ticket}")

        self.pipelines[ticket].update({
            "status": "cancelled",
            "completed_at": datetime.utcnow().isoformat()
        })

    def delete_pipeline(self, ticket: str):
        """Delete pipeline"""

        if ticket not in self.pipelines:
            raise Exception(f"Pipeline not found: {ticket}")

        del self.pipelines[ticket]

    def get_logs(self, ticket: str, step: Optional[str] = None) -> List[str]:
        """Get pipeline logs"""

        # In practice file read logs from file system
        log_dir = self.team_root / "projects" / "logs"

        if not log_dir.exists():
            return []

        # Simple implementation
        return ["Log line 1", "Log line 2"]

    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""

        total = len(self.pipelines)
        by_status = {}

        for pipeline in self.pipelines.values():
            status = pipeline["status"]
            by_status[status] = by_status.get(status, 0) + 1

        return {
            "total": total,
            "by_status": by_status,
            "success_rate": by_status.get("success", 0) / total if total > 0 else 0
        }
