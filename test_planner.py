from ai.agent.planner import Planner

planner = Planner()

tasks = planner.plan(
    "open chrome then search python classes and tell me the time"
)

for task in tasks:
    print(task)