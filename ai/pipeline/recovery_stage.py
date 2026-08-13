from ai.pipeline.context import PipelineContext


class RecoveryStage:
    """Attempt one intelligent recovery after verified failure."""

    def __init__(self, brain):
        self.brain = brain

    def run(self, context: PipelineContext):

        # Only recover failed executions.
        if context.verified:
            return

        if not context.verification_errors:
            return

        # Never allow an uncontrolled recovery loop.
        if context.recovery_attempted:
            return

        context.recovery_attempted = True

        failed_tasks = [
            task
            for task in context.tasks
            if not task.success
        ]

        if not failed_tasks:
            return

        failed_task = failed_tasks[0]

        print("=" * 50)
        print("RECOVERY STAGE")
        print("=" * 50)

        print(
            "Failed action:",
            failed_task.action,
        )

        print(
            "Failed target:",
            failed_task.target,
        )

        print(
            "Failure:",
            failed_task.error,
        )

        recovery_task = (
            self.brain.recovery_manager.recover(
                failed_task
            )
        )

        if recovery_task is None:

            print(
                "No safe recovery available."
            )

            return

        context.recovery_task = recovery_task

        print(
            "Recovery action:",
            recovery_task.action,
        )

        print(
            "Recovery target:",
            recovery_task.target,
        )

        # ----------------------------------------------------
        # Build a graph for the recovery task.
        # ----------------------------------------------------

        recovery_graph = (
            self.brain.graph_builder.build(
                [recovery_task]
            )
        )

        response = (
            self.brain.execution_engine.execute(
                tasks=[recovery_task],
                graph=recovery_graph,
            )
        )

        # ----------------------------------------------------
        # Verify recovery result.
        # ----------------------------------------------------

        if recovery_task.success:

            context.tasks.append(
                recovery_task
            )

            context.graph = recovery_graph

            context.response = response

            context.verification_errors = []

            context.verified = True

            print(
                "RECOVERY SUCCESSFUL"
            )

            return

        # ----------------------------------------------------
        # Recovery failed.
        # ----------------------------------------------------

        context.verification_errors = [
            recovery_task.error
            or str(response)
            or "Recovery action failed."
        ]

        context.verified = False

        print(
            "RECOVERY FAILED"
        )