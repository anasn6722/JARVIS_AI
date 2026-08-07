class PlanningStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        context.tasks = []

        for item in context.decisions:

            command = item["command"]
            decision = item["decision"]

            # Skip commands that don't require planning
            if decision.route != "PLANNER":
                continue

            tasks = self.brain.planning_manager.plan(
                command
            )
            
            context.tasks.extend(tasks)
            
            context.graph = self.brain.graph_builder.build(
                tasks
            )

        print("=" * 50)
        print("ALL PLANNED TASKS")

        for task in context.tasks:
            print(task)

        print("=" * 50)