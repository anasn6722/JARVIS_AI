import json
from dataclasses import asdict
from pathlib import Path

from ai.memory.execution.execution_record import ExecutionRecord


class ExecutionMemory:
    """Persistent storage for JARVIS execution records."""


    def __init__(self, file_path=None):
        if file_path is None:
            file_path = (
                Path(__file__).resolve().parents[3]
                / "data"
                / "executions.json"
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
    # CLEAR
    # ========================================================

    def clear(self):
        self.executions.clear()
        self.save()

    # ========================================================
    # SAVE
    # ========================================================

    def save(self):
        data = [
            asdict(execution)
            for execution in self.executions
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
                default=str,
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
                execution = ExecutionRecord(
                    **item,
                )

                self.executions.append(
                    execution,
                )

            except Exception as error:
                print(
                    "ExecutionMemory load error:",
                    error,
                )
