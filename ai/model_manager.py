class ModelManager:
    def __init__(self):
        self.models = [
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
        ]

        self.index = 0

    @property
    def current(self):
        return self.models[self.index]

    def next_model(self):
        self.index += 1

        if self.index >= len(self.models):
            self.index = 0

        return self.current

    def reset(self):
        self.index = 0