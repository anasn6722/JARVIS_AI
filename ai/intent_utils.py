class IntentUtils:

    @staticmethod
    def contains_any(text: str, words):

        text = text.lower()

        return any(
            word in text
            for word in words
        )

    @staticmethod
    def starts_with_any(text: str, words):

        text = text.lower()

        return any(
            text.startswith(word)
            for word in words
        )