from ai.task import Task


class Planner:

    def plan(self, command):

        tasks = []

        entities = command.entities

        # ---------- OPEN ----------
        if command.intent == "open":

            for app in entities.get("apps", []):
                tasks.append(Task("open", app))

            for website in entities.get("websites", []):
                tasks.append(Task("open", website))

        # ---------- SEARCH ----------
        if command.intent == "search":

            for query in entities.get("searches", []):

                tasks.append(
                    Task(
                        "search",
                        query,
                    )
                )

        # ---------- TIME ----------
        if command.intent == "time":

            tasks.append(
                Task("time")
            )

        return tasks