from datetime import datetime
from uuid import uuid4

from ai.agent.goal_state import GoalState
from ai.agent.goal_state_controller import GoalStateController
from ai.agent.task import Task
from ai.memory.goal_record import GoalRecord


class GoalManager:
    """Service layer for persistent JARVIS goals."""

    def __init__(self, goal_memory):
        self.goal_memory = goal_memory
        self.state_controller = GoalStateController()

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    def _resolve_goal(self, goal):
        """Resolve a goal object, id, or title into GoalRecord."""

        if isinstance(goal, GoalRecord):
            return goal

        if goal is None:
            return None

        value = str(goal).strip()

        # Try goal ID first.
        found = self.goal_memory.get(value)

        if found is not None:
            return found

        # Then try title.
        for item in self.goal_memory.all():
            if item.title.lower() == value.lower():
                return item

        return None

    @staticmethod
    def _goal_summary(goal):
        """Return the legacy dictionary representation."""

        return {
            "id": goal.id,
            "title": goal.title,
            "created": goal.created,
            "tasks": goal.tasks,
            "completed": goal.completed,
            "progress": goal.progress,
            "paused": goal.paused,
            "archived": goal.archived,
            "state": goal.state.value,
            "description": goal.description,
            "metadata": goal.metadata,
        }

    # =========================================================
    # CREATE
    # =========================================================

    def create_goal(self, title, tasks=None):
        if tasks is None:
            tasks = []

        goal = GoalRecord(
            id=str(uuid4()),
            title=str(title).strip(),
            created=datetime.now(),
            tasks=list(tasks),
            state=GoalState.PENDING,
        )

        self.goal_memory.add(
            goal
        )

        return goal

    # =========================================================
    # COMPATIBILITY: ADD
    # =========================================================

    def add(self, title):
        """Compatibility wrapper used by GoalHandler."""

        existing = self._resolve_goal(title)

        if existing is not None:
            return existing

        return self.create_goal(
            title
        )

    # =========================================================
    # READ
    # =========================================================

    def get_goal(self, goal_id):
        return self.goal_memory.get(
            goal_id
        )

    def all_goals(self):
        """Return native GoalRecord objects."""

        return self.goal_memory.all()

    def all(self):
        """Compatibility API returning dictionaries."""

        return [
            self._goal_summary(
                goal
            )
            for goal in self.goal_memory.all()
        ]

    # =========================================================
    # ADD TASK
    # =========================================================

    def add_task(self, goal, task):
        """Add a task to a goal."""

        goal_record = self._resolve_goal(
            goal
        )

        if goal_record is None:
            return None

        # Goal planners may return a Task object.
        if isinstance(task, Task):
            task_object = task

        # Or they may return a plain string.
        else:
            task_object = Task(
                id=str(uuid4()),
                action=str(task),
                target="",
            )

        goal_record.tasks.append(
            task_object
        )

        self.update_progress(
            goal_record
        )

        self.goal_memory.save()

        return task_object

    # =========================================================
    # PROGRESS
    # =========================================================

    def update_progress(self, goal):
        """Recalculate goal progress."""

        goal = self._resolve_goal(
            goal
        )

        if goal is None:
            return None

        if not goal.tasks:
            goal.progress = 100.0
            goal.completed = True
            goal.paused = False
            goal.state = GoalState.COMPLETED

            self.goal_memory.save()

            return goal.progress

        completed = sum(
            1
            for task in goal.tasks
            if task.completed
        )

        goal.progress = (
            completed
            / len(goal.tasks)
        ) * 100.0

        if completed == len(
            goal.tasks
        ):
            goal.completed = True
            goal.paused = False
            goal.state = GoalState.COMPLETED

        elif completed > 0:
            goal.completed = False

            if not goal.paused:
                goal.state = GoalState.RUNNING

        else:
            goal.completed = False

            if not goal.paused:
                goal.state = GoalState.PENDING

        self.goal_memory.save()

        return goal.progress

    def progress(self, goal):
        """Compatibility API returning numeric progress."""

        goal_record = self._resolve_goal(
            goal
        )

        if goal_record is None:
            return 0

        self.update_progress(
            goal_record
        )

        return float(
            goal_record.progress
        )

    # =========================================================
    # NEXT TASK
    # =========================================================

    def next_task(self, goal):
        """Return the next incomplete task."""

        goal_record = self._resolve_goal(
            goal
        )

        if goal_record is None:
            return None

        for task in goal_record.tasks:
            if not task.completed:
                return task

        return None

    # =========================================================
    # COMPLETE TASK
    # =========================================================

    def complete_task(self, goal, task):
        """Mark a specific task as completed."""

        goal_record = self._resolve_goal(
            goal
        )

        if goal_record is None:
            return False

        task_object = None

        # If caller passed the actual Task object.
        if isinstance(task, Task):
            task_object = task

        else:
            task_text = str(task).strip().lower()

            for item in goal_record.tasks:
                candidates = (
                    str(
                        getattr(
                            item,
                            "action",
                            "",
                        )
                    ),
                    str(
                        getattr(
                            item,
                            "target",
                            "",
                        )
                    ),
                )

                if any(
                    candidate.lower()
                    == task_text
                    for candidate in candidates
                ):
                    task_object = item
                    break

        if task_object is None:
            return False

        task_object.completed = True
        task_object.success = True

        self.update_progress(
            goal_record
        )

        self.goal_memory.save()

        return True

    # =========================================================
    # DELETE
    # =========================================================

    def delete_goal(self, goal_id):
        self.goal_memory.remove(
            goal_id
        )

    def remove(self, goal):
        """Compatibility API supporting ID or title."""

        goal_record = self._resolve_goal(
            goal
        )

        if goal_record is None:
            return False

        self.goal_memory.remove(
            goal_record.id
        )

        return True

    # =========================================================
    # STATE
    # =========================================================

    def get_state(self, goal_id):
        goal = self.get_goal(
            goal_id
        )

        if goal is None:
            return None

        return self.state_controller.get_state(
            goal
        )

    # =========================================================
    # START
    # =========================================================

    def start_goal(self, goal_id):
        goal = self.get_goal(
            goal_id
        )

        if goal is None:
            return False, "Goal not found."

        result = self.state_controller.start(
            goal
        )

        self.goal_memory.save()

        return result

    # =========================================================
    # PAUSE
    # =========================================================

    def pause_goal(self, goal_id):
        goal = self.get_goal(
            goal_id
        )

        if goal is None:
            return False, "Goal not found."

        result = self.state_controller.pause(
            goal
        )

        self.goal_memory.save()

        return result

    # =========================================================
    # RESUME
    # =========================================================

    def resume_goal(self, goal_id):
        goal = self.get_goal(
            goal_id
        )

        if goal is None:
            return False, "Goal not found."

        result = self.state_controller.resume(
            goal
        )

        self.goal_memory.save()

        return result

    # =========================================================
    # COMPLETE GOAL
    # =========================================================

    def complete_goal(self, goal_id):
        goal = self.get_goal(
            goal_id
        )

        if goal is None:
            return False, "Goal not found."

        result = self.state_controller.complete(
            goal
        )

        self.goal_memory.save()

        return result

    # =========================================================
    # ARCHIVE
    # =========================================================

    def archive_goal(self, goal_id):
        goal = self.get_goal(
            goal_id
        )

        if goal is None:
            return False, "Goal not found."

        result = self.state_controller.archive(
            goal
        )

        self.goal_memory.save()

        return result

    # =========================================================
    # RESTORE
    # =========================================================

    def restore_goal(self, goal_id):
        goal = self.get_goal(
            goal_id
        )

        if goal is None:
            return False, "Goal not found."

        result = self.state_controller.restore(
            goal
        )

        self.goal_memory.save()

        return result