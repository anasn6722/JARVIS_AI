from ai.task import Task


class Planner:
    def __init__(self, brain):
        self.brain = brain

    def plan(self, command):

        tasks = []

        entities = command.entities

        # ---------- OPEN ----------
        if command.intent == "open":

            text = command.original.lower()

            # Open favourite browser
            if "favorite browser" in text or "favourite browser" in text:

                browser = self.brain.long_memory.profile.get(
                    "favorite_browser"
                )

                if browser:
                    tasks.append(Task("open", browser))
                    return tasks

            # Open favourite IDE
            if "favorite ide" in text or "favourite ide" in text:

                ide = self.brain.long_memory.profile.get(
                    "favorite_ide"
                )

                if ide:
                    tasks.append(Task("open", ide))
                    return tasks

            # Open favourite editor
            if "favorite editor" in text or "favourite editor" in text:

                editor = self.brain.long_memory.profile.get(
                    "favorite_editor"
                )

                if editor:
                    tasks.append(Task("open", editor))
                    return tasks

            # Existing behaviour
            for app in entities.get("apps", []):
                tasks.append(Task("open", app))

            for website in entities.get("websites", []):
                tasks.append(Task("open", website))

        # ---------- CLOSE ----------
        elif command.intent == "close":

            # "close chrome"
            if entities.get("apps"):

                for app in entities["apps"]:
                    tasks.append(Task("close", app))

            # "close it"
            else:

                tasks.append(Task("close_last"))

        # ---------- SEARCH ----------
        elif command.intent == "search":

            for query in entities.get("searches", []):

                tasks.append(
                    Task(
                        "search",
                        query,
                    )
                )

        # ---------- TIME ----------
        elif command.intent == "time":

            tasks.append(
                Task("time")
            )

        return tasks