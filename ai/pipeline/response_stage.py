import re

from voice.language_manager import language_manager


class ResponseStage:

    def __init__(self, brain):
        self.brain = brain

        # LLM translation cache is retained only for
        # genuine AI-generated responses.
        self._translation_cache = {}

    # =========================================================
    # RUN
    # =========================================================

    def run(self, context):

        # =====================================================
        # CHECK WHETHER THIS IS A REAL AI RESPONSE
        # =====================================================

        has_ai_command = self._has_real_ai_command(
            context
        )

        # =====================================================
        # LANGUAGE SWITCH
        # =====================================================

        language_response = (
            self._build_language_switch_response(
                context
            )
        )

        if language_response:

            context.response = language_response

            print(
                "Using local language-switch response."
            )

        else:

            # =================================================
            # ORDERED COMMAND RESULTS
            # =================================================

            ordered_results = (
                context.ordered_command_results()
            )

            if ordered_results:

                context.response = (
                    self._humanize_results(
                        context,
                        ordered_results,
                    )
                )

            # =================================================
            # DEFAULT RESPONSE
            # =================================================

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
        # LOCAL RESPONSE
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

        # =====================================================
        # AI RESPONSES ONLY
        # =====================================================

        elif has_ai_command:

            print(
                "AI response requires localization."
            )

            context.response = (
                self._localize_with_llm(
                    context.response,
                    response_language,
                )
            )

        else:

            # -------------------------------------------------
            # IMPORTANT:
            # No Gemini for normal desktop commands.
            # -------------------------------------------------

            print(
                "Using local response without LLM."
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
    # REAL AI COMMAND CHECK
    # =========================================================

    @staticmethod
    def _has_real_ai_command(context):

        for item in getattr(
            context,
            "decisions",
            [],
        ):

            decision = item.get(
                "decision"
            )

            if decision is None:
                continue

            intent = getattr(
                decision,
                "intent",
                "",
            )

            route = getattr(
                decision,
                "route",
                "",
            )

            if (
                route == "AI"
                and intent
                not in (
                    "voice_language",
                )
            ):

                return True

        return False

    # =========================================================
    # LANGUAGE SWITCH RESPONSE
    # =========================================================

    @staticmethod
    def _build_language_switch_response(
        context
    ):

        for item in getattr(
            context,
            "commands",
            [],
        ):

            command = item.get(
                "command"
            )

            if command is None:
                continue

            if getattr(
                command,
                "intent",
                "",
            ) != "voice_language":
                continue

            language = (
                language_manager.get_primary_language()
            )

            if language == "English":

                return (
                    "Language changed to English."
                )

            if language == "Urdu":

                return (
                    "زبان اردو میں تبدیل کر دی گئی ہے۔"
                )

            if language == "Roman Urdu":

                return (
                    "Zaban Roman Urdu mein tabdeel kar di gayi hai."
                )

            if language == "Hindi":

                return (
                    "भाषा हिंदी में बदल दी गई है।"
                )

            if language == "Punjabi":

                return (
                    "ਭਾਸ਼ਾ ਪੰਜਾਬੀ ਵਿੱਚ ਬਦਲ ਦਿੱਤੀ ਗਈ ਹੈ।"
                )

        return None

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
            r"(?:Opening|Opened)\s+(.+?)(?:\.)",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            target = match.group(1)

            if language == "Urdu":

                return (
                    f"{target} کھول رہا ہوں۔"
                )

            if language == "Roman Urdu":

                return (
                    f"{target} khol raha hoon."
                )

            if language == "Hindi":

                return (
                    f"{target} खोल रहा हूँ।"
                )

            if language == "Punjabi":

                return (
                    f"{target} ਖੋਲ੍ਹ ਰਿਹਾ ਹਾਂ।"
                )

        # =====================================================
        # CLOSE
        # =====================================================

        match = re.fullmatch(
            r"(?:Closing|Closed|.+\s+has been closed)\.?",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            close_target = self._extract_closed_target(
                text
            )

            if close_target:

                if language == "Urdu":

                    return (
                        f"{close_target} بند کر دیا گیا ہے۔"
                    )

                if language == "Roman Urdu":

                    return (
                        f"{close_target} band kar diya gaya hai."
                    )

                if language == "Hindi":

                    return (
                        f"{close_target} बंद कर दिया गया है।"
                    )

                if language == "Punjabi":

                    return (
                        f"{close_target} ਬੰਦ ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ।"
                    )

        # =====================================================
        # CLICK
        # =====================================================

        match = re.fullmatch(
            r"Clicked\s+(.+)\.",
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
                    f"{target} 'ਤੇ ਕਲਿੱਕ ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ۔"
                )

        # =====================================================
        # SEARCH
        # =====================================================

        match = re.fullmatch(
            r"Searched for ['\"](.+?)['\"]\.",
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
                    f"'{query}' ਲਈ ਖੋਜ ਪੂਰੀ ਹੋ ਗਈ ਹੈ۔"
                )

        # =====================================================
        # TEXT ENTERED
        # =====================================================

        if text.lower() == (
            "text entered successfully."
        ).lower():

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
            r"Pressed\s+(.+)\.",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            key = match.group(1)

            if language == "Urdu":

                return (
                    f"{key} دبا دیا گیا ہے۔"
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
                    f"{key} ਦਬਾ ਦਿੱਤਾ ਗਿਆ ਹੈ۔"
                )

        # =====================================================
        # WINDOW ACTIONS
        # =====================================================

        window_patterns = (

            (
                r"(?:Minimized|.+\s+is now minimized)\s+(.+?)\.?",
                {
                    "Urdu": "{} کو minimize کر دیا گیا ہے۔",
                    "Roman Urdu": "{} minimize kar diya gaya hai.",
                    "Hindi": "{} को minimize कर दिया गया है।",
                    "Punjabi": "{} ਨੂੰ minimize ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ۔",
                },
            ),

            (
                r"(?:Maximized|.+\s+is now maximized)\s+(.+?)\.?",
                {
                    "Urdu": "{} کو maximize کر دیا گیا ہے۔",
                    "Roman Urdu": "{} maximize kar diya gaya hai.",
                    "Hindi": "{} को maximize कर दिया गया है۔",
                    "Punjabi": "{} ਨੂੰ maximize ਕਰ ਦਿੱਤਾ ਗਿਆ ہے۔",
                },
            ),

            (
                r"(?:Restored|.+\s+has been restored)\s*(.*?)\.?",
                {
                    "Urdu": "{} کو restore کر دیا گیا ہے۔",
                    "Roman Urdu": "{} restore kar diya gaya hai.",
                    "Hindi": "{} को restore कर दिया गया है۔",
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

            target = match.group(1).strip()

            translation = translations.get(
                language
            )

            if translation and target:

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
                    f"{task} ਪੂਰਾ ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ۔ "
                    f"ਤਰੱਕੀ ਹੁਣ {progress} ਫੀਸਦੀ ਹੈ۔"
                )

        return None

    # =========================================================
    # CLOSED TARGET
    # =========================================================

    @staticmethod
    def _extract_closed_target(
        text
    ):

        patterns = (
            r"Closing\s+(.+?)\.?$",
            r"Closed\s+(.+?)\.?$",
            r"(.+?)\s+has been closed\.?$",
        )

        for pattern in patterns:

            match = re.fullmatch(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:

                return match.group(1).strip()

        return ""

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
        print("LOCALIZING AI RESPONSE WITH LLM")
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

    # =========================================================
    # HUMANIZE COMMAND RESULTS
    # =========================================================

    def _humanize_results(
        self,
        context,
        results,
    ):

        commands = getattr(
            context,
            "commands",
            [],
        )

        responses = []

        for index, result in enumerate(results):

            command_data = None

            if index < len(commands):

                item = commands[index]

                if isinstance(item, dict):

                    command_data = item.get(
                        "command"
                    )

            intent = getattr(
                command_data,
                "intent",
                "",
            )

            original = getattr(
                command_data,
                "original",
                "",
            )

            target = self._extract_target(
                command_data
            )

            # -------------------------------------------------
            # CREATE FOLDER
            # -------------------------------------------------

            if intent == "create_folder":

                folder_name = (
                    target
                    or self._extract_name(
                        original,
                        ("folder",),
                    )
                )

                if self._is_success(result):

                    if folder_name:

                        responses.append(
                            f"Done. I created the folder "
                            f"'{folder_name}'."
                        )

                    else:

                        responses.append(
                            "Done. The folder was created successfully."
                        )

                    continue

            # -------------------------------------------------
            # CREATE FILE
            # -------------------------------------------------

            if intent == "create_file":

                file_name = (
                    target
                    or self._extract_name(
                        original,
                        ("file",),
                    )
                )

                if self._is_success(result):

                    if file_name:

                        responses.append(
                            f"Done. I created the file "
                            f"'{file_name}'."
                        )

                    else:

                        responses.append(
                            "Done. The file was created successfully."
                        )

                    continue

            # -------------------------------------------------
            # LIST DIRECTORY
            # -------------------------------------------------

            if intent == "list_directory":

                if isinstance(result, list):

                    directories = 0
                    files = 0

                    for item in result:

                        if not isinstance(
                            item,
                            dict,
                        ):
                            continue

                        if item.get("type") == "directory":

                            directories += 1

                        elif item.get("type") == "file":

                            files += 1

                    total = directories + files

                    location = (
                        target
                        or self._extract_location(
                            original
                        )
                        or "the directory"
                    )

                    if total == 0:

                        responses.append(
                            f"The {location} is empty."
                        )

                    else:

                        parts = []

                        if directories:

                            parts.append(
                                f"{directories} "
                                f"{'folder' if directories == 1 else 'folders'}"
                            )

                        if files:

                            parts.append(
                                f"{files} "
                                f"{'file' if files == 1 else 'files'}"
                            )

                        responses.append(
                            f"I found {total} items in "
                            f"{location}: "
                            f"{' and '.join(parts)}."
                        )

                    continue

            # -------------------------------------------------
            # SEARCH FILES
            # -------------------------------------------------

            if intent == "search_files":

                if isinstance(result, list):

                    count = len(result)

                    if count == 0:

                        responses.append(
                            "I couldn't find any matching files."
                        )

                    elif count == 1:

                        responses.append(
                            f"I found one matching file: "
                            f"{result[0]}"
                        )

                    else:

                        responses.append(
                            f"I found {count} matching files."
                        )

                    continue

            # -------------------------------------------------
            # KEYBOARD
            # -------------------------------------------------

            if intent == "keyboard_press":

                key = (
                    target
                    or self._extract_key(
                        original
                    )
                )

                if key:

                    responses.append(
                        f"Done. I pressed {key}."
                    )

                    continue

            if intent == "keyboard_hotkey":

                shortcut = target or ""

                if shortcut:

                    responses.append(
                        f"Done. I pressed {shortcut}."
                    )

                    continue

            # -------------------------------------------------
            # OPEN
            # -------------------------------------------------

            if intent == "open":

                if target:

                    responses.append(
                        f"Opening {target}."
                    )

                    continue

            # -------------------------------------------------
            # CLOSE
            # -------------------------------------------------

            if intent == "close":

                if target:

                    responses.append(
                        f"{target} has been closed."
                    )

                    continue

            # -------------------------------------------------
            # WINDOW ACTIONS
            # -------------------------------------------------

            if intent == "minimize_window":

                if target:

                    responses.append(
                        f"{target} is now minimized."
                    )

                    continue

            if intent == "maximize_window":

                if target:

                    responses.append(
                        f"{target} is now maximized."
                    )

                    continue

            if intent == "restore_window":

                if target:

                    responses.append(
                        f"{target} has been restored."
                    )

                    continue

            # -------------------------------------------------
            # COPY
            # -------------------------------------------------

            if intent == "copy":

                if self._is_success(result):

                    responses.append(
                        "Done. The item was copied successfully."
                    )

                    continue

            # -------------------------------------------------
            # MOVE
            # -------------------------------------------------

            if intent == "move":

                if self._is_success(result):

                    responses.append(
                        "Done. The item was moved successfully."
                    )

                    continue

            # -------------------------------------------------
            # RENAME
            # -------------------------------------------------

            if intent == "rename":

                if self._is_success(result):

                    responses.append(
                        "Done. The item was renamed successfully."
                    )

                    continue

            # -------------------------------------------------
            # FALLBACK
            # -------------------------------------------------

            responses.append(
                self._humanize_generic_result(
                    result
                )
            )

        return "\n".join(
            response
            for response in responses
            if response
        )

    # =========================================================
    # TARGET EXTRACTION
    # =========================================================

    @staticmethod
    def _extract_target(command):

        if command is None:
            return ""

        entities = getattr(
            command,
            "entities",
            {},
        )

        if not isinstance(
            entities,
            dict,
        ):
            return ""

        for key in (
            "apps",
            "websites",
            "windows",
            "searches",
            "goals",
        ):

            values = entities.get(
                key,
                [],
            )

            if values:

                if isinstance(
                    values,
                    list,
                ):

                    return str(
                        values[0]
                    )

                return str(values)

        return ""

    # =========================================================
    # NAME EXTRACTION
    # =========================================================

    @staticmethod
    def _extract_name(
        text,
        kinds,
    ):

        if not text:
            return ""

        patterns = (
            r"called\s+(.+?)(?:\s+inside\s+.+)?$",
            r"named\s+(.+?)(?:\s+inside\s+.+)?$",
        )

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:

                return match.group(1).strip(
                    " ."
                )

        return ""

    # =========================================================
    # LOCATION EXTRACTION
    # =========================================================

    @staticmethod
    def _extract_location(text):

        if not text:
            return ""

        match = re.search(
            r"\b(?:in|inside|from)\s+(.+?)(?:\s+with\s+|\s+called\s+|$)",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            return match.group(1).strip()

        return ""

    # =========================================================
    # KEY EXTRACTION
    # =========================================================

    @staticmethod
    def _extract_key(text):

        if not text:
            return ""

        match = re.search(
            r"press\s+(.+)$",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            return match.group(1).strip()

        return ""

    # =========================================================
    # SUCCESS CHECK
    # =========================================================

    @staticmethod
    def _is_success(result):

        if result is None:
            return False

        text = str(result).lower()

        failure_words = (
            "failed",
            "error",
            "exception",
            "couldn't",
            "not found",
            "unable",
        )

        return not any(
            word in text
            for word in failure_words
        )

    # =========================================================
    # GENERIC RESULT
    # =========================================================

    @staticmethod
    def _humanize_generic_result(
        result
    ):

        if isinstance(
            result,
            list,
        ):

            count = len(result)

            if count == 0:

                return (
                    "Done. I didn't find any matching items."
                )

            return (
                f"Done. I found {count} matching items."
            )

        if isinstance(
            result,
            dict,
        ):

            return (
                "Done. The requested operation "
                "completed successfully."
            )

        text = str(
            result
        ).strip()

        if not text:

            return (
                "Done. The operation completed successfully."
            )

        if text.startswith(
            "Pressed "
        ):

            return (
                "Done. "
                f"{text[8:].rstrip('.')}"
                "."
            )

        if text.startswith(
            "Created folder:"
        ):

            path = text.split(
                ":",
                1,
            )[1].strip()

            return (
                "Done. I created the folder at "
                f"{path}."
            )

        if text.startswith(
            "Created file:"
        ):

            path = text.split(
                ":",
                1,
            )[1].strip()

            return (
                "Done. I created the file at "
                f"{path}."
            )

        return text