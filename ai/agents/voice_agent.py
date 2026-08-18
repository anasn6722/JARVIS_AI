from ai.agents.base_agent import BaseAgent
from ai.orchestration.agent_result import AgentResult
from voice.language_manager import language_manager


class VoiceAgent(BaseAgent):
    """Handles JARVIS voice and language configuration."""

    name = "voice"

    description = (
        "Handles voice interaction, speech recognition, "
        "wake words, languages, Roman Urdu, and speech output."
    )

    VOICE_PHRASES = (
        "voice",
        "voice settings",
        "voice system",
        "wake word",
        "wake up word",
        "language",
        "spoken language",
        "speech language",
        "recognition language",
        "voice language",
        "roman urdu",
        "urdu",
        "punjabi",
        "hindi",
        "english",
        "speak",
        "speech",
        "microphone",
        "mic",
        "listen",
        "stop listening",
        "start listening",
    )

    LANGUAGE_ALIASES = {
        "english": "English",
        "urdu": "Urdu",
        "roman urdu": "Roman Urdu",
        "punjabi": "Punjabi",
        "hindi": "Hindi",
    }

    def can_handle(self, command):
        text = (
            command.original
            .lower()
            .strip()
        )
    
        if command.intent == "navigate" and "voice" in text:
            return False
    
        if command.intent == "voice_language":
            return True
    
        return any(
            phrase in text
            for phrase in self.VOICE_PHRASES
        )

    # =========================================================
    # LANGUAGE DETECTION
    # =========================================================

    @classmethod
    def _extract_language(cls, text):
        text = text.lower()

        # Longest phrases first.
        for alias in sorted(
            cls.LANGUAGE_ALIASES,
            key=len,
            reverse=True,
        ):
            if alias in text:
                return cls.LANGUAGE_ALIASES[
                    alias
                ]

        return None

    # =========================================================
    # PRIMARY LANGUAGE
    # =========================================================

    def _change_primary_language(self, text):
        language = self._extract_language(
            text
        )

        if language is None:
            return (
                False,
                "Please tell me which language "
                "you want to use.",
            )

        if not language_manager.set_primary_language(
            language
        ):
            return (
                False,
                f"I couldn't activate {language}.",
            )

        language_manager.enable_language(
            language
        )

        return (
            True,
            f"Primary voice language changed to {language}.",
        )

    # =========================================================
    # AUTOMATIC DETECTION
    # =========================================================

    @staticmethod
    def _set_auto_detection(text):
        if (
            "disable automatic language detection"
            in text
            or "turn off automatic language detection"
            in text
            or "stop automatic language detection"
            in text
        ):
            language_manager.set_auto_detect(
                False
            )

            return (
                True,
                "Automatic language detection disabled.",
            )

        if (
            "enable automatic language detection"
            in text
            or "turn on automatic language detection"
            in text
            or "use automatic language detection"
            in text
            or "automatically detect language"
            in text
        ):
            language_manager.set_auto_detect(
                True
            )

            return (
                True,
                "Automatic language detection enabled.",
            )

        return None

    # =========================================================
    # RESPONSE LANGUAGE
    # =========================================================

    @staticmethod
    def _set_response_language(text):
        if (
            "respond in detected language"
            in text
            or "reply in detected language"
            in text
            or "respond in the detected language"
            in text
            or "reply in the detected language"
            in text
        ):
            language_manager.set_respond_in_detected_language(
                True
            )

            return (
                True,
                "I will respond in the detected language.",
            )

        if (
            "respond in primary language"
            in text
            or "reply in primary language"
            in text
            or "use my primary language for responses"
            in text
        ):
            language_manager.set_respond_in_detected_language(
                False
            )

            return (
                True,
                "I will respond in the primary language.",
            )

        return None

    # =========================================================
    # ENABLE LANGUAGE
    # =========================================================

    def _enable_language(self, text):
        language = self._extract_language(
            text
        )

        if language is None:
            return None

        if (
            "enable " in text
            or "allow " in text
            or "support " in text
            or "understand " in text
        ):
            language_manager.enable_language(
                language
            )

            return (
                True,
                f"{language} is now enabled.",
            )

        if (
            "disable " in text
            or "turn off " in text
        ):
            if language_manager.disable_language(
                language
            ):
                return (
                    True,
                    f"{language} has been disabled.",
                )

            return (
                False,
                f"{language} cannot be disabled "
                "while it is the primary language.",
            )

        return None

    # =========================================================
    # RUN
    # =========================================================

    def run(self, context):

        text = (
            context.command.original
            .lower()
            .strip()
        )

        # -----------------------------------------------------
        # Automatic detection
        # -----------------------------------------------------

        result = self._set_auto_detection(
            text
        )

        if result is not None:
            success, response = result

            return AgentResult(
                success=success,
                agent=self.name,
                metadata={
                    "voice_operation": "auto_detection",
                    "response": response,
                },
            )

        # -----------------------------------------------------
        # Response language
        # -----------------------------------------------------

        result = self._set_response_language(
            text
        )

        if result is not None:
            success, response = result

            return AgentResult(
                success=success,
                agent=self.name,
                metadata={
                    "voice_operation": "response_language",
                    "response": response,
                },
            )

        # -----------------------------------------------------
        # Enable / disable supported languages
        # -----------------------------------------------------

        result = self._enable_language(
            text
        )

        if result is not None:
            success, response = result

            return AgentResult(
                success=success,
                agent=self.name,
                metadata={
                    "voice_operation": "language_enabled",
                    "response": response,
                },
            )

        # -----------------------------------------------------
        # Change primary language
        # -----------------------------------------------------

        if any(
            phrase in text
            for phrase in (
                "switch to",
                "change to",
                "change my voice language",
                "change my speech language",
                "use ",
                "speak ",
                "talk in ",
                "set language to",
                "set my language to",
            )
        ):
            success, response = (
                self._change_primary_language(
                    text
                )
            )

            return AgentResult(
                success=success,
                agent=self.name,
                metadata={
                    "voice_operation": "primary_language",
                    "language": (
                        language_manager.get_primary_language()
                    ),
                    "response": response,
                },
            )

        # -----------------------------------------------------
        # No direct operation
        # -----------------------------------------------------

        return AgentResult(
            success=True,
            agent=self.name,
            metadata={
                "delegate_to_existing_pipeline": True,
                "voice_intent": context.command.intent,
            },
        )

    