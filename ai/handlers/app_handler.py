from __future__ import annotations

from automation.config.apps import APPS
from automation.config.websites import WEBSITES


class AppHandler:
    """
    Handles application and website automation.

    Application resolution is delegated to the shared
    ApplicationResolver so registered applications,
    Windows applications, shell targets, aliases, and
    dynamically discovered applications follow one path.
    """

    def __init__(self, brain):
        self.brain = brain

    # =========================================================
    # OPEN
    # =========================================================

    def open(self, command):
        """
        Open one or more applications or websites.

        Supported inputs:
            - command string
            - Command object with entities
        """

        targets = self._extract_targets(command)

        if not targets:
            return (
                False,
                "I couldn't find anything to open.",
            )

        responses: list[str] = []
        overall_success = True

        for target in targets:
            success, message = self._open_target(target)

            responses.append(message)

            if not success:
                overall_success = False

        return (
            overall_success,
            "\n".join(responses),
        )

    # =========================================================
    # TARGET EXTRACTION
    # =========================================================

    def _extract_targets(self, command) -> list[str]:
        """
        Convert a command/string into normalized targets.
        """

        if isinstance(command, str):
            value = command.strip()

            if not value:
                return []

            return [value]

        targets: list[str] = []

        try:
            entities = command.entities
        except AttributeError:
            entities = {}

        apps = entities.get("apps", [])
        websites = entities.get("websites", [])

        targets.extend(apps)
        targets.extend(websites)

        return [
            str(target).strip()
            for target in targets
            if str(target).strip()
        ]

    # =========================================================
    # OPEN TARGET
    # =========================================================

    def _open_target(self, target: str):
        """
        Decide whether target is a website or application.
        """

        target = target.strip()

        normalized = target.lower()

        # -----------------------------------------------------
        # WEBSITE
        # -----------------------------------------------------

        if normalized in WEBSITES:
            return self._open_website(normalized)

        # -----------------------------------------------------
        # APPLICATION
        # -----------------------------------------------------

        return self._open_application(target)

    # =========================================================
    # OPEN WEBSITE
    # =========================================================

    def _open_website(self, website: str):
        """Open a registered website."""

        try:
            url = WEBSITES[website]

            self.brain.web.open_url(url)

            self._remember_website(website)

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
    # OPEN APPLICATION
    # =========================================================

    def _open_application(self, target: str):
        """
        Open an application using ApplicationResolver.

        Registered APPS remain supported, but their configured
        executable is resolved/launched through the same resolver
        path as dynamically discovered applications.
        """

        # -----------------------------------------------------
        # Resolve configured application
        # -----------------------------------------------------

        application_request = target

        registered = APPS.get(
            target.lower().strip()
        )

        if registered:
            application_request = registered.get(
                "open",
                target,
            )

        # -----------------------------------------------------
        # Use shared resolver
        # -----------------------------------------------------

        try:
            resolver = self.brain.application_resolver

            success, message = resolver.launch(
                application_request
            )

        except AttributeError:
            return (
                False,
                "Application resolver is not available.",
            )

        except Exception as error:
            return (
                False,
                f"Couldn't open {target.title()}: {error}",
            )

        if not success:
            return (
                False,
                message,
            )

        # -----------------------------------------------------
        # Memory / context
        # -----------------------------------------------------

        self._remember_app(
            target
        )

        return (
            True,
            f"Opened {target.title()}.",
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self, app):
        """
        Close an application.

        Strategy:
            1. Use configured process from APPS.
            2. Resolve executable dynamically.
            3. Derive process name from executable.
            4. Use SystemController close_program.
        """

        if not app:
            return (
                False,
                "No application was specified.",
            )

        target = str(app).strip()

        if not target:
            return (
                False,
                "No application was specified.",
            )

        normalized = target.lower()

        # -----------------------------------------------------
        # 1. Registered application
        # -----------------------------------------------------

        registered = APPS.get(normalized)

        if registered:
            process_name = registered.get("process")

            if process_name:
                return self._close_process(
                    target,
                    process_name,
                )

        # -----------------------------------------------------
        # 2. Dynamic resolution
        # -----------------------------------------------------

        try:
            resolved = (
                self.brain.application_resolver.resolve(
                    target
                )
            )

        except Exception as error:
            return (
                False,
                f"Couldn't resolve {target}: {error}",
            )

        if not resolved:
            return (
                False,
                f"I couldn't find an application called "
                f"{target}.",
            )

        # -----------------------------------------------------
        # 3. URI / shell targets cannot be process names
        # -----------------------------------------------------

        if (
            resolved.startswith("shell:")
            or resolved.startswith("ms-settings:")
            or resolved.endswith(":")
        ):
            return (
                False,
                f"{target.title()} is a Windows shell/settings "
                f"target and does not have a directly closable "
                f"application process.",
            )

        # -----------------------------------------------------
        # 4. Determine process name
        # -----------------------------------------------------

        process_name = self._process_name_from_resolved(
            resolved
        )

        if not process_name:
            return (
                False,
                f"I found {target}, but couldn't determine "
                f"its process.",
            )

        return self._close_process(
            target,
            process_name,
        )

    # =========================================================
    # CLOSE PROCESS
    # =========================================================

    def _close_process(
        self,
        target: str,
        process_name: str,
    ):
        """Close a process through the existing system layer."""

        try:
            success = (
                self.brain.system.close_program(
                    process_name
                )
            )

        except Exception as error:
            return (
                False,
                f"Couldn't close {target.title()}: {error}",
            )

        if not success:
            return (
                False,
                f"Couldn't close {target.title()}.",
            )

        # Update memory when possible.
        try:
            self.brain.conversation_memory.forget_app(
                target
            )
        except Exception:
            pass

        return (
            True,
            f"Closed {target.title()}.",
        )

    # =========================================================
    # PROCESS NAME
    # =========================================================

    @staticmethod
    def _process_name_from_resolved(
        resolved: str,
    ) -> str | None:
        """
        Convert an executable path/target into a process name.
        """

        value = str(resolved).strip()

        if not value:
            return None

        # Normal executable
        if value.lower().endswith(".exe"):
            filename = value.replace("\\", "/").split("/")[-1]

            if filename:
                return filename

        # Shortcut
        if value.lower().endswith(".lnk"):
            return None

        # MSC / CPL targets usually launch through MMC/control,
        # therefore don't guess their process.
        if value.lower().endswith(
            (".msc", ".cpl")
        ):
            return None

        return None

    # =========================================================
    # CLOSE LAST
    # =========================================================

    def close_last(self, argument=None):
        """
        Close the most recently referenced application or website.
        """

        reference = None

        try:
            reference = (
                self.brain.conversation_memory.last_reference()
            )
        except Exception:
            reference = None

        print(
            "🧠 CLOSE LAST REFERENCE:",
            reference,
        )

        if not reference:
            return (
                False,
                "There is no previously opened "
                "application or website.",
            )

        reference_type, reference_value = reference

        # -----------------------------------------------------
        # APPLICATION
        # -----------------------------------------------------

        if reference_type == "app":
            return self.close(
                reference_value
            )

        # -----------------------------------------------------
        # WEBSITE
        # -----------------------------------------------------

        if reference_type == "website":
            browser = self._resolve_last_browser()

            return self.close(
                browser
            )

        return (
            False,
            "I don't know how to close "
            "the last reference.",
        )

    # =========================================================
    # LAST BROWSER
    # =========================================================

    def _resolve_last_browser(self) -> str:
        """
        Determine a browser to close for a website reference.

        Chrome remains the default for backward compatibility.
        """

        for candidate in (
            "chrome",
            "edge",
            "firefox",
        ):
            if candidate.lower() in APPS:
                return candidate

        return "chrome"

    # =========================================================
    # MEMORY — APPLICATION
    # =========================================================

    def _remember_app(self, app: str) -> None:
        try:
            self.brain.conversation_memory.remember_app(
                app
            )
        except Exception:
            pass

        try:
            self.brain.session.last_app = app
        except Exception:
            pass

        try:
            self.brain.context.update(
                app=app
            )
        except Exception:
            pass

    # =========================================================
    # MEMORY — WEBSITE
    # =========================================================

    def _remember_website(self, website: str) -> None:
        try:
            self.brain.conversation_memory.remember_website(
                website
            )
        except Exception:
            pass

        try:
            self.brain.context.update(
                website=website
            )
        except Exception:
            pass
