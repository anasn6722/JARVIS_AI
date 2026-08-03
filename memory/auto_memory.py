import re
from typing import ClassVar


class AutoMemoryExtractor:

    PATTERNS: ClassVar[list[tuple[str, str]]] = [

        (
            r"i live in (.+)",
            "city",
        ),

        (
            r"my name is (.+)",
            "name",
        ),

        (
            r"i am (?:a|an) (.+)",
            "occupation",
        ),

        (
            r"my birthday is (.+)",
            "birthday",
        ),

        (
            r"i was born on (.+)",
            "birthday",
        ),

        (
            r"my favorite language is (.+)",
            "favorite_language",
        ),

        (
            r"i use (.+)",
            "favorite_tool",
        ),

        (
            r"i study at (.+)",
            "university",
        ),

        (
            r"my email is (.+)",
            "email",
        ),
    ]
    def extract(self, text):

        text = text.lower().strip()

        for pattern, key in self.PATTERNS:

            match = re.search(pattern, text)

            if match:

                return (
                    key,
                    match.group(1).strip(),
                )

        return None