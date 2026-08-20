from ai.workflow.graph import WorkflowGraph
from ai.workflow.graph_node import GraphNode


class GraphBuilder:
    """
    Build a dependency-aware workflow graph.

    Rules:

    1. Tasks with no dependencies are independent root nodes.
    2. Tasks with depends_on are connected to those task IDs.
    3. The builder never creates artificial sequential dependencies.
    4. Unknown dependencies are left disconnected and reported.
    """

    def build(self, tasks):

        graph = WorkflowGraph()

        if not tasks:
            return graph

        # ========================================================
        # CREATE ALL NODES FIRST
        # ========================================================

        for task in tasks:

            node = GraphNode(
                id=task.id,
                task=task,
            )

            graph.add_node(
                node
            )

        # ========================================================
        # CONNECT EXPLICIT DEPENDENCIES
        # ========================================================

        for task in tasks:

            if not task.depends_on:
                continue

            for dependency_id in task.depends_on:

                dependency_id = str(
                    dependency_id
                ).strip()

                if not dependency_id:
                    continue

                parent = graph.get(
                    dependency_id
                )

                if parent is None:

                    print(
                        "WARNING: Unknown task "
                        "dependency:",
                        dependency_id,
                        "for task:",
                        task.id,
                    )

                    continue

                graph.connect(
                    dependency_id,
                    task.id,
                )

        # ========================================================
        # DEBUG GRAPH
        # ========================================================

        print(
            "=" * 60
        )

        print(
            "WORKFLOW GRAPH"
        )

        for node in graph.all_nodes():

            print(
                f"Task: {node.id} | "
                f"Action: {node.task.action} | "
                f"Target: {node.task.target}"
            )

            print(
                "  Depends on:",
                node.task.depends_on,
            )

            print(
                "  Parents:",
                node.parents,
            )

            print(
                "  Children:",
                node.children,
            )

        print(
            "=" * 60
        )

        return graph