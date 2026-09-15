from ai.agent.goal_classifier import GoalClassifier
from ai.command import Command
from ai.context_resolver import ContextResolver
from ai.conversation.command_splitter import CommandSplitter
from ai.conversation.reference_resolver import ReferenceResolver
from ai.entity_extractor import EntityExtractor
from ai.intent_classifier import IntentClassifier
from ai.text_utils import TextUtils


class CommandManager:
    """
    Convert raw user commands into normalized Command objects.

    Desktop/filesystem commands are resolved before goal promotion
    so phrases such as "create a folder" are not accidentally
    classified as memory/goal commands.
    """

    # =========================================================
    # PLANNER INTENTS
    # =========================================================

    PLANNER_INTENTS = {
        # Applications
        "open",
        "close",
        "close_last",

        # Desktop windows
        "focus_window",
        "close_window",
        "close_active_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",
        "active_window",
        "list_windows",

        # Mouse
        "mouse_position",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll_up",
        "mouse_scroll_down",

        # Keyboard
        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",

        # Semantic UI
        "ui_find",
        "ui_click",
        "ui_focus",
        "ui_click_at",
        "ui_describe",
        "ui_type",
        "ui_find_descriptor",
        "ui_click_descriptor",
        "ui_type_descriptor",

        # Desktop search
        "search_ui",
        "open_search_result",

        # Filesystem
        "path_exists",
        "list_directory",
        "create_folder",
        "create_file",
        "read_file",
        "file_info",
        "copy",
        "move",
        "rename",
        "search_files",
        "open_path",
        "open_in_explorer",
    }

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(
        self,
        context,
        intent_classifier,
        entity_extractor,
        goal_classifier,
        reference_resolver,
    ):
        self.context = context
        self.intent_classifier = intent_classifier
        self.entity_extractor = entity_extractor
        self.goal_classifier = goal_classifier
        self.command_splitter = CommandSplitter()
        self.context_resolver = ContextResolver(context)
        self.reference_resolver = reference_resolver

    # =========================================================
    # PROCESS SINGLE
    # =========================================================

    def process_single(
        self,
        command: str,
    ):
        original = command

        command = TextUtils.normalize(
            command
        )

        command = self.context_resolver.resolve(
            command
        )

        entities = self.entity_extractor.extract(
            command
        )

        # -----------------------------------------------------
        # Determine ordinary intent first
        # -----------------------------------------------------

        result = self.intent_classifier.classify(
            command
        )

        # -----------------------------------------------------
        # Filesystem priority
        # -----------------------------------------------------

        filesystem_intent = (
            self._detect_filesystem_intent(
                command
            )
        )

        if filesystem_intent:
            result = {
                "intent": filesystem_intent,
                "destination": "BRAIN",
            }

            goal = None

        else:
            goal = self.goal_classifier.classify(
                command
            )

            # -------------------------------------------------
            # Goal promotion
            # -------------------------------------------------

            if (
                goal
                and result["intent"] == "chat"
            ):
                result["intent"] = "add_goal"
                result["destination"] = "BRAIN"

        command_data = Command(
            original=original,
            intent=result["intent"],
            destination=result["destination"],
            entities=entities,
            requires_planning=(
                goal is not None
                or result["intent"]
                in self.PLANNER_INTENTS
            ),
        )

        command_data = (
            self.reference_resolver.resolve(
                command_data
            )
        )

        return command_data, goal

    # =========================================================
    # PROCESS
    # =========================================================

    def process(
        self,
        command: str,
    ):
        original = command

        command = TextUtils.normalize(
            command
        )

        command = self.context_resolver.resolve(
            command
        )

        entities = self.entity_extractor.extract(
            command
        )

        # -----------------------------------------------------
        # Classify normal intent FIRST
        # -----------------------------------------------------

        result = self.intent_classifier.classify(
            command
        )

        # -----------------------------------------------------
        # Filesystem gets priority over goal detection
        # -----------------------------------------------------

        filesystem_intent = (
            self._detect_filesystem_intent(
                command
            )
        )

        if filesystem_intent:

            result = {
                "intent": filesystem_intent,
                "destination": "BRAIN",
            }

            goal = None

        else:

            goal = self.goal_classifier.classify(
                command
            )

            # -------------------------------------------------
            # Goal Promotion
            # -------------------------------------------------

            if (
                goal
                and result["intent"] == "chat"
            ):
                result["intent"] = "add_goal"
                result["destination"] = "BRAIN"

        command_data = Command(
            original=original,
            intent=result["intent"],
            destination=result["destination"],
            entities=entities,
            goal=goal,
            requires_planning=(
                goal is not None
                or result["intent"]
                in self.PLANNER_INTENTS
            ),
        )

        command_data = (
            self.reference_resolver.resolve(
                command_data
            )
        )

        return command_data, goal

    # =========================================================
    # FILESYSTEM INTENT DETECTION
    # =========================================================

    @staticmethod
    def _detect_filesystem_intent(
        text: str,
    ) -> str | None:
        """
        Detect deterministic filesystem commands.

        This runs before goal promotion because words such as
        "create" and "make" are also common goal-language words.
        """

        if not text:
            return None

        normalized = " ".join(
            str(text).lower().split()
        )

        # -----------------------------------------------------
        # CREATE FOLDER
        # -----------------------------------------------------

        folder_phrases = (
            "create a folder",
            "create folder",
            "make a folder",
            "make folder",
            "new folder",
        )

        if normalized.startswith(
            folder_phrases
        ):
            return "create_folder"

        # -----------------------------------------------------
        # CREATE FILE
        # -----------------------------------------------------

        file_phrases = (
            "create a file",
            "create file",
            "make a file",
            "make file",
            "new file",
        )

        if normalized.startswith(
            file_phrases
        ):
            return "create_file"

        # -----------------------------------------------------
        # DIRECTORY LISTING
        # -----------------------------------------------------

        if normalized.startswith(
            (
                "list my desktop",
                "list desktop",
                "show my desktop files",
                "show desktop files",
            )
        ):
            return "list_directory"

        if normalized.startswith(
            (
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
            )
        ):
            return "list_directory"

        if normalized.startswith(
            (
                "list files in ",
                "list the files in ",
                "show files in ",
                "show the files in ",
                "show what is in ",
                "show what's in ",
            )
        ):
            return "list_directory"

        
        # -----------------------------------------------------
        # FILE SEARCH
        # -----------------------------------------------------

        if normalized.startswith(
            (
                "find files ",
                "find my files ",
                "find all files ",
                "find all ",
                "search files ",
                "search my files ",
                "search for files ",
            )
        ) and " files" in normalized:
            return "search_files"


        # -----------------------------------------------------
        # FILE INFORMATION
        # -----------------------------------------------------

        if normalized.startswith(
            (
                "what is this file",
                "what is this folder",
                "file information",
                "file info",
                "folder information",
                "folder info",
            )
        ):
            return "file_info"

        # -----------------------------------------------------
        # COPY
        # -----------------------------------------------------

        if normalized.startswith(
            (
                "copy ",
                "copy the file ",
                "copy the folder ",
            )
        ):
            return "copy"

        # -----------------------------------------------------
        # MOVE
        # -----------------------------------------------------

        if normalized.startswith(
            (
                "move ",
                "move the file ",
                "move the folder ",
            )
        ):
            return "move"

        # -----------------------------------------------------
        # RENAME
        # -----------------------------------------------------

        if normalized.startswith(
            (
                "rename ",
                "rename the file ",
                "rename the folder ",
            )
        ):
            return "rename"

        # -----------------------------------------------------
        # OPEN KNOWN WINDOWS LOCATIONS
        # -----------------------------------------------------

        if normalized in {
            "open desktop",
            "open my desktop",
            "open downloads",
            "open my downloads",
            "open documents",
            "open my documents",
            "open pictures",
            "open my pictures",
            "open videos",
            "open my videos",
            "open music",
            "open my music",
        }:
            return "open_in_explorer"

        # -----------------------------------------------------
        # OPEN PATH / FILE / FOLDER
        # -----------------------------------------------------

        if normalized.startswith(
            (
                "open file ",
                "open folder ",
                "open path ",
            )
        ):
            return "open_path"

        # -----------------------------------------------------
        # PATH EXISTENCE
        # -----------------------------------------------------

        if normalized.startswith(
            (
                "does ",
                "is there ",
                "is the file ",
                "is the folder ",
            )
        ) and any(
            word in normalized
            for word in (
                "exist",
                "there",
                "available",
            )
        ):
            return "path_exists"

        return None
