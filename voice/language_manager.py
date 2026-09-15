from config.languages import (
    DEFAULT_LANGUAGE,
    LANGUAGES,
)


class LanguageManager:
    """Manage JARVIS single-language recognition and response mode."""

    def __init__(self):
        self.primary_language = DEFAULT_LANGUAGE

        # Only one language is active at a time.
        self.enabled_languages = [
            DEFAULT_LANGUAGE
        ]

        # Strict single-language mode.
        self.auto_detect = False

        # Responses follow the selected language.
        self.respond_in_detected_language = False

        # Kept for compatibility with the existing response system.
        self.detected_language = DEFAULT_LANGUAGE

    # =========================================================
    # PRIMARY LANGUAGE
    # =========================================================

    def set_primary_language(self, language):
        """
        Select the ONE active language.

        Selecting a language automatically makes it the only
        enabled language.
        """

        if language not in LANGUAGES:
            return False

        self.primary_language = language

        # Strict single-language mode:
        self.enabled_languages = [
            language
        ]

        # Keep response language synchronized immediately.
        self.detected_language = language

        return True

    def get_primary_language(self):
        return self.primary_language

    # =========================================================
    # ENABLED LANGUAGES
    # =========================================================

    def enable_language(self, language):
        """
        Compatibility method.

        In single-language mode, enabling a language actually
        selects it as the only active language.
        """

        return self.set_primary_language(
            language
        )

    def disable_language(self, language):
        """
        A selected language cannot be disabled directly.
        Select another language instead.
        """

        if language == self.primary_language:
            return False

        # Nothing to remove because only the primary language
        # is active.
        return True

    def is_enabled(self, language):
        return language == self.primary_language

    # =========================================================
    # RECOGNITION
    # =========================================================

    def recognition_code(self):
        """
        Return the ONLY recognition code allowed.
        """

        return LANGUAGES[
            self.primary_language
        ]["code"]

    def speech_codes(self):
        """
        Return speech codes for the selected language.

        The first/main code represents the active language.
        """

        return LANGUAGES[
            self.primary_language
        ].get(
            "speech_codes",
            [
                self.recognition_code()
            ],
        )

    # =========================================================
    # RESPONSE LANGUAGE
    # =========================================================

    def set_detected_language(self, language):
        """
        Compatibility method.

        In strict mode we do not actually switch languages
        based on detected speech.
        """

        if language not in LANGUAGES:
            return False

        # Do not allow recognition to silently switch the
        # selected language.
        self.detected_language = (
            self.primary_language
        )

        return True

    def get_response_language(self):
        """
        Always respond in the selected language.
        """

        return self.primary_language

    def set_respond_in_detected_language(self, enabled):
        """
        Compatibility method.

        Strict mode always responds in the selected language.
        """

        self.respond_in_detected_language = False

    # =========================================================
    # AUTO DETECTION
    # =========================================================

    def set_auto_detect(self, enabled):
        """
        Automatic language detection is intentionally disabled.
        """

        self.auto_detect = False

    def is_auto_detect(self):
        return False

    # =========================================================
    # AVAILABLE
    # =========================================================

    @staticmethod
    def available_languages():
        return list(
            LANGUAGES.keys()
        )

    # =========================================================
    # ACTIVE LANGUAGE
    # =========================================================

    def active_languages(self):
        """
        Return the single active language.
        """

        return [
            self.primary_language
        ]

    # =========================================================
    # RECOGNITION CODES
    # =========================================================

    def enabled_recognition_codes(self):
        """
        Return ONLY the recognition code for the selected
        language.

        This method is retained because listener.py still
        uses it.
        """

        return [
            self.recognition_code()
        ]

    # =========================================================
    # LANGUAGE LOOKUP
    # =========================================================

    def language_for_code(self, code):
        """
        Return the selected language only when the code belongs
        to the selected language.

        Unknown/non-selected codes fall back to the primary
        language instead of changing the active language.
        """

        selected = LANGUAGES.get(
            self.primary_language
        )

        if selected:

            if code == selected.get("code"):
                return self.primary_language

            if code in selected.get(
                "speech_codes",
                [],
            ):
                return self.primary_language

        return self.primary_language


language_manager = LanguageManager()