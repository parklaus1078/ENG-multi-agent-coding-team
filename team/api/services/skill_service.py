"""Skill Service - Skill responsible for execution"""

import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


class SkillService:
    """Skill execution service"""

    def __init__(self):
        self.team_root = Path(__file__).parent.parent.parent
        self.run_skill_script = self.team_root / "scripts" / "run-skill.sh"

    def run_skill(
        self,
        skill_name: str,
        ticket: Optional[str],
        project: str,
        args: Dict[str, Any],
        auto_fix: bool = False
    ) -> Dict[str, Any]:
        """
        Skill execution

        Returns:
            execution result dictionary
        """

        # run-skill.sh call
        cmd = [
            "bash",
            str(self.run_skill_script),
            skill_name
        ]

        # Ticket number
        if ticket:
            cmd.extend(["--ticket", ticket])

        # Auto-fix
        if auto_fix:
            cmd.append("--auto-fix")

        # Additional arguments
        for key, value in args.items():
            cmd.extend([f"--{key}", str(value)])

        # Run in project directory
        project_dir = self.team_root / "projects" / project

        if not project_dir.exists():
            raise Exception(f"Project not found: {project}")

        result = subprocess.run(
            cmd,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=600  # 10minute timeout
        )

        # result parsing (simple version)
        success = result.returncode == 0
        output = result.stdout

        return {
            "success": success,
            "output": output,
            "error": result.stderr if not success else None
        }
