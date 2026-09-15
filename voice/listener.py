import math
import time
from array import array

import speech_recognition as sr

from config.constants import (
    VOICE_PHRASE_LIMIT,
    VOICE_TIMEOUT,
)
from config.states import AssistantState
from core import app_state
from core.logger import logger
from voice.language_manager import language_manager
from voice.profile_manager import VoiceProfileManager
from voice.speaker_auth import SpeakerAuth
from voice.voice_identity import VoiceIdentity


class Listener:
    """Capture microphone input, authenticate the OWNER, and recognize speech."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.5

        self._calibrated = False

        self.last_text = ""
        self.last_time = 0.0

        self.input_level = 0

        # =========================================================
        # SPEAKER AUTHENTICATION / OWNER IDENTITY
        # =========================================================

        # Keep the existing SpeakerAuth object available.
        # It provides the SpeechBrain model and embedding generation.
        self.speaker_auth = SpeakerAuth(
            threshold=0.28
        )

        # Profile-based identity system.
        self.profile_manager = VoiceProfileManager()

        self.voice_identity = VoiceIdentity(
            self.profile_manager,
            threshold=0.28,
        )

        # OWNER-ONLY MODE
        #
        # For now, only the OWNER profile is allowed to use JARVIS.
        # Even if an AUTHORIZED profile is later present, this
        # listener will still reject it until OWNER-ONLY mode is
        # explicitly changed.
        self.owner_only = True

        self.voice_authorized = False

        self.last_voice_score = 0.0
        self.last_voice_identity = "UNKNOWN"
        self.last_voice_user_id = None
        self.last_voice_display_name = None

        # =========================================================
        # LANGUAGE
        # =========================================================

        self.last_recognition_language = (
            language_manager.get_primary_language()
        )

    # =========================================================
    # LISTEN
    # =========================================================

    def listen(self, wake_mode=False):
        """
        Listen once and return recognized text.

        wake_mode=True:
            Use primary language only for wake-word detection.

        wake_mode=False:
            Use configured multilingual recognition behavior.

        Security:
            Speaker identity is checked immediately after
            microphone capture and BEFORE speech recognition.

            In OWNER-ONLY mode, only the OWNER profile can
            continue to STT.
        """

        try:
            with self.microphone as source:

                # -------------------------------------------------
                # CALIBRATION
                # -------------------------------------------------

                if not self._calibrated:

                    logger.info(
                        "🎤 Calibrating microphone..."
                    )

                    self.recognizer.adjust_for_ambient_noise(
                        source,
                        duration=1,
                    )

                    self._calibrated = True

                    logger.info(
                        "✅ Calibration complete."
                    )

                # -------------------------------------------------
                # LISTENING
                # -------------------------------------------------

                app_state.state_machine.change(
                    AssistantState.LISTENING
                )

                logger.info(
                    "🎤 Listening..."
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=VOICE_TIMEOUT,
                    phrase_time_limit=VOICE_PHRASE_LIMIT,
                )

                self.input_level = (
                    self._calculate_audio_level(
                        audio
                    )
                )

            # =====================================================
            # OWNER VOICE IDENTITY
            # =====================================================

            logger.info(
                "🔐 Verifying OWNER voice..."
            )

            # -----------------------------------------------------
            # OWNER PROFILE CHECK
            # -----------------------------------------------------

            owner_profile = (
                self.profile_manager.get_profile(
                    "OWNER"
                )
            )

            if not self.profile_manager.validate_profile(
                owner_profile
            ):

                self.voice_authorized = False
                self.last_voice_score = 0.0
                self.last_voice_identity = "UNKNOWN"
                self.last_voice_user_id = None
                self.last_voice_display_name = None

                logger.error(
                    "❌ OWNER profile missing or invalid. "
                    "Voice command rejected."
                )

                return ""

            # -----------------------------------------------------
            # CREATE SPEAKER EMBEDDING
            # -----------------------------------------------------

            try:

                candidate_embedding = (
                    self.speaker_auth.embedding_from_audio(
                        audio
                    )
                )

            except Exception as error:

                self.voice_authorized = False
                self.last_voice_score = 0.0
                self.last_voice_identity = "UNKNOWN"
                self.last_voice_user_id = None
                self.last_voice_display_name = None

                logger.exception(
                    "Speaker embedding failed: %s",
                    error,
                )

                return ""

            if candidate_embedding is None:

                self.voice_authorized = False
                self.last_voice_score = 0.0
                self.last_voice_identity = "UNKNOWN"
                self.last_voice_user_id = None
                self.last_voice_display_name = None

                logger.warning(
                    "🚫 Could not create speaker embedding."
                )

                return ""

            # -----------------------------------------------------
            # IDENTIFY SPEAKER
            # -----------------------------------------------------

            try:

                identity_result = (
                    self.voice_identity.identify(
                        candidate_embedding
                    )
                )

            except Exception as error:

                self.voice_authorized = False
                self.last_voice_score = 0.0
                self.last_voice_identity = "UNKNOWN"
                self.last_voice_user_id = None
                self.last_voice_display_name = None

                logger.exception(
                    "Voice identity matching failed: %s",
                    error,
                )

                return ""

            # -----------------------------------------------------
            # STORE IDENTITY RESULT
            # -----------------------------------------------------

            identity = str(
                identity_result.get(
                    "identity",
                    "UNKNOWN",
                )
            ).upper()

            user_id = (
                identity_result.get(
                    "user_id"
                )
            )

            display_name = (
                identity_result.get(
                    "display_name"
                )
            )

            score = float(
                identity_result.get(
                    "score",
                    0.0,
                )
            )

            threshold = float(
                identity_result.get(
                    "threshold",
                    self.voice_identity.threshold,
                )
            )

            self.last_voice_score = score
            self.last_voice_identity = identity
            self.last_voice_user_id = user_id
            self.last_voice_display_name = display_name

            # =====================================================
            # OWNER-ONLY DECISION
            # =====================================================

            if (
                self.owner_only
                and identity == "OWNER"
            ):

                self.voice_authorized = True

                logger.info(
                    "✅ OWNER VOICE VERIFIED | "
                    "name=%s score=%.4f threshold=%.4f",
                    display_name or "Owner",
                    score,
                    threshold,
                )

            else:

                self.voice_authorized = False

                # Normalize anything that isn't OWNER into UNKNOWN
                # for the external listener state.
                if identity != "OWNER":
                    self.last_voice_identity = "UNKNOWN"

                logger.warning(
                    "🚫 VOICE REJECTED | "
                    "identity=%s score=%.4f threshold=%.4f",
                    identity,
                    score,
                    threshold,
                )

                logger.info(
                    "🔒 OWNER-ONLY MODE: "
                    "command blocked before speech recognition."
                )

                return ""

            # =====================================================
            # RECOGNITION
            # =====================================================

            logger.info(
                "🧠 Recognizing..."
            )

            result = self._recognize_audio(
                audio,
                wake_mode=wake_mode,
            )

            # Release the AudioData reference after recognition.
            audio = None

            if not result:
                return ""

            text, language = result

            text = text.strip().lower()

            if not text:
                return ""

            # =====================================================
            # UPDATE DETECTED LANGUAGE
            # =====================================================

            language_manager.set_detected_language(
                language
            )

            self.last_recognition_language = (
                language
            )

            logger.info(
                "Detected language: %s",
                language,
            )

            # =====================================================
            # DUPLICATE PROTECTION
            # =====================================================

            now = time.time()

            if (
                text == self.last_text
                and (
                    now
                    - self.last_time
                ) < 2.5
            ):

                logger.info(
                    "🔁 Duplicate command ignored: %s",
                    text,
                )

                return ""

            self.last_text = text
            self.last_time = now

            # =====================================================
            # FINAL RESULT
            # =====================================================

            logger.info(
                "Recognized [%s]: %s",
                language,
                text,
            )

            return text

        # =========================================================
        # TIMEOUT
        # =========================================================

        except sr.WaitTimeoutError:

            return ""

        # =========================================================
        # UNKNOWN SPEECH
        # =========================================================

        except sr.UnknownValueError:

            return ""

        # =========================================================
        # RECOGNITION SERVICE
        # =========================================================

        except sr.RequestError as error:

            logger.error(
                "Speech recognition service error: %s",
                error,
            )

            return ""

        # =========================================================
        # MICROPHONE
        # =========================================================

        except OSError as error:

            logger.exception(
                "Microphone error: %s",
                error,
            )

            return ""

        # =========================================================
        # OTHER
        # =========================================================

        except Exception as error:

            logger.exception(
                "Listener error: %s",
                error,
            )

            return ""

    # =========================================================
    # RECOGNITION
    # =========================================================

    def _recognize_audio(
        self,
        audio,
        wake_mode=False,
    ):
        """
        Recognize speech.

        Wake mode:
            Primary language only.

        Normal mode:
            Manual primary language or multilingual detection.
        """

        # =========================================================
        # WAKE WORD MODE
        # =========================================================

        if wake_mode:

            language = (
                language_manager.get_primary_language()
            )

            code = (
                language_manager.recognition_code()
            )

            logger.info(
                "Wake-word recognition language: %s (%s)",
                language,
                code,
            )

            text = self._recognize_with_code(
                audio,
                code,
            )

            if not text:
                return None

            return (
                text,
                language,
            )

        # =========================================================
        # MANUAL LANGUAGE MODE
        # =========================================================

        if not language_manager.is_auto_detect():

            language = (
                language_manager.get_primary_language()
            )

            code = (
                language_manager.recognition_code()
            )

            logger.info(
                "Recognition language: %s (%s)",
                language,
                code,
            )

            text = self._recognize_with_code(
                audio,
                code,
            )

            if not text:
                return None

            return (
                text,
                language,
            )

        # =========================================================
        # STRICT SINGLE-LANGUAGE MODE
        # =========================================================

        language = (
            language_manager.get_primary_language()
        )

        code = (
            language_manager.recognition_code()
        )

        logger.info(
            "Strict recognition language: %s (%s)",
            language,
            code,
        )

        try:
            text = self._recognize_with_code(
                audio,
                code,
            )

        except sr.UnknownValueError:
            logger.info(
                "Speech was not recognized as %s.",
                language,
            )
            return None

        if not text:
            return None

        text = text.strip()

        if not text:
            return None

        logger.info(
            "Strict recognition result [%s]: %s",
            language,
            text,
        )

        return (
            text,
            language,
        )

    # =========================================================
    # SCRIPT DETECTION
    # =========================================================

    @staticmethod
    def _detect_script(text):
        """Detect the dominant writing system."""

        latin = 0
        urdu = 0
        gurmukhi = 0
        devanagari = 0

        for char in text:

            codepoint = ord(char)

            # Basic Latin letters.
            if (
                0x0041
                <= codepoint
                <= 0x007A
            ):

                latin += 1

            # Arabic / Urdu.
            elif (
                0x0600
                <= codepoint
                <= 0x06FF
            ):

                urdu += 1

            # Gurmukhi / Punjabi.
            elif (
                0x0A00
                <= codepoint
                <= 0x0A7F
            ):

                gurmukhi += 1

            # Devanagari / Hindi.
            elif (
                0x0900
                <= codepoint
                <= 0x097F
            ):

                devanagari += 1

        counts = {
            "latin": latin,
            "urdu": urdu,
            "gurmukhi": gurmukhi,
            "devanagari": devanagari,
        }

        script, count = max(
            counts.items(),
            key=lambda item: item[1],
        )

        if count == 0:

            return "unknown"

        return script

    # =========================================================
    # RECOGNIZE WITH CODE
    # =========================================================

    def _recognize_with_code(
        self,
        audio,
        code,
    ):
        """Recognize audio using one language code."""

        return (
            self.recognizer.recognize_google(
                audio,
                language=code,
            )
        )

    # =========================================================
    # RECOGNIZE WITH DETAILS
    # =========================================================

    def _recognize_with_details(
        self,
        audio,
        code,
    ):
        """Return transcript and optional confidence."""

        response = (
            self.recognizer.recognize_google(
                audio,
                language=code,
                show_all=True,
            )
        )

        if not response:

            return None

        if isinstance(
            response,
            dict,
        ):

            alternatives = response.get(
                "alternative",
                [],
            )

            if not alternatives:

                return None

            best = alternatives[0]

            return {
                "text": best.get(
                    "transcript",
                    "",
                ),
                "confidence": best.get(
                    "confidence"
                ),
            }

        if isinstance(
            response,
            str,
        ):

            return {
                "text": response,
                "confidence": None,
            }

        return None

    # =========================================================
    # UNIQUE RECOGNITION CODES
    # =========================================================

    @staticmethod
    def _get_unique_recognition_codes():
        """Get unique enabled speech-recognition codes."""

        codes = (
            language_manager
            .enabled_recognition_codes()
        )

        unique = []

        for code in codes:

            if code not in unique:

                unique.append(
                    code
                )

        return unique

    # =========================================================
    # AUDIO LEVEL
    # =========================================================

    @staticmethod
    def _calculate_audio_level(audio):
        """Estimate RMS level of captured audio."""

        raw = audio.get_raw_data()

        if not raw:

            return 0

        width = audio.sample_width

        try:

            if width == 1:

                samples = array(
                    "B",
                    raw,
                )

                if not samples:

                    return 0

                values = [
                    sample - 128
                    for sample in samples
                ]

                max_amplitude = 128

            elif width == 2:

                samples = array(
                    "h"
                )

                samples.frombytes(
                    raw
                )

                if not samples:

                    return 0

                values = samples
                max_amplitude = 32768

            elif width == 4:

                samples = array(
                    "i"
                )

                samples.frombytes(
                    raw
                )

                if not samples:

                    return 0

                values = samples
                max_amplitude = 2147483648

            else:

                return 0

            mean_square = (
                sum(
                    sample * sample
                    for sample in values
                )
                / len(values)
            )

            rms = math.sqrt(
                mean_square
            )

            # Amplify normalized RMS into a useful 0-100 range.
            level = (
                rms
                / max_amplitude
                * 100
                * 10
            )

            return int(
                max(
                    0,
                    min(
                        level,
                        100,
                    ),
                )
            )

        except Exception:

            return 0