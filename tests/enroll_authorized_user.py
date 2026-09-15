from __future__ import annotations

import time

import speech_recognition as sr
import torch

from voice.profile_manager import VoiceProfileManager
from voice.speaker_auth import SpeakerAuth


SAMPLES = 5
THRESHOLD = 0.28


def normalize_embedding(embedding):
    tensor = torch.as_tensor(
        embedding,
        dtype=torch.float32,
    ).detach().cpu()

    tensor = tensor.reshape(-1)

    norm = torch.norm(tensor)

    if norm <= 0:
        raise ValueError(
            "Embedding has zero magnitude."
        )

    return tensor / norm


def record_samples(
    auth: SpeakerAuth,
    display_name: str,
):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    embeddings = []

    print()
    print("=" * 60)
    print("AUTHORIZED VOICE ENROLLMENT")
    print("=" * 60)
    print()
    print(f"Name: {display_name}")
    print(f"Samples required: {SAMPLES}")
    print()
    print(
        "IMPORTANT: the person speaking must be "
        "the person being registered."
    )
    print()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(
            source,
            duration=1,
        )

        for index in range(SAMPLES):
            print()
            print(
                f"[AUTHORIZED] "
                f"Sample {index + 1}/{SAMPLES}"
            )
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
                    print(
                        "❌ Could not create embedding."
                    )
                    continue

                embedding = normalize_embedding(
                    embedding
                )

                embeddings.append(embedding)

                print("✅ Sample captured.")

            except Exception as exc:
                print(
                    f"❌ Capture failed: {exc}"
                )

            time.sleep(0.5)

    return embeddings


def main():
    print("Loading speaker verification model...")

    auth = SpeakerAuth(
        threshold=THRESHOLD
    )

    manager = VoiceProfileManager()

    print()
    print("=" * 60)
    print("AUTHORIZED USER SETUP")
    print("=" * 60)

    user_id = input(
        "Enter user ID "
        "(example: brother_01): "
    ).strip()

    if not user_id:
        print("❌ User ID cannot be empty.")
        return

    display_name = input(
        "Enter display name "
        "(example: Brother): "
    ).strip()

    if not display_name:
        display_name = user_id

    # ---------------------------------------------------------
    # RECORD VOICE
    # ---------------------------------------------------------

    embeddings = record_samples(
        auth,
        display_name,
    )

    if len(embeddings) < 3:
        print()
        print(
            "❌ Enrollment failed. "
            "At least 3 usable samples are required."
        )
        return

    # ---------------------------------------------------------
    # SAVE PROFILE
    # ---------------------------------------------------------

    profile_path = manager.save_allowed_user(
        user_id=user_id,
        embeddings=embeddings,
        display_name=display_name,
    )

    print()
    print("=" * 60)
    print("ENROLLMENT SUCCESSFUL")
    print("=" * 60)
    print()
    print(f"Identity   : AUTHORIZED")
    print(f"User ID    : {user_id}")
    print(f"Name       : {display_name}")
    print(f"Samples    : {len(embeddings)}")
    print(f"Profile    : {profile_path}")
    print()

    # ---------------------------------------------------------
    # SHOW REGISTERED PROFILES
    # ---------------------------------------------------------

    print("=" * 60)
    print("REGISTERED VOICE PROFILES")
    print("=" * 60)

    for profile in manager.list_profiles():
        print(
            f"{profile.get('identity')} | "
            f"{profile.get('user_id')} | "
            f"{profile.get('display_name')} | "
            f"samples={profile.get('sample_count')}"
        )

    print()
    print("✅ Authorized voice is ready.")


if __name__ == "__main__":
    main()