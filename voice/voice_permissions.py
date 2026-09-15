from __future__ import annotations


OWNER = "OWNER"
AUTHORIZED = "AUTHORIZED"
UNKNOWN = "UNKNOWN"


class VoicePermissions:
    """
    Maps voice identities to command permissions.
    """

    OWNER_ONLY = {
        "enroll_voice",
        "add_authorized_voice",
        "remove_authorized_voice",
        "list_authorized_voices",
        "lock_voice_access",
        "unlock_voice_access",
        "change_voice_threshold",
        "delete_files",
        "shutdown",
        "restart",
    }

    NORMAL_COMMANDS = {
        "open",
        "close",
        "keyboard",
        "mouse",
        "search",
        "youtube",
        "time",
        "chat",
        "ui",
        "window",
    }

    @classmethod
    def can_execute(
        cls,
        identity: str,
        command_category: str,
    ) -> bool:

        identity = str(identity).upper().strip()
        command_category = (
            str(command_category)
            .lower()
            .strip()
        )

        # Unknown voices get no command access.
        if identity == UNKNOWN:
            return False

        # Owner has full normal permissions.
        if identity == OWNER:
            return True

        # Authorized users cannot perform owner-only actions.
        if identity == AUTHORIZED:
            return (
                command_category
                not in cls.OWNER_ONLY
            )

        return False

    @classmethod
    def is_owner(cls, identity: str) -> bool:
        return (
            str(identity).upper().strip()
            == OWNER
        )

    @classmethod
    def is_authorized(cls, identity: str) -> bool:
        return (
            str(identity).upper().strip()
            in {
                OWNER,
                AUTHORIZED,
            }
        )