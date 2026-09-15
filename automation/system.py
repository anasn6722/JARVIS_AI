from __future__ import annotations

import subprocess
from pathlib import Path

from automation.application_resolver import ApplicationResolver


class SystemController:
    """
    Windows system controller.

    Centralizes application launching and process control while
    reusing the shared ApplicationResolver.
    """

    def __init__(
        self,
        application_resolver: ApplicationResolver | None = None,
    ):
        self.application_resolver = (
            application_resolver
            or ApplicationResolver()
        )

    # ============================================================
    # BUILT-IN WINDOWS APPS
    # ============================================================

    def open_notepad(self) -> bool:
        """Open Windows Notepad."""
        return self.open_program("notepad")

    def open_calculator(self) -> bool:
        """Open Windows Calculator."""
        return self.open_program("calculator")

    def open_explorer(self) -> bool:
        """Open Windows File Explorer."""
        return self.open_program("file explorer")

    def open_camera(self) -> bool:
        """Open Windows Camera."""
        return self.open_program("camera")

    # ============================================================
    # OPEN PROGRAM
    # ============================================================

    def open_program(
        self,
        executable: str,
        arguments: list[str] | None = None,
    ) -> bool:
        """
        Resolve and launch a Windows application.

        Supports:
            - executable names
            - full paths
            - Windows aliases
            - shell targets
            - settings URIs
            - .lnk shortcuts
            - .msc/.cpl system tools
        """

        if not executable:
            return False

        target = str(executable).strip()

        if not target:
            return False

        args = arguments or []

        try:
            # ----------------------------------------------------
            # Resolve and launch through the canonical resolver
            # ----------------------------------------------------

            success, message = self.application_resolver.launch(
                target,
                arguments=args,
            )

            print(
                f"[SYSTEM] launch: {target!r}"
            )
            print(
                f"[SYSTEM] success: {success}"
            )
            print(
                f"[SYSTEM] message: {message}"
            )

            return success

        except (
            FileNotFoundError,
            OSError,
            PermissionError,
        ) as error:

            print(
                f"[SYSTEM] launch failed: {error}"
            )

            return False

        except Exception as error:

            print(
                f"[SYSTEM] unexpected launch error: {error}"
            )

            return False

    # ============================================================
    # OPEN PATH
    # ============================================================

    def open_path(self, path: str) -> bool:
        """
        Open a file, folder, drive, or Windows shell path.
        """

        if not path:
            return False

        target = str(path).strip()

        if not target:
            return False

        try:
            # ----------------------------------------------------
            # Existing filesystem object
            # ----------------------------------------------------

            filesystem_path = Path(target)

            if filesystem_path.exists():

                subprocess.Popen(
                    [
                        "explorer.exe",
                        str(filesystem_path),
                    ]
                )

                return True

            # ----------------------------------------------------
            # Drive
            # ----------------------------------------------------

            if len(target) == 2 and target[1] == ":":
                subprocess.Popen(
                    [
                        "explorer.exe",
                        target,
                    ]
                )

                return True

            # ----------------------------------------------------
            # Shell target
            # ----------------------------------------------------

            if target.lower().startswith("shell:"):
                subprocess.Popen(
                    [
                        "explorer.exe",
                        target,
                    ]
                )

                return True

        except (
            FileNotFoundError,
            OSError,
            PermissionError,
        ):

            return False

        return False

    # ============================================================
    # CLOSE PROGRAM
    # ============================================================

    def close_program(
        self,
        process_name: str,
    ) -> bool:
        """
        Close a Windows process by executable name.

        Example:
            chrome.exe
            notepad.exe
            code.exe
        """

        if not process_name:
            return False

        process = str(
            process_name
        ).strip().strip('"')

        if not process:
            return False

        if not process.lower().endswith(".exe"):
            process += ".exe"

        print("=" * 50)
        print("SYSTEM CONTROLLER CLOSE")
        print("Process:", process)

        try:
            result = subprocess.run(
                [
                    "taskkill",
                    "/F",
                    "/IM",
                    process,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

        except (
            FileNotFoundError,
            OSError,
            PermissionError,
        ) as error:

            print(
                "Close error:",
                error,
            )

            return False

        print(
            "Return Code:",
            result.returncode,
        )

        if result.stdout:
            print(
                "STDOUT:",
                result.stdout,
            )

        if result.stderr:
            print(
                "STDERR:",
                result.stderr,
            )

        return result.returncode == 0

    # ============================================================
    # PROCESS EXISTS
    # ============================================================

    def process_exists(
        self,
        process_name: str,
    ) -> bool:
        """
        Check whether a Windows process is running.
        """

        if not process_name:
            return False

        process = str(
            process_name
        ).strip()

        if not process:
            return False

        if not process.lower().endswith(".exe"):
            process += ".exe"

        try:
            result = subprocess.run(
                [
                    "tasklist",
                    "/FI",
                    f"IMAGENAME eq {process}",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            output = (
                result.stdout
                + "\n"
                + result.stderr
            ).lower()

            return (
                process.lower() in output
            )

        except (
            FileNotFoundError,
            OSError,
            PermissionError,
        ):
            return False

    # ============================================================
    # TOGGLE / SYSTEM ACTIONS
    # ============================================================

    def lock_pc(self) -> bool:
        """Lock the Windows workstation."""

        try:
            result = subprocess.run(
                [
                    "rundll32.exe",
                    "user32.dll,LockWorkStation",
                ],
                check=False,
            )

            return result.returncode == 0

        except OSError:
            return False

    def shutdown_pc(
        self,
        timeout: int = 0,
    ) -> bool:
        """Request Windows shutdown."""

        try:
            result = subprocess.run(
                [
                    "shutdown",
                    "/s",
                    "/t",
                    str(timeout),
                ],
                check=False,
            )

            return result.returncode == 0

        except OSError:
            return False

    def restart_pc(
        self,
        timeout: int = 0,
    ) -> bool:
        """Request Windows restart."""

        try:
            result = subprocess.run(
                [
                    "shutdown",
                    "/r",
                    "/t",
                    str(timeout),
                ],
                check=False,
            )

            return result.returncode == 0

        except OSError:
            return False

    def cancel_shutdown(self) -> bool:
        """Cancel a pending Windows shutdown/restart."""

        try:
            result = subprocess.run(
                [
                    "shutdown",
                    "/a",
                ],
                check=False,
            )

            return result.returncode == 0

        except OSError:
            return False