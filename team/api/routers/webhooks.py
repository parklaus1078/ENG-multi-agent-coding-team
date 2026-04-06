"""Webhooks Router"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Request, Header
from api.models.request import GitHubWebhookRequest, DiscordCommandRequest
from api.models.response import WebhookResponse
from api.services.webhook_service import WebhookService
from api.services.discord_service import DiscordService
import hmac
import hashlib
import os

router = APIRouter()
webhook_service = WebhookService()
discord = DiscordService()


@router.post("/github", response_model=WebhookResponse)
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None)
):
    """GitHub Webhook Receive"""

    # Signature verification
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    if secret:
        body = await request.body()
        signature = hmac.new(
            secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(f"sha256={signature}", x_hub_signature_256 or ""):
            raise HTTPException(status_code=401, detail="Invalid signature")

    # Payload parsing
    payload = await request.json()

    # event handling
    event_type = x_github_event
    action = payload.get("action", "")

    # PR event
    if event_type == "pull_request":
        pr = payload.get("pull_request", {})
        pr_number = pr.get("number")
        pr_title = pr.get("title")

        if action in ["opened", "synchronize"]:
            # review-pr skill Run
            background_tasks.add_task(
                webhook_service.handle_pr_event,
                pr_number=pr_number,
                action=action,
                repository=payload.get("repository", {})
            )

            # Discord notification
            await discord.send_notification(
                title=f"🔔 GitHub PR {action.capitalize()}",
                description=f"**PR #{pr_number}**: {pr_title}",
                color=5814783,  # Purple
                url=pr.get("html_url")
            )

            return WebhookResponse(
                received=True,
                event=event_type,
                action=action,
                queued=True,
                message=f"PR #{pr_number} review queued"
            )

    # Issue event
    elif event_type == "issues":
        issue = payload.get("issue", {})
        issue_number = issue.get("number")
        issue_title = issue.get("title")

        if action == "opened":
            # Automatically create ticket
            background_tasks.add_task(
                webhook_service.handle_issue_event,
                issue_number=issue_number,
                issue=issue,
                repository=payload.get("repository", {})
            )

            # Discord notification
            await discord.send_notification(
                title=f"🔔 GitHub Issue Opened",
                description=f"**Issue #{issue_number}**: {issue_title}",
                color=5814783,  # Purple
                url=issue.get("html_url")
            )

            return WebhookResponse(
                received=True,
                event=event_type,
                action=action,
                queued=True,
                message=f"Issue #{issue_number} ticket creation queued"
            )

    # basic response
    return WebhookResponse(
        received=True,
        event=event_type,
        action=action,
        queued=False,
        message="Event received but not processed"
    )


@router.post("/discord", response_model=WebhookResponse)
async def discord_webhook(request: DiscordCommandRequest, background_tasks: BackgroundTasks):
    """Discord Receive command"""

    command = request.command
    args = request.args or []

    # Command handling
    if command == "run":
        # pipeline Run
        if not args:
            return WebhookResponse(
                received=True,
                event="discord",
                action=command,
                queued=False,
                message="Usage: /run <ticket>"
            )

        ticket = args[0]

        background_tasks.add_task(
            webhook_service.handle_discord_command,
            command=command,
            args=args,
            user_id=request.user_id,
            channel_id=request.channel_id
        )

        return WebhookResponse(
            received=True,
            event="discord",
            action=command,
            queued=True,
            message=f"Pipeline {ticket} started"
        )

    elif command == "status":
        # Status query
        if not args:
            return WebhookResponse(
                received=True,
                event="discord",
                action=command,
                queued=False,
                message="Usage: /status <ticket>"
            )

        ticket = args[0]

        background_tasks.add_task(
            webhook_service.handle_discord_command,
            command=command,
            args=args,
            user_id=request.user_id,
            channel_id=request.channel_id
        )

        return WebhookResponse(
            received=True,
            event="discord",
            action=command,
            queued=True,
            message=f"Checking status for {ticket}"
        )

    elif command == "help":
        # Help
        help_text = """
**Available Commands**:
- `/run <ticket>` - Run pipeline
- `/status <ticket>` - Check status
- `/cancel <ticket>` - Cancel pipeline
- `/list` - List active pipelines
- `/help` - Show this help
"""
        background_tasks.add_task(
            discord.send_message,
            channel_id=request.channel_id,
            content=help_text
        )

        return WebhookResponse(
            received=True,
            event="discord",
            action=command,
            queued=False,
            message="Help sent"
        )

    else:
        return WebhookResponse(
            received=True,
            event="discord",
            action=command,
            queued=False,
            message=f"Unknown command: {command}"
        )
