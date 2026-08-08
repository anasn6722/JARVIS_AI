from collections.abc import Callable

from ai.agent.ai_planner import AIPlanner


class PlanningManager:
    """Coordinates rule-based planners and AI planning fallback."""

    
    def __init__(
        self,
        planner_registry,
        ai_planner: AIPlanner,
        available_tools_provider: Callable[[], object],
        planner_context_provider: Callable[[], object],
    ):
        self.registry = planner_registry
        self.ai_planner = ai_planner
        self.available_tools_provider = available_tools_provider
        self.planner_context_provider = planner_context_provider

    def plan(self, command):
        """Create tasks for a command.

        Rule-based planners are tried first. If none of them can
        handle the command, the AI planner is used as a fallback.

        Always returns a list of tasks.
        """

        # ---------------------------------
        # Rule-based planning
        # ---------------------------------

        tasks = self.registry.plan(command)

        if tasks:
            return tasks

        # ---------------------------------
        # AI planning fallback
        # ---------------------------------

        tasks = self.ai_planner.plan(
            command.original,
            self.available_tools_provider(),
            self.planner_context_provider(),
        )

        return tasks or []
   
