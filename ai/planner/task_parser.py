from ai.agent.task import Task


class TaskParser:
    """Converts AI-generated task data into Task objects."""

    def parse(self, ai_tasks):
        """Convert a list of dictionaries into Task objects.

        Invalid task entries are ignored.
        Always returns a list.
        """

        tasks = []

        if not ai_tasks:
            return tasks

        for item in ai_tasks:
            if not isinstance(item, dict):
                continue

            action = item.get("action")
            target = item.get("target", "")

            if not action:
                continue

            tasks.append(
                Task(
                    action=action,
                    target=target,
                )
            )

        return tasks