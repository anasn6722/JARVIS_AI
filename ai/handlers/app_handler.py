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

    def close_last(self):

        app = self.brain.session.last_app

        if not app:

            return (
                "There is no previously opened "
                "application."
            )

        return self.close(app)