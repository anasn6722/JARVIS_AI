import re


class CommandSplitter:
    """
    Split independent commands while preserving commands that
    represent one desktop task.
    """

    ACTIONS = (
        "open",
        "close",
        "search",
        "play",
        "focus",
        "click",
        "type",
        "press",
    )

    # =========================================================
    # COMMANDS THAT MUST STAY TOGETHER
    # =========================================================

    COMPOSITE_PATTERNS = (
        # Open/search + type
        r"^open\s+search\b.*\btype\b",
        r"^open\s+the\s+search\b.*\btype\b",
        r"^search\b.*\btype\b",

        # UI focus/click + type
        r"^focus\b.*\btype\b",
        r"^click\b.*\btype\b",

        # UI action + keyboard action
        r"^focus\b.*\bpress\b",
        r"^click\b.*\bpress\b",
        r"^open\b.*\bpress\b",
    )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def split(self, text):
        """
        Split a user request into commands.

        Desktop composite commands are preserved as one command
        so the DesktopTaskComposer can process them.
        """

        if not text:
            return []

        text = str(text).strip()

        if not text:
            return []

        normalized = text.lower()

        # =====================================================
        # PRESERVE DESKTOP COMPOSITE COMMAND
        # =====================================================

        if self._is_composite_command(
            normalized
        ):
            return [text]

        # =====================================================
        # NORMAL SPLITTING
        # =====================================================

        parts = re.split(
            r"\bthen\b|,|\band\b",
            normalized,
        )

        commands = []
        current_action = None

        for part in parts:
            part = part.strip()

            if not part:
                continue

            words = part.split()

            if not words:
                continue

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

    # =========================================================
    # COMPOSITE DETECTION
    # =========================================================

    @classmethod
    def _is_composite_command(cls, text):
        """Return True for commands that must remain intact."""

        normalized = " ".join(
            text.strip().split()
        )

        for pattern in cls.COMPOSITE_PATTERNS:
            if re.search(
                pattern,
                normalized,
                flags=re.IGNORECASE,
            ):
                return True

        return False