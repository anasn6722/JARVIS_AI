import re


class TextNormalizer:

    def normalize(self, text: str) -> str:

        text = text.lower().strip()

        replacements = {
            "launch": "open",
            "start": "open",
            "run": "open",
            "please": "",
            "could you": "",
            "can you": "",
            "would you": "",
            "kindly": "",
            "favourite": "favorite",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        text = re.sub(r"\s+", " ", text)

        return text.strip()