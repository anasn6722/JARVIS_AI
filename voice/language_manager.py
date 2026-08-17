from config.languages import (
    DEFAULT_LANGUAGE,
    LANGUAGES,
)


class LanguageManager:
    """Manage JARVIS recognition and response language."""

    def __init__(self):
        self.primary_language = DEFAULT_LANGUAGE

        self.enabled_languages = {
            "English",
            "Urdu",
            "Roman Urdu",
            "Punjabi",
            "Hindi",
        }

        self.auto_detect = True
        self.respond_in_detected_language = True

        # Language detected from the most recent user input.
        self.detected_language = DEFAULT_LANGUAGE

    # =========================================================
    # PRIMARY LANGUAGE
    # =========================================================

    def set_primary_language(self, language):
        if language not in LANGUAGES:
            return False

        self.primary_language = language
        return True

    def get_primary_language(self):
        return self.primary_language

    # =========================================================
    # ENABLED LANGUAGES
    # =========================================================

    def enable_language(self, language):
        if language not in LANGUAGES:
            return False

        self.enabled_languages.add(language)
        return True

    def disable_language(self, language):
        if language == self.primary_language:
            return False

        self.enabled_languages.discard(language)
        return True

    def is_enabled(self, language):
        return language in self.enabled_languages

    # =========================================================
    # RECOGNITION
    # =========================================================

    def recognition_code(self):
        return LANGUAGES[
            self.primary_language
        ]["code"]

    def speech_codes(self):
        return LANGUAGES[
            self.primary_language
        ]["speech_codes"]

    # =========================================================
    # RESPONSE LANGUAGE
    # =========================================================

    def set_detected_language(self, language):
        if language not in LANGUAGES:
            return False

        self.detected_language = language
        return True

    def get_response_language(self):
        if self.respond_in_detected_language:
            return self.detected_language

        return self.primary_language

    def set_respond_in_detected_language(self, enabled):
        self.respond_in_detected_language = bool(
            enabled
        )

    # =========================================================
    # AUTO DETECTION
    # =========================================================

    def set_auto_detect(self, enabled):
        self.auto_detect = bool(enabled)

    def is_auto_detect(self):
        return self.auto_detect

    # =========================================================
    # AVAILABLE
    # =========================================================

    @staticmethod
    def available_languages():
        return list(
            LANGUAGES.keys()
        )


language_manager = LanguageManager()