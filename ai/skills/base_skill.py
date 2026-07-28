from abc import ABC, abstractmethod


class BaseSkill(ABC):

    @abstractmethod
    def can_handle(self, intent: str) -> bool:
        pass

    @abstractmethod
    def execute(self, command: str):
        pass