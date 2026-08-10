class GoalHistory:
    """Manage the lifecycle of stored goals."""

    def __init__(self, goal_memory):
        self.goal_memory = goal_memory

    # ============================================================
    # PAUSE
    # ============================================================

    def pause(self, goal_id):
        goal = self.goal_memory.get(goal_id)

        if goal is None:
            return False, "Goal not found."

        if goal.completed:
            return False, "Completed goals cannot be paused."

        if goal.archived:
            return False, "Archived goals cannot be paused."

        goal.paused = True

        return True, "Goal paused."

    # ============================================================
    # RESUME
    # ============================================================

    def resume(self, goal_id):
        goal = self.goal_memory.get(goal_id)

        if goal is None:
            return False, "Goal not found."

        if goal.archived:
            return False, "Archived goals cannot be resumed."

        if goal.completed:
            return False, "Goal is already completed."

        goal.paused = False

        return True, "Goal resumed."

    # ============================================================
    # ARCHIVE
    # ============================================================

    def archive(self, goal_id):
        goal = self.goal_memory.get(goal_id)

        if goal is None:
            return False, "Goal not found."

        if not goal.completed:
            return False, "Only completed goals can be archived."

        goal.archived = True
        goal.paused = False

        return True, "Goal archived."

    # ============================================================
    # RESTORE
    # ============================================================

    def restore(self, goal_id):
        goal = self.goal_memory.get(goal_id)

        if goal is None:
            return False, "Goal not found."

        if not goal.archived:
            return False, "Goal is not archived."

        goal.archived = False

        return True, "Goal restored."

    # ============================================================
    # ACTIVE GOALS
    # ============================================================

    def active(self):
        return [
            goal
            for goal in self.goal_memory.all()
            if not goal.completed
            and not goal.paused
            and not goal.archived
        ]

    # ============================================================
    # PAUSED GOALS
    # ============================================================

    def paused(self):
        return [
            goal
            for goal in self.goal_memory.all()
            if goal.paused
            and not goal.archived
        ]

    # ============================================================
    # COMPLETED GOALS
    # ============================================================

    def completed(self):
        return [
            goal
            for goal in self.goal_memory.all()
            if goal.completed
            and not goal.archived
        ]

    # ============================================================
    # ARCHIVED GOALS
    # ============================================================

    def archived(self):
        return [
            goal
            for goal in self.goal_memory.all()
            if goal.archived
        ]