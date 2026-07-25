from datetime import datetime, timezone

from automation.system import SystemController
from automation.web import WebController


class Brain:
    def __init__(self):
        self.system = SystemController()
        self.web = WebController()
        self.apps = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "spotify": "spotify.exe",
        "discord": "Discord.exe",
        "vscode": "Code.exe",
        "code": "Code.exe",
        "camera": "microsoft.windows.camera:",
        "paint": "mspaint.exe",
        }
        self.websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "chatgpt": "https://chat.openai.com",
        "github": "https://github.com",
        "gmail": "https://mail.google.com",
        "wikipedia": "https://www.wikipedia.org",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        }
        
    """
    The central command processor for JARVIS.
    """

    def process(self, command: str) -> str:
        """
        Process a user command and return a response.
        """

        command = command.lower()
        if "open notepad" in command:
            self.system.open_notepad()
            return "Opening Notepad."

        if "open calculator" in command:
            self.system.open_calculator()
            return "Opening Calculator."

        if "open explorer" in command:
            self.system.open_explorer()
            return "Opening File Explorer."

        if command == "hello":
            return "Hello Anas! 👋"

        if command == "who are you":
            return "I am JARVIS, your personal AI assistant."

        if command == "time":
            return datetime.now(timezone.utc).astimezone().strftime(
            "Current time: %I:%M:%S %p"
            )
        if command.startswith("open "):

            name = command.replace("open ", "").strip()

        if name in self.websites:
            self.web.open_url(self.websites[name])
            return f"Opening {name.title()}."

        if command.startswith("open "):

            app_name = command.replace("open ", "").strip()

            if app_name in self.apps:

                if self.system.open_program(self.apps[app_name]):

                    return f"Opening {app_name.title()}."

                return f"I couldn't open {app_name}."    

        return "Sorry, I don't understand that command yet."