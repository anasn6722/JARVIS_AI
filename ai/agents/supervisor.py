from concurrent.futures import ThreadPoolExecutor, as_completed

from ai.agents.conversation_agent import ConversationAgent
from ai.agents.desktop_agent import DesktopAgent
from ai.agents.memory_agent import MemoryAgent
from ai.agents.research_agent import ResearchAgent
from ai.agents.ui_agent import UIAgent
from ai.agents.voice_agent import VoiceAgent


class SupervisorAgent:
    """Routes JARVIS commands to specialist agents."""

    name = "supervisor"

    def __init__(self):
        self.agents = (
            UIAgent(),
            MemoryAgent(),
            VoiceAgent(),
            ResearchAgent(),
            DesktopAgent(),
            ConversationAgent(),
        )

    # =========================================================
    # SINGLE AGENT
    # =========================================================

    def select_agent(self, command):
        """
        Preserve the original behavior.

        Returns the first specialist agent that can handle
        the command.
        """

        for agent in self.agents:

            try:

                if agent.can_handle(command):
                    return agent

            except Exception as error:

                print(
                    f"Supervisor agent check failed "
                    f"for {agent.name}: {error}"
                )

        return None

    # =========================================================
    # ALL MATCHING AGENTS
    # =========================================================

    def select_agents(self, command):
        """
        Return every specialist capable of handling the command.

        The first agent remains the primary agent.
        """

        matches = []

        for agent in self.agents:

            try:

                if agent.can_handle(command):
                    matches.append(agent)

            except Exception as error:

                print(
                    f"Supervisor agent check failed "
                    f"for {agent.name}: {error}"
                )

        return matches

    # =========================================================
    # SINGLE ROUTE
    # =========================================================

    def route(self, command, context):

        agent = self.select_agent(
            command
        )

        if agent is None:
            return None

        context.agent_name = (
            agent.name
        )

        return agent.run(
            context
        )

    # =========================================================
    # MULTI-AGENT ROUTE
    # =========================================================

    def route_many(
        self,
        command_contexts,
        *,
        max_workers=4,
    ):
        """
        Route independent commands to specialist agents.

        Each item must be:

            (command, AgentContext)

        The contexts are isolated from each other.

        This method is intentionally separate from `route()`
        so existing single-command behavior stays unchanged.
        """

        if not command_contexts:
            return []

        results = []

        worker_count = min(
            max_workers,
            len(command_contexts),
        )

        print("=" * 60)
        print("MULTI-AGENT SUPERVISOR")
        print(
            "Commands:",
            len(command_contexts),
        )
        print(
            "Workers:",
            worker_count,
        )
        print("=" * 60)

        with ThreadPoolExecutor(
            max_workers=worker_count,
            thread_name_prefix="jarvis-agent",
        ) as executor:

            future_map = {}

            for command, context in command_contexts:

                future = executor.submit(
                    self._route_one,
                    command,
                    context,
                )

                future_map[
                    future
                ] = (
                    command,
                    context,
                )

            for future in as_completed(
                future_map
            ):

                command, context = (
                    future_map[future]
                )

                try:

                    result = future.result()

                except Exception as error:

                    print(
                        "Multi-agent execution error:",
                        error,
                    )

                    context.set_error(
                        error
                    )

                    results.append(
                        {
                            "command": command,
                            "context": context,
                            "result": None,
                            "error": str(error),
                        }
                    )

                    continue

                results.append(
                    {
                        "command": command,
                        "context": context,
                        "result": result,
                        "error": None,
                    }
                )

        # -----------------------------------------------------
        # Restore original command order.
        # -----------------------------------------------------

        results.sort(
            key=lambda item: (
                getattr(
                    item["context"],
                    "metadata",
                    {},
                ).get(
                    "command_index",
                    0,
                )
            )
        )

        print("=" * 60)
        print("MULTI-AGENT SUPERVISOR FINISHED")
        print("=" * 60)

        return results

    # =========================================================
    # INTERNAL ROUTE
    # =========================================================

    def _route_one(
        self,
        command,
        context,
    ):

        agent = self.select_agent(
            command
        )

        if agent is None:

            context.set_error(
                f"No agent can handle: "
                f"{command.original}"
            )

            return None

        context.agent_name = (
            agent.name
        )

        print(
            f"[Agent] "
            f"{agent.name} "
            f"← "
            f"{command.original}"
        )

        result = agent.run(
            context
        )

        return result