"""Agent Service - agent responsible for execution"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any


class AgentService:
    """agent execution service"""

    def __init__(self):
        self.team_root = Path(__file__).parent.parent.parent
        self.run_agent_script = self.team_root / "scripts" / "run-agent.sh"

    def run_agent(
        self,
        agent_name: str,
        ticket: str,
        project: str,
        prompt: Optional[str] = None,
        auto_mode: bool = True
    ) -> Dict[str, Any]:
        """
        agent execution

        Returns:
            {"session_id": str, "message_count": int, "output": str}
        """

        # run-agent.sh call
        cmd = [
            "bash",
            str(self.run_agent_script),
            agent_name,
            "--ticket", ticket
        ]

        if auto_mode:
            cmd.append("--auto")

        # Run in project directory
        project_dir = self.team_root / "projects" / project

        if not project_dir.exists():
            raise Exception(f"Project not found: {project}")

        result = subprocess.run(
            cmd,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=3600  # 1hour timeout
        )

        if result.returncode != 0:
            raise Exception(f"Agent execution failed: {result.stderr}")

        # Parse output
        output = result.stdout

        # Session ID extract (simple version)
        session_id = "unknown"
        message_count = 0

        return {
            "session_id": session_id,
            "message_count": message_count,
            "output": output
        }
