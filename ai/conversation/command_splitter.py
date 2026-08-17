import re


class CommandSplitter:
    """
    Split independent commands while preserving natural-language
    phrases and multi-step desktop commands.
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
        "find",
        "locate",
        "describe",
    )

    # =========================================================
    # PHRASES THAT MUST REMAIN ONE COMMAND
    # =========================================================

    COMPOSITE_PATTERNS = (
        # Search + typing
        r"^open\s+(?:the\s+)?search\b.*\btype\b",
        r"^search\b.*\btype\b",

        # UI interaction + typing
        r"^(?:focus|click)\b.*\btype\b",

        # UI interaction + keyboard action
        r"^(?:focus|click)\b.*\bpress\b",

        # Open + keyboard action
        r"^open\b.*\bpress\b",

        # Open + UI click
        r"^open\b.*\bclick\b",

        # Type + keyboard action
        r"^type\b.*\bpress\b",

        # Find + click
        r"^(?:find|locate)\b.*\bclick\b",

        # Find + type
        r"^(?:find|locate)\b.*\btype\b",

        
    )

    # =========================================================
    # "AND" PHRASES THAT ARE NATURAL LANGUAGE
    # =========================================================

    NON_COMMAND_AND_PHRASES = (
        "tell me",
        "show me",
        "give me",
        "let me",
        "help me",
        "find out",
        "check if",
        "what is",
        "what's",
        "how is",
        "who is",
        "where is",
        "when is",
        "why is",
        "and tell",
        "and show",
        "and give",
    )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def split(self, text):
        """
        Split a voice request into executable commands.

        Examples:

            open search and type Python
                -> one command

            open Chrome and tell me the time
                -> one command

            open Chrome and search Google for Python
                -> two commands

            open Chrome then search Google for Python
                -> two commands
        """

        if not text:
            return []

        text = str(text).strip()

        if not text:
            return []

        normalized = self._normalize(text)

        # -----------------------------------------------------
        # Preserve known composite desktop commands.
        # -----------------------------------------------------

        if self._is_composite_command(normalized):
            return [text]

        # -----------------------------------------------------
        # Find explicit command boundaries.
        # -----------------------------------------------------

        parts = self._split_on_command_boundaries(
            normalized
        )

        commands = []

        for part in parts:
            part = part.strip()

            if not part:
                continue

            commands.append(part)

        return commands

    # =========================================================
    # NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize(text):
        """Normalize whitespace and casing."""

        return " ".join(
            text.lower().strip().split()
        )

    # =========================================================
    # COMPOSITE DETECTION
    # =========================================================

    @classmethod
    def _is_composite_command(cls, text):
        """Return True when the whole request is one task."""

        for pattern in cls.COMPOSITE_PATTERNS:
            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            ):
                return True

        return False

    # =========================================================
    # ACTION DETECTION
    # =========================================================

    @classmethod
    def _starts_with_action(cls, text):
        """Check whether text starts with a known command action."""

        words = text.strip().split()

        if not words:
            return False

        return words[0] in cls.ACTIONS

    # =========================================================
    # COMMAND BOUNDARY SPLITTER
    # =========================================================

    @classmethod
    def _split_on_command_boundaries(cls, text):
        """
        Split only when the next phrase looks like a genuine
        new command.

        This avoids splitting ordinary language such as:

            open Chrome and tell me the time
        """

        # First normalize explicit "then".
        text = re.sub(
            r"\s+\bthen\b\s+",
            "|||",
            text,
            flags=re.IGNORECASE,
        )

        raw_parts = text.split("|||")

        if len(raw_parts) > 1:
            return [
                part.strip()
                for part in raw_parts
                if part.strip()
            ]

        # -----------------------------------------------------
        # Handle "and" intelligently.
        # -----------------------------------------------------

        words = text.split()

        if "and" not in words:
            return [text]

        result = []
        current = []

        index = 0

        while index < len(words):
            word = words[index]

            # ---------------------------------------------
            # Potential "and" boundary
            # ---------------------------------------------

            if word == "and":
                remainder = " ".join(
                    words[index + 1:]
                ).strip()

                # If the remainder starts with an action,
                # this is a likely second command.
                if cls._starts_with_action(
                    remainder
                ):
                    if current:
                        result.append(
                            " ".join(current).strip()
                        )

                    result.append(remainder)
                    return [
                        part
                        for part in result
                        if part
                    ]

                # Otherwise "and" is ordinary language.
                current.append(word)

            else:
                current.append(word)

            index += 1

        return [
            " ".join(current).strip()
        ]

    # =========================================================
    # DEBUG HELPER
    # =========================================================

    def explain(self, text):
        """
        Return the split result together with useful debugging
        information.
        """

        normalized = self._normalize(
            text
        )

        return {
            "original": text,
            "normalized": normalized,
            "composite": self._is_composite_command(
                normalized
            ),
            "commands": self.split(text),
        }