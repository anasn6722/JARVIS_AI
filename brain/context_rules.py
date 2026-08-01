class ContextRules:

    @staticmethod
    def resolve(command, conversation):

        if (
            command.intent == "search"
            and not command.entities["websites"]
        ):

            previous = conversation.last_command

            if previous:

                if previous.intent == "open":

                    apps = previous.entities.get("apps", [])

                    if "chrome" in apps:

                        command.entities["websites"].append(
                            "google"
                        )

        return command