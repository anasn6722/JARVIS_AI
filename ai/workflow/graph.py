from ai.workflow.graph_node import GraphNode


class WorkflowGraph:

    def __init__(self):

        self.nodes: dict[str, GraphNode] = {}


    def add_node(self, node: GraphNode):

        self.nodes[node.id] = node


    def connect(
        self,
        parent: str,
        child: str,
    ):

        self.nodes[parent].children.append(child)

        self.nodes[child].parents.append(parent)


    def get(
        self,
        node_id: str,
    ):

        return self.nodes.get(node_id)


    def all_nodes(self):

        return list(self.nodes.values())


    def root_nodes(self):

        return [
            node
            for node in self.nodes.values()
            if not node.parents
        ]