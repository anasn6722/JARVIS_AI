from typing import ClassVar


class GoalClassifier:
    """
    Detect long-term user goals while excluding ordinary
    desktop/filesystem/computer-control commands.
    """

    GOAL_KEYWORDS: ClassVar[set[str]] = {
        "build",
        "create",
        "make",
        "develop",
        "design",
        "learn",
        "study",
        "master",
        "plan",
        "organize",
        "prepare",
        "buy",
        "purchase",
        "order",
        "write",
        "generate",
        "improve",
        "upgrade",
        "fix",
        "start",
    }

    NON_GOAL_PREFIXES: ClassVar[tuple[str, ...]] = (
        # Applications
        "open ",
        "launch ",
        "start ",
        "run ",
        "close ",
        "exit ",
        "quit ",
        "terminate ",

        # Windows
        "focus ",
        "switch to ",
        "minimize ",
        "maximize ",
        "restore ",
        "list windows",
        "show windows",
        "show all windows",
        "list all windows",
        "active window",
        "current window",
        "close active window",
        "close current window",

        # Mouse
        "move mouse",
        "move the mouse",
        "move cursor",
        "move the cursor",
        "click ",
        "click on ",
        "double click",
        "double-click",
        "right click",
        "right-click",
        "middle click",
        "middle-click",
        "scroll up",
        "scroll down",
        "mouse position",
        "cursor position",

        # Keyboard
        "type ",
        "write text ",
        "enter text ",
        "press ",
        "hit ",
        "push ",
        "hotkey ",
        "keyboard shortcut",
        "key combination",

        # UI automation
        "find ",
        "locate ",
        "describe ",
        "select ",
        "activate ",
        "search ",

        # Filesystem
        "create a folder",
        "create folder",
        "make a folder",
        "make folder",
        "new folder",
        "create a file",
        "create file",
        "make a file",
        "make file",
        "new file",
        "list my desktop",
        "list desktop",
        "show my desktop files",
        "show desktop files",
        "list downloads",
        "show downloads",
        "list documents",
        "show documents",
        "list pictures",
        "show pictures",
        "list videos",
        "show videos",
        "list music",
        "show music",
        "copy ",
        "move ",
        "rename ",
        "find files ",
        "find all files ",
        "find all ",
        "find my files ",
        "search files ",
        "search my files ",
        "search for files ",
        "file info ",
        "file information ",
        "folder info ",
        "folder information ",
        "open path ",
        "open in explorer ",
    )

    def classify(self, command: str):
        """
        Return a goal object only for genuine long-term goals.

        Ordinary PC-control commands always return None.
        """

        if not command:
            return None

        normalized = " ".join(
            str(command).lower().split()
        )

        if not normalized:
            return None

        # -----------------------------------------------------
        # NEVER treat deterministic computer operations as goals
        # -----------------------------------------------------

        for prefix in self.NON_GOAL_PREFIXES:
            if normalized == prefix.rstrip():
                return None

            if normalized.startswith(prefix):
                return None

        # -----------------------------------------------------
        # Long-term goal detection
        # -----------------------------------------------------

        words = normalized.split()

        for word in words:
            if word in self.GOAL_KEYWORDS:
                return "goal"

        return None
