from ai.agent.goal_classifier import GoalClassifier
from ai.command import Command
from ai.context_resolver import ContextResolver
from ai.conversation.command_splitter import CommandSplitter
from ai.conversation.reference_resolver import ReferenceResolver
from ai.entity_extractor import EntityExtractor
from ai.intent_classifier import IntentClassifier
from ai.text_utils import TextUtils


class CommandManager:

    def __init__(
        self,
        context,
        intent_classifier,
        entity_extractor,
        goal_classifier,
        reference_resolver,
    ):
        self.context = context
        self.intent_classifier = intent_classifier
        self.entity_extractor = entity_extractor
        self.goal_classifier = goal_classifier
        self.command_splitter = CommandSplitter()
        self.context_resolver = ContextResolver(context)
        self.reference_resolver = reference_resolver

    def process_single(
        self,
        command: str,
    ):

        original = command

        command = TextUtils.normalize(command)

        command = self.context_resolver.resolve(command)

        entities = self.entity_extractor.extract(command)

        goal = self.goal_classifier.classify(command)

        result = self.intent_classifier.classify(command)

        # --------------------------
        # Goal Promotion
        # --------------------------

        if goal and result["intent"] == "chat":

            result["intent"] = "add_goal"
            result["destination"] = "BRAIN"

        command_data = Command(
            original=original,
            intent=result["intent"],
            destination=result["destination"],
            entities=entities,
        )

        command_data = self.reference_resolver.resolve(command_data)

        return command_data, goal


    def process(
        self,
        command: str,
    ):
    
        original = command
    
        command = TextUtils.normalize(command)
    
        command = self.context_resolver.resolve(command)
    
        entities = self.entity_extractor.extract(command)
    
        goal = self.goal_classifier.classify(command)
    
        result = self.intent_classifier.classify(command)
    
        # Goal Promotion
        if goal and result["intent"] == "chat":
            result["intent"] = "add_goal"
            result["destination"] = "BRAIN"
    
        command_data = Command(
            original=original,
            intent=result["intent"],
            destination=result["destination"],
            entities=entities,
            goal=goal,
            requires_planning=(goal is not None),
        )
    
        command_data = self.reference_resolver.resolve(command_data)
    
        return command_data,goal