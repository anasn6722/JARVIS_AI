from ai.workflow.graph import WorkflowGraph
from ai.workflow.graph_node import GraphNode


class GraphBuilder:

    def build(self, tasks):

        graph = WorkflowGraph()

        previous = None

        for task in tasks:

            node = GraphNode(
                id=task.id,
                task=task,
            )

            graph.add_node(node)

            if previous is not None:
                graph.connect(
                    previous.id,
                    node.id,
                )

            previous = node

        return graph