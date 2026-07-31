from ai.agent.goal_classifier import GoalClassifier
from ai.command import Command
from ai.context_resolver import ContextResolver
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
    ):
        self.context = context

        self.intent_classifier = intent_classifier

        self.entity_extractor = entity_extractor

        self.goal_classifier = goal_classifier

        self.context_resolver = ContextResolver(
            context,
        )

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
        
        command_data = Command(
            original=original,      # Original speech
            intent=result["intent"],
            destination=result["destination"],
            entities=entities,
        )

        return command_data, goal