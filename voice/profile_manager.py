from __future__ import annotations

from pathlib import Path
from typing import Any

import torch


class VoiceProfileManager:
    """
    Manages local voice identity profiles.

    Each profile stores multiple speaker embeddings.
    This allows VoiceIdentity to compare a live voice against
    several real samples rather than relying on one averaged vector.
    """

    ROOT = Path("voice") / "voice_profiles"
    OWNER_DIR = ROOT / "owner"
    ALLOWED_DIR = ROOT / "allowed"

    def __init__(self):
        self.OWNER_DIR.mkdir(parents=True, exist_ok=True)
        self.ALLOWED_DIR.mkdir(parents=True, exist_ok=True)

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    @staticmethod
    def _normalize_embedding(embedding: torch.Tensor) -> torch.Tensor:
        embedding = torch.as_tensor(
            embedding,
            dtype=torch.float32,
        ).detach().cpu()

        # Flatten old [1, 1, 192] / [1, 192] formats.
        embedding = embedding.reshape(-1)

        norm = torch.norm(embedding)

        if norm <= 0:
            raise ValueError("Embedding has zero magnitude.")

        return embedding / norm

    @classmethod
    def _normalize_embeddings(
        cls,
        embeddings,
    ) -> list[torch.Tensor]:
        if embeddings is None:
            return []

        # A single tensor was supplied.
        if isinstance(embeddings, torch.Tensor):
            tensor = embeddings.detach().cpu()

            # Single embedding.
            if tensor.ndim <= 2:
                return [cls._normalize_embedding(tensor)]

            # Multiple embeddings stacked together.
            tensor = tensor.reshape(-1, tensor.shape[-1])

            return [
                cls._normalize_embedding(item)
                for item in tensor
            ]

        # A Python list/tuple of embeddings.
        if isinstance(embeddings, (list, tuple)):
            result = []

            for item in embeddings:
                try:
                    result.append(
                        cls._normalize_embedding(item)
                    )
                except Exception:
                    continue

            return result

        raise TypeError(
            "Embeddings must be a torch.Tensor, list, or tuple."
        )

    @staticmethod
    def _profile_payload(
        identity: str,
        user_id: str,
        display_name: str,
        embeddings: list[torch.Tensor],
    ) -> dict[str, Any]:
        return {
            "identity": identity,
            "user_id": user_id,
            "display_name": display_name,
            "embeddings": embeddings,
            "sample_count": len(embeddings),
            "version": 2,
        }

    # =========================================================
    # SAVE OWNER
    # =========================================================

    def save_owner(
        self,
        embedding=None,
        embeddings=None,
        display_name: str = "Owner",
    ):
        """
        Save the OWNER profile.

        Preferred:
            embeddings=[embedding1, embedding2, ...]

        Compatibility:
            embedding=single_embedding
        """

        if embeddings is None:
            embeddings = embedding

        normalized = self._normalize_embeddings(
            embeddings
        )

        if not normalized:
            raise ValueError(
                "Cannot save owner profile without embeddings."
            )

        path = self.OWNER_DIR / "profile.pt"

        payload = self._profile_payload(
            identity="OWNER",
            user_id="owner",
            display_name=display_name,
            embeddings=normalized,
        )

        # Also retain a centroid for compatibility/debugging.
        stacked = torch.stack(normalized)
        centroid = torch.mean(stacked, dim=0)
        centroid = self._normalize_embedding(centroid)

        payload["embedding"] = centroid


        # -----------------------------------------------------
        # WINDOWS-SAFE PROFILE SAVE
        # -----------------------------------------------------

        try:
            torch.save(
                payload,
                path,
                _use_new_zipfile_serialization=False,
            )
        except Exception:
            # Remove a possibly corrupted profile.
            try:
                if path.exists():
                    path.unlink()
            except PermissionError:
                pass
            raise

        return path

    # =========================================================
    # SAVE AUTHORIZED USER
    # =========================================================

    def save_allowed_user(
        self,
        user_id: str,
        embedding=None,
        embeddings=None,
        display_name: str | None = None,
    ):
        """
        Save an AUTHORIZED profile using multiple voice samples.
        """

        if not user_id:
            raise ValueError("user_id is required.")

        if embeddings is None:
            embeddings = embedding

        normalized = self._normalize_embeddings(
            embeddings
        )

        if not normalized:
            raise ValueError(
                "Cannot save authorized profile without embeddings."
            )

        if display_name is None:
            display_name = user_id

        user_dir = self.ALLOWED_DIR / user_id
        user_dir.mkdir(parents=True, exist_ok=True)

        path = user_dir / "profile.pt"

        payload = self._profile_payload(
            identity="AUTHORIZED",
            user_id=user_id,
            display_name=display_name,
            embeddings=normalized,
        )

        stacked = torch.stack(normalized)
        centroid = torch.mean(stacked, dim=0)
        centroid = self._normalize_embedding(centroid)

        payload["embedding"] = centroid

        # -----------------------------------------------------
        # WINDOWS-SAFE PROFILE SAVE
        # -----------------------------------------------------

        try:
            torch.save(
                payload,
                path,
                _use_new_zipfile_serialization=False,
            )
        except Exception:
            # Remove a possibly corrupted profile.
            try:
                if path.exists():
                    path.unlink()
            except PermissionError:
                pass
            raise

        return path

    # =========================================================
    # LOAD PROFILE
    # =========================================================

    def load_profile(self, path: str | Path):
        path = Path(path)

        if not path.exists():
            return None

        try:
            profile = torch.load(
                path,
                map_location="cpu",
                weights_only=False,
            )
        except TypeError:
            # Compatibility with older PyTorch versions.
            profile = torch.load(
                path,
                map_location="cpu",
            )

        if not isinstance(profile, dict):
            return None

        return profile

    # =========================================================
    # PROFILE VALIDATION
    # =========================================================

    def validate_profile(self, profile) -> bool:
        if not isinstance(profile, dict):
            return False

        identity = profile.get("identity")

        if identity not in {
            "OWNER",
            "AUTHORIZED",
        }:
            return False

        # New format.
        embeddings = profile.get("embeddings")

        if isinstance(embeddings, (list, tuple)):
            valid_count = 0

            for embedding in embeddings:
                try:
                    normalized = self._normalize_embedding(
                        embedding
                    )

                    if normalized.numel() > 0:
                        valid_count += 1

                except Exception:
                    continue

            return valid_count > 0

        # Compatibility with old single-embedding format.
        embedding = profile.get("embedding")

        if embedding is None:
            return False

        try:
            normalized = self._normalize_embedding(
                embedding
            )
            return normalized.numel() > 0
        except Exception:
            return False

    # =========================================================
    # PROFILE LIST
    # =========================================================

    def list_profiles(self):
        profiles = []

        # OWNER
        owner_path = self.OWNER_DIR / "profile.pt"

        if owner_path.exists():
            profile = self.load_profile(owner_path)

            if self.validate_profile(profile):
                profiles.append(
                    self._profile_summary(
                        profile,
                        owner_path,
                    )
                )

        # AUTHORIZED USERS
        if self.ALLOWED_DIR.exists():
            for user_dir in sorted(
                self.ALLOWED_DIR.iterdir()
            ):
                if not user_dir.is_dir():
                    continue

                profile_path = user_dir / "profile.pt"

                if not profile_path.exists():
                    continue

                profile = self.load_profile(
                    profile_path
                )

                if self.validate_profile(profile):
                    profiles.append(
                        self._profile_summary(
                            profile,
                            profile_path,
                        )
                    )

        return profiles

    # =========================================================
    # GET PROFILE
    # =========================================================

    def get_profile(
        self,
        identity: str,
        user_id: str | None = None,
    ):
        identity = identity.upper()

        if identity == "OWNER":
            path = self.OWNER_DIR / "profile.pt"
            return self.load_profile(path)

        if identity == "AUTHORIZED":
            if not user_id:
                return None

            path = (
                self.ALLOWED_DIR
                / user_id
                / "profile.pt"
            )

            return self.load_profile(path)

        return None

    # =========================================================
    # REMOVE AUTHORIZED USER
    # =========================================================

    def remove_allowed_user(
        self,
        user_id: str,
    ) -> bool:
        if not user_id:
            return False

        user_dir = self.ALLOWED_DIR / user_id

        if not user_dir.exists():
            return False

        for child in user_dir.iterdir():
            if child.is_file():
                child.unlink()

        user_dir.rmdir()

        return True

    # =========================================================
    # SUMMARY
    # =========================================================

    def _profile_summary(
        self,
        profile,
        path: Path,
    ):
        embeddings = profile.get("embeddings")

        if isinstance(embeddings, (list, tuple)):
            sample_count = len(
                [
                    item
                    for item in embeddings
                    if item is not None
                ]
            )
        else:
            sample_count = int(
                profile.get("sample_count", 1)
            )

        return {
            "identity": profile.get(
                "identity",
                "UNKNOWN",
            ),
            "user_id": profile.get(
                "user_id",
                "",
            ),
            "display_name": profile.get(
                "display_name",
                "",
            ),
            "sample_count": sample_count,
            "path": str(path),
            "version": profile.get(
                "version",
                1,
            ),
        }