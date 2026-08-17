from core.ui_events import ui_events


class ExecutionStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        if context.decision is None:
            return

        # =========================================================
        # AI ROUTE
        # =========================================================

        if context.decision.route == "AI":
            return

        # =========================================================
        # JARVIS UI ROUTE
        # =========================================================

        if context.decision.route == "UI":

            page_index = getattr(
                context.decision,
                "page_index",
                None,
            )

            if page_index is None:
                context.response = (
                    "I couldn't determine "
                    "which interface page to open."
                )

                return context.response

            try:
                page_index = int(
                    page_index
                )

            except (
                TypeError,
                ValueError,
            ):
                context.response = (
                    "Invalid JARVIS page navigation request."
                )

                return context.response

            # -------------------------------------------------
            # VALID JARVIS PAGES
            # -------------------------------------------------

            if page_index not in {
                0,
                1,
                2,
                3,
                4,
            }:
                context.response = (
                    "That JARVIS interface page "
                    "does not exist."
                )

                return context.response

            # -------------------------------------------------
            # SEND REQUEST TO QT GUI THREAD
            # -------------------------------------------------

            ui_events.navigate_requested.emit(
                page_index
            )

            page_names = {
                0: "Dashboard",
                1: "Chat Console",
                2: "Voice Interface",
                3: "Memory Core",
                4: "System Settings",
            }

            page_name = page_names.get(
                page_index,
                "JARVIS interface",
            )

            context.response = (
                f"Opening {page_name}."
            )

            return context.response

        # =========================================================
        # BUILTIN ROUTE
        # =========================================================

        if context.decision.route == "BUILTIN":

            command = None

            if context.commands:

                last_item = context.commands[-1]

                if isinstance(
                    last_item,
                    dict,
                ):
                    command = last_item.get(
                        "command"
                    )

            if command is None:
                context.response = None
                return None

            response = self.brain.execute_builtin(
                context.decision.intent,
                command.original,
            )

            context.response = response

            return response

        # =========================================================
        # NORMAL PLANNER / DESKTOP EXECUTION
        # =========================================================

        return self.brain.execution_manager.execute(
            context
        )