from automation.config.apps import APPS
from automation.config.websites import WEBSITES


class AppHandler:
    """Handles application and website opening/closing."""

    def __init__(self, brain):
        self.brain = brain

    # -------------------------
    # Open
    # -------------------------

    def open(self, command):
        if isinstance(command, str):
            targets = [
                command.lower().strip()
            ]
        else:
            targets = list(
                command.entities.get(
                    "apps",
                    [],
                )
            )

            targets.extend(
                command.entities.get(
                    "websites",
                    [],
                )
            )

        if not targets:
            return "I couldn't find anything to open."

        responses = []

        for target in targets:
            target = target.lower().strip()

            # -------------------------
            # Website
            # -------------------------

            if target in WEBSITES:
                responses.append(
                    self._open_website(target)
                )
                continue

            # -------------------------
            # Application
            # -------------------------

            if target in APPS:
                responses.append(
                    self._open_application(target)
                )
                continue

            # -------------------------
            # Unknown
            # -------------------------

            responses.append(
                f"I don't know {target}."
            )

        return "\n".join(responses)

    # -------------------------
    # Open Website
    # -------------------------

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

    # -------------------------
    # Open Application
    # -------------------------

    def _open_application(self, app):
        success = self.brain.system.open_program(
            APPS[app]["open"]
        )

        if not success:
            return f"Couldn't open {app.title()}."

        self.brain.conversation_memory.remember_app(
            app
        )

        self.brain.session.last_app = app

        self.brain.context.update(
            app=app,
        )

        return f"Opened {app.title()}."

    # -------------------------
    # Close Application
    # -------------------------

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
            return f"Couldn't close {app}."

        return f"Closed {app.title()}."

    # -------------------------
    # Close Last Application
    # -------------------------

    def close_last(self):
        app = self.brain.session.last_app

        if not app:
            return (
                "There is no previously opened "
                "application."
            )

        return self.close(app)