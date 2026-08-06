from abc import ABC, abstractmethod


class Planner(ABC):

    @abstractmethod
    def can_plan(self, command):
        pass

    @abstractmethod
    def plan(self, command):
        pass