class GoalHandler:

    def __init__(self, brain):
        self.brain = brain

    def add_goal(self, command):

        if hasattr(command, "entities"):

            goals = command.entities.get(
                "goals",
                [],
            )

            if not goals:
                return "Please tell me your goal."

            goal = goals[0]

        else:
            goal = command.strip()

        existing = [
            g["title"].lower()
            for g in self.brain.goal_manager.all()
        ]

        if goal.lower() not in existing:
            self.brain.goal_manager.add(goal)

        try:
            tasks = self.brain.goal_ai_planner.create_plan(
                goal
            )

        except Exception:

            tasks = []

        for task in tasks:

            self.brain.goal_manager.add_task(
                goal,
                task,
            )

        self.brain.context.update(
            goal=goal,
        )

        return (
            f"I created a plan for {goal}. "
            f"It contains {len(tasks)} tasks."
        )

    def show_goals(self):

        goals = self.brain.goal_manager.all()

        if not goals:
            return "You don't have any goals."

        total = len(goals)

        completed = sum(
            1
            for goal in goals
            if goal["completed"]
        )

        current = goals[0]

        return (
            f"You have {total} goals. "
            f"{completed} are completed. "
            f"Your current goal is "
            f"{current['title']} "
            f"with {current['progress']} percent progress."
        )

    def next_task(self):

        goals = self.brain.goal_manager.all()

        if not goals:
            return "You don't have any goals."

        goal_name = self.brain.context.current_goal

        if goal_name:

            goal = next(
                (
                    g
                    for g in goals
                    if g["title"] == goal_name
                ),
                goals[0],
            )

        else:

            goal = goals[0]

        task = self.brain.goal_manager.next_task(
            goal["title"]
        )

        if not task:
            return "Everything is completed."

        self.brain.context.update(
            goal=goal["title"],
            task=task,
        )

        self.brain.context.add_task_history(
            task
        )

        return f"Your next task is {task}."

    def complete_task(self):

        goals = self.brain.goal_manager.all()

        if not goals:
            return "You don't have any goals."

        goal_name = self.brain.context.current_goal

        if goal_name:

            goal = next(
                (
                    g
                    for g in goals
                    if g["title"] == goal_name
                ),
                goals[0],
            )

        else:

            goal = goals[0]

        task = self.brain.goal_manager.next_task(
            goal["title"]
        )

        if not task:
            return "Everything is already completed."

        self.brain.goal_manager.complete_task(
            goal["title"],
            task,
        )

        self.brain.context.update(
            goal=goal["title"],
            task=task,
        )

        self.brain.context.add_task_history(
            task
        )

        progress = self.brain.goal_manager.progress(
            goal["title"]
        )

        return (
            f"Completed {task}. "
            f"Progress is now {progress}%."
        )

    def progress(self):

        goals = self.brain.goal_manager.all()

        if not goals:
            return "You don't have any goals."

        goal_name = self.brain.context.current_goal

        if goal_name:

            goal = next(
                (
                    g
                    for g in goals
                    if g["title"] == goal_name
                ),
                goals[0],
            )

        else:

            goal = goals[0]

        progress = self.brain.goal_manager.progress(
            goal["title"]
        )

        return (
            f"You have completed "
            f"{progress}% of "
            f"{goal['title']}."
        )

    def delete_goal(self):

        goals = self.brain.goal_manager.all()

        if not goals:
            return "You don't have any goals."

        goal_name = self.brain.context.current_goal

        if goal_name:

            goal = next(
                (
                    g
                    for g in goals
                    if g["title"] == goal_name
                ),
                goals[0],
            )

        else:

            goal = goals[0]

        self.brain.goal_manager.remove(
            goal["title"]
        )

        return (
            f"I removed the goal "
            f"{goal['title']}."
        )