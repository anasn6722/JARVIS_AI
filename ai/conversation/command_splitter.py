import re


class CommandSplitter:

    ACTIONS = (
        "open",
        "close",
        "search",
        "play",
    )

    def split(self, text):

        parts = re.split(
            r"\bthen\b|,|\band\b",
            text.lower().strip(),
        )

        commands = []

        current_action = None

        for part in parts:

            part = part.strip()

            if not part:
                continue

            words = part.split()

            if words[0] in self.ACTIONS:

                current_action = words[0]
                commands.append(part)

            elif current_action:

                commands.append(
                    f"{current_action} {part}"
                )

            else:

                commands.append(part)

        return commands