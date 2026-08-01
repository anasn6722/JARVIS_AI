from ai.agent.task import Task


class Planner:

    def plan(self, command):

        tasks = []

        intent = command.intent

        entities = command.entities

        if intent == "open":

            apps = entities.get("apps", [])
            websites = entities.get("websites", [])

            for app in apps:
                tasks.append(Task("open", app))

            for website in websites:
                tasks.append(Task("open", website))

        elif intent == "close":

            apps = entities.get("apps", [])

            for app in apps:
                tasks.append(Task("close", app))

        elif intent == "search":

            for query in entities.get("searches", []):
                tasks.append(Task("search", query))

        elif intent == "youtube_search":

            searches = entities.get("searches", [])

            if searches:
                for query in searches:
                    tasks.append(
                        Task(
                            "youtube_search",
                            query,
                        )
                    )
            else:
                tasks.append(
                    Task(
                        "youtube_search",
                        "",
                    )
                )

        elif intent == "time":

            tasks.append(Task("time", ""))

        elif intent == "identity":

            tasks.append(Task("identity", ""))

        elif intent == "set_name":

            tasks.append(
                Task(
                    "set_name",
                    command.original,
                )
            )

        elif intent == "get_name":

            tasks.append(Task("get_name", ""))

        elif intent == "history":

            tasks.append(Task("history", ""))

        elif intent == "last_message":

            tasks.append(Task("last_message", ""))

        elif intent == "add_goal":

            tasks.append(
                Task(
                    "add_goal",
                    command.original,
                )
            )

        elif intent == "show_goals":

            tasks.append(Task("show_goals", ""))

        else:

            tasks.append(
                Task(
                    "chat",
                    command.original,
                )
            )

        print("=" * 50)
        print("RULE PLANNER TASKS")

        for task in tasks:
            print(task)

        print("=" * 50)

        return tasks