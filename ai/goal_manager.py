from datetime import datetime
from uuid import uuid4

from ai.memory.goal_record import GoalRecord


class GoalManager:

    def __init__(self, goal_memory):
        self.goal_memory = goal_memory

    # -------------------------
    # Create Goal
    # -------------------------

    def create_goal(self, title, tasks):

        goal = GoalRecord(
            id=str(uuid4()),
            title=title,
            created=datetime.now(),
            tasks=tasks,
        )

        self.goal_memory.add(goal)

        return goal

    # -------------------------
    # Read
    # -------------------------

    def get_goal(self, goal_id):

        return self.goal_memory.get(goal_id)

    def all_goals(self):

        return self.goal_memory.all()

    # -------------------------
    # Delete
    # -------------------------

    def delete_goal(self, goal_id):

        self.goal_memory.remove(goal_id)

    # -------------------------
    # Progress
    # -------------------------

    def update_progress(self, goal):

        if not goal.tasks:

            goal.progress = 100
            goal.completed = True
            return

        completed = sum(
            task.completed
            for task in goal.tasks
        )

        goal.progress = (
            completed / len(goal.tasks)
        ) * 100

        goal.completed = (
            completed == len(goal.tasks)
        )

    # -------------------------
    # Next Task
    # -------------------------

    def next_task(self, goal):

        for task in goal.tasks:

            if not task.completed:

                return task

        return None