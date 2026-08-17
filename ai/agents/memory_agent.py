from ai.agents.base_agent import BaseAgent
from ai.orchestration.agent_result import AgentResult


class MemoryAgent(BaseAgent):
    """Handles JARVIS memory, profile, runtime, and goals."""

    name = "memory"

    description = (
        "Handles user profile, preferences, conversation memory, "
        "runtime references, goals, tasks, and execution history."
    )

    MEMORY_INTENTS = {
        "set_name",
        "get_name",
        "set_preference",
        "get_preference",
        "last_message",
        "history",
        "add_goal",
        "show_goals",
        "next_task",
        "complete_task",
        "complete_current_task",
        "goal_progress",
        "delete_goal",
        "close_last",
    }

    MEMORY_PHRASES = (
        "remember",
        "do you remember",
        "my name",
        "what is my name",
        "what's my name",
        "what do i like",
        "my favorite",
        "my preference",
        "what was the last",
        "last app",
        "last website",
        "last search",
        "last message",
        "show my goals",
        "what are my goals",
        "my goals",
        "next task",
        "goal progress",
        "complete task",
        "finish task",
        "delete goal",
        "remove goal",
    )

    def can_handle(self, command):
        if command.intent in self.MEMORY_INTENTS:
            return True

        text = (
            command.original
            .lower()
            .strip()
        )

        return any(
            phrase in text
            for phrase in self.MEMORY_PHRASES
        )

    def run(self, context):
        return AgentResult(
            success=True,
            agent=self.name,
            metadata={
                "delegate_to_existing_pipeline": True,
                "memory_intent": context.command.intent,
            },
        )