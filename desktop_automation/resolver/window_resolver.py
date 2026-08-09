class WindowResolver:
    """Resolve natural window names to actual desktop windows."""

    ALIASES = {
        "vs code": [
            "vs code",
            "vscode",
            "code",
            "visual studio code",
        ],
        "whatsapp": [
            "whatsapp",
            "whatsapp desktop",
        ],
        "whatsapp business": [
            "whatsapp business",
        ],
        "chatgpt": [
            "chatgpt",
            "chat gpt",
        ],
    }

    def __init__(self, window_manager):
        self.window_manager = window_manager

    def resolve(self, name):
        """Find a window using its name or a known alias."""

        if not name:
            return None

        name = name.lower().strip()

        # Direct search first
        window = self.window_manager.find_window(name)

        if window:
            return window

        # Alias search
        for canonical_name, aliases in self.ALIASES.items():

            if name not in aliases:
                continue

            for alias in aliases:

                window = self.window_manager.find_window(
                    alias
                )

                if window:
                    return window

        return None