from voice.speaker_auth import (
    SpeakerAuth,
    capture_voice,
)


def main():

    auth = SpeakerAuth()

    print(
        "========================================"
    )
    print(
        " JARVIS UNKNOWN VOICE TEST"
    )
    print(
        "========================================"
    )

    if not auth.enrolled:
        print(
            "ERROR: Owner profile does not exist."
        )
        return

    print()
    print(
        "IMPORTANT:"
    )
    print(
        "Have a DIFFERENT person speak."
    )

    print(
        "Do not use the owner's voice."
    )

    results = []

    for index in range(1, 4):

        print()
        print(
            f"--- UNKNOWN TEST {index}/3 ---"
        )

        audio = capture_voice(
            "Unauthorized speaker: speak now."
        )

        result = auth.verify_audio(
            audio
        )

        results.append(
            result["score"]
        )

        print(
            "Authorized:",
            result["authorized"],
        )

        print(
            "Score:",
            f"{result['score']:.4f}",
        )

    print()
    print(
        "========================================"
    )
    print(
        " UNKNOWN VOICE SUMMARY"
    )
    print(
        "========================================"
    )

    print(
        "Minimum:",
        f"{min(results):.4f}",
    )

    print(
        "Maximum:",
        f"{max(results):.4f}",
    )

    print(
        "Average:",
        f"{sum(results) / len(results):.4f}",
    )

    print(
        "Current threshold:",
        auth.threshold,
    )


if __name__ == "__main__":
    main()