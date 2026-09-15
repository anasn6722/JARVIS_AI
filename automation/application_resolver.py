from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import ClassVar


class ApplicationResolver:
    """
    Robust Windows application resolver.

    Resolution priority:
        1. Built-in Windows aliases / shell commands
        2. Existing executable path
        3. Windows PATH
        4. Common executable aliases
        5. Registry App Paths
        6. Start Menu shortcuts / executables
        7. Common application directories
    """

    # =========================================================
    # WINDOWS SYSTEM / SHELL APPS
    # =========================================================

    SPECIAL_APPS: ClassVar[dict[str, str]] = {
        # File Explorer
        "file explorer": "explorer.exe",
        "windows explorer": "explorer.exe",
        "explorer": "explorer.exe",
        "windows file explorer": "explorer.exe",
        "my computer": "explorer.exe",

        # Windows shell locations
        "desktop": "shell:Desktop",
        "downloads": "shell:Downloads",
        "documents": "shell:Personal",
        "pictures": "shell:Pictures",
        "videos": "shell:Videos",
        "music": "shell:Music",
        "home": "shell:Home",
        "this pc": "shell:MyComputerFolder",
        "recycle bin": "shell:RecycleBinFolder",

        # Windows applications
        "calculator": "calc.exe",
        "windows calculator": "calc.exe",
        "notepad": "notepad.exe",
        "text editor": "notepad.exe",
        "paint": "mspaint.exe",
        "microsoft paint": "mspaint.exe",
        "snipping tool": "ms-screenclip:",
        "camera": "microsoft.windows.camera:",
        "windows camera": "microsoft.windows.camera:",

        # Terminals
        "command prompt": "cmd.exe",
        "cmd": "cmd.exe",
        "windows command prompt": "cmd.exe",
        "powershell": "powershell.exe",
        "windows powershell": "powershell.exe",
        "terminal": "wt.exe",
        "windows terminal": "wt.exe",

        # System tools
        "task manager": "taskmgr.exe",
        "control panel": "control.exe",
        "device manager": "devmgmt.msc",
        "registry editor": "regedit.exe",
        "services": "services.msc",
        "disk management": "diskmgmt.msc",
        "resource monitor": "resmon.exe",
        "system information": "msinfo32.exe",
        "event viewer": "eventvwr.msc",
        "computer management": "compmgmt.msc",

        # Settings
        "settings": "ms-settings:",
        "windows settings": "ms-settings:",
        "wifi settings": "ms-settings:network-wifi",
        "network settings": "ms-settings:network",
        "bluetooth settings": "ms-settings:bluetooth",
        "display settings": "ms-settings:display",
        "sound settings": "ms-settings:sound",
        "storage settings": "ms-settings:storagesense",
        "apps settings": "ms-settings:appsfeatures",
        "windows update": "ms-settings:windowsupdate",
    }

    # =========================================================
    # NATURAL-LANGUAGE EXECUTABLE ALIASES
    # =========================================================

    EXECUTABLE_ALIASES: ClassVar[dict[str, str]] = {
        "chrome": "chrome.exe",
        "google chrome": "chrome.exe",
        "browser": "chrome.exe",

        "code": "code.exe",
        "vs code": "code.exe",
        "vscode": "code.exe",
        "visual studio code": "code.exe",

        "edge": "msedge.exe",
        "microsoft edge": "msedge.exe",

        "firefox": "firefox.exe",
        "mozilla firefox": "firefox.exe",

        "word": "winword.exe",
        "microsoft word": "winword.exe",

        "excel": "excel.exe",
        "microsoft excel": "excel.exe",

        "powerpoint": "powerpnt.exe",
        "microsoft powerpoint": "powerpnt.exe",

        "outlook": "outlook.exe",
        "microsoft outlook": "outlook.exe",

        "spotify": "spotify.exe",
        "discord": "discord.exe",
        "steam": "steam.exe",
    }

    # =========================================================
    # NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize(value: str) -> str:
        value = str(value).strip().strip('"').strip("'").lower()

        # Collapse whitespace
        value = re.sub(r"\s+", " ", value)

        # Common spoken punctuation cleanup
        value = value.replace("’", "'")

        # Remove trailing "application" / "app" wording
        value = re.sub(r"\s+(application|app)$", "", value)

        return value.strip()

    # =========================================================
    # PUBLIC RESOLVE
    # =========================================================

    def resolve(self, executable: str) -> str | None:
        """
        Resolve an application or Windows component.

        Returns:
            Executable path, command, URI, shell target,
            or None if no match is found.
        """

        if not executable:
            return None

        original = executable
        name = self._normalize(executable)

        if not name:
            return None

        # -----------------------------------------------------
        # 1. SPECIAL WINDOWS / SHELL APPS
        # -----------------------------------------------------

        special = self.SPECIAL_APPS.get(name)

        if special:
            return special

        # -----------------------------------------------------
        # 2. DIRECT EXISTING PATH
        # -----------------------------------------------------

        direct = self._resolve_direct_path(original)

        if direct:
            return direct

        # -----------------------------------------------------
        # 3. EXACT PATH / PATH COMMAND
        # -----------------------------------------------------

        path_result = self._resolve_from_path(name)

        if path_result:
            return path_result

        # -----------------------------------------------------
        # 4. EXECUTABLE ALIAS
        # -----------------------------------------------------

        alias = self.EXECUTABLE_ALIASES.get(name)

        if alias:
            result = self._resolve_from_path(alias)

            if result:
                return result

            result = self._search_registry(alias)

            if result:
                return result

            result = self._search_application_directories(alias)

            if result:
                return result

        # -----------------------------------------------------
        # 5. NORMALIZE EXE NAME
        # -----------------------------------------------------

        executable_name = Path(name).name

        if not executable_name.endswith(".exe"):
            executable_name += ".exe"

        # -----------------------------------------------------
        # 6. PATH AGAIN USING FINAL EXE NAME
        # -----------------------------------------------------

        path_result = shutil.which(executable_name)

        if path_result:
            return path_result

        # -----------------------------------------------------
        # 7. REGISTRY APP PATHS
        # -----------------------------------------------------

        registry_result = self._search_registry(
            executable_name
        )

        if registry_result:
            return registry_result

        # -----------------------------------------------------
        # 8. START MENU
        # -----------------------------------------------------

        start_menu_result = self._search_start_menu(
            name,
            executable_name,
        )

        if start_menu_result:
            return start_menu_result

        # -----------------------------------------------------
        # 9. COMMON APPLICATION DIRECTORIES
        # -----------------------------------------------------

        directory_result = self._search_application_directories(
            executable_name
        )

        if directory_result:
            return directory_result

        return None

    # =========================================================
    # DIRECT PATH
    # =========================================================

    def _resolve_direct_path(
        self,
        value: str,
    ) -> str | None:

        cleaned = str(value).strip().strip('"')

        if not cleaned:
            return None

        path = Path(cleaned)

        try:
            if path.is_file():
                return str(path.resolve())
        except OSError:
            pass

        return None

    # =========================================================
    # WINDOWS PATH
    # =========================================================

    def _resolve_from_path(
        self,
        name: str,
    ) -> str | None:

        candidates = [name]

        if not name.endswith(".exe"):
            candidates.append(f"{name}.exe")

        for candidate in candidates:
            result = shutil.which(candidate)

            if result:
                return result

        return None

    # =========================================================
    # REGISTRY APP PATHS
    # =========================================================

    def _search_registry(
        self,
        executable_name: str,
    ) -> str | None:

        if os.name != "nt":
            return None

        try:
            import winreg
        except ImportError:
            return None

        executable_name = executable_name.lower()

        registry_locations = [
            (
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\App Paths",
            ),
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\Microsoft\Windows\CurrentVersion\App Paths",
            ),
        ]

        for hive, base_key in registry_locations:

            try:
                with winreg.OpenKey(
                    hive,
                    base_key,
                ) as root:

                    count = winreg.QueryInfoKey(root)[0]

                    for index in range(count):
                        try:
                            subkey_name = winreg.EnumKey(
                                root,
                                index,
                            )
                        except OSError:
                            continue

                        if subkey_name.lower() != executable_name:
                            continue

                        try:
                            with winreg.OpenKey(
                                root,
                                subkey_name,
                            ) as app_key:

                                value, _ = winreg.QueryValueEx(
                                    app_key,
                                    None,
                                )

                                if value and os.path.isfile(value):
                                    return value

                        except OSError:
                            continue

            except OSError:
                continue

        return None

    # =========================================================
    # START MENU SEARCH
    # =========================================================

    def _search_start_menu(
        self,
        requested_name: str,
        executable_name: str,
    ) -> str | None:

        locations = [
            os.path.join(
                os.environ.get("APPDATA", ""),
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
            ),
            os.path.join(
                os.environ.get("PROGRAMDATA", ""),
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
            ),
        ]

        requested = self._normalize(requested_name)

        # First inspect shortcuts.
        for location in locations:
            if not location or not os.path.isdir(location):
                continue

            result = self._search_shortcuts(
                location,
                requested,
            )

            if result:
                return result

        # Then inspect real executables.
        for location in locations:
            if not location or not os.path.isdir(location):
                continue

            try:
                for root, _, files in os.walk(location):

                    for filename in files:
                        lower = filename.lower()

                        if lower == executable_name.lower():
                            return os.path.join(
                                root,
                                filename,
                            )

            except OSError:
                continue

        return None

    # =========================================================
    # SHORTCUT SEARCH
    # =========================================================

    def _search_shortcuts(
        self,
        directory: str,
        requested_name: str,
    ) -> str | None:

        requested_tokens = set(
            requested_name.split()
        )

        try:
            for root, _, files in os.walk(directory):

                for filename in files:

                    if not filename.lower().endswith(".lnk"):
                        continue

                    shortcut_name = Path(
                        filename
                    ).stem.lower()

                    normalized_shortcut = self._normalize(
                        shortcut_name
                    )

                    if normalized_shortcut == requested_name:
                        return os.path.join(
                            root,
                            filename,
                        )

                    shortcut_tokens = set(
                        normalized_shortcut.split()
                    )

                    if requested_tokens and requested_tokens.issubset(
                        shortcut_tokens
                    ):
                        return os.path.join(
                            root,
                            filename,
                        )

        except OSError:
            pass

        return None

    # =========================================================
    # COMMON APPLICATION DIRECTORIES
    # =========================================================

    def _search_application_directories(
        self,
        executable_name: str,
    ) -> str | None:

        locations: list[str] = [
            os.environ.get("ProgramFiles", ""),
            os.environ.get("ProgramFiles(x86)", ""),
            os.environ.get("LOCALAPPDATA", ""),
        ]

        executable_name = executable_name.lower()

        for base in locations:

            if not base or not os.path.isdir(base):
                continue

            # First-level search avoids extremely expensive
            # whole-disk traversal.
            try:
                for entry in os.scandir(base):

                    if not entry.is_dir():
                        continue

                    try:
                        candidate = os.path.join(
                            entry.path,
                            executable_name,
                        )

                        if os.path.isfile(candidate):
                            return candidate

                    except OSError:
                        continue

            except OSError:
                continue

        return None

    # =========================================================
    # LAUNCH
    # =========================================================

    def launch(
        self,
        application: str,
        *,
        arguments: list[str] | None = None,
    ) -> tuple[bool, str]:
        """
        Resolve and launch an application.

        Handles normal executables, shell targets,
        URI targets and shortcuts.
        """

        resolved = self.resolve(application)

        if not resolved:
            return (
                False,
                f"I couldn't find an application or Windows component "
                f"called {application}.",
            )

        args = arguments or []

        # -----------------------------------------------------
        # Shell / URI targets
        # -----------------------------------------------------

        if (
            resolved.startswith("shell:")
            or resolved.startswith("ms-settings:")
            or resolved.endswith(":")
        ):
            try:
                subprocess.Popen(
                    ["explorer.exe", resolved],
                    shell=False,
                )

                return (
                    True,
                    f"Opened {application}.",
                )

            except OSError as error:
                return (
                    False,
                    f"Could not open {application}: {error}",
                )

        # -----------------------------------------------------
        # Shortcut
        # -----------------------------------------------------

        if resolved.lower().endswith(".lnk"):

            try:
                os.startfile(resolved)

                return (
                    True,
                    f"Opened {application}.",
                )

            except OSError as error:
                return (
                    False,
                    f"Could not open {application}: {error}",
                )

        # -----------------------------------------------------
        # .msc / .cpl / other Windows targets
        # -----------------------------------------------------

        if not resolved.lower().endswith(".exe"):
            try:
                subprocess.Popen(
                    ["cmd", "/c", "start", "", resolved, *args],
                    shell=False,
                )

                return (
                    True,
                    f"Opened {application}.",
                )

            except OSError as error:
                return (
                    False,
                    f"Could not open {application}: {error}",
                )

        # -----------------------------------------------------
        # Normal executable
        # -----------------------------------------------------

        try:
            subprocess.Popen(
                [resolved, *args],
                shell=False,
            )

            return (
                True,
                f"Opened {application}.",
            )

        except OSError as error:
            return (
                False,
                f"Could not launch {application}: {error}",
            )
