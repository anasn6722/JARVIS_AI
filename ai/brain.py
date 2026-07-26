from datetime import datetime, timezone

from ai.commands import CommandRegistry
from ai.intent import IntentRecognizer
from ai.text_utils import TextUtils
from automation.system import SystemController
from automation.web import WebController
from memory.chat_memory import ChatMemory
from memory.profile_memory import ProfileMemory


class Brain:
    def __init__(self):
        self.system = SystemController()
        self.web = WebController()
        self.intent = IntentRecognizer()
        self.registry = CommandRegistry()
        self.memory = ChatMemory()
        self.profile = ProfileMemory()
        self.memory = ChatMemory()
        self.profile = ProfileMemory()
        self.registry.register("hello", self.handle_hello)
        self.registry.register("time", self.handle_time)
        self.registry.register("identity", self.handle_identity)
        self.registry.register("search", self.handle_search)
        self.registry.register("youtube", self.handle_youtube)
        self.registry.register("open", self.handle_open)

        self.registry.register(
            "last_message",
            self.handle_last_message,
        )
        
        self.registry.register(
            "history",
            self.handle_history,
        )
        self.registry.register(
            "set_name",
            self.handle_set_name,
        )

        self.registry.register(
            "get_name",
            self.handle_get_name,
        )
        
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
        command = TextUtils.normalize(command)
        self.memory.add(
            "User",
            command,
        )
        
        intent = self.intent.recognize(command)

        return self.registry.execute(
            intent,
            command,
        )
        

    def handle_hello(self, command):
        return "Hello Anas! 👋"

    def handle_identity(self, command):
        return "I am JARVIS, your personal AI assistant."

    def handle_time(self, command):
        return datetime.now(timezone.utc).astimezone().strftime(
        "Current time: %I:%M:%S %p"
        )

    def handle_search(self, command):
        query = command.replace("search ", "", 1).strip()

        self.web.google_search(query)

        return f"Searching Google for {query}."

    def handle_youtube(self, command):
        query = command.replace("youtube ", "", 1).strip()

        self.web.youtube_search(query)

        return f"Searching YouTube for {query}."

    def handle_open(self, command):
        words = command.split()
        name = words[-1].lower()

        if name in self.websites:
            self.web.open_url(self.websites[name])
            return f"Opening {name.title()}."

        if name in self.apps:
            if self.system.open_program(self.apps[name]):
               return f"Opening {name.title()}."

            return f"I couldn't open {name}."

        return f"I don't know how to open {name}."

    def handle_last_message(self, command):
        history = self.memory.get_all()

        if len(history) >= 2:
           return f"Your last message was: {history[-2]['message']}"

        return "I don't remember any previous message."

    def handle_history(self, command):
        history = self.memory.get_all()

        if len(history) <= 1:
            return "No previous conversation found."

        response = "Conversation History:\n\n"

        for i, item in enumerate(history[:-1], start=1):
            response += (
                f"{i}. {item['speaker']}: "
                f"{item['message']}\n"
            )

        return response

    def handle_set_name(self, command):
        name = command.replace(
            "my name is",
            "",
            1,
        ).strip()

        if not name:
            return "Please tell me your name."

        self.profile.set("name", name)

        return f"Nice to meet you, {name}! I'll remember your name."

    def handle_get_name(self, command):
        name = self.profile.get("name")

        if name:
            return f"Your name is {name}."

        return "I don't know your name yet."