from ai.agent.task import Task
from ai.planner.planner import Planner


class AppPlanner(Planner):
    """Plans application open/close commands."""

    def can_plan(self, command):
        return command.intent in (
            "open",
            "close",
        )

    def plan(self, command):
        tasks = []

        # =========================================================
        # OPEN
        # =========================================================

        if command.intent == "open":

            # -------------------------
            # Applications
            # -------------------------

            for app in command.entities.get("apps", []):
                tasks.append(
                    Task(
                        action="open",
                        target=app,
                    )
                )

            # -------------------------
            # Websites
            # -------------------------

            for website in command.entities.get("websites", []):
                tasks.append(
                    Task(
                        action="open",
                        target=website,
                    )
                )

        # =========================================================
        # CLOSE
        # =========================================================

        elif command.intent == "close":

            apps = command.entities.get(
                "apps",
                [],
            )

            if apps:

                for app in apps:
                    tasks.append(
                        Task(
                            action="close",
                            target=app,
                        )
                    )

            else:

                tasks.append(
                    Task(
                        action="close_last",
                        target="",
                    )
                )

        # =========================================================
        # DEBUG
        # =========================================================

        print("=" * 50)
        print("APP PLANNER")

        for task in tasks:
            print(task)

        print("=" * 50)

        return tasks