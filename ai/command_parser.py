class CommandParser:

    SEARCH_WORDS = (
        "can you",
        "could you",
        "please",
        "search",
        "google",
        "find",
        "look up",
        "lookup",
    )

    OPEN_WORDS = (
        "please",
        "open",
        "launch",
        "start",
        "run",
    )

    YOUTUBE_WORDS = (
        "please",
        "youtube",
        "watch",
        "play",
    )

    @staticmethod
    def remove_words(text: str, words: tuple) -> str:
        text = text.lower()

        for word in words:
            text = text.replace(word, "")

        return " ".join(text.split())

    @classmethod
    def search_query(cls, text):
        return cls.remove_words(
            text,
            cls.SEARCH_WORDS,
        )

    @classmethod
    def youtube_query(cls, text):
        return cls.remove_words(
            text,
            cls.YOUTUBE_WORDS,
        )

    @classmethod
    def app_name(cls, text):
        return cls.remove_words(
            text,
            cls.OPEN_WORDS,
        )