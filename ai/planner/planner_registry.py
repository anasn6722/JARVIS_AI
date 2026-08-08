class PlannerRegistry:
    """Registry for rule-based planners."""

    
    def __init__(self):
        self.planners = []

    def register(self, planner):
        """Register a planner."""
        self.planners.append(planner)

    def get(self, command):
        """Return the first planner capable of handling the command."""

        for planner in self.planners:
            if planner.can_plan(command):
                print(
                    f"Planner selected: "
                    f"{planner.__class__.__name__}"
                )
                return planner

        print("No planner matched.")
        return None

    def plan(self, command):
        """Plan a command using a matching rule-based planner.

        Returns:
            list: A list of Task objects.
        """

        planner = self.get(command)

        if not planner:
            return []

        tasks = planner.plan(command)

        return tasks or []

