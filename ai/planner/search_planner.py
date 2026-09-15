from ai.agent.task import Task
from ai.planner.planner import Planner


class SearchPlanner(Planner):
    """Plans web search, YouTube search, and search-result references."""

    SEARCH_RESULT_REFERENCES = {
        "open the first result": "first",
        "open first result": "first",
        "open the first one": "first",
        "open first": "first",
        "open the second result": "second",
        "open second result": "second",
        "open second": "second",
        "open the third result": "third",
        "open third result": "third",
        "open third": "third",
    }

    def can_plan(self, command):
        return command.intent in (
            "search",
            "youtube_search",
            "search_result",
        )

    def plan(self, command):
        tasks = []

        # =====================================================
        # GOOGLE SEARCH
        # =====================================================

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

        # =====================================================
        # YOUTUBE SEARCH
        # =====================================================

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

        # =====================================================
        # SEARCH RESULT REFERENCE
        # =====================================================

        elif command.intent == "search_result":

            original = (
                command.original
                or ""
            ).strip().lower()

            reference = (
                self.SEARCH_RESULT_REFERENCES.get(
                    original
                )
            )

            if reference is None:

                # Safe fallback for common variations.
                if "first" in original:
                    reference = "first"

                elif "second" in original:
                    reference = "second"

                elif "third" in original:
                    reference = "third"

            if reference is not None:

                tasks.append(
                    Task(
                        action="open_search_result",
                        target=reference,
                    )
                )

        # =====================================================
        # DEBUG
        # =====================================================

        print("=" * 50)
        print("SEARCH PLANNER")

        for task in tasks:
            print(task)

        print("=" * 50)

        return tasks