"""Discord Service"""

import os
import aiohttp
from typing import Optional, List, Dict, Any


class DiscordService:
    """Discord Integration service"""

    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "")

        if not self.webhook_url:
            print("⚠️  DISCORD_WEBHOOK_URL environment variable is not set.")
            print("   Discord To receive notifications, set it:")
            print("   export DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...")

    async def send_notification(
        self,
        title: str,
        description: str,
        color: int = 3447003,  # Blue
        fields: Optional[List[Dict[str, Any]]] = None,
        url: Optional[str] = None,
        footer: Optional[str] = None
    ):
        """Discord Send notification"""

        if not self.webhook_url:
            print(f"[Discord] {title}: {description}")
            return

        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": None  # ISO 8601 format
        }

        if fields:
            embed["fields"] = fields

        if url:
            embed["url"] = url

        if footer:
            embed["footer"] = {"text": footer}
        else:
            embed["footer"] = {"text": "Multi-Agent Coding Team"}

        payload = {
            "embeds": [embed]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status not in [200, 204]:
                        print(f"⚠️  Discord webhook failure: {response.status}")
        except Exception as e:
            print(f"⚠️  Discord webhook error: {e}")

    async def send_message(self, channel_id: str, content: str):
        """Discord Send message (Bot required)"""
        # Bot Token required - to be implemented
        print(f"[Discord] Channel {channel_id}: {content}")

    async def send_pipeline_progress(
        self,
        ticket: str,
        status: str,
        current_step: str,
        progress: int
    ):
        """Send pipeline progress notification"""

        # Colors by status
        colors = {
            "running": 3447003,   # Blue
            "success": 3066993,   # Green
            "failed": 15158332,   # Red
            "cancelled": 16776960  # Yellow
        }

        # Status emoji
        status_emoji = {
            "running": "🟢",
            "success": "✅",
            "failed": "❌",
            "cancelled": "⏹️"
        }

        await self.send_notification(
            title=f"{status_emoji.get(status, '🔵')} Pipeline {status.capitalize()}",
            description=f"**Ticket**: {ticket}",
            color=colors.get(status, 3447003),
            fields=[
                {"name": "Current Step", "value": current_step, "inline": True},
                {"name": "Progress", "value": f"{progress}%", "inline": True}
            ]
        )

    async def send_test_results(
        self,
        ticket: str,
        total: int,
        passed: int,
        failed: int,
        coverage: float
    ):
        """Send test results notification"""

        if failed > 0:
            color = 15158332  # Red
            title = "❌ Tests Failed"
        else:
            color = 3066993  # Green
            title = "✅ All Tests Passed"

        await self.send_notification(
            title=title,
            description=f"**Ticket**: {ticket}",
            color=color,
            fields=[
                {"name": "Total", "value": str(total), "inline": True},
                {"name": "Passed", "value": str(passed), "inline": True},
                {"name": "Failed", "value": str(failed), "inline": True},
                {"name": "Coverage", "value": f"{coverage*100:.1f}%", "inline": False}
            ]
        )

    async def send_deployment_notification(
        self,
        ticket: str,
        environment: str,
        status: str,
        url: Optional[str] = None
    ):
        """Send deployment notification"""

        if status == "success":
            color = 3066993  # Green
            title = f"🚀 Deployed to {environment.capitalize()}"
        else:
            color = 15158332  # Red
            title = f"❌ Deployment Failed ({environment})"

        fields = [
            {"name": "Ticket", "value": ticket, "inline": True},
            {"name": "Environment", "value": environment, "inline": True}
        ]

        if url:
            fields.append({"name": "URL", "value": url, "inline": False})

        await self.send_notification(
            title=title,
            description=f"Deployment to {environment}",
            color=color,
            fields=fields,
            url=url
        )

    async def send_pr_review_notification(
        self,
        pr_number: int,
        status: str,
        issues_count: int,
        auto_fixed: int = 0
    ):
        """PR Send PR review result notification"""

        if status == "approved":
            color = 3066993  # Green
            title = f"✅ PR #{pr_number} Approved"
        else:
            color = 16776960  # Yellow
            title = f"⚠️ PR #{pr_number} Changes Requested"

        fields = [
            {"name": "Issues Found", "value": str(issues_count), "inline": True}
        ]

        if auto_fixed > 0:
            fields.append({"name": "Auto-Fixed", "value": str(auto_fixed), "inline": True})

        await self.send_notification(
            title=title,
            description=f"Pull Request #{pr_number} reviewed",
            color=color,
            fields=fields
        )
