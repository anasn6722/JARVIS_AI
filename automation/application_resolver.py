import os
import shutil
import subprocess
from typing import ClassVar


class ApplicationResolver:
    """Find installed Windows applications."""

    # =========================================================
    # WINDOWS STORE / SYSTEM APPS
    # =========================================================

    SPECIAL_APPS: ClassVar[dict[str, str]] = {
        "camera": "microsoft.windows.camera:",
        "windows camera": "microsoft.windows.camera:",
        "calculator": "calculator:",
        "windows calculator": "calculator:",
    }

    # =========================================================
    # RESOLVE APPLICATION
    # =========================================================

    def resolve(
        self,
        executable: str,
    ) -> str | None:
        """
        Resolve an executable name or path.

        Returns:
            str | None:
                Resolved executable path, URI, or None.
        """

        if not executable:
            return None

        executable = (
            executable
            .strip()
            .strip('"')
            .lower()
        )

        if not executable:
            return None

        # -----------------------------------------------------
        # 1. Special Windows / Store Apps
        # -----------------------------------------------------

        special_app = self.SPECIAL_APPS.get(
            executable
        )

        if special_app:
            return special_app

        # -----------------------------------------------------
        # 2. Existing Full Path
        # -----------------------------------------------------

        if os.path.isfile(executable):
            return executable

        # -----------------------------------------------------
        # 3. Windows PATH
        # -----------------------------------------------------

        program = shutil.which(executable)

        if program:
            return program

        # -----------------------------------------------------
        # 4. Try With .exe Extension
        # -----------------------------------------------------

        if not executable.endswith(".exe"):
            program = shutil.which(
                f"{executable}.exe"
            )

            if program:
                return program

        # -----------------------------------------------------
        # 5. Extract Executable Filename
        # -----------------------------------------------------

        executable_name = os.path.basename(
            executable
        )

        if not executable_name.endswith(".exe"):
            executable_name += ".exe"

        # -----------------------------------------------------
        # 6. Search PATH Again
        # -----------------------------------------------------

        program = shutil.which(
            executable_name
        )

        if program:
            return program

        # -----------------------------------------------------
        # 7. Common Windows Application Directories
        # -----------------------------------------------------

        locations = [
            os.environ.get("ProgramFiles"),
            os.environ.get("ProgramFiles(x86)"),
            os.environ.get("LOCALAPPDATA"),
        ]

        for location in locations:
            if not location:
                continue

            candidate = os.path.join(
                location,
                executable_name,
            )

            if os.path.isfile(candidate):
                return candidate

        # -----------------------------------------------------
        # 8. Start Menu Search
        # -----------------------------------------------------

        start_menu_locations = [
            os.path.join(
                os.environ.get(
                    "APPDATA",
                    "",
                ),
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
            ),
            os.path.join(
                os.environ.get(
                    "ProgramData",
                    "",
                ),
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
            ),
        ]

        for start_menu in start_menu_locations:
            if not os.path.isdir(start_menu):
                continue

            result = self._search_start_menu(
                start_menu,
                executable_name,
            )

            if result:
                return result

        return None

    # =========================================================
    # START MENU SEARCH
    # =========================================================

    def _search_start_menu(
        self,
        directory: str,
        executable_name: str,
    ) -> str | None:
        """
        Search Start Menu recursively.

        Searches for executable files.
        """

        executable_name = (
            executable_name.lower()
        )

        for root, _, files in os.walk(
            directory
        ):
            for filename in files:
                if filename.lower() == executable_name:
                    return os.path.join(
                        root,
                        filename,
                    )

        return None

