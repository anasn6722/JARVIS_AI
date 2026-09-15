from pathlib import Path

import speech_recognition as sr
import torch
from speechbrain.inference.speaker import SpeakerRecognition


class SpeakerAuth:
    """
    Local speaker verification for JARVIS.

    The owner profile is created from multiple voice samples.
    Only the resulting speaker embedding is stored.
    """

    MODEL_SOURCE = (
        "speechbrain/spkrec-ecapa-voxceleb"
    )

    MODEL_DIR = (
        "models/speaker_verification"
    )

    def __init__(
        self,
        profile_path=(
            "voice/voice_profiles/owner.pt"
        ),
        threshold=0.38,
    ):
        self.profile_path = Path(
            profile_path
        )

        self.profile_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.threshold = threshold

        self.verifier = (
            SpeakerRecognition.from_hparams(
                source=self.MODEL_SOURCE,
                savedir=self.MODEL_DIR,
            )
        )

        self.owner_embedding = None

        self._load_profile()

    # =========================================================
    # PROFILE
    # =========================================================

    @property
    def enrolled(self):
        return (
            self.owner_embedding is not None
        )

    def _load_profile(self):

        if not self.profile_path.exists():
            return

        data = torch.load(
            self.profile_path,
            map_location="cpu",
            weights_only=False,
        )

        if isinstance(data, dict):

            self.owner_embedding = (
                data.get("embedding")
            )

        else:

            self.owner_embedding = data

    # =========================================================
    # AUDIO → EMBEDDING
    # =========================================================

    def embedding_from_audio(
        self,
        audio_data,
    ):
        raw = audio_data.get_raw_data(
            convert_rate=16000,
            convert_width=2,
        )

        waveform = torch.frombuffer(
            bytearray(raw),
            dtype=torch.int16,
        ).float()

        if waveform.numel() == 0:
            raise ValueError(
                "Captured audio is empty."
            )

        waveform = (
            waveform / 32768.0
        )

        waveform = waveform.unsqueeze(0)

        embedding = (
            self.verifier.encode_batch(
                waveform
            )
        )

        embedding = (
            embedding
            .detach()
            .cpu()
        )

        # Normalize before storing/comparing.
        embedding = (
            torch.nn.functional.normalize(
                embedding,
                p=2,
                dim=-1,
            )
        )

        return embedding

    # =========================================================
    # MULTI-SAMPLE ENROLLMENT
    # =========================================================

    def enroll_samples(
        self,
        audio_samples,
    ):
        if not audio_samples:
            raise ValueError(
                "No enrollment samples supplied."
            )

        embeddings = []

        for index, audio in enumerate(
            audio_samples,
            start=1,
        ):

            print(
                f"Processing enrollment "
                f"sample {index}/{len(audio_samples)}..."
            )

            embedding = (
                self.embedding_from_audio(
                    audio
                )
            )

            embeddings.append(
                embedding
            )

        # Average multiple samples.
        combined = torch.stack(
            embeddings,
            dim=0,
        ).mean(
            dim=0,
            keepdim=True,
        )

        # Normalize the resulting profile.
        combined = (
            torch.nn.functional.normalize(
                combined,
                p=2,
                dim=-1,
            )
        )

        torch.save(
            {
                "embedding": combined,
                "sample_count": len(
                    embeddings
                ),
            },
            self.profile_path,
        )

        self.owner_embedding = combined

        return {
            "success": True,
            "sample_count": len(
                embeddings
            ),
            "profile": str(
                self.profile_path
            ),
        }

    # =========================================================
    # VERIFY
    # =========================================================

    def verify_audio(
        self,
        audio_data,
    ):
        if not self.enrolled:
            raise RuntimeError(
                "No owner voice is enrolled."
            )

        candidate = (
            self.embedding_from_audio(
                audio_data
            )
        )

        owner = (
            self.owner_embedding.flatten()
        )

        candidate = (
            candidate.flatten()
        )

        score = (
            torch.nn.functional.cosine_similarity(
                owner.unsqueeze(0),
                candidate.unsqueeze(0),
            )
            .item()
        )

        authorized = (
            score >= self.threshold
        )

        return {
            "authorized": authorized,
            "score": score,
            "threshold": self.threshold,
        }


# =============================================================
# MICROPHONE
# =============================================================

def capture_voice(
    prompt,
    phrase_time_limit=6,
):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print()
    print(prompt)

    with microphone as source:

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5,
        )

        print(
            "Listening..."
        )

        audio = recognizer.listen(
            source,
            timeout=8,
            phrase_time_limit=phrase_time_limit,
        )

    print(
        "Audio captured."
    )

    return audio

def embedding_from_audio(
        self,
        audio_data,
    ):
        raw = audio_data.get_raw_data(
            convert_rate=16000,
            convert_width=2,
        )

        waveform = torch.frombuffer(
            bytearray(raw),
            dtype=torch.int16,
        ).float()

        if waveform.numel() == 0:
            raise ValueError(
                "Captured audio is empty."
            )

        waveform = (
            waveform / 32768.0
        )

        waveform = waveform.unsqueeze(0)

        embedding = (
            self.verifier.encode_batch(
                waveform
            )
        )

        embedding = (
            embedding
            .detach()
            .cpu()
        )

        embedding = (
            torch.nn.functional.normalize(
                embedding,
                p=2,
                dim=-1,
            )
        )

        return embedding