from ai.agent.task import Task


class Planner:

    def plan(self, command):

        tasks = []

        intent = command.intent

        if intent == "open":

            apps = command.entities.get("apps", [])

            for app in apps:
                tasks.append(Task("open", app))

        elif intent == "search":

            searches = command.entities.get("searches", [])

            if searches:
                tasks.append(Task("search", searches[0]))

        elif intent == "youtube_search":

            searches = command.entities.get("searches", [])

            if searches:
                tasks.append(Task("youtube_search", searches[0]))
            else:
                tasks.append(Task("youtube_search", ""))

        elif intent == "time":

            tasks.append(Task("time", ""))

        elif intent == "identity":

            tasks.append(Task("identity", ""))

        elif intent == "set_name":

            tasks.append(Task("set_name", command.original))

        elif intent == "get_name":

            tasks.append(Task("get_name", ""))

        elif intent == "history":

            tasks.append(Task("history", ""))

        elif intent == "last_message":

            tasks.append(Task("last_message", ""))

        elif intent == "add_goal":

            tasks.append(Task("add_goal", command.original))

        elif intent == "show_goals":

            tasks.append(Task("show_goals", ""))

        else:

            tasks.append(Task("chat", command.original))

        return tasks