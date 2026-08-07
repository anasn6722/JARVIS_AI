from abc import ABC, abstractmethod


class KnowledgeSource(ABC):

    @property
    @abstractmethod
    def name(self):
        ...

    @abstractmethod
    def search(self, query):
        ...