from automation.config.apps import APPS
from automation.config.websites import WEBSITES


class AppHandler:
    """Handles application and website opening/closing."""

    def __init__(self, brain):
        self.brain = brain

    # =========================================================
    # OPEN
    # =========================================================

    def open(self, command):
        """Open one or more applications or websites."""

        if isinstance(command, str):
            targets = [command.lower().strip()]

        else:
            targets = list(
                command.entities.get("apps", [])
            )

            targets.extend(
                command.entities.get("websites", [])
            )

        if not targets:
            return (
                False,
                "I couldn't find anything to open.",
            )

        responses = []
        overall_success = True

        for target in targets:

            target = target.lower().strip()

            # -------------------------------------------------
            # Website
            # -------------------------------------------------

            if target in WEBSITES:

                success, message = self._open_website(
                    target
                )

            # -------------------------------------------------
            # Registered application
            # -------------------------------------------------

            elif target in APPS:

                success, message = self._open_application(
                    target
                )

            # -------------------------------------------------
            # Automatic application detection
            # -------------------------------------------------

            else:

                success, message = (
                    self._open_unknown_application(
                        target
                    )
                )

            responses.append(message)

            if not success:
                overall_success = False

        return (
            overall_success,
            "\n".join(responses),
        )

    # =========================================================
    # OPEN WEBSITE
    # =========================================================

    def _open_website(self, website):
        """Open a registered website."""

        try:
            self.brain.web.open_url(
                WEBSITES[website]
            )

            self.brain.conversation_memory.remember_website(
                website
            )

            self.brain.context.update(
                website=website,
            )

            return (
                True,
                f"Opened {website.title()}.",
            )

        except Exception as error:

            return (
                False,
                f"Couldn't open {website.title()}: {error}",
            )

    # =========================================================
    # OPEN REGISTERED APPLICATION
    # =========================================================

    def _open_application(self, app):
        """Open an application registered in APPS."""

        try:
            success = self.brain.system.open_program(
                APPS[app]["open"]
            )

        except Exception as error:

            return (
                False,
                f"Couldn't open {app.title()}: {error}",
            )

        if not success:

            return (
                False,
                f"Couldn't open {app.title()}.",
            )

        self.brain.conversation_memory.remember_app(
            app
        )

        self.brain.session.last_app = app

        self.brain.context.update(
            app=app,
        )

        return (
            True,
            f"Opened {app.title()}.",
        )

    # =========================================================
    # OPEN UNKNOWN APPLICATION
    # =========================================================

    def _open_unknown_application(self, target):
        """Resolve and open an application not in APPS."""

        try:
            executable = (
                self.brain.application_resolver.resolve(
                    target
                )
            )

        except Exception as error:

            return (
                False,
                f"Couldn't resolve {target}: {error}",
            )

        if not executable:

            return (
                False,
                f"I couldn't find an installed application "
                f"called {target}.",
            )

        try:
            success = self.brain.system.open_program(
                executable
            )

        except Exception as error:

            return (
                False,
                f"I found {target}, but couldn't open it: "
                f"{error}",
            )

        if not success:

            return (
                False,
                f"I found {target}, but couldn't open it.",
            )

        self.brain.conversation_memory.remember_app(
            target
        )

        self.brain.session.last_app = target

        self.brain.context.update(
            app=target,
        )

        return (
            True,
            f"Opened {target.title()}.",
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self, app):
        """Close a registered application."""

        app = app.lower().strip()

        program = APPS.get(app)

        if not program:

            return (
                False,
                f"I don't know how to close {app}.",
            )

        try:
            success = self.brain.system.close_program(
                program["process"]
            )

        except Exception as error:

            return (
                False,
                f"Couldn't close {app.title()}: {error}",
            )

        if not success:

            return (
                False,
                f"Couldn't close {app.title()}.",
            )

        return (
            True,
            f"Closed {app.title()}.",
        )

    # =========================================================
    # CLOSE LAST
    # =========================================================

    def close_last(self, argument=None):
        """Close the most recently referenced application or website."""

        reference = None

        if hasattr(
            self.brain.conversation_memory,
            "last_reference",
        ):
            reference = (
                self.brain.conversation_memory.last_reference()
            )

        print(
            "🧠 CLOSE LAST REFERENCE:",
            reference,
        )

        # -----------------------------------------------------
        # No reference
        # -----------------------------------------------------

        if not reference:

            return (
                False,
                "There is no previously opened "
                "application or website.",
            )

        reference_type, reference_value = reference

        # =====================================================
        # APPLICATION
        # =====================================================

        if reference_type == "app":

            return self.close(
                reference_value
            )

        # =====================================================
        # WEBSITE
        # =====================================================

        if reference_type == "website":

            # Websites run inside a browser, so close Chrome
            # for now.

            browser = "chrome"

            success, message = self.close(
                browser
            )

            if success:

                return (
                    True,
                    f"Closed {reference_value.title()} "
                    f"by closing Chrome.",
                )

            return (
                False,
                message,
            )

        # =====================================================
        # UNKNOWN
        # =====================================================

        return (
            False,
            "I don't know how to close "
            "the last reference.",
        )