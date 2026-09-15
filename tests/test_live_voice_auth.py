from voice.speaker_auth import SpeakerAuth, capture_voice


def main():
    auth = SpeakerAuth(threshold=0.38)

    print()
    print("========================================")
    print(" JARVIS LIVE VOICE AUTH TEST")
    print("========================================")
    print()
    print("Speak naturally.")
    print("The command will NOT be sent to JARVIS.")
    print()

    audio = capture_voice(
        "Speak now."
    )

    result = auth.verify_audio(audio)

    print()
    print("========================================")
    print(" VOICE AUTH RESULT")
    print("========================================")
    print(
        "Authorized:",
        result["authorized"],
    )
    print(
        "Score:",
        f"{result['score']:.4f}",
    )
    print(
        "Threshold:",
        result["threshold"],
    )

    if result["authorized"]:
        print()
        print("✅ OWNER VERIFIED")
    else:
        print()
        print("❌ VOICE REJECTED")


if __name__ == "__main__":
    main()
