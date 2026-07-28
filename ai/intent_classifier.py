from ai.intent_utils import IntentUtils


class IntentClassifier:

    OPEN_WORDS = (
        "open",
        "launch",
        "start",
        "run",
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
        # Default
        # -----------------------
        return {
            "destination": "AI",
            "intent": "chat",
        }