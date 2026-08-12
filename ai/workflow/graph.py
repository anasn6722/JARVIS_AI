from ai.workflow.graph_node import GraphNode


class WorkflowGraph:

    def __init__(self):
        self.nodes: dict[str, GraphNode] = {}

    # ============================================================
    # ADD NODE
    # ============================================================

    def add_node(self, node: GraphNode):
        self.nodes[node.id] = node

    # ============================================================
    # CONNECT NODES
    # ============================================================

    def connect(
        self,
        parent: str,
        child: str,
    ):
        self.nodes[parent].children.append(child)
        self.nodes[child].parents.append(parent)

    # ============================================================
    # GET NODE
    # ============================================================

    def get(
        self,
        node_id: str,
    ):
        return self.nodes.get(node_id)

    # ============================================================
    # ALL NODES
    # ============================================================

    def all_nodes(self):
        return list(self.nodes.values())

    # ============================================================
    # ROOT NODES
    # ============================================================

    def root_nodes(self):
        return [
            node
            for node in self.nodes.values()
            if not node.parents
        ]

    # ============================================================
    # EXECUTABLE NODES
    # ============================================================

    def executable(self):
        """
        Return all nodes whose dependencies have completed.
        """

        ready_nodes = []

        for node in self.nodes.values():

            if node.completed:
                continue

            if node.failed:
                continue

            if node.blocked:
                continue

            if node.running:
                continue

            dependencies_complete = True

            for parent_id in node.parents:

                parent = self.nodes.get(parent_id)

                if parent is None:
                    dependencies_complete = False
                    break

                if not parent.completed:
                    dependencies_complete = False
                    break

            if dependencies_complete:
                ready_nodes.append(node)

        return ready_nodes

    # ============================================================
    # GRAPH COMPLETED
    # ============================================================

    def completed(self):
        """
        Return True when every graph node has completed.
        """

        if not self.nodes:
            return True

        return all(
            node.completed
            for node in self.nodes.values()
        )