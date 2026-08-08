from ai.agent.task import Task
from ai.planner.planner import Planner


class SearchPlanner(Planner):
    """Plans web and YouTube search commands."""

    def can_plan(self, command):
        return command.intent in (
            "search",
            "youtube_search",
        )

    def plan(self, command):
        tasks = []

        # -------------------------
        # GOOGLE SEARCH
        # -------------------------

        if command.intent == "search":
            searches = command.entities.get(
                "searches",
                [],
            )

            for query in searches:
                tasks.append(
                    Task(
                        action="search",
                        target=query,
                    )
                )

        # -------------------------
        # YOUTUBE SEARCH
        # -------------------------

        elif command.intent == "youtube_search":
            searches = command.entities.get(
                "searches",
                [],
            )

            if searches:
                for query in searches:
                    tasks.append(
                        Task(
                            action="youtube_search",
                            target=query,
                        )
                    )
            else:
                tasks.append(
                    Task(
                        action="youtube_search",
                        target="",
                    )
                )

        # -------------------------
        # DEBUG
        # -------------------------

        print("=" * 50)
        print("SEARCH PLANNER")

        for task in tasks:
            print(task)

        print("=" * 50)

        return tasks