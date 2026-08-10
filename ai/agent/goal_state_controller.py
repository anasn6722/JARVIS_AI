from ai.agent.goal_state import GoalState


class GoalStateController:
    """Control the lifecycle of a JARVIS goal."""

    def get_state(self, goal):
        return goal.state

    # ============================================================
    # START
    # ============================================================

    def start(self, goal):
        if goal.archived:
            return False, "Cannot start an archived goal."

        if goal.completed:
            return False, "Goal is already completed."

        goal.paused = False
        goal.state = GoalState.RUNNING

        return True, "Goal started."

    # ============================================================
    # PAUSE
    # ============================================================

    def pause(self, goal):
        if goal.archived:
            return False, "Cannot pause an archived goal."

        if goal.completed:
            return False, "Cannot pause a completed goal."

        goal.paused = True
        goal.state = GoalState.PAUSED

        return True, "Goal paused."

    # ============================================================
    # RESUME
    # ============================================================

    def resume(self, goal):
        if goal.archived:
            return False, "Cannot resume an archived goal."

        if goal.completed:
            return False, "Goal is already completed."

        goal.paused = False
        goal.state = GoalState.RUNNING

        return True, "Goal resumed."

    # ============================================================
    # COMPLETE
    # ============================================================

    def complete(self, goal):
        if goal.archived:
            return False, "Cannot complete an archived goal."

        goal.completed = True
        goal.progress = 100.0
        goal.paused = False
        goal.state = GoalState.COMPLETED

        return True, "Goal completed."

    # ============================================================
    # ARCHIVE
    # ============================================================

    def archive(self, goal):
        if not goal.completed:
            return False, "Only completed goals can be archived."

        goal.archived = True
        goal.paused = False
        goal.state = GoalState.ARCHIVED

        return True, "Goal archived."

    # ============================================================
    # RESTORE
    # ============================================================

    def restore(self, goal):
        if not goal.archived:
            return False, "Goal is not archived."

        goal.archived = False

        # A restored completed goal remains completed.
        if goal.completed:
            goal.state = GoalState.COMPLETED
        else:
            goal.state = GoalState.PENDING

        return True, "Goal restored."
