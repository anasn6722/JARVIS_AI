from dataclasses import dataclass, field

from ai.agent.task import Task


@dataclass
class GoalNode:

    task: Task

    parents: list["GoalNode"] = field(default_factory=list)

    children: list["GoalNode"] = field(default_factory=list)

    completed: bool = False

    failed: bool = False

    blocked: bool = False

    def add_child(self, node: "GoalNode"):

        self.children.append(node)

        node.parents.append(self)

    @property
    def ready(self):

        return all(parent.completed for parent in self.parents)

    def __repr__(self):

        return (
            f"GoalNode("
            f"{self.task.action}:"
            f"{self.task.target}"
            f")"
        )