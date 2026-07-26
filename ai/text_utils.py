import re


class TextUtils:
    @staticmethod
    def normalize(command: str):
        command = command.lower()

        command = re.sub(
            r"[^\w\s]",
            "",
            command,
        )

        command = " ".join(command.split())

        return command