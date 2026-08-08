import subprocess

from automation.application_resolver import ApplicationResolver


class SystemController:
    """Controls Windows system applications and processes."""

    def __init__(self):
        self.application_resolver = ApplicationResolver()

    # ============================================================
    # BUILT-IN WINDOWS APPS
    # ============================================================

    def open_notepad(self):
        """Open Windows Notepad."""
        subprocess.Popen(["notepad.exe"])

    def open_calculator(self):
        """Open Windows Calculator."""
        subprocess.Popen(["calc.exe"])

    def open_explorer(self):
        """Open Windows File Explorer."""
        subprocess.Popen(["explorer.exe"])

    def open_camera(self) -> bool:
        """Open the Windows Camera app."""

        try:
            subprocess.Popen(
                [
                    "explorer.exe",
                    "microsoft.windows.camera:",
                ]
            )

            return True

        except (
            FileNotFoundError,
            OSError,
            PermissionError,
        ):
            return False

    # ============================================================
    # OPEN PROGRAMS
    # ============================================================

    def open_program(
        self,
        executable: str,
    ) -> bool:
        """Open a Windows program or drive."""

        try:
            executable = executable.strip()

            if not executable:
                return False

            # ----------------------------------------------------
            # WINDOWS CAMERA
            # ----------------------------------------------------

            if executable.lower() in {
                "camera",
                "windows camera",
            }:
                return self.open_camera()

            # ----------------------------------------------------
            # WINDOWS DRIVE
            # ----------------------------------------------------

            if executable.endswith(":"):
                subprocess.Popen(
                    [
                        "explorer.exe",
                        executable,
                    ]
                )

                return True

            # ----------------------------------------------------
            # RESOLVE APPLICATION
            # ----------------------------------------------------

            program = self.application_resolver.resolve(
                executable
            )

            if not program:
                return False

            # ----------------------------------------------------
            # LAUNCH APPLICATION
            # ----------------------------------------------------

            subprocess.Popen([program])

            return True

        except (
            FileNotFoundError,
            OSError,
            PermissionError,
        ):
            return False

    # ============================================================
    # CLOSE PROGRAMS
    # ============================================================

    def close_program(
        self,
        process_name: str,
    ) -> bool:
        """Close a Windows process."""

        print("=" * 50)
        print("SYSTEM CONTROLLER CLOSE")
        print("Process:", process_name)

        result = subprocess.run(
            [
                "taskkill",
                "/F",
                "/IM",
                process_name,
            ],
            capture_output=True,
            text=True,
        )

        print(
            "Return Code:",
            result.returncode,
        )

        print(
            "STDOUT:",
            result.stdout,
        )

        print(
            "STDERR:",
            result.stderr,
        )

        return result.returncode == 0