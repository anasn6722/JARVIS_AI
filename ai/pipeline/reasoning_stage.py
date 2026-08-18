from types import SimpleNamespace


class ReasoningStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        context.decisions = []
        context.decision = None

        for item in context.commands:

            command = item["command"]

            agent_result = item.get(
                "agent_result"
            )

            agent_name = item.get(
                "agent",
                "",
            )

            # =================================================
            # UI AGENT
            # =================================================

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

            # =================================================
            # VOICE AGENT
            # =================================================

            elif (
                agent_name == "voice"
                and agent_result is not None
                and agent_result.success
                and "response" in agent_result.metadata
            ):

                decision = SimpleNamespace(
                    route="VOICE",
                    intent=command.intent,
                    agent="voice",
                    confidence=1.0,
                    tool=None,
                    response=(
                        agent_result.metadata.get(
                            "response"
                        )
                    ),
                    reason=(
                        "Handled directly by "
                        "VoiceAgent."
                    ),
                )

            # =================================================
            # MEMORY AGENT
            # =================================================

            elif agent_name == "memory":

                decision = SimpleNamespace(
                    route="BUILTIN",
                    intent=command.intent,
                    agent="memory",
                    confidence=1.0,
                    tool=None,
                    reason=(
                        "Handled by MemoryAgent "
                        "using existing memory handlers."
                    ),
                )

            # =================================================
            # NORMAL REASONING
            # =================================================

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