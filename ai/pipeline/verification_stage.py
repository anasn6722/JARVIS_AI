class VerificationStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        # Normal AI conversation does not have executable tasks.
        if not context.tasks:
            context.verified = True
            return

        errors = []

        for task in context.tasks:

            if task.success:
                continue

            error = task.error or (
                f"Task failed: {task.action}"
            )

            errors.append(error)

        context.verification_errors = errors
        context.verified = not errors

        if errors:
            print("=" * 50)
            print("VERIFICATION FAILED")
            print("=" * 50)

            for error in errors:
                print(error)

        else:
            print("=" * 50)
            print("VERIFICATION PASSED")
            print("=" * 50)