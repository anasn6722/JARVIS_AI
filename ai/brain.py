from datetime import datetime, timezone

from ai.intent import IntentRecognizer
from automation.system import SystemController
from automation.web import WebController


class Brain:
    def __init__(self):
        self.system = SystemController()
        self.web = WebController()
        self.intent = IntentRecognizer()

        self.apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "explorer": "explorer.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "paint": "mspaint.exe",
            "camera": "microsoft.windows.camera:",
            "spotify": "spotify.exe",
            "discord": "Discord.exe",
            "code": "Code.exe",
            "vscode": "Code.exe",
        }

        self.websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://github.com",
            "chatgpt": "https://chat.openai.com",
            "gmail": "https://mail.google.com",
            "wikipedia": "https://www.wikipedia.org",
            "instagram": "https://www.instagram.com",
            "facebook": "https://www.facebook.com",
        }

    def process(self, command: str) -> str:
        intent = self.intent.recognize(command)
        command = command.lower().strip()

        # Greetings
        if intent == "hello":
            return "Hello Anas! 👋"

        if intent == "identity":
            return "I am JARVIS, your personal AI assistant."

        # Time
        if intent == "time":
            return datetime.now(timezone.utc).astimezone().strftime(
                "Current time: %I:%M:%S %p"
            )

        # Google Search
        if intent == "search":
            query = command.replace("search ", "", 1).strip()

            self.web.google_search(query)

            return f"Searching Google for {query}."

        # YouTube Search
        if intent == "youtube":
            query = command.replace("youtube ", "", 1).strip()

            self.web.youtube_search(query)

            return f"Searching YouTube for {query}."

        # Open websites and applications
        if intent == "open":
            name = command.replace("open ", "", 1).strip()

            # Website
            if name in self.websites:
                self.web.open_url(self.websites[name])
                return f"Opening {name.title()}."

            # Desktop application
            if name in self.apps:
                if self.system.open_program(self.apps[name]):
                    return f"Opening {name.title()}."

                return f"I couldn't open {name}."

        return "Sorry, I don't understand that command yet."