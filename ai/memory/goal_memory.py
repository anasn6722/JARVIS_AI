
import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from ai.agent.goal_state import GoalState
from ai.agent.task import Task
from ai.memory.goal_record import GoalRecord


class GoalMemory:
    """Persistent storage for JARVIS goals."""

    def __init__(self, file_path=None):
        if file_path is None:
            file_path = (
                Path(__file__).resolve().parents[2]
                / "data"
                / "goals.json"
            )

        self.file_path = Path(file_path)
        self.goals = {}

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.load()

    # ============================================================
    # ADD
    # ============================================================

    def add(self, goal):
        self.goals[goal.id] = goal
        self.save()

    # ============================================================
    # GET
    # ============================================================

    def get(self, goal_id):
        return self.goals.get(goal_id)

    # ============================================================
    # ALL
    # ============================================================

    def all(self):
        return list(self.goals.values())

    # ============================================================
    # REMOVE
    # ============================================================

    def remove(self, goal_id):
        self.goals.pop(goal_id, None)
        self.save()

    # ============================================================
    # CLEAR
    # ============================================================

    def clear(self):
        self.goals.clear()
        self.save()

    # ============================================================
    # SAVE
    # ============================================================

    def save(self):
        data = [
            self._goal_to_dict(goal)
            for goal in self.goals.values()
        ]

        with self.file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return True

    # ============================================================
    # LOAD
    # ============================================================

    def load(self):
        if not self.file_path.exists():
            self.goals = {}
            return

        try:
            with self.file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except (json.JSONDecodeError, OSError):
            self.goals = {}
            return

        if not isinstance(data, list):
            self.goals = {}
            return

        self.goals = {}

        for item in data:
            if not isinstance(item, dict):
                continue

            try:
                goal = self._goal_from_dict(item)
                self.goals[goal.id] = goal

            except Exception as error:
                print(
                    "GoalMemory load error:",
                    error,
                )

    # ============================================================
    # SERIALIZATION
    # ============================================================

    def _goal_to_dict(self, goal):
        return {
            "id": goal.id,
            "title": goal.title,
            "created": goal.created.isoformat(),
            "tasks": [
                {
                    "id": task.id,
                    "action": task.action,
                    "target": task.target,
                    "depends_on": task.depends_on,
                    "completed": task.completed,
                    "success": task.success,
                    "retry_count": task.retry_count,
                    "max_retries": task.max_retries,
                    "result": task.result,
                    "error": task.error,
                }
                for task in goal.tasks
            ],
            "completed": goal.completed,
            "progress": goal.progress,
            "paused": goal.paused,
            "archived": goal.archived,
            "state": goal.state.value,
            "description": goal.description,
            "metadata": goal.metadata,
        }

    # ============================================================
    # DESERIALIZATION
    # ============================================================

    def _goal_from_dict(self, data):
        goal_id = data.get("id")

        # Compatibility with old goals.json
        if not goal_id:
            goal_id = str(uuid4())

        created = data.get("created")

        if isinstance(created, str):
            try:
                created = datetime.fromisoformat(created)
            except ValueError:
                created = datetime.now()

        elif not isinstance(created, datetime):
            created = datetime.now()

        tasks = []

        for task_data in data.get("tasks", []):
            if not isinstance(task_data, dict):
                continue

            # New task format
            if "action" in task_data:
                task = Task(
                    id=task_data.get("id", ""),
                    action=task_data.get("action", ""),
                    target=task_data.get("target", ""),
                    depends_on=task_data.get(
                        "depends_on",
                        [],
                    ),
                    completed=task_data.get(
                        "completed",
                        False,
                    ),
                    success=task_data.get(
                        "success",
                        False,
                    ),
                    retry_count=task_data.get(
                        "retry_count",
                        0,
                    ),
                    max_retries=task_data.get(
                        "max_retries",
                        2,
                    ),
                    result=task_data.get(
                        "result",
                        "",
                    ),
                    error=task_data.get(
                        "error",
                        "",
                    ),
                )

            # Old task format
            else:
                task = Task(
                    action=task_data.get(
                        "task",
                        "",
                    ),
                    completed=task_data.get(
                        "done",
                        False,
                    ),
                    success=task_data.get(
                        "done",
                        False,
                    ),
                )

            tasks.append(task)


        state_value = data.get("state", "pending")

        try:
            state = GoalState(state_value)
        except ValueError:
            state = GoalState.PENDING

        return GoalRecord(
            id=goal_id,
            title=data.get(
                "title",
                "Untitled Goal",
            ),
            created=created,
            tasks=tasks,
            completed=data.get(
                "completed",
                False,
            ),
            progress=float(
                data.get(
                    "progress",
                    0.0,
                )
            ),
            paused=data.get(
                "paused",
                False,
            ),
            archived=data.get(
                "archived",
                False,
            ),
            state=state,
            description=data.get(
                "description",
                "",
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )
