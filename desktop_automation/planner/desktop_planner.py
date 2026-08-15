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
    }

    def __init__(self):
        self.composer = DesktopTaskComposer()

    # =========================================================
    # CAN PLAN
    # =========================================================

    def can_plan(self, command):
        """Return True for supported desktop or composed commands."""

        if not command:
            return False

        # First check deterministic multi-step commands.
        if self.composer.compose(
            command.original
        ):
            return True

        # Then check normal single-action intents.
        return command.intent in self.DESKTOP_INTENTS

    # =========================================================
    # PLAN
    # =========================================================

    def plan(self, command):
        """Convert a Command into desktop Task objects."""

        if not command:
            return []

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
        # CREATE SINGLE TASK
        # =====================================================

        return [
            Task(
                action=action,
                target=target,
            )
        ]