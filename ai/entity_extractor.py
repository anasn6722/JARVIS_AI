from brain.services import APPS, WEBSITES


class EntityExtractor:

    def extract(self, command: str):

        command = command.lower()

        entities = {
            "apps": [],
            "websites": [],
            "searches": [],
            "goals": [],
        }

        # ------------------------
        # Apps
        # ------------------------

        for app in APPS:
            if app in command:
                entities["apps"].append(app)

        # ------------------------
        # Websites
        # ------------------------

        for website in WEBSITES:
            if website in command:
                entities["websites"].append(website)

        # ------------------------
        # Search
        # ------------------------

        if command.startswith("search"):

            query = (
                command
                .replace("search", "", 1)
                .strip()
            )

            if query:
                entities["searches"].append(query)

        # ------------------------
        # Goals
        # ------------------------

        if command.startswith("my goal is"):

            goal = (
                command
                .replace("my goal is", "", 1)
                .strip()
            )

            if goal:
                entities["goals"].append(goal)

        return entities