from ai.workflow.event_bus import EventBus
from ai.workflow.retry_manager import RetryManager
from ai.workflow.workflow_context import WorkflowContext
from ai.workflow.workflow_event import WorkflowEvent
from ai.workflow.workflow_status import WorkflowStatus


class LinearRunner:

    def __init__(
        self,
        tool_executor,
    ):

        self.tool_executor = tool_executor
        self.events = EventBus()
        self.retry_manager = RetryManager()


    def run(self, tasks):

        context = WorkflowContext(tasks)

        context.status = WorkflowStatus.RUNNING

        self.events.publish(
            WorkflowEvent(
                name="WORKFLOW_STARTED",
                data=context,
            )
        )

        print("=" * 60)
        print("WORKFLOW START")
        print("=" * 60)


        while context.has_next:

            if context.cancelled:

                context.status = WorkflowStatus.CANCELLED

                self.events.publish(
                    WorkflowEvent(
                        name="WORKFLOW_CANCELLED",
                        data=context,
                    )
                )

                break


            task = context.next_task()


            if task is None:
                break


            self.events.publish(
                WorkflowEvent(
                    name="TASK_STARTED",
                    task=task,
                    data=context,
                )
            )


            print(
                f"\nTASK {context.current_index}/{len(context.tasks)}"
            )

            print(
                "Action :",
                task.action,
            )

            print(
                "Target :",
                task.target,
            )


            success = self.execute_task(task)


            task.completed = True
            task.success = success


            if success:

                context.completed.append(task)


                self.events.publish(
                    WorkflowEvent(
                        name="TASK_COMPLETED",
                        task=task,
                        data=context,
                    )
                )


            else:

                context.failed.append(task)

                context.result.errors.append(
                    task.error
                )


                self.events.publish(
                    WorkflowEvent(
                        name="TASK_FAILED",
                        task=task,
                        data=context,
                    )
                )



        if context.status != WorkflowStatus.CANCELLED:


            if context.failed:

                context.status = WorkflowStatus.FAILED

            else:

                context.status = WorkflowStatus.COMPLETED



        self.events.publish(
            WorkflowEvent(
                name="WORKFLOW_FINISHED",
                data=context,
            )
        )


        print("=" * 60)
        print("WORKFLOW COMPLETE")
        print("=" * 60)


        return self.build_result(context)



    def execute_task(self, task):

        while True:

            try:

                result = self.tool_executor.execute(
                    task.action,
                    task.target,
                )


                task.result = result


                print(
                    "Success :",
                    True,
                )

                print(
                    "Result  :",
                    result,
                )


                return True


            except Exception as e:


                task.error = str(e)


                print(
                    f"Attempt {task.retry_count + 1} failed:",
                    e,
                )


                if self.retry_manager.should_retry(task):

                    print("Retrying...")


                    self.retry_manager.retry(task)

                    continue


                print(
                    "Task failed permanently."
                )


                return False



    def build_result(self, context):

        responses = []


        for task in context.completed:

            if task.result:

                responses.append(
                    task.result
                )


        for task in context.failed:

            responses.append(
                f"Failed: {task.action}"
            )


        context.result.success = (
            len(context.failed) == 0
        )


        context.result.completed_tasks = len(
            context.completed
        )


        context.result.failed_tasks = len(
            context.failed
        )


        context.result.response = "\n".join(
            responses
        )


        return context.result.response