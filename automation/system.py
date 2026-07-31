import shutil
import subprocess


class SystemController:
    def open_notepad(self):
        subprocess.Popen("notepad.exe")

    def open_calculator(self):
        subprocess.Popen("calc.exe")

    def open_explorer(self):
        subprocess.Popen("explorer.exe")

    def open_program(self, executable: str) -> bool:
        try:
            # Open drive like C:
            if executable.endswith(":"):
                subprocess.Popen(
                    ["explorer.exe", executable]
                )
                return True

            # Search executable in Windows PATH
            program = shutil.which(executable)

            if program:
                subprocess.Popen(program)
                return True

            # Fallback
            subprocess.Popen(executable)
            return True

        except (
            FileNotFoundError,
            OSError,
            PermissionError,
        ):
            return False

    import subprocess

    def close(self, app):

        processes = {
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "firefox": "firefox.exe",
            "notepad": "notepad.exe",
            "calculator": "CalculatorApp.exe",
        }
    
        process = processes.get(app)
    
        if not process:
            return f"I don't know how to close {app}."
    
        subprocess.run(
            ["taskkill", "/IM", process, "/F"],
            capture_output=True,
        )
    
        return f"Closed {app.title()}."