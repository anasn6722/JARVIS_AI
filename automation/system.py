import subprocess


class SystemController:

    def open_notepad(self):
        subprocess.Popen("notepad.exe")

    def open_calculator(self):
        subprocess.Popen("calc.exe")

    def open_explorer(self):
        subprocess.Popen("explorer.exe")

    def open_program(self, executable: str):
        try:
            if executable.endswith(":"):
              subprocess.Popen(
                ["explorer.exe", executable]
            )
            else:
              subprocess.Popen(executable)

            return True

        except (FileNotFoundError, OSError):
         return False