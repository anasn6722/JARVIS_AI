import re


class MemoryQueryParser:

    ALIASES = {

        # Birthday
        "what is my birthday": "birthday",
        "what's my birthday": "birthday",
        "tell me my birthday": "birthday",
        "my birthday": "birthday",

        # Name
        "what is my name": "name",
        "what's my name": "name",
        "tell me my name": "name",

        # Email
        "what is my email": "email",
        "what's my email": "email",
        "tell me my email": "email",

        # City
        "where do i live": "city",
        "where am i from": "city",
        "what is my city": "city",

        # University
        "where do i study": "university",

        # Language
        "what is my favorite language": "favorite_language",
        "what's my favorite language": "favorite_language",
        "favorite language": "favorite_language",
    }

    def extract(self, text: str):

        text = text.lower().strip()

        # Normalize contractions
        text = text.replace("what's", "what is")
        text = text.replace("who's", "who is")
        text = text.replace("where's", "where is")
        text = text.replace("how's", "how is")

        # Exact aliases
        if text in self.ALIASES:
            return self.ALIASES[text]

        # Generic patterns
        patterns = [

            r"what is my (.+)",
            r"tell me my (.+)",
            r"show me my (.+)",
            r"remember my (.+)",
            r"do you remember my (.+)",
        ]

        for pattern in patterns:

            match = re.search(pattern, text)

            if match:

                return (
                    match.group(1)
                    .strip()
                    .replace(" ", "_")
                )

        return None