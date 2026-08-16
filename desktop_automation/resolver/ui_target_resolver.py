from dataclasses import dataclass


@dataclass(frozen=True)
class UITarget:
    """Normalized semantic UI target."""

    original: str
    target: str
    capability: str | None = None


class UITargetResolver:
    """
    Resolve natural-language UI references into stable semantic
    targets.

    This layer intentionally sits above UI Automation and below
    the command/planner layers.
    """

    # =========================================================
    # NORMALIZED TARGET ALIASES
    # =========================================================

    ALIASES = {
        # Search
        "search": "Search",
        "the search": "Search",
        "search icon": "Search",
        "the search icon": "Search",
        "search button": "Search",
        "the search button": "Search",
        "search panel": "Search",
        "the search panel": "Search",
        "search view": "Search",
        "the search view": "Search",

        # Explorer
        "explorer": "Explorer",
        "the explorer": "Explorer",
        "explorer button": "Explorer",
        "explorer icon": "Explorer",
        "the explorer icon": "Explorer",
        "file explorer": "Explorer",

        # File
        "file": "File",
        "the file": "File",
        "file menu": "File",
        "the file menu": "File",

        # Edit
        "edit": "Edit",
        "the edit": "Edit",
        "edit menu": "Edit",
        "the edit menu": "Edit",

        # Terminal
        "terminal": "Terminal",
        "the terminal": "Terminal",
        "terminal panel": "Terminal",
        "the terminal panel": "Terminal",

        # Chat
        "chat": "Toggle Chat",
        "the chat": "Toggle Chat",
        "chat button": "Toggle Chat",
        "the chat button": "Toggle Chat",
        "toggle chat": "Toggle Chat",

        # Quick access
        "quick access": "Open Quick Access",
        "the quick access": "Open Quick Access",
        "quick access button": "Open Quick Access",
    }

    # =========================================================
    # CAPABILITIES
    # =========================================================

    CAPABILITIES = {
        "Search": "search_ui",
        "Explorer": "explorer_ui",
    }

    # =========================================================
    # RESOLVE
    # =========================================================

    @classmethod
    def normalize(cls, text):
        """Normalize whitespace and casing."""

        if text is None:
            return ""

        text = str(text).strip().lower()

        return " ".join(
            text.split()
        )

    @classmethod
    def resolve(cls, text):
        """
        Resolve a natural-language UI target.

        Returns:
            UITarget | None
        """

        normalized = cls.normalize(text)

        if not normalized:
            return None

        target = cls.ALIASES.get(
            normalized
        )

        if target is not None:
            return UITarget(
                original=str(text),
                target=target,
                capability=cls.CAPABILITIES.get(
                    target
                ),
            )

        # -----------------------------------------------------
        # Generic cleanup
        # -----------------------------------------------------

        cleaned = normalized

        removable_prefixes = (
            "the ",
            "a ",
            "an ",
        )

        for prefix in removable_prefixes:
            if cleaned.startswith(prefix):
                cleaned = cleaned[
                    len(prefix):
                ]
                break

        removable_suffixes = (
            " button",
            " icon",
            " menu",
            " panel",
            " view",
        )

        for suffix in removable_suffixes:
            if cleaned.endswith(suffix):
                cleaned = cleaned[
                    :-len(suffix)
                ].strip()
                break

        target = cls.ALIASES.get(
            cleaned
        )

        if target is not None:
            return UITarget(
                original=str(text),
                target=target,
                capability=cls.CAPABILITIES.get(
                    target
                ),
            )

        # -----------------------------------------------------
        # Preserve unknown target.
        # -----------------------------------------------------

        return UITarget(
            original=str(text),
            target=str(text).strip(),
            capability=None,
        )

    # =========================================================
    # CAPABILITY
    # =========================================================

    @classmethod
    def capability(cls, text):
        """Return a capability name for a semantic target."""

        resolved = cls.resolve(text)

        if resolved is None:
            return None

        return resolved.capability

    # =========================================================
    # TARGET
    # =========================================================

    @classmethod
    def target(cls, text):
        """Return the normalized UI target."""

        resolved = cls.resolve(text)

        if resolved is None:
            return None

        return resolved.target