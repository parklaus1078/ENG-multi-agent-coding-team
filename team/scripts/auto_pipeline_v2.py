#!/usr/bin/env python3
"""
Auto Pipeline v2 - Claude Code Interactive Session Based

New pipeline leveraging Claude Code's interactive nature:
1. Start a session in a new terminal tab for each agent
2. Maintain sessions so users can return later
3. Record and manage session IDs
4. Sequential execution between agents

⚠️ Important:
- macOS only (uses Terminal.app + AppleScript)
- Requires Claude Code CLI
- User confirms each step during progress
"""

import os
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AutoPipelineV2:
    """
    Claude Code Interactive Session Based Auto Pipeline

    Architecture:
    1. Each agent = separate Terminal tab
    2. Session maintained (not terminated)
    3. Tab IDs recorded in .sessions/session-map.json
    4. User can return to tabs later
    """

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.workspace_root = self.project_path.parent.parent
        self.sessions_dir = self.project_path / ".sessions"
        self.sessions_dir.mkdir(exist_ok=True)

        # Session map file
        self.session_map_file = self.sessions_dir / "session-map.json"
        self.session_map = self._load_session_map()

        # Check Terminal.app support (macOS only)
        self._check_macos()

    def _check_macos(self):
        """Check macOS and Terminal.app availability"""
        if os.uname().sysname != "Darwin":
            raise RuntimeError("This script is macOS only.")

        print("✅ macOS confirmed")
        print("✅ Terminal.app session management enabled")

    def _load_session_map(self) -> dict:
        """Load session map"""
        if self.session_map_file.exists():
            with open(self.session_map_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_session_map(self):
        """Save session map"""
        with open(self.session_map_file, 'w') as f:
            json.dump(self.session_map, f, indent=2)
        print(f"✅ Session map saved: {self.session_map_file}")

    def open_agent_in_new_tab(
        self,
        agent_name: str,
        ticket_num: str,
        initial_prompt: str
    ) -> str:
        """
        Start agent session in a new Terminal tab

        Args:
            agent_name: pm, coding, qa, etc.
            ticket_num: Ticket number (e.g., BILL-001)
            initial_prompt: Initial prompt

        Returns:
            Session ID (Terminal tab identifier)
        """
        agent_dir = self.workspace_root / ".agents" / agent_name

        if not agent_dir.exists():
            raise FileNotFoundError(f"Agent directory not found: {agent_dir}")

        # Generate session ID (timestamp based)
        session_id = f"{agent_name}-{ticket_num}-{int(time.time())}"

        # Load previous session context
        context_text = self._load_previous_sessions_text(ticket_num, agent_name)

        # Combine final prompt
        if context_text:
            full_prompt = f"""## Previous Agent Session Information

{context_text}

---

## Current Task

{initial_prompt}
"""
        else:
            full_prompt = initial_prompt

        # Create prompt file
        prompt_file = self.sessions_dir / f".prompt-{session_id}.txt"
        prompt_file.write_text(full_prompt, encoding='utf-8')

        # Open new Terminal tab with AppleScript
        applescript = f'''
tell application "Terminal"
    activate

    -- Create new tab
    tell application "System Events"
        keystroke "t" using command down
    end tell

    delay 0.5

    -- Navigate to agent directory
    do script "cd {agent_dir}" in front window

    delay 0.3

    -- Run Claude Code (initialize with prompt file)
    do script "echo '🤖 {agent_name.upper()} Agent Session Started'" in front window
    do script "echo '📋 Ticket: {ticket_num}'" in front window
    do script "echo '🔑 Session ID: {session_id}'" in front window
    do script "echo ''" in front window
    do script "cat {prompt_file}" in front window
    do script "echo ''" in front window
    do script "echo '⬆️ Copy and paste the above prompt into Claude Code.'" in front window
    do script "echo ''" in front window
    do script "claude" in front window

    -- Set tab title
    set custom title of front window to "{agent_name.upper()} - {ticket_num}"
end tell
'''

        # Execute AppleScript
        subprocess.run(
            ["osascript", "-e", applescript],
            check=True
        )

        print(f"\n{'='*60}")
        print(f"✅ {agent_name.upper()} Agent started in new Terminal tab")
        print(f"📋 Ticket: {ticket_num}")
        print(f"🔑 Session ID: {session_id}")
        print(f"📁 Agent Dir: {agent_dir}")
        print('='*60)

        # Record in session map
        if ticket_num not in self.session_map:
            self.session_map[ticket_num] = {}

        self.session_map[ticket_num][agent_name] = {
            "session_id": session_id,
            "started_at": datetime.now().isoformat(),
            "status": "active",
            "agent_dir": str(agent_dir),
            "prompt_file": str(prompt_file)
        }

        self._save_session_map()

        return session_id

    def _load_previous_sessions_text(self, ticket_num: str, current_agent: str) -> str:
        """Generate summary text of previous agent sessions"""
        agent_order = ["project-planner", "pm", "coding", "qa"]

        try:
            current_index = agent_order.index(current_agent)
        except ValueError:
            return ""

        previous_agents = agent_order[:current_index]

        if ticket_num not in self.session_map:
            return ""

        context_parts = []

        for prev_agent in previous_agents:
            if prev_agent in self.session_map[ticket_num]:
                session_info = self.session_map[ticket_num][prev_agent]
                context_parts.append(f"""### {prev_agent.upper()} Agent
- Session ID: {session_info['session_id']}
- Started: {session_info['started_at']}
- Status: {session_info['status']}

Work details can be reviewed in the Terminal tab.
""")

        if not context_parts:
            return ""

        return "\n".join(context_parts)

    def wait_for_user_confirmation(self, agent_name: str, ticket_num: str):
        """
        Wait until user confirms agent task completion

        User interacts with agent in Terminal tab to complete task.
        After completion, return to this script and press Enter.
        """
        print(f"\n{'='*60}")
        print(f"⏳ Waiting for {agent_name.upper()} Agent to complete...")
        print(f"📋 Ticket: {ticket_num}")
        print(f"\nInstructions:")
        print(f"1. Navigate to Terminal tab '{agent_name.upper()} - {ticket_num}'")
        print(f"2. Complete task by interacting with Claude Code")
        print(f"3. Return to this window and press Enter after completion")
        print('='*60)

        input("\n✅ Press Enter after task completion... ")

        # Update session status
        if ticket_num in self.session_map and agent_name in self.session_map[ticket_num]:
            self.session_map[ticket_num][agent_name]["status"] = "completed"
            self.session_map[ticket_num][agent_name]["completed_at"] = datetime.now().isoformat()
            self._save_session_map()

        print(f"✅ {agent_name.upper()} Agent task completion confirmed")

    def run_full_pipeline(self, ticket_num: str):
        """
        Execute full pipeline

        Args:
            ticket_num: Ticket number (e.g., BILL-001)

        Flow:
        1. PM Agent → Open new tab → User works → Wait for confirmation
        2. Coding Agent → Open new tab → User works → Wait for confirmation
        3. QA Agent → Open new tab → User works → Wait for confirmation
        """
        print(f"\n{'='*60}")
        print(f"🚀 Auto Pipeline Started")
        print(f"📂 Project: {self.project_path.name}")
        print(f"📋 Ticket: {ticket_num}")
        print('='*60)

        # Check ticket file
        ticket_file = self._find_ticket_file(ticket_num)

        if not ticket_file:
            raise FileNotFoundError(f"Ticket file not found: {ticket_num}")

        # Read ticket content
        ticket_content = ticket_file.read_text(encoding='utf-8')

        # Step 1: PM Agent
        print(f"\n{'='*60}")
        print("1️⃣ Running PM Agent")
        print('='*60)

        pm_prompt = f"""Please generate specifications for the following ticket:

{ticket_content}

Tasks:
1. Generate API specifications (planning/specs/backend/)
2. Generate UI requirements (planning/specs/frontend/)
3. Generate test cases (planning/test-cases/)
"""

        self.open_agent_in_new_tab("pm", ticket_num, pm_prompt)
        self.wait_for_user_confirmation("pm", ticket_num)

        # Step 2: Coding Agent
        print(f"\n{'='*60}")
        print("2️⃣ Running Coding Agent")
        print('='*60)

        coding_prompt = f"""Please implement ticket {ticket_num}.

Tasks:
1. Review specifications generated by PM Agent
2. Implement code (in src/ directory)
3. Create Git branch and commit
"""

        self.open_agent_in_new_tab("coding", ticket_num, coding_prompt)
        self.wait_for_user_confirmation("coding", ticket_num)

        # Step 3: QA Agent
        print(f"\n{'='*60}")
        print("3️⃣ Running QA Agent")
        print('='*60)

        qa_prompt = f"""Please write tests for ticket {ticket_num}.

Tasks:
1. Review test cases from PM Agent
2. Review code implemented by Coding Agent
3. Write and execute test code
"""

        self.open_agent_in_new_tab("qa", ticket_num, qa_prompt)
        self.wait_for_user_confirmation("qa", ticket_num)

        # Complete
        print(f"\n{'='*60}")
        print("🎉 Full pipeline completed!")
        print(f"📋 Ticket: {ticket_num}")
        print(f"\nSession Information:")
        if ticket_num in self.session_map:
            for agent_name, session_info in self.session_map[ticket_num].items():
                print(f"  - {agent_name.upper()}: {session_info['session_id']}")
        print('='*60)

        print(f"\n💡 Tip:")
        print(f"  - Each agent tab remains open.")
        print(f"  - If modifications are needed later, return to the respective tab to continue the conversation")
        print(f"  - Session map: {self.session_map_file}")

    def _find_ticket_file(self, ticket_num: str) -> Optional[Path]:
        """Find ticket file"""
        tickets_dir = self.project_path / "planning" / "tickets"

        if not tickets_dir.exists():
            return None

        # Find {ACRONYM}-XXX-*.md pattern
        for ticket_file in tickets_dir.glob(f"{ticket_num}-*.md"):
            return ticket_file

        return None

    def resume_agent_session(self, ticket_num: str, agent_name: str):
        """
        Resume existing agent session (for modification tasks)

        Args:
            ticket_num: Ticket number
            agent_name: Agent name
        """
        if ticket_num not in self.session_map:
            print(f"❌ Session for ticket {ticket_num} not found.")
            return

        if agent_name not in self.session_map[ticket_num]:
            print(f"❌ {agent_name.upper()} Agent session not found.")
            return

        session_info = self.session_map[ticket_num][agent_name]

        print(f"\n{'='*60}")
        print(f"📍 Session Information")
        print(f"  - Agent: {agent_name.upper()}")
        print(f"  - Ticket: {ticket_num}")
        print(f"  - Session ID: {session_info['session_id']}")
        print(f"  - Started: {session_info['started_at']}")
        print(f"  - Status: {session_info['status']}")
        print('='*60)

        print(f"\n💡 Find the tab in Terminal:")
        print(f"   Tab title: '{agent_name.upper()} - {ticket_num}'")
        print(f"\n   Navigate to the tab where the Claude Code session is maintained.")
        print(f"   Continue the conversation to proceed with modification tasks.")


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Auto Pipeline v2 - Claude Code Interactive Session Based"
    )

    parser.add_argument(
        "--project",
        help="Project path (if omitted, read from .project-config.json)"
    )

    parser.add_argument(
        "--ticket",
        required=True,
        help="Ticket number (e.g., BILL-001, TODO-002)"
    )

    parser.add_argument(
        "--resume",
        metavar="AGENT",
        help="Resume existing session (pm, coding, qa)"
    )

    args = parser.parse_args()

    # Determine project path
    if args.project:
        project_path = Path(args.project)
    else:
        # Read from .project-config.json
        config_file = Path(__file__).parent.parent / ".project-config.json"
        if not config_file.exists():
            print("❌ .project-config.json not found.")
            print("   Specify path with --project option")
            return

        with open(config_file) as f:
            config = json.load(f)

        current_project = config["current_project"]
        project_path = Path(__file__).parent.parent / "projects" / current_project

    # Execute Auto Pipeline
    pipeline = AutoPipelineV2(str(project_path))

    if args.resume:
        # Resume existing session
        pipeline.resume_agent_session(args.ticket, args.resume)
    else:
        # Execute full pipeline
        pipeline.run_full_pipeline(args.ticket)


if __name__ == "__main__":
    main()
