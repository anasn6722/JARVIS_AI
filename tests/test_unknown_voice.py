import time
import torch
import speech_recognition as sr

from voice.speaker_auth import SpeakerAuth
from voice.profile_manager import VoiceProfileManager
from voice.voice_identity import VoiceIdentity


THRESHOLD = 0.25
TEST_SAMPLES = 8


def normalize_embedding(embedding):
    embedding = torch.as_tensor(
        embedding,
        dtype=torch.float32,
    ).reshape(-1)

    return embedding / (
        torch.norm(embedding) + 1e-8
    )


def cosine_similarity(a, b):
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

    owner_profile = manager.get_profile("OWNER")

    if not owner_profile:
        print("❌ OWNER profile not found.")
        return

    references = owner_profile.get(
        "embeddings",
        []
    )

    references = [
        normalize_embedding(x)
        for x in references
    ]

    if not references:
        print("❌ OWNER embeddings not found.")
        return

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    scores = []

    print()
    print("=" * 60)
    print("UNKNOWN / IMPOSTOR VOICE TEST")
    print("=" * 60)
    print()
    print(
        "IMPORTANT: another person must speak "
        "for all 8 samples."
    )

    with microphone as source:
        recognizer.adjust_for_ambient_noise(
            source,
            duration=1,
        )

        for i in range(TEST_SAMPLES):
            print()
            print(
                f"Unknown speaker sample "
                f"{i + 1}/{TEST_SAMPLES}"
            )

            print("Speak naturally...")

            try:
                audio = recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=6,
                )

                candidate = auth.embedding_from_audio(
                    audio
                )

                if candidate is None:
                    print("❌ Embedding failed.")
                    continue

                candidate = normalize_embedding(
                    candidate
                )

                sample_scores = [
                    cosine_similarity(
                        candidate,
                        reference,
                    )
                    for reference in references
                ]

                best_score = max(sample_scores)

                scores.append(best_score)

                print(
                    f"Score: {best_score:.4f} | "
                    f"{'WOULD PASS' if best_score >= THRESHOLD else 'BLOCK'}"
                )

            except Exception as exc:
                print(f"❌ Failed: {exc}")

            time.sleep(0.5)

    if not scores:
        print("❌ No usable test samples.")
        return

    print()
    print("=" * 60)
    print("IMPOSTOR RESULTS")
    print("=" * 60)

    minimum = min(scores)
    maximum = max(scores)
    average = sum(scores) / len(scores)

    passes = sum(
        score >= THRESHOLD
        for score in scores
    )

    print(f"Minimum : {minimum:.4f}")
    print(f"Maximum : {maximum:.4f}")
    print(f"Average : {average:.4f}")
    print(f"Threshold: {THRESHOLD:.4f}")
    print(f"Would pass: {passes}/{len(scores)}")

    print()
    print("=" * 60)
    print("IDENTITY ENGINE")
    print("=" * 60)

    print(
        "The following tests use the complete "
        "OWNER + AUTHORIZED profile system."
    )

    for i in range(min(3, len(scores))):
        print(
            f"Impostor sample {i + 1}: "
            f"score={scores[i]:.4f}"
        )

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()