from ai.agents.base_agent import BaseAgent
from ai.orchestration.agent_result import AgentResult


class ConversationAgent(BaseAgent):
    """Handles normal conversational requests."""

    name = "conversation"
    description = (
        "Handles general conversation, questions, "
        "and natural-language responses."
    )

    def can_handle(self, command):
        return command.intent == "chat"

    def run(self, context):
        return AgentResult(
            success=True,
            agent=self.name,
            metadata={
                "delegate_to_existing_pipeline": True,
            },
        )