from ai.model_manager import ModelManager


class ModelRouter:

    def __init__(self):

        self.manager = ModelManager()

    @property
    def current(self):

        return self.manager.current

    def next(self):

        self.manager.next_model()

    def reset(self):

        self.manager.reset()

    @property
    def count(self):

        return len(
            self.manager.models
        )