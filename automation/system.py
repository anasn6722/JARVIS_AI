import os
import shutil
import subprocess


class SystemController:
    """Controls Windows system applications and processes."""

    # -------------------------
    # Built-in Windows Apps
    # -------------------------

    def open_notepad(self):
        """Open Windows Notepad."""
        subprocess.Popen(["notepad.exe"])

    def open_calculator(self):
        """Open Windows Calculator."""
        subprocess.Popen(["calc.exe"])

    def open_explorer(self):
        """Open Windows File Explorer."""
        subprocess.Popen(["explorer.exe"])

    # -------------------------
    # Open Programs
    # -------------------------

    def open_program(self, executable: str) -> bool:
        """Open a Windows program or drive."""

        try:
            executable = executable.strip()

            if not executable:
                return False

            # -------------------------
            # Windows Drive
            # -------------------------

            if executable.endswith(":"):
                subprocess.Popen(
                    ["explorer.exe", executable]
                )
                return True

            # -------------------------
            # Existing Full Path
            # -------------------------

            if os.path.isfile(executable):
                subprocess.Popen([executable])
                return True

            # -------------------------
            # Search Windows PATH
            # -------------------------

            program = shutil.which(executable)

            if program:
                subprocess.Popen([program])
                return True

            # -------------------------
            # Search Executable Name
            # -------------------------

            executable_name = os.path.basename(
                executable
            )

            program = shutil.which(
                executable_name
            )

            if program:
                subprocess.Popen([program])
                return True

            # -------------------------
            # Common Windows Locations
            # -------------------------

            common_locations = [
                os.environ.get("ProgramFiles"),
                os.environ.get("ProgramFiles(x86)"),
                os.environ.get("LOCALAPPDATA"),
            ]

            for location in common_locations:
                if not location:
                    continue

                candidate = os.path.join(
                    location,
                    executable_name,
                )

                if os.path.isfile(candidate):
                    subprocess.Popen([candidate])
                    return True

            # -------------------------
            # Final Fallback
            # -------------------------

            subprocess.Popen(executable)
            return True

        except (
            FileNotFoundError,
            OSError,
            PermissionError,
        ):
            return False

    # -------------------------
    # Close Programs
    # -------------------------

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