from ai.agents.base_agent import BaseAgent
from ai.orchestration.agent_result import AgentResult


class ResearchAgent(BaseAgent):
    """Handles search, research, and information retrieval."""

    name = "research"

    description = (
        "Handles Google search, YouTube search, web research, "
        "knowledge retrieval, and information lookup."
    )

    RESEARCH_INTENTS = {
        "search",
        "youtube",
        "search_ui",
    }

    RESEARCH_PHRASES = (
        "search for",
        "search the web",
        "search online",
        "look up",
        "look it up",
        "find information",
        "research",
        "research this",
        "google",
        "youtube",
        "watch on youtube",
        "find videos",
        "latest news",
        "latest information",
        "current information",
    )

    def can_handle(self, command):
        if command.intent in self.RESEARCH_INTENTS:
            return True

        text = (
            command.original
            .lower()
            .strip()
        )

        return any(
            phrase in text
            for phrase in self.RESEARCH_PHRASES
        )

    def run(self, context):
        return AgentResult(
            success=True,
            agent=self.name,
            metadata={
                "delegate_to_existing_pipeline": True,
                "research_intent": context.command.intent,
            },
        )