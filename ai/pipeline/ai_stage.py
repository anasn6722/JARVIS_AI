class AIStage:

    def __init__(self, brain):
        self.brain = brain

    # =========================================================
    # RUN
    # =========================================================

    def run(self, context):

        print("=" * 50)
        print("AI STAGE ENTERED")
        print("=" * 50)

        if not context.decisions:
            print("No decisions")
            return

        ai_commands = []

        # =====================================================
        # FIND REAL AI COMMANDS ONLY
        # =====================================================

        for index, item in enumerate(context.decisions):

            decision = item.get("decision")
            command = item.get("command")

            if decision is None:
                continue

            if command is None:
                continue

            intent = getattr(
                decision,
                "intent",
                "",
            )

            route = getattr(
                decision,
                "route",
                None,
            )

            # -------------------------------------------------
            # NEVER SEND CONTROL COMMANDS TO GEMINI
            # -------------------------------------------------

            if intent in (
                "voice_language",
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
            ):
                print(
                    f"AI BYPASS: intent='{intent}' "
                    f"will not be sent to Gemini."
                )
                continue

            if route != "AI":
                continue

            ai_commands.append(
                (
                    index,
                    command,
                    decision,
                )
            )

        # =====================================================
        # NO AI COMMANDS
        # =====================================================

        if not ai_commands:

            print(
                "No AI-routed commands."
            )

            return

        # =====================================================
        # PROCESS REAL AI COMMANDS
        # =====================================================

        history = (
            self.brain.chat_memory.recent()
        )

        for (
            decision_index,
            command,
            decision,
        ) in ai_commands:

            command_index = (
                self._find_command_index(
                    context,
                    command,
                    decision_index,
                )
            )

            print("=" * 50)
            print(
                "AI COMMAND:",
                command.original,
            )
            print(
                "COMMAND INDEX:",
                command_index,
            )
            print(
                "DECISION:",
                decision,
            )
            print("=" * 50)

            # -------------------------------------------------
            # KNOWLEDGE SEARCH
            # -------------------------------------------------

            print("=" * 50)
            print("KNOWLEDGE SEARCH")
            print("QUERY:", command.original)
            print("=" * 50)

            knowledge = (
                self.brain.knowledge_manager.search(
                    command.original
                )
            )

            if knowledge.success:

                print("=" * 50)
                print("KNOWLEDGE FOUND")
                print(
                    "SOURCE:",
                    knowledge.source,
                )
                print(
                    "CONFIDENCE:",
                    knowledge.confidence,
                )
                print(
                    "CONTENT:",
                    knowledge.content,
                )
                print("=" * 50)

                prompt = f"""
User Question:
{command.original}

External Knowledge:
{knowledge.content}

Instructions:
Use the external knowledge above as the primary factual source.
Answer the user's question naturally and clearly.
Do not mention the source unless necessary.
Do not invent facts that are not supported by the knowledge.
"""

            else:

                print("=" * 50)
                print("NO KNOWLEDGE FOUND")
                print(
                    "ERROR:",
                    knowledge.error,
                )
                print("=" * 50)

                prompt = command.original

            # -------------------------------------------------
            # RESPONSE LANGUAGE
            # -------------------------------------------------

            response_language = (
                self._response_language()
            )

            prompt = f"""
Respond in {response_language}.

User request:
{prompt}
"""

            # -------------------------------------------------
            # LLM
            # -------------------------------------------------

            print("=" * 50)
            print("CALLING LLM")
            print(
                "REASON:",
                "Genuine AI/chat request",
            )
            print(
                "LANGUAGE:",
                response_language,
            )
            print("=" * 50)

            response = self.brain.llm.ask(
                prompt=prompt,
                history=history,
                name="User",
            )

            if not response:
                response = (
                    "I couldn't generate a response."
                )

            response = str(
                response
            ).strip()

            print("=" * 50)
            print("LLM RESPONSE")
            print(response)
            print("=" * 50)

            # =================================================
            # STORE RESULT
            # =================================================

            context.set_command_result(
                command_index,
                response,
            )

            print(
                "AI COMMAND RESULT:",
                command_index,
                "->",
                response,
            )

        # =====================================================
        # RESPONSESTAGE HANDLES FINAL RESPONSE
        # =====================================================

        context.response = None

    # =========================================================
    # COMMAND INDEX
    # =========================================================

    @staticmethod
    def _find_command_index(
        context,
        command,
        fallback,
    ):

        for index, item in enumerate(
            context.commands
        ):

            item_command = item.get(
                "command"
            )

            if item_command is command:

                return item.get(
                    "command_index",
                    index,
                )

            if (
                item_command is not None
                and getattr(
                    item_command,
                    "original",
                    None,
                )
                == getattr(
                    command,
                    "original",
                    None,
                )
            ):

                return item.get(
                    "command_index",
                    index,
                )

        return fallback

    # =========================================================
    # RESPONSE LANGUAGE
    # =========================================================

    @staticmethod
    def _response_language():

        try:

            from voice.language_manager import (
                language_manager,
            )

            return (
                language_manager.get_response_language()
            )

        except Exception:

            return "English"