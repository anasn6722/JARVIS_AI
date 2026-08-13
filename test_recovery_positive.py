from ai.agent.recovery_manager import RecoveryManager
from ai.agent.task import Task


class FakeLLM:
    def ask(self, prompt, history=None, name="User"):
        return '{"action": "search", "target": "python"}'


manager = RecoveryManager(
    llm=FakeLLM(),
    available_tools_provider=lambda: [
        {
            "name": "open",
            "description": "Open an application",
        },
        {
            "name": "search",
            "description": "Search Google",
        },
    ],
    execution_context_provider=lambda: (
        "open unknown_app failed"
    ),
)

failed = Task(
    action="open",
    target="unknown_app",
)

failed.error = "Application not found."
failed.result = "Application not found."
failed.retry_count = 2

recovered = manager.recover(failed)

assert recovered is not None
assert recovered.action == "search"
assert recovered.target == "python"

print("RECOVERY POSITIVE TEST PASSED")
print("Recovered:", recovered)
