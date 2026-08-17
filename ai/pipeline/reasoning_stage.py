from types import SimpleNamespace


class ReasoningStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        context.decisions = []
        context.decision = None

        for item in context.commands:

            command = item["command"]

            # =================================================
            # MULTI-AGENT DECISION OVERRIDE
            # =================================================

            agent_result = item.get(
                "agent_result"
            )

            agent_name = item.get(
                "agent",
                "",
            )

            # -------------------------------------------------
            # JARVIS INTERNAL UI NAVIGATION
            # -------------------------------------------------

            if (
                agent_name == "ui"
                and agent_result is not None
                and agent_result.success
                and agent_result.metadata.get(
                    "internal_navigation",
                    False,
                )
            ):
                decision = SimpleNamespace(
                    route="UI",
                    intent="navigate",
                    agent="ui",
                    page_index=(
                        agent_result.metadata.get(
                            "page_index"
                        )
                    ),
                    confidence=1.0,
                    tool=None,
                    reason=(
                        "Handled by UIAgent "
                        "as internal JARVIS navigation."
                    ),
                )

            # -------------------------------------------------
            # NORMAL REASONING
            # -------------------------------------------------

            else:
                decision = (
                    self.brain.reasoning.decide(
                        command
                    )
                )

            context.decisions.append(
                {
                    "command": command,
                    "decision": decision,
                }
            )

            context.decision = decision

            print(
                "=" * 50
            )

            print(
                "REASONING"
            )

            print(
                decision
            )

            print(
                "=" * 50
            )