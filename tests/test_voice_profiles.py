from voice.profile_manager import (
    VoiceProfileManager,
)
from voice.speaker_auth import (
    SpeakerAuth,
    capture_voice,
)
from voice.voice_identity import (
    VoiceIdentity,
)


def main():

    print(
        "========================================"
    )
    print(
        " JARVIS VOICE PROFILE TEST"
    )
    print(
        "========================================"
    )

    profile_manager = (
        VoiceProfileManager()
    )

    auth = SpeakerAuth(
        threshold=0.38
    )

    identity = VoiceIdentity(
        profile_manager=profile_manager,
        threshold=0.38,
    )

    # =========================================================
    # OWNER
    # =========================================================

    print()
    print(
        "Creating owner embedding..."
    )

    owner_audio = capture_voice(
        "OWNER: speak now."
    )

    owner_embedding = (
        auth.embedding_from_audio(
            owner_audio
        )
    )

    path = (
        profile_manager.save_owner(
            owner_embedding,
            display_name="Owner",
        )
    )

    print(
        "Owner profile:",
        path,
    )

    # =========================================================
    # AUTHORIZED USER
    # =========================================================

    print()
    print(
        "Now enroll an authorized user."
    )

    print(
        "This must be a DIFFERENT person."
    )

    user_audio = capture_voice(
        "AUTHORIZED USER: speak now."
    )

    user_embedding = (
        auth.embedding_from_audio(
            user_audio
        )
    )

    user_path = (
        profile_manager.save_allowed_user(
            "user_01",
            user_embedding,
            display_name="Authorized User",
        )
    )

    print(
        "Authorized-user profile:",
        user_path,
    )

    # =========================================================
    # LIST
    # =========================================================

    print()
    print(
        "Registered profiles:"
    )

    for profile in (
        profile_manager.list_profiles()
    ):

        print(
            " -",
            profile["identity"],
            "|",
            profile["user_id"],
            "|",
            profile["display_name"],
        )

    # =========================================================
    # OWNER TEST
    # =========================================================

    print()
    print(
        "OWNER VERIFICATION"
    )

    audio = capture_voice(
        "Owner: speak now."
    )

    embedding = (
        auth.embedding_from_audio(
            audio
        )
    )

    result = (
        identity.identify(
            embedding
        )
    )

    print(
        "Identity:",
        result["identity"],
    )

    print(
        "User ID:",
        result["user_id"],
    )

    print(
        "Score:",
        f"{result['score']:.4f}",
    )

    print(
        "Authorized:",
        result["authorized"],
    )

    # =========================================================
    # AUTHORIZED USER TEST
    # =========================================================

    print()
    print(
        "AUTHORIZED USER VERIFICATION"
    )

    audio = capture_voice(
        "Authorized user: speak now."
    )

    embedding = (
        auth.embedding_from_audio(
            audio
        )
    )

    result = (
        identity.identify(
            embedding
        )
    )

    print(
        "Identity:",
        result["identity"],
    )

    print(
        "User ID:",
        result["user_id"],
    )

    print(
        "Score:",
        f"{result['score']:.4f}",
    )

    print(
        "Authorized:",
        result["authorized"],
    )

    # =========================================================
    # UNKNOWN TEST
    # =========================================================

    print()
    print(
        "UNKNOWN SPEAKER VERIFICATION"
    )

    print(
        "Use a THIRD person if available."
    )

    audio = capture_voice(
        "Unknown speaker: speak now."
    )

    embedding = (
        auth.embedding_from_audio(
            audio
        )
    )

    result = (
        identity.identify(
            embedding
        )
    )

    print(
        "Identity:",
        result["identity"],
    )

    print(
        "User ID:",
        result["user_id"],
    )

    print(
        "Score:",
        f"{result['score']:.4f}",
    )

    print(
        "Authorized:",
        result["authorized"],
    )


if __name__ == "__main__":
    main()