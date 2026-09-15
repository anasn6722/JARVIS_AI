import time

import speech_recognition as sr
import torch

from voice.profile_manager import VoiceProfileManager
from voice.speaker_auth import SpeakerAuth
from voice.voice_identity import VoiceIdentity

SAMPLES_PER_PERSON = 5
THRESHOLD = 0.38


def normalize_embedding(embedding: torch.Tensor) -> torch.Tensor:
    return embedding / (torch.norm(embedding) + 1e-8)


def record_samples(auth: SpeakerAuth, label: str, count: int):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    samples = []

    print()
    print("=" * 60)
    print(f"RECORDING VOICE PROFILE: {label}")
    print(f"{count} samples required")
    print("=" * 60)

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        for i in range(count):
            print()
            print(f"[{label}] Sample {i + 1}/{count}")
            print("Speak naturally...")

            try:
                audio = recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=6,
                )

                embedding = auth.embedding_from_audio(audio)

                if embedding is None:
                    print("❌ Could not create embedding.")
                    continue

                samples.append(embedding.squeeze())
                print("✅ Sample captured.")

            except Exception as exc:
                print(f"❌ Capture failed: {exc}")

            time.sleep(0.5)

    return samples




def enroll_profile(
    manager: VoiceProfileManager,
    profile_type: str,
    samples,
    user_id: str | None = None,
    display_name: str = "User",
):
    if not samples:
        print(f"❌ No usable samples for {display_name}.")
        return False

    if profile_type == "owner":
        manager.save_owner(
            embeddings=samples,
            display_name=display_name,
        )
    else:
        manager.save_allowed_user(
            user_id=user_id,
            embeddings=samples,
            display_name=display_name,
        )

    print(f"✅ Saved {display_name} profile using {len(samples)} samples.")
    return True


def test_identity(
    auth: SpeakerAuth,
    identity: VoiceIdentity,
    label: str,
):
    recognizer = sr.Recognizer()

    print()
    print("=" * 60)
    print(f"LIVE TEST: {label}")
    print("=" * 60)

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Speak now...")
        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=6,
        )

    candidate = auth.embedding_from_audio(audio)

    if candidate is None:
        print("❌ Could not create test embedding.")
        return

    result = identity.identify(candidate)

    print()
    print("IDENTITY RESULT")
    print("-" * 40)
    print(f"Identity   : {result.get('identity')}")
    print(f"Score      : {result.get('score')}")
    print(f"Authorized : {result.get('authorized')}")
    print(f"Threshold  : {result.get('threshold')}")


def main():
    print("Loading speaker verification model...")

    auth = SpeakerAuth(threshold=THRESHOLD)
    manager = VoiceProfileManager()
    identity = VoiceIdentity(manager, threshold=THRESHOLD)

    # ---------------------------------------------------------
    # OWNER
    # ---------------------------------------------------------
    owner_samples = record_samples(
        auth,
        "OWNER",
        SAMPLES_PER_PERSON,
    )

    enroll_profile(
        manager,
        profile_type="owner",
        samples=owner_samples,
        display_name="Owner",
    )

    # ---------------------------------------------------------
    # AUTHORIZED USER
    # ---------------------------------------------------------
    authorized_samples = record_samples(
        auth,
        "AUTHORIZED USER",
        SAMPLES_PER_PERSON,
    )

    enroll_profile(
        manager,
        profile_type="allowed",
        samples=authorized_samples,
        user_id="authorized_01",
        display_name="Authorized User",
    )

    # ---------------------------------------------------------
    # SHOW PROFILES
    # ---------------------------------------------------------
    print()
    print("=" * 60)
    print("REGISTERED PROFILES")
    print("=" * 60)

    profiles = manager.list_profiles()

    for profile in profiles:
        print(
            f"{profile['identity']} | "
            f"{profile['user_id']} | "
            f"{profile['display_name']} | "
            f"samples={profile['sample_count']}"
        )

    # ---------------------------------------------------------
    # TEST OWNER
    # ---------------------------------------------------------
    test_identity(
        auth,
        identity,
        "OWNER",
    )

    # ---------------------------------------------------------
    # TEST AUTHORIZED USER
    # ---------------------------------------------------------
    test_identity(
        auth,
        identity,
        "AUTHORIZED USER",
    )

    # ---------------------------------------------------------
    # TEST UNKNOWN
    # ---------------------------------------------------------
    test_identity(
        auth,
        identity,
        "UNKNOWN PERSON",
    )

    print()
    print("=" * 60)
    print("MULTI-SAMPLE PROFILE TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()