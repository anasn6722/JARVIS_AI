import pyttsx3

from voice.language_manager import language_manager


class Speaker:

    def speak(self, text):

        print(
            "Creating engine..."
        )

        engine = pyttsx3.init(
            "sapi5"
        )

        voices = engine.getProperty(
            "voices"
        )

        selected_voice = None

        # -----------------------------------------------------
        # Try to find a voice matching the selected language.
        # -----------------------------------------------------

        language_codes = (
            language_manager.speech_codes()
        )

        for voice in voices:

            voice_languages = getattr(
                voice,
                "languages",
                [],
            )

            voice_data = str(
                voice_languages
            ).lower()

            for code in language_codes:

                normalized_code = (
                    code.lower()
                    .replace("-", "")
                    .replace("_", "")
                )

                if normalized_code in voice_data:

                    selected_voice = voice
                    break

            if selected_voice:
                break

        # -----------------------------------------------------
        # Fallback to first installed voice.
        # -----------------------------------------------------

        if selected_voice is None and voices:
            selected_voice = voices[0]

        if selected_voice is not None:

            engine.setProperty(
                "voice",
                selected_voice.id,
            )

            print(
                "Selected voice:",
                selected_voice.name,
            )

        engine.setProperty(
            "rate",
            175,
        )

        engine.setProperty(
            "volume",
            1.0,
        )

        print(
            "Speaking:",
            text,
        )

        engine.say(
            text
        )

        engine.runAndWait()

        engine.stop()

        print(
            "Finished"
        )