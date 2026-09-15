from __future__ import annotations

from desktop_automation.controller.desktop_controller import (
    DesktopController,
)
from desktop_automation.filesystem.file_manager import FileManager
from desktop_automation.planner.desktop_planner import (
    DesktopPlanner,
)


class DesktopHandler:
    """
    High-level desktop automation orchestration layer.

    This handler exposes the full DesktopController capability
    surface through structured actions while preserving the
    existing planner-based execution path.
    """

    def __init__(self):
        self.desktop = DesktopController()
        self.files = FileManager()
        self.planner = DesktopPlanner()

    # =========================================================
    # NATURAL-LANGUAGE EXECUTION
    # =========================================================

    def execute(self, command):
        """
        Plan and execute a natural-language desktop command.
        """

        if command is None:
            return False, "Desktop command is required."

        plan = self.planner.plan(command)

        if not plan:
            return (
                False,
                f"Could not understand desktop command: {command}",
            )

        if not isinstance(plan, dict):
            return (
                False,
                "Desktop planner returned an invalid plan.",
            )

        action = plan.get("action")
        target = plan.get("target")

        if not action:
            return False, "Desktop plan contains no action."

        return self.handle(
            action,
            target,
        )

    # =========================================================
    # STRUCTURED ACTION DISPATCH
    # =========================================================

    def handle(
        self,
        action,
        target=None,
    ):
        """
        Execute a structured desktop automation action.

        The handler intentionally maps actions to the existing
        DesktopController instead of implementing low-level
        automation here.
        """

        if not action:
            return False, "Desktop action is required."

        action = str(action).strip().lower()

        # =====================================================
        # WINDOWS — INFORMATION
        # =====================================================

        if action == "list_windows":
            return self._safe_call(
                self.desktop.list_windows
            )

        if action in {
            "active_window",
            "get_active_window",
        }:
            return self._safe_call(
                self.desktop.get_active_window
            )

        if action == "find_window":
            return self._require_target_call(
                target,
                self.desktop.find_window,
            )

        # =====================================================
        # WINDOWS — CONTROL
        # =====================================================

        if action == "focus_window":
            return self._require_target_call(
                target,
                self.desktop.focus_window,
            )

        if action == "close_window":
            return self._require_target_call(
                target,
                self.desktop.close_window,
            )

        if action == "minimize_window":
            return self._require_target_call(
                target,
                self.desktop.minimize_window,
            )

        if action == "maximize_window":
            return self._require_target_call(
                target,
                self.desktop.maximize_window,
            )

        if action == "restore_window":
            return self._require_target_call(
                target,
                self.desktop.restore_window,
            )

        if action == "minimize_active_window":
            return self._safe_call(
                self.desktop.minimize_active_window
            )

        if action == "maximize_active_window":
            return self._safe_call(
                self.desktop.maximize_active_window
            )

        if action == "restore_active_window":
            return self._safe_call(
                self.desktop.restore_active_window
            )

        # =====================================================
        # MOUSE
        # =====================================================

        if action == "mouse_position":
            return self._safe_call(
                self.desktop.mouse_position
            )

        if action == "mouse_move":
            return self._require_target_call(
                target,
                self.desktop.mouse_move,
            )

        if action in {
            "mouse_click",
            "click",
        }:
            return self._optional_target_call(
                target,
                self.desktop.mouse_click,
            )

        if action in {
            "mouse_double_click",
            "double_click",
        }:
            return self._optional_target_call(
                target,
                self.desktop.mouse_double_click,
            )

        if action in {
            "mouse_right_click",
            "right_click",
        }:
            return self._optional_target_call(
                target,
                self.desktop.mouse_right_click,
            )

        if action in {
            "mouse_middle_click",
            "middle_click",
        }:
            return self._optional_target_call(
                target,
                self.desktop.mouse_middle_click,
            )

        if action in {
            "mouse_scroll",
            "scroll",
        }:
            return self._require_target_call(
                target,
                self.desktop.mouse_scroll,
            )

        # =====================================================
        # KEYBOARD
        # =====================================================

        if action in {
            "keyboard_type",
            "type",
            "type_text",
        }:
            return self._require_target_call(
                target,
                self.desktop.keyboard_type,
            )

        if action in {
            "keyboard_press",
            "press_key",
            "key_press",
        }:
            return self._require_target_call(
                target,
                self.desktop.keyboard_press,
            )

        if action in {
            "keyboard_hotkey",
            "hotkey",
        }:
            return self._require_target_call(
                target,
                self.desktop.keyboard_hotkey,
            )

        # =====================================================
        # UI AUTOMATION — DISCOVERY
        # =====================================================

        if action == "ui_find":
            return self._require_target_call(
                target,
                self.desktop.ui_find,
            )

        if action in {
            "ui_find_descriptor",
            "find_ui_descriptor",
        }:
            return self._require_target_call(
                target,
                self.desktop.ui_find_descriptor,
            )

        if action == "ui_describe":
            return self._require_target_call(
                target,
                self.desktop.ui_describe,
            )

        # =====================================================
        # UI AUTOMATION — ACTION
        # =====================================================

        if action == "ui_click":
            return self._require_target_call(
                target,
                self.desktop.ui_click,
            )

        if action == "ui_focus":
            return self._require_target_call(
                target,
                self.desktop.ui_focus,
            )

        if action == "ui_click_at":
            return self._require_target_call(
                target,
                self.desktop.ui_click_at,
            )

        if action == "ui_type":
            return self._require_target_call(
                target,
                self.desktop.ui_type,
            )

        if action == "ui_click_descriptor":
            return self._require_target_call(
                target,
                self.desktop.ui_click_descriptor,
            )

        if action == "ui_type_descriptor":
            return self._require_target_call(
                target,
                self.desktop.ui_type_descriptor,
            )

        # =====================================================
        # SEARCH
        # =====================================================

        if action in {
            "search_ui",
            "desktop_search",
        }:
            return self._require_target_call(
                target,
                self.desktop.search_ui,
            )

        if action in {
            "open_search_result",
            "click_search_result",
        }:
            return self._require_target_call(
                target,
                self.desktop.open_search_result,
            )

        # =====================================================
        # FILESYSTEM
        # =====================================================

        if action == "path_exists":
            return self._require_target_call(
                target,
                lambda value: (
                    True,
                    self.files.exists(value),
                ),
            )

        if action == "list_directory":
            return self._require_target_call(
                target,
                self.files.list_directory,
            )

        if action == "file_info":
            return self._require_target_call(
                target,
                self.files.file_info,
            )

        if action == "create_folder":
            return self._require_target_call(
                target,
                self.files.create_folder,
            )

        if action == "create_file":
            payload = self._split_pair(
                target,
                "create_file",
            )

            if payload is None:
                return (
                    False,
                    "Create-file target must use: path||content",
                )

            path, content = payload

            return self.files.create_file(
                path,
                content,
            )

        if action == "read_file":
            return self._require_target_call(
                target,
                self.files.read_text,
            )

        if action == "copy":
            payload = self._split_pair(
                target,
                "copy",
            )

            if payload is None:
                return (
                    False,
                    "Copy target must use: source||destination",
                )

            source, destination = payload

            return self.files.copy(
                source,
                destination,
            )

        if action == "move":
            payload = self._split_pair(
                target,
                "move",
            )

            if payload is None:
                return (
                    False,
                    "Move target must use: source||destination",
                )

            source, destination = payload

            return self.files.move(
                source,
                destination,
            )

        if action == "rename":
            payload = self._split_pair(
                target,
                "rename",
            )

            if payload is None:
                return (
                    False,
                    "Rename target must use: source||new_name",
                )

            source, new_name = payload

            return self.files.rename(
                source,
                new_name,
            )

        if action == "search_files":
            payload = self._split_pair(
                target,
                "search_files",
            )

            if payload is None:
                return (
                    False,
                    "Search target must use: directory||pattern",
                )

            directory, pattern = payload

            return self.files.search(
                directory,
                pattern,
            )

        if action == "open_path":
            return self._require_target_call(
                target,
                self.files.open_path,
            )

        if action == "open_in_explorer":
            return self._require_target_call(
                target,
                self.files.open_in_explorer,
            )

        # =====================================================
        # UNKNOWN ACTION
        # =====================================================

        # =====================================================
        # UNKNOWN ACTION
        # =====================================================

        return (
            False,
            f"Unknown desktop action: {action}",
        )

    # =========================================================
    # SAFE CALL HELPERS
    # =========================================================

    @staticmethod
    def _safe_call(function):
        """
        Execute a controller function safely.

        Preserves controller return values while converting
        unexpected exceptions into structured failures.
        """

        try:
            return function()

        except Exception as error:
            return (
                False,
                f"Desktop action failed: {error}",
            )

    @staticmethod
    def _require_target_call(
        target,
        function,
    ):
        """
        Execute a controller function that requires a target.
        """

        if target is None:
            return (
                False,
                "A target is required for this desktop action.",
            )

        if isinstance(target, str):
            target = target.strip()

            if not target:
                return (
                    False,
                    "A target is required for this desktop action.",
                )

        try:
            return function(target)

        except Exception as error:
            return (
                False,
                f"Desktop action failed: {error}",
            )

    @staticmethod
    def _optional_target_call(
        target,
        function,
    ):
        """
        Execute a controller function where target is optional.
        """

        if isinstance(target, str):
            target = target.strip()

            if not target:
                target = None

        try:
            return function(target)

        except Exception as error:
            return (
                False,
                f"Desktop action failed: {error}",
            )

    # =========================================================
    # FILESYSTEM PAYLOAD PARSING
    # =========================================================

    @staticmethod
    def _split_pair(
        target,
        action_name,
    ):
        """
        Parse a two-part filesystem target.

        Format:

            first||second
        """

        if target is None:
            return None

        value = str(target).strip()

        if not value:
            return None

        if "||" not in value:
            return None

        first, second = value.split(
            "||",
            1,
        )

        first = first.strip()
        second = second.strip()

        if not first or not second:
            return None

        return first, second

    # =========================================================
    # RESOURCE CLEANUP
    # =========================================================

    def close(self):
        """
        Release resources owned by DesktopController.
        """

        try:
            self.desktop.close()
        except Exception:
            pass
