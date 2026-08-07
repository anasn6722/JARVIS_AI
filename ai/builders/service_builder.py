from ai.agent.ai_planner import AIPlanner
from ai.agent.goal_ai_planner import GoalAIPlanner
from ai.agent.goal_classifier import GoalClassifier
from ai.agent.verifier import AgentVerifier
from ai.builders.tool_registry_builder import ToolRegistryBuilder
from ai.context.session_context import SessionContext
from ai.context_manager import ContextManager
from ai.conversation.command_splitter import CommandSplitter
from ai.conversation.conversation_manager import ConversationManager
from ai.conversation.conversation_memory import ConversationMemory
from ai.conversation.reference_resolver import ReferenceResolver
from ai.entity_extractor import EntityExtractor
from ai.execution.ai_executor import AIExecutor
from ai.execution.builtin_executor import BuiltinExecutor
from ai.execution.execution_engine import ExecutionEngine
from ai.execution.execution_manager import ExecutionManager
from ai.execution.planner_executor import PlannerExecutor
from ai.execution.plugin_executor import PluginExecutor
from ai.goal_manager import GoalManager
from ai.handlers.app_handler import AppHandler
from ai.handlers.builtin_handler import BuiltinHandler
from ai.handlers.chat_handler import ChatHandler
from ai.handlers.execution_handler import ExecutionHandler
from ai.handlers.goal_handler import GoalHandler
from ai.handlers.memory_handler import MemoryHandler
from ai.history.action_history import ActionHistory
from ai.intent_classifier import IntentClassifier
from ai.knowledge.manager import KnowledgeManager
from ai.knowledge.source_registry import SourceRegistry
from ai.knowledge.sources.memory_source import MemorySource
from ai.knowledge.sources.wikipedia_source import WikipediaSource
from ai.llm.manager import LLMManager
from ai.managers.command_manager import CommandManager
from ai.managers.planning_manager import PlanningManager
from ai.memory.goal_memory import GoalMemory
from ai.memory_extractor import MemoryExtractor
from ai.planner.app_planner import AppPlanner
from ai.planner.goal_planner import GoalPlanner
from ai.planner.identity_planner import IdentityPlanner
from ai.planner.memory_planner import MemoryPlanner
from ai.planner.planner_registry import PlannerRegistry
from ai.planner.search_planner import SearchPlanner
from ai.planner.task_parser import TaskParser
from ai.planner.time_planner import TimePlanner
from ai.reasoning.reasoning_engine import ReasoningEngine
from ai.skills.skill_manager import SkillManager
from ai.skills.system_skill import SystemSkill
from ai.tools.tool_executor import ToolExecutor
from ai.tools.tool_registry import ToolRegistry
from ai.workflow.graph_builder import GraphBuilder
from ai.workflow.workflow_manager import WorkflowManager
from automation.system import SystemController
from automation.web import WebController
from memory.auto_memory import AutoMemoryExtractor
from memory.chat_memory import ChatMemory
from memory.database import Database
from memory.memory_manager import MemoryManager
from memory.memory_service import MemoryService
from memory.profile_memory import ProfileMemory
from memory.query_parser import MemoryQueryParser
from plugins.plugin_manager import PluginManager


class ServiceBuilder:

    @staticmethod
    def build(brain):
        

        # =====================================================
        # Core
        # =====================================================

        brain.system = SystemController()
        brain.web = WebController()
        brain.database = Database()

        # =====================================================
        # Database & Memory
        # =====================================================

        brain.chat_memory = ChatMemory(brain.database)
        brain.profile = ProfileMemory(brain.database)

        brain.memory = MemoryService(brain.database)
        brain.memory_manager = MemoryManager(brain.database)

        brain.goal_memory = GoalMemory()
        brain.goal_manager = GoalManager(brain.goal_memory)

        brain.memory_query_parser = MemoryQueryParser()
        brain.memory_extractor = MemoryExtractor()
        brain.auto_memory = AutoMemoryExtractor()

        # =====================================================
        # Knowledge
        # =====================================================

        brain.source_registry = SourceRegistry()

        brain.source_registry.register(
            MemorySource(brain.memory)
        )

        brain.source_registry.register(
            WikipediaSource()
        )

        brain.knowledge_manager = KnowledgeManager(
            brain.source_registry
        )

        # =====================================================
        # AI / LLM
        # =====================================================

        brain.llm = LLMManager()

        # =====================================================
        # Plugins
        # =====================================================

        brain.plugin_manager = PluginManager()

        # =====================================================
        # Context
        # =====================================================

        brain.context = ContextManager()
        brain.session = SessionContext()
        brain.action_history = ActionHistory()

        # =====================================================
        # NLP
        # =====================================================

        brain.intent_classifier = IntentClassifier()
        brain.entity_extractor = EntityExtractor()
        brain.goal_classifier = GoalClassifier()

        # =====================================================
        # Conversation
        # =====================================================

        brain.conversation_manager = ConversationManager()
        brain.conversation_memory = ConversationMemory()

        brain.command_splitter = CommandSplitter()
        brain.task_parser = TaskParser()

        brain.graph_builder = GraphBuilder()

        brain.reference_resolver = ReferenceResolver(
            brain.conversation_memory
        )

        brain.reasoning = ReasoningEngine(brain)

        # =====================================================
        # Planning
        # =====================================================

        brain.ai_planner = AIPlanner(brain.llm)

        brain.goal_ai_planner = GoalAIPlanner(
            brain.llm
        )

        brain.planner_registry = PlannerRegistry()

        brain.planner_registry.register(AppPlanner())
        brain.planner_registry.register(SearchPlanner())
        brain.planner_registry.register(MemoryPlanner())

        brain.planner_registry.register(
            GoalPlanner(
                brain.goal_ai_planner,
                brain.task_parser,
            )
        )

        brain.planner_registry.register(TimePlanner())
        brain.planner_registry.register(IdentityPlanner())

        brain.planning_manager = PlanningManager(
            brain.planner_registry,
            brain.ai_planner,
            brain,
        )

        # =====================================================
        # Handlers
        # =====================================================

        brain.builtin = BuiltinHandler(brain)

        brain.app_handler = AppHandler(brain)

        brain.chat_handler = ChatHandler(brain)

        brain.memory_handler = MemoryHandler(brain)

        brain.goal_handler = GoalHandler(brain)

        brain.execution_handler = ExecutionHandler(brain)

        # =====================================================
        # Tool System
        # =====================================================

        ToolRegistryBuilder.build(brain)

        # =====================================================
        # Workflow
        # =====================================================

        brain.workflow_manager = WorkflowManager(
            brain.tool_executor
        )

        # =====================================================
        # Execution
        # =====================================================

        brain.execution_engine = ExecutionEngine(
            brain.workflow_manager
        )

        brain.execution_manager = ExecutionManager(
            execution_engine=brain.execution_engine,
            conversation_memory=brain.conversation_memory,
            chat_memory=brain.chat_memory,
            conversation_manager=brain.conversation_manager,
            context=brain.context,
            action_history=brain.action_history,
        )

        brain.ai_executor = AIExecutor(
            brain.llm,
            brain.conversation_manager,
            brain.memory,
        )

        brain.builtin_executor = BuiltinExecutor(brain)

        brain.plugin_executor = PluginExecutor(brain)

        brain.planner_executor = PlannerExecutor(brain)

        # =====================================================
        # Command System
        # =====================================================

        brain.command_manager = CommandManager(
            brain.context,
            brain.intent_classifier,
            brain.entity_extractor,
            brain.goal_classifier,
            brain.reference_resolver,
        )

        brain.agent_verifier = AgentVerifier()

        # =====================================================
        # Skills
        # =====================================================   

        brain.skill_manager = SkillManager()

        brain.skill_manager.register(
            SystemSkill(brain)
        )  