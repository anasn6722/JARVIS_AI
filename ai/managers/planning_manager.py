from ai.agent.ai_planner import AIPlanner
from ai.agent.planner import Planner


class PlanningManager:

    def __init__(
        self,
        ai_planner: AIPlanner,
        planner: Planner,
        brain,
    ):
        self.ai_planner = ai_planner
        self.planner = planner
        self.brain = brain

    def plan(self, command):

        print("PlanningManager received:", command.intent)
    
        simple = {
            "open",
            "search",
            "youtube_search",
            "time",
            "identity",
            "set_name",
            "get_name",
            "history",
            "last_message",
            "add_goal",
            "show_goals",
        }
    
        if command.intent in simple:
            print("Using Rule Planner")
            tasks = self.planner.plan(command)
            print("Planner returned:", tasks)
            return tasks
    
        print("Using AI Planner")
    
        tasks = self.ai_planner.plan(
            command.original,
            self.brain.available_tools(),
            self.brain.planner_context(),
        )
    
        print("AI returned:", tasks)
    
        if not tasks:
            tasks = self.planner.plan(command)
    
        print("Final tasks:", tasks)
    
        return tasks