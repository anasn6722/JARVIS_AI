from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


class FileManager:
    """
    Deterministic Windows filesystem automation.

    Responsibilities:
        - Resolve common Windows locations
        - Inspect files and directories
        - Create files and folders
        - Copy / move / rename
        - Search for files
        - Open files and folders

    Destructive operations such as delete are exposed separately
    so the higher-level safety layer can require confirmation.
    """

    # =========================================================
    # SPECIAL WINDOWS LOCATIONS
    # =========================================================

    SPECIAL_LOCATIONS = {
        "desktop": Path.home() / "Desktop",
        "downloads": Path.home() / "Downloads",
        "documents": Path.home() / "Documents",
        "pictures": Path.home() / "Pictures",
        "videos": Path.home() / "Videos",
        "music": Path.home() / "Music",
    }

    # =========================================================
    # WORKSPACE ALIASES
    # =========================================================

    @staticmethod
    def _workspace_aliases() -> dict[str, Path]:
        """
        Return aliases for the current JARVIS workspace.
        """

        cwd = Path.cwd().resolve()

        aliases = {
            cwd.name.lower(): cwd,
            "jarvis": cwd,
            "jarvis_ai": cwd,
            "current project": cwd,
            "project": cwd,
            "workspace": cwd,
        }

        return aliases

    # =========================================================
    # PATH RESOLUTION
    # =========================================================

    def resolve_path(
        self,
        path: str | os.PathLike[str],
        *,
        base: str | os.PathLike[str] | None = None,
    ) -> Path:
        """
        Resolve a user-friendly path into an absolute Path.

        Examples:
            Desktop
            Downloads
            Desktop\\Projects
            C:\\Users\\...
        """

        if path is None:
            raise ValueError("Path is required.")

        value = str(path).strip().strip('"').strip("'")

        if not value:
            raise ValueError("Path is empty.")

        normalized = " ".join(
            value.lower().split()
        )
        # -----------------------------------------------------
        # Current workspace aliases
        # -----------------------------------------------------

        workspace_aliases = (
            self._workspace_aliases()
        )

        if normalized in workspace_aliases:
            return workspace_aliases[
                normalized
            ]

        # -----------------------------------------------------
        # SPECIAL LOCATION EXACT MATCH
        # -----------------------------------------------------

        if normalized in self.SPECIAL_LOCATIONS:
            return self.SPECIAL_LOCATIONS[
                normalized
            ]

        # -----------------------------------------------------
        # SPECIAL LOCATION PREFIX
        # -----------------------------------------------------

        for name, location in self.SPECIAL_LOCATIONS.items():
            prefix = f"{name}\\"

            if normalized.startswith(prefix):
                remainder = value[
                    len(name) + 1:
                ].strip()

                if remainder:
                    return (
                        location / remainder
                    ).expanduser()

                return location

        # -----------------------------------------------------
        # Expand environment variables
        # -----------------------------------------------------

        expanded = os.path.expandvars(value)

        # -----------------------------------------------------
        # Home shortcut
        # -----------------------------------------------------

        if expanded == "~":
            return Path.home()

        if expanded.startswith("~/") or expanded.startswith("~\\"):
            return Path(expanded).expanduser()

        # -----------------------------------------------------
        # Absolute path
        # -----------------------------------------------------

        path_obj = Path(expanded)

        if path_obj.is_absolute():
            return path_obj

        # -----------------------------------------------------
        # Base directory
        # -----------------------------------------------------

        if base is not None:
            base_path = self.resolve_path(base)

            return (
                base_path / expanded
            ).resolve()

        # -----------------------------------------------------
        # Default relative location
        # -----------------------------------------------------

        return (
            Path.cwd() / expanded
        ).resolve()

    # =========================================================
    # EXISTS
    # =========================================================

    def exists(self, path: str) -> bool:
        """Return True when a file or directory exists."""

        try:
            return self.resolve_path(path).exists()
        except (OSError, ValueError):
            return False

    # =========================================================
    # FILE EXISTS
    # =========================================================

    def is_file(self, path: str) -> bool:
        """Return True when path is a file."""

        try:
            return self.resolve_path(path).is_file()
        except (OSError, ValueError):
            return False

    # =========================================================
    # DIRECTORY EXISTS
    # =========================================================

    def is_directory(self, path: str) -> bool:
        """Return True when path is a directory."""

        try:
            return self.resolve_path(path).is_dir()
        except (OSError, ValueError):
            return False

    # =========================================================
    # LIST DIRECTORY
    # =========================================================

    def list_directory(
        self,
        path: str,
    ) -> tuple[bool, list[dict[str, Any]] | str]:
        """
        List entries in a directory.
        """

        try:
            directory = self.resolve_path(path)

            if not directory.exists():
                return (
                    False,
                    f"Directory not found: {directory}",
                )

            if not directory.is_dir():
                return (
                    False,
                    f"Not a directory: {directory}",
                )

            items: list[dict[str, Any]] = []

            for entry in sorted(
                directory.iterdir(),
                key=lambda item: (
                    not item.is_dir(),
                    item.name.lower(),
                ),
            ):
                try:
                    items.append(
                        {
                            "name": entry.name,
                            "path": str(entry),
                            "type": (
                                "directory"
                                if entry.is_dir()
                                else "file"
                            ),
                            "size": (
                                entry.stat().st_size
                                if entry.is_file()
                                else None
                            ),
                        }
                    )
                except OSError:
                    continue

            return True, items

        except (OSError, ValueError) as error:
            return False, str(error)

    # =========================================================
    # CREATE FOLDER
    # =========================================================

    def create_folder(
        self,
        path: str,
    ) -> tuple[bool, str]:
        """Create a directory and missing parent directories."""

        try:
            directory = self.resolve_path(path)

            if directory.exists():
                if directory.is_dir():
                    return (
                        True,
                        f"Folder already exists: {directory}",
                    )

                return (
                    False,
                    f"A file already exists at: {directory}",
                )

            directory.mkdir(
                parents=True,
                exist_ok=False,
            )

            return (
                True,
                f"Created folder: {directory}",
            )

        except (OSError, ValueError) as error:
            return (
                False,
                f"Could not create folder: {error}",
            )

    # =========================================================
    # CREATE FILE
    # =========================================================

    def create_file(
        self,
        path: str,
        content: str = "",
    ) -> tuple[bool, str]:
        """
        Create a text file.

        Parent directories are created automatically.
        """

        try:
            file_path = self.resolve_path(path)

            if file_path.exists():
                return (
                    False,
                    f"File already exists: {file_path}",
                )

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_path.write_text(
                str(content),
                encoding="utf-8",
            )

            return (
                True,
                f"Created file: {file_path}",
            )

        except (OSError, ValueError) as error:
            return (
                False,
                f"Could not create file: {error}",
            )

    # =========================================================
    # READ TEXT FILE
    # =========================================================

    def read_text(
        self,
        path: str,
    ) -> tuple[bool, str]:
        """Read a UTF-8 text file."""

        try:
            file_path = self.resolve_path(path)

            if not file_path.exists():
                return (
                    False,
                    f"File not found: {file_path}",
                )

            if not file_path.is_file():
                return (
                    False,
                    f"Not a file: {file_path}",
                )

            return (
                True,
                file_path.read_text(
                    encoding="utf-8"
                ),
            )

        except (OSError, UnicodeError, ValueError) as error:
            return (
                False,
                f"Could not read file: {error}",
            )

    # =========================================================
    # COPY
    # =========================================================

    def copy(
        self,
        source: str,
        destination: str,
    ) -> tuple[bool, str]:
        """
        Copy a file or directory.
        """

        try:
            source_path = self.resolve_path(source)
            destination_path = self.resolve_path(
                destination
            )

            if not source_path.exists():
                return (
                    False,
                    f"Source not found: {source_path}",
                )

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            if source_path.is_dir():
                target = destination_path

                if target.exists():
                    target = (
                        target
                        / source_path.name
                    )

                shutil.copytree(
                    source_path,
                    target,
                    dirs_exist_ok=True,
                )

                return (
                    True,
                    f"Copied folder to: {target}",
                )

            target = destination_path

            if destination_path.exists() and destination_path.is_dir():
                target = (
                    destination_path
                    / source_path.name
                )

            shutil.copy2(
                source_path,
                target,
            )

            return (
                True,
                f"Copied file to: {target}",
            )

        except (OSError, shutil.Error, ValueError) as error:
            return (
                False,
                f"Could not copy: {error}",
            )

    # =========================================================
    # MOVE
    # =========================================================

    def move(
        self,
        source: str,
        destination: str,
    ) -> tuple[bool, str]:
        """
        Move a file or directory.
        """

        try:
            source_path = self.resolve_path(source)
            destination_path = self.resolve_path(
                destination
            )

            if not source_path.exists():
                return (
                    False,
                    f"Source not found: {source_path}",
                )

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            target = destination_path

            if (
                destination_path.exists()
                and destination_path.is_dir()
            ):
                target = (
                    destination_path
                    / source_path.name
                )

            result = shutil.move(
                str(source_path),
                str(target),
            )

            return (
                True,
                f"Moved to: {result}",
            )

        except (OSError, shutil.Error, ValueError) as error:
            return (
                False,
                f"Could not move: {error}",
            )

    # =========================================================
    # RENAME
    # =========================================================

    def rename(
        self,
        source: str,
        new_name: str,
    ) -> tuple[bool, str]:
        """
        Rename a file or directory.

        new_name should be a name, not a complete path.
        """

        if not new_name:
            return (
                False,
                "New name is required.",
            )

        try:
            source_path = self.resolve_path(source)

            if not source_path.exists():
                return (
                    False,
                    f"Source not found: {source_path}",
                )

            clean_name = str(
                new_name
            ).strip().strip('"').strip("'")

            if not clean_name:
                return (
                    False,
                    "New name is empty.",
                )

            if (
                Path(clean_name).name
                != clean_name
            ):
                return (
                    False,
                    "New name must be a single filename or folder name.",
                )

            destination = (
                source_path.parent
                / clean_name
            )

            if destination.exists():
                return (
                    False,
                    f"Destination already exists: {destination}",
                )

            source_path.rename(
                destination
            )

            return (
                True,
                f"Renamed to: {destination}",
            )

        except (OSError, ValueError) as error:
            return (
                False,
                f"Could not rename: {error}",
            )

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        path: str,
    ) -> tuple[bool, str]:
        """
        Delete a file or directory.

        This method is intentionally separate so the higher-level
        safety layer can require user confirmation before calling it.
        """

        try:
            target = self.resolve_path(path)

            if not target.exists():
                return (
                    False,
                    f"Path not found: {target}",
                )

            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()

            return (
                True,
                f"Deleted: {target}",
            )

        except (OSError, shutil.Error, ValueError) as error:
            return (
                False,
                f"Could not delete: {error}",
            )

    # =========================================================
    # SEARCH
    # =========================================================

    def search(
        self,
        directory: str,
        pattern: str,
        *,
        recursive: bool = True,
        limit: int = 100,
    ) -> tuple[bool, list[str] | str]:
        """
        Search a directory for files/folders matching a pattern.

        Examples:
            *.pdf
            *.py
            notes*
            report.docx
        """

        if not pattern:
            return (
                False,
                "Search pattern is required.",
            )

        if limit <= 0:
            return (
                False,
                "Search limit must be greater than zero.",
            )

        try:
            root = self.resolve_path(directory)

            if not root.exists():
                return (
                    False,
                    f"Directory not found: {root}",
                )

            if not root.is_dir():
                return (
                    False,
                    f"Not a directory: {root}",
                )

            if recursive:
                iterator = root.rglob(
                    pattern
                )
            else:
                iterator = root.glob(
                    pattern
                )

            results: list[str] = []

            for item in iterator:
                results.append(
                    str(item)
                )

                if len(results) >= limit:
                    break

            return True, results

        except (OSError, ValueError) as error:
            return (
                False,
                f"Search failed: {error}",
            )

    # =========================================================
    # FILE INFORMATION
    # =========================================================

    def file_info(
        self,
        path: str,
    ) -> tuple[bool, dict[str, Any] | str]:
        """Return metadata for a file or directory."""

        try:
            target = self.resolve_path(path)

            if not target.exists():
                return (
                    False,
                    f"Path not found: {target}",
                )

            stats = target.stat()

            return (
                True,
                {
                    "name": target.name,
                    "path": str(target),
                    "type": (
                        "directory"
                        if target.is_dir()
                        else "file"
                    ),
                    "size": stats.st_size,
                    "extension": (
                        target.suffix
                        if target.is_file()
                        else ""
                    ),
                    "parent": str(
                        target.parent
                    ),
                },
            )

        except (OSError, ValueError) as error:
            return (
                False,
                f"Could not inspect path: {error}",
            )

    # =========================================================
    # OPEN
    # =========================================================

    def open_path(
        self,
        path: str,
    ) -> tuple[bool, str]:
        """
        Open a file or folder with Windows' default application.
        """

        try:
            target = self.resolve_path(path)

            if not target.exists():
                return (
                    False,
                    f"Path not found: {target}",
                )

            os.startfile(str(target))

            return (
                True,
                f"Opened: {target}",
            )

        except (OSError, ValueError) as error:
            return (
                False,
                f"Could not open path: {error}",
            )

    # =========================================================
    # OPEN IN EXPLORER
    # =========================================================

    def open_in_explorer(
        self,
        path: str,
    ) -> tuple[bool, str]:
        """Open a file/folder using Windows Explorer."""

        try:
            target = self.resolve_path(path)

            if not target.exists():
                return (
                    False,
                    f"Path not found: {target}",
                )

            subprocess.Popen(
                [
                    "explorer.exe",
                    str(target),
                ]
            )

            return (
                True,
                f"Opened in File Explorer: {target}",
            )

        except (OSError, ValueError) as error:
            return (
                False,
                f"Could not open in File Explorer: {error}",
            )
