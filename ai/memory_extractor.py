import re
from typing import ClassVar


class MemoryExtractor:

    PATTERNS: ClassVar[list[tuple[str, str]]] = [
        (r"my (.+) is (.+)", "my"),
        (r"i am (.+)", "iam"),
        (r"i live in (.+)", "city"),
        (r"remember that (.+) is (.+)", "remember"),
    ]

    def extract(self, text: str):
        text = text.lower().strip()

        text = text.replace("favourite", "favorite")

        match = re.match(r"my (.+?) is (.+)", text)

        if match:
            key = match.group(1).strip().replace(" ", "_")
            value = match.group(2).strip()
            return key, value

        if text.startswith("i live in "):
            return "city", text.replace("i live in ", "").strip()

        return None, None