class IntentClassifier:

    def classify(self, text: str) -> dict:
        text = text.lower().strip()

        # -----------------------
        # Open Applications
        # -----------------------
        if any(word in text for word in (
            "open",
            "launch",
            "start",
            "run",
            )):
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
        if any(word in text for word in (
            "hello",
            "hi",
            "hey",
        )):
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
        if text.startswith("search "):
            return {
                "destination": "BRAIN",
                "intent": "search",
            }

        # -----------------------
        # YouTube
        # -----------------------
        if text.startswith("youtube "):
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