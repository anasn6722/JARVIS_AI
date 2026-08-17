from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base contract for all JARVIS specialist agents."""

    name = "base"
    description = "Base JARVIS agent"

    @abstractmethod
    def can_handle(self, command):
        """Return True when this agent can handle the command."""
        raise NotImplementedError

    @abstractmethod
    def run(self, context):
        """Execute the agent's task."""
        raise NotImplementedError