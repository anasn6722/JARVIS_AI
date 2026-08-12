from ai.pipeline.ai_stage import AIStage
from ai.pipeline.command_stage import CommandStage
from ai.pipeline.execution_stage import ExecutionStage
from ai.pipeline.memory_stage import MemoryStage
from ai.pipeline.planning_stage import PlanningStage
from ai.pipeline.reasoning_stage import ReasoningStage
from ai.pipeline.response_stage import ResponseStage


class Pipeline:

    def __init__(self, brain):

        self.stages = [
            MemoryStage(brain),
            CommandStage(brain),
            ReasoningStage(brain),
            PlanningStage(brain),
            ExecutionStage(brain),
            ResponseStage(brain),
            AIStage(brain),
        ]

    def run(self, context):

        print("\n===== PIPELINE START =====")

        for stage in self.stages:

            print(
                f"Running: {stage.__class__.__name__}"
            )

            stage.run(context)

            if context.stop:
                print("Pipeline stopped.")
                break

        print("===== PIPELINE END =====\n")