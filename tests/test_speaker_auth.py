from voice.speaker_auth import (
    SpeakerAuth,
    capture_voice,
)

SAMPLE_COUNT = 5


def main():

    auth = SpeakerAuth()

    print(
        "========================================"
    )
    print(
        " JARVIS VOICE CALIBRATION"
    )
    print(
        "========================================"
    )

    samples = []

    # ---------------------------------------------------------
    # OWNER ENROLLMENT
    # ---------------------------------------------------------

    print()
    print(
        f"We need {SAMPLE_COUNT} voice samples."
    )

    print(
        "Speak naturally and use a different sentence"
    )
    print(
        "for each sample."
    )

    for index in range(
        1,
        SAMPLE_COUNT + 1,
    ):

        print()
        print(
            f"--- OWNER SAMPLE "
            f"{index}/{SAMPLE_COUNT} ---"
        )

        audio = capture_voice(
            f"Sample {index}: speak now."
        )

        samples.append(
            audio
        )

    result = auth.enroll_samples(
        samples
    )

    print()
    print(
        "========================================"
    )
    print(
        " OWNER PROFILE CREATED"
    )
    print(
        "========================================"
    )

    print(
        "Samples:",
        result["sample_count"],
    )

    print(
        "Profile:",
        result["profile"],
    )

    # ---------------------------------------------------------
    # OWNER VERIFICATION TEST
    # ---------------------------------------------------------

    print()
    print(
        "Now perform 3 verification tests"
    )
    print(
        "using natural sentences."
    )

    owner_scores = []

    for index in range(1, 4):

        print()
        print(
            f"--- OWNER TEST {index}/3 ---"
        )

        audio = capture_voice(
            "Speak now."
        )

        result = auth.verify_audio(
            audio
        )

        owner_scores.append(
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
        " OWNER VERIFICATION SUMMARY"
    )
    print(
        "========================================"
    )

    print(
        "Minimum:",
        f"{min(owner_scores):.4f}",
    )

    print(
        "Maximum:",
        f"{max(owner_scores):.4f}",
    )

    print(
        "Average:",
        f"{sum(owner_scores) / len(owner_scores):.4f}",
    )

    print(
        "Current threshold:",
        auth.threshold,
    )

    print()
    print(
        "Do NOT connect this profile to live JARVIS"
    )
    print(
        "until we test an unauthorized voice too."
    )


if __name__ == "__main__":
    main()