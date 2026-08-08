import re

from ai.aliases import APP_ALIASES
from brain.services import APPS, WEBSITES


class EntityExtractor:
    """Extract applications, websites, searches, and goals from commands."""

    # ============================================================
    # REFERENCE WORDS
    # ============================================================

    REFERENCE_WORDS = {
        "it",
        "that",
        "there",
        "this",
        "last",
        "previous",
    }

    # ============================================================
    # EXTRACT ENTITIES
    # ============================================================

    def extract(self, command: str):
        """Extract structured entities from a command."""

        original = command

        text = command.lower().strip()

        # --------------------------------------------------------
        # Remove punctuation
        # --------------------------------------------------------

        text = re.sub(
            r"[,.!?]",
            " ",
            text,
        )

        # --------------------------------------------------------
        # Normalize spaces
        # --------------------------------------------------------

        text = " ".join(
            text.split()
        )

        # --------------------------------------------------------
        # Entity structure
        # --------------------------------------------------------

        entities = {
            "apps": [],
            "websites": [],
            "searches": [],
            "goals": [],
        }

        # ========================================================
        # REFERENCE DETECTION
        # ========================================================

        words = set(
            text.split()
        )

        has_reference = bool(
            words.intersection(
                self.REFERENCE_WORDS
            )
        )

        # ========================================================
        # APP ALIASES
        # ========================================================

        # Only extract applications when the command
        # contains an explicit application name.
        #
        # For commands such as:
        #
        #     close it
        #     open it
        #     close that
        #
        # the ReferenceResolver must decide the target.

        if not has_reference:

            for alias, app in APP_ALIASES.items():

                if (
                    alias in text
                    and app not in entities["apps"]
                ):
                    entities["apps"].append(
                        app
                    )

        # ========================================================
        # APPS
        # ========================================================

        if not has_reference:

            for app in APPS:

                if (
                    app in text
                    and app not in entities["apps"]
                ):
                    entities["apps"].append(
                        app
                    )

        # ========================================================
        # WEBSITES
        # ========================================================

        if not has_reference:

            for website in WEBSITES:

                if (
                    website in text
                    and website not in entities["websites"]
                ):
                    entities["websites"].append(
                        website
                    )

        # ========================================================
        # SEARCH
        # ========================================================

        if text.startswith("search"):

            query = (
                text
                .replace(
                    "search",
                    "",
                    1,
                )
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
                        entities["searches"].append(
                            item
                        )

        # ========================================================
        # GOALS
        # ========================================================

        goal = ""

        if text.startswith("my goal is"):

            goal = text.replace(
                "my goal is",
                "",
                1,
            ).strip()

        elif text.startswith("add goal"):

            goal = text.replace(
                "add goal",
                "",
                1,
            ).strip()

        elif text.startswith("create goal"):

            goal = text.replace(
                "create goal",
                "",
                1,
            ).strip()

        elif text.startswith("new goal"):

            goal = text.replace(
                "new goal",
                "",
                1,
            ).strip()

        if goal:
            entities["goals"].append(
                goal
            )

        # ========================================================
        # REMOVE DUPLICATES
        # ========================================================

        for key in entities:

            entities[key] = list(
                dict.fromkeys(
                    entities[key]
                )
            )

        # ========================================================
        # DEBUG
        # ========================================================

        print("=" * 50)
        print("ENTITY EXTRACTOR")

        for key, value in entities.items():

            print(
                f"{key}: {value}"
            )

        print("=" * 50)

        return entities
