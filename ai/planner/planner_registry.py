class PlannerRegistry:

    def __init__(self):
        self.planners = []

    def register(self, planner):
        self.planners.append(planner)

    def get(self, command):

        for planner in self.planners:

            if planner.can_plan(command):

                print(f"Planner selected: {planner.__class__.__name__}")

                return planner

        print("No planner matched.")

        return None

    def plan(self, command):

        planner = self.get(command)

        if planner:
            return planner.plan(command)

        return []