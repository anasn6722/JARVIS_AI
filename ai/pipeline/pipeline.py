from ai.pipeline.ai_stage import AIStage
from ai.pipeline.command_stage import CommandStage
from ai.pipeline.execution_stage import ExecutionStage
from ai.pipeline.memory_stage import MemoryStage
from ai.pipeline.planning_stage import PlanningStage
from ai.pipeline.reasoning_stage import ReasoningStage
from ai.pipeline.recovery_stage import RecoveryStage
from ai.pipeline.response_stage import ResponseStage
from ai.pipeline.verification_stage import VerificationStage
from core.hud_state import hud_state


class Pipeline:
    """
    Central JARVIS execution pipeline.

    Besides running the AI stages, this class publishes live
    execution telemetry to HudState so the GUI can display:

        COMMAND
        REASONING
        PLANNER
        EXECUTION
        VERIFICATION
        RESPONSE
    """

    STAGE_DEFINITIONS = (
        (
            MemoryStage,
            "COMMAND",
            "CONTEXT INITIALIZATION",
        ),
        (
            CommandStage,
            "COMMAND",
            "COMMAND PARSING",
        ),
        (
            ReasoningStage,
            "REASONING",
            "INTENT ANALYSIS",
        ),
        (
            PlanningStage,
            "PLANNER",
            "TASK PLANNING",
        ),
        (
            AIStage,
            "REASONING",
            "AI PROCESSING",
        ),
        (
            ExecutionStage,
            "EXECUTION",
            "TASK EXECUTION",
        ),
        (
            VerificationStage,
            "VERIFICATION",
            "RESULT VERIFICATION",
        ),
        (
            RecoveryStage,
            "EXECUTION",
            "RECOVERY",
        ),
        (
            ResponseStage,
            "RESPONSE",
            "RESPONSE GENERATION",
        ),
    )

    def __init__(self, brain):

        self.brain = brain

        self.stages = [
            stage_class(brain)
            for stage_class, _, _ in self.STAGE_DEFINITIONS
        ]

    # =========================================================
    # RUN
    # =========================================================

    def run(self, context):

        print("\n===== PIPELINE START =====")

        total_stages = len(
            self.STAGE_DEFINITIONS
        )

        # -----------------------------------------------------
        # INITIAL HUD STATE
        # -----------------------------------------------------

        self._publish(
            state="COMMAND",
            event="PIPELINE_STARTED",
            progress=0,
            context=context,
        )

        # -----------------------------------------------------
        # STAGE LOOP
        # -----------------------------------------------------

        for index, (
            stage,
            definition,
        ) in enumerate(
            zip(
                self.stages,
                self.STAGE_DEFINITIONS,
            )
        ):
        
            stage_state = definition[1]
            stage_event = definition[2]
        
            stage_number = index + 1
        
            start_progress = int(
                (
                    index
                    / total_stages
                )
                * 100
            )
        
            end_progress = int(
                (
                    stage_number
                    / total_stages
                )
                * 100
            )
        
            print(
                f"Running: {stage.__class__.__name__}"
            )
        
            # =================================================
            # BEFORE STAGE
            # =================================================
        
            self._publish(
                state=stage_state,
                event=stage_event,
                progress=start_progress,
                context=context,
            )
        
            # =================================================
            # RUN STAGE
            # =================================================
        
            try:
            
                stage.run(context)
        
            except Exception as error:
            
                print(
                    f"Stage failed: "
                    f"{stage.__class__.__name__}"
                )
        
                print(
                    "ERROR:",
                    error,
                )
        
                context.verification_errors.append(
                    str(error)
                )
        
                self._publish(
                    state="ERROR",
                    event=(
                        f"{stage.__class__.__name__}"
                        "_FAILED"
                    ),
                    progress=start_progress,
                    context=context,
                    result=str(error),
                )
        
                break
            
            # =================================================
            # AFTER STAGE
            # =================================================
        
            self._publish(
                state=stage_state,
                event=f"{stage_event}_COMPLETE",
                progress=end_progress,
                context=context,
            )
        
            # =================================================
            # STOP
            # =================================================
        
            if context.stop:
            
                self._publish(
                    state="RESPONSE",
                    event="RESPONSE_READY",
                    progress=100,
                    context=context,
                    result=context.response,
                )
        
                print(
                    "Pipeline stopped."
                )
        
                break

        else:

            # -------------------------------------------------
            # NORMAL COMPLETION
            # -------------------------------------------------

            self._publish(
                state="RESPONSE",
                event="PIPELINE_COMPLETE",
                progress=100,
                context=context,
                result=context.response,
            )

        print(
            "===== PIPELINE END =====\n"
        )

    # =========================================================
    # HUD PUBLISHER
    # =========================================================

    def _publish(
        self,
        *,
        state,
        event,
        progress,
        context,
        result=None,
    ):
        """
        Publish a thread-safe snapshot to HudState.

        The GUI polls HudState independently, so this method
        never touches Qt widgets directly.
        """

        action, target = (
            self._extract_action_target(
                context
            )
        )

        if result is None:

            result = getattr(
                context,
                "response",
                None,
            )

        hud_state.update(
            state=state,
            event=event,
            action=action,
            target=target,
            result=(
                str(result)
                if result is not None
                else ""
            ),
            progress=progress,
            completed=progress,
            total=100,
        )

        print(
            "HUD:",
            state,
            "|",
            event,
            "| action=",
            action,
            "| target=",
            target,
            "| progress=",
            progress,
        )

    # =========================================================
    # ACTION / TARGET
    # =========================================================

    @staticmethod
    def _extract_action_target(
        context,
    ):
        """
        Extract the most useful action and target for the HUD.
        """

        action = ""
        target = ""

        # -----------------------------------------------------
        # CURRENT COMMAND
        # -----------------------------------------------------

        command = getattr(
            context,
            "current_command",
            None,
        )

        if command is not None:

            action = str(
                getattr(
                    command,
                    "intent",
                    "",
                )
                or ""
            )

            original = str(
                getattr(
                    command,
                    "original",
                    "",
                )
                or ""
            )

            if not target and original:

                target = original

        # -----------------------------------------------------
        # PARSED COMMANDS
        # -----------------------------------------------------

        commands = getattr(
            context,
            "commands",
            [],
        )

        if commands:

            last_item = commands[-1]

            if isinstance(
                last_item,
                dict,
            ):

                command = last_item.get(
                    "command"
                )

                if command is not None:

                    if not action:

                        action = str(
                            getattr(
                                command,
                                "intent",
                                "",
                            )
                            or ""
                        )

                    original = str(
                        getattr(
                            command,
                            "original",
                            "",
                        )
                        or ""
                    )

                    if original:

                        target = original

        # -----------------------------------------------------
        # EXECUTION TASKS
        # -----------------------------------------------------

        tasks = getattr(
            context,
            "tasks",
            [],
        )

        if tasks:

            for task in reversed(
                tasks
            ):

                task_action = str(
                    getattr(
                        task,
                        "action",
                        "",
                    )
                    or ""
                )

                task_target = str(
                    getattr(
                        task,
                        "target",
                        "",
                    )
                    or ""
                )

                if task_action:

                    action = (
                        task_action
                    )

                if task_target:

                    target = (
                        task_target
                    )

                if (
                    task_action
                    or task_target
                ):
                    break

        # -----------------------------------------------------
        # NORMALIZE
        # -----------------------------------------------------

        if not action:

            action = ""

        if not target:

            target = ""

        return (
            action,
            target,
        )