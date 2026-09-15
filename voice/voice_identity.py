from __future__ import annotations

import torch
import torch.nn.functional as F

from voice.profile_manager import VoiceProfileManager


class VoiceIdentity:
    """
    Identifies a speaker against OWNER and AUTHORIZED
    voice profiles.

    Each profile may contain multiple voice embeddings.

    Instead of trusting only one enrollment sample, the
    identity score is calculated from the average of the
    three strongest matching samples.
    """

    def __init__(
        self,
        profile_manager: VoiceProfileManager | None = None,
        threshold: float = 0.28,
    ):
        self.profile_manager = (
            profile_manager
            or VoiceProfileManager()
        )

        self.threshold = float(threshold)

    # =========================================================
    # NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize(
        embedding,
    ) -> torch.Tensor:
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

    # =========================================================
    # EXTRACT PROFILE EMBEDDINGS
    # =========================================================

    def _get_profile_embeddings(
        self,
        profile,
    ) -> list[torch.Tensor]:
        if not isinstance(profile, dict):
            return []

        embeddings = profile.get(
            "embeddings"
        )

        result = []

        # -----------------------------------------------------
        # NEW MULTI-SAMPLE FORMAT
        # -----------------------------------------------------

        if isinstance(
            embeddings,
            (list, tuple),
        ):
            for embedding in embeddings:
                try:
                    result.append(
                        self._normalize(
                            embedding
                        )
                    )
                except Exception:
                    continue

            if result:
                return result

        # -----------------------------------------------------
        # OLD SINGLE-EMBEDDING FORMAT
        # -----------------------------------------------------

        embedding = profile.get(
            "embedding"
        )

        if embedding is not None:
            try:
                result.append(
                    self._normalize(
                        embedding
                    )
                )
            except Exception:
                pass

        return result

    # =========================================================
    # SIMILARITY
    # =========================================================

    @staticmethod
    def _similarity(
        candidate: torch.Tensor,
        reference: torch.Tensor,
    ) -> float:

        candidate = candidate.reshape(-1)
        reference = reference.reshape(-1)

        if candidate.shape != reference.shape:
            return -1.0

        score = F.cosine_similarity(
            candidate.unsqueeze(0),
            reference.unsqueeze(0),
            dim=1,
        )

        return float(score.item())

    # =========================================================
    # SCORE PROFILE
    # =========================================================

    def _score_profile(
        self,
        candidate: torch.Tensor,
        profile,
    ):
        embeddings = self._get_profile_embeddings(
            profile
        )

        if not embeddings:
            return -1.0, -1

        scores = []

        for index, reference in enumerate(
            embeddings
        ):
            score = self._similarity(
                candidate,
                reference,
            )

            if score >= 0:
                scores.append(
                    (score, index)
                )

        if not scores:
            return -1.0, -1

        # -----------------------------------------------------
        # SORT HIGHEST → LOWEST
        # -----------------------------------------------------

        scores.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        # -----------------------------------------------------
        # USE TOP 3 MATCHES
        # -----------------------------------------------------

        top_scores = scores[:3]

        average_score = (
            sum(
                score
                for score, _ in top_scores
            )
            / len(top_scores)
        )

        # Keep the strongest sample index for diagnostics.
        best_score, best_index = top_scores[0]

        return average_score, best_index

    # =========================================================
    # IDENTIFY
    # =========================================================

    def identify(
        self,
        candidate_embedding,
    ):
        candidate = self._normalize(
            candidate_embedding
        )

        best_identity = "UNKNOWN"
        best_user_id = None
        best_display_name = None
        best_score = -1.0
        best_sample = -1

        # =====================================================
        # OWNER
        # =====================================================

        owner_profile = (
            self.profile_manager.get_profile(
                "OWNER"
            )
        )

        if self.profile_manager.validate_profile(
            owner_profile
        ):
            score, sample_index = (
                self._score_profile(
                    candidate,
                    owner_profile,
                )
            )

            if score > best_score:
                best_score = score
                best_identity = "OWNER"

                best_user_id = (
                    owner_profile.get(
                        "user_id",
                        "owner",
                    )
                )

                best_display_name = (
                    owner_profile.get(
                        "display_name",
                        "Owner",
                    )
                )

                best_sample = sample_index

        # =====================================================
        # AUTHORIZED USERS
        # =====================================================

        for summary in (
            self.profile_manager.list_profiles()
        ):
            if summary.get(
                "identity"
            ) != "AUTHORIZED":
                continue

            user_id = summary.get(
                "user_id"
            )

            if not user_id:
                continue

            profile = (
                self.profile_manager.get_profile(
                    "AUTHORIZED",
                    user_id,
                )
            )

            if not self.profile_manager.validate_profile(
                profile
            ):
                continue

            score, sample_index = (
                self._score_profile(
                    candidate,
                    profile,
                )
            )

            if score > best_score:
                best_score = score
                best_identity = "AUTHORIZED"
                best_user_id = user_id

                best_display_name = (
                    profile.get(
                        "display_name",
                        user_id,
                    )
                )

                best_sample = sample_index

        # =====================================================
        # THRESHOLD DECISION
        # =====================================================

        authorized = (
            best_score >= self.threshold
        )

        if not authorized:
            best_identity = "UNKNOWN"
            best_user_id = None
            best_display_name = None
            best_sample = -1

        return {
            "identity": best_identity,
            "user_id": best_user_id,
            "display_name": best_display_name,
            "authorized": authorized,
            "score": best_score,
            "threshold": self.threshold,
            "matched_sample": best_sample,
        }