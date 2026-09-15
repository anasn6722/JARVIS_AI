import time

import speech_recognition as sr
import torch

from voice.profile_manager import VoiceProfileManager
from voice.speaker_auth import SpeakerAuth
from voice.voice_identity import VoiceIdentity

ENROLL_SAMPLES = 5
TEST_SAMPLES = 8
THRESHOLD = 0.25


def record_embeddings(
    auth,
    label,
    count,
):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    embeddings = []

    print()
    print("=" * 60)
    print(f"{label}")
    print(f"{count} samples")
    print("=" * 60)

    with microphone as source:
        recognizer.adjust_for_ambient_noise(
            source,
            duration=1,
        )

        for i in range(count):
            print()
            print(f"Sample {i + 1}/{count}")
            print("Speak naturally...")

            try:
                audio = recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=6,
                )

                embedding = auth.embedding_from_audio(
                    audio
                )

                if embedding is None:
                    print("❌ Embedding failed.")
                    continue

                embedding = torch.as_tensor(
                    embedding,
                    dtype=torch.float32,
                ).reshape(-1)

                embedding = embedding / (
                    torch.norm(embedding) + 1e-8
                )

                embeddings.append(embedding)

                print("✅ Captured.")

            except Exception as exc:
                print(f"❌ Failed: {exc}")

            time.sleep(0.5)

    return embeddings


def cosine(a, b):
    return torch.nn.functional.cosine_similarity(
        a.unsqueeze(0),
        b.unsqueeze(0),
        dim=1,
    ).item()


def main():
    print("Loading speaker verification model...")

    auth = SpeakerAuth(
        threshold=THRESHOLD
    )

    manager = VoiceProfileManager()

    identity = VoiceIdentity(
        manager,
        threshold=THRESHOLD,
    )

    # ========================================================
    # FRESH OWNER ENROLLMENT
    # ========================================================

    owner_samples = record_embeddings(
        auth,
        "OWNER ENROLLMENT",
        ENROLL_SAMPLES,
    )

    if len(owner_samples) < 3:
        print("❌ Not enough owner samples.")
        return

    manager.save_owner(
        embeddings=owner_samples,
        display_name="Owner",
    )

    print()
    print(
        f"✅ Owner profile saved with "
        f"{len(owner_samples)} samples."
    )

    # ========================================================
    # OWNER LIVE TESTS
    # ========================================================

    test_samples = record_embeddings(
        auth,
        "OWNER LIVE CONSISTENCY TEST",
        TEST_SAMPLES,
    )

    if not test_samples:
        print("❌ No test samples.")
        return

    profile = manager.get_profile("OWNER")

    references = profile.get(
        "embeddings",
        [],
    )

    references = [
        torch.as_tensor(
            x,
            dtype=torch.float32,
        ).reshape(-1)
        for x in references
    ]

    print()
    print("=" * 60)
    print("OWNER CONSISTENCY RESULTS")
    print("=" * 60)

    scores = []

    for i, candidate in enumerate(
        test_samples,
        start=1,
    ):
        sample_scores = [
            cosine(candidate, reference)
            for reference in references
        ]

        best = max(sample_scores)

        scores.append(best)

        print(
            f"Test {i}: "
            f"score={best:.4f} "
            f"{'PASS' if best >= THRESHOLD else 'FAIL'}"
        )

    print()
    print("-" * 60)

    minimum = min(scores)
    maximum = max(scores)
    average = sum(scores) / len(scores)

    print(f"Minimum : {minimum:.4f}")
    print(f"Maximum : {maximum:.4f}")
    print(f"Average : {average:.4f}")
    print(f"Threshold: {THRESHOLD:.4f}")

    passed = sum(
        score >= THRESHOLD
        for score in scores
    )

    print(
        f"Passed  : {passed}/{len(scores)}"
    )

    # ========================================================
    # IDENTITY CHECK
    # ========================================================

    print()
    print("=" * 60)
    print("IDENTITY ENGINE CHECK")
    print("=" * 60)

    for i, candidate in enumerate(
        test_samples,
        start=1,
    ):
        result = identity.identify(
            candidate
        )

        print(
            f"Test {i}: "
            f"{result['identity']} | "
            f"score={result['score']:.4f} | "
            f"authorized={result['authorized']}"
        )

    print()
    print("=" * 60)
    print("CALIBRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()