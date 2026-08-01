import re

from ai.intent_utils import IntentUtils


class IntentClassifier:

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

    
    def classify(self, text: str) -> dict:
        text = text.lower().strip()

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

        # -----------------------
        # Time
        # -----------------------
        if any(word in text for word in (
            "time",
            "clock",
        )):
            return {
                "destination": "BRAIN",
                "intent": "time",
            }

        # -----------------------
        # Greeting
        # -----------------------
        if IntentUtils.contains_any(
            text,
            self.HELLO_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "hello",
            }

        # -----------------------
        # Identity
        # -----------------------
        if any(word in text for word in (
            "who are you",
            "your name",
        )):
            return {
                "destination": "BRAIN",
                "intent": "identity",
            }

        # -----------------------
        # Google Search
        # -----------------------

        if IntentUtils.contains_any(
            text,
            self.SEARCH_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "search",
            }

        # -----------------------
        # YouTube
        # -----------------------
        if IntentUtils.contains_any(
            text,
            self.YOUTUBE_WORDS,
        ):
            return {
                "destination": "BRAIN",
                "intent": "youtube",
            }

        # -----------------------
        # Set Name
        # -----------------------
        if text.startswith("my name is"):
            return {
                "destination": "BRAIN",
                "intent": "set_name",
            }

        # -----------------------
        # Get Name
        # -----------------------
        if "what is my name" in text:
            return {
                "destination": "BRAIN",
                "intent": "get_name",
            }

        # -----------------------
        # Add Goal
        # -----------------------
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
           

        # -----------------------
        # Show Goals
        # -----------------------
        if (
            "what are my goals" in text
            or"what is my goal" in text
            or "show my goals" in text
            or"show my goal" in text
            or "show goals" in text
            or "my goals" == text
        ):
            return {
                "destination": "BRAIN",
                "intent": "show_goals",
            }

        # -----------------------
        # Memory Preferences
        # -----------------------

        # Set preference
        if (
            re.match(r"my .+ is .+", text)
            or text.startswith((
                "i live in ",
                "remember that my ",
            ))
        ):
            return {
                "destination": "BRAIN",
                "intent": "set_preference",
            }

        # Get preference
        if (
            re.match(r"what is my .+", text)
            or text.startswith((
                "tell me my ",
                "do you remember my ",
            ))
        ):
            return {
                "destination": "BRAIN",
                "intent": "get_preference",
            }
        
       
        if text in (
            "close it",
            "close",
        ):
            return {
                "destination": "BRAIN",
                "intent": "close_last",
            }
        

        # -----------------------
        # Default
        # -----------------------
        return {
            "destination": "AI",
            "intent": "chat",
        }

        