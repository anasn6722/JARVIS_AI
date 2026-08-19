import re

from voice.language_manager import language_manager


class ResponseStage:

    def __init__(self, brain):
        self.brain = brain

        self._translation_cache = {}

    def run(self, context):

        # =====================================================
        # DEFAULT RESPONSE
        # =====================================================

        if not context.response:

            if context.verification_errors:

                context.response = (
                    "I couldn't complete the request."
                )

            else:

                context.response = (
                    "The request completed, "
                    "but no response was produced."
                )

        # =====================================================
        # VERIFICATION ERRORS
        # =====================================================

        if context.verification_errors:

            errors = "\n".join(
                f"- {error}"
                for error in context.verification_errors
            )

            context.response = (
                "I couldn't complete the request.\n"
                f"{errors}"
            )

        # =====================================================
        # RESPONSE LANGUAGE
        # =====================================================

        response_language = (
            language_manager.get_response_language()
        )

        print(
            "Response language:",
            response_language,
        )

        print(
            "Detected language:",
            language_manager.detected_language,
        )

        # =====================================================
        # FAST LOCALIZATION
        # =====================================================

        localized = (
            self._localize_common_response(
                context.response,
                response_language,
            )
        )

        if localized is not None:

            print(
                "Using local response template."
            )

            context.response = localized

        else:

            # =================================================
            # LLM FALLBACK
            # =================================================

            context.response = (
                self._localize_with_llm(
                    context.response,
                    response_language,
                )
            )

        # =====================================================
        # MEMORY
        # =====================================================

        self.brain.chat_memory.add(
            "Assistant",
            context.response,
        )

        self.brain.conversation_manager.remember_response(
            context.response
        )

        # =====================================================
        # STOP
        # =====================================================

        context.stop = True

    # =========================================================
    # COMMON RESPONSE LOCALIZATION
    # =========================================================

    def _localize_common_response(
        self,
        response,
        language,
    ):
        if not response:
            return response

        if language == "English":
            return response

        text = response.strip()

        # =====================================================
        # OPEN
        # =====================================================

        match = re.fullmatch(
            r"Opened (.+)\.",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            target = match.group(1)

            if language == "Urdu":

                return (
                    f"{target} کھول دیا گیا ہے۔"
                )

            if language == "Roman Urdu":

                return (
                    f"{target} khol diya gaya hai."
                )

            if language == "Hindi":

                return (
                    f"{target} खोल दिया गया है।"
                )

            if language == "Punjabi":

                return (
                    f"{target} ਖੋਲ੍ਹ ਦਿੱਤਾ ਗਿਆ ਹੈ।"
                )

        # =====================================================
        # CLOSE
        # =====================================================

        match = re.fullmatch(
            r"Closed (.+)\.",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            target = match.group(1)

            if language == "Urdu":

                return (
                    f"{target} بند کر دیا گیا ہے۔"
                )

            if language == "Roman Urdu":

                return (
                    f"{target} band kar diya gaya hai."
                )

            if language == "Hindi":

                return (
                    f"{target} बंद कर दिया गया है।"
                )

            if language == "Punjabi":

                return (
                    f"{target} ਬੰਦ ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ।"
                )

        # =====================================================
        # CLICK
        # =====================================================

        match = re.fullmatch(
            r"Clicked (.+)\.",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            target = match.group(1)

            if language == "Urdu":

                return (
                    f"{target} پر کلک کر دیا گیا ہے۔"
                )

            if language == "Roman Urdu":

                return (
                    f"{target} par click kar diya gaya hai."
                )

            if language == "Hindi":

                return (
                    f"{target} पर क्लिक कर दिया गया है।"
                )

            if language == "Punjabi":

                return (
                    f"{target} 'ਤੇ ਕਲਿੱਕ ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ।"
                )

        # =====================================================
        # SEARCH
        # =====================================================

        match = re.fullmatch(
            r"Searched for '(.+)'\.",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            query = match.group(1)

            if language == "Urdu":

                return (
                    f"'{query}' کے لیے تلاش مکمل ہو گئی ہے۔"
                )

            if language == "Roman Urdu":

                return (
                    f"'{query}' ke liye search mukammal ho gayi hai."
                )

            if language == "Hindi":

                return (
                    f"'{query}' के लिए खोज पूरी हो गई है।"
                )

            if language == "Punjabi":

                return (
                    f"'{query}' ਲਈ ਖੋਜ ਪੂਰੀ ਹੋ ਗਈ ਹੈ।"
                )

        # =====================================================
        # TYPE
        # =====================================================

        if (
            text == "Text entered successfully."
        ):

            if language == "Urdu":

                return (
                    "متن کامیابی سے درج کر دیا گیا ہے۔"
                )

            if language == "Roman Urdu":

                return (
                    "Text kamyabi se enter kar diya gaya hai."
                )

            if language == "Hindi":

                return (
                    "टेक्स्ट सफलतापूर्वक दर्ज कर दिया गया है।"
                )

            if language == "Punjabi":

                return (
                    "ਟੈਕਸਟ ਸਫਲਤਾਪੂਰਵਕ ਦਰਜ ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ।"
                )

        # =====================================================
        # KEY PRESS
        # =====================================================

        match = re.fullmatch(
            r"Pressed (.+)\.",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            key = match.group(1)

            if language == "Urdu":

                return (
                    f"{key} کی دبانے کی کمانڈ مکمل ہو گئی ہے۔"
                )

            if language == "Roman Urdu":

                return (
                    f"{key} press kar diya gaya hai."
                )

            if language == "Hindi":

                return (
                    f"{key} दबा दिया गया है।"
                )

            if language == "Punjabi":

                return (
                    f"{key} ਦਬਾ ਦਿੱਤਾ ਗਿਆ ਹੈ।"
                )

        # =====================================================
        # WINDOW ACTIONS
        # =====================================================

        window_patterns = (
            (
                r"Minimized (.+)\.",
                {
                    "Urdu": "{} کو minimize کر دیا گیا ہے۔",
                    "Roman Urdu": "{} minimize kar diya gaya hai.",
                    "Hindi": "{} को minimize कर दिया गया है।",
                    "Punjabi": "{} ਨੂੰ minimize ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ।",
                },
            ),
            (
                r"Maximized (.+)\.",
                {
                    "Urdu": "{} کو maximize کر دیا گیا ہے۔",
                    "Roman Urdu": "{} maximize kar diya gaya hai.",
                    "Hindi": "{} को maximize कर दिया गया है।",
                    "Punjabi": "{} ਨੂੰ maximize ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ۔",
                },
            ),
            (
                r"Restored (.+)\.",
                {
                    "Urdu": "{} کو restore کر دیا گیا ہے۔",
                    "Roman Urdu": "{} restore kar diya gaya hai.",
                    "Hindi": "{} को restore कर दिया गया है।",
                    "Punjabi": "{} ਨੂੰ restore ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ۔",
                },
            ),
        )

        for pattern, translations in window_patterns:

            match = re.fullmatch(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if not match:
                continue

            target = match.group(1)

            translation = translations.get(
                language
            )

            if translation:
                return translation.format(
                    target
                )

        # =====================================================
        # GOAL
        # =====================================================

        match = re.fullmatch(
            r"Completed (.+)\. Progress is now ([0-9.]+)%\.",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            task = match.group(1)
            progress = match.group(2)

            if language == "Urdu":

                return (
                    f"{task} مکمل کر دیا گیا ہے۔ "
                    f"پیش رفت اب {progress} فیصد ہے۔"
                )

            if language == "Roman Urdu":

                return (
                    f"{task} complete kar diya gaya hai. "
                    f"Progress ab {progress} percent hai."
                )

            if language == "Hindi":

                return (
                    f"{task} पूरा कर दिया गया है। "
                    f"प्रगति अब {progress} प्रतिशत है।"
                )

            if language == "Punjabi":

                return (
                    f"{task} ਪੂਰਾ ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ। "
                    f"ਤਰੱਕੀ ਹੁਣ {progress} ਫੀਸਦੀ ਹੈ।"
                )

        # =====================================================
        # NOT A COMMON TEMPLATE
        # =====================================================

        return None

    # =========================================================
    # LLM LOCALIZATION
    # =========================================================

    def _localize_with_llm(
        self,
        response,
        language,
    ):
        if not response:
            return response

        if language == "English":
            return response

        cache_key = (
            language,
            response,
        )

        if cache_key in self._translation_cache:

            print(
                "Using cached localized response."
            )

            return self._translation_cache[
                cache_key
            ]

        prompt = self._build_localization_prompt(
            response,
            language,
        )

        print("=" * 50)
        print("LOCALIZING RESPONSE WITH LLM")
        print("Target language:", language)
        print("=" * 50)

        try:

            localized = self.brain.llm.ask(
                prompt=prompt,
                history=[],
                name="JARVIS",
            )

            if not localized:
                return response

            localized = localized.strip()

            self._translation_cache[
                cache_key
            ] = localized

            return localized

        except Exception as error:

            print(
                "Response localization failed:",
                error,
            )

            return response

    # =========================================================
    # LOCALIZATION PROMPT
    # =========================================================

    @staticmethod
    def _build_localization_prompt(
        response,
        language,
    ):

        if language == "Roman Urdu":

            return f"""
Translate the following JARVIS response into natural
Roman Urdu.

Rules:
- Use Latin letters only.
- Do not use Urdu/Arabic script.
- Preserve names, numbers, paths, URLs, application names,
  and technical terms.
- Return only the translation.

JARVIS response:
{response}
"""

        if language == "Urdu":

            return f"""
Translate the following JARVIS response into natural
Pakistani Urdu.

Rules:
- Use Urdu script.
- Preserve names, numbers, paths, URLs, application names,
  and technical terms.
- Return only the translation.

JARVIS response:
{response}
"""

        if language == "Hindi":

            return f"""
Translate the following JARVIS response into natural Hindi.

Rules:
- Use Devanagari script.
- Preserve names, numbers, paths, URLs, application names,
  and technical terms.
- Return only the translation.

JARVIS response:
{response}
"""

        if language == "Punjabi":

            return f"""
Translate the following JARVIS response into natural Punjabi.

Rules:
- Use Punjabi/Gurmukhi script.
- Preserve names, numbers, paths, URLs, application names,
  and technical terms.
- Return only the translation.

JARVIS response:
{response}
"""

        return f"""
Translate the following JARVIS response into {language}.

Return only the translation.

JARVIS response:
{response}
"""