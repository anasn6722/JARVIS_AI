from ai.agents.conversation_agent import ConversationAgent
from ai.agents.desktop_agent import DesktopAgent
from ai.agents.memory_agent import MemoryAgent
from ai.agents.research_agent import ResearchAgent
from ai.agents.ui_agent import UIAgent


class SupervisorAgent:
    """Routes JARVIS commands to specialist agents."""

    name = "supervisor"

    def __init__(self):
        # Order matters.
        self.agents = (
            UIAgent(),
            MemoryAgent(),
            ResearchAgent(),
            DesktopAgent(),
            ConversationAgent(),
        )

    def select_agent(self, command):
        for agent in self.agents:
            if agent.can_handle(command):
                return agent

        return None

    def route(self, command, context):
        agent = self.select_agent(command)

        if agent is None:
            return None

        context.agent_name = agent.name

        return agent.run(context)