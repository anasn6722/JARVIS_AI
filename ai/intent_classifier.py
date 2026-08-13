
import re
from typing import ClassVar

from ai.intent_utils import IntentUtils


class IntentClassifier:
    """Classifies natural-language commands into JARVIS intents."""

    OPEN_WORDS = (
        "open",
        "launch",
        "start",
        "run",
    )

    CLOSE_WORDS = (
        "close",
        "exit",
        "quit",
        "terminate",
    )

    FOCUS_WORDS = (
        "focus",
        "switch to",
        "bring up",
        "bring forward",
    )

    DESKTOP_WINDOW_WORDS = (
        "window",
        "windows",
    )

    LIST_WINDOW_PHRASES = (
        "show windows",
        "list windows",
        "show all windows",
        "list all windows",
        "what windows are open",
        "which windows are open",
    )

    ACTIVE_WINDOW_PHRASES = (
        "active window",
        "current window",
        "which window is active",
        "what window is active",
        "what is the active window",
    )

    CLOSE_ACTIVE_WINDOW_PHRASES = (
        "close active window",
        "close current window",
        "close this window",
        "close the active window",
        "close the current window",
    )

    # =====================================================
    # MOUSE CONTROL
    # =====================================================

    MOUSE_POSITION_PHRASES = (
        "mouse position",
        "cursor position",
        "where is my mouse",
        "where is the mouse",
        "where is my cursor",
        "where is the cursor",
    )

    MOUSE_MOVE_PHRASES = (
        "move mouse",
        "move the mouse",
        "move cursor",
        "move the cursor",
        "move mouse to",
        "move the mouse to",
        "move cursor to",
        "move the cursor to",
    )

    MOUSE_DOUBLE_CLICK_PHRASES = (
        "double click",
        "double-click",
        "double click at",
        "double-click at",
    )

    MOUSE_RIGHT_CLICK_PHRASES = (
        "right click",
        "right-click",
        "right click at",
        "right-click at",
    )

    MOUSE_MIDDLE_CLICK_PHRASES = (
        "middle click",
        "middle-click",
        "middle click at",
        "middle-click at",
    )

    MOUSE_CLICK_PHRASES = (
        "click",
        "left click",
        "left-click",
        "click at",
    )

    MOUSE_SCROLL_UP_PHRASES = (
        "scroll up",
        "scroll upward",
        "scroll upwards",
    )

    MOUSE_SCROLL_DOWN_PHRASES = (
        "scroll down",
        "scroll downward",
        "scroll downwards",
    )

        # =====================================================
    # KEYBOARD CONTROL
    # =====================================================

    KEYBOARD_TYPE_PHRASES = (
        "type ",
        "type text",
        "write ",
        "enter text",
        "write text",
    )

    KEYBOARD_PRESS_PHRASES = (
        "press ",
        "hit ",
        "push ",
    )

    KEYBOARD_HOTKEY_PHRASES = (
        "hotkey ",
        "keyboard shortcut",
        "key combination",
        "press control",
        "press ctrl",
        "press alt",
        "press shift",
        "press windows",
        "press win",
        "press command",
    )

    # =====================================================
    # WINDOW CONTROL
    # =====================================================

    MINIMIZE_ACTIVE_WINDOW_PHRASES = (
        "minimize active window",
        "minimize the active window",
        "minimize current window",
        "minimize the current window",
        "minimize this window",
    )

    MAXIMIZE_ACTIVE_WINDOW_PHRASES = (
        "maximize active window",
        "maximize the active window",
        "maximize current window",
        "maximize the current window",
        "maximize this window",
    )

    RESTORE_ACTIVE_WINDOW_PHRASES = (
        "restore active window",
        "restore the active window",
        "restore current window",
        "restore the current window",
        "restore this window",
    )

    MINIMIZE_WORDS = (
        "minimize",
    )

    MAXIMIZE_WORDS = (
        "maximize",
    )

    RESTORE_WORDS = (
        "restore",
    )

    SEARCH_WORDS = (
        "search",
        "google",
        "find",
        "look up",
        "lookup",
    )

    YOUTUBE_WORDS = (
        "youtube",
        "watch",
        "play",
    )

    HELLO_WORDS = (
        "hello",
        "hi",
        "hey",
    )

    NORMALIZATION: ClassVar[dict[str, str]] = {
        "gold": "goal",
        "goalss": "goals",
        "goal's": "goals",
        "favourite": "favorite",

        # Contractions
        "what's": "what is",
        "who's": "who is",
        "where's": "where is",
        "how's": "how is",
        "it's": "it is",
        "i'm": "i am",
        "don't": "do not",
        "can't": "cannot",
        "won't": "will not",
    }

    MEMORY_QUERIES: ClassVar[dict[str, str]] = {
        # City
        "where do i live": "city",
        "where i live": "city",
        "do i live": "city",
        "where am i from": "city",
        "where i am from": "city",

        # University
        "where do i study": "university",
        "where i study": "university",

        # Language
        "what is my favorite language": "favorite_language",
        "what's my favorite language": "favorite_language",
        "favorite language": "favorite_language",
        "my favorite language": "favorite_language",

        # Identity
        "who am i": "identity",

        # Favorites
        "what do i like": "favorites",
    }

    PRONOUNS: ClassVar[set[str]] = {
        "it",
        "that",
        "this",
        "them",
        "those",
        "him",
        "her",
    }

    NEXT_TASK_WORDS = (
        "next",
        "next task",
        "what next",
        "what's next",
        "what is next",
        "what is my next task",
        "continue",
        "continue it",
        "continue learning",
        "continue goal",
        "resume",
        "resume it",
        "after that",
    )

    COMPLETE_TASK_WORDS = (
        "complete task",
        "mark task done",
        "task done",
        "finish task",
    )

    PROGRESS_WORDS = (
        "goal progress",
        "progress",
        "how much progress",
        "how far am i",
    )

    DELETE_GOAL_WORDS = (
        "delete goal",
        "remove goal",
        "forget goal",
    )

    def classify(self, text: str) -> dict:
        """Classify user input into an intent."""

        text = text.lower().strip()
        text = self.normalize(text)

        # =====================================================
        # REFERENCE / CONTEXT COMMANDS
        # =====================================================

        # -----------------------
        # Close Last Reference
        # -----------------------

        if text in (
            "close it",
            "close that",
            "close this",
            "close",
            "exit it",
            "quit it",
        ):
            return {
                "destination": "BRAIN",
                "intent": "close_last",
            }

        # -----------------------
        # Complete Current Task
        # -----------------------

        if text in (
            "mark it done",
            "complete it",
            "finish it",
        ):
            return {
                "destination": "BRAIN",
                "intent": "complete_current_task",
            }

        # =====================================================
        # DESKTOP AUTOMATION
        # =====================================================

        # -----------------------
        # Close Active Window
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.CLOSE_ACTIVE_WINDOW_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "close_active_window",
            }

        # -----------------------
        # Minimize Active Window
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.MINIMIZE_ACTIVE_WINDOW_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "minimize_active_window",
            }

        # -----------------------
        # Maximize Active Window
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.MAXIMIZE_ACTIVE_WINDOW_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "maximize_active_window",
            }

        # -----------------------
        # Restore Active Window
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.RESTORE_ACTIVE_WINDOW_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "restore_active_window",
            }

        # -----------------------
        # List Windows
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.LIST_WINDOW_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "list_windows",
            }

        # -----------------------
        # Active Window
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.ACTIVE_WINDOW_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "active_window",
            }

        # -----------------------
        # Focus Window
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.FOCUS_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "focus_window",
            }

        # -----------------------
        # Minimize Specific Window
        # -----------------------

        if (
            IntentUtils.contains_any(
                text,
                self.MINIMIZE_WORDS,
            )
            and "window" in text
        ):
            return {
                "destination": "BRAIN",
                "intent": "minimize_window",
            }

        # -----------------------
        # Maximize Specific Window
        # -----------------------

        if (
            IntentUtils.contains_any(
                text,
                self.MAXIMIZE_WORDS,
            )
            and "window" in text
        ):
            return {
                "destination": "BRAIN",
                "intent": "maximize_window",
            }

        # -----------------------
        # Restore Specific Window
        # -----------------------

        if (
            IntentUtils.contains_any(
                text,
                self.RESTORE_WORDS,
            )
            and "window" in text
        ):
            return {
                "destination": "BRAIN",
                "intent": "restore_window",
            }

        # -----------------------
        # Close Specific Window
        # -----------------------

        if (
            text.startswith("close ")
            and "window" in text
            and text not in self.CLOSE_ACTIVE_WINDOW_PHRASES
        ):
            return {
                "destination": "BRAIN",
                "intent": "close_window",
            }

        # =====================================================
        # MOUSE CONTROL
        # =====================================================

        if IntentUtils.contains_any(
            text,
            self.MOUSE_POSITION_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "mouse_position",
            }

        if IntentUtils.contains_any(
            text,
            self.MOUSE_DOUBLE_CLICK_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "mouse_double_click",
            }

        if IntentUtils.contains_any(
            text,
            self.MOUSE_RIGHT_CLICK_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "mouse_right_click",
            }

        if IntentUtils.contains_any(
            text,
            self.MOUSE_MIDDLE_CLICK_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "mouse_middle_click",
            }

        if IntentUtils.contains_any(
            text,
            self.MOUSE_SCROLL_UP_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "mouse_scroll_up",
            }

        if IntentUtils.contains_any(
            text,
            self.MOUSE_SCROLL_DOWN_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "mouse_scroll_down",
            }

        if IntentUtils.contains_any(
            text,
            self.MOUSE_MOVE_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "mouse_move",
            }

        if IntentUtils.contains_any(
            text,
            self.MOUSE_CLICK_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "mouse_click",
            }

        # =====================================================
        # KEYBOARD CONTROL
        # =====================================================

        # -----------------------
        # Keyboard Hotkey
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.KEYBOARD_HOTKEY_PHRASES,
        ):
            return {
                "destination": "BRAIN",
                "intent": "keyboard_hotkey",
            }

        # -----------------------
        # Keyboard Type
        # -----------------------

        if text.startswith(
            self.KEYBOARD_TYPE_PHRASES
        ):
            return {
                "destination": "BRAIN",
                "intent": "keyboard_type",
            }

        # -----------------------
        # Keyboard Press
        # -----------------------

        if text.startswith(
            self.KEYBOARD_PRESS_PHRASES
        ):
            return {
                "destination": "BRAIN",
                "intent": "keyboard_press",
            }

        # =====================================================
        # APPLICATIONS
        # =====================================================

        # -----------------------
        # Open Applications
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.OPEN_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "open",
            }

        # -----------------------
        # Close Applications
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.CLOSE_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "close",
            }

        # =====================================================
        # TIME
        # =====================================================

        if any(
            word in text
            for word in (
                "time",
                "clock",
            )
        ):
            return {
                "destination": "BRAIN",
                "intent": "time",
            }

        # =====================================================
        # GREETING
        # =====================================================

        if IntentUtils.contains_any(
            text,
            self.HELLO_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "hello",
            }

        # =====================================================
        # IDENTITY
        # =====================================================

        if any(
            word in text
            for word in (
                "who are you",
                "your name",
            )
        ):
            return {
                "destination": "BRAIN",
                "intent": "identity",
            }

        # =====================================================
        # GOOGLE SEARCH
        # =====================================================

        if IntentUtils.contains_any(
            text,
            self.SEARCH_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "search",
            }

        # =====================================================
        # YOUTUBE
        # =====================================================

        if IntentUtils.contains_any(
            text,
            self.YOUTUBE_WORDS,
        ):
            return {
            "destination": "BRAIN",
            "intent": "youtube",
        }

        # =====================================================
        # SET NAME
        # =====================================================

        if text.startswith("my name is"):
            return {
                "destination": "BRAIN",
                "intent": "set_name",
            }

        # =====================================================
        # GET NAME
        # =====================================================

        if "what is my name" in text:
            return {
                "destination": "BRAIN",
                "intent": "get_name",
            }

        # =====================================================
        # ADD GOAL
        # =====================================================

        if text.startswith(
            (
                "my goal is",
                "i want to",
                "remember that i want to",
                "add goal",
                "create goal",
                "new goal",
            )
        ):
            return {
                "destination": "BRAIN",
                "intent": "add_goal",
            }

        # =====================================================
        # SHOW GOALS
        # =====================================================

        if (
            "what are my goals" in text
            or "what is my goal" in text
            or "show my goals" in text
            or "my goal" in text
            or "my goals" in text
            or "show my goal" in text
            or "show goals" in text
            or "my goals" == text
            or "goal" == text
            or "goals" == text
        ):
            return {
                "destination": "BRAIN",
                "intent": "show_goals",
            }

        # =====================================================
        # NEXT TASK
        # =====================================================

        if IntentUtils.contains_any(
            text,
            self.NEXT_TASK_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "next_task",
            }

        # =====================================================
        # COMPLETE TASK
        # =====================================================

        if IntentUtils.contains_any(
            text,
            self.COMPLETE_TASK_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "complete_task",
            }

        # =====================================================
        # GOAL PROGRESS
        # =====================================================

        if IntentUtils.contains_any(
            text,
            self.PROGRESS_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "goal_progress",
            }

        # =====================================================
        # DELETE GOAL
        # =====================================================

        if IntentUtils.contains_any(
            text,
            self.DELETE_GOAL_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "delete_goal",
            }

        # =====================================================
        # MEMORY PREFERENCES
        # =====================================================

        # -----------------------
        # Set Preference
        # -----------------------

        if (
            re.match(r"my .+ is .+", text)
            or text.startswith(
                (
                    "i live in ",
                    "remember that my ",
                )
            )
        ):
            return {
                "destination": "BRAIN",
                "intent": "set_preference",
            }

        # -----------------------
        # Get Preference
        # -----------------------

        for phrase in self.MEMORY_QUERIES:
            if phrase in text:
                return {
                    "destination": "BRAIN",
                    "intent": "get_preference",
                }

        if (
            re.match(r"what is my .+", text)
            or text.startswith(
                (
                    "tell me my ",
                    "do you remember my ",
                )
            )
        ):
            return {
                "destination": "BRAIN",
                "intent": "get_preference",
            }

        # =====================================================
        # SEARCH RESULT REFERENCE
        # =====================================================

        if text in (
            "open the first one",
            "open first result",
            "open first",
            "open second",
            "open third",
        ):
            return {
                "destination": "BRAIN",
                "intent": "search_result",
            }

        # =====================================================
        # DEFAULT
        # =====================================================

        return {
            "destination": "AI",
            "intent": "chat",
        }

    def normalize(self, text):
        """Normalize common variations and contractions."""

        text = text.lower().strip()

        for wrong, correct in self.NORMALIZATION.items():
            text = text.replace(
                wrong,
                correct,
            )

        return text
