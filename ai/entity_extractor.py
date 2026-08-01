import re
from ai.aliases import APP_ALIASES
from brain.services import APPS, WEBSITES


class EntityExtractor:

    def extract(self, command: str):

        text = command.lower().strip()

        # Remove punctuation
        text = re.sub(r"[,.!?]", " ", text)

        # Normalize multiple spaces
        text = " ".join(text.split())
        entities = {
            "apps": [],
            "websites": [],
            "searches": [],
            "goals": [],
        }

        # ---------- APP ALIASES ----------
        for alias, app in APP_ALIASES.items():

            if alias in text and app not in entities["apps"]:
                entities["apps"].append(app)

        
        # ------------------------
        # Apps
        # ------------------------

        for app in APPS:
            if app in text and app not in entities["apps"]:
                entities["apps"].append(app)

        # ------------------------
        # Websites
        # ------------------------

        for website in WEBSITES:
            if website in text and website not in entities["websites"]:
                entities["websites"].append(website)

        # ------------------------
        # Search
        # ------------------------

        if command.startswith("search"):

            query = (
                text
                .replace("search", "", 1)
                .strip()
            )

            if query:
            
                queries = re.split(
                    r"\band\b|,|then",
                    query,
                )

                for item in queries:
                
                    item = item.strip()

                    if item:
                        entities["searches"].append(item)

        # ------------------------
        # Goals
        # ------------------------

        if command.startswith("my goal is"):

            goal = (
                text
                .replace("my goal is", "", 1)
                .strip()
            )

            if goal:
                entities["goals"].append(goal)

        # Remove duplicates
                
        for key in entities:
            entities[key] = list(dict.fromkeys(entities[key]))

        print("=" * 50)
        print("ENTITY EXTRACTOR")
        
        for key, value in entities.items():
            print(f"{key}: {value}")
        
        print("=" * 50)

        return entities
