from ai.agent.task import Task
from ai.planner.planner import Planner
from desktop_automation.planner.desktop_task_composer import (
    DesktopTaskComposer,
)


class DesktopPlanner(Planner):
    """Plan desktop, keyboard, mouse, and semantic UI commands."""

    DESKTOP_INTENTS = {
        # -----------------------------------------------------
        # Window control
        # -----------------------------------------------------
        "focus_window",
        "open_search_result",

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

        # -----------------------------------------------------
        # Mouse control
        # -----------------------------------------------------
        "mouse_position",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll_up",
        "mouse_scroll_down",

        # -----------------------------------------------------
        # Keyboard control
        # -----------------------------------------------------
        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",

        # -----------------------------------------------------
        # Semantic UI
        # -----------------------------------------------------
        "ui_find",
        "ui_click",
        "ui_focus",
        "ui_click_at",
        "ui_describe",
        "ui_type",

        # -----------------------------------------------------
        # Desktop search
        # -----------------------------------------------------
        "search_ui",

        # -----------------------------------------------------
        # Filesystem
        # -----------------------------------------------------
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

    ACTIONS = {
        # -----------------------------------------------------
        # Window control
        # -----------------------------------------------------
        "focus_window": "focus_window",
        "close_window": "close_window",
        "close_active_window": "close_active_window",
        "minimize_window": "minimize_window",
        "maximize_window": "maximize_window",
        "restore_window": "restore_window",
        "minimize_active_window": "minimize_active_window",
        "maximize_active_window": "maximize_active_window",
        "restore_active_window": "restore_active_window",
        "active_window": "active_window",
        "list_windows": "list_windows",

        # -----------------------------------------------------
        # Mouse control
        # -----------------------------------------------------
        "mouse_position": "mouse_position",
        "mouse_move": "mouse_move",
        "mouse_click": "mouse_click",
        "mouse_double_click": "mouse_double_click",
        "mouse_right_click": "mouse_right_click",
        "mouse_middle_click": "mouse_middle_click",
        "mouse_scroll_up": "mouse_scroll",
        "mouse_scroll_down": "mouse_scroll",

        # -----------------------------------------------------
        # Keyboard control
        # -----------------------------------------------------
        "keyboard_type": "keyboard_type",
        "keyboard_press": "keyboard_press",
        "keyboard_hotkey": "keyboard_hotkey",

        # -----------------------------------------------------
        # Semantic UI
        # -----------------------------------------------------
        "ui_find": "ui_find",
        "ui_click": "ui_click",
        "ui_focus": "ui_focus",
        "ui_click_at": "ui_click_at",
        "ui_describe": "ui_describe",
        "ui_type": "ui_type",

        # -----------------------------------------------------
        # Desktop search
        # -----------------------------------------------------
        "search_ui": "search_ui",
        # -----------------------------------------------------
        # Filesystem
        # -----------------------------------------------------
        "path_exists": "path_exists",
        "list_directory": "list_directory",
        "create_folder": "create_folder",
        "create_file": "create_file",
        "read_file": "read_file",
        "file_info": "file_info",
        "copy": "copy",
        "move": "move",
        "rename": "rename",
        "search_files": "search_files",
        "open_path": "open_path",
        "open_in_explorer": "open_in_explorer",

    }


    def __init__(self):
        self.composer = DesktopTaskComposer()

    # =========================================================
    # CAN PLAN
    # =========================================================

    def can_plan(self, command):
        """Return True for supported desktop commands."""

        if not command:
            return False

        original = str(
            getattr(
                command,
                "original",
                "",
            )
        ).strip()

        if not original:
            return False

        # -----------------------------------------------------
        # Deterministic multi-step desktop commands
        # -----------------------------------------------------

        if self.composer.compose(
            original
        ):
            return True

        # -----------------------------------------------------
        # Existing desktop intents
        # -----------------------------------------------------

        if command.intent in self.DESKTOP_INTENTS:
            return True

        # -----------------------------------------------------
        # Filesystem natural-language detection
        # -----------------------------------------------------

        normalized = " ".join(
            original.lower().split()
        )

        filesystem_patterns = (
            "create a folder",
            "create folder",
            "make a folder",
            "make folder",
            "new folder",
            "create a file",
            "create file",
            "make a file",
            "make file",
            "list my desktop",
            "list desktop",
            "show my desktop files",
            "show desktop files",
            "list downloads",
            "show downloads",
            "open downloads",
            "open documents",
            "open desktop",
            "open pictures",
            "open videos",
            "open music",
            "open this file",
            "open this folder",
            "copy ",
            "move ",
            "rename ",
            "find files",
            "search files",
            "search my files",
            "find my files",
            "what files are in",
            "what is in my",
        )

        return any(
            normalized.startswith(pattern)
            for pattern in filesystem_patterns
        )

    # =========================================================
    # PLAN
    # =========================================================

    def plan(self, command):
        """Convert a Command into desktop Task objects."""

        if not command:
            return []

        filesystem_task = (
            self._plan_filesystem_command(
                command
            )
        )

        if filesystem_task:
            return filesystem_task

        # =====================================================
        # MULTI-STEP DESKTOP COMPOSITION
        # =====================================================

        composed_tasks = self.composer.compose(
            command.original
        )

        if composed_tasks:
            return composed_tasks

        # =====================================================
        # NORMAL SINGLE-ACTION PLANNING
        # =====================================================

        if not self.can_plan(command):
            return []

        action = self.ACTIONS.get(
            command.intent
        )

        if not action:
            return []

        target = None

        # =====================================================
        # WINDOW / APP TARGETS
        # =====================================================

        if hasattr(command, "entities"):
            entities = command.entities or {}

            windows = entities.get(
                "windows",
                [],
            )

            apps = entities.get(
                "apps",
                [],
            )

            if windows:
                target = windows[0]

            elif apps:
                target = apps[0]

        # =====================================================
        # ACTIVE WINDOW ACTIONS
        # =====================================================

        if action in {
            "active_window",
            "list_windows",
            "close_active_window",
            "minimize_active_window",
            "maximize_active_window",
            "restore_active_window",
        }:
            target = None

        # =====================================================
        # SEMANTIC UI ACTIONS
        # =====================================================

        if action in {
            "ui_find",
            "ui_click",
            "ui_focus",
            "ui_describe",
        }:
            target = command.original.strip()

            prefixes = (
                "press the button ",
                "click on ",
                "click ",
                "focus on ",
                "focus the ",
                "focus ",
                "activate the ",
                "activate ",
                "find ",
                "locate ",
                "describe ",
            )

            normalized = target.lower()

            for prefix in prefixes:
                if normalized.startswith(prefix):
                    target = target[
                        len(prefix):
                    ].strip()
                    break

        # =====================================================
        # SEMANTIC UI TYPE
        # =====================================================

        if action == "ui_type":
            original = command.original.strip()
            normalized = original.lower()

            prefix = "type "

            if not normalized.startswith(prefix):
                return []

            body = original[
                len(prefix):
            ].strip()

            marker = " in "

            marker_index = body.lower().rfind(
                marker
            )

            if marker_index == -1:
                return []

            text_to_type = body[
                :marker_index
            ].strip()

            element_name = body[
                marker_index + len(marker):
            ].strip()

            if element_name.lower().startswith(
                "the "
            ):
                element_name = element_name[
                    4:
                ].strip()

            if (
                not text_to_type
                or not element_name
            ):
                return []

            target = (
                f"{element_name}||{text_to_type}"
            )

        # =====================================================
        # DESKTOP SEARCH
        # =====================================================

        if action == "search_ui":
            original = command.original.strip()

            prefixes = (
                "search for ",
                "search ",
            )

            target = original

            for prefix in prefixes:
                if original.lower().startswith(
                    prefix
                ):
                    target = original[
                        len(prefix):
                    ].strip()
                    break

            if not target:
                return []

        # =====================================================
        # COORDINATE UI ACTION
        # =====================================================

        if action == "ui_click_at":
            entities = command.entities or {}

            coordinates = entities.get(
                "coordinates",
                [],
            )

            if coordinates:
                target = coordinates[0]

        # =====================================================
        # KEYBOARD PRESS
        # =====================================================

        if action == "keyboard_press":
            original = command.original.strip()
            normalized = original.lower().strip()

            prefixes = (
                "press ",
                "hit ",
                "push ",
            )

            target = ""

            for prefix in prefixes:
                if normalized.startswith(prefix):
                    target = original[
                        len(prefix):
                    ].strip()
                    break

            if not target:
                return []

            target = target.rstrip(" ,.")

            # Normalize common spoken key names.
            key_aliases = {
                "return": "enter",
                "escape key": "esc",
                "escape": "esc",
                "space bar": "space",
                "spacebar": "space",
                "tab key": "tab",
                "control": "ctrl",
                "control key": "ctrl",
                "windows key": "win",
                "window key": "win",
            }

            target = key_aliases.get(
                target.lower(),
                target.lower(),
            )

        # =====================================================
        # CREATE SINGLE TASK
        # =====================================================

        return [
            Task(
                action=action,
                target=target,
            )
        ]

    
    # =========================================================
    # FILESYSTEM PLANNING
    # =========================================================

    def _plan_filesystem_command(self, command):
        """
        Convert common natural-language filesystem commands
        into deterministic Tasks.

        Supported examples:

            list my desktop
            open downloads
            create a folder called Projects
            create a folder called Projects inside Documents
            create a file called notes.txt
            create notes.txt inside Documents
            copy test.txt from Downloads to Desktop
            move report.pdf from Downloads to Documents
            rename report.txt to final_report.txt
            find all Python files in JARVIS_AI
        """

        original = str(
            command.original
        ).strip()

        if not original:
            return []

        normalized = " ".join(
            original.lower().split()
        )

        # =====================================================
        # SPECIAL WINDOWS LOCATIONS
        # =====================================================

        location_map = {
            "desktop": "Desktop",
            "my desktop": "Desktop",
            "downloads": "Downloads",
            "my downloads": "Downloads",
            "documents": "Documents",
            "my documents": "Documents",
            "pictures": "Pictures",
            "my pictures": "Pictures",
            "videos": "Videos",
            "my videos": "Videos",
            "music": "Music",
            "my music": "Music",
        }

        # =====================================================
        # OPEN SPECIAL LOCATIONS
        # =====================================================

        if normalized.startswith("open "):

            requested = original[
                len("open "):
            ].strip()

            requested_key = requested.lower()

            if requested_key in location_map:
                return [
                    Task(
                        action="open_in_explorer",
                        target=location_map[
                            requested_key
                        ],
                    )
                ]

            # Explicit file/folder/path.
            for prefix in (
                "open file ",
                "open folder ",
                "open path ",
            ):
                if normalized.startswith(prefix):
                    target = original[
                        len(prefix):
                    ].strip()

                    if target:
                        return [
                            Task(
                                action="open_path",
                                target=target,
                            )
                        ]

        # =====================================================
        # LIST DIRECTORY
        # =====================================================

        list_patterns = (
            "list my desktop",
            "list desktop",
            "show my desktop files",
            "show desktop files",
            "list downloads",
            "list documents",
            "list pictures",
            "list videos",
            "list music",
        )

        if normalized in list_patterns:

            if "desktop" in normalized:
                target = "Desktop"
            elif "download" in normalized:
                target = "Downloads"
            elif "document" in normalized:
                target = "Documents"
            elif "picture" in normalized:
                target = "Pictures"
            elif "video" in normalized:
                target = "Videos"
            else:
                target = "Music"

            return [
                Task(
                    action="list_directory",
                    target=target,
                )
            ]

        # -----------------------------------------------------
        # "list files in X"
        # -----------------------------------------------------

        for prefix in (
            "list files in ",
            "list the files in ",
            "show files in ",
            "show the files in ",
            "show what is in ",
            "show what is inside ",
            "show what is in my ",
            "show what is inside my ",
        ):

            if normalized.startswith(prefix):

                target = original[
                    len(prefix):
                ].strip()

                target = self._normalize_location(
                    target
                )

                if target:
                    return [
                        Task(
                            action="list_directory",
                            target=target,
                        )
                    ]

        # =====================================================
        # CREATE FOLDER
        # =====================================================

        folder_prefixes = (
            "create a folder called ",
            "create folder called ",
            "create a folder named ",
            "create folder named ",
            "make a folder called ",
            "make folder called ",
            "new folder called ",
        )

        for prefix in folder_prefixes:

            if normalized.startswith(prefix):

                remainder = original[
                    len(prefix):
                ].strip()

                # ---------------------------------------------
                # "called X inside Y"
                # ---------------------------------------------

                parsed = self._split_inside_phrase(
                    remainder
                )

                if parsed:
                    folder_name, parent = parsed

                    parent = self._normalize_location(
                        parent
                    )

                    return [
                        Task(
                            action="create_folder",
                            target=(
                                f"{parent}\\{folder_name}"
                            ),
                        )
                    ]

                if remainder:

                    return [
                        Task(
                            action="create_folder",
                            target=(
                                f"Desktop\\{remainder}"
                            ),
                        )
                    ]

        # =====================================================
        # CREATE FILE
        # =====================================================

        file_prefixes = (
            "create a file called ",
            "create file called ",
            "create a file named ",
            "create file named ",
            "make a file called ",
            "make file called ",
        )

        for prefix in file_prefixes:

            if normalized.startswith(prefix):

                remainder = original[
                    len(prefix):
                ].strip()

                parsed = self._split_inside_phrase(
                    remainder
                )

                if parsed:
                    filename, parent = parsed

                    parent = self._normalize_location(
                        parent
                    )

                    return [
                        Task(
                            action="create_file",
                            target=(
                                f"{parent}\\{filename}||"
                            ),
                        )
                    ]

                if remainder:
                    return [
                        Task(
                            action="create_file",
                            target=(
                                f"Desktop\\{remainder}||"
                            ),
                        )
                    ]

        # =====================================================
        # CREATE FILE — NATURAL SHORT FORM
        # =====================================================

        if normalized.startswith(
            "create "
        ):
            remainder = original[
                len("create "):
            ].strip()

            parsed = self._split_inside_phrase(
                remainder
            )

            if parsed:
                filename, parent = parsed

                # Only treat it as a file when it looks
                # like a filename.
                if "." in filename:
                    parent = self._normalize_location(
                        parent
                    )

                    return [
                        Task(
                            action="create_file",
                            target=(
                                f"{parent}\\{filename}||"
                            ),
                        )
                    ]

        # =====================================================
        # COPY
        # =====================================================

        if normalized.startswith(
            (
                "copy ",
                "copy the file ",
                "copy the folder ",
            )
        ):

            body = self._remove_command_prefix(
                original,
                (
                    "copy the file ",
                    "copy the folder ",
                    "copy ",
                ),
            )

            parsed = self._parse_from_to(
                body
            )

            if parsed:
                source, destination = parsed

                source = self._normalize_location(
                    source
                )

                destination = self._normalize_location(
                    destination
                )

                return [
                    Task(
                        action="copy",
                        target=(
                            f"{source}||{destination}"
                        ),
                    )
                ]

        # =====================================================
        # MOVE
        # =====================================================

        if normalized.startswith(
            (
                "move ",
                "move the file ",
                "move the folder ",
            )
        ):

            body = self._remove_command_prefix(
                original,
                (
                    "move the file ",
                    "move the folder ",
                    "move ",
                ),
            )

            parsed = self._parse_from_to(
                body
            )

            if parsed:
                source, destination = parsed

                source = self._normalize_location(
                    source
                )

                destination = self._normalize_location(
                    destination
                )

                return [
                    Task(
                        action="move",
                        target=(
                            f"{source}||{destination}"
                        ),
                    )
                ]

        # =====================================================
        # RENAME
        # =====================================================

        if normalized.startswith(
            (
                "rename ",
                "rename the file ",
                "rename the folder ",
            )
        ):

            body = self._remove_command_prefix(
                original,
                (
                    "rename the file ",
                    "rename the folder ",
                    "rename ",
                ),
            )

            lower_body = body.lower()

            marker = " to "

            index = lower_body.rfind(
                marker
            )

            if index != -1:

                source = body[
                    :index
                ].strip()

                new_name = body[
                    index + len(marker):
                ].strip()

                source = self._normalize_location(
                    source
                )

                if source and new_name:
                    return [
                        Task(
                            action="rename",
                            target=(
                                f"{source}||{new_name}"
                            ),
                        )
                    ]

        # =====================================================
        # SEARCH FILES
        # =====================================================

        search_prefixes = (
            "find files ",
            "find my files ",
            "find all files ",
            "find all ",
            "search files ",
            "search my files ",
            "search for files ",
        )


        for prefix in search_prefixes:

            if normalized.startswith(prefix):

                body = original[
                    len(prefix):
                ].strip()

                # ---------------------------------------------
                # "in X"
                # ---------------------------------------------

                lower_body = body.lower()

                marker = " in "

                index = lower_body.rfind(
                    marker
                )

                if index != -1:

                    pattern = body[
                        :index
                    ].strip()

                    directory = body[
                        index + len(marker):
                    ].strip()

                else:

                    pattern = body
                    directory = "Desktop"

                # Natural wording:
                #
                #   Python files
                #   all Python files
                #   PDF files
                #   all PDF files
                #

                lower_pattern = pattern.lower().strip()

                if lower_pattern.startswith(
                    "all "
                ):
                    pattern = pattern[
                        len("all "):
                    ].strip()

                lower_pattern = pattern.lower().strip()

                if lower_pattern.endswith(
                    " files"
                ):
                    pattern = pattern[
                        :-len(" files")
                    ].strip()

                pattern = pattern.strip()


                pattern = self._normalize_search_pattern(
                    pattern
                )

                directory = self._normalize_location(
                    directory
                )

                if pattern and directory:
                    return [
                        Task(
                            action="search_files",
                            target=(
                                f"{directory}||{pattern}"
                            ),
                        )
                    ]

        # =====================================================
        # FILE INFORMATION
        # =====================================================

        for prefix in (
            "file info ",
            "file information ",
            "folder info ",
            "folder information ",
            "information about ",
            "details about ",
        ):

            if normalized.startswith(prefix):

                target = original[
                    len(prefix):
                ].strip()

                target = self._normalize_location(
                    target
                )

                if target:
                    return [
                        Task(
                            action="file_info",
                            target=target,
                        )
                    ]

        return []

    # =========================================================
    # FILESYSTEM HELPERS
    # =========================================================

    @staticmethod
    def _remove_command_prefix(
        text,
        prefixes,
    ):
        """Remove the first matching command prefix."""

        normalized = text.lower()

        for prefix in prefixes:
            if normalized.startswith(
                prefix
            ):
                return text[
                    len(prefix):
                ].strip()

        return text.strip()

    @staticmethod
    def _split_inside_phrase(
        text,
    ):
        """
        Split:

            Projects inside Documents

        into:

            ("Projects", "Documents")
        """

        normalized = text.lower()

        markers = (
            " inside ",
            " in ",
        )

        best_index = -1
        best_marker = ""

        for marker in markers:

            index = normalized.rfind(
                marker
            )

            if index != -1 and index > best_index:
                best_index = index
                best_marker = marker

        if best_index == -1:
            return None

        first = text[
            :best_index
        ].strip()

        second = text[
            best_index + len(best_marker):
        ].strip()

        if not first or not second:
            return None

        return first, second

    @staticmethod
    def _parse_from_to(
        text,
    ):
        """
        Parse:

            source from X to Y

        Also supports:

            source to Y

        """

        normalized = text.lower()

        marker = " from "

        from_index = normalized.find(
            marker
        )

        if from_index != -1:

            source = text[
                :from_index
            ].strip()

            remainder = text[
                from_index + len(marker):
            ].strip()

        else:

            source = text.strip()
            remainder = ""

        if remainder:

            to_marker = " to "

            to_index = remainder.lower().rfind(
                to_marker
            )

            if to_index == -1:
                return None

            # The phrase before the final "to" is
            # still part of the source context.
            middle = remainder[
                :to_index
            ].strip()

            destination = remainder[
                to_index + len(to_marker):
            ].strip()

            if middle:
                source = (
                    f"{source}\\{middle}"
                    if source
                    else middle
                )

        else:

            to_marker = " to "

            to_index = normalized.rfind(
                to_marker
            )

            if to_index == -1:
                return None

            source = text[
                :to_index
            ].strip()

            destination = text[
                to_index + len(to_marker):
            ].strip()

        if not source or not destination:
            return None

        # Handle natural "from Downloads"
        # source context.
        source = source.strip()
        destination = destination.strip()

        # A source such as:
        # "test.txt from Downloads"
        # is parsed by the branch above.

        return source, destination

    @staticmethod
    def _normalize_location(
        value,
    ):
        """
        Normalize common Windows location names.
        """

        if value is None:
            return ""

        value = str(value).strip()

        if not value:
            return ""

        normalized = " ".join(
            value.lower().split()
        )

        locations = {
            "desktop": "Desktop",
            "my desktop": "Desktop",
            "downloads": "Downloads",
            "my downloads": "Downloads",
            "documents": "Documents",
            "my documents": "Documents",
            "pictures": "Pictures",
            "my pictures": "Pictures",
            "videos": "Videos",
            "my videos": "Videos",
            "music": "Music",
            "my music": "Music",
        }

        return locations.get(
            normalized,
            value,
        )

    @staticmethod
    def _normalize_search_pattern(
        pattern,
    ):
        """
        Convert natural language file descriptions into
        deterministic glob patterns.
        """

        if not pattern:
            return ""

        value = str(
            pattern
        ).strip()

        normalized = value.lower()

        known_patterns = {
            "python": "*.py",
            "python files": "*.py",
            "py files": "*.py",
            "pdf": "*.pdf",
            "pdf files": "*.pdf",
            "word": "*.docx",
            "word files": "*.docx",
            "text": "*.txt",
            "text files": "*.txt",
            "images": "*.*",
            "image": "*.*",
            "png": "*.png",
            "jpg": "*.jpg",
            "jpeg": "*.jpeg",
        }

        return known_patterns.get(
            normalized,
            value,
        )
