from ai.nlu.language_command_adapter import (
    language_command_adapter,
)


class CommandStage:

    def __init__(self, brain):
        self.brain = brain

    # ============================================================
    # AUTHORITATIVE LOCAL ACTIONS
    # ============================================================

    LOCAL_ACTIONS = {
        "open",
        "close",
        "close_last",
        "list_windows",
        "active_window",
        "find_window",
        "focus_window",
        "close_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",
        "mouse_position",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll",
        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",
        "ui_find",
        "ui_click",
        "ui_find_descriptor",
        "ui_click_descriptor",
        "ui_type_descriptor",
        "ui_focus",
        "ui_click_at",
        "ui_describe",
        "ui_type",
        "search_ui",
        "open_search_result",
        "path_exists",
        "list_directory",
        "file_info",
        "create_folder",
        "create_file",
        "read_file",
        "copy",
        "move",
        "rename",
        "search_files",
        "open_path",
        "open_in_explorer",
        "search",
        "youtube_search",
        "time",
        "identity",
    }

    @classmethod
    def _authoritative_local_intent(cls, canonical_text):
        """
        The language adapter is authoritative for registered
        local actions.

        Examples:
            'mouse_position'          -> mouse_position
            'keyboard_press enter'   -> keyboard_press
            'ui_click file'          -> ui_click
        """

        if not isinstance(canonical_text, str):
            return None

        text = canonical_text.strip().lower()

        if not text:
            return None

        # Exact canonical action.
        if text in cls.LOCAL_ACTIONS:
            return text

        # Canonical action followed by arguments.
        first_token = text.split(maxsplit=1)[0]

        if first_token in cls.LOCAL_ACTIONS:
            return first_token

        return None
    # ============================================================
    # COMMAND PREPROCESSING
    # ============================================================

    @staticmethod
    def _prepare_command(text):
        """
        Prepare a command for the existing English parser.

        Returns:
            original_text
            canonical_text
            requested_language
            rejected_by_language
        """

        original_text = (
            text.strip()
            if isinstance(text, str)
            else ""
        )

        if not original_text:
            return (
                "",
                "",
                None,
                True,
            )

        # --------------------------------------------------------
        # LANGUAGE SWITCH
        #
        # IMPORTANT:
        # Do NOT change the active language here.
        # First classify the command as voice_language.
        # Actual language change happens afterwards.
        # --------------------------------------------------------

        requested_language = (
            language_command_adapter
            .detect_language_switch(
                original_text
            )
        )

        if requested_language:

            canonical_text = (
                f"set language to "
                f"{requested_language.lower()}"
            )

            print(
                "LANGUAGE SWITCH REQUEST:",
                original_text,
                "->",
                requested_language,
            )

            return (
                original_text,
                canonical_text,
                requested_language,
                False,
            )

        # --------------------------------------------------------
        # NORMAL COMMAND
        # --------------------------------------------------------

        canonical_text = (
            language_command_adapter
            .canonicalize(
                original_text
            )
        )

        # --------------------------------------------------------
        # STRICT LANGUAGE REJECTION
        # --------------------------------------------------------

        if not canonical_text:

            selected_language = (
                language_command_adapter
                .active_language()
            )

            print(
                "=================================================="
            )

            print(
                "LANGUAGE REJECTED"
            )

            print(
                "Original:",
                original_text,
            )

            print(
                "Expected language:",
                selected_language,
            )

            print(
                "Command blocked before intent classification."
            )

            print(
                "=================================================="
            )

            return (
                original_text,
                "",
                None,
                True,
            )

        # --------------------------------------------------------
        # NORMALIZATION DEBUG
        # --------------------------------------------------------

        if (
            canonical_text
            != original_text.lower()
        ):

            print(
                "LANGUAGE NORMALIZATION:",
                original_text,
                "->",
                canonical_text,
            )

        return (
            original_text,
            canonical_text,
            None,
            False,
        )

    # ============================================================
    # LANGUAGE REJECTION RESPONSE
    # ============================================================

    @staticmethod
    def _language_rejection_response():

        language = (
            language_command_adapter
            .active_language()
        )

        responses = {

            "English": (
                "Please speak in English."
            ),

            "Urdu": (
                "براہ کرم اردو میں بات کریں۔"
            ),

            "Roman Urdu": (
                "Barah-e-karam Roman Urdu mein baat karein."
            ),

            "Hindi": (
                "कृपया हिंदी में बात करें।"
            ),

            "Punjabi": (
                "ਕਿਰਪਾ ਕਰਕੇ ਪੰਜਾਬੀ ਵਿੱਚ ਗੱਲ ਕਰੋ।"
            ),
        }

        return responses.get(
            language,
            "Please use the selected language.",
        )

    # ============================================================
    # APPLY LANGUAGE AFTER CLASSIFICATION
    # ============================================================

    @staticmethod
    def _apply_requested_language(
        requested_language,
        command_data,
    ):

        if not requested_language:
            return

        intent = getattr(
            command_data,
            "intent",
            "",
        )

        if intent != "voice_language":
            return

        changed = (
            language_command_adapter
            .apply_language_switch(
                f"set language to "
                f"{requested_language.lower()}"
            )
        )

        if changed:

            print(
                "LANGUAGE CHANGED:",
                requested_language,
            )

    # ============================================================
    # RUN COMMAND STAGE
    # ============================================================

    def run(self, context):

        commands = (
            self.brain.command_splitter.split(
                context.input
            )
        )

        context.commands = []

        # --------------------------------------------------------
        # Track language rejections.
        # --------------------------------------------------------

        context.language_rejections = []

        if not commands:

            context.response = (
                "I didn't hear a command."
            )

            return

        # ========================================================
        # SINGLE COMMAND
        # ========================================================

        if len(commands) == 1:

            item = (
                self._process_single_command(
                    commands[0],
                    context,
                    command_index=0,
                )
            )

            # ----------------------------------------------------
            # Rejected language command.
            # ----------------------------------------------------

            if item is None:

                context.response = (
                    self._language_rejection_response()
                )

                print(
                    "COMMAND STAGE:",
                    "command blocked due to language mismatch.",
                )

                return

            context.commands.append(
                item
            )

        # ========================================================
        # MULTIPLE COMMANDS
        # ========================================================

        else:

            self._process_multiple_commands(
                commands,
                context,
            )

            # ----------------------------------------------------
            # If every command was rejected.
            # ----------------------------------------------------

            if (
                not context.commands
                and context.language_rejections
            ):

                context.response = (
                    self._language_rejection_response()
                )

                print(
                    "COMMAND STAGE:",
                    "all commands blocked due to language mismatch.",
                )

                return

            self._print_commands( context )

    # ============================================================
    # SINGLE COMMAND
    # ============================================================

    def _process_single_command(
        self,
        text,
        context,
        command_index,
    ):

        (
            original_text,
            canonical_text,
            requested_language,
            rejected_by_language,
        ) = self._prepare_command(
            text
        )

        # --------------------------------------------------------
        # BLOCK BEFORE PARSER
        # --------------------------------------------------------

        if rejected_by_language:

            context.language_rejections.append(
                original_text
            )

            return None

        # --------------------------------------------------------
        # EXISTING COMMAND MANAGER
        # --------------------------------------------------------

        command_data, goal = (
            self.brain.command_manager.process(
                canonical_text
            )
        )

        # --------------------------------------------------------
        # LANGUAGE ADAPTER IS AUTHORITATIVE FOR LOCAL ACTIONS
        # --------------------------------------------------------

        authoritative_intent = (
            self._authoritative_local_intent(
                canonical_text
            )
        )

        if authoritative_intent:

            old_intent = getattr(
                command_data,
                "intent",
                "",
            )

            if old_intent != authoritative_intent:

                print(
                    "LOCAL INTENT OVERRIDE:",
                    old_intent,
                    "->",
                    authoritative_intent,
                )

            command_data.intent = (
                authoritative_intent
            )

            command_data.destination = (
                "BRAIN"
            )

            try:
                command_data.confidence = 1.0
            except Exception:
                pass

            try:
                command_data.requires_planning = True
            except Exception:
                pass

        # --------------------------------------------------------
        # APPLY LANGUAGE ONLY AFTER CLASSIFICATION
        # --------------------------------------------------------

        self._apply_requested_language(
            requested_language,
            command_data,
        )

        # --------------------------------------------------------
        # PRESERVE SPOKEN TEXT
        # --------------------------------------------------------

        try:

            command_data.original = (
                original_text.lower()
            )

        except Exception:
            pass

        # --------------------------------------------------------
        # REFERENCE RESOLUTION
        # --------------------------------------------------------

        command_data = (
            self.brain.reference_resolver.resolve(
                command_data
            )
        )

        # --------------------------------------------------------
        # AGENT ROUTING
        # --------------------------------------------------------

        agent_result = (
            self.brain.agent_router.route(
                command_data,
                brain=self.brain,
                pipeline_context=context,
            )
        )

        item = {

            "command": command_data,

            "goal": goal,

            "original_text": original_text,

            "canonical_text": canonical_text,

            "command_index": command_index,

            "agent": "unassigned",

            "agent_result": None,

            "requested_language": requested_language,

        }

        if agent_result is not None:

            item["agent_result"] = (
                agent_result
            )

            item["agent"] = getattr(
                agent_result,
                "agent",
                "unassigned",
            )

        # --------------------------------------------------------
        # METADATA
        # --------------------------------------------------------

        if agent_result is not None:

            metadata = getattr(
                agent_result,
                "metadata",
                None,
            )

            if isinstance(
                metadata,
                dict,
            ):

                metadata[
                    "command_index"
                ] = command_index

                metadata[
                    "original_text"
                ] = original_text

                metadata[
                    "canonical_text"
                ] = canonical_text

                metadata[
                    "requested_language"
                ] = requested_language

        return item

    # ============================================================
    # MULTIPLE COMMANDS
    # ============================================================

    def _process_multiple_commands(
        self,
        commands,
        context,
    ):

        parsed = []

        # ========================================================
        # PARSE COMMANDS
        # ========================================================

        for index, text in enumerate(
            commands
        ):

            (
                original_text,
                canonical_text,
                requested_language,
                rejected_by_language,
            ) = self._prepare_command(
                text
            )

            # ----------------------------------------------------
            # Reject only this command.
            # ----------------------------------------------------

            if rejected_by_language:

                context.language_rejections.append(
                    original_text
                )

                continue

            # ----------------------------------------------------
            # EXISTING PARSER
            # ----------------------------------------------------

            command_data, goal = (
                self.brain.command_manager.process(
                    canonical_text
                )
            )
            
            # ----------------------------------------------------
            # LANGUAGE ADAPTER IS AUTHORITATIVE FOR LOCAL ACTIONS
            # ----------------------------------------------------

            authoritative_intent = (
                self._authoritative_local_intent(
                    canonical_text
                )
            )

            if authoritative_intent:

                old_intent = getattr(
                    command_data,
                    "intent",
                    "",
                )

                if old_intent != authoritative_intent:

                    print(
                        "LOCAL INTENT OVERRIDE:",
                        old_intent,
                        "->",
                        authoritative_intent,
                    )

                command_data.intent = (
                    authoritative_intent
                )

                command_data.destination = (
                    "BRAIN"
                )

                try:
                    command_data.confidence = 1.0
                except Exception:
                    pass

                try:
                    command_data.requires_planning = True
                except Exception:
                    pass

            self._apply_requested_language(
                requested_language,
                command_data,
            )

            # ----------------------------------------------------
            # Preserve original speech.
            # ----------------------------------------------------

            try:

                command_data.original = (
                    original_text.lower()
                )

            except Exception:
                pass

            # ----------------------------------------------------
            # Reference resolution.
            # ----------------------------------------------------

            command_data = (
                self.brain.reference_resolver.resolve(
                    command_data
                )
            )

            parsed.append(
                {

                    "command": command_data,

                    "goal": goal,

                    "original_text": original_text,

                    "canonical_text": canonical_text,

                    "requested_language": (
                        requested_language
                    ),

                    "index": index,

                }
            )

        # ========================================================
        # NOTHING VALID
        # ========================================================

        if not parsed:
            return

        # ========================================================
        # PARALLEL EXECUTION
        # ========================================================

        if self._can_parallelize(
            parsed
        ):

            print(
                "MULTI-AGENT MODE: "
                "parallel execution enabled."
            )

            commands_only = [
                item["command"]
                for item in parsed
            ]

            results = (
                self.brain.agent_router.route_many(
                    commands_only,
                    brain=self.brain,
                    pipeline_context=context,
                )
            )

            result_by_index = {}

            for result in results:

                result_context = (
                    result.get(
                        "context"
                    )
                )

                metadata = getattr(
                    result_context,
                    "metadata",
                    {},
                )

                index = metadata.get(
                    "command_index",
                    0,
                )

                result_by_index[
                    index
                ] = result

            for item in parsed:

                index = item["index"]

                result = (
                    result_by_index.get(
                        index
                    )
                )

                agent_result = (
                    result.get(
                        "result"
                    )
                    if result
                    else None
                )

                agent_name = (
                    getattr(
                        agent_result,
                        "agent",
                        "unassigned",
                    )
                    if agent_result
                    else "unassigned"
                )

                context.commands.append(
                    {
                        "command": item["command"],

                        "goal": item["goal"],

                        "original_text": item[
                            "original_text"
                        ],

                        "canonical_text": item[
                            "canonical_text"
                        ],

                        "requested_language": item[
                            "requested_language"
                        ],

                        "agent": agent_name,

                        "agent_result": agent_result,

                        "command_index": index,
                    }
                )

        # ========================================================
        # SEQUENTIAL EXECUTION
        # ========================================================

        else:

            print(
                "MULTI-AGENT MODE: "
                "sequential dependency mode."
            )

            for item in parsed:

                command_data = item[
                    "command"
                ]

                agent_result = (
                    self.brain.agent_router.route(
                        command_data,
                        brain=self.brain,
                        pipeline_context=context,
                    )
                )

                agent_name = (
                    getattr(
                        agent_result,
                        "agent",
                        "unassigned",
                    )
                    if agent_result
                    else "unassigned"
                )

                context.commands.append(
                    {
                        "command": command_data,

                        "goal": item["goal"],

                        "original_text": item[
                            "original_text"
                        ],

                        "canonical_text": item[
                            "canonical_text"
                        ],

                        "requested_language": item[
                            "requested_language"
                        ],

                        "agent": agent_name,

                        "agent_result": agent_result,

                        "command_index": item[
                            "index"
                        ],
                    }
                )

    # ============================================================
    # PARALLELIZATION RULES
    # ============================================================

    @staticmethod
    def _can_parallelize(
        parsed_commands,
    ):

        if len(
            parsed_commands
        ) <= 1:

            return False

        dependency_phrases = (

            "it",
            "that",
            "this",
            "those",
            "the result",
            "last result",
            "last ui",
            "previous",
            "after that",
            "then",
            "next",
            "same",
            "again",

        )

        for item in parsed_commands:

            text = (
                item[
                    "canonical_text"
                ]
                .lower()
                .strip()
            )

            if any(
                phrase in text
                for phrase in dependency_phrases
            ):

                return False

            command = item[
                "command"
            ]

            goal = getattr(
                command,
                "goal",
                None,
            )

            if isinstance(
                goal,
                dict,
            ):

                if goal.get(
                    "parent_goal"
                ):

                    return False

        return True

    # ============================================================
    # DEBUG
    # ============================================================

    @staticmethod
    def _print_commands(
        context
    ):

        print(
            "=" * 50
        )

        print(
            "COMMAND STAGE"
        )

        for index, item in enumerate(
            context.commands
        ):

            print(
                f"Command {index + 1}:",
                item["command"],
            )

            print(
                "Original:",
                item.get(
                    "original_text",
                    "",
                ),
            )

            print(
                "Canonical:",
                item.get(
                    "canonical_text",
                    "",
                ),
            )

            print(
                "Agent:",
                item.get(
                    "agent",
                    "unassigned",
                ),
            )

        # --------------------------------------------------------
        # Rejected commands
        # --------------------------------------------------------

        rejected = getattr(
            context,
            "language_rejections",
            [],
        )

        if rejected:

            print(
                "Language rejected:",
                rejected,
            )

        print(
            "=" * 50
        )
