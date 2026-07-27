from config.constants import WAKE_WORD


class WakeWordDetector:
    def __init__(self):
        self.keyword = WAKE_WORD.lower()

    def detect(self, text: str) -> tuple[bool, str]:
        text = text.lower().strip()

        if text.startswith(self.keyword):
            command = text[len(self.keyword):].strip()
            return True, command

        return False, text