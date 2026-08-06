from dataclasses import dataclass

from ai.agent.goal import Goal
from ai.planning.goal_graph import GoalGraph


@dataclass
class GoalPlan:

    goal: Goal

    graph: GoalGraph

    success: bool = True