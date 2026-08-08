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
            return "I couldn't find anything to open."

        responses = []

        for target in targets:

            target = target.lower().strip()

            # -------------------------------------------------
            # Website
            # -------------------------------------------------

            if target in WEBSITES:

                responses.append(
                    self._open_website(target)
                )

                continue

            # -------------------------------------------------
            # Registered application
            # -------------------------------------------------

            if target in APPS:

                responses.append(
                    self._open_application(target)
                )

                continue

            # -------------------------------------------------
            # Automatic application detection
            # -------------------------------------------------

            response = self._open_unknown_application(
                target
            )

            responses.append(response)

        return "\n".join(responses)

    # =========================================================
    # OPEN WEBSITE
    # =========================================================

    def _open_website(self, website):

        self.brain.web.open_url(
            WEBSITES[website]
        )

        self.brain.conversation_memory.remember_website(
            website
        )

        self.brain.context.update(
            website=website,
        )

        return f"Opened {website.title()}."

    # =========================================================
    # OPEN REGISTERED APPLICATION
    # =========================================================

    def _open_application(self, app):

        success = self.brain.system.open_program(
            APPS[app]["open"]
        )

        if not success:

            return (
                f"Couldn't open {app.title()}."
            )

        self.brain.conversation_memory.remember_app(
            app
        )

        self.brain.session.last_app = app

        self.brain.context.update(
            app=app,
        )

        return f"Opened {app.title()}."

    # =========================================================
    # OPEN UNKNOWN APPLICATION
    # =========================================================

    def _open_unknown_application(self, target):

        executable = self.brain.application_resolver.resolve(
            target
        )

        if not executable:

            return (
                f"I couldn't find an installed application "
                f"called {target}."
            )

        success = self.brain.system.open_program(
            executable
        )

        if not success:

            return (
                f"I found {target}, but couldn't open it."
            )

        self.brain.conversation_memory.remember_app(
            target
        )

        self.brain.session.last_app = target

        self.brain.context.update(
            app=target,
        )

        return f"Opened {target.title()}."

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self, app):

        app = app.lower().strip()

        program = APPS.get(app)

        if not program:

            return (
                f"I don't know how to close {app}."
            )

        process = program["process"]

        success = self.brain.system.close_program(
            process
        )

        if not success:

            return (
                f"Couldn't close {app.title()}."
            )

        return f"Closed {app.title()}."

    
    
    # =========================================================
    # CLOSE LAST
    # =========================================================

    def close_last(self, argument=None):

        reference = None

        # -----------------------------------------------------
        # Get latest memory reference
        # -----------------------------------------------------

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
                "There is no previously opened "
                "application or website."
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

            # -------------------------------------------------
            # No WebManager exists.
            # Websites run inside the browser, so close
            # the browser for now.
            # -------------------------------------------------

            browser = "chrome"

            result = self.close(browser)

            if result.startswith("Closed Chrome"):
                return (
                    f"Closed {reference_value.title()} "
                    f"by closing Chrome."
                )

            return result

        # =====================================================
        # UNKNOWN
        # =====================================================

        return (
            "I don't know how to close "
            "the last reference."
        )
