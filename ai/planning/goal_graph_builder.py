from ai.planning.goal_graph import GoalGraph
from ai.planning.goal_node import GoalNode


class GoalGraphBuilder:

    def build(
        self,
        tasks,
    ):

        graph = GoalGraph()

        previous = None

        for task in tasks:

            node = GoalNode(task)

            graph.add_node(node)

            if previous:

                graph.connect(
                    previous,
                    node,
                )

            previous = node

        return graph