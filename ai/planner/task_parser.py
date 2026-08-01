from ai.planner.task import Task


class TaskParser:
    """
    Converts raw AI output into Task objects.
    """

    def parse(self, ai_output: str):
        tasks = []

        if not ai_output:
            return tasks

        for line in ai_output.splitlines():

            line = line.strip()

            if not line:
                continue

            parts = line.split(":", 1)

            if len(parts) != 2:
                continue

            action = parts[0].strip().lower()
            target = parts[1].strip()

            tasks.append(
                Task(
                    action=action,
                    target=target,
                )
            )

        return tasks