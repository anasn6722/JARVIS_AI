from ai.agent.task import Task


class Planner:
    def plan(self, command: str):
        command = command.lower()

        separators = [
            " then ",
            " and ",
            ",",
        ]

        commands = [command]

        for separator in separators:
            new_commands = []

            for cmd in commands:
                new_commands.extend(cmd.split(separator))

            commands = new_commands

        tasks = []

        for cmd in commands:
            cmd = cmd.strip()

            if not cmd:
                continue

            if cmd.startswith(("open ", "launch ")):
                target = (
                    cmd.replace("open ", "", 1)
                    .replace("launch ", "", 1)
                    .strip()
                )

                tasks.append(Task("open", target))

            elif cmd.startswith("search "):
                target = cmd.replace("search ", "", 1).strip()
                tasks.append(Task("search", target))

            elif "time" in cmd:
                tasks.append(Task("get_time"))

            else:
                tasks.append(Task("chat", cmd))

        return tasks