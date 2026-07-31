from datetime import datetime, timezone

from ai.agent.ai_planner import AIPlanner
from ai.agent.executor import AgentExecutor
from ai.agent.goal_classifier import GoalClassifier
from ai.agent.planner import Planner
from ai.agent.verifier import AgentVerifier
from ai.command import Command
from ai.command_parser import CommandParser
from ai.commands import CommandRegistry
from ai.context_manager import ContextManager
from ai.context_resolver import ContextResolver
from ai.entity_extractor import EntityExtractor
from ai.goal_manager import GoalManager
from ai.intent_classifier import IntentClassifier
from ai.llm import LLM
from ai.managers.command_manager import CommandManager
from ai.planner import Planner
from ai.skills.skill_manager import SkillManager
from ai.skills.system_skill import SystemSkill
from ai.text_utils import TextUtils
from ai.tools.tool_executor import ToolExecutor
from ai.tools.tool_registry import ToolRegistry
from automation.system import SystemController
from automation.web import WebController
from brain.services import APPS, WEBSITES
from memory.chat_memory import ChatMemory
from memory.memory_manager import MemoryManager
from memory.profile_memory import ProfileMemory
from plugins.plugin_manager import PluginManager


class Brain:
    def __init__(self):
        

        self.system = SystemController()
        self.web = WebController()
        self.registry = CommandRegistry()
        self.memory = ChatMemory()
        self.llm = LLM()
        self.profile = ProfileMemory()
        self.plugin_manager = PluginManager()
        self.intent_classifier = IntentClassifier()
        self.context = ContextManager()
        # Skill System
        self.skill_manager = SkillManager()
        self.planner = Planner()
        self.agent_executor = AgentExecutor(self)
        self.goal_classifier = GoalClassifier()
        self.goal_manager = GoalManager()
        self.entity_extractor = EntityExtractor()
        self.long_memory = MemoryManager()
        
        self.agent_verifier = AgentVerifier()
        self.skill_manager.register(
            SystemSkill(self)
        )
        self.planner = Planner()
        self.ai_planner = AIPlanner(self.llm)
        from ai.managers.planning_manager import PlanningManager
        self.planning_manager = PlanningManager(
            self.ai_planner,
            self.planner,
            self,
        )

        

        self.tool_registry = ToolRegistry()
        self.tool_executor = ToolExecutor(
            self.tool_registry
        )
        self.context_resolver = ContextResolver(
            self.context
        )
        self.command_manager = CommandManager(
            self.context,
            self.intent_classifier,
            self.entity_extractor,
            self.goal_classifier,
        )
        
        self.registry.register("hello", self.handle_hello)
        self.registry.register("time", self.handle_time)
        self.registry.register("identity", self.handle_identity)
        self.registry.register("search", self.handle_search)
        self.registry.register("youtube", self.handle_youtube)
        self.registry.register("open", self.handle_open)

        self.tool_registry.register(
            "open",
            "Open any application",
            self.handle_open,
        )

        self.tool_registry.register(
            "search",
            "Search Google",
            self.handle_search,
        )

        self.tool_registry.register(
            "youtube_search",
            "Search videos on YouTube",
            self.handle_youtube,
        )

        self.tool_registry.register(
            "time",
            "current time",
            self.handle_time,
        )

        self.tool_registry.register(
            "identity",
            "Who is JARVIS",
            self.handle_identity,
        )

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
        self.registry.register(
            "add_goal",
            self.handle_add_goal,
        )

        self.registry.register(
            "show_goals",
            self.handle_show_goals,
        )

        self.apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "explorer": "explorer.exe",

            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",

            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",

            "paint": "mspaint.exe",

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
        
        self.memory.add(
            "User",
            command,
        )

        command_data, goal = self.command_manager.process(
            command,
        )
        
        destination = command_data.destination
        intent = command_data.intent
        self.context.update(
            intent=command_data.intent,
            command=command_data.original,
        )

        # -------------------------
        # Plugin Commands
        # -------------------------

        if destination == "PLUGIN":

            plugin_response = self.plugin_manager.execute(
                intent,
                command,
            )
            if plugin_response:
                return plugin_response

        print("=" * 50)
        print("ENTITIES:", command_data.entities)

        print("=" * 50)
        print("GOAL:", goal)

        print("=" * 50)
        print(command_data)

        print("=" * 50)
        print("COMMAND:", command_data.original)
        print("DESTINATION:", command_data.destination)
        print("INTENT:", command_data.intent)


        # -------------------------
        # Built-in Commands
        # -------------------------

        builtin_intents = {
            "set_name",
            "get_name",
            "last_message",
            "history",
            "add_goal",
            "show_goals",
        }

        if intent in builtin_intents:
        
            response = self.registry.execute(
                intent,
                command_data.original,
            )
            print("Registry returned:", response)

            if response:
            
                self.memory.add(
                    "Assistant",
                    response,
                )

                return response


        # -------------------------
        # AI Planner
        # -------------------------

        if destination == "BRAIN":
        
            tasks = self.planning_manager.plan(command_data)
            print("Brain received tasks:", tasks)

            if tasks:
            
                response = self.agent_executor.execute(tasks)

                self.context.last_tasks = tasks

                if response:
                
                    self.memory.add(
                        "Assistant",
                        response,
                    )

                    return response
        

    def handle_hello(self, command):
        return "Hello Anas! 👋"

    def handle_identity(self, command):
        return "I am JARVIS, your personal AI assistant."

    def handle_time(self, command):
        return datetime.now(timezone.utc).astimezone().strftime(
        "Current time: %I:%M:%S %p"
        )

    def handle_search(self, command):
        query = CommandParser.search_query(command)
        self.context.last_search = query
        self.context.update(
            search=query
        )

        self.web.google_search(query)

        return f"Searching Google for {query}."

    def handle_youtube(self, command):
        query = CommandParser.youtube_query(command)

        self.web.youtube_search(query)

        return f"Searching YouTube for {query}."
    
    def handle_open(self, command):

        # Called by ToolExecutor
        if isinstance(command, str):
            apps = [command.lower().strip()]

            # Called directly from Brain
        else:
            apps = command.entities.get("apps", [])
            websites = command.entities.get("websites", [])

            # Allow websites too
            apps.extend(websites)

        if not apps:
            return "I couldn't find anything to open."

        responses = []

        for app in apps:

            # Website
            if app in WEBSITES:
                self.web.open_url(WEBSITES[app])
                self.context.last_website = app
                responses.append(f"Opened {app.title()}.")
                continue

            # Application
            if app in APPS:

                success = self.system.open_program(APPS[app])

                if success:
                    self.context.last_app = app
                    responses.append(f"Opened {app.title()}.")
                else:
                    responses.append(f"Couldn't open {app.title()}.")

                continue

            responses.append(f"I don't know {app}.")

        return "\n".join(responses)
    
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
        name = command.replace("my name is", "", 1).strip()

        print("Saving:", name)

        if not name:
            return "Please tell me your name."

        self.profile.set("name", name)

        print("Database now contains:", self.profile.get("name"))

        return f"Nice to meet you, {name}!"
    
    def handle_get_name(self, command):
        name = self.profile.get("name")

        print("Retrieved:", name)

        if name:
            return f"Your name is {name}."

        return "I don't know your name yet."
    

    def available_tools(self):
        return [
            {
                "name": tool.name,
                "description": tool.description,
            }
        for tool in self.tool_registry.all()
        ]

    def process_agent(self, command: str):
        tasks = self.ai_planner.plan(command)

        if not tasks:
            tasks = self.planner.plan(command)

        responses = self.agent_executor.execute(tasks)

        return " ".join(responses)

    def handle_add_goal(self, command):
        goal = (
            command
            .replace("my goal is", "", 1)
            .replace("remember that i want to", "", 1)
            .replace("i want to", "", 1)
            .strip()
        )

        if not goal:
            return "Please tell me your goal."

        self.goal_manager.add(goal)
        self.context.update(
            goal=goal,
        )

        return f"I'll remember your goal: {goal}."


    def handle_show_goals(self, command):
        goals = self.goal_manager.all()

        if not goals:
            return "You don't have any saved goals."

        response = "Your goals are:\n"

        for i, goal in enumerate(goals, start=1):
            response += f"{i}. {goal}\n"

        return response.strip()

    def handle_open_task(self, app):

        if app in WEBSITES:
            self.web.open_url(WEBSITES[app])
            return f"Opened {app}."

        if app in APPS:

            if self.system.open_program(APPS[app]):
                return f"Opened {app}."

            return f"Couldn't open {app}."

        return f"I don't know {app}."

    def planner_context(self):

        last_tasks = getattr(
            self.context,
            "last_tasks",
            [],
        )

        return f"""
     Last App: {self.context.last_app}
     
     Last Search: {self.context.last_search}
     
     Current Goal: {self.context.current_goal}
     
     Previous Tasks:
     
     {last_tasks}
     """



if __name__ == "__main__":
        brain = Brain()

        print(
            brain.process_agent(
                "open chrome then search python classes and tell me the time"
            )
        )