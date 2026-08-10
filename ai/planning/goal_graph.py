from ai.planning.goal_node import GoalNode


class GoalGraph:

    def __init__(self):

        self.nodes = []

    def add_node(self, node: GoalNode):

        self.nodes.append(node)

    def all_nodes(self):
        """Return all nodes in the graph."""
        return self.nodes

    def connect(
        self,
        parent: GoalNode,
        child: GoalNode,
    ):

        parent.add_child(child)

    def roots(self):

        return [

            node

            for node in self.nodes

            if not node.parents

        ]

    def executable(self):

        return [

            node

            for node in self.nodes

            if (
                node.ready
                and not node.completed
                and not node.failed
                and not node.blocked
            )

        ]

    def completed(self):

        return all(

            node.completed

            for node in self.nodes

        )

    def reset(self):

        for node in self.nodes:

            node.completed = False

            node.failed = False

            node.blocked = False