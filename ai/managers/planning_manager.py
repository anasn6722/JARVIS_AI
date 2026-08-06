from ai.agent.ai_planner import AIPlanner


class PlanningManager:

    def __init__(
        self,
        planner_registry,
        ai_planner: AIPlanner,
        brain,
    ):
        self.registry = planner_registry
        self.ai_planner = ai_planner
        self.brain = brain

    def plan(self, command):

        # Rule-based planners
        tasks = self.registry.plan(command)

        if tasks:
            return tasks

        # AI Planner fallback
        return self.ai_planner.plan(
            command.original,
            self.brain.available_tools(),
            self.brain.planner_context(),
        )