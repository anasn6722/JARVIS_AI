from ai.planner.planner import Planner


class DesktopPlanner(Planner):
    """Plan desktop window and mouse automation commands."""

    DESKTOP_INTENTS = {
        # Window control
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
        # Mouse control
        "mouse_position",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll_up",
        "mouse_scroll_down",
        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",
        "ui_find",
        "ui_click",
        "ui_focus",
        "ui_click_at",
        "ui_describe",
    }

    ACTIONS = {
        # Window control
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
        # Mouse control
        "mouse_position": "mouse_position",
        "mouse_move": "mouse_move",
        "mouse_click": "mouse_click",
        "mouse_double_click": "mouse_double_click",
        "mouse_right_click": "mouse_right_click",
        "mouse_middle_click": "mouse_middle_click",
        "mouse_scroll_up": "mouse_scroll",
        "mouse_scroll_down": "mouse_scroll",
        #keyboard control
        "keyboard_type": "keyboard_type",
        "keyboard_press": "keyboard_press",
        "keyboard_hotkey": "keyboard_hotkey",
        #UI
        "ui_find": "ui_find",
        "ui_click": "ui_click",
        "ui_focus": "ui_focus",
        "ui_click_at": "ui_click_at",
        "ui_describe": "ui_describe",
    }

    def can_plan(self, command):
        """Return True when this planner handles the command."""

        if not command:
            return False

        return command.intent in self.DESKTOP_INTENTS

    def plan(self, command):
        """Convert a Command object into desktop Task objects."""
    
        if not self.can_plan(command):
            return []
    
        action = self.ACTIONS.get(command.intent)
    
        if not action:
            return []
    
        target = None
    
        # =========================================================
        # EXISTING WINDOW / APP TARGETS
        # =========================================================
    
        if hasattr(command, "entities"):
            entities = command.entities or {}
    
            windows = entities.get("windows", [])
            apps = entities.get("apps", [])
    
            if windows:
                target = windows[0]
    
            elif apps:
                target = apps[0]
    
        # =========================================================
        # ACTIVE WINDOW ACTIONS
        # =========================================================
    
        if action in {
            "active_window",
            "list_windows",
            "close_active_window",
            "minimize_active_window",
            "maximize_active_window",
            "restore_active_window",
        }:
            target = None
    
        # =========================================================
        # SEMANTIC UI ACTIONS
        # =========================================================
    
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
                    target = target[len(prefix):].strip()
                    break
                
        # =========================================================
        # COORDINATE UI ACTION
        # =========================================================
    
        if action == "ui_click_at":
            entities = command.entities or {}
            coordinates = entities.get("coordinates", [])
    
            if coordinates:
                target = coordinates[0]
    
        # =========================================================
        # CREATE TASK
        # =========================================================
    
        from ai.agent.task import Task
    
        task = Task(
            action=action,
            target=target,
        )
    
        return [task]