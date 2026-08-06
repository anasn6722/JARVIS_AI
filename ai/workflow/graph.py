from ai.workflow.graph_node import GraphNode


class WorkflowGraph:

    def __init__(self):

        self.nodes = {}

    def add_node(self,node):

        self.nodes[node.id] = node

    def connect(self,parent,child):

        self.nodes[parent].children.append(child)

        self.nodes[child].parents.append(parent)

    def get(self,node_id):

        return self.nodes[node_id]