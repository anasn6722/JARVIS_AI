from ai.aliases import APP_ALIASES
from brain.services import APPS, WEBSITES


class EntityExtractor:

    def extract(self, command: str):

        command = command.lower()
        text = command
        entities = {
            "apps": [],
            "websites": [],
            "searches": [],
            "goals": [],
        }

        # ---------- APP ALIASES ----------
        for alias, app in APP_ALIASES.items():

            if alias in text:
                entities["apps"].append(app)

        
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

        # Remove duplicates
                
        entities["apps"] = list(set(entities["apps"]))

        return entities
