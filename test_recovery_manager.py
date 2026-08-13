from ai.agent.recovery_manager import RecoveryManager
from ai.agent.task import Task


class FakeLLM:

    def __init__(self, response):
        self.response = response

    def ask(
        self,
        prompt,
        history=None,
        name="User",
    ):
        return self.response


def test_recovery_creates_alternative_task():

    llm = FakeLLM(
        """
        {
            "action": "search",
            "target": "chrome alternative"
        }
        """
    )

    manager = RecoveryManager(
        llm=llm,
        available_tools_provider=lambda: [
            {
                "name": "search",
                "description": "Search Google",
            },
            {
                "name": "open",
                "description": "Open an application",
            },
        ],
        execution_context_provider=lambda: (
            "Previous action failed."
        ),
    )

    failed_task = Task(
        action="open",
        target="x",
    )

    failed_task.error = (
        "I couldn't find an installed application "
        "called x."
    )

    failed_task.retry_count = 2

    recovered = manager.recover(
        failed_task
    )

    assert recovered is not None
    assert recovered.action == "search"
    assert recovered.target == (
        "chrome alternative"
    )


def test_recovery_rejects_same_task():

    llm = FakeLLM(
        """
        {
            "action": "open",
            "target": "x"
        }
        """
    )

    manager = RecoveryManager(
        llm=llm,
        available_tools_provider=lambda: [
            {
                "name": "open",
                "description": "Open an application",
            }
        ],
        execution_context_provider=lambda: "",
    )

    failed_task = Task(
        action="open",
        target="x",
    )

    recovered = manager.recover(
        failed_task
    )

    assert recovered is None