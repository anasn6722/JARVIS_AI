from datetime import datetime
from uuid import uuid4

from ai.agent.goal_state import GoalState
from ai.agent.goal_state_controller import GoalStateController
from ai.memory.goal_record import GoalRecord


class GoalManager:

    def __init__(self, goal_memory):
        self.goal_memory = goal_memory
        self.state_controller = GoalStateController()

    # -------------------------
    # Create Goal
    # -------------------------

    def create_goal(self, title, tasks):

        goal = GoalRecord(
            id=str(uuid4()),
            title=title,
            created=datetime.now(),
            tasks=tasks,
            state=GoalState.PENDING,
        )

        self.goal_memory.add(goal)

        return goal

    # -------------------------
    # Read
    # -------------------------

    def get_goal(self, goal_id):

        return self.goal_memory.get(goal_id)

    def all_goals(self):

        return self.goal_memory.all()

    # -------------------------
    # Delete
    # -------------------------

    def delete_goal(self, goal_id):

        self.goal_memory.remove(goal_id)

    # -------------------------
    # Progress
    # -------------------------

        def update_progress(self, goal):
            if not goal.tasks: 
                goal.progress = 100.0 
                goal.completed = True 
                goal.paused = False 
                goal.state = GoalState.COMPLETED 
                self.goal_memory.save() 
                return 
            completed = sum( task.completed for task in goal.tasks ) 
            goal.progress = ( completed / len(goal.tasks) ) * 100.0 
            if completed == len(goal.tasks): 
                goal.completed = True 
                goal.paused = False 
                goal.state = GoalState.COMPLETED 
            elif completed > 0: 
                goal.completed = False 
                if not goal.paused: 
                    goal.state = GoalState.RUNNING 
                else: 
                    goal.completed = False 

                    if not goal.paused: 
                        goal.state = GoalState.PENDING 
                self.goal_memory.save()

    # -------------------------
    # Next Task
    # -------------------------

    def next_task(self, goal):

        for task in goal.tasks:

            if not task.completed:

                return task

        return None

    # ============================================================
    # STATE
    # ============================================================
    
    def get_state(self, goal_id):
        goal = self.get_goal(goal_id)
    
        if goal is None:
            return None
    
        return self.state_controller.get_state(goal)
    
    
    # ============================================================
    # START
    # ============================================================
    
    def start_goal(self, goal_id):
        goal = self.get_goal(goal_id)
    
        if goal is None:
            return False, "Goal not found."
    
        result = self.state_controller.start(goal)
    
        self.goal_memory.save()
    
        return result
    
    
    # ============================================================
    # PAUSE
    # ============================================================
    
    def pause_goal(self, goal_id):
        goal = self.get_goal(goal_id)
    
        if goal is None:
            return False, "Goal not found."
    
        result = self.state_controller.pause(goal)
    
        self.goal_memory.save()
    
        return result
    
    
    # ============================================================
    # RESUME
    # ============================================================
    
    def resume_goal(self, goal_id):
        goal = self.get_goal(goal_id)
    
        if goal is None:
            return False, "Goal not found."
    
        result = self.state_controller.resume(goal)
    
        self.goal_memory.save()
    
        return result
    
    
    # ============================================================
    # COMPLETE
    # ============================================================
    
    def complete_goal(self, goal_id):
        goal = self.get_goal(goal_id)
    
        if goal is None:
            return False, "Goal not found."
    
        result = self.state_controller.complete(goal)
    
        self.goal_memory.save()
    
        return result
    
    
    # ============================================================
    # ARCHIVE
    # ============================================================
    
    def archive_goal(self, goal_id):
        goal = self.get_goal(goal_id)
    
        if goal is None:
            return False, "Goal not found."
    
        result = self.state_controller.archive(goal)
    
        self.goal_memory.save()
    
        return result
    
    
    # ============================================================
    # RESTORE
    # ============================================================
    
    def restore_goal(self, goal_id):
        goal = self.get_goal(goal_id)
    
        if goal is None:
            return False, "Goal not found."
    
        result = self.state_controller.restore(goal)
    
        self.goal_memory.save()
    
        return result