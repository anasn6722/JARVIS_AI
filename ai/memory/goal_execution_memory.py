import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from ai.memory.goal_execution import GoalExecution


class GoalExecutionMemory:
    """Persistent storage for JARVIS goal execution history."""

    def __init__(self, file_path=None):
        if file_path is None:
            file_path = (
                Path(__file__).resolve().parents[2]
                / "data"
                / "goal_execution_history.json"
            )

        self.file_path = Path(file_path)
        self.executions = []

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.load()

    # ========================================================
    # ADD
    # ========================================================

    def add(self, execution):
        self.executions.append(execution)
        self.save()

    # ========================================================
    # ALL
    # ========================================================

    def all(self):
        return list(self.executions)

    # ========================================================
    # BY GOAL
    # ========================================================

    def by_goal(self, goal_id):
        return [
            execution
            for execution in self.executions
            if execution.goal_id == goal_id
        ]

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self):
        self.executions.clear()
        self.save()

    # ========================================================
    # SAVE
    # ========================================================

    def save(self):
        data = []

        for execution in self.executions:
            item = asdict(execution)

            if execution.started:
                item["started"] = execution.started.isoformat()

            if execution.completed:
                item["completed"] = (
                    execution.completed.isoformat()
                )

            data.append(item)

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

    # ========================================================
    # LOAD
    # ========================================================

    def load(self):
        if not self.file_path.exists():
            self.executions = []
            return

        try:
            with self.file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except (json.JSONDecodeError, OSError):
            self.executions = []
            return

        if not isinstance(data, list):
            self.executions = []
            return

        self.executions = []

        for item in data:
            if not isinstance(item, dict):
                continue

            try:
                started = item.get("started")
                completed = item.get("completed")

                if isinstance(started, str):
                    started = datetime.fromisoformat(started)

                if isinstance(completed, str):
                    completed = datetime.fromisoformat(
                        completed,
                    )

                execution = GoalExecution(
                    goal_id=item.get(
                        "goal_id",
                        "",
                    ),
                    action=item.get(
                        "action",
                        "",
                    ),
                    target=item.get(
                        "target",
                        "",
                    ),
                    started=started,
                    completed=completed,
                    success=item.get(
                        "success",
                        False,
                    ),
                    result=item.get(
                        "result",
                        "",
                    ),
                    error=item.get(
                        "error",
                        "",
                    ),
                )

                self.executions.append(
                    execution,
                )

            except Exception as error:
                print(
                    "GoalExecutionMemory load error:",
                    error,
                )
