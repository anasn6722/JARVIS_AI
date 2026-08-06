import time
from datetime import datetime

from ai.workflow.scheduled_task import ScheduledTask
from ai.workflow.scheduler_queue import SchedulerQueue


class Scheduler:


    def __init__(self, workflow_manager):

        self.workflow_manager = workflow_manager

        self.queue = SchedulerQueue()

        self.running = False



    def schedule(
        self,
        task,
        delay_seconds=0
    ):

        run_time = (
            datetime.now()
            +
            __import__("datetime")
            .timedelta(
                seconds=delay_seconds
            )
        )


        scheduled = ScheduledTask(
            run_at=run_time,
            task=task,
        )


        self.queue.add(
            scheduled
        )


        return scheduled



    def run_pending(self):


        self.running = True


        while self.running:


            item = self.queue.peek()


            if item is None:

                break



            if item.run_at <= datetime.now():


                item = self.queue.next()


                if not item.cancelled:


                    self.workflow_manager.execute_task(
                        item.task
                    )


                    item.executed = True


            else:

                time.sleep(0.5)



    def stop(self):

        self.running = False