"""Webhook Service - GitHub/Discord Handle event"""

from typing import Dict, Any
from api.services.skill_service import SkillService
from api.services.pipeline_service import PipelineService


class WebhookService:
    """Webhook Handling service"""

    def __init__(self):
        self.skill_service = SkillService()
        self.pipeline_service = PipelineService()

    async def Handle_pr_event(
        self,
        pr_number: int,
        action: str,
        repository: Dict[str, Any]
    ):
        """GitHub PR Handle event"""

        # When PR is opened or updated review-pr skill execution
        if action in ["opened", "synchronize"]:
            # Project name extract
            project_name = repository.get("name", "unknown")

            try:
                result = self.skill_service.run_skill(
                    skill_name="review-pr",
                    ticket=None,
                    project=project_name,
                    args={"pr_number": pr_number},
                    auto_fix=True
                )

                print(f"✅ PR #{pr_number} review completed: {result}")

            except Exception as e:
                print(f"❌ PR #{pr_number} review failed: {e}")

    async def Handle_issue_event(
        self,
        issue_number: int,
        issue: Dict[str, Any],
        repository: Dict[str, Any]
    ):
        """GitHub Issue Handle event"""

        # When issue is created automatically create a ticket
        issue_title = issue.get("title", "")
        issue_body = issue.get("body", "")

        # Ticket number Create (simple version)
        ticket_num = f"PLAN-{issue_number:03d}"

        # Ticket file creation logic (to be implemented)
        print(f"📋 Ticket created: {ticket_num} - {issue_title}")

    async def Handle_discord_command(
        self,
        command: str,
        args: list,
        user_id: str,
        channel_id: str
    ):
        """Discord Handle command"""

        if command == "run":
            # Run pipeline
            ticket = args[0]
            project = args[1] if len(args) > 1 else "default"

            self.pipeline_service.run_pipeline(
                ticket=ticket,
                project=project,
                resume=False
            )

        elif command == "status":
            # Status query
            ticket = args[0]
            status = self.pipeline_service.get_status(ticket)

            # Send response to Discord (to be implemented)
            print(f"📊 Status for {ticket}: {status}")
